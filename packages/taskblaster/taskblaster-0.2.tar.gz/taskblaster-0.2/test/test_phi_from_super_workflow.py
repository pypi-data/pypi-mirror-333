from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from itertools import product

import pytest

import taskblaster as tb


@tb.workflow
class BaseSuperWf(ABC):
    a = tb.var()
    b = tb.var()
    expected_result = tb.var()

    @tb.branch('entry')
    @tb.jump('enter_while')
    @tb.task
    def a_minus_b(self):
        return tb.node(subtract, a=self.a, b=self.b)

    @tb.branch('enter_while')
    @tb._if(true='final', false='iterate')
    @tb.task
    def is_negative(self):
        return tb.node(is_negative, num=self.a_minus_b)

    @tb.branch('iterate', loop=True)
    @tb.task
    def a_minus_multiple_bs(self):
        return tb.node(
            subtract,
            a=self.Phi(
                enter_while=self.a_minus_b, iterate=self.a_minus_multiple_bs
            ),
            b=self.b,
        )

    @tb.branch('iterate', loop=True)
    @tb._if(true='final', false='iterate')
    @tb.task
    def stop_iteration(self):
        return tb.node(is_negative, num=self.a_minus_multiple_bs)

    @tb.branch('final')
    @tb.subworkflow
    def negate_via_subwf(self):
        """Should create SubWf with a `negate` task."""
        return self._negate_via_subwf()

    @abstractmethod
    def _negate_via_subwf(self):
        raise NotImplementedError

    @property
    def result(self):
        return self.negate_via_subwf.negate

    @tb.branch('final')
    @tb.task
    def test(self):
        return tb.node(assert_equal, num=self.result, ref=self.expected_result)


@tb.workflow
class SimpleSubWf:
    num = tb.var()

    @tb.task
    def negate(self):
        return tb.node(negate, num=self.num)


class SimpleReferencingSuperWf(BaseSuperWf):
    def _negate_via_subwf(self):
        # NB: In this case we are not sensitive to tb.Phi vs. self.Phi
        phi = self.Phi(
            enter_while=self.a_minus_b,
            iterate=self.a_minus_multiple_bs,
            debug=True,
        )
        return SimpleSubWf(num=phi)


@dataclass
class DataContainer:
    num: int

    def tb_encode(self):
        return dict(num=self.num)

    @classmethod
    def tb_decode(cls, dct):
        return cls(**dct)


@tb.workflow
class AdvancedSubWf:
    data = tb.var()  # DataContainer

    @tb.task
    def negate(self):
        return tb.node(negate, num=self.data.num)


class AdvancedReferencingSuperWf(BaseSuperWf):
    def _negate_via_subwf(self):
        # NB: When constructing a subworkflow, which as input takes a
        # taskblaster variable with a Phi operator inside it, we need to use
        # self.Phi in order to correctly resolve the operator.

        # For some reason error was triggered whenever Phi was nested inside
        # a container as [Phi(...)] or DataContainer(Phi(...)),
        # but not when Phi was passed directly as above.
        return AdvancedSubWf(
            data=DataContainer(
                num=self.Phi(
                    enter_while=self.a_minus_b,
                    iterate=self.a_minus_multiple_bs,
                )
            )
        )


def subtract(a: int, b: int) -> int:
    return a - b


def negate(num: int) -> int:
    return -num


def is_negative(num: int) -> bool:
    return num < 0


def assert_equal(num: int, ref: int) -> None:
    assert num == ref


@pytest.mark.parametrize(
    'a,b,cls',
    product(
        [0, 1, 3],
        [1, 6],
        [SimpleReferencingSuperWf, AdvancedReferencingSuperWf],
    ),
)
def test_phi_from_superworkflow(a, b, cls, tool):
    """Tests that subworkflows can resolve Phi operators from their
    superworkflows, also when Phi is passed inside a taskblaster variable.

    As a test algorithm, we take input integers `a` and `b`, subtract `b` from
    `a` until the result becomes negative, after which we negate it. The
    iterative subtraction of `b` necessitates a while-loop, why the input to
    the negate task (carried out in the subworkflow) involves a Phi operator.
    """
    # Run algorithm in while-loop
    result = a - b
    iterations = 0
    while result >= 0:
        result -= b
        iterations += 1
    result = -result
    ntasks = 4 + 2 * iterations

    # Run algorithm using wf
    for _ in range(2 + iterations):
        tool.workflow(cls(a=a, b=b, expected_result=result))
        tool.run()
    tool.count(new=0, queue=0, done=ntasks)
