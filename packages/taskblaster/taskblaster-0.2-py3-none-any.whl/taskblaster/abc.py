from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, fields


def tb_dataclass(cls):
    cls = dataclass(cls)

    def tb_encode(self):
        return {
            field.name: getattr(self, field.name) for field in fields(self)
        }

    @classmethod
    def tb_decode(cls, data):
        return cls(**data)

    cls.tb_encode = tb_encode
    cls.tb_decode = tb_decode

    return cls


@tb_dataclass
class ExceptionData:
    module: str
    name: str
    info: str

    @classmethod
    def from_exception(cls, exception: BaseException):
        assert isinstance(exception, BaseException)
        e_cls = type(exception)
        info = f'{e_cls.__name__}: {str(exception)}'
        return cls(module=e_cls.__module__, name=e_cls.__name__, info=info)

    def write(self, codec, loaded_task):
        loaded_task.entry.exceptiondatafile.write_text(
            codec.serialize(self.tb_encode(), loaded_task.name)
        )

    @classmethod
    def read(cls, codec, loaded_task):
        return cls(
            **codec.loads_task_buf(
                loaded_task.entry.read_datafied_exception(), loaded_task.name
            )
        )

    def __repr__(self):
        return (
            f'{self.__class__.__name__}(info={self.info}, module={self.module}'
            f', name={self.name})'
        )


class ErrorHandler(ABC):
    def __init__(self, max_attempts: int = 5):
        self.max_attempts = max_attempts

    @abstractmethod
    def handle(
        self, handler_data, loaded_task, exception_data: ExceptionData
    ) -> Outcome:
        """this is the user's implementation for handling exceptions"""
        pass

    # XXX make sure to implement this correctly
    def tb_encode(self):
        return dict(self.__dict__)

    @classmethod
    def tb_decode(cls, dct: dict):
        return cls(**dct)

    def __repr__(self):
        return f'{self.__class__.__name__}(max_attempts={self.max_attempts})'

    @property
    def name(self):
        return self.__class__.__name__


class Outcome:
    explanation = 'Your handler returned a standard Outcome.'

    def __init__(self, exception_data: ExceptionData):
        assert isinstance(exception_data, ExceptionData)
        self.exception_data = exception_data

    @property
    def update_task_partial(self):
        return False

    @property
    def write_datafiles(self):
        return False

    @property
    def create_record(self):
        return True

    @property
    def update_task_failed(self):
        return True

    @property
    def update_tags(self):
        return False

    @property
    def name(self):
        return self.__class__.__name__

    @property
    def explain(self):
        return self.explanation

    @property
    def _is_unhandled(self):
        # XXX This is used internally in the warden.handle to skip to the next
        # handler in the handlers list.
        return False


class UpdateTaskOutcome(Outcome):
    explanation = """Handler returned UpdateTaskOutcome. The handler
successfully handled the error. Warden will now update the task."""

    def __init__(self, loaded_task, exception, handler_data):
        super().__init__(exception_data=exception)
        self.loaded_task = loaded_task
        self.handler_data = handler_data

    @property
    def update_task_partial(self):
        return True

    @property
    def write_datafiles(self):
        return True

    @property
    def create_record(self):
        return False

    @property
    def update_task_failed(self):
        return False


# WARDEN.handle() Outcomes that indicate the Handler encountered an issue while
# handling the exception
class NoHandlersOutcome(Outcome):
    explanation = """Found no registered handlers on task. Marking task as
    failed."""
    pass


class MaxAttemptsOutcome(Outcome):
    explanation = """The handler has reached the maximum attempts without
successfully handling the error. Marking task as failed."""
    pass


class HandlerExceptionOutcome(Outcome):
    explanation = """The handler passed to the warden raised an exception
during handling. Check the log file for the stacktrace. Skipping record
creation."""
    msg = 'Handler threw the following exception:'

    def __init__(self, exception_data, handler_exception_data):
        assert isinstance(exception_data, ExceptionData)
        exception_data.info = (
            f'{HandlerExceptionOutcome.msg} {handler_exception_data.info}.\n'
            f'Trying to handle the original exception: {exception_data.info}'
        )
        super().__init__(exception_data=exception_data)

    @property
    def create_record(self):
        return False


class SkipHandlingOutcome(Outcome):
    explanation = """Handler was unable to handler the exception, returning
SkipHandlingOutcome. Continuing to the next handler or marking task as
failed."""

    @property
    def _is_unhandled(self):
        return True
