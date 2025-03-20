import pytest


@pytest.fixture
def frozen(tool):
    wf = tool.simpleworkflow(msg='hello')
    tool.workflow(wf)
    with tool.repo:
        tool.repo.tree('tree/fail').freeze(why='because')


def test_freeze(tool, frozen):
    with tool.repo:
        all_frozen_info = tool.frozen_tasks()

    assert all_frozen_info['fail'] == ['because']
    assert {'fail', 'dependsonfail', 'dependsondependsonfail'} < set(
        all_frozen_info
    )

    for name, why in all_frozen_info.items():
        if name == 'fail':
            continue
        for reason in why:
            assert reason.startswith('parent:')
            _, parent = reason.split(':')
            assert parent in all_frozen_info


def test_unfreeze(tool, frozen):
    with tool.repo:
        frozen_originally = tool.frozen_tasks()
        assert len(frozen_originally) > 3  # sanity check

        # Freeze another subtree:
        tool.repo.tree('tree/dependsondependsonfail').freeze(why='because')
        # frozen_many = frozen_tasks(tool)

        tool.repo.tree('tree/fail').unfreeze(why='because')

        # We are unfreezing a specific task for "because" reason,
        # which should not affect other tasks (even descendants) that
        # are frozen for the same or another reason.
        frozen_finally = tool.frozen_tasks()
        assert frozen_finally['dependsondependsonfail'] == ['because']


def test_unfreeze_nonexistent(tool, frozen):
    # Unfreezing the wrong name, or a name that includes no frozen
    # tasks, has no effect:
    with tool.repo:
        frozen_tasks = tool.frozen_tasks()
        tool.repo.tree('tree/fail').unfreeze(why='hello')
        assert tool.frozen_tasks() == frozen_tasks
