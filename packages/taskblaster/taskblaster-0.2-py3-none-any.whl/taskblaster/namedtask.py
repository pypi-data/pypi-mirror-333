from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from taskblaster import Node, Reference
from taskblaster.abc import ErrorHandler


@dataclass
class Task:
    name: str
    node: Node
    kwargs: None = None  # XXX to be removed
    branch: str = None
    source: str | None = None
    tags: set = field(default_factory=set)
    has_record: bool = False
    error_handlers: list[ErrorHandler] = field(default_factory=list)
    _if: dict | None = None
    jump: str | None = None

    def __post_init__(self) -> None:
        if self.kwargs is not None:
            import warnings

            warnings.warn(
                'Please use Task(name, tb.Node(target, kwargs), ...)',
                FutureWarning,
            )

            self.node = Node(self.node, self.kwargs)
            self.kwargs = None

        # assert self.source is not None
        assert self.branch is not None
        assert self.tags is not None
        # Except totree (to be removed), the source and fullname
        # are mostly redundant and we can verify that:

        # if self.source == '':
        #     assert '/' not in self.name, self.name
        # else:
        #     assert self.name.split('/')[:-1] == self.source.split('/')

    def signature(self) -> str:
        return self.node.signature()

    def add_implicit_dependency(
        self, dependency: Reference, *, remove: bool
    ) -> None:
        """Add implicit dependency to Task

        We store the dependencies in kwargs in a list of 2-tuples in a variable
        called either __tb_implicit__ or __tb_implicit_remove__ with the
        full name of the dependency, and the dependency itself in the tuple.

        In case of __tb_implicit__, unrun will unrun this task, if the
        implicit dependency is unrun.

        In case of __tb_implicit_remove__, unrun will remove this task,
        if the 'implicit remove' dependency is unrun.
        """
        if not hasattr(dependency, 'name'):
            raise AttributeError('No attribute called name in dependency.')
        argname = f'__tb_implicit{"_remove" if remove else ""}__'

        # ~~~~~ ☠ ☠ ☠ XXX ☠ ☠ ☠ Avoid mutation ☠ ☠ ☠ !!!!! ☠ ☠ ☠ ~~~~~~~
        if argname not in self.node.kwargs:
            self.node.kwargs[argname] = []
        for name, dep in self.node.kwargs[argname]:
            if name == dependency.name:
                raise Exception(
                    f'Task {self.name} already has a dependency {name}.'
                )
        if not Path(self.name).parent.is_relative_to(
            Path(dependency.name).parent
        ):
            raise RuntimeError(
                'name', self.name, 'implicit_dependency', dependency.name
            )
        self.node.kwargs[argname].append((dependency.name, dependency))

    def __repr__(self) -> str:
        sig = self.signature()
        return f'Task({self.name}, {sig})'
