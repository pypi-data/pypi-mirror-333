import importlib

import click

import taskblaster.cli.main as cli
from taskblaster.abc import ExceptionData


@click.group()
def warden():  # noqa: F811
    """Use Warden to handle failures."""


@warden.command()
@cli.tree_argument()
@cli.tag_option()
@cli.with_repo
def kick(repo, tree, tags):
    """Kick failed tasks to the warden's handler added after failure occurs."""
    # kick needs to reset records if a task has_records
    from taskblaster.state import State
    from taskblaster.worker import LoadedTask, Worker

    tree = repo.tree(tree, states={State.fail}, tags=tags)
    worker = Worker(repo)

    for indexnode in tree.nodes():
        worker.log(
            f'WARDEN: looping over tasks in tree {indexnode.name} {indexnode}'
        )
        entry = repo.cache.entry(indexnode.name)
        target, kwargs = worker.actualize_runtime_files(entry, indexnode.name)
        has_record = repo.registry.has_records.get(indexnode.name, False)

        loaded_task = LoadedTask(
            entry, indexnode.name, target, kwargs, has_record
        )
        # get exception data from dropped stacktrace/exception_data.json
        worker.log(f'WARDEN: loading exception from: {indexnode.name}')
        try:
            exception_data = ExceptionData.read(
                worker.cache.json_protocol, loaded_task
            )
            worker.log('WARDEN: loading ExceptionData.')
        # XXX We can remove this code once errors are reliably written as
        # exception_data.json. Until then, we have to load stacktrace files and
        # hope we can get enough error information to handler the error. It is
        # only needed in kick since moving forward the worker will write the
        # exception to a json file.
        except FileNotFoundError:
            stacktraces = list(entry.stacktracefiles())
            if len(stacktraces) > 0:
                worker.log('WARDEN: found stacktrace file to kick to handler')
                err = stacktraces[0].read_text().split('\n')
                exception_data = ExceptionData.from_exception(
                    load_exception(err)
                )
                worker.log('WARDEN: loading ExceptionData from stacktrace')
        # update to partial state
        worker.warden_handle_failed_state(
            indexnode.name, loaded_task, exception_data
        )


def load_exception(err):
    for line in reversed(err):
        if line == '':
            continue
        bodymsg = line.split(':')
        body = bodymsg[0]
        msg = bodymsg[1:]

        modname, classname = body.rsplit('.', 1)
        if modname:
            module = importlib.import_module(modname)
        cls = getattr(module, classname)

        exception = cls(*msg)
        return exception


@warden.command()
@cli.tree_argument()
@cli.tag_option()
@cli.with_repo
def update_task_inputs(repo, tree, state, tags):
    """User override of the task's inputs."""


@warden.command()
@cli.tree_argument()
@cli.with_repo
def handler_rollback(repo, tree, state):
    """XXX if you use a handler, this will be used to undo the last attempt
    the handler made."""
