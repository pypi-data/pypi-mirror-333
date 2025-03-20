from abc import ABC, abstractmethod

import pytest

import taskblaster as tb


@tb.workflow
class BaseSubWf(ABC):
    a = tb.var()
    b = tb.var()

    @tb.task
    @abstractmethod
    def result(self):
        """Should contain `a + b`."""
        raise NotImplementedError


@tb.workflow
class BaseMainWf(ABC):
    a = tb.var()
    b = tb.var()
    c = tb.var()
    expected_result = tb.var()

    @tb.branch('entry')
    @tb.jump('iterate')
    @tb.subworkflow
    @abstractmethod
    def a_plus_b(self) -> BaseSubWf:
        raise NotImplementedError

    @tb.branch('iterate', loop=True)
    @tb.task
    def double(self):
        return tb.node(
            double,
            num=self.Phi(entry=self.a_plus_b.result, iterate=self.double),
        )

    @tb.branch('iterate', loop=True)
    @tb._if(true='final', false='iterate')
    @tb.task
    def stop_iteration(self):
        return tb.node(greater_than, num=self.double, ref=self.c)

    @tb.branch('final')
    @tb.task
    def test(self):
        return tb.node(assert_equal, num=self.double, ref=self.expected_result)


def add(a: int, b: int) -> int:
    return a + b


def double(num: int) -> int:
    return 2 * num


def greater_than(num: int, ref: int) -> bool:
    return num > ref


def assert_equal(num: int, ref: int) -> None:
    assert num == ref


@tb.workflow
class SimplestSubWf(BaseSubWf):
    @tb.task
    def result(self):
        return tb.node(add, a=self.a, b=self.b)


@tb.workflow
class SimplerSubWf(BaseSubWf):
    @tb.branch('entry')
    @tb.jump('final')
    @tb.task
    def in_between(self):
        return tb.node('define', obj=self.a)

    @tb.branch('final')
    @tb.task
    def result(self):
        return tb.node(add, a=self.in_between, b=self.b)


@tb.workflow
class NestedSubWf(BaseSubWf):
    @tb.subworkflow
    def actual_work(self):
        return SimplestSubWf(a=self.a, b=self.b)

    @tb.task
    def result(self):
        return tb.node('define', obj=self.actual_work.result)


@tb.workflow
class ConditionalSubWf(BaseSubWf):
    @tb.task
    def two_a(self):
        return tb.node(add, a=self.a, b=self.a)

    @tb._if(true='final', false='redo')
    @tb.task
    def compare(self):
        return tb.node(is_equal, a=self.a, b=self.b, aplusb=self.two_a)

    @tb.branch('redo')
    @tb.jump('final')
    @tb.task
    def aplusb(self):
        return tb.node(add, a=self.a, b=self.b)

    @tb.branch('final')
    @tb.fixedpoint
    @tb.task
    def result(self):
        return tb.node(
            'define', obj=self.Phi(entry=self.two_a, redo=self.aplusb)
        )


def is_equal(a: int, b: int, aplusb: int) -> bool:
    return a + b == aplusb


@pytest.mark.parametrize(
    'cls',
    [SimplestSubWf, SimplerSubWf, NestedSubWf, ConditionalSubWf],
)
def test_jump_to_while(cls, tool):
    a, b, c = 2, 4, 10
    # Run algorithm in while-loop
    result = 2 * (a + b)
    iterations = 0
    while result <= c:
        result *= 2
        iterations += 1

    # Define workflow
    @tb.workflow
    class MainWf(BaseMainWf):
        @tb.branch('entry')
        @tb.jump('iterate')
        @tb.subworkflow
        def a_plus_b(self):
            return cls(a=self.a, b=self.b)

    # Calculate the number of steps in the algorithm
    subiterations = 1
    if cls is SimplestSubWf:
        ntasks = 4
    elif cls is ConditionalSubWf:
        ntasks = 6 if a == b else 7
        subiterations += 1
    else:
        ntasks = 5
    ntasks += 2 * iterations

    def run_algorithm():
        for _ in range(1 + subiterations + iterations):
            tool.workflow(MainWf(a=a, b=b, c=c, expected_result=result))
            tool.run()

    run_algorithm()
    tool.count(new=0, queue=0, done=ntasks)

    def verify_fixed_point(task):
        assert tool.get_dependencies(task) == (0, 1)
        with tool.repo:
            ancestry = tool.repo.registry.ancestry
            assert ancestry.ancestors(task) == {'__tb_unreachable__'}

    # Test unrunning with reset external: True
    if cls is ConditionalSubWf:
        taskhash = tool.task_hash()
        tool.unrun('tree/a_plus_b/two_a')
        tool.count(new=5)
        # The result task is a fixed point, and it should have been reset
        # To this end, make sure it has no ancestors
        verify_fixed_point('a_plus_b/result')
        run_algorithm()
        assert taskhash == tool.task_hash()
        tool.unrun('tree/a_plus_b/aplusb')
        tool.count(new=4)
        run_algorithm()
        assert taskhash == tool.task_hash()
