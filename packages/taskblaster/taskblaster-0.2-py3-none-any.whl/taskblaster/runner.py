import os
from collections import defaultdict
from pathlib import Path

import click

from taskblaster import (
    ENTRY_BRANCH,
    TB_STRICT,
    BoundTaskSpecification,
    DummyUnboundTask,
    DynamicalWorkflowGeneratorSpecificationProperty,
    Node,
    Phi,
    Reference,
    TaskSpecificationProperty,
    TBUserError,
    UnreachableReference,
    WorkflowSpecificationProperty,
    create_record_for_task,
)
from taskblaster.future import Future
from taskblaster.namedtask import Task
from taskblaster.registry import IndexNode
from taskblaster.state import State
from taskblaster.util import color
from taskblaster.workflowtable import BoundWorkflow

TOPOLOGY_DEBUG = bool(int(os.environ.get('TB_TOPOLOGY_DEBUG') or 0))


def define(obj):
    return obj


class RunnerLogs:
    """Logging functionality for the workflow runner"""

    def __init__(self, silent=False):
        self._silent = silent
        self._pre_print = ''
        self._post_print = ''

    def set_branch(self, branch):
        self.pre_print(color(f'{branch}:', fg='bright_cyan'))

    def print_success_jump(self, jump_to):
        self.post_print(
            color('jump: ', fg='bright_green')
            + color(jump_to, fg='bright_cyan')
        )

    def print_unrealized_jump(self, jump_to):
        self.post_print(
            color('if success jump: ', fg='bright_blue')
            + color(jump_to, fg='bright_cyan')
        )

    def jump_print(self, jump_to):
        self.post_print(
            color('jump: ', fg='bright_magenta')
            + color(jump_to, fg='bright_cyan')
        )

    def pre_print(self, s):
        self._pre_print = self._pre_print.rstrip()
        self._pre_print += s
        self._pre_print += ' ' * (15 - len(click.unstyle(self._pre_print)))

    def post_print(self, s):
        self._post_print += s

    def print(self, s):
        self.pre_print('')
        print(self._pre_print, end='')
        print(s, end=' ')
        print(self._post_print)
        self._pre_print = ''
        self._post_print = ''

    def print_new_if(self, bound_task):
        self.pre_print(color('if:', fg='bright_blue'))
        for key, value in bound_task._if.items():
            if key is True:
                key = 'T'
            if key is False:
                key = 'F'
            self.post_print(color(f'{key}=', fg='bright_cyan'))
            self.post_print(color(value, fg=State.new.color))
            self.post_print(' ')

    def print_realized_if(self, bound_task, output, jump_to):
        self.pre_print(color('if:', fg='bright_blue'))
        for key, value in bound_task._if.items():
            cl = State.done.color if output == key else State.fail.color
            if key is True:
                key = 'T'
            if key is False:
                key = 'F'
            self.post_print(color(f'{key}=', fg='bright_cyan'))
            self.post_print(color(value, fg=cl))
            self.post_print(' ')

        self.post_print(
            color('jump: ', fg='bright_magenta')
            + color(jump_to, fg='bright_cyan')
        )

    def print_task(self, action_str, future_description, *, metaaction):
        colors = {
            'have': 'yellow',
            'amend': 'cyan',
            'update': 'bright_yellow',
            'add': 'bright_blue',
            'conflict': 'bright_red',
            'resolved': 'bright_blue',
        }

        self.print(
            '{}{} {}'.format(
                ' ' * (14 - len(action_str)),
                click.style(action_str, colors[action_str])
                + ' '
                + click.style(metaaction, colors['update']),
                future_description,
            )
        )


class RunnerState:
    """Mutable part of the runner."""

    def __init__(self):
        self._current_workflow = None
        self._current_branch = None
        self._from_branch = None
        self._seen_branches = defaultdict(int)
        self.jump_to = None
        self.if_task = None

    def _new_branch(self, branch_name, from_branch=None):
        if from_branch is None:
            self._from_branch = self._current_branch
        else:
            self._from_branch = from_branch
        self._current_branch = branch_name

        if not self._current_workflow.workflow_obj._branches[branch_name].loop:
            if branch_name in self._seen_branches:
                raise TBUserError(
                    f'Revisiting a non-loop branch {branch_name}'
                )
        self._seen_branches[self._current_branch] += 1
        self.jump_to = None
        self.if_task = None

    def new_jump(self, target, log: RunnerLogs = None, if_task=None):
        if target is None:
            return
        assert self.jump_to is None
        self.jump_to = target

        if if_task:
            assert self.if_task is None
            self.if_task = if_task

        if log is not None:
            if if_task is None:
                log.jump_print(target)


# Add temporary debug helper to ensure that now new attributes are set
class Immutable(object):
    _isimmutable = False

    def __setattr__(self, key, value):
        if self._isimmutable:
            raise TypeError('Runner is immutable.')
        object.__setattr__(self, key, value)

    def _immutable(self):
        self._isimmutable = True


def NodeLike(workflow, name, _property):
    bound_node = getattr(workflow, name)
    if isinstance(_property, WorkflowSpecificationProperty):
        return _NodeLikeSubworkflow(name, _property, bound_node.get_node())
    if isinstance(_property, DynamicalWorkflowGeneratorSpecificationProperty):
        return _NodeLikeDynamicalWorkflowGenerator(
            name, _property, bound_node.get_node()
        )
    if isinstance(_property, TaskSpecificationProperty):
        return _NodeLikeTask(name, _property, bound_node.__task__())
    raise RuntimeError(f'Unknown type {_property.__class__.__name__}')


class _NodeLike:
    def __init__(self, short_name, _property, obj):
        self._short_name = short_name
        self._property = _property
        self._obj = obj

    def __repr__(self):
        return f'{self.__class__.name} {self.name} {self.jump}'

    @property
    def name(self):
        return self._obj.name

    @property
    def _if(self):
        return self._property._if

    @property
    def jump(self):
        return self._property.jump

    @property
    def is_workflow(self):
        return False


class _NodeLikeTask(_NodeLike):
    def handle(
        self,
        runner,
        callback,
        add_workflows_to_registry,
        source,
        *,
        implicit_dependencies,
    ):
        bound_workflow = runner.state._current_workflow
        self.check_ifs(runner, self._obj, bound_workflow)

    def check_ifs(self, runner, bound_task, bound_workflow):
        if bound_task._if is None:
            return

        # There cannot be both _if and jump in a single task
        assert bound_task.jump is None
        jump_to = None
        try:
            # Have we previously seen this task?
            entry = runner._cache.entry(bound_task.name)
        except KeyError:
            # If not, we print out new if statement logging
            runner.logs.print_new_if(bound_task)
            # Workflow is not finished as all jumps are not taken
            bound_workflow.finished = False
        else:
            # We do have a task in repo, does it have output?
            if entry.has_output():
                # If it has, we realize the output and jump accordingly
                output = entry.output()
                jump_to = bound_task._if[output]
                runner.logs.print_realized_if(bound_task, output, jump_to)
            else:
                # If not, we are still an ondetermined if, log accordingly
                runner.logs.print_new_if(bound_task)
                bound_workflow.finished = False
        runner.state.new_jump(jump_to, log=runner.logs, if_task=bound_task)


class _NodeLikeExternal(_NodeLikeTask):
    @property
    def _if(self):
        return None

    @property
    def jump(self):
        return None


class _NodeLikeSubworkflow(_NodeLike):
    @property
    def is_workflow(self):
        return True

    @property
    def name(self):
        return self._short_name

    def handle(
        self,
        runner,
        callback,
        add_workflows_to_registry,
        source,
        *,
        implicit_dependencies,
    ):
        bound_workflow = runner.state._current_workflow
        subworkflow = self._obj
        # Clean up hacky management of _rn attribute
        assert subworkflow._rn is not None

        # Move to here
        runner.resolve_subworkflow_input_phi(subworkflow)

        sub_rn = subworkflow._rn
        subworkflow._rn = None

        bound_subwf = sub_rn.run_workflow(
            subworkflow,
            callback=callback,
            add_workflows_to_registry=add_workflows_to_registry,
            source=bound_workflow.data.name,
            implicit_dependencies=implicit_dependencies.copy(),
        )
        bound_workflow.finished &= bound_subwf.finished


class _NodeLikeDynamicalWorkflowGenerator(_NodeLikeSubworkflow):
    def handle(
        self,
        runner,
        callback,
        add_workflows_to_registry,
        source,
        *,
        implicit_dependencies,
    ):
        super().handle(
            runner,
            callback,
            add_workflows_to_registry,
            source,
            implicit_dependencies=implicit_dependencies,
        )
        from taskblaster.worker import run_dynamical_init

        bound_workflow = runner.state._current_workflow
        subworkflow = self._obj
        init_name = subworkflow._rn.get_full_name('init')
        if (
            init_name in runner._cache
            and runner._cache.entry(init_name).has_output()
        ):
            target, kwargs = runner._cache.load_inputs_and_resolve_references(
                init_name
            )
            bound_workflow.finished &= run_dynamical_init(
                subworkflow._rn,
                kwargs,
                runner._repo.import_task_function(target),
                Reference(init_name),
                source,
            )


class Runner(Immutable):
    def __init__(
        self,
        repo,
        *,
        directory=Path(),
        dry_run=False,
        silent=False,
        max_tasks=None,
        clobber_implicit_deps: bool = False,
    ):
        self._repo = repo
        self._directory = Path(directory)
        assert self._directory.is_absolute()
        self._dry_run = dry_run
        self._clobber_implicit_deps = clobber_implicit_deps

        self.logs = RunnerLogs(silent=silent)
        self.state = RunnerState()

        self._immutable()

    def relative_to(self, pth):
        return str(
            Path(pth).relative_to(
                self._directory.relative_to(self._cache.directory)
            )
        )

    @property
    def prefix(self):
        return str(self._directory)

    @property
    def _cache(self):
        return self._repo.cache

    @property
    def directory(self):
        # XXX self._directory is already absolute?? / is unnecessary.
        return self._repo.tree_path / self._directory

    @property
    def relative_name(self):
        return self._directory.relative_to(self._repo.tree_path)

    def with_directory(self, directory):
        return self._new(directory=self._repo.tree_path / directory)

    def with_subdirectory(self, directory):
        return self._new(directory=self._directory / directory)

    def get_full_name(self, name):
        fullpath = self.directory / name
        relpath = fullpath.relative_to(self._cache.directory)
        return str(relpath)

    def _new(self, **kwargs):
        kwargs = {
            'repo': self._repo,
            'dry_run': self._dry_run,
            'silent': self.logs._silent,
            'directory': self._directory,
            'clobber_implicit_deps': self._clobber_implicit_deps,
            **kwargs,
        }

        return Runner(**kwargs)

    def _find_refs(self, task):
        import json

        from taskblaster import Input

        runner_self = self

        class ReferenceFinder:
            def __init__(self, codec):
                self._refs = []
                self.codec = codec

            def add_reference(self, ref):
                self._refs.append(ref)

            def default(self, obj):
                if isinstance(obj, Path):
                    return None
                if isinstance(obj, Input):
                    return obj.getvalue()
                if isinstance(obj, Reference):
                    resolved = obj.resolve_reference()
                    self.add_reference(resolved)
                    return None
                if isinstance(obj, Future):
                    # XXX also there's Reference
                    raise RuntimeError('should not receive Future here?')
                if isinstance(obj, Phi):
                    resolved = obj.resolve(runner_self)
                    return resolved
                if hasattr(obj, '_refhook'):
                    ref = obj._refhook()
                    self.add_reference(ref)
                    return None

                return self.codec.encode(obj)

            def find_refs(self, task):
                # (The encoder extracts the references as a side
                # effect of encoding.)
                json.dumps(
                    (task.node.target, task.node.kwargs), default=self.default
                )
                return self._refs

        reffinder = ReferenceFinder(codec=self._cache.json_protocol.codec)
        refs = reffinder.find_refs(task)
        return refs

    def _bind_workflow(self, workflow, source, add_workflows_to_registry):
        workflowname = self.get_full_name('')
        if workflowname == '.':
            # XXX clean up the get_full_name() business.
            # This is for the root workflow.
            workflowname = ''

        # Is serialize_inputs() necessarily what we want for workflows?
        # It may do more than we bargained for in some cases, but 95%
        # of it is probably what we want.
        if add_workflows_to_registry:
            buf = self._cache.json_protocol.serialize_inputs(
                workflow, workflowname
            )
        else:
            buf = None

        bound_workflow = BoundWorkflow.bind(
            name=workflowname,
            workflow=workflow,
            serialized_input=buf,
            source=source,
            rn=self,
        )

        if TB_STRICT:
            assert source is not None

        if add_workflows_to_registry:
            self._cache.registry.workflows[bound_workflow.data.name] = (
                bound_workflow.data
            )
        return bound_workflow

    def run_workflow(
        self,
        workflow,
        callback=lambda x: None,
        add_workflows_to_registry: bool = False,
        source=None,
        implicit_dependencies=None,
    ):
        if TB_STRICT:
            assert add_workflows_to_registry
            assert source is not None

        is_workflow = getattr(workflow, '_is_tb_workflow', False)
        if not is_workflow:
            raise TBUserError(
                'run_workflow commands expects a Workflow '
                '(decorated with @tb.workflow). Got '
                f'{type(workflow)}.'
            )

        bound_workflow = self._bind_workflow(
            workflow,
            source,
            add_workflows_to_registry=add_workflows_to_registry,
        )

        assert self.state._current_workflow is None
        self.state._current_workflow = bound_workflow

        seen = set()

        implicit_dependencies = implicit_dependencies or []

        # All workflow execution starts from entry
        assert self.state._current_branch is None
        self.state._new_branch('entry', from_branch='default')

        while True:
            for nodelike in self._iterate_tasks(
                bound_workflow,
                callback=callback,
                add_workflows_to_registry=add_workflows_to_registry,
            ):
                assert isinstance(nodelike, _NodeLike)
                self.state.new_jump(nodelike.jump, log=self.logs)

                nodelike.handle(
                    self,
                    callback,
                    add_workflows_to_registry,
                    source,
                    implicit_dependencies=implicit_dependencies.copy(),
                )

                if nodelike.is_workflow:
                    continue

                task = nodelike._obj
                for required_task in self._topological_order(task, seen):
                    if self.relative_name == Path(required_task.name).parent:
                        branch_name = required_task.branch
                        if branch_name not in self.state._seen_branches:
                            raise TBUserError(
                                f'Task {required_task} depending on branch not'
                                f' yet visited ({branch_name}).'
                                ' Visited branches'
                                f' {set(self.state._seen_branches)}.'
                            )
                    if Path(required_task.name).parent.is_relative_to(
                        self.relative_name
                    ):
                        for dependency in implicit_dependencies:
                            required_task.add_implicit_dependency(
                                dependency, remove=True
                            )

                    self._add_task(required_task, callback=callback)

            if self.state.jump_to is None:
                break

            workflow._rn = None
            if self.state.if_task is not None:
                implicit_dependencies.append(
                    Reference(self.state.if_task.name)
                )
                # Tentative fix for inherited implicit dependencies
                # that works in simple cases but would be wrong in other
                # cases:
                # implicit_dependencies = [Reference(self.state.if_task.name)]

            self.state._new_branch(self.state.jump_to)

        return bound_workflow

    def _topological_order(self, task: Task, seen):
        if task.name in seen:
            return
        refs = self._find_refs(task)
        for ref in refs:
            # Bare references are only supported, if they relate to the
            # current workflow. This is used by records.
            if type(ref) is Reference:
                wf = self.state._current_workflow.workflow_obj

                # will fail for outside workflows
                attribute = self.relative_to(ref.name)

                # make also sure that refers to an element in this wf
                assert '/' not in attribute

                boundtaskspec = getattr(wf, attribute)
                for args in ref.index:
                    boundtaskspec = boundtaskspec._accessor(*args)
                yield from self._topological_order(
                    boundtaskspec.__task__(), seen
                )
                continue

            if not isinstance(
                ref,
                (
                    BoundTaskSpecification,
                    DummyUnboundTask,
                    UnreachableReference,
                ),
            ):
                raise TBUserError(
                    f'INTERNAL ERROR: Unknown reference type {ref} TYPE: '
                    f'{ref.__class__}'
                )
            if ref.name in seen:
                continue

            if ref.unreachable:
                continue

            if ref.name in self._cache:
                # Ignore task which already exists -- we don't need
                # to generate that task.
                #
                # Although somewhere we should check, or be able to check,
                # that it isn't outdated.
                continue

            ref_task = ref.__task__()

            # Should use iterative rather than recursive
            yield from self._topological_order(ref_task, seen)

        if task.name in seen:
            return

        if task.node.target != 'fixedpoint':
            seen.add(task.name)

        yield task

        if task.has_record:
            indexnode: IndexNode = self._cache.registry.index.node(task.name)
            record_task = create_record_for_task(task.name, indexnode.state)
            if record_task.name not in seen:
                seen.add(record_task.name)
                yield record_task

    def resolve_subworkflow_input_phi(self, subworkflow):
        for var in subworkflow._inputvars:
            inputvar = getattr(subworkflow, var)
            if isinstance(inputvar, Phi):
                setattr(subworkflow, var, inputvar.resolve(self))

    def _iterate_tasks(
        self,
        bound_workflow,
        no_assert=False,
        callback=None,
        *,
        add_workflows_to_registry,
        source=None,
    ):
        workflow = bound_workflow.workflow_obj
        # XXX We need a WorkflowRunner which takes just one workflow
        # and a Runner. Now Runner is mutable with two states:
        # either it is assigned to a workflow or not
        # self._current_workflow and the asserts are there to disable problems
        # arising from this mutability
        # assert self._current_workflow is None

        self.logs.set_branch(self.state._current_branch)

        if not no_assert:
            assert workflow._rn is None
        workflow._rn = self

        # Create fixedpoint tasks
        for task_name, task in workflow._external.items():
            full_name = self.get_full_name(task_name)
            if full_name not in self._cache:
                unmet_ref = UnreachableReference()
                task = Task(
                    full_name,
                    Node('fixedpoint', {'obj': unmet_ref}),
                    branch='entry',
                    source=bound_workflow.data.name,
                )
                yield _NodeLikeExternal(task_name, None, task)

        for (
            name,
            _property,
        ) in workflow._dynamical_workflow_generators.items():
            yield NodeLike(workflow, name, _property)

        # For subworkflows reversed, one asrlib test fails
        for name, _property in workflow._subworkflows.items():
            yield NodeLike(workflow, name, _property)

        wrapper = reversed if TOPOLOGY_DEBUG else lambda x: x
        for name, _property in wrapper(workflow._unbound_tasks.items()):
            yield NodeLike(workflow, name, _property)

        # XXX See above XXX
        assert self.state._current_workflow.workflow_obj is workflow

    def _add_task(
        self, task, callback=lambda task: None, *, force_overwrite=False
    ):
        """
        # XXX This below is apparently no longer needed, after bug fixes!!!
        # To fix a critical bug, we inherit the __tb_implicit_remove__ from
        # the task corresponding to this record.
        if task.name.endswith('.record'):
            orig_encoded_task = self._cache.encoded_task(
                task.name.split('.record')[0]
            )
            node = self._cache.json_protocol.deserialize_node(
                orig_encoded_task.serialized_input, orig_encoded_task.name
            )

            implicits = node.kwargs.get('__tb_implicit_remove__', [])
            for _, ref in implicits:
                task.add_implicit_dependency(ref, remove=True)
        """
        callback(task)

        encoded_task = self._cache.json_protocol.encode_task(task)

        action_str, metaaction_str, indexnode = self._cache.add_or_update(
            encoded_task,
            force_overwrite=force_overwrite,
            clobber_implicit_deps=self._clobber_implicit_deps,
        )

        future = Future(encoded_task, self._cache)

        self.logs.print_task(
            action_str, future.describe(), metaaction=metaaction_str
        )

        return action_str, future

    def define(self, obj, name, source):
        task = Task(
            name,
            Node('define', {'obj': obj}),
            branch=ENTRY_BRANCH,
            source=source,
        )

        return self._add_task(task)
