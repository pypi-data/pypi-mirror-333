import pytest

import taskblaster as tb


def run_algorithm(a: int):
    """Python version of our algorithm"""
    iterations = 0
    if a == 0:
        b = a
    else:
        while True:
            b = increment(a)
            iterations += 1
            if abs_sum_is_one(a, b):
                break
            a = b
    assert b == 0
    return iterations


def increment(a: int) -> int:
    if a < 0:
        return a + 1
    elif a > 0:
        return a - 1
    return a


def abs_sum_is_one(a: int, b: int) -> bool:
    assert a != b
    return abs(a + b) == 1


@tb.workflow
class SubWf:
    a = tb.var()

    @tb.task
    def b(self):
        return tb.node(increment, a=self.a)


@tb.workflow
class MainWf:
    start = tb.var()

    @tb.branch('entry')
    @tb._if(true='final', false='iterate')
    @tb.task
    def start_iteration(self):
        return tb.node(is_zero, num=self.start)

    @tb.branch('iterate', loop=True)
    @tb.subworkflow
    def iterate(self):
        return SubWf(a=self.state)

    @tb.branch('iterate', loop=True)
    @tb._if(true='final', false='iterate')
    @tb.task
    def stop_iteration(self):
        return tb.node(abs_sum_is_one, b=self.iterate.b, a=self.state)

    @property
    def state(self):
        return self.Phi(entry=self.start, iterate=self.iterate.b)

    @tb.branch('final')
    @tb.fixedpoint
    @tb.task
    def test(self):
        return tb.node(assert_zero, num=self.state)


def is_zero(num: int) -> bool:
    return num == 0


def assert_zero(num: int) -> None:
    assert num == 0


@pytest.mark.parametrize('a', range(4))
def test_reference_to_subworkflow_inputs(a, tool):
    # Run algorithm in while-loop
    iterations = run_algorithm(a)
    ntasks = 2 + 2 * iterations

    # Run algorithm using wf
    for _ in range(2 + iterations):
        tool.workflow(MainWf(start=a))
        tool.run()
    tool.count(new=0, queue=0, done=ntasks)
