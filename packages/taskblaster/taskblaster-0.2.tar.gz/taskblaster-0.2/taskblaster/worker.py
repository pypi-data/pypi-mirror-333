from __future__ import annotations

import time
import traceback
from datetime import datetime

from taskblaster import (
    ENTRY_BRANCH,
    Node,
    Reference,
    TaskBlasterInterrupt,
    TBUserError,
    WardenPanic,
    create_record_for_task,
)
from taskblaster.abc import ExceptionData
from taskblaster.entry import Entry
from taskblaster.errorhandlers import Warden
from taskblaster.namedtask import Task
from taskblaster.parallel import SerialCommunicator
from taskblaster.registry import Missing
from taskblaster.runner import Runner
from taskblaster.state import State
from taskblaster.util import workdir


class Panic(Exception):
    pass


def pop_special_kwargs(kwargs):
    special_kwargs = [
        '__tb_record__',
        '__tb_implicit__',
        '__tb_external__',
        '__tb_implicit_remove__',
    ]
    for kwarg in special_kwargs:
        kwargs.pop(kwarg, None)


def run_dynamical_init(rn, kwargs, function, init_ref: Reference, source: str):
    # On purpose not taking care of implicit remove for compatibility
    implicit_remove = kwargs.get('__tb_implicit_remove__', [])

    result_tasks = kwargs.pop('__tb_result_tasks__')
    from collections import defaultdict

    result_task_dct = defaultdict(dict)
    implicit_remove_dct = defaultdict(dict)
    from taskblaster.util import pattern_match

    def filter_tasks(task):
        task.add_implicit_dependency(init_ref, remove=False)
        relname = rn.relative_to(task.name)
        for result_task, pattern in result_tasks.items():
            if not pattern_match(relname, pattern):
                continue
            result_task_dct[result_task][relname] = Reference(task.name)
            for name, ref in task.node.kwargs.get(
                '__tb_implicit_remove__', []
            ):
                implicit_remove_dct[result_task][name] = name, ref

    try:
        pop_special_kwargs(kwargs)
        generator = function(**kwargs)
    except TypeError:
        print(
            'Inconsistent call signature.'
            f'Task did not accept kwargs {kwargs.keys()}.'
        )
        raise
    finished = True

    # XXX We set the source one level too high
    # We should get the source like this:
    # source = rn.get_full_name('')

    for name, wf in generator:
        if hasattr(wf, '_is_tb_workflow') and wf._is_tb_workflow:
            subrn = rn.with_subdirectory(name)
            bound_workflow = subrn.run_workflow(
                wf,
                callback=filter_tasks,
                add_workflows_to_registry=False,
                source=source,
            )
            finished &= bound_workflow.finished
        else:
            taskname = rn.get_full_name(name)
            task = Task(
                taskname,
                Node(wf.target, wf.kwargs),
                branch=ENTRY_BRANCH,
                source=source,
            )
            rn._add_task(task)
            filter_tasks(task)

    if not finished:
        return finished

    for result_task in result_tasks:
        obj = result_task_dct[result_task]
        rn._add_task(
            Task(
                rn.get_full_name(result_task),
                Node(
                    'define',
                    {
                        'obj': obj,
                        '__tb_implicit__': [(init_ref.name, init_ref)],
                        **(
                            lambda x: {'__tb_implicit_remove__': x}
                            if x
                            else {}
                        )(
                            implicit_remove
                            + list(implicit_remove_dct[result_task].values())
                        ),
                    },
                ),
                branch=ENTRY_BRANCH,
                source=source,
            )
        )
    return finished


class TaskContext:
    """Object that allows tasks to access information about worker."""

    def __init__(self, comm, tb_comm, workername):
        self.comm = comm
        self.tb_comm = tb_comm
        self.workername = workername

    def parprint(self, *args, **kwargs):
        if self.tb_comm.rank == 0:
            print(*args, **kwargs)


class PartialTask(Exception):
    pass


def inject_context_vars(function, kwargs, context_obj):
    """Inject variables from @tb.context decorator into kwargs."""
    kwargs = kwargs.copy()
    contextvars = getattr(function, '_tb_context', None)
    if not contextvars:
        return kwargs

    for name in contextvars:
        assert name not in kwargs
        if name == 'context':
            kwargs[name] = context_obj
        else:
            kwargs[name] = getattr(context_obj, name)

    return kwargs


class LoadedTask:
    def __init__(self, entry, name, target, kwargs, has_record):
        # We have quite a few rules for whether a task can run.
        # Most of the code that decides whether to run or not resides
        # elsewhere, since we don't want to even load the task if it cannot
        # run.  But it might be wise to add a sanity check here at worker
        # level in case we loaded a task that we should not be running.
        self.entry = entry
        self.directory = entry.directory
        self.name = name
        self.target = target
        self.kwargs = kwargs
        self.has_record = has_record

    @property
    def node(self):
        from taskblaster import Node

        return Node(self.target, self.kwargs)

    def __repr__(self):
        return f'{self.name}: {self.target} {self.kwargs}'

    def run(self, worker):
        if callable(self.target):
            function = self.target
        else:
            function = worker.repo.import_task_function(self.target)

        if not callable(function):
            raise TypeError(f'Expected callable but got {function}')

        kwargs = inject_context_vars(function, self.kwargs, worker.context_obj)

        with workdir(self.directory):
            # TODO: Deprecate the MPI thing.
            if getattr(function, '_tb_mpi', False):
                assert 'mpi' not in kwargs
                kwargs['mpi'] = TaskContext(
                    comm=worker.comm.usercomm(),
                    tb_comm=worker.comm,
                    workername=worker.name,
                )

            # XXX magical incantation to recognize workflow entry points (WIP):
            if hasattr(function, '_tb_dynamical_workflow_generator_task'):
                if worker.comm.rank == 0:
                    with worker.repo:
                        self._run_dynamical_init(worker.repo, function, kwargs)

                output = None
            else:
                pop_special_kwargs(kwargs)
                output = function(**kwargs)

            if worker.comm.rank == 0:
                self.entry.dump_output(output)

    def _run_dynamical_init(self, repo, function, kwargs):
        registry = repo.registry
        rn = Runner(repo, directory=self.directory.parent)
        # XXX we set the source to our own source, because
        # I am not yet sure how to handle storage of
        # dynamical workflows.  This is not great, but it
        # only means we sometimes rerun more workflow than
        # necessary.
        source = registry.sources[self.name]
        run_dynamical_init(
            rn,
            kwargs,
            function,
            Reference(self.name),
            source=source,
        )


# XXX The inputdigest should be created from the actual digests
# of the inputs rather than just the encoded JSON, which contains
# the names.

# XXX here we need to save the hash of the inputs, where the
# namerefs are replaced by hashes.  That will work like before.
# But it's somewhat redundant since it only replaces the namerefs
# but otherwise is the same structure as the existing inputs.

# Then we hash the contents in that file, and that's the hash which
# we save to the registry.

# we need to dump a dictionary of {ref_id: hash}.
# Presumably we would save the digest to the registry,
# but then dump the actual

# Also: maybe some tasks are compared by return value,
# which is something that we can allow.  For example
# spacegroup might be 5, and remain 5 even if the inputs
# used to determine it change, and subsequent tasks should not
# be invalidated due to that.  Which means in the hashing
# it must be "5" that appears rather than a reference.


def exception_summary(exc):
    if exc is None:
        return None
    return f'{exc}'


class Worker:
    def __init__(
        self,
        repo,
        name='worker',
        selection=None,
        myqueue_id=None,
        comm=SerialCommunicator(),
        rules=None,
    ):
        self.name = name
        self.repo = repo
        self.comm = comm

        if rules is None:
            from taskblaster.repository import WorkerSpecification

            rules = WorkerSpecification()
        self.rules = rules

        print('Starting worker rank=%03d size=%03d' % (comm.rank, comm.size))
        self.log(*rules.headers())
        self.log(rules.description())

        if selection is None:
            selection = self._select_any()

        self.selection = selection
        self.cache = repo.cache
        self.registry = repo.registry
        self.myqueue_id = myqueue_id
        self.start_time = time.time()
        # If a worker executes a workflow which generates tasks,
        # it often makes sense for that worker to immediately pick up
        # and run those tasks.  This is a stack of "prioritized" tasks
        # that will be executed before the worker returns to its normal
        # task selection method.
        #
        # If the worker never executes some prioritized tasks,
        # they will simply be left alone and another worker can pick them up.
        self._affinity_tasks = []

        context_cls = self.repo.context_class()
        self.context_obj = context_cls(self)

    def log(self, *messages):
        now = datetime.now()
        timestamp = f'{now:%Y-%m-%d %H:%M:%S}'
        stamp = f'[rank={self.comm.rank:03d} {timestamp} {self.name}]'
        for message in messages:
            print(f'{stamp} {message}')
        print(end='', flush=True)

    def _select_any(self):
        while True:
            yield self.cache.find_ready(
                supported_tags=self.rules.get_compatible_tags(),
                required_tags=self.rules.required_tags,
            )

    def acquire_task(self):
        while True:
            if self.comm.rank == 0:
                loaded_task = self._acquire_task()
            else:
                loaded_task = None

            loaded_task = self.comm.broadcast_object(loaded_task)

            if loaded_task is None:
                raise Missing
            if loaded_task == 'PANIC':
                raise Panic
            if loaded_task == 'CONTINUE':
                continue

            if not isinstance(loaded_task, LoadedTask):
                self.log(
                    f'Rank {self.comm.rank} expected to acquire a'
                    'LoadedTask from MPI broadcast_object, but got'
                    f'{loaded_task} instead of type {type(loaded_task)}.'
                )
                raise Panic

            break

        return loaded_task

    def _tags_compatible(self, tags):
        # XXX Looks like this function can be removed?
        return (
            self.rules.required_tags
            <= tags
            <= self.rules.get_compatible_tags()
        )

    def _acquire_task(self):
        assert self.comm.rank == 0
        registry = self.cache.registry
        with registry.conn:
            try:
                if self._affinity_tasks:
                    name = self._affinity_tasks.pop()
                    indexnode = registry.index.node(name)
                    # XXX task may have been picked up by another
                    # worker in the meantime, must guard against this.
                else:
                    try:
                        indexnode = next(self.selection)
                        # task_tags = self.registry.resources.get_tags(
                        #     indexnode.name)
                        # if not self._tags_compatible(task_tags):
                        #     return 'CONTINUE'
                    except StopIteration:
                        raise Missing

                directory = self.cache.directory / indexnode.name
                directory.mkdir(parents=True, exist_ok=True)
                registry.update_task_running(
                    indexnode.name,
                    worker_name=self.name,
                    myqueue_id=self.myqueue_id,
                )

                entry = self.cache.entry(indexnode.name)
                target, kwargs = self.actualize_runtime_files(
                    entry, indexnode.name
                )
                has_record = registry.has_records.get(indexnode.name, False)

                return LoadedTask(
                    entry, indexnode.name, target, kwargs, has_record
                )
            except Missing:
                return
            except TBUserError as ex:
                self.log(f'Error initializing task {indexnode.name}: {ex}')
                self._failed(indexnode, ex)
                return 'CONTINUE'
            except Exception as ex:
                print('Worker panic! Stopping.')
                print('Exception occurred while trying to initialize ')
                print('queued task to be run at the worker')
                print(traceback.format_exc())
                self._failed(indexnode, ex)
            return 'PANIC'

    def actualize_runtime_files(self, entry, name):
        # check for error handler updates to the task
        serialized_input = entry.updated_serialized_inputs
        if serialized_input is None:
            serialized_input = self.cache.registry.inputs.get(name)
        serialized_handlers = self.cache.registry.handlers.get(name, '[]')
        target, kwargs = self.cache.json_protocol._actually_load(
            self.cache, serialized_input, entry.directory / name
        )

        if not entry.has_updated_inputs:
            entry.inputfile.write_text(serialized_input)
        entry.handlersfile.write_text(serialized_handlers)

        return target, kwargs

    def _failed(self, indexnode, exception):
        self.registry.update_task_failed(
            indexnode.name, error_msg=exception_summary(exception)
        )

    def check_soft_termination(self, ntasks: int) -> str | None:
        if ntasks == self.rules.max_tasks:
            return f'Max tasks {ntasks} reached'

        elapsed = time.time() - self.start_time

        if self.rules.wall_time is not None and elapsed > self.rules.wall_time:
            return 'Worker walltime exceeded'

        return None

    def main(self):
        self.log('Main loop')
        self.repo.worker_start_hook()
        try:
            ntasks = 0
            while True:
                trouble = self.check_soft_termination(ntasks)
                if trouble:
                    self.log(f'Ending main loop: {trouble}')
                    return

                ntasks += 1

                try:
                    self.process_one_task()
                except Missing:
                    self.log('No available tasks, end worker main loop')
                    return
                except Panic:
                    self.log(
                        'Worker terminating due to exception in task '
                        'initialization.'
                    )
                    return
        finally:
            self.repo.worker_finish_hook()

    def process_one_task(self):
        loaded_task = None
        prospective_state = State.fail
        try:
            try:
                loaded_task = self.acquire_task()
            except Missing:
                raise
            except Panic:
                raise
            except Exception as err:
                self.log(traceback.format_exc())
                self.log(f'Failed in initialization: {err}')
                # Log exception somehow.
                return

            starttime = datetime.now()
            self.log(f'Running {loaded_task.name} ...')
            exception = None
            try:
                loaded_task.run(self)
            except (KeyboardInterrupt, TaskBlasterInterrupt, Exception) as err:
                stacktrace = traceback.format_exc()
                self.log(stacktrace)
                fname = Entry.stacktracetemplate.format(self.comm.rank)
                stacktracefile = loaded_task.entry.directory / fname
                stacktracefile.write_text(stacktrace)
                exception = err
                msg = exception_summary(exception)
                self.log(f'Task {loaded_task.name} failed: {msg}')

                if not isinstance(err, Exception):
                    raise  # Interrupts must be reraised and we abort
            else:
                prospective_state = State.done
                elapsed = datetime.now() - starttime
                self.log(f'Task {loaded_task.name} finished in {elapsed}')

        finally:
            if loaded_task is not None and self.comm.rank == 0:
                name = loaded_task.name
                with self.registry.conn:
                    if prospective_state == State.done:
                        self.registry.update_task_done(name)
                        if loaded_task.has_record:
                            self._affinity_tasks.append(name + '.record')
                    elif prospective_state == State.fail:
                        # datafy exception for better recovery
                        exception_data = ExceptionData.from_exception(
                            exception
                        )
                        exception_data.write(
                            self.cache.json_protocol, loaded_task
                        )

                        self.warden_handle_failed_state(
                            name, loaded_task, exception_data
                        )
                    else:
                        raise ValueError(
                            f'Unexpected state {prospective_state}'
                        )

    def warden_handle_failed_state(self, name, loaded_task, exception_data):
        try:
            return self._warden_handle_failed_state(
                name, loaded_task, exception_data
            )
        except WardenPanic:
            self.registry.update_task_failed(
                name,
                error_msg=exception_summary(
                    'Warden trying to set a state to partial that is '
                    'currently not a supported transition.'
                ),
            )

    def _warden_handle_failed_state(
        self, name, loaded_task, exception_data: ExceptionData
    ):
        # always pass failures through the warden in case we
        # can handle the exception
        warden = Warden(self.cache, self.log, name)
        outcome = warden.handle(loaded_task, exception_data)

        # XXX reminder to also update tags for tasks in database
        if outcome.update_tags:
            warden.log_warden('Updating tags.')

        # ask Outcome if we need to write handler files
        if outcome.write_datafiles:
            assert hasattr(outcome, 'handler_data')
            warden.write_handler(loaded_task, outcome.handler_data)

        # check an outcome if we update affinity tasks
        if outcome.update_task_partial:
            # XXX we need to check the tags match the queue
            # for the worker, in case tags are the source of
            # handling the error i.e. case of high memory
            self.log('WARDEN: Updating state to partial.')
            self.registry.update_task_partial(loaded_task.name)

        # intercept the record task before it is canceled on failure
        if loaded_task.has_record and outcome.create_record:
            self.log('RECORD: Creating record for failed tasks')
            encoded_task = create_record_for_task(
                name,
                parent_state=State.fail,
                cache=self.cache,
                output_as='EncodedTask',
            )
            self.log('RECORD: Adding record to _affinity_tasks')
            self._affinity_tasks.append(name + '.record')
            self.cache.add_or_update(
                encoded_task,
                force_overwrite=True,
            )

        # now we need to update the state of this task correctly
        if outcome.update_task_failed:
            self.registry.update_task_failed(
                name,
                error_msg=exception_summary(outcome.exception_data.info),
            )
