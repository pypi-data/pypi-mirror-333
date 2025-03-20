from __future__ import annotations

import os
import traceback
from dataclasses import field
from typing import Dict, List

from taskblaster.abc import (
    ExceptionData,
    HandlerExceptionOutcome,
    MaxAttemptsOutcome,
    NoHandlersOutcome,
    Outcome,
    tb_dataclass,
)


class IncorrectHandlerReturnType(Exception):
    msg = 'All handler methods must return an outcome.'

    def __init__(self, handler, outcome):
        msg = f'{self.msg} {handler.name}.handle() returned: {outcome}'
        super().__init__(msg)


@tb_dataclass
class ErrorHandlerData:
    max_attempts: int
    updated_params: List[Dict] = field(default_factory=list)

    @property
    def count(self):
        return len(self.updated_params)


class Warden:
    """The warden nurtures the tree as it grows, saving users time."""

    def __init__(self, cache, log, name, global_max_attempts: int = 5):
        self.name = name
        self.cache = cache
        self.registry = cache.registry
        self.codec = cache.json_protocol
        self.log = log
        self.global_max_attempts = global_max_attempts

        _handlers_buf = self.registry.handlers.get(name, '[]')
        self.all_handlers = (
            self.codec.loads_task_buf(_handlers_buf, self.name) or []
        )

        self.log_warden(f'Task {self.name} has handlers {self.all_handlers}.')

    def log_debug(self, msg, with_traceback=False):
        if os.environ.get('TB_DEBUG', False):
            self.log(f'WARDEN DEBUG: {msg}')
        if with_traceback:
            print(traceback.format_exc(), flush=True)

    def log_warden(self, msg):
        self.log(f'WARDEN: {msg}')

    @property
    def has_handlers(self):
        return len(self.all_handlers) > 0

    def handle(self, loaded_task, exception_data: ExceptionData) -> Outcome:
        assert isinstance(exception_data, ExceptionData)
        # no handlers outcome
        if not self.has_handlers:
            self.log_warden('No handlers found.')
            return NoHandlersOutcome(exception_data)
        self.log_warden(f'Checking {exception_data} for each handler.')

        # now load handler data
        handler_data = self.load_handler_data(loaded_task)
        if handler_data.count >= handler_data.max_attempts:
            self.log_warden(
                'MAX ATTEMPTS reached. Unable to handle exception.'
            )
            return MaxAttemptsOutcome(exception_data)

        for handler in self.all_handlers:
            self.log_debug(f'Calling handler {handler.name}.handle()')
            try:
                outcome = handler.handle(
                    handler_data, loaded_task, exception_data
                )
            except Exception as e:
                self.log_debug(
                    f'{handler.name}.handle() raised the following exception '
                    f'during handling:',
                    True,
                )
                return HandlerExceptionOutcome(
                    exception_data, ExceptionData.from_exception(e)
                )

            # handler.handle is required to return an Outcome
            if not isinstance(outcome, Outcome):
                self.log_debug(
                    f'Handler {handler.name} did not return an outcome during '
                    f'handling of {exception_data.info}. Ensure {handler.name}'
                    '.handle returns Outcome.'
                )
                return HandlerExceptionOutcome(
                    exception_data,
                    ExceptionData.from_exception(
                        IncorrectHandlerReturnType(handler, outcome)
                    ),
                )

            # handler returns skip true if it fails to catch the error
            if not outcome._is_unhandled:
                self.log_debug(f'{handler.name}: {outcome.explanation}')
                break

        self.log_warden(f'{outcome.name}: {outcome.explanation}')
        return outcome

    def load_handler_data(self, loaded_task):
        # load handler data from disk, or construct it because we are count 0
        try:
            return self.codec.loads_task_buf(
                loaded_task.entry.handlersdatafile.read_text(),
                loaded_task.name,
            )
        except FileNotFoundError:
            self.log_warden('Initializing handler_data.json.')
            return ErrorHandlerData(max_attempts=self.global_max_attempts)

    def write_handler(
        self, loaded_task, handler_data: ErrorHandlerData
    ) -> None:
        loaded_task.entry.handlersdatafile.write_text(
            self.codec.serialize(handler_data, loaded_task.name)
        )

        serialized_input = self.cache.json_protocol.serialize_node(
            loaded_task.node, loaded_task.name
        )
        loaded_task.entry.updatedinputfile.write_text(serialized_input)


# we need one more layer to protect against useless runs: handler doesn't
# actually change anything. one should compare the loaded_tasks (the old) and
# new loaded_task (handler task)
