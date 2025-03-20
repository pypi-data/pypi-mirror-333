from enum import Enum

_unsuccessful = set('FCTMø')
_descendants_can_be_submitted = set('nqhrd')

# It is necessary to have q here for now, or otherwise the result task update
# done by Workflow.init task doesn't overwrite the task (displays conflict)
# if it is queued.
_pristine = set('nqC')

_bad_color = 'bright_red'

# Whether a directory is associated with this task.
# This may currently happen to be "not pristine", but that may change.
_have_data = set('rdFp')

# XXX These are click color names
_colors = dict(
    ø='yellow',
    n='bright_blue',
    q='cyan',
    Q='cyan',
    h='yellow',
    r='bright_yellow',
    d='green',
    p='magenta',
    F=_bad_color,
    C='yellow',
    T=_bad_color,
    M=_bad_color,
)


class State(Enum):
    new = 'n'
    queue = 'q'
    # myqueue = 'Q'
    # hold = 'h'
    run = 'r'
    done = 'd'
    fail = 'F'
    # timeout = 'T'
    # memory = 'M'
    partial = 'p'
    cancel = 'C'
    # missing = 'ø'

    @classmethod
    def statecodes(cls):
        return ''.join(state.value for state in cls)

    @property
    def have_data(self):
        return self.value in _have_data

    @property
    def is_pristine(self):
        return self.value in _pristine

    @property
    def unsuccessful(self):
        return self.value in _unsuccessful

    @property
    def color(self):
        return _colors[self.value]

    @property
    def ansiname(self):
        import click

        return click.style(self.name, self.color)
