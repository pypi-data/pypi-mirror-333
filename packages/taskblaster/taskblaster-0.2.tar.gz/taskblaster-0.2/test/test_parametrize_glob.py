import taskblaster as tb


def assert_task(a, b):
    assert a == b - 1


@tb.workflow
class ParametrizedWorkflow:
    material = tb.var()
    relax = tb.var()

    @tb.task
    def check_task(self):
        return tb.node(assert_task, a=self.material, b=self.relax)


def test_totree(tool):
    repo = tool.repo
    materials = {f'mat{i:03d}': i for i in range(3)}
    with repo:
        tb.totree(materials, 'material')(repo.runner())
        assert (
            repo.registry.index.task_name_hash()
            == 'ba61a81f5ea0e6709140341cd3f9c0d58a5e93b5dcc146e1b4a5f997488f0706'  # noqa: E501
        )
        tb.totree(
            {key: value + 1 for key, value in materials.items()}, 'relax'
        )(repo.runner())
        assert (
            repo.registry.index.task_name_hash()
            == 'd363e43f3d31638893aaeefc4c47f63272cd27f2249527003e86b3252eab0fdc'  # noqa: E501
        )

    @tb.parametrize_glob('*/material')
    def workflow(material):
        return ParametrizedWorkflow(
            material=material, relax=material.parent / 'relax'
        )

    with repo:
        workflow(repo.runner())

    tool.run()

    with repo:
        assert (
            repo.registry.index.task_name_hash()
            == '464ec5e9cafe0a652bdddb868e66ca0bf26c3252c8d322a45151efd1c8fe6441'  # noqa: E501
        )
