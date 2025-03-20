from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property, lru_cache
from pathlib import Path

# from taskblaster.cache import FileCache
from taskblaster.state import State
from taskblaster.util import color, format_duration, relative_path_walkup


@dataclass
class Column:
    key: str
    methodname: str
    name: str | None
    width: int
    ellipsize: bool = False
    description: str | None = None

    def __post_init__(self):
        if self.description is None:
            self.description = self.name

    def padded_title(self):
        return self.name.ljust(self.width)


def column(
    key: str, width: int, *, title: str | None = None, **kwargs
) -> Column:
    def deco(meth):
        if title is None:
            name = meth.__name__
        else:
            name = title

        meth.column_format = Column(key, meth.__name__, name, width, **kwargs)
        return meth

    return deco


def ls_listing(columns, cache, treedir, fromdir):
    return Listing(columns, cache, treedir, fromdir)


@dataclass
class Listing:
    # We should refactor so column information is defined in a single place.
    # Here we define the headers but the formatting is done elsewhere.
    # nodes: list[nodes]
    columns: str
    cache: object  # FileCache
    treedir: Path
    fromdir: Path

    def nodeinfo(self, indexnode, columns):
        return NodeInfo(
            indexnode=indexnode,
            cache=self.cache,
            treedir=self.treedir,
            fromdir=self.fromdir,
            columns=columns,
        )

    def to_string(self, indexnodes):
        columns = TaskListing.select_columns(self.columns)
        yield from TaskListing.header(columns)

        for indexnode in indexnodes:
            yield self.nodeinfo(indexnode, columns).to_string()


# TODO: Listing should be BaseListing instead of the current TaskListing.
# Also, NodeInfo should be eliminated/merged with current TaskListing.
class NodeInfo:
    def __init__(self, indexnode, cache, treedir, fromdir, columns):
        from taskblaster.future import parent_state_info

        self.indexnode = indexnode
        self.name = indexnode.name
        self.state = indexnode.state
        self.relpath = relative_path_walkup(treedir / indexnode.name, fromdir)
        self.columns = columns
        assert not isinstance(self.columns, str)

        self.registry = cache.registry
        self.cache = cache

        self.parent_state_info = parent_state_info(
            registry=self.registry, name=self.name
        )

        self.tags = self.registry.resources.get_tags(self.name)

    @cached_property
    def runinfo(self):
        return self.registry.workers.get_runinfo(self.name)

    @cached_property
    def conflict_info(self):
        return self.registry.conflict_info(self.name)

    def to_string(self) -> str:
        line = format_line_from_columns(TaskListing(self), self.columns)

        if self.exception is not None:
            line += '\n^^^^  ' + color(self.exception, 'bright_red')
            # So not really a line then

        return line

    @cached_property
    def exception(self) -> str | None:
        if self.runinfo is None or self.runinfo.exception is None:
            return None

        exception = self.runinfo.exception
        if len(exception) > 120:
            exception = exception[:120] + '…'
        return exception


def format_timestamp(timestamp) -> str:
    if timestamp is None:
        return ''
    return timestamp.strftime('%y-%m-%d %H:%M')


def format_line_from_columns(listing, columns) -> str:
    import click

    output = []
    spacing_deficit = 0

    for column in columns:
        meth = getattr(listing, column.methodname)
        token = meth()

        if column.ellipsize and len(token) > column.width:
            token = token[: column.width - 1] + '…'

        printed_width = len(click.unstyle(token))
        target_width = column.width - spacing_deficit
        padding_length = max(target_width - printed_width, 0)
        token += ' ' * padding_length
        spacing_deficit += printed_width + padding_length - column.width
        output.append(token)

    return ' '.join(output).rstrip()


class BaseListing:
    @classmethod
    @lru_cache
    def all_columns(cls):
        """Get all Column objects on this class."""
        columns = {}
        for name, item in vars(cls).items():
            column_format = getattr(item, 'column_format', None)
            if column_format is None:
                continue
            columns[column_format.key] = column_format
        return columns

    @classmethod
    def select_columns(cls, specifier: str):
        all_columns = cls.all_columns()
        return [all_columns[key] for key in specifier]

    @classmethod
    def header(cls, columns):
        padded_titles = [column.padded_title() for column in columns]
        headerline = ' '.join(padded_titles).rstrip()
        underline = ' '.join('─' * len(title) for title in padded_titles)
        yield headerline
        yield underline


class TaskListing(BaseListing):
    default_columns = 'sirITf'

    def __init__(self, nodeinfo):
        self.nodeinfo = nodeinfo
        self.indexnode = self.nodeinfo.indexnode
        self.state = self.indexnode.state
        self.name = self.indexnode.name

        self.conflict_info = self.nodeinfo.conflict_info
        self.cache = self.nodeinfo.cache
        self.runinfo = self.nodeinfo.runinfo

    @property
    def okcount(self):
        return self.nodeinfo.parent_state_info[0]

    @property
    def deps_color(self):
        return self.nodeinfo.parent_state_info[2]

    @property
    def nparents(self):
        from taskblaster.registry import UNKNOWN_AWAITCOUNT

        n = self.nodeinfo.parent_state_info[1]
        if self.indexnode.awaitcount == UNKNOWN_AWAITCOUNT:
            n = '?'
        return n

    @cached_property
    def serialized_input(self) -> str:
        return self.nodeinfo.cache.registry.inputs[self.name]

    @column('f', 29)
    def folder(self):
        if self.nodeinfo.cache.registry.frozentasks.get_tags(self.name):
            textcolor = 'white'
        elif self.state.have_data:
            textcolor = 'bright_green'
        else:
            textcolor = 'yellow'
        return color(str(self.nodeinfo.relpath), textcolor)

    @column('s', title='state', width=8)
    def _state_column(self):
        # (Named to avoid clash with self.state)
        return color(self.state.name, self.state.color)

    @column('i', 10)
    def info(self):
        info = [f'{self.okcount}/{self.nparents}']
        info_color = self.deps_color

        if self.cache.registry.frozentasks.get_tags(self.name):
            info.append('❄')
            info_color = State.fail.color

        if self.conflict_info.is_conflict():
            info.append(self.conflict_info.abbreviation)

        tags = self.nodeinfo.tags
        if len(tags) > 0:
            info.append(f'tags={len(tags)}')
        info_str = ' '.join(info)
        return color(info_str, info_color)

    @column('I', 11, description='myqueue id and subworker')
    def worker(self):
        if self.runinfo is None:
            return ''
        return color(self.runinfo.subworkerid, self.state.color)

    @column('r', 11)
    def tags(self):
        return ','.join(self.nodeinfo.tags)

    @column(
        't',
        title='start time'.ljust(15) + 'end time',
        width=15 + 16,
        description='time info',
    )
    def starttime_and_endtime(self):
        if self.runinfo is None:
            return ''

        runinfo = self.nodeinfo.runinfo

        start_time = format_timestamp(runinfo.start_time)
        end_time = format_timestamp(runinfo.end_time)
        return f'{start_time} {end_time}'

    # (padded so title aligns with hours)
    @column('T', width=11, title='   time', description='time duration')
    def duration(self):
        if self.runinfo is None:
            return ''

        duration = format_duration(
            start_time=self.runinfo.start_time,
            end_time=self.runinfo.end_time,
        )
        return color(str(duration), self.state.color)

    @column('c', 11)
    def conflict(self):
        conflict_state = self.conflict_info.state
        return color(conflict_state.name, conflict_state.color)

    @column('C', title='conflict info', width=15)
    def _conflict_info(self):
        return self.nodeinfo.conflict_info.colordiff(self.serialized_input)

    @column('o', 24, ellipsize=True)
    def output(self):
        if self.indexnode.state != State.done:
            return color('ø', 'yellow')

        return repr(self.nodeinfo.cache.entry(self.name).output())

    @column('Z', 6, description='frozen info')
    def frozen(self):
        return '|'.join(self.cache.registry.frozentasks.get_tags(self.name))

    @column('S', 12)
    def source(self):
        return self.cache.registry.sources[self.name]
