from __future__ import annotations

import importlib
import runpy
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List

import taskblaster as tb
from taskblaster import TBReadOnlyRepository, TBUserError
from taskblaster.cache import FileCache
from taskblaster.future import Future
from taskblaster.registry import Registry
from taskblaster.runner import Runner
from taskblaster.state import State
from taskblaster.storage import JSONProtocol
from taskblaster.tree import Tree
from taskblaster.util import get_task_actions


def T(t: str) -> int:
    """Convert string to seconds. Borrowed from myqueue"""
    return {'s': 1, 'm': 60, 'h': 3600, 'd': 24 * 3600}[t[-1]] * int(t[:-1])


@dataclass
class WorkerSpecification:
    name: str | None = None
    tags: set[str] = field(default_factory=set)
    required_tags: set[str] = field(default_factory=set)
    resources: str | None = None
    max_tasks: int | None = None
    subworker_size: int | None = None
    subworker_count: int | None = None
    wall_time: float | None = None

    @classmethod
    def from_workerconfig(cls, config_dct):
        worker_specs = {}
        for name, dct in config_dct.items():
            wall_time = dct.get('wall_time')
            if wall_time is not None:
                wall_time = T(wall_time)

            worker_specs[name] = cls(
                name=name,
                tags=set(dct.get('tags', [])),
                required_tags=set(dct.get('required_tags', [])),
                resources=dct.get('resources'),
                wall_time=wall_time,
            )

        return worker_specs

    def get_compatible_tags(self):
        compatible_tags = self.required_tags | self.tags
        if self.name is not None:
            compatible_tags.add(self.name)
        return compatible_tags

    def headers(self) -> list[str]:
        required_tags = sorted(self.required_tags)
        compatible_tags = sorted(self.get_compatible_tags())
        return [
            f'Worker class: {self.name or "—"}',
            f'Required tags: {" ".join(required_tags) or "—"}',
            f'Supported tags: {" ".join(compatible_tags) or "—"}',
        ]

    def asdict(self) -> dict:
        return asdict(self).copy()

    def merge(self, other):
        mydict = self.asdict()
        otherdict = other.asdict()

        # Tags combine inclusively:
        mydict['tags'] |= otherdict.pop('tags')
        mydict['required_tags'] |= otherdict.pop('required_tags')

        # Other attributes are just overwrite-if-not-None:
        for name, value in otherdict.items():
            if value is not None:
                mydict[name] = value

        return WorkerSpecification(**mydict)

    def description(self):
        dct = self.asdict()

        def jointags(tags):
            return ' '.join(tags) if tags else '—'

        # Slightly nicer strings for printing:
        dct['tags'] = jointags(self.tags)
        dct['required_tags'] = jointags(self.required_tags)
        dct['resources'] = repr(dct['resources'])

        return '\n    '.join(
            [f'{name}: {value}' for name, value in dct.items()]
        )


def read_resource_file(path):
    if not path.exists():
        return {}

    try:
        namespace = runpy.run_path(str(path))
    except Exception as err:
        # This is a user error, but in this particular case the user
        # will definitely want to see the stack trace.
        raise tb.TBUserError(f'Could not load resources from {path}') from err

    try:
        resources_dict = namespace['resources']
    except KeyError:
        # Error message should be made more informative once syntax is stable
        example = 'resources = {}'
        raise tb.TBUserError(
            f'Resource file {path} exists but does not contain at least '
            f'"{example}"'
        )

    return resources_dict


class Repository:
    _tasks_module_name = 'tasks.py'
    _tree_name = 'tree'
    _registry_name = 'registry.db'
    _magic_dirname = '.taskblaster'
    _py_filename = 'pymodule'
    _resource_filename = 'resources.py'
    _read_only_marker = 'READONLY'

    class RepositoryError(Exception):
        pass

    def __init__(self, root, usercodec=None, read_only=False):
        self.root = root.resolve()

        override_read_only = (self.magicdir / self._read_only_marker).exists()
        read_only = read_only or override_read_only

        self.read_only = read_only
        self.registry = Registry(self.registry_path, read_only=read_only)
        self.cache = FileCache(
            directory=self.tree_path,
            registry=self.registry,
            json_protocol=JSONProtocol(self.tree_path, usercodec),
        )

        # When testing within a single process, it is useful to have a
        # namespace of ready-made tasks without having to import from files.
        self._tasks = {}

        from taskblaster.runner import define

        self._tasks['define'] = define

    def worker_start_hook(self):
        pass

    def worker_finish_hook(self):
        pass

    def get_resources(self):
        dct = read_resource_file(self.resource_path)
        return WorkerSpecification.from_workerconfig(dct)

    def mpi_world(self):
        from taskblaster.parallel import SerialCommunicator

        return SerialCommunicator()

    def context_class(self):
        return tb.WorkerContext

    @property
    def magicdir(self):
        return self.root / self._magic_dirname

    @property
    def registry_path(self):
        return self.magicdir / self._registry_name

    @property
    def tree_path(self):
        return self.root / self._tree_name

    @property
    def resource_path(self):
        return self.root / self._resource_filename

    @property
    def project_pythonpath(self):
        # (To be added to sys.path in CLI startup when running tb commands.)
        return self.root / 'src'

    def __enter__(self):
        # A process (e.g. this process) is allowed to hold the lock more
        # than once.  This is useful because we can perform actions
        # that require locking without needing to check whether we are
        # already holding the lock.
        #
        # Thus, we keep a count of the number of times we have acquired
        # the lock.
        #
        # The lock is not thread safe, but it is safe wrt. other (external)
        # processes.
        self.registry.conn.__enter__()
        return self

    def __exit__(self, *args):
        self.registry.conn.__exit__(*args)

    def __repr__(self):
        return f'<Repository(root={self.root})>'

    def tree(self, directories=None, **kwargs):
        return Tree(self, directories=directories, **kwargs)

    def import_task_function(self, taskname):
        if taskname in self._tasks:
            return self._tasks[taskname]

        tokens = taskname.rsplit(':', 1)
        if len(tokens) == 1:
            tokens = taskname.rsplit('.', 1)

        if len(tokens) == 2:
            module, funcname = tokens
            func = importlib.import_module(module)
            for name in funcname.split('.'):
                func = getattr(func, name)
            return func

        namespace = self.import_tasks()
        try:
            return namespace[taskname]
        except KeyError:
            raise tb.TBUserError(
                f'Could not import task with target: {taskname}'
            )

    def import_tasks(self) -> Dict[str, Any]:
        # We need some way of guaranteeing that tasks cannot invoke
        # malicious functions.
        #
        # Right now we allow loading from any function named via
        # import path, so that can execute anything.
        #
        # Maybe ASR can have a way to point to 'valid' things.
        try:
            # we do str() for mypy
            target = str(self.tasks_module)
            return runpy.run_path(target, run_name=target)
        except FileNotFoundError:
            return {}
        #    raise self.RepositoryError('No tasks defined.  Define tasks in '
        #                               f'{self.tasks_module}')

    @property
    def tasks_module(self) -> Path:
        return self.root / self._tasks_module_name

    @classmethod
    def create(
        cls, root, modulename='taskblaster.repository', exists_ok=False
    ) -> 'Repository':
        root = root.resolve()

        def trouble(msg):
            raise cls.RepositoryError(msg)

        try:
            module = importlib.import_module(modulename)
        except ModuleNotFoundError:
            trouble(f'Specified module "{modulename}" must exist')

        try:
            tb_init_repo = module.tb_init_repo
        except AttributeError:
            trouble(
                f'Specified module "{modulename}" '
                'does not implement a tb_init_repo(root) '
                'function or class'
            )

        magic_dir = root / cls._magic_dirname
        magic_dir.mkdir(parents=True, exist_ok=True)

        modulefile = magic_dir / cls._py_filename
        modulefile.write_text(f'{modulename}\n')

        registry = magic_dir / cls._registry_name

        if not exists_ok and registry.exists():
            trouble(f'Already exists: {registry}')
        registry.touch()

        tree_path = root / cls._tree_name
        tree_path.mkdir(exist_ok=True)
        repo = tb_init_repo(root)
        return repo

    @classmethod
    def find_root_directory(cls, directory='.'):
        directory = Path(directory).resolve()
        for root in (directory, *directory.parents):
            registry_location = root / cls._magic_dirname / cls._registry_name
            if registry_location.exists():
                return root

        raise cls.RepositoryError(
            f'No registry found in {directory} or parents. '
            'Run tb init MODULE to initialize empty repository here.'
        )

    @classmethod
    def find(cls, directory='.', read_only=False) -> 'Repository':
        root = cls.find_root_directory(directory)
        pymodulefile = root / cls._magic_dirname / cls._py_filename
        pymodulename = pymodulefile.read_text().strip()
        try:
            pymodule = importlib.import_module(pymodulename)
        except ModuleNotFoundError:
            raise TBUserError(
                f'Cannot find module {pymodulename}, which is '
                'current module of this repo. Please make sure '
                'it is in the import path.'
            )

        tb_init_repo = pymodule.tb_init_repo

        # Do not force old implementations of tb_init_repo to pass
        # the read_only argument.
        if read_only:
            repo = tb_init_repo(root, read_only=True)
        else:
            repo = tb_init_repo(root)

        if read_only:
            # repo might override read_only attribute, so it is ok
            # to ask for read_only False database, and get a read_only
            # True database. It will just fail in later stages, when
            # one attempts to do something.
            assert repo.read_only

        if not isinstance(repo, cls):
            raise cls.RepositoryError(
                f'{pymodulename}.tb_init_repo did not return'
                ' a repository object.'
            )
        return repo

    def plugin_pymodule(self):
        return (self.magicdir / self._py_filename).read_text().strip()

    def info(self) -> List[str]:
        have_tasks = self.tasks_module.is_file()
        taskfile = str(self.tasks_module)

        if not have_tasks:
            taskfile += ' (not created)'

        index = self.cache.registry.index

        lenstring = 'entry' if index.count() == 1 else 'entries'

        pymodulename = self.plugin_pymodule()
        pymodule = importlib.import_module(pymodulename)

        resources = self.get_resources()
        resource_string = str(self.resource_path)

        if not self.resource_path.is_file():
            resource_string += ' (not created)'
        else:
            resource_string += f' ({len(resources)} worker classes)'

        return [
            f'Module:     {pymodulename}',
            f'Code:       {pymodule.__file__}',
            f'Root:       {self.root}',
            f'Tree:       {self.cache.directory}',
            f'Registry:   {self.registry_path} ({index.count()} {lenstring})',
            f'Pythonpath: {self.project_pythonpath}',
            f'Tasks:      {taskfile}',
            f'Resources:  {resource_string}',
            f'Read only:  {self.read_only}',
        ]

    def runner(self, **kwargs):
        if self.read_only:
            raise self.RepositoryError(
                'Cannot create runner on a readonly repository'
            )
        return Runner(self, directory=self.cache.directory, **kwargs)

    def listing(self, columns, fromdir):
        from taskblaster.listing import ls_listing

        return ls_listing(
            columns=columns,
            cache=self.cache,
            fromdir=fromdir,
            treedir=self.tree_path,
        )

    def graph(self, tree):
        from taskblaster.util import tree_to_graphviz_text

        tree = self.tree(tree)
        txt = tree_to_graphviz_text(tree)
        print(txt)

    def _view(self, tree):
        from taskblaster.view import view_node

        for node in self.tree(tree).nodes():
            view_node(self, node)

    def rename_import_path(self, tree, old, new):
        if self.read_only:
            raise self.RepositoryError(
                'Cannot perform rename-import-path to a readonly repository'
            )

        registry = self.cache.registry
        to_be_patched = []

        for indexnode in self.tree(tree).nodes():
            encoded_task = self.cache.encoded_task(indexnode.name)
            node = self.cache.json_protocol.deserialize_node(
                encoded_task.serialized_input, encoded_task.name
            )

            if node.target == old:
                to_be_patched.append((encoded_task, node, indexnode.state))

        def rename_fcn():
            for encoded_task, node, state in to_be_patched:
                name = encoded_task.name

                buf = self.cache.json_protocol.serialize_node(
                    tb.Node(new, node.kwargs), name
                )

                newnode = encoded_task.replace(serialized_input=buf)

                # We re-serialize the kwargs, and it should get the same
                # string afterwards except for the one changed path.
                # Let's do a sanity check:
                assert (
                    encoded_task.serialized_input.replace(old, new, 1)
                    == newnode.serialized_input
                )

                registry.inputs[name] = newnode.serialized_input

                # If the task is associated with a directory, we must update
                # the input in directory as well.
                # But this file update is not transactional.  If we want it
                # to be, we should try to write down transactionally
                # that we intend to perform this update so that we can
                # carry it out later, should it not be possible now.
                if indexnode.state.have_data:
                    entry = self.cache.entry(name)
                    entry.inputfile.write_text(newnode.serialized_input)
                print(f'Renamed import path for {name}.')
            print(f'Renamed {len(to_be_patched)} task import paths.')

        # XXX improve naming here.
        return [things[0].name for things in to_be_patched], rename_fcn

    def view(self, tree, action=None, relative_to=None):
        if action is None:
            return self._view(tree)
        else:
            return self._run_action(
                tree, action=action, relative_to=relative_to
            )

    def _run_action(self, tree, action, relative_to):
        results = []
        for indexnode in self.tree(tree, relative_to=relative_to).nodes():
            name = indexnode.name
            encoded_task = self.cache.encoded_task(name)
            node = self.cache.json_protocol.deserialize_node(
                encoded_task.serialized_input, name
            )

            function = self.import_task_function(node.target)
            if indexnode.state == State.done:
                # This will take time even for tasks that do not have this
                # action -- we must load their return value before we know
                # if they have the action.  How do we feel about this?
                #
                # We could instead determine the import part and from that
                # see if the action exists without decoding the output.
                output = self.cache.entry(name).output()
            else:
                output = None

            actions = get_task_actions(function, output)

            if action not in actions:
                print(f'<task "{name}" does not have action "{action}">')
                continue

            actionfunc = actions[action]
            future = Future(encoded_task, self.cache)
            record = tb.TaskView(indexnode=indexnode, future=future)
            results.append(actionfunc(record))

        return results

    def run_worker(self, tree=None, name='worker', greedy=False, rules=None):
        if self.read_only:
            raise self.RepositoryError(
                'Cannot run workers on a readonly repository'
            )
        from taskblaster.parallel import choose_subworkers
        from taskblaster.worker import Worker

        if rules is None:
            rules = WorkerSpecification()

        world = self.mpi_world()
        subworker_size, subworker_count = choose_subworkers(
            size=world.size,
            subworker_count=rules.subworker_count,
            subworker_size=rules.subworker_size,
        )

        comm = world.split(subworker_size)
        subworker_group = world.rank // subworker_size
        subworker_id = f'{name}-{subworker_group}/{subworker_count}'

        runnable = {State.queue, State.partial, State.new}
        if tree:
            tree = self.tree(tree, states=runnable)

            def find_tasks():
                # XXX We need to base this on a query instead of this hack
                # Here we try to discard tasks that do not have the right
                # tags.

                while True:
                    found = False
                    if greedy:
                        search_fun = tree.nodes
                    else:
                        search_fun = tree.nodes_topological
                    for indexnode in search_fun():
                        # The nodes_topological() iterator may have outdated
                        # information, so we need to refresh everything we see:
                        indexnode = self.registry.index.node(indexnode.name)

                        if indexnode.state not in runnable:
                            continue

                        if indexnode.awaitcount != 0:
                            continue

                        tags = self.registry.resources.get_tags(indexnode.name)
                        if not worker._tags_compatible(tags):
                            # XXX beware of repeated looping over the same
                            # tasks!  This should probably be changed
                            # to a database query of some kind.
                            continue

                        # Do not run frozen tasks.
                        if self.registry.frozentasks.get_tags(indexnode.name):
                            continue

                        found = True
                        yield indexnode
                    if not found:
                        break

            selection = find_tasks()
        else:
            selection = None

        # Names are a bit illogical, meaning of "worker name" differs below
        worker = Worker(
            repo=self,
            name=subworker_id,
            myqueue_id=name,
            comm=comm,
            selection=selection,
            rules=rules,
        )
        worker.main()

    def run_workflow_script(
        self,
        script,
        script_name='workflow',
        **kwargs,
    ):
        import importlib
        import runpy

        if self.read_only:
            raise TBReadOnlyRepository

        script = Path(script)

        try:
            importpath = script.resolve().relative_to(self.project_pythonpath)
        except ValueError:
            try:
                namespace = runpy.run_path(script)
            except Exception as e:
                raise e from None
        else:
            module = '.'.join(importpath.with_suffix('').parts)
            namespace = vars(importlib.import_module(module))

        if script_name not in namespace:
            raise self.RepositoryError(
                f'When running `tb workflow {script}`, the {script} must '
                'contain `def workflow(rn)`.'
            )
        workflow = namespace[script_name]

        rn = self.runner(**kwargs)
        workflow(rn)


def tb_init_repo(root):
    return Repository(root)
