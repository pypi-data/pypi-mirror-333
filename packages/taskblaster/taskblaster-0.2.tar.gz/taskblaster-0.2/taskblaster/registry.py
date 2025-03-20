import os
import sqlite3
import warnings
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from dataclasses import replace as _dataclass_replace
from pathlib import Path
from random import random
from time import sleep
from typing import Set

from taskblaster import TB_STRICT, UNREACHABLE_REF, WardenPanic, writes
from taskblaster.conflict import ConflictInfo, ConflictState
from taskblaster.labeltable import LabelTable
from taskblaster.state import State
from taskblaster.tablemapping import TableMapping
from taskblaster.workers import Workers
from taskblaster.workflowtable import WorkflowTable

UNKNOWN_DEPTH = 9999


@dataclass
class IndexNode:
    name: str
    state: State
    awaitcount: int  # how many direct ancestors are not done?

    @classmethod
    def fromrow(cls, row):
        return cls(name=row[0], state=State(row[1]), awaitcount=row[2])

    def replace(self, **kwargs):
        return _dataclass_replace(self, **kwargs)

    def torow(self):
        return (self.name, self.state.value, self.awaitcount)


def topological_depth_table(conn, tablename='topological_depth', *, read_only):
    return TableMapping(
        conn, tablename, 'depth', 'INTEGER', read_only=read_only
    )


def migrate_topological_keys_table(conn):
    print(
        'Updating Taskblaster database to a new version. '
        'Adding a FOREIGN_KEY constraint to topological_depth.'
    )

    backup_table = topological_depth_table(
        conn, 'topological_depth_backup', read_only=False
    )
    backup_table.create_if_not_exists()

    conn.execute(
        'INSERT INTO topological_depth_backup (name, depth)'
        ' SELECT name, depth FROM topological_depth;'
    )
    conn.execute('DROP TABLE topological_depth;')

    depth_table = topological_depth_table(conn, read_only=False)
    depth_table.create_if_not_exists()

    conn.execute(
        'INSERT INTO topological_depth (name, depth) '
        'SELECT name, depth FROM topological_depth_backup;'
    )
    conn.execute('DROP TABLE topological_depth_backup;')
    print('Success.')


class Index:
    def __init__(self, conn, read_only=False):
        self.conn = conn
        self.read_only = read_only

    @classmethod
    def initialize(cls, conn):
        conn.execute(
            """
CREATE TABLE IF NOT EXISTS registry (
    name VARCHAR(512) PRIMARY KEY,
    state CHAR(1),
    awaitcount INTEGER,
    workerclass VARCHAR(512),
    argtext VARCHAR(80),
    digest CHAR(64)
)"""
        )

        indices = {
            'state_index': 'registry(state)',
            'name_index': 'registry(name)',
            'awaitcount_index': 'registry(awaitcount)',
            'ready_index': 'registry(state, awaitcount, workerclass)',
            'digest_index': 'registry(digest)',
        }

        for indexname, target in indices.items():
            statement = f'CREATE INDEX IF NOT EXISTS {indexname} ON {target}'
            conn.execute(statement)

        """conflicts table keeps track of tasks with conflicts. I.e. tasks
           that are marked as done but which were excecuted with different
           input paramaters than in the current workflow.
        """

        # We no longer use the "reason" field.  It was equal to the existing
        # input always, and that is stored on the task anyway.
        conn.execute(
            """
CREATE TABLE IF NOT EXISTS conflicts (
    task_name VARCHAR(512) PRIMARY KEY,
    conflict CHAR(1),
    reason BLOB,
    buf BLOB)
    """
        )

        return cls(conn)

    @writes
    def add(self, indexnode: IndexNode) -> None:
        self.conn.execute(
            'INSERT INTO registry (name, state, awaitcount) VALUES (?, ?, ?)',
            indexnode.torow(),
        )

    @writes
    def update_states(self, names, state):
        query = 'UPDATE registry SET state=(?) WHERE name=(?)'
        self.conn.executemany(query, [(state, name) for name in names])

    @writes
    def update_state(self, name, state):
        self.update_states([name], state)

    @writes
    def update_awaitcount(self, name, awaitcount):
        query = 'UPDATE registry SET awaitcount=(?) WHERE name=(?)'
        self.conn.execute(query, (awaitcount, name))

    def count(self) -> int:
        cursor = self.conn.execute('SELECT COUNT(*) FROM registry')
        return cursor.fetchone()[0]

    def glob_simple(self, pattern: str):
        query = 'SELECT * FROM registry WHERE name GLOB (?)'
        cursor = self.conn.execute(query, (pattern,))
        return [IndexNode.fromrow(row) for row in cursor.fetchall()]

    def glob(
        self, patterns, states=None, sort='name', failure=None, tags=set()
    ):
        # matching a/b should include itself (obviously)
        # matching a/b should also include a/b/c and other subdirectories.
        #
        # To get both, we pass pattern as well as pattern/*, matching either.
        query_args = list(patterns)
        query_args += [pattern + '/*' for pattern in patterns]

        # Is there a way to execute multiple globs or must we build
        # this potentially very long string?
        glob_where = ' OR '.join(['registry.name GLOB (?)'] * len(query_args))

        glob_where = '(' + glob_where + ') '
        if states:
            statechars = [state.value for state in states]
            questionmarks = ', '.join('?' * len(statechars))
            where = f'{glob_where} AND registry.state IN ({questionmarks})'
            query_args += list(statechars)
        else:
            where = glob_where

        tables = ['registry']

        if failure is not None:
            tables.append('runinfo')
            where += (
                ' AND registry.name = runinfo.task_name'
                f" AND instr(runinfo.exception, '{failure}')>0 "
            )

        if tags:
            tables.append('resources')
            tagset = ', '.join([f'"{tag}"' for tag in tags])
            where += (
                ' AND resources.name == registry.name AND '
                f'resources.tag IN ({tagset}) '
            )

        tables = ', '.join(tables)
        if sort == 'name':
            query = f'SELECT * FROM {tables} WHERE {where} ORDER BY name'
        elif sort == 'topo':
            query = (
                f'SELECT registry.* FROM {tables} JOIN topological_depth '
                f'on registry.name = topological_depth.name '
                f'WHERE {where} order by topological_depth.depth, name'
            )
        else:
            raise ValueError(f'Invalid sort: {sort!r}')
        cursor = self.conn.execute(query, query_args)
        return [IndexNode.fromrow(row) for row in cursor.fetchall()]

        # We should re-enable more globbing/name filtering options:
        # Selecting tasks with given name or folders that contain pattern
        # XXX Could be done more efficient
        # output = []
        # for row in cursor.fetchall():
        #    indxnode = IndexNode.fromrow(row)
        #    if name == indxnode.name.split('/')[-1]:
        #        output.append(indxnode)
        #    elif pattern:
        #        if pattern in indxnode.name:
        #            output.append(indxnode)
        # return output

    def nodes(self):
        cursor = self.conn.execute('SELECT * FROM registry ORDER BY name')
        for row in cursor:
            yield IndexNode.fromrow(row)

    def _getnode(self, name):
        query = 'SELECT * FROM registry WHERE name=(?)'
        cursor = self.conn.execute(query, (name,))
        rows = cursor.fetchall()
        return rows

    def node(self, name: str) -> IndexNode:
        rows = self._getnode(name)
        if len(rows) != 1:
            raise Missing(name)
        return IndexNode.fromrow(rows[0])

    def contains(self, name: str) -> bool:
        rows = self._getnode(name)
        return bool(rows)

    @writes
    def remove_multiple(self, names):
        query = 'DELETE FROM registry WHERE name=(?)'
        self.conn.executemany(query, [(name,) for name in names])

    def asdict(self):
        return {node.name: node for node in self.nodes()}

    def task_name_hash(self):
        import hashlib

        m = hashlib.sha256()
        for node in self.nodes():
            m.update(node.name.encode('utf-8'))
            m.update(node.state.value.encode('utf-8'))
        return m.hexdigest()


class Missing(LookupError):
    pass


class Ancestry:
    """Storage of vertices in dependency graph as node --> parent map."""

    tablename = 'dependencies'

    def __init__(self, conn, read_only=False):
        self.conn = conn
        self.read_only = read_only

    @classmethod
    def initialize(cls, conn):
        table = cls.tablename
        conn.execute(
            f"""\
CREATE TABLE IF NOT EXISTS {table} (
    ancestor CHAR(64),
    descendant CHAR(64),
    PRIMARY KEY (ancestor, descendant)
)"""
        )
        conn.execute(
            f'CREATE INDEX IF NOT EXISTS ancestor_index ON {table}(ancestor)'
        )
        conn.execute(
            'CREATE INDEX IF NOT EXISTS descendant_index '
            f'ON {table}(descendant)'
        )
        conn.execute(
            'CREATE INDEX IF NOT EXISTS combined_index '
            f'ON {table}(ancestor, descendant)'
        )
        return cls(conn)

    def _all(self):
        query = f'SELECT * FROM {self.tablename}'
        return self.conn.execute(query).fetchall()

    def graph(self):
        tokens = ['digraph ancestors {']

        for ancestor, descendant in self._all():
            for node in [ancestor, descendant]:
                tokens.append(f'  "{node}" [label="{node[:6]}"]')

            tokens.append(f'  "{ancestor}" -> "{descendant}"')

        tokens.append('}')
        return '\n'.join(tokens)

    @writes
    def add(self, parent_name: str, name: str) -> None:
        query = f'INSERT INTO {self.tablename} VALUES (?, ?)'
        self.conn.execute(query, (parent_name, name))

    def contains(self, parent_name: str, name: str) -> bool:
        query = (
            f'SELECT ancestor, descendant FROM {self.tablename} '
            'WHERE ancestor=(?) AND descendant=(?)'
        )
        cursor = self.conn.execute(query, (parent_name, name))
        count = len(cursor.fetchall())
        assert count <= 1
        return bool(count)

    @writes
    def remove(self, parent_name: str, name: str) -> None:
        assert not self.read_only
        if not self.contains(parent_name, name):
            raise KeyError(parent_name, name)
        query = (
            f'DELETE FROM {self.tablename} '
            'WHERE ancestor=(?) AND descendant=(?)'
        )
        self.conn.execute(query, (parent_name, name))

    def _get_any(self, which: str, other: str, name: str) -> Set[str]:
        query = f'SELECT {which} FROM {self.tablename} WHERE {other}=(?)'
        cursor = self.conn.execute(query, (name,))
        return {obj[0] for obj in cursor.fetchall()}

    def ancestors(self, name: str) -> Set[str]:
        return self._get_any('ancestor', 'descendant', name)

    def descendants(self, name: str) -> Set[str]:
        return self._get_any('descendant', 'ancestor', name)

    # High-level functions -- they don't quite belong here.
    # Move to registry or something
    @writes
    def add_node(self, name: str, parents: Sequence[str]) -> None:
        for parent_name in parents:
            self.add(parent_name, name)

    @writes
    def remove_node(self, name: str) -> None:
        for parent_name in self.ancestors(name):
            self.remove(parent_name, name)


UNKNOWN_AWAITCOUNT = -1


class Registry:
    """Collection of tasks providing efficient access.

    The registry is a mapping from task IDs (hashes) to task locations
    (directories inside cache)."""

    def __init__(self, regfile: Path, timeout=60, read_only=False):
        self.regfile = regfile
        self.conn = Connection(
            regfile,
            timeout,
            read_only=read_only,
            initialize_tables=self._initialize_tables,
        )
        self.read_only = read_only

    def _initialize_tables(self):
        Index.initialize(self.conn)
        Ancestry.initialize(self.conn)
        Workers.initialize(self.conn)
        self.resources.initialize()
        self.frozentasks.initialize()
        self.inputs.create_if_not_exists()
        self.topological_depth.create_if_not_exists()
        WorkflowTable.initialize(self.conn)
        self.sources.create_if_not_exists()
        self.has_records.create_if_not_exists()
        self.handlers.create_if_not_exists()

    @writes
    def unrun(self, name: str) -> None:
        self.workers.remove_runinfo(name)
        self._update_state(name, State.new)
        self.clear_conflict(name)
        self._recursive_update_descendant_state(
            name, State.new, until_state=State.new, clear_conflict=True
        )

    @writes
    def _recursive_update_descendant_state(
        self, nodename, state, until_state, clear_conflict=False
    ) -> None:
        for descendant in self._recurse_descendants(nodename, until_state):
            self._update_state(descendant, state)
            if clear_conflict:
                self.clear_conflict(descendant)

    @writes
    def cancel_descendants(self, nodename: str) -> None:
        self._recursive_update_descendant_state(
            nodename, State.cancel, State.cancel
        )

    @staticmethod
    def frozen_by_parent(parentname: str) -> str:
        """Return the "why"-label signifying freeze inherited from parent."""
        return f'parent:{parentname}'

    @writes
    def freeze(self, nodename: str, why: str):
        if self.frozentasks.has_tag(nodename, why):
            return

        self.frozentasks.add_tag(nodename, why)
        for descendant_name in self.ancestry.descendants(nodename):
            self.freeze(descendant_name, why=self.frozen_by_parent(nodename))

    @writes
    def unfreeze(self, nodename: str, why: str):
        # Note: We need to make this fast at some point since it's recursive
        # and may affect many tasks.
        if not self.frozentasks.has_tag(nodename, why):
            return

        tags = self.frozentasks.get_tags(nodename)
        self.frozentasks.untag(nodename, why)
        tags_afterwards = self.frozentasks.get_tags(nodename)
        assert tags_afterwards == tags - {why}

        if tags_afterwards:
            # We are still frozen, so do not unfreeze descendants.
            return

        # Sanity check:
        for ancestor in self.ancestry.ancestors(nodename):
            assert not self.frozentasks.get_tags(ancestor)

        for descendant_nodename in self.ancestry.descendants(nodename):
            self.unfreeze(
                descendant_nodename, why=self.frozen_by_parent(nodename)
            )

    def _recurse_descendants(self, nodename: str, until_state):
        for descendant in self.ancestry.descendants(nodename):
            node = self.index.node(descendant)
            if node.state == until_state:
                continue

            yield from self._recurse_descendants(descendant, until_state)
            yield descendant

    def _awaitcount(self, name: str) -> int:
        parent_names = self.ancestry.ancestors(name)
        awaitcount = 0
        for parent_name in parent_names:
            if parent_name == UNREACHABLE_REF:
                return UNKNOWN_AWAITCOUNT

            parent_state = State(self.index.node(parent_name).state)
            awaitcount += parent_state != State.done

        return awaitcount

    def _compute_depth(self, name: str) -> int:
        ancestors = self.ancestry.ancestors(name)

        if UNREACHABLE_REF in ancestors:
            # XXX not obvious this exception
            return UNKNOWN_DEPTH

        depths = sorted(
            self.topological_depth[ancestor] for ancestor in ancestors
        )
        if not depths:
            return 0
        if UNKNOWN_DEPTH in depths:
            return UNKNOWN_DEPTH
        return depths[-1] + 1

    @writes
    def _add(self, encoded_task, force_state=None):
        name = encoded_task.name
        self.ancestry.add_node(name, encoded_task.parents)
        awaitcount = self._awaitcount(name)
        indexnode = IndexNode(name, state=State.new, awaitcount=awaitcount)
        self.index.add(indexnode)

        for tag in encoded_task.tags:
            self.resources.add_tag(name, tag)

        self.inputs[name] = encoded_task.serialized_input
        # To be enabled
        # assert encoded_task.source in self.workflows, encoded_task
        if TB_STRICT:
            assert encoded_task.source in self.workflows
        if encoded_task.source is None:
            assert not TB_STRICT
        else:
            self.sources[name] = encoded_task.source

        if encoded_task.has_record:
            self.has_records[name] = True
        self.handlers[name] = encoded_task.serialized_handlers

        if force_state:
            self._update_state(name, force_state)
        else:
            parent_states = set(self.parent_states(name)[0].values())
            if State.cancel in parent_states or State.fail in parent_states:
                self._update_state(name, State.cancel)
                indexnode.state = State.cancel

        for parent in encoded_task.parents:
            if self.frozentasks.get_tags(parent):
                self.freeze(name, why=self.frozen_by_parent(parent))

        self.topological_depth[name] = self._compute_depth(name)
        return indexnode

    # When we rerun a workflow, we should probably load all tasks
    # known to have been generated by that workflow and print something
    # if the workflow would not generate the same tasks (i.e. detect orphans).
    # def tasks_from_workflow(self, workflowname):
    # query = f'SELECT name FROM index WHERE registry.source=?'

    @writes
    def add_or_update_metadata(self, encoded_task):
        meta_actions = []
        name = encoded_task.name
        old_tags = self.resources.get_tags(name)
        add_tags = encoded_task.tags - old_tags

        for tag in add_tags:
            self.resources.add_tag(name, tag)

        if encoded_task.serialized_handlers != self.handlers.get(name, '[]'):
            meta_actions.append('handlers')
        self.handlers[name] = encoded_task.serialized_handlers
        if add_tags:
            meta_actions += 'tags'
        return ' '.join(meta_actions)

    @writes
    def add_or_update(self, encoded_task, force_overwrite=False):
        name = encoded_task.name

        try:
            indexnode = self.index.node(name)
        except Missing:
            return 'add', self._add(encoded_task)
        else:
            depth = self.topological_depth[name]

            # Update the record no matter what
            if encoded_task.has_record != self.has_records.get(name, False):
                self.has_records[name] = encoded_task.has_record

            # XXX insert a bloody parenthesis or something
            if (
                force_overwrite
                or depth == UNKNOWN_DEPTH
                and indexnode.state.is_pristine
            ):
                # XXX unduplicate
                self.ancestry.remove_node(name)
                del self.sources[name]
                del self.inputs[name]
                del self.handlers[name]
                del self.topological_depth[name]
                del self.has_records[name]
                self.index.remove_multiple([name])
                self.workers.remove_runinfo(name)
                # Note: The task will be in new state.
                return 'update', self._add(encoded_task)
            return 'have', indexnode

    def find_ready(self, *args, **kwargs):
        """Find one task that is ready to run."""
        cursor = self._find_ready(*args, **kwargs)
        result = cursor.fetchone()
        if result is None:
            raise Missing()

        return IndexNode.fromrow(result)

    def find_all_ready(self, *args, **kwargs):
        # We use this for testing, but it will be useful for workers
        # to pick up some number of small tasks simultaneously.
        cursor = self._find_ready(*args, **kwargs)
        return [IndexNode.fromrow(result) for result in cursor.fetchall()]

    def _find_ready(self, required_tags=None, supported_tags=None, names=None):
        if required_tags is None:
            required_tags = set()

        if supported_tags is None:
            supported_tags = set()

        supported_tags |= required_tags

        def questionmarks(seq):
            txt = ', '.join('?' * len(seq))
            return f'({txt})'

        required_tags_query = f"""\
SELECT name FROM resources
WHERE tag IN {questionmarks(required_tags)}
"""
        bad_tags_query = f"""\
SELECT DISTINCT(name) FROM resources
WHERE tag NOT IN {questionmarks(supported_tags)}
"""

        query_params = []
        requirements = [
            "(registry.state='q' or registry.state='p')",
            'registry.awaitcount=0',
        ]

        requirements.append(f'registry.name NOT IN ({bad_tags_query})')

        query_params += supported_tags

        # FIXME: There's probably a better SQL syntax for this, but I'm
        # currently offline.
        frozen_query = """\
SELECT DISTINCT(name) FROM frozentasks
WHERE name = registry.name
"""

        requirements.append(f'registry.name NOT IN ({frozen_query})')

        if required_tags:
            requirements.append(f'registry.name IN ({required_tags_query})')
            query_params += required_tags

        where = '\n AND '.join(requirements)
        query = f'SELECT registry.* FROM registry WHERE\n {where}'
        return self.conn.execute(query, query_params)

    def _fetchall(self, query, *args):
        return self.conn.execute(query, *args).fetchall()

    def parent_states(self, name):
        states = {}

        done_count = 0
        for parent_name in self.ancestry.ancestors(name):
            valid_dep_states = {State.done}
            if parent_name == UNREACHABLE_REF:
                states[parent_name] = State.new
                continue
            state = State(self.index.node(parent_name).state)
            done_count += state in valid_dep_states
            states[parent_name] = state

        node = self.index.node(name)
        awaitcount = node.awaitcount
        if not (
            awaitcount == len(states) - done_count
            or (awaitcount == UNKNOWN_AWAITCOUNT)
        ):
            only_warn = os.environ.get('TB_DEBUG', False)
            msg = (
                f'Await count mismatch: {name} has awaitcount {awaitcount} '
                f'but {len(states)} parents of which {done_count} are done '
                f'which should correspond to {len(states) - done_count}.'
            )
            if only_warn:
                warnings.warn(msg)
            else:
                raise RuntimeError(msg)
        return states, done_count

    @writes
    def update_task_partial(self, name):
        # only a failed/running task currently goes into a partial state. fail
        # state is kicked into partial, run state is handled in the worker
        # before it fails. If any other state is encountered, we panic.
        if self.index.node(name).state not in [State.run, State.fail]:
            raise WardenPanic()
        self._update_state(name, State.partial)
        self._recursive_update_descendant_state(
            name,
            State.new,
            State.new,
        )

    @writes
    def update_task_done(self, name):
        self._update_state(name, State.done)
        self.workers.register_task_done(name)

    @writes
    def update_task_running(self, name, worker_name, myqueue_id):
        self._update_state(name, State.run)
        self.workers.register_task_running(name, myqueue_id, worker_name)

    @writes
    def update_task_failed(self, name, error_msg):
        self._update_state(name, State.fail)
        self.cancel_descendants(name)
        self.workers.register_task_failed(name, error_msg)

    @writes
    def clear_conflict(self, name):
        query = 'DELETE FROM conflicts WHERE task_name=(?)'
        self.conn.execute(query, (name,))
        self.unfreeze(name, why='conflict')

    @writes
    def update_conflict(self, name, conflict_info):
        """Updates conflict info adding row if it does not exist."""

        # "reason" is the old string and "buf" is the new string.
        query = (
            'INSERT INTO conflicts '
            '(task_name, conflict, buf) VALUES (?, ?, ?) '
            'ON CONFLICT(task_name) '
            'DO UPDATE SET conflict=?, buf=?'
        )
        # Should centralize knowledge of conflicts to a conflicts.py module
        conflict_tuple = conflict_info.astuple()
        self.conn.execute(query, (name, *conflict_tuple, *conflict_tuple))

        is_already_frozen = self.frozentasks.has_tag(name, 'conflict')
        if conflict_info.state == ConflictState.resolved:
            if is_already_frozen:
                self.unfreeze(name, why='conflict')
            else:
                import warnings

                warnings.warn('Conflicted task was not frozen, ignoring')
        elif conflict_info.state == ConflictState.conflict:
            # It's OK to "re-conflict" a conflicted task.  Inputs may be
            # updated any number of times.
            self.freeze(name, why='conflict')
        else:
            raise ValueError(f'Bad conflict state {conflict_info.state}')

    def conflict_info(self, name):
        query = 'SELECT conflict, buf from conflicts WHERE task_name=(?)'
        rows = self.conn.execute(query, (name,))
        for row in rows:
            return ConflictInfo.from_tuple(row)
        return ConflictInfo(ConflictState.none, '')

    @writes
    def _update_state(self, name, state):
        descendants = self.ancestry.descendants(name)
        indexnode = self.index.node(name)

        oldstate = State(indexnode.state)
        delta_readiness = (state == State.done) - (oldstate == State.done)

        self.index.update_state(indexnode.name, state.value)
        if state == State.new:
            self.workers.remove_runinfo(indexnode.name)
        for descendant in descendants:
            descendant_indexnode = self.index.node(descendant)
            if descendant_indexnode.awaitcount == UNKNOWN_AWAITCOUNT:
                continue

            if delta_readiness != 0:
                self.index.update_awaitcount(
                    descendant_indexnode.name,
                    descendant_indexnode.awaitcount - delta_readiness,
                )

    @writes
    def remove_nodes(self, names):
        # Refactor: Too many things to remove that we can remember all of them.
        # We should subscribe some kind of registry even listener.
        for name in names:
            if self.ancestry.descendants(name):
                raise Exception(
                    f'Interal error: Trying to remove a node {name}'
                    f' with descendants {self.ancestry.descendants(name)}.'
                    f' Full list {names}'
                )
            self.ancestry.remove_node(name)
            self.clear_conflict(name)
            self.workers.remove_runinfo(name)
            self.resources.remove(name)
            self.frozentasks.remove(name)
            del self.topological_depth[name]
            del self.inputs[name]
            del self.sources[name]
            del self.has_records[name]
            del self.handlers[name]

        self.index.remove_multiple(names)

    def contains(self, name):
        return self.index.contains(name)

    @property
    def index(self):
        # XXX we need to hide the database tables
        # so we can keep them in sync
        # assert self.conn is not None
        return Index(self.conn, read_only=self.read_only)

    @property
    def workers(self):
        return Workers(self.conn, read_only=self.read_only)

    @property
    def ancestry(self):
        assert self.conn is not None
        return Ancestry(self.conn, read_only=self.read_only)

    @property
    def topological_depth(self):
        # Stores the depth inside the directed acyclic graph of each task.
        #
        # The depth is longest distance to root task, i.e., the depths
        # are a partial topological ordering of states.
        return topological_depth_table(self.conn, read_only=self.read_only)

    @property
    def resources(self):
        return LabelTable(
            'resources',
            self.conn,
            read_only=self.read_only,
            valid_tag_regex=r'[-\w]+$',
        )

    @property
    def frozentasks(self):
        return LabelTable('frozentasks', self.conn, read_only=self.read_only)

    @property
    def inputs(self) -> Mapping[str, str]:
        return TableMapping(
            self.conn,
            'inputs',
            'input',
            'VARCHAR(1024)',
            read_only=self.read_only,
        )

    @property
    def handlers(self) -> Mapping[str, str]:
        return TableMapping(
            self.conn,
            'handlers',
            'handler',
            'VARCHAR(1024)',
            read_only=self.read_only,
        )

    @property
    def workflows(self):
        return WorkflowTable(self.conn, read_only=self.read_only)

    @property
    def sources(self) -> Mapping[str, str]:
        return TableMapping(
            self.conn,
            'sources',
            'source',
            'VARCHAR(256)',
            read_only=self.read_only,
        )

    @property
    def has_records(self) -> Mapping[str, bool]:
        return TableMapping(
            self.conn,
            'has_records',
            'has_record',
            'BOOLEAN',
            read_only=self.read_only,
        )


class Connection:
    def __init__(
        self,
        filename,
        timeout: float,
        read_only: bool = False,
        initialize_tables=None,
    ):
        self.filename = filename
        self._conn = None
        self.timeout = timeout
        self.read_only = read_only

        self._initialize_tables = initialize_tables

    @property
    def execute(self):
        return self._conn.execute

    @property
    def executemany(self):
        return self._conn.executemany

    def __enter__(self):
        assert self._conn is None

        self._conn = self._connect()

        if not self.read_only and self._initialize_tables is not None:
            self._initialize_tables()
            # We don't want to initialize more than once if there are multiple
            # rounds of locking, so we set initializer to None afterwards.
            self._initialize_tables = None

        return self._conn

    def __exit__(self, type, value, tb):
        if type is None:
            action = 'COMMIT'
        else:
            action = 'ROLLBACK'
        self._conn.execute(action)
        self._conn = None

    def sneaky_commit(self):
        # Hack to allow impromptu flush of the current transaction.
        # It is not particularly safe to use this, since highlevel
        # code might rely on changes being transactional, and that will
        # not be the case if we commit here and there.
        # So try not to use this.
        self.execute('COMMIT')
        self.execute('BEGIN EXCLUSIVE')

    def _connect(self, max_retries=20):
        import time

        total_timeout = self.timeout
        pre_delay = 0.1
        warning_displayed = False
        while True:
            start = time.time()
            timeout = min(pre_delay + random() * 5, total_timeout)
            total_timeout -= timeout
            pre_delay += 1.5

            # This is the standard way in Python 3 to open a read only
            # sqlite3 database
            if self.read_only:
                database = f'file:{self.filename}?mode=ro'
                isolation_level = 'DEFERRED'
            else:
                database = self.filename
                isolation_level = 'EXCLUSIVE'

            try:
                connection = sqlite3.connect(
                    database,
                    timeout=timeout,
                    uri=self.read_only,
                    detect_types=sqlite3.PARSE_DECLTYPES
                    | sqlite3.PARSE_COLNAMES,
                    isolation_level=isolation_level,
                )
                connection.execute('PRAGMA foreign_keys = 1')
                connection.execute(f'BEGIN {isolation_level}')

                # If warning was displayed, also then display that we
                # got the lock
                if warning_displayed:
                    print(f'Obtained lock in {time.time() - start:.2f}.')

            except sqlite3.OperationalError as err:
                max_retries -= 1
                if total_timeout > 0 and max_retries > 0:
                    print(
                        'Warning: Failed to obtain lock in',
                        time.time() - start,
                        'due to',
                        err,
                    )
                    warning_displayed = True
                    sleep(timeout / 3)
                    continue
                msg = f'Failed to open sqlite3-connection to{self.filename}'
                raise RegistryError(msg) from err
            break

        return connection


class RegistryError(Exception):
    pass
