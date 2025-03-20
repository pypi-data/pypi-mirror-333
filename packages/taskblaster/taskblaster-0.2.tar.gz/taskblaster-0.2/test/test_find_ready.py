import pytest

import taskblaster as tb
from taskblaster.registry import Missing


def hello(whom):
    return f'hello {whom}'


@tb.workflow
class Hello:
    @tb.task
    def hello(self):
        return tb.node(hello, whom='world')

    @tb.task
    def hello2(self):
        return tb.node(hello, whom=self.hello)


def test_find_ready_frozen(tool):
    """Test that frozen task is not picked up by find_ready()."""
    tool.workflow(Hello())
    repo = tool.repo
    tool.submit()

    with repo:
        assert repo.cache.find_ready().name == 'hello'
        repo.registry.freeze('hello', why='manual')
        with pytest.raises(Missing):
            repo.cache.find_ready()


def test_run_frozen(tool):
    """Test that explicit run (tb run tree/...) does not run frozen task."""
    tool.workflow(Hello())

    # We want a task which runs and one which does not due to frozenness.
    with tool.repo:
        tool.repo.registry.freeze('hello2', why='manual')

    tool.repo.run_worker(['tree'])
    assert tool.count(done=1, new=1)


def test_new_task_inherits_freeze(tool):
    tool.workflow(Hello())
    assert tool.count(new=2)

    # Delete a task so we can freeze its parent before generating it again.
    repo = tool.repo
    with repo:
        nodes, delete = repo.tree(['tree/hello2']).remove()
        assert len(nodes) == 1
        delete()
    assert tool.count(new=1)

    with repo:
        repo.registry.freeze('hello', 'manual')

    tool.workflow(Hello())

    with repo:
        frozen_why = repo.registry.frozentasks.get_tags('hello2')
    assert frozen_why == {'parent:hello'}
