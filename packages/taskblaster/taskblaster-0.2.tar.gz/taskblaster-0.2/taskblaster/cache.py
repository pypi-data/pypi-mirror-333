from collections.abc import Mapping
from pathlib import Path

from taskblaster import TBReadOnlyRepository
from taskblaster.conflict import ConflictInfo, ConflictState
from taskblaster.encodedtask import EncodedTask
from taskblaster.entry import Entry
from taskblaster.future import Future
from taskblaster.registry import Missing


class FileCache(Mapping):
    def __init__(self, *, directory, registry, json_protocol):
        self.directory = Path(directory)
        self._absdir = self.directory.absolute()

        self.registry = registry
        self.json_protocol = json_protocol
        self.read_only = registry.read_only

    def entry(self, name) -> Entry:
        if not self.registry.contains(name):
            raise KeyError(name)
        directory = self.directory / name
        return Entry(directory, self.json_protocol, read_only=self.read_only)

    def __len__(self):
        return self.registry.index.count()

    def __iter__(self):
        return (indexnode.name for indexnode in self.registry.index.nodes())

    def serialized_input(self, name: str) -> str:
        try:
            return self.registry.inputs[name]
        except KeyError:
            raise Missing(name)

    def unresolved_input(self, name: str) -> dict:
        return self.json_protocol.load_inputs_without_resolving_references(
            self.serialized_input(name), name
        )[0]

    def encoded_task(self, name: str) -> EncodedTask:
        serialized_input = self.serialized_input(name)

        assert serialized_input is not None
        serialized_errorhandlers = self.registry.handlers.get(name, '[]')

        obj = self.json_protocol.load_inputs_without_resolving_references(
            serialized_input, name
        )

        (target, target_kwargs), refs = obj
        parents = tuple(sorted({ref.name for ref in refs}))

        assert serialized_input is not None

        return EncodedTask(
            name=name,
            serialized_input=serialized_input,
            parents=parents,
            tags=self.registry.resources.get_tags(name),
            source=self.registry.sources.get(name),  # should be more strict
            has_record=self.registry.has_records.get(name, False),
            serialized_handlers=serialized_errorhandlers,
        )

    def __getitem__(self, name) -> Future:
        try:
            encoded_task = self.encoded_task(name)
        except Missing:
            raise KeyError(name)
        return Future(encoded_task, self)

    def __repr__(self):
        return (
            f'{type(self).__name__}({self.directory}, '
            f'[{self.registry.index.count()} entries])'
        )

    def add_or_update_task(
        self,
        encoded_task: EncodedTask,
        *,
        clobber_implicit_deps: bool,
        force_overwrite=False,
    ):
        if self.read_only:
            raise TBReadOnlyRepository

        name = encoded_task.name
        if self.registry.contains(name):
            previous_task = self.encoded_task(name)

            previous_indexnode = self.registry.index.node(name)
            inputs_same = (
                encoded_task.serialized_input == previous_task.serialized_input
            )

            if inputs_same:
                self.registry.clear_conflict(name)
            else:
                if not previous_indexnode.state.is_pristine:
                    # We could punt the state back to new and overwrite,
                    # but for now the user will have to unrun manually.
                    from taskblaster.clobber import (
                        can_patch_implicit_dependencies,
                        dangerously_clobber_implicit_dependencies,
                    )

                    conflict = self.registry.conflict_info(name)

                    new_input = encoded_task.serialized_input
                    # Update the conflict string, and if conflict was
                    # unresolved, make it conflict:
                    if new_input != conflict.conflicting_input:
                        conflict = ConflictInfo(
                            ConflictState.conflict,
                            conflicting_input=new_input,
                        )
                        self.registry.update_conflict(name, conflict)

                    if clobber_implicit_deps:
                        if can_patch_implicit_dependencies(
                            previous_task.serialized_input,
                            new_input,
                        ):
                            # We avert the conflict here by overwriting
                            # the old inputs:
                            dangerously_clobber_implicit_dependencies(
                                self,
                                encoded_task,
                            )
                            # Uhh should we not wipe the conflict here, if
                            # we did this succcessfully and there is no other
                            # conflicting info?
                            indexnode = self.registry.index.node(name)
                            return 'update', indexnode

                    return conflict.state.name, previous_indexnode

                force_overwrite = True

        action, indexnode = self.registry.add_or_update(
            encoded_task, force_overwrite=force_overwrite
        )

        assert action in {'add', 'update', 'have'}
        return action, indexnode

    def add_or_update(
        self,
        encoded_task: EncodedTask,
        *,
        force_overwrite=False,
        clobber_implicit_deps: bool = False,
    ):
        if self.read_only:
            raise TBReadOnlyRepository

        action, indexnode = self.add_or_update_task(
            encoded_task,
            force_overwrite=force_overwrite,
            clobber_implicit_deps=clobber_implicit_deps,
        )
        meta_action = self.registry.add_or_update_metadata(encoded_task)
        return action, meta_action, indexnode

    def load_inputs_and_resolve_references(self, name: str):
        serialized_input = self.registry.inputs[name]
        return self.json_protocol._actually_load(
            self, serialized_input, self.directory / name
        )

    def find_ready(self, required_tags=None, supported_tags=None):
        """Return a task which is ready to run right now.

        Returns None if no such task is found.
        """

        # TODO: Change to raise NoSuchTask() if there is no task.
        # Also: We need to find things only with the right kind of worker.
        # What if we depend on things in other directories?  We need to
        # be able to run those, too.
        #
        # Probably we should also be able to limit searching to a particular
        # directory, but that doesn't always work well since dependencies
        # often reside in different directories
        return self.registry.find_ready(required_tags, supported_tags)

    def delete_nodes(self, names):
        if self.read_only:
            raise TBReadOnlyRepository
        # XXX must work if registry/tree are inconsistent.
        import shutil

        entries = [self.entry(name) for name in names]
        cachedir = self._absdir.resolve()

        for entry in entries:
            assert cachedir in entry.directory.parents

        self.registry.remove_nodes(names)

        for entry in entries:
            entry.delete()

            directory = entry.directory.resolve()
            # Let's be a little bit paranoid before rmtreeing:
            assert 'tree' in directory.parent.parts
            assert self.directory.is_absolute()
            assert self.directory in directory.parents
            if directory.exists():
                shutil.rmtree(directory)
            remove_empty_dirs(cachedir, entry.directory)


def remove_empty_dirs(root, directory):
    """Remove directory and all empty parent directories up to root."""
    if root not in directory.parents:
        raise RuntimeError(f'Refusing to delete dirs outside {root}!')

    for parent in directory.parents:
        if parent == root:
            break
        try:
            parent.rmdir()
        except OSError:  # directory not empty
            break


class DirectoryConflict(OSError):
    pass
