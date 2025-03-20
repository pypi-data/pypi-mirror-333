import pytest

import taskblaster as tb
from taskblaster.state import State


def nil(x=0):
    pass


@tb.workflow
class TwoTasks:
    @tb.task
    def task1(self):
        return tb.node(nil)

    @tb.task
    def task2(self):
        return tb.node(nil, x=self.task1)

    @tb.task
    def task3(self):
        return tb.node(nil, x=self.task1)


@pytest.mark.parametrize(
    'arg, expected_queued',
    [
        ('', ['task1', 'task2', 'task3']),  # Submit everything
        ('tree/task1', ['task1']),
        ('tree/task2', ['task1', 'task2']),
    ],
)
def test_submit(tool, arg, expected_queued):
    tool.workflow(TwoTasks())
    tool.submit(arg)
    tasks = tool.select(states={State.queue})
    assert sorted(task.name for task in tasks) == expected_queued
