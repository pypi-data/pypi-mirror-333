from pathlib import Path

import pytest

from taskblaster import Node, Reference
from taskblaster.cache import FileCache
from taskblaster.namedtask import Task
from taskblaster.registry import Missing
from taskblaster.state import State
from taskblaster.storage import JSONProtocol


@pytest.fixture
def cache(tmp_path, registry):
    cache = FileCache(
        directory=tmp_path / 'tree',
        registry=registry,
        json_protocol=JSONProtocol(tmp_path),
    )
    with cache.registry.conn:
        yield cache


def mktask(target, dct, name):
    json_protocol = JSONProtocol(Path('/tmp/nonexistent'))

    task = Task(
        name,
        Node(target, dct),
        branch='entry',
        source='',
        has_record=False,
        tags=set(),
        error_handlers=None,
    )
    return json_protocol.encode_task(task)


@pytest.fixture
def tasks():
    return [
        mktask('hello', {}, 'a'),
        mktask('hello2', {}, 'b'),
        mktask('hello', {'a': 42}, 'c'),
    ]


def test_empty_cache(cache):
    assert len(cache) == 0
    assert '12345' not in cache
    assert len(list(cache)) == 0
    with pytest.raises(KeyError):
        cache['12345']


def test_cache_add(cache):
    """Test behaviour when adding a single node."""
    task = mktask('hello', {'a': 3, 'b': 4}, 'id')

    assert len(cache) == 0
    assert task.name not in cache
    action, _, indexnode = cache.add_or_update(task)
    assert action == 'add'
    assert len(cache) == 1

    assert indexnode.name in cache
    future1 = cache[task.name]
    assert future1.node.name == indexnode.name


def test_has_already(cache):
    task = mktask('hello', {}, 'id')
    cache.add_or_update(task)
    assert task.name in cache
    action, _, indexnode = cache.add_or_update(task)
    assert action == 'have'


def test_remove(cache, tasks):
    # We make 3 nodes.  Then we delete nodes[1] and verify that.

    for task in tasks:
        cache.add_or_update(task)

    n_initial = 3
    assert len(cache) == n_initial
    cache.delete_nodes([tasks[1].name])
    n_remains = len(cache)
    assert n_remains == 2

    for i in range(3):
        exists = i != 1
        name = tasks[i].name
        assert (name in cache) == exists

        if exists:
            indexnode = cache.registry.index.node(name)
            assert indexnode.name == tasks[i].name
            assert cache.registry.inputs.get(name) == tasks[i].serialized_input


def test_repr(cache):
    print(str(cache))
    print(repr(cache))


def test_finished(cache):
    task = mktask('func', {'x': 1}, 'n1')
    cache.add_or_update(task)
    future = cache[task.name]  # Future(node, cache)
    task2 = mktask('func', {'x': future}, 'n2')
    cache.add_or_update(task2)

    def node2_awaitcount():
        return cache.registry.index.node(task2.name).awaitcount

    assert node2_awaitcount() == 1
    cache.registry._update_state(task.name, State.done)
    assert node2_awaitcount() == 0
    cache.registry._update_state(task.name, State.fail)
    assert node2_awaitcount() == 1


def test_find_ready(cache):
    task = mktask('func', {}, 'nodename')
    cache.add_or_update(task)
    with pytest.raises(Missing):
        cache.find_ready()
    cache.registry._update_state(task.name, State.queue)
    indexnode = cache.find_ready()
    assert indexnode.name == task.name


def test_none_ready(cache):
    with pytest.raises(Missing):
        cache.find_ready()


def add_and_submit_multiple(cache, ntasks):
    for n in range(ntasks):
        name = f'hello{n}'
        task = mktask('hello', {}, name)
        cache.add_or_update(task)
        cache.registry._update_state(task.name, State.queue)


def test_find_ready_tag(cache):
    add_and_submit_multiple(cache, ntasks=3)

    with pytest.raises(Missing):
        cache.find_ready(required_tags={'sometag'})

    cache.registry.resources.add_tag('hello2', 'sometag')

    node = cache.find_ready(required_tags={'sometag'})
    assert node.name == 'hello2'


def find_all_ready(cache, **kwargs):
    add_and_submit_multiple(cache, ntasks=5)

    resources = cache.registry.resources
    # (hello0 is left untagged)
    tagdata = [
        ('hello1', 'tag1'),
        ('hello2', 'tag1'),
        ('hello2', 'tag2'),
        ('hello3', 'tag2'),
        ('hello4', 'tag3'),
    ]

    resources.add_tags(tagdata)
    nodes = cache.registry.find_all_ready(**kwargs)
    return {node.name for node in nodes}


@pytest.mark.parametrize(
    'supported, required, expected_result',
    [
        (['tag1'], [], ['hello0', 'hello1']),
        (['tag2', 'tag3'], [], ['hello0', 'hello3', 'hello4']),
        ([], ['tag1'], ['hello1']),
        (['tag1'], ['tag2'], ['hello2', 'hello3']),
    ],
)
def test_find_by_tag_multi(cache, supported, required, expected_result):
    # The find_all_ready() function has a number of variously tagged tasks.
    #
    # This test issues some selections on that, then verifies the result.
    print(supported, required, expected_result)
    tasknames = find_all_ready(
        cache,
        supported_tags=set(supported),
        required_tags=set(required),
    )
    assert tasknames == set(expected_result)


@pytest.fixture
def nodes():
    a = mktask('a', {}, 'a')
    b = mktask('b', {'x': ref(a)}, 'b')
    c = mktask('c', {'x': ref(a), 'y': ref(b)}, 'c')
    d = mktask('d', {'args': [ref(n) for n in [a, b, c]]}, 'd')
    return (a, b, c, d)


def ref(node):
    # Utility function for building trees of nodes.
    return Reference(node.name)


def test_node_parents(nodes):
    (a, b, c, d) = nodes
    assert a.parents == tuple()
    assert b.parents == (a.name,)
    assert set(c.parents) == {a.name, b.name}
    assert set(d.parents) == {a.name, b.name, c.name}
