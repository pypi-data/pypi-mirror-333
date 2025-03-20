import os
import sys
from contextlib import contextmanager
from pathlib import Path

from taskblaster.state import State


def get_actions(obj):
    actions = {}
    for name, value in getattr(obj, '__tb_actions__', {}).items():
        if isinstance(value, str):
            value = getattr(obj, value)

        # (It might be wiser to the decorator to check callability)
        assert callable(value), f'Action not callable, got {value!r}'
        actions[name] = value
    return actions


def get_task_actions(function, output):
    # (Output can override the action names, for better or worse)
    return {**get_actions(function), **get_actions(output)}


def color(string, fg=None, bg=None):
    import click

    if fg and ':' in fg and bg is None:
        fg, bg = fg.split(':')
    return click.style(string, fg=fg, bg=bg)


def absolute(pth):
    if '..' in pth.parts:
        return pth.resolve()
    else:
        return pth.absolute()


def is_subpath(directory, fromdir):
    try:
        directory.relative_to(fromdir)
        return True
    except ValueError:
        return False


def relative_path_walkup(directory, fromdir):
    if sys.version_info >= (3, 12, 1):
        return directory.relative_to(fromdir, walk_up=True)
    else:
        common = Path(
            os.path.commonpath([absolute(directory), absolute(fromdir)])
        )
        to_common = Path('../' * len(fromdir.relative_to(common).parts))
        return to_common / directory.relative_to(common)


@contextmanager
def workdir(directory):
    cwd = Path.cwd()
    try:
        os.chdir(directory)
        yield
    finally:
        os.chdir(cwd)


def normalize(string):
    from hashlib import sha256

    # The string must be a valid graphviz node name.  We just
    # do a hexdigest and be sure that the first character is alphabetic:
    return 'x' + sha256(string.encode('utf-8')).hexdigest()


def pattern_match(pth, pattern):
    if isinstance(pattern, list):
        for ptrn in pattern:
            if pattern_match(pth, ptrn):
                return True
        return False
    # XXX if pattern absolute then ** glob patterns are ignored unless
    # leading with a /
    if pattern != '**':
        return Path('/' + pth).match('/' + pattern)
    return Path(pth).match(pattern)


graphviz_state_colors = {
    State.done: 'mediumspringgreen',
    State.run: 'gold1',
    State.fail: 'crimson',
    State.new: 'cornflowerblue',
}


def tree_to_graphviz_text(tree):
    tokens = ['digraph tasks {']

    cache = tree.cache
    registry = tree.registry

    graph = {}

    for node in tree.nodes_topological():
        ancestors = registry.ancestry.ancestors(node.name)
        graph[node.name] = ancestors

    for name in graph:
        graphviz_name = normalize(name)
        state = registry.index.node(name).state
        color = graphviz_state_colors.get(state, 'grey')
        if color == 'crimson':
            fontcolor = 'white'
        else:
            fontcolor = 'black'

        json_protocol = tree.cache.json_protocol
        encoded_task = cache.encoded_task(name)
        node = json_protocol.deserialize_node(
            encoded_task.serialized_input, name
        )

        # Align nicely for use with monospace font:
        labelparts = [
            f'name:   {name}\\l',
            f'target: {node.target}(…)\\l',
            f'state:  {state.name}\\l',
        ]

        node_attrs = dict(
            label=''.join(labelparts),
            fontname='monospace',
            style='rounded,filled',
            color=color,
            fontcolor=fontcolor,
            shape='rectangle',
        )

        attrs = ' '.join(
            f'{key}="{value}"' for key, value in node_attrs.items()
        )
        tokens.append(f'  {graphviz_name} [{attrs}]')

    for descendant, ancestors in graph.items():
        assert descendant in graph
        node2 = normalize(descendant)

        for ancestor in ancestors:
            assert ancestor in graph
            node1 = normalize(ancestor)
            tokens.append(f'  {node1} -> {node2}')

    tokens.append('}')
    return '\n'.join(tokens)


def format_duration(start_time, end_time):
    """
    If end_time is not given, duration is the current time running. If end_time
    is given, duration is the time the calculation took to run.

    :param start_time: Datetime start time string.
    :param end_time: Datetime end time string, if none is provided,
        datetime.now() is used.
    :return: duration = end_time - start_time
    """
    import datetime

    if start_time is None:
        return ''

    end_time = datetime.datetime.now() if end_time is None else end_time

    duration = end_time - start_time
    days, seconds = duration.days, duration.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds %= 60
    if days > 0:
        duration = f'{days}d {hours:02}:{minutes:02}:{seconds:02}'
    else:
        duration = f'   {hours:02}:{minutes:02}:{seconds:02}'

    return duration
