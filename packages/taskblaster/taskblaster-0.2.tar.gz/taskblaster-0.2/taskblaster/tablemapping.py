from collections.abc import MutableMapping

from taskblaster import writes


class TableMapping(MutableMapping):
    def __init__(self, conn, tablename, fieldname, typename, read_only=False):
        self.conn = conn
        self.tablename = tablename
        self.fieldname = fieldname
        self.typename = typename
        self.read_only = read_only

    @writes
    def create_if_not_exists(self):
        lines = [
            'name VARCHAR(512) PRIMARY KEY,',
            f'{self.fieldname} {self.typename},',
        ]

        lines += [
            'FOREIGN KEY(name) REFERENCES registry(name)',
            'ON UPDATE RESTRICT',
            'ON DELETE RESTRICT',
        ]

        meat = '\n'.join(lines)

        statement = f'CREATE TABLE IF NOT EXISTS {self.tablename} ({meat})'
        self.conn.execute(statement)

    def __len__(self):
        query = f'SELECT COUNT(*) FROM {self.tablename}'
        cursor = self.conn.execute(query)
        return cursor.fetchone()[0]

    def __iter__(self):
        query = f'SELECT name FROM {self.tablename}'
        for result in self.conn.execute(query).fetchall():
            yield result[0]

    def __getitem__(self, key):
        query = f'SELECT {self.fieldname} FROM {self.tablename} WHERE name=?'
        cursor = self.conn.execute(query, (key,))
        results = cursor.fetchall()

        if not results:
            raise KeyError(key)

        return results[0][0]

    @writes
    def __setitem__(self, key, value):
        assert value is not None
        # Note: For safety we may not always want to allow updates of
        # existing keys.  We should perhaps add a separate method.
        query = (
            f'INSERT INTO {self.tablename} VALUES (?, ?)'
            f'ON CONFLICT (name) DO UPDATE SET {self.fieldname} = ?'
        )
        self.conn.execute(query, (key, value, value))

    @writes
    def __delitem__(self, key):
        query = f'DELETE FROM {self.tablename} WHERE name=?'
        self.conn.execute(query, (key,))
