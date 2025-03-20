def test_rename_import_path(tool):
    tool.workflow(tool.simpleworkflow())
    tasks = tool.select('*')

    def get_target_functions(names):
        cache = tool.repo.cache
        with tool.repo:
            return {
                name: cache.json_protocol.deserialize_node(
                    cache.registry.inputs[name], name
                ).target
                for name in names
            }

    old_targets = get_target_functions(task.name for task in tasks)

    old_targetfunc = 'ok'
    new_targetfunc = 'new.target.function'

    tool.command(
        f'special rename-import-path --force {old_targetfunc} {new_targetfunc}'
    )

    new_targets = get_target_functions(task.name for task in tasks)

    assert old_targetfunc in old_targets.values()
    assert old_targetfunc not in new_targets.values()
    assert new_targetfunc not in old_targets.values()
    assert new_targetfunc in new_targets.values()

    for task in tasks:
        assert (old_targets[task.name] == old_targetfunc) == (
            new_targets[task.name] == new_targetfunc
        )
