import json
import warnings
from collections import defaultdict
from copy import deepcopy

from taskblaster import (
    BoundTaskSpecification,
    BoundWorkflowSpecification,
    Input,
    Phi,
)
from taskblaster.runner import RunnerState
from taskblaster.view_workflow_html import (
    DEFAULT_STYLE,
    LEADER_LINE,
    ViewWorkflowTemplate,
)


class HTMLElement:
    def __init__(self, html, name, _class=None, _id=None):
        self.html = html
        self.name = name
        self._class = _class
        self._id = _id

    def __enter__(self):
        self.html.begin(self.name, _class=self._class, _id=self._id)

    def __exit__(self, *args):
        self.html.end(self.name)


class InputVarWrapper:
    def __init__(self, name):
        self.name = name


class HTMLWriter:
    def __init__(self, filename):
        self.filename = filename
        self.indent = 0

    @property
    def space(self):
        return '    ' * self.indent

    def begin(self, tag, **kwargs):
        self._print(f'{self.space}<{tag}', end='')
        for key, value in kwargs.items():
            if value is None:
                continue
            if key.startswith('_'):
                key = key[1:]
            self._print(f' {key}="{value}"', end='')
        self._print('>')
        self.indent += 1

    def print(self, *args, **kwargs):
        print(self.space, end='', file=self.f)
        print(*args, **kwargs, file=self.f)

    def _print(self, *args, **kwargs):
        print(*args, **kwargs, file=self.f)

    def end(self, tag):
        self.indent -= 1
        self._print(f'{self.space}</{tag}>')

    def __enter__(self):
        self.f = open(self.filename, 'w')
        return self

    def div(self, _class=None, _id=None):
        return HTMLElement(self, 'div', _class=_class, _id=_id)

    def span(self, _class=None, _id=None):
        return HTMLElement(self, 'span', _class=_class, _id=_id)

    def __exit__(self, *args):
        self.f.close()
        self.f = None


class FakeRunnerState(RunnerState):
    pass


class FakeRunner:
    def __init__(self, directory=''):
        self._seen_branches = defaultdict(int)
        if directory is None:
            directory = ''
        self.directory = directory
        self.state = FakeRunnerState()

    def get_full_name(self, methname):
        if self.directory != '':
            directory = self.directory + '-' + methname
            return directory
        else:
            return methname

    def with_subdirectory(self, folder):
        directory = (
            self.directory + '-' if self.directory != '' else ''
        ) + folder
        return FakeRunner(directory)

    def with_directory(self, folder):
        return FakeRunner(folder.replace('/', '-'))


class WorkflowView:
    def __init__(self, style):
        self.script = ''
        self.total_lines = 0
        self.taskids = []
        self.wfstyle = deepcopy(DEFAULT_STYLE)
        if style:
            with open(style, 'r') as f:
                self.wfstyle.update(json.load(f))
        self.template = ViewWorkflowTemplate(self.wfstyle)

    def new_line(
        self,
        frm,
        to,
        startSocket='bottom',
        endSocket='top',
        color='green',
        dropShadow=False,
    ):
        assert 'base-base' not in frm
        beforeto = ''
        afterto = ''
        self.total_lines += 1
        if frm == to:
            if 'branchcontent' in to:
                to = to.replace('branchcontent', 'branch')
            else:
                # print('Warning: Line to itself', frm, to)
                return
        assert '-' in frm
        # assert frm != to
        frm = frm.replace('-000', '')
        to = to.replace('-000', '')
        assert '--' not in frm
        if dropShadow:
            arrowtype = 'branch'
        else:
            arrowtype = 'parameter'
        self.script += LEADER_LINE.format(
            to=to,
            beforeto=beforeto,
            afterto=afterto,
            frm=frm,
            startSocket=startSocket,
            endSocket=endSocket,
            color=color,
            dropShadow=str(dropShadow).lower(),
            arrow_path=self.wfstyle.get(
                f'{arrowtype}-arrow-path', self.wfstyle['arrow-path']
            ),
            dash=str(self.wfstyle.get(f'{arrowtype}-dash', False)).lower(),
            size=self.wfstyle.get(
                f'{arrowtype}-arrow-size', self.wfstyle['arrow-size']
            ),
            startSocketGravity=self.wfstyle.get(
                f'{arrowtype}-startSocketGravity',
                self.wfstyle['startSocketGravity'],
            ),
            endSocketGravity=self.wfstyle.get(
                f'{arrowtype}-endSocketGravity',
                self.wfstyle['endSocketGravity'],
            ),
        )

    def print_workflow_header(self, html, wf_variable, wfname, cls, wf):
        with html.div(_class='workflowheader'):
            with html.span(_class='workflowtitle'):
                html.print(wf_variable + ': ' + wfname)
            with html.span(_class='workflowinputs'):
                for inputvar in sorted(cls._inputvars):
                    if self.wfstyle['display-parameters']:
                        if inputvar not in self.wfstyle['display-parameters']:
                            continue
                    with html.span(
                        _class='workflowinput',
                        _id=wf._rn.get_full_name(inputvar),
                    ):
                        html.print(inputvar)

    def print_workflow_branch(self, html, wf, branch, branchspec):
        def add_lines(task, kwarg, value):
            prev_lines = self.total_lines
            target = 'tinput-' + wf._rn.get_full_name(task) + '-' + kwarg

            def route(value, target):
                if isinstance(value, InputVarWrapper):
                    self.new_line(f'base-{value.name}', target)
                elif isinstance(value, Input):
                    assert isinstance(value.input_name, str)
                    self.new_line(
                        wf._rn.get_full_name(value.input_name), target
                    )
                    route(value._value, wf._rn.get_full_name(value.input_name))
                elif isinstance(value, BoundWorkflowSpecification):
                    value = value.resolve_reference()
                    route(value, target)
                elif isinstance(value, BoundTaskSpecification):
                    self.new_line(f'taskbody-{value.name}', target)
                elif isinstance(value, Phi):
                    for branch, arg in value.kwargs.items():
                        add_lines(task, kwarg, arg)
                elif value is None:
                    warnings.warn(
                        'view-workflow is still experimental. '
                        'Got unexpected None.'
                    )
                elif isinstance(value, list):
                    lst = value
                    if len(lst) > 0:
                        value = lst[-1]
                    else:
                        return
                    if len(lst) > 1:
                        route(lst[:-1], target)
                    pass
                elif isinstance(value, (float, str)):
                    warnings.warn(
                        'Outputting default values not yet implemented.'
                    )
                    self.total_lines += 1
                else:
                    raise TypeError(
                        f'Warning: Unkown element:{type(value)} {value}'
                    )

            route(value, target)
            if self.total_lines == prev_lines:
                warnings.warn(
                    'view-workflow is still experimental. '
                    'Some lines might be missing.'
                )

        with html.div(_class='branch'):
            with html.div(
                _class='branchtitle',
                _id='branch-' + wf._rn.get_full_name(branch),
            ):
                html.print(branch)
            with html.div(
                _class='branchcontent',
                _id='branchcontent-' + wf._rn.get_full_name(branch),
            ):
                for (
                    subwfname,
                    wfspec,
                ) in branchspec.subworkflows.items():
                    with html.div(_class='subworkflow'):
                        subwf = getattr(wf, subwfname).get_node()
                        subwf._rn = wf._rn.with_subdirectory(subwfname)
                        for var in subwf._inputvars:
                            getattr(subwf, var).__dict__['input_name'] = var
                        self.print_workflow(
                            html,
                            subwf,
                            subwfname,
                            mainworkflow=False,
                        )
                for (
                    task,
                    taskspec,
                ) in branchspec.unbound_tasks.items():
                    taskid = 'actualtask-' + wf._rn.get_full_name(task)
                    self.taskids.append(taskid)
                    with html.div(_class='task', _id=taskid):
                        with html.div(_class='taskparameter-line'):
                            node = taskspec.unbound_meth(wf)
                            for i, (kwarg, value) in enumerate(
                                sorted(node.kwargs.items())
                            ):
                                if self.wfstyle['display-parameters']:
                                    if (
                                        kwarg
                                        not in self.wfstyle[
                                            'display-parameters'
                                        ]
                                    ):
                                        continue
                                add_lines(task, kwarg, value)
                                with html.span(
                                    _class=('ifcolor ' if taskspec._if else '')
                                    + ('first-' if i == 0 else '')
                                    + 'taskparameter',
                                    _id='tinput-'
                                    + wf._rn.get_full_name(task)
                                    + '-'
                                    + kwarg,
                                ):
                                    html.print(kwarg)
                            with html.div(_class='taskname'):
                                html.print(task)
                        with html.div(
                            _class=('if' if taskspec._if else '') + 'taskbody',
                            _id='taskbody-' + wf._rn.get_full_name(task),
                        ):
                            with html.div(_class='taskimport'):
                                html.print(node.target.split('.')[-1])
                    if taskspec.jump:
                        to_branch = taskspec.jump
                        self.new_line(
                            'branchcontent-' + wf._rn.get_full_name(branch),
                            self.wfstyle['branch-arrow-target']
                            + '-'
                            + wf._rn.get_full_name(to_branch),
                            startSocket='right',
                            endSocket=self.wfstyle['branch-end-socket'],
                            color='black',
                            dropShadow=True,
                        )
                    if taskspec._if:
                        for (
                            key,
                            to_branch,
                        ) in taskspec._if.items():
                            if to_branch is None:
                                continue
                            self.new_line(
                                'branchcontent-'
                                + wf._rn.get_full_name(branch),
                                self.wfstyle['branch-arrow-target']
                                + '-'
                                + wf._rn.get_full_name(to_branch),
                                startSocket='right',
                                endSocket=self.wfstyle['branch-end-socket'],
                                color='green' if key else 'red',
                                dropShadow=True,
                            )

    def print_workflow_body(self, html, wf, cls):
        with html.div(_class='workflowbody'):
            with html.div(_class='branchlist'):
                for branch, branchspec in cls._branches.items():
                    self.print_workflow_branch(html, wf, branch, branchspec)

    def print_workflow(self, html, wf, wf_variable='', mainworkflow=True):
        cls = wf.__class__
        wfname = cls.__name__

        with html.div(
            _class='workflow' + (' mainworkflow' if mainworkflow else '')
        ):
            self.print_workflow_header(html, wf_variable, wfname, cls, wf)
            self.print_workflow_body(html, wf, cls)

    def write_html(self, filename, cls):
        inputs = {
            input_var: InputVarWrapper(input_var)
            for input_var in cls._inputvars
        }
        wf = cls(**inputs)
        wf._rn = FakeRunner('base')
        for var in wf._inputvars:
            assert isinstance(var, str)
            getattr(wf, var).__dict__['input_name'] = var

        # self._inputvars = cls._inputvars
        # self.name = cls.__name__
        # for input_var in cls._inputvars:
        #    print(input_var, type(input_var))
        # self.cls = cls

        with HTMLWriter(filename) as html:
            html.print(self.template.head)
            self.print_workflow(html, wf)
            html.print('<script>')
            html.print(self.script)
            for taskid in self.taskids:
                pass
                # html.print(f"new PlainDraggable(
                # document.getElementById('{taskid}'));")
            html.print('</script>')
            html.print(self.template.tail)
        print(f'Succesfully wrote workflow visualization to {filename}.')


def view_workflow(cls, output='workflow.html', style=None):
    view = WorkflowView(style)
    view.write_html(output, cls)
