import pytest

import taskblaster as tb


def interrupt():
    raise tb.TaskBlasterInterrupt('hello')


importname = f'{__name__}.interrupt'


@tb.workflow
class Interrupt:
    @tb.task
    def interrupted(self):
        return tb.node(importname)

    @tb.task
    def does_not_run(self):
        # If this task runs, worker was not interrupted.
        return tb.node(importname)


def test_interrupt(tool):
    """Test that TaskBlasterInterrupt interrupts worker."""
    tool.workflow(Interrupt())
    with pytest.raises(tb.TaskBlasterInterrupt):
        tool.run(['tree/interrupted', 'tree/does_not_run'])
    assert tool.count(fail=1, new=1)
