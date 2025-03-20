import taskblaster as tb


def myaction(record):
    # In this test, we do not run the task and its output is therefore None
    # (thus being indistinguishable from whether it ran and returned None)
    return 'hello'


@tb.actions(myaction=myaction)
def myfunc():
    return 'potato'


@tb.workflow
class MyWorkflow:
    @tb.task
    def actionable_task(self):
        return tb.node(myfunc)

    @tb.task
    def actionable_output_task(self):
        return tb.node(task_with_output_action)


def run_action(tool, action):
    with tool.repo:
        return tool.repo.view(['tree'], action)


def test_action(tool):
    tool.workflow(MyWorkflow())
    # Task did not run, so myaction returns None as output
    assert run_action(tool, 'myaction') == ['hello']


def task_with_output_action():
    return OutputTypeWithAction('potato')


def my_output_action(record):
    return f'hello {record.output.msg}'


@tb.actions(output_action=my_output_action)
class OutputTypeWithAction:
    def __init__(self, msg):
        self.msg = msg

    def tb_encode(self):
        return self.msg

    @classmethod
    def tb_decode(cls, msg):
        return cls(msg)


def test_output_action(tool):
    # First let's be sure the @actions decorator worked:
    assert (
        OutputTypeWithAction.__tb_actions__['output_action']
        is my_output_action
    )

    # We can only run the action once task is done, so this is a no-op:
    tool.workflow(MyWorkflow())
    assert run_action(tool, 'output_action') == []

    tool.run()

    from taskblaster.util import get_task_actions

    output = tool.peek('actionable_output_task')
    assert 'output_action' in get_task_actions(my_output_action, output)

    assert run_action(tool, 'output_action') == ['hello potato']
