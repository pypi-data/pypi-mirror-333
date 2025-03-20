from taskblaster.state import State


def test_clone_subtree(tool, tmp_path_factory, tmp_path):
    tool.workflow(tool.simpleworkflow())
    tool.run()

    # Note: We get a deadlock if trying to clone into repo subdirectory.
    clonepath = tmp_path_factory.mktemp('tmp-clonepath')

    tasks = tool.select_topological('ok2')
    names = ['ok', 'ok2']
    assert [task.name for task in tasks] == names

    tool2 = tool.clone(clonepath, 'tree/ok2')

    cloned_repo = tool2.repo
    tasks2 = tool2.select('*')
    assert len(tasks2) == 2
    assert [task.name for task in tasks2] == names
    with cloned_repo:
        for task in tasks2:
            assert task.state == State.done
            outputfile = cloned_repo.cache.entry(task.name).outputfile
            assert outputfile.exists()
