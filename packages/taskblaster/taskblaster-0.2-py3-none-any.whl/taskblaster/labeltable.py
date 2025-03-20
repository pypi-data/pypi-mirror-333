from __future__ import annotations

from taskblaster.registry import writes

create_table = """
CREATE TABLE IF NOT EXISTS {tablename} (
    name VARCHAR(256), tag VARCHAR(256), PRIMARY KEY (name, tag)
)
"""


class LabelTable:
    def __init__(
        self, tablename, conn, read_only=False, *, valid_tag_regex=r'\S+'
    ):
        self.tablename = tablename
        self.conn = conn
        self.read_only = read_only
        self.valid_tag_regex = valid_tag_regex

    def initialize(self):
        assert not self.read_only
        self.conn.execute(create_table.format(tablename=self.tablename))

        indices = {
            'name_index': f'{self.tablename}(name)',
            'tag_index': f'{self.tablename}(tag)',
        }
        for indexname, target in indices.items():
            statement = f'CREATE INDEX IF NOT EXISTS {indexname} ON {target}'
            self.conn.execute(statement)

    def select_all(self):
        query = f'SELECT * FROM {self.tablename}'
        cursor = self.conn.execute(query)
        return cursor.fetchall()

    @writes
    def add_tags(self, data: list[tuple[str, str]]) -> None:
        for name, tag in data:
            self.add_tag(name, tag)

    def has_tag(self, name, tag) -> bool:
        query = (
            f'SELECT * FROM {self.tablename} WHERE name = (?) AND tag = (?)'
        )
        results = self.conn.execute(query, (name, tag)).fetchall()
        return bool(results)

    @writes
    def add_tag(self, name: str, tag: str) -> None:
        """Add name with tag.

        If name and tag were already added, do nothing.

        Return whether something changed or not."""
        import re

        if not re.match(self.valid_tag_regex, tag):
            # Let's not have whitespace and other funnies for now.
            raise ValueError(
                'Invalid tag {tag!r}.  '
                'Tags should be consist of alphanumeric characters, -, or _.'
            )

        if self.has_tag(name, tag):
            return

        query = f'INSERT INTO {self.tablename} VALUES (?, ?)'
        self.conn.execute(query, (name, tag))

    def select_tag(self, tag: str) -> list[str]:
        query = f'SELECT name FROM {self.tablename} WHERE tag == (?)'
        results = self.conn.execute(query, (tag,)).fetchall()
        return [results[0] for result in results]

    def get_tags(self, name: str) -> set[str]:
        query = f'SELECT tag FROM {self.tablename} WHERE name == (?)'
        results = self.conn.execute(query, (name,)).fetchall()
        return set(result[0] for result in results)

    @writes
    def remove(self, name: str) -> None:
        query = f'DELETE FROM {self.tablename} WHERE name == (?)'
        self.conn.execute(query, (name,))

    @writes
    def untag(self, name: str, tag: str) -> None:
        query = (
            f'DELETE FROM {self.tablename} WHERE name == (?) AND tag == (?)'
        )
        self.conn.execute(query, (name, tag))
