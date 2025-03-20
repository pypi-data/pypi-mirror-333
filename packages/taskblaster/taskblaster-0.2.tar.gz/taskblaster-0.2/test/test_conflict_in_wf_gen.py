from taskblaster.state import State
from taskblaster.testing import DynamicalGeneratedComplexWorkflow


def test_complex_conflict_handling(tool):
    def run_wf(fc1='1', fc2='2'):
        tool.workflow(
            DynamicalGeneratedComplexWorkflow(
                msg=['hi1'], fail_cond1=fc1, fail_cond2=fc2
            )
        )

    def have_new():
        run_wf()
        with tool.repo as repo:
            stat = repo.tree('tree').stat()
        print(stat.counts)
        new = stat.counts[State.new]
        return new > 0

    def run_all():
        max_iter = 100
        while have_new():
            tool.run()
            max_iter -= 1
            if max_iter == 0:
                raise Exception('Infinite loop.')

    def count_tree(tree):
        with tool.repo as repo:
            stat = repo.tree('tree/generate_wfs_from_list').stat()
        return sum(stat.counts.values())

    run_all()
    tool.count(done=7, fail=1, cancel=8)

    # Changing input should create a conflict which
    # should freeze descendents
    run_wf(fc2='3')
    with tool.repo:
        frozen = tool.frozen_tasks()

    # Since there is a conflict in the dwg init all generated
    # tasks are frozen + 1 additional task where there is also
    # a conflict
    length = count_tree('tree/generate_wfs_from_list')

    # Number of frozen tasks should be number of generated tasks + 4
    # (depends_on_ok, depends_on_result0, depends_on_all and cond_ok)
    assert len(frozen) == length + 4

    # resolve one conflict
    tool.resolve_conflict(tree='tree/generate_wfs_from_list/init')
    with tool.repo:
        frozen = tool.frozen_tasks()
    # one conflict remains which should result in one frozen task
    assert len(frozen) == 1

    # resolve final conflict
    tool.resolve_conflict()
    with tool.repo:
        frozen = tool.frozen_tasks()
    # one conflict remains which should result in one frozen task
    assert len(frozen) == 0
