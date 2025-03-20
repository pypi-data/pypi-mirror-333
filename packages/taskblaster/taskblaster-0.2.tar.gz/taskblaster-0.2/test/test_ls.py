import pytest

from taskblaster.listing import TaskListing


@pytest.fixture
def columns():
    return ''.join(TaskListing.all_columns())


def test_ls(simplerepo, columns):
    with simplerepo:
        lines = [*simplerepo.tree().ls(columns=columns)]
    print(lines)


def test_ls_empty(repo, columns):
    assert repo.registry.index.count() == 0
    lines = [*repo.tree().ls(columns=columns)]
    assert set(lines[0].split()) >= {'info', 'state', 'folder'}
    assert set(lines[1]) == {'─', ' '}
    assert len(lines) == 2


def test_ls_nonempty(tool, simplerepo):
    lines = [line for line in tool.ls().splitlines() if 'tree/' in line]
    assert len(lines) > 5  # "there are at least a few tasks"


def test_ls_outside_tree(simplerepo, columns):
    """Test that ls does not crash if there are tasks outside cwd."""
    # (The repo fixture restores cwd)
    path = simplerepo.tree_path / 'arbitrary_dir'
    path.mkdir()
    with simplerepo:
        print([*simplerepo.tree().ls(columns=columns, fromdir=path)])


def test_ls_across_subdirs(simplerepo, columns):
    import click

    path = simplerepo.tree_path / 'subworkflow'

    with simplerepo:
        lines = [
            *simplerepo.tree().ls(parents=True, columns=columns, fromdir=path)
        ]

    found = False
    for line in lines:
        tokens = click.unstyle(line).split()
        if '../ok' in tokens:
            found = True
            break

    assert found
