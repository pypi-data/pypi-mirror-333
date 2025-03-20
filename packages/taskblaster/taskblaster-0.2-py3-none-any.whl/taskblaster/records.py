from __future__ import annotations

from pathlib import Path
from typing import Any

from taskblaster.abc import tb_dataclass
from taskblaster.future import Future
from taskblaster.state import State


@tb_dataclass
class Record:
    name: str
    inputs: dict[str, Any]
    directory: Path
    output: Any
    state: State

    def __repr__(self):
        return f'<Record({self.name}, {self.directory})'


def create_task_record(name: str) -> Record:
    """This creates persistent data for users and should not be refactored
    without ensuring the persistent data remains unaffected."""
    from taskblaster.repository import Repository

    my_repo = Repository.find()
    with my_repo:
        return get_record_from_repo(name, my_repo)


def get_record_from_repo(name: str, repo) -> Record:
    encoded_task = repo.cache.encoded_task(name)
    future = Future(encoded_task, repo.cache)

    output = future._actual_output if future.has_output() else None
    inputs = future._actual_inputs
    state = future.indexnode.state
    return Record(name, inputs, future.directory, output, state.value)
