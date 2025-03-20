import sqlite3

from taskblaster.repository import Repository
from taskblaster.util import color

_TOPOLOGICAL_DEPTH_ORPHAN_QUERY = (
    'SELECT * FROM topological_depth WHERE NOT EXISTS '
    '(SELECT 1 FROM registry WHERE registry.name == topological_depth.name);'
)

_TOPOLOGICAL_DEPTH_TEMPORARY_TABLE = (
    'CREATE TEMPORARY TABLE actual_depth (name VARCHAR(512), depth INT);'
)

_TOPOLOGICAL_DEPTH_ADD_NODES = (
    'INSERT INTO actual_depth (name, depth) SELECT name, 9999 FROM registry;'
)

_TOPOLOGICAL_DEPTH_FIND_ROOT_NODES = (
    'UPDATE actual_depth SET depth=0 WHERE NOT '
    'EXISTS (SELECT * FROM dependencies WHERE '
    'dependencies.descendant==actual_depth.name);'
)

_TOPOLOGICAL_DEPTH_CHECK_MISSING_ROWS = (
    'SELECT actual_depth.name, actual_depth.depth FROM actual_depth LEFT'
    ' JOIN topological_depth ON topological_depth.name=actual_depth.name'
    ' WHERE topological_depth.name IS NULL'
)

_TOPOLOGICAL_DEPTH_MISSING_ROWS = (
    'INSERT OR IGNORE INTO topological_depth SELECT * FROM actual_depth;'
)


_TOPOLOGIGAL_DEPTH_UPDATE_DESCENDANTS = (
    'UPDATE actual_depth SET depth={depthp1}'
    ' WHERE actual_depth.name IN (SELECT dependencies.descendant FROM'
    ' dependencies JOIN actual_depth ON'
    ' dependencies.ancestor==actual_depth.name'
    ' WHERE actual_depth.depth=={depth});'
)

_TOPOLOGICAL_DEPTH_MISMATCHES = (
    'select actual_depth.name,'
    ' actual_depth.depth, topological_depth.depth from actual_depth JOIN'
    ' topological_depth ON topological_depth.name == actual_depth.name'
    ' WHERE actual_depth.depth<>topological_depth.depth ORDER by '
    'actual_depth.depth;'
)

_AWAITCOUNT_TEMPORARY_TABLE = (
    'CREATE TEMPORARY TABLE actual_awaitcount'
    ' (name VARCHAR(512), awaitcount INT);'
)

_AWAITCOUNT_ADD_NODES = (
    'INSERT INTO actual_awaitcount (name, awaitcount)'
    ' SELECT name, -1 FROM registry;'
)

_AWAITCOUNT_UPDATE_COUNTS = (
    'UPDATE actual_awaitcount SET awaitcount=(select'
    ' COUNT(dependencies.ancestor)'
    ' from dependencies JOIN registry ON registry.name=dependencies.ancestor '
    'WHERE dependencies.descendant = actual_awaitcount.name'
    ' AND registry.state <>"d");'
)

_AWAITCOUNT_UPDATE_UNMET_REFERENCES = (
    'UPDATE actual_awaitcount SET '
    'awaitcount=-1 WHERE EXISTS (SELECT 1 from dependencies WHERE'
    ' dependencies.descendant=actual_awaitcount.name AND '
    'dependencies.ancestor = "__tb_unreachable__");'
)


_AWAITCOUNT_MISMATCHES = (
    'select actual_awaitcount.name,'
    ' actual_awaitcount.awaitcount, registry.awaitcount FROM actual_awaitcount'
    ' JOIN registry ON registry.name == actual_awaitcount.name'
    ' WHERE actual_awaitcount.awaitcount<>registry.awaitcount'
)


class RegistryRepair:
    def __init__(self, conn, echo, dry_run=True, force=False):
        self.conn = conn
        self.echo = echo
        self.dry_run = dry_run
        self.force = force

    def orphan_topological_depth_rows(self):
        conn = self.conn
        echo = self.echo
        cursor = conn.execute(_TOPOLOGICAL_DEPTH_ORPHAN_QUERY)

        orphan_names = []
        for row in cursor.fetchall():
            echo(color('orphan_topological_depth: ', 'red') + row[0])
            orphan_names.append(row[0])

        orphan_rows = len(orphan_names)
        if orphan_rows == 0:
            echo(color('No orphan topological_depth rows found.', 'green'))

        else:
            echo(
                color(
                    f'!!! Found {orphan_rows} orphan topological_depth'
                    ' row(s).',
                    'red',
                )
            )

        if not self.dry_run:
            if orphan_rows and (
                self.force
                or echo.are_you_sure(
                    f'Delete {orphan_rows} orphan topological_depth'
                    'row(s) from the registry?'
                )
            ):
                for name in orphan_names:
                    echo(
                        color('removed', 'green')
                        + f': topological_depth: {name}'
                    )
                    conn.execute(
                        'DELETE FROM topological_depth WHERE name=?', (name,)
                    )
            else:
                if orphan_rows:
                    echo('Never mind.')

    def topological_depth_correctness(self):
        conn = self.conn
        echo = self.echo

        echo('Creating temporary table...')
        conn.execute(_TOPOLOGICAL_DEPTH_TEMPORARY_TABLE)
        cursor = conn.execute(_TOPOLOGICAL_DEPTH_ADD_NODES)
        echo(f'{cursor.rowcount} nodes found.')
        cursor = conn.execute(_TOPOLOGICAL_DEPTH_FIND_ROOT_NODES)
        echo(f'{cursor.rowcount} root nodes found.')

        depth = 0
        while True:
            echo(f'Updating from depth {depth} to depth {depth + 1}...')
            cursor = conn.execute(
                _TOPOLOGIGAL_DEPTH_UPDATE_DESCENDANTS.format(
                    depth=depth, depthp1=depth + 1
                )
            )
            echo(f'{cursor.rowcount} nodes affected.')
            depth += 1
            if cursor.rowcount == 0:
                break

        cursor = conn.execute(_TOPOLOGICAL_DEPTH_MISMATCHES)
        mismatches = []
        for row in cursor.fetchall():
            echo(
                f'{color("topological_depth_mismatch", "red")}:'
                f' {row[0]} actual={row[1]} indb={row[2]}'
            )
            mismatches.append((row[0], row[1]))

        mismatch_count = len(mismatches)

        if mismatch_count == 0:
            echo(color('No mismatched topological_depth rows found.', 'green'))

        else:
            echo(
                color(
                    f'!!! Found {mismatch_count} incorrect topological_depth'
                    ' row(s).',
                    'red',
                )
            )

        cursor = conn.execute(_TOPOLOGICAL_DEPTH_CHECK_MISSING_ROWS)

        missing = []
        for row in cursor.fetchall():
            echo(
                f'{color("topological_depth_missing", "red")}:'
                f' {row[0]} actual={row[1]}'
            )
            missing.append((row[0], row[1]))

        missing_count = len(missing)

        if missing_count == 0:
            echo(color('No missing topological_depth rows found.', 'green'))

        else:
            echo(
                color(
                    f'!!! Found {missing_count} missing topological_depth'
                    ' row(s).',
                    'red',
                )
            )

        if not self.dry_run:
            if (mismatch_count + missing_count) and (
                self.force
                or echo.are_you_sure(
                    f'Fix {mismatch_count + missing_count} topological_depth'
                    'row(s) to the registry?'
                )
            ):
                for name, true_depth in mismatches:
                    echo(
                        color('updated', 'green')
                        + f': topological_depth: {name}'
                    )
                    conn.execute(
                        'UPDATE topological_depth SET depth=? WHERE name=?;',
                        (true_depth, name),
                    )
                conn.execute(_TOPOLOGICAL_DEPTH_MISSING_ROWS)
                for name, true_depth in missing:
                    echo(
                        color('added', 'green')
                        + f': topological_depth: {name}'
                    )
            else:
                if mismatch_count:
                    echo('Never mind.')

    def topological_depth_foreign_key(self):
        """SQLite does not support ALTER TABLE ... ADD FOREIGN KEY.

        Since topological_depth is just a helper table, and can be easily
        rebuilt with tb special repair command, it is safe to add the
        foreign key constraint here.
        """
        conn = self.conn
        cursor = conn.execute('PRAGMA foreign_key_list(topological_depth);')
        foreign_keys = cursor.fetchall()
        if len(foreign_keys) == 0:
            self.echo('No foreign key found in topological depth table.')
            if self.dry_run:
                return
            if not (
                self.force
                or self.echo.are_you_sure(
                    "You don't have foreign key in topo"
                    'logical depth table. Add it?'
                )
            ):
                self.echo('Never mind.')
                return
            from taskblaster.registry import migrate_topological_keys_table

            migrate_topological_keys_table(conn)
        else:
            self.echo('Topological depth foreign key ok.')

    def awaitcount_correctness(self):
        conn = self.conn
        echo = self.echo

        echo('Creating temporary table...')
        conn.execute(_AWAITCOUNT_TEMPORARY_TABLE)

        echo('Initializing awaitcount table.')
        cursor = conn.execute(_AWAITCOUNT_ADD_NODES)
        echo(f'{cursor.rowcount} nodes added.')

        echo('Calculating awaitcounts, this may take a while...')
        cursor = conn.execute(_AWAITCOUNT_UPDATE_COUNTS)
        echo(f'{cursor.rowcount} await counts calculated.')

        cursor = conn.execute(_AWAITCOUNT_UPDATE_UNMET_REFERENCES)
        echo(f'{cursor.rowcount} unmet references updated.')

        echo('Finding mismatches...')
        cursor = conn.execute(_AWAITCOUNT_MISMATCHES)

        mismatches = []
        for row in cursor.fetchall():
            echo(
                f'{color("awaitcount_mismatch", "red")}:'
                f' {row[0]} actual={row[1]} indb={row[2]}'
            )
            mismatches.append((row[0], row[1]))

        mismatch_count = len(mismatches)
        if mismatch_count:
            echo(
                color(
                    f'!!! number of mismatched await counts: {mismatch_count}',
                    'red',
                )
            )
        else:
            echo(color('No mismatches awaitcounts found.', 'green'))

        if not self.dry_run:
            if mismatch_count and (
                self.force
                or echo.are_you_sure(
                    f'Fix {mismatch_count} await countrow(s) to the registry?'
                )
            ):
                for name, await_count in mismatches:
                    echo(color('updated', 'green') + f': await_count: {name}')
                    conn.execute(
                        'UPDATE registry SET awaitcount=? WHERE name=?;',
                        (await_count, name),
                    )
            else:
                if mismatch_count:
                    echo('Never mind.')


def repair_registry(
    echo,
    dry_run=True,
    orphan_topological_depth_rows=True,
    topological_depth_correctness=True,
    topological_depth_foreign_key=True,
    awaitcount_correctness=True,
    force=False,
):
    # Repair only access the database directly
    # Thus, find the database registry path
    root = Repository.find_root_directory()
    registry_path = str(
        root / Repository._magic_dirname / Repository._registry_name
    )

    # Create db uri based whether we want write protected or mutable database
    mode_uri = '?mode=ro' if dry_run else ''
    uri = 'file:' + registry_path + mode_uri
    isolation_level = 'DEFERRED' if dry_run else 'EXCLUSIVE'

    # Create sqlite3 connection
    connection = sqlite3.connect(
        uri,
        uri=True,
        timeout=60,
        detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
        isolation_level=isolation_level,
    )
    if isolation_level == 'EXCLUSIVE':
        connection.execute('BEGIN EXCLUSIVE;')

    try:
        repair = RegistryRepair(connection, echo, dry_run=dry_run, force=force)

        if orphan_topological_depth_rows:
            repair.orphan_topological_depth_rows()

        if topological_depth_correctness:
            repair.topological_depth_correctness()

        if topological_depth_foreign_key:
            repair.topological_depth_foreign_key()

        if awaitcount_correctness:
            repair.awaitcount_correctness()

        echo('Committing changes to db.')
        connection.execute('COMMIT;')
    except Exception:
        echo('Error during heuristics. Rolling database back.')
        connection.execute('ROLLBACK;')
        raise
