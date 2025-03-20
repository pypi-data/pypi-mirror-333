import taskblaster as tb


def _importpath(func):
    return f'{func.__module__}.{func.__name__}'


def func0():
    """Test function which returns the importname of the "next" function."""
    return _importpath(func1)


def func1():
    return _importpath(func2)


def func2():
    return 'potato'


@tb.workflow
class Workflow:
    target = tb.var()

    @tb.task
    def task1(self):
        """Test dynamic taskname via inputvar."""
        return tb.node(self.target)

    @tb.task
    def task2(self):
        """Test dynamic taskname via reference."""
        return tb.node(self.task1)


@tb.workflow
class NextWorkflow:
    target = tb.var()

    @tb.task
    def task3(self):
        """Test that dynamic target works also in composed workflow."""
        return tb.node(self.target)


def test_dynamic_target(tool):
    # Cannot pass callable to workflow so we need the name:
    target = _importpath(func0)

    wf = Workflow(target=target)
    tool.workflow(wf)
    tool.run()
    assert tool.peek('task1') == _importpath(func1)
    assert tool.peek('task2') == _importpath(func2)

    new_wf = NextWorkflow(target=wf.task2)
    tool.workflow(new_wf)
    tool.run()

    assert tool.peek('task3') == 'potato'
