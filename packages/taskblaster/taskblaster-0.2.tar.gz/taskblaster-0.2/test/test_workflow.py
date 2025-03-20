import pytest

import taskblaster as tb
from taskblaster.testing import GeneratedWorkflow, WorkflowSleep


@pytest.fixture
def bigrepo(tool):
    inputs = ['hi1', 'hi2', 'hi3']
    wf = GeneratedWorkflow(inputs=inputs)
    tool.workflow(wf)
    tool.repo.run_worker(tree=['tree/generate_wfs_from_list/init'])
    return tool.repo


def test_min_worker_wall_time(tool):
    from taskblaster.repository import WorkerSpecification

    wf = WorkflowSleep(msg='hi')
    tool.workflow(wf)

    # Test pick up job when wall time is sufficient
    tool.run(rules=WorkerSpecification(wall_time=7))

    tool.count(done=2)
    tool.unrun()
    tool.count(new=2)

    rules = WorkerSpecification(wall_time=1)

    # Test do not pick up job when wall time is too short
    tool.run(rules=rules)
    tool.count(done=1, new=1)

    tool.run(rules=rules)
    tool.count(done=2)


def add(a, b):
    return a + b


def multiply(a, b):
    return a * b


@tb.workflow
class Arithmetics:
    @tb.task
    def add(self):
        return tb.node(add, a=2, b=3)

    @tb.task
    def mul(self):
        return tb.node(multiply, a=self.add, b=4)


def test_workflow(tool):
    tool.workflow(Arithmetics())
    tool.run()

    assert tool.peek('mul') == 20
    digest = 'fa9668d4f8f7cf3cbfabbfb40b42508f13df6b0a352bb0c0f6ac3552f62cf755'
    assert tool.task_hash() == digest


def test_generate_wf(tool, bigrepo):
    tool.count(new=41, done=1)


def test_fix_registry(bigrepo, tool):
    from taskblaster.registry import topological_depth_table

    with bigrepo:
        bigrepo.registry.conn.execute('drop table topological_depth;')
        topological_depth_table(
            bigrepo.registry.conn, read_only=False
        ).create_if_not_exists()
    inputs = ['hi1', 'hi2', 'hi3']
    wf = GeneratedWorkflow(inputs=inputs)
    with pytest.raises(KeyError):
        tool.workflow(wf)
    tool.command('special repair --force')
    wf = GeneratedWorkflow(inputs=inputs)
    tool.workflow(wf)


def test_create_cancelled(tool):
    from taskblaster.state import State

    repo = tool.repo
    wf = tool.simpleworkflow(msg='hello')

    tool.workflow(wf)
    tool.run()

    with repo:
        nodename = 'dependsondependsonfail'
        print(repo.tree().stat())
        node = repo.registry.index.node(nodename)
        assert node.state == State.cancel

        _, confirm = repo.tree([f'tree/{nodename}']).remove()
        confirm()
        assert not repo.registry.contains(nodename)

    wf = tool.simpleworkflow(msg='hello')
    tool.workflow(wf)

    with repo:
        node = repo.registry.index.node(nodename)
        assert node.state == State.cancel
        assert (
            repo.registry.index.task_name_hash()
            == '3b311971555d55902e5268c5c2a98d33df702eb1b3f6cea8ba3946faa8c85539'  # noqa: E501
        )
