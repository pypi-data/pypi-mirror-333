from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum

from taskblaster.util import color


class ConflictState(Enum):
    none = 'n'
    resolved = 'r'
    conflict = 'c'

    @property
    def color(self):
        conflictcolors = {'n': 'green', 'r': 'bright_blue', 'c': 'red'}
        return conflictcolors[self.value]


@dataclass
class ConflictInfo:
    state: ConflictState
    conflicting_input: str

    def __post_init__(self):
        if not self.is_conflict():
            assert self.conflicting_input == ''

    def is_conflict(self):
        return self.state is not ConflictState.none

    @property
    def abbreviation(self) -> str | None:
        char = self.state.value
        return None if char == 'n' else char.upper()

    @classmethod
    def from_tuple(cls, tupl):
        return cls(ConflictState(tupl[0]), tupl[1])

    def astuple(self):
        return (self.state.value, self.conflicting_input)

    def replace(self, **kwargs):
        return replace(self, **kwargs)

    def colordiff(self, old_input: str):
        if self.state == ConflictState.none:
            return 'No conflict'
        return color_conflictinfo(old_input, self.conflicting_input)


def oldcolor(string):
    return color(string, 'red')


def newcolor(string):
    return color(string, 'bright_yellow')


def highlight_differences(old: str, new: str) -> tuple[str, str]:
    from difflib import SequenceMatcher

    import click

    matcher = SequenceMatcher(None, old, new)

    oldtokens = []
    newtokens = []

    for op, start1, end1, start2, end2 in matcher.get_opcodes():
        oldtoken = old[start1:end1]
        newtoken = new[start2:end2]

        if op == 'equal':
            assert oldtoken == newtoken
            oldtokens.append(oldtoken)
            newtokens.append(newtoken)
        elif op == 'insert':
            assert not oldtoken
            newtokens.append(newcolor(newtoken))
        elif op == 'replace':
            oldtokens.append(oldcolor(oldtoken))
            newtokens.append(newcolor(newtoken))
        elif op == 'delete':
            assert not newtoken
            oldtokens.append(oldcolor(oldtoken))
        else:
            raise RuntimeError(f'Strange diffing operation {op}')

    highlighted_old = ''.join(oldtokens)
    highlighted_new = ''.join(newtokens)
    assert click.unstyle(highlighted_old) == old
    assert click.unstyle(highlighted_new) == new
    return highlighted_old, highlighted_new


def color_conflictinfo(msg1: str, msg2: str) -> str:
    """Highlight differences between two strings."""
    msg1_new, msg2_new = highlight_differences(msg1, msg2)
    return f'Input changed. Old input\n {msg1_new}\n New input:\n {msg2_new}'
