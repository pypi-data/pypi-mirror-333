from collections.abc import Iterable, MutableMapping
from dataclasses import asdict, astuple, dataclass

from taskblaster import TB_STRICT, writes

tablename = 'workflows'

create_table = f"""\
CREATE TABLE IF NOT EXISTS {tablename} (
  name VARCHAR(256) PRIMARY KEY,
  importpath VARCHAR(256),
  serialized_input VARCHAR(256),
  source VARCHAR(256),
  metadata VARCHAR(256)
)
"""

# In general name can be different from the directory.  Maybe
# we need to save the directory as well?


@dataclass
class WorkflowData:
    name: str
    importpath: str
    serialized_input: str
    source: str
    metadata: str

    def __post_init__(self):
        if TB_STRICT:
            assert self.source is not None


class BoundWorkflow:
    def __init__(self, workflow_obj, data: WorkflowData, rn, finished):
        self.workflow_obj = workflow_obj
        self.data = data
        self.rn = rn
        self.finished = finished

    @classmethod
    def bind(cls, name, workflow, serialized_input, source, rn, finished=True):
        wf_cls = workflow.__class__
        importpath = f'{wf_cls.__module__}.{wf_cls.__qualname__}'

        # In order not to update all the tests, some of these default
        # to None here and there in the code.
        #
        # We should remove that, but until then:
        assert name != '.'

        data = WorkflowData(
            name, importpath, serialized_input, source, metadata=''
        )
        return cls(workflow, data, rn, finished)


class WorkflowTable(MutableMapping):
    def __init__(self, conn, read_only=False):
        self.conn = conn
        self.read_only = read_only

    @classmethod
    def initialize(cls, conn):
        conn.execute(create_table)
        return cls(conn)

    def __getitem__(self, name: str) -> WorkflowData:
        query = f'SELECT * FROM {tablename} WHERE name=?'
        row = self.conn.execute(query, (name,)).fetchone()
        if row is None:
            raise KeyError(name)
        return WorkflowData(*row)

    def __iter__(self) -> Iterable[str]:
        query = f'SELECT name FROM {tablename}'
        for nametuple in self.conn.execute(query).fetchall():
            yield nametuple[0]

    def __len__(self) -> int:
        query = f'SELECT COUNT(*) FROM {tablename}'
        cursor = self.conn.execute(query)
        return cursor.fetchone()[0]

    @writes
    def __setitem__(self, name: str, workflowdata: WorkflowData) -> None:
        # name/workflowdata are actually redundant, but we get a lot of
        # value from Mapping so let's just leave it at that.
        assert name == workflowdata.name
        if TB_STRICT:
            if workflowdata.name != '':
                assert workflowdata.source in self, workflowdata
        self._add(workflowdata)

    @writes
    def __delitem__(self, name: str) -> None:
        query = f'DELETE FROM {tablename} WHERE name=?'
        self.conn.execute(query, (name,))

    def _add(self, data):
        # Currently we have no metadata, but we might need to contain
        # some kind of "selector" e.g. to apply totree() only on some
        # materials.  I wonder how we represent that selector.
        query = f"""\
INSERT INTO {tablename} (name, importpath, serialized_input, source, metadata)
VALUES (?, ?, ?, ?, ?)
ON CONFLICT (name)
DO UPDATE SET importpath=?, serialized_input=?, source=?, metadata=?
"""

        dct = asdict(data)
        for name, thing in dct.items():
            assert thing is not None, name

        tuple1 = astuple(data)
        tuple2 = tuple1[1:]
        self.conn.execute(query, (*tuple1, *tuple2))


# What do we need here?
#  * Removing a name must remove workflows under that name.
#    But what are the repercussions to tasks, can there be a task
#    that remains even though its workflow is deleted?
#  * We need an ancestry graph of workflows, so removing
#    a workflow removes descendant workflows.
#  * List workflows?
#    Should workflows be listed in ls ordinarily?
#    Should it be a different command?
