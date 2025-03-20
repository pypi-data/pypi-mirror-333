import taskblaster as tb


def hello(whom):
    return f'hello, {whom}!'


@tb.workflow
class SubSubWorkflow:
    msg = tb.var()

    @tb.task
    def subsubhello(self):
        return tb.node(hello, whom='subsubworld')


@tb.workflow
class MySubWorkflow:
    msg = tb.var()

    @tb.task
    def subhello(self):
        return tb.node(hello, whom='subworld')

    @tb.subworkflow
    def subsubworkflow(self):
        return SubSubWorkflow(msg=self.msg)


@tb.workflow
class HelloWorkflow:
    @tb.task
    def hello(self):
        return tb.node(hello, whom='world')

    @tb.subworkflow
    def mysubworkflow(self):
        return MySubWorkflow(msg=self.hello)


def test_workflow_serialization(tool):
    tool.workflow(HelloWorkflow(), add_workflows_to_registry=True)
    with tool.repo:
        workflows = dict(tool.repo.registry.workflows)

    assert set(workflows) == {
        '',
        'mysubworkflow',
        'mysubworkflow/subsubworkflow',
    }

    # Root workflow has root as source:
    assert workflows[''].source == ''
    assert workflows['mysubworkflow'].source == ''
    assert workflows['mysubworkflow/subsubworkflow'].source == 'mysubworkflow'
