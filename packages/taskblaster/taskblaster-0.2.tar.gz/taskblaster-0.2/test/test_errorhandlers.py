import taskblaster as tb
from taskblaster import ErrorHandler, State
from taskblaster.abc import (
    ExceptionData,
    HandlerExceptionOutcome,
    Outcome,
    SkipHandlingOutcome,
    UpdateTaskOutcome,
)
from taskblaster.errorhandlers import (
    ErrorHandlerData,
    IncorrectHandlerReturnType,
)


class SomeRecoverableError(Exception):
    pass


class MyHandler(ErrorHandler):
    params = [
        {'some_key': 1},
        {'some_key': 2},
        {'some_key': 3},
        {'some_key': 4},
        {'some_key': 5},
    ]

    def handle(
        self,
        handler_data: ErrorHandlerData,
        loaded_task,
        exception_data: ExceptionData,
    ) -> Outcome:
        if exception_data.name == 'SomeRecoverableError':
            params = loaded_task.kwargs['params']
            params.update(self._get_params_by_attempt(handler_data.count))
            # XXX warden needs to update handler_data.updated_params
            # automatically when the params are updated.
            handler_data.updated_params.append(params)
            loaded_task.kwargs['params'] = params
            return UpdateTaskOutcome(loaded_task, exception_data, handler_data)
        else:
            return SkipHandlingOutcome(exception_data)

    def _get_params_by_attempt(self, count: int):
        return self.params[count]


class BrokenHandler(ErrorHandler):
    def handle(
        self, handler_data: ErrorHandlerData, loaded_task, exception_data
    ) -> Outcome:
        raise Exception(
            'Simulated Handler.handle() method raising an exception.'
        )


class IncorrectReturnType(ErrorHandler):
    def handle(
        self, handler_data: ErrorHandlerData, loaded_task, exception_data
    ) -> Outcome:
        return 'Purposely do not return an Outcome.'


def maybe_throw_an_error(params: dict, exception_succeeds: bool = False):
    # if exception_succeeds is true, we always fail so we can test
    # that max_attempts. If true, we 'handled the error' and return
    if exception_succeeds:
        if params['some_key'] < 5:
            raise SomeRecoverableError()
        else:
            return 'Successfully handled some recoverable error.'
    raise SomeRecoverableError()


# XXX the tasks on the workflow are the same because we attach different
# handlers. This is so we can ensure we can handle the various ways handlers
# can fail/succeed. We programmatically equip them with different error
# handlers using a helper classmethod later
@tb.workflow
class FailWorkflow:
    params = tb.var()

    @tb.task
    def broken_handler_handle_error(self):
        return tb.node(maybe_throw_an_error, params=self.params)

    @tb.task
    def return_incorrect_handle_type(self):
        return tb.node(maybe_throw_an_error, params=self.params)

    @tb.task
    def succeed_in_handling_error(self):
        return tb.node(
            maybe_throw_an_error,
            params=self.params,
            exception_succeeds=True,
        )


@tb.workflow
class WorkflowThatCanNOTHandleErrors:
    params = tb.var(default={'some_key': 0})

    @tb.task
    def cannot_handle_error(self):
        return tb.node(maybe_throw_an_error, params=self.params)

    @tb.task
    def succeed_in_handling_error(self):
        return tb.node(
            maybe_throw_an_error,
            params=self.params,
            exception_succeeds=True,
        )

    @tb.task
    def broken_handler_handle_error(self):
        return tb.node(maybe_throw_an_error, params=self.params)

    @tb.task
    def return_incorrect_handle_type(self):
        return tb.node(maybe_throw_an_error, params=self.params)

    @tb.subworkflow
    def subworkflow_that_fails(self):
        workflow_class = self.subworkflow_decorator(FailWorkflow)
        return workflow_class(params=self.params)

    @classmethod
    def subworkflow_decorator(cls, subwf_class):
        return subwf_class


def modify_handler_from_task(cls, tasks: dict, set_handler: bool = True):
    for meth, handler in tasks.items():
        task = getattr(cls, meth)
        task.error_handlers = [handler] if set_handler else []
    return cls


# using functino to attach handlers to class and reduce code duplication
def classception(handlers_to_override, set_handler: bool = True):
    class WorkflowThatCanHandleErrors(WorkflowThatCanNOTHandleErrors):
        params = tb.var(default={'some_key': 2})

        @classmethod
        def subworkflow_decorator(cls, subwf_class):
            for meth, handler in handlers_to_override.items():
                task = getattr(subwf_class, meth)
                task.error_handlers = [handler] if set_handler else []
            return subwf_class

    return WorkflowThatCanHandleErrors


@tb.workflow
class RecordsWithErrorHandlers:
    params = tb.var(default={'some_key': 0})

    @staticmethod
    def print_hello(params):
        return params

    @staticmethod
    def assert_state(record, expected_state: str):
        must_equal = record.state == expected_state
        assert must_equal
        return must_equal

    @tb.task(error_handlers=MyHandler(), has_record=True)
    def with_record_and_task_failed(self):
        return tb.node(maybe_throw_an_error, params=self.params)

    @tb.task
    def depend_on_failed_record(self):
        return tb.node(
            RecordsWithErrorHandlers.assert_state,
            record=tb.record(self.with_record_and_task_failed),
            expected_state=State.fail.value,
        )

    @tb.task(error_handlers=MyHandler(), has_record=True)
    def with_record_and_task_failed_then_succeeds_with_handler(self):
        return tb.node(
            maybe_throw_an_error, params=self.params, exception_succeeds=True
        )

    @tb.task
    def depend_on_failed_task_with_handler_passes(self):
        return tb.node(
            RecordsWithErrorHandlers.assert_state,
            record=tb.record(
                self.with_record_and_task_failed_then_succeeds_with_handler
            ),
            expected_state=State.done.value,
        )

    @tb.task(error_handlers=MyHandler(), has_record=True)
    def with_record_and_task_pass(self):
        return tb.node(
            RecordsWithErrorHandlers.print_hello, params=self.params
        )

    @tb.task
    def depend_on_succeeded_record(self):
        return tb.node(
            RecordsWithErrorHandlers.assert_state,
            record=tb.record(self.with_record_and_task_pass),
            expected_state=State.done.value,
        )


def check_task_results(failure_types, err_key, tool):
    for k, err in failure_types.items():
        if err[err_key] is not None:
            assert err[err_key] in tool.get_failure(k)
        else:
            assert err[err_key] == tool.get_failure(k)


sre = 'SomeRecoverableError'
err_noerr = {'no_handler': sre, 'handler': None}
err_handler1 = {'no_handler': sre, 'handler': HandlerExceptionOutcome.msg}
err_handler2 = {'no_handler': sre, 'handler': IncorrectHandlerReturnType.msg}
expected_task_results = {
    'succeed_in_handling_error': err_noerr,
    'subworkflow_that_fails/succeed_in_handling_error': err_noerr,
    'cannot_handle_error': {'no_handler': sre, 'handler': sre},
    'broken_handler_handle_error': err_handler1,
    'subworkflow_that_fails/broken_handler_handle_error': err_handler1,
    'return_incorrect_handle_type': err_handler2,
    'subworkflow_that_fails/return_incorrect_handle_type': err_handler2,
}
common_handlers = {
    'succeed_in_handling_error': MyHandler(),
    'broken_handler_handle_error': BrokenHandler(),
    'return_incorrect_handle_type': IncorrectReturnType(),
}
handlers_for_tasks = {'cannot_handle_error': MyHandler(), **common_handlers}


def test_kick_with_conflict(tool):
    tool.workflow(
        modify_handler_from_task(
            classception(common_handlers, False), handlers_for_tasks, False
        )()
    )
    tool.run()
    tool.count(done=0, fail=7)
    check_task_results(expected_task_results, 'no_handler', tool)

    # apply worker with handlers added, then tell warden to kick then to
    # partial state, resolve the conflict, run the workflow
    tool.workflow(
        modify_handler_from_task(
            classception(common_handlers), handlers_for_tasks
        )()
    )
    tool.kick()
    tool.resolve_conflict()
    tool.run()
    tool.count(done=2, fail=5)
    check_task_results(expected_task_results, 'handler', tool)


def test_kick_handler_to_action(tool):
    tool.workflow(
        modify_handler_from_task(
            classception(common_handlers, False), handlers_for_tasks, False
        )()
    )
    tool.run()
    tool.count(done=0, fail=7)
    check_task_results(expected_task_results, 'no_handler', tool)

    tool.workflow(
        modify_handler_from_task(
            classception(common_handlers), handlers_for_tasks
        )()
    )
    tool.kick()
    tool.count(partial=3, fail=4)
    tool.resolve_conflict()
    tool.run()
    tool.count(done=2, fail=5)
    check_task_results(expected_task_results, 'handler', tool)


def test_basic_error_handling(tool):
    tool.workflow(
        modify_handler_from_task(
            classception(common_handlers), handlers_for_tasks
        )()
    )
    tool.run()
    check_task_results(expected_task_results, 'handler', tool)
    tool.count(done=2, fail=5)


def test_records_with_handling(tool):
    tool.workflow(RecordsWithErrorHandlers())
    tool.run()
    tool.count(done=8, fail=1)
    assert sre in tool.get_failure('with_record_and_task_failed')
