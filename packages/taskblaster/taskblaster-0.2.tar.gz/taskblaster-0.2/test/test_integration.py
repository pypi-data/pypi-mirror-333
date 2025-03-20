import pytest

from taskblaster.state import State


def run_wf_with_inp(tool, WorkflowClass, msgs, fail_cond1='1', fail_cond2='2'):
    def workflow(rn):
        for i, msg in enumerate(msgs):
            rn2 = rn.with_subdirectory(str(i))
            wf = WorkflowClass(
                msg=msg, fail_cond1=fail_cond1, fail_cond2=fail_cond2
            )
            rn2.run_workflow(wf)

    tool.workflow_function(workflow)


def test_run_all(simplerepo, tool):
    with simplerepo:
        stats0 = simplerepo.tree().stat()

    ntasks = stats0.ntasks

    assert stats0.counts[State.new] == ntasks

    tool.run()

    with simplerepo:
        stats = simplerepo.tree().stat()
    assert stats.ntasks == ntasks

    print(stats)

    end_states = [State.done, State.fail, State.cancel]

    for state in end_states:
        assert stats.counts[state] > 0

    assert sum(stats.counts[state] for state in end_states) == ntasks


def test_realistic_wf(tool):
    from taskblaster.testing import ComplexWorkflow

    def run_wf1():
        run_wf_with_inp(tool, ComplexWorkflow, ['hi0', 'hi1', 'hi2'])

    run_wf1()
    tool.run()

    def check1():
        tool.count('tree/0', done=6)

    def check2():
        tool.count('tree/1', done=1, fail=1, cancel=4)

    def check3():
        tool.count('tree/2', done=4, fail=1, cancel=1)

    def checkall():
        check1()
        check2()
        check3()

    checkall()

    # Make conflict
    def run_wf2():
        run_wf_with_inp(tool, ComplexWorkflow, ['hi0', 'hi3', 'hi2'])

    run_wf2()

    # Check so that states have not changed
    checkall()

    # Check so that conflict is correct
    tool.check_conflict(conflicts=1, resolved=0)

    # Check so that conflict can be resolved
    tool.resolve_conflict()
    tool.check_conflict(conflicts=0, resolved=1)

    # Check so that conflict is removed if orig wf is run
    run_wf1()
    tool.check_conflict(conflicts=0, resolved=0)

    # unrun failed task and check that descendants are updated correctly
    tool.unrun('tree/1/cond_ok')
    tool.count('tree/1/cond_ok', cancel=0)
    check1()
    check3()

    # do tb workflow with new input that will not crash
    def run_wf3():
        run_wf_with_inp(tool, ComplexWorkflow, ['hi0', 'hi0', 'hi0'])

    run_wf3()

    tool.check_conflict(conflicts=2)

    for name in tool.where_conflict():
        tool.unrun(f'tree/{name}')

    tool.count(fail=0)
    tool.check_conflict(conflicts=0)

    run_wf3()
    tool.run()
    tool.count(done=18, fail=0)


@pytest.mark.parametrize(
    'wf', ['DynamicalGeneratedComplexWorkflow', 'GeneratedComplexWorkflow']
)
def test_realistic_wf_generator(tool, wf):
    """Tests both dynamical and statically generated workflow
    A dynamical generated wf will have two extra tasks (thus 2)
    """

    from taskblaster.testing import (
        DynamicalGeneratedComplexWorkflow,
        GeneratedComplexWorkflow,
    )

    # Different number of tasks in diffent wfs
    if 'Dynamical' in wf:
        dynamical = 1
        WorkflowClass = DynamicalGeneratedComplexWorkflow
    else:
        dynamical = 0
        WorkflowClass = GeneratedComplexWorkflow

    def run_wf1():
        run_wf_with_inp(tool, WorkflowClass, [['hi0', 'hi1']])

    run_wf1()
    tool.run()
    tool.count(done=14 + dynamical, fail=1, cancel=6)

    def run_wf2():
        run_wf_with_inp(tool, WorkflowClass, [['hi0', 'hi3']], fail_cond1='5')

    run_wf2()

    tool.ls()
    # States should not have changed
    tool.count(done=14 + dynamical, fail=1, cancel=6)

    # Check conflict state
    # check_conflict(6, 0)
    # XXX I do not think this behavoiur is entirely correct
    # Currently the init task of the dynamical workflow is set to
    # conflict, but unrunning the init does not unrun the tasks that
    # actually had a conflict.
    # I have made a seperate test that fails for this and will update
    # this test once we have decided what should happen
    tool.check_conflict(3 + dynamical, 0)
    tool.resolve_conflict()

    # Check conflict state updated to resolved
    # check_conflict(0, 6)
    # TEST
    tool.check_conflict(0, 3 + dynamical)
    tool.unrun('tree/0/generate_wfs_from_list/1/cond_ok')

    # Check so that states were properly unrun
    tool.count(done=14 + dynamical, new=7)
    tool.run()

    # check so that there is still failures
    # due to resolved conflict
    tool.count(done=14 + dynamical, fail=1, cancel=6)

    # unrun tree and rerun
    tool.unrun()
    run_wf2()
    tool.run()

    # Check so that all tasks are done
    tool.count(done=21 + dynamical, fail=0)


def test_wf_generator_depend_on_nonexisting_task(tool):
    from taskblaster.testing import GeneratedWrongWorkflow

    run_wf_with_inp(tool, GeneratedWrongWorkflow, [['hi0', 'hi1']])
    tool.run()
    tool.count('tree/0/depends_on_nonexisting', done=1)


@pytest.fixture
def preparedrepo(tool):
    """Test so that tb unrun tree marks all tasks of dynamical wf as new."""
    from taskblaster.testing import DynamicalGeneratedComplexWorkflow as WF

    run_wf_with_inp(tool, WF, [['hi0', 'hi1']])
    tool.run()
    run_wf_with_inp(tool, WF, [['hi0', 'hi3']], fail_cond1='5')


def test_unrun_all(preparedrepo, tool):
    tool.unrun()
    tool.count(new=22, done=0, fail=0)


def test_unrun_init(tool):
    """Test so that tb unrun task that generates the input to
    dynamical workflow, unruns all task of the dynamical workflow
    and all tasks that depend on the dynamical wf"""
    from taskblaster.testing import DynamicalGeneratedComplexWorkflow as WF

    run_wf_with_inp(tool, WF, [['hi0', 'hi1']])
    tool.run()

    # Unrun task that wf generator depends on
    tool.unrun('tree/0/gen_input')
    tool.count(done=2, new=20)

    # Unrun wf generator init task
    tool.run()
    tool.unrun('tree/0/generate_wfs_from_list/init')
    tool.count(done=3, new=19)
