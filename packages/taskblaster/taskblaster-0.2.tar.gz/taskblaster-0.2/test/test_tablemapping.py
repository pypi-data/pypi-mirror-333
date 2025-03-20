import pytest

from taskblaster.tablemapping import TableMapping


@pytest.fixture
def mapping():
    import sqlite3

    conn = sqlite3.connect(':memory:')
    tablemap = TableMapping(conn, 'things', 'fieldname', 'VARCHAR(123)')
    tablemap.create_if_not_exists()
    return tablemap


def test_empty(mapping):
    assert len(mapping) == 0
    assert dict(mapping) == {}
    assert not mapping
    assert 'qwerty' not in mapping


def test_set_get(mapping):
    mapping['hello'] = 'world'
    assert 'hello' in mapping
    assert mapping['hello'] == 'world'


def test_iterate(mapping):
    dct = {'a': 'b', 'c': 'd'}
    mapping.update(dct)
    assert mapping == dct
    assert [*mapping] == [*dct]
    assert len(mapping) == len(dct)


def test_upsert(mapping):
    mapping['thing'] = 'onion'
    mapping['thing'] = 'potato'
    assert mapping['thing'] == 'potato'
