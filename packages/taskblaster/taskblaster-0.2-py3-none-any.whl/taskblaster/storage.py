import inspect
import json
import typing
from abc import ABC, abstractmethod
from pathlib import Path

from taskblaster import (
    Accessor,
    BoundWorkflowSpecification,
    JSONCodec,
    Node,
    Reference,
)
from taskblaster.encodedtask import EncodedTask
from taskblaster.encoding import decode_object, encode_object
from taskblaster.namedtask import Task


class NullCodec(JSONCodec):
    def decode(self, dct):
        return dct

    def encode(self, obj):
        clsname = type(obj).__name__
        raise TypeError(f'No encoding rule for type {clsname}: {obj}')


class ExtensibleCodec(JSONCodec):
    def __init__(self, usercodec):
        self.usercodec = usercodec

    def encode(self, obj):
        if hasattr(obj, 'tb_encode'):
            return encode_object(obj)
        if callable(obj):
            if hasattr(obj, '__self__') and not inspect.isclass(obj.__self__):
                from taskblaster import TBUserError

                raise TBUserError('Unreferenced instance methods not allowed.')
            spacer = '.' if obj.__qualname__ == obj.__name__ else ':'
            return obj.__module__ + spacer + obj.__qualname__

        return self.usercodec.encode(obj)

    def decode(self, dct):
        if '__tb_enc__' in dct:
            return decode_object(dct)
        return self.usercodec.decode(dct)


class JSONProtocol:
    def __init__(self, root, usercodec=None):
        if usercodec is None:
            usercodec = NullCodec()

        self.root = root
        self.codec = ExtensibleCodec(usercodec)

    def decode_workflow(self, workflowdata):
        # using name here is a little bit questionable I think
        obj, refs = self.load_inputs_without_resolving_references(
            workflowdata.serialized_input, workflowdata.name
        )
        return obj, refs

    def encode_task(self, task: Task) -> EncodedTask:
        # The input dictionary contains Futures, References etc., which
        # have a reference to the cache and hence cannot be directly
        # serialized.
        #
        # We want to obtain those as "packed" quantities that can
        # be serialized.  We serialize them using a hook which packs them
        # (thus delegating to JSON the responsibility of object tree
        #  traversal) and then we load them again, at which point
        # the inter-task dependencies are "packed" as data.
        serialized_input = self.serialize_node(task.node, task.name)
        return self.load_encoded_task(
            serialized_input=serialized_input,
            name=task.name,
            source=task.source,
            has_record=task.has_record,
            tags=task.tags,
            serialized_handlers=self.serialize(task.error_handlers, task.name),
        )

    def serialize_node(self, node: Node, name: str) -> str:
        return self.serialize_inputs([node.target, node.kwargs], name)

    def deserialize_node(self, serialized_input: str, name: str) -> Node:
        (target, target_kwargs), refs = (
            self.load_inputs_without_resolving_references(
                serialized_input, name
            )
        )
        # assert set(self.parents) == {ref.name for ref in refs}
        return Node(target, target_kwargs)

    def load_encoded_task(self, serialized_input: str, name: str, **kwargs):
        obj, refs = self.load_inputs_without_resolving_references(
            serialized_input, name
        )
        target, target_kwargs = obj
        encoded_task = EncodedTask(
            name=name,
            serialized_input=serialized_input,
            parents=tuple(sorted({ref.name for ref in refs})),
            **kwargs,
        )
        assert encoded_task.serialized_input == serialized_input
        return encoded_task

    def serialize_inputs(self, obj: typing.Any, name) -> str:
        # The taskblaster caching mechanism uses hashes of serialized objects.
        # This is the function which serializes those things.  We should be
        # quite careful that this doesn't change behaviour.
        #
        # Note that keys are sorted so equal dictionaries will hash equally.

        outputencoder = self.outputencoder(self.root / name)
        return json.dumps(
            obj,
            default=outputencoder.encode_and_pack_references,
            sort_keys=True,
        )

    def load_inputs_without_resolving_references(self, buf, name):
        # Workflow inputs
        directory = self.root / name
        outputencoder = self.outputencoder(directory)
        decoder = NodeDecoder(outputencoder.decode)
        obj = json.loads(buf, object_hook=decoder.decode)
        return obj, decoder.references

    def serialize(self, obj, name) -> str:
        outputencoder = self.outputencoder(self.root / name)
        return outputencoder.dumps(obj=obj)

    def loads_task_buf(self, buf: str, name):
        """Used to load and decode any taskblaster file in entry."""
        outputencoder = self.outputencoder(self.root / name)
        return outputencoder.loads(buf)

    def _actually_load(self, cache, jsontext, directory):
        outputencoder = self.outputencoder(directory)
        unpacker = ReferenceDecoder(outputencoder.decode, cache)
        name, namespace = json.loads(jsontext, object_hook=unpacker.decode)

        # The commented code below decides how we hash an input.
        #  * First we hash the text of the inputfile.
        #
        #  * Then we decode the references inside the inputfile.  When doing
        #    so, the ReferenceDecoder remembers the hashes of all the refs
        #    it sees.  This gives us a {name: digest} mapping for all the refs,
        #
        #  * Then we hash the {name: digest} mapping
        #
        #  * Finally we combine the inputfile hash and the refmap hash,
        #    which is then the full inputhash which will change if any
        #    names or dependency digests should change.
        #
        # This logic is relatively essential so it should probably not
        # be nearly as "buried" as is the case here.

        # digestmap = {
        #    name: digest.long for name, digest in unpacker.name2digest.items()
        # }
        # digestmap_text = json.dumps(digestmap, sort_keys=True)
        # digestmap_digest = mkhash(digestmap_text.encode('ascii'))
        # final_digest = mkhash(
        #    (json_digest + digestmap_digest).encode('ascii'))
        return name, namespace

    def outputencoder(self, directory):
        return OutputEncoding(self.codec, self.root, directory)


class BaseNodeDecoder(ABC):
    """Helper class to determine dependencies while reading JSON.

    Since dependencies (input "kwargs") can be arbitrarily nested,
    determining the dependencies requires complicated looping and
    type checking.

    This class implements a JSON hook which, whenever it reads a
    dependency, stores it.  That way, the JSON read loop
    takes care of the complicated looping, and we build the
    dependencies as a side effect when loading.

    That is what this class implements.
    """

    def __init__(self, decode):
        self._decode = decode
        self.references = []

    def decode(self, dct):
        if dct.get('__tb_type__') == 'ref':
            name = dct['name']
            index = dct['index']
            ref = self.decode_reference(name, index)
            self.references.append(ref)
            return ref

        return self._decode(dct)

    @abstractmethod
    def decode_reference(self, name, index): ...


class NodeDecoder(BaseNodeDecoder):
    def decode_reference(self, name, index):
        return Reference(name, index)


class ReferenceDecoder(BaseNodeDecoder):
    def __init__(self, decode, cache):
        super().__init__(decode)
        self.cache = cache

    def decode_reference(self, name, index):
        entry = self.cache.entry(name)
        if index is None:
            raise RuntimeError('Index is None!')

        value = entry.output()
        assert isinstance(index, list)
        return Accessor.accessor_index(value, index)


class OutputEncoding:
    """Helper for passing files between tasks via JSON encoding/decoding.

    We don't want to persistently save absolute paths because they
    become wrong if anything is moved.  But we are okay with saving
    a reference such as "myfile.dat".  When loading the file (and
    for passing result objects to other tasks), the file should then
    be resoved relative to the location of the original task.

    For example suppose we have cachedir/mytask-12345/myfile.dat .

    The task returns Path('myfile.dat') which we serialize as myfile.dat.
    That way if we rename/move cachedir or mytask-12345, the information
    which we stored does not become wrong.

    Only at runtime when we load the resultfile do we evaluate myfile
    inside whatever cachedir it was loaded from – at that point it becomes
    an absolute path.

    Note also how the value of that path will not be used for any hashes
    or equality checks, since we track identity through the dependency graph.
    """

    def __init__(self, codec, root, directory):
        self.codec = codec
        self.root = root
        # XXX get rid of .absolute()
        self.directory = directory.absolute()

    def decode(self, dct):
        tbtype = dct.get('__tb_type__')
        if tbtype is None:
            return self.codec.decode(dct)
        elif tbtype == 'Path':
            return self._decode_path(dct)

        raise RuntimeError(f'bad tbtype={tbtype!r}')

    def encode(self, obj):
        if isinstance(obj, Path):
            return self._encode_path(obj)
        return self.codec.encode(obj)

    def loads(self, jsontext):
        return json.loads(jsontext, object_hook=self.decode)

    def dumps(self, obj):
        # sort keys or not?  For consistency with hashable inputs,
        # we could sort the keys.  But we don't need to, because this
        # is for storing outputs.  We'll sort them.
        return json.dumps(obj, default=self.encode, sort_keys=True)

    def encode_and_pack_references(self, obj, _recursions=[0]):
        # If the encoder also ends up encoding its dependencies'
        # dependencies, then that's bad and we have a problem.
        # This is a little check that'll fail if this is called
        # recursively:
        assert _recursions[0] == 0
        _recursions[0] += 1

        try:
            if isinstance(obj, BoundWorkflowSpecification):
                obj = obj.resolve_reference()
            if hasattr(obj, '_tb_pack'):
                return obj._tb_pack()
        finally:
            _recursions[0] -= 1
        return self.encode(obj)

    def _encode_path(self, path):
        if '..' in path.parts:
            # (Should this be user error?  Let's be nasty about it though)
            raise RuntimeError('Refusing to encode path with ".." in it')

        if path.is_absolute():
            # We only want to encode the part after TB root:
            relpath = path.relative_to(self.root)

            # Use magic string '//' for "absolute" TB paths here:
            path_string = f'//{relpath}'
        else:
            path_string = str(path)
        return {'__tb_type__': 'Path', 'path': path_string}

    def _decode_path(self, dct):
        assert set(dct) == {'__tb_type__', 'path'}
        # Should we require that the path is relative?
        path_string = dct['path']
        if path_string.startswith('//'):
            path = self.root / path_string[2:]
        else:
            path = self.directory / dct['path']

        if '..' in path.parts:
            raise RuntimeError('Refusing to decode dangerous ".." path')

        return path
