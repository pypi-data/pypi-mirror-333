import pytest

import taskblaster as tb
from taskblaster.parallel import SerialCommunicator
from taskblaster.repository import Repository, WorkerSpecification
from taskblaster.worker import TaskContext, inject_context_vars


@tb.workflow
class MyWorkflow:
    @tb.task(tags={'helloworld'})
    def mytask(self):
        return tb.node(mytask, a=2, b=3)


@tb.context
def mytask(context, a, b):
    assert context.rules.tags == {'helloworld'}
    for comm in [context.comm, context.tb_comm]:
        assert comm.rank == 0
        assert comm.size == 1
    return a + b + context.c


class MyContextClass(tb.WorkerContext):
    @property
    def c(self):
        return 42


class MyRepository(Repository):
    def context_class(self):
        return MyContextClass


def tb_init_repo(root):
    return MyRepository(root)


@pytest.fixture
def tool(testdir):
    from conftest import Tool

    repo = MyRepository.create(testdir, modulename=__name__)
    return Tool(repo)


def test_context_object(tool):
    tool.workflow(MyWorkflow())
    tool.run(rules=WorkerSpecification(tags={'helloworld'}))
    assert tool.peek('mytask') == 2 + 3 + 42


class DummyComm:
    rank = 17
    size = 42


@pytest.fixture
def context():
    return TaskContext(DummyComm(), SerialCommunicator(), 'dummyname')


def test_no_injection(context):
    """ "Test that injection works (does nothing) on plain function."""

    def ordinary_function(n):
        return n + 1

    kwargs = inject_context_vars(ordinary_function, {'n': 4}, context)
    assert ordinary_function(**kwargs) == 5


def test_context_injection(context):
    """Test that injection of the whole context object works."""

    @tb.context
    def context_function(context, n):
        return context, n + 1

    kwargs = inject_context_vars(context_function, {'n': 4}, context)
    context, five = context_function(**kwargs)
    assert five == 5
    assert context.tb_comm.rank == 0
    assert context.tb_comm.size == 1
    assert context.comm.rank == 17
    assert context.comm.size == 42


def test_comm_injection(context):
    """Test that injection of single context variable ('comm') works."""

    @tb.context('comm')
    def comm_function(comm, n):
        return comm, n + 1

    kwargs = inject_context_vars(comm_function, {'n': 4}, context)
    comm, five = comm_function(**kwargs)
    assert five == 5
    assert comm.rank == 17
    assert comm.size == 42


@tb.context('comm')
def task_with_comm(comm, otherinput):
    print(comm.rank)
    return otherinput


@tb.context('comm')
def task_with_comm2(otherinput, comm):
    print(comm.rank)
    return otherinput


@tb.workflow
class ContextWF:
    inputs = tb.var()  # list of input vars

    @tb.task
    def task1(self):
        return tb.node(task_with_comm, otherinput=self.inputs)

    @tb.task
    def task2(self):
        return tb.node(task_with_comm2, otherinput=self.inputs)


# Two integration teststesting so that comm is
# properly passed in wf
def test_comm_in_wf(tool):
    wf = ContextWF(inputs=['hi'])
    tool.workflow(wf)
    tool.run()
    tool.count(done=2, fail=0, cancel=0)
