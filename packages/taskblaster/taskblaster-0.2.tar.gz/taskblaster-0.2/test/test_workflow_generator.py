import pytest

import taskblaster as tb
from taskblaster.testing import CompositeWorkflow


@tb.dynamical_workflow_generator_task
def looped_generator(ntasks):
    for i in range(ntasks - 1):
        yield 'task%d' % i, tb.node('define', obj=i)


def count_tasks(tasks):
    return len(tasks)


def check_results(results):
    return bool(len(results))


@tb.dynamical_workflow_generator_task
def thetask(inputs):
    for i, inp in enumerate(inputs):
        wf = CompositeWorkflow(msg=inp)
        name = 'muforloop' + str(i)
        yield name, wf


@tb.dynamical_workflow_generator_task
def thetaskwithdot(inputs):
    for i, inp in enumerate(inputs):
        wf = CompositeWorkflow(msg=inp)
        name = 'muforloop.' + str(i)
        yield name, wf


@tb.dynamical_workflow_generator_task
def dependingtask(inputs):
    inp = inputs
    for i in range(3):
        wf = CompositeWorkflow(msg=inp)
        name = 'loop' + str(i)
        yield name, wf
        inp = wf.hello


@tb.dynamical_workflow_generator_task
def nestedtask(inputs):
    for i, inp in enumerate(inputs):
        wf = GeneratedWorkflow(inputs=inp)
        name = 'mainloop' + str(i)
        yield name, wf


@tb.workflow
class FailingInitWorkflow:
    fail_if_true = tb.var()

    @tb.dynamical_workflow_generator({'gather': '**'})
    def generate(self):
        return tb.node(failing_init, fail_if_true=self.fail_if_true)


@tb.workflow
class GeneratedWorkflow:
    inputs = tb.var()  # list of input vars

    @tb.dynamical_workflow_generator({'results': '*/hello'})
    def generate_wfs_from_list(self):
        return tb.node(thetask, inputs=self.inputs)

    @tb.task
    def depends_on_generate(self):
        return tb.node(
            'taskblaster.testing.post_process',
            tasks=self.generate_wfs_from_list.results,
        )


@tb.workflow
class GeneratedWorkflowWithDot:
    inputs = tb.var()  # list of input vars

    @tb.dynamical_workflow_generator({'results': '*/hello'})
    def generate_wfs_from_list(self):
        return tb.node(thetask, inputs=self.inputs)

    @tb.task
    def depends_on_generate(self):
        return tb.node(
            'taskblaster.testing.post_process',
            tasks=self.generate_wfs_from_list.results,
        )


@tb.dynamical_workflow_generator_task
def failing_init(fail_if_true):
    yield 'first_works', GeneratedWorkflow(inputs=['first'])
    yield 'first_works2', GeneratedWorkflow(inputs=['first2'])
    if fail_if_true:
        raise ValueError('Failing on purpose to test failing init task')
    yield 'second_missing', GeneratedWorkflow(inputs=['missing'])


@tb.workflow
class NestedGeneratedWorkflow:
    inputs = tb.var()

    @tb.dynamical_workflow_generator({'results': '**'})
    def generate_nested_wfs_from_list(self):
        return tb.node(nestedtask, inputs=self.inputs)


@tb.workflow
class DependingGeneratedWorkflow:
    inputs = tb.var()

    @tb.dynamical_workflow_generator({'results': '**'})
    def generate_depending_wfs_from_list(self):
        return tb.node(dependingtask, inputs=self.inputs)


def test_depending_workflow_generator(tool):
    wf = DependingGeneratedWorkflow(inputs='A')
    tool.workflow(wf)
    tool.run()
    tool.count(done=22, fail=9, cancel=10)
    assert (
        tool.task_hash()
        == 'e820f4db38f5cfce3c2c4f3488104a2aa0f25fbd5ef2e099e201c7478c493be1'
    )


def test_nested_workflow_generator(tool):
    wf = NestedGeneratedWorkflow(inputs=[['A', 'B', 'C'], ['A', 'B', 'C']])
    tool.workflow(wf)
    tool.run()
    tool.count(done=50, fail=18, cancel=18)
    assert (
        tool.task_hash()
        == 'a6cde6a0bac8dff40d23c8ed986baecf7777a3a8779236e113e18b07ea40352e'
    )


def test_workflow_generator_init_failing(tool):
    tool.workflow(FailingInitWorkflow(fail_if_true=True))
    tool.run()
    tool.count(fail=1, cancel=1)
    tool.unrun()

    tool.workflow(FailingInitWorkflow(fail_if_true=False))
    tool.count(new=2)


# Test so that basic wf generator works with and without dots in
# folder names
@pytest.mark.parametrize('with_dot', [True, False])
def test_workflow_generator(tool, with_dot):
    if with_dot:
        wf = GeneratedWorkflowWithDot(inputs=['inputA', 'inputB', 'inputC'])
    else:
        wf = GeneratedWorkflow(inputs=['inputA', 'inputB', 'inputC'])
    tool.workflow(wf)
    tool.run()
    tool.count(fail=9, done=24, cancel=9, new=0)

    assert (
        tool.task_hash()
        == '21abca43c1518b94d403e823c233042359ca61628e1eba124828608bcb483b65'
    )


@tb.workflow
class LoopedWorkflowGenerator:
    iterations = tb.var(4)

    @tb.jump('iterate')
    @tb.task
    def count(self):
        return tb.node('define', obj=self.iterations)

    @tb.branch('iterate', loop=True)
    @tb.dynamical_workflow_generator({'results': '**'})
    def generator_task(self):
        return tb.node(
            looped_generator,
            ntasks=self.Phi(entry=self.count, iterate=self.count_tasks),
        )

    @tb.branch('iterate', loop=True)
    @tb.task
    def count_tasks(self):
        return tb.node(count_tasks, tasks=self.generator_task.results)

    @tb.branch('iterate', loop=True)
    @tb._if(true='iterate', false='final')
    @tb.task
    def check_results(self):
        return tb.node(check_results, results=self.generator_task.results)

    @tb.branch('final')
    @tb.task
    def final(self):
        return tb.node('define', obj=None)


def test_dynamical_workflow_generator_in_a_loop(tool):
    for i in range(5):
        wf = LoopedWorkflowGenerator()
        tool.workflow(wf)
        tool.run()
    tool.ls()
    assert (
        tool.task_hash()
        == 'aecdf4676f00e0d4ad3da6ff87271f2d1c303cde4978ec0e23ee245c599d641d'
    )
