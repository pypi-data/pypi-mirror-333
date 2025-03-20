import os
import sys
import warnings
from functools import wraps
from pathlib import Path

import click

from taskblaster import TaskBlasterInterrupt
from taskblaster.listing import TaskListing
from taskblaster.repository import Repository
from taskblaster.state import State

# Translate --color options to click.echo() inputs:
TB_COLOR_MODES = {
    'auto': None,
    'always': True,
    'never': False,
}


class Echo:
    def __init__(self, mode):
        self.mode = mode

    def __call__(self, *args, **kwargs):
        """Echo string in correct color mode."""
        return click.echo(*args, color=self.mode, **kwargs)

    def restyle(self, string):
        """Uncolor or leave the string unchanged depending on mode.

        Functions like click.confirm() do not take a color flag,
        so we need to send strings through this when we want another
        behaviour than click's default behaviour."""
        if self.mode is False:
            string = click.unstyle(string)

        return string

    def are_you_sure(self, prompt):
        # Click confirm() does not support the color option.
        # It will always remove colors if we are not a tty.
        # Of course this is a fringe case since interactive prompts
        # make little sense in the non-tty case.
        if self.mode is not False:
            prompt = click.style(prompt, 'bright_red')
        return click.confirm(prompt)


def colormode(mode):
    if mode is None:
        mode = os.environ.get('TB_COLORS', 'auto')
        if mode not in TB_COLOR_MODES:
            warnings.warn(f'Ignoring bad TB_COLORS mode: {mode}')
            mode = 'auto'

    return Echo(TB_COLOR_MODES[mode])


def echo_mode():
    return click.option(
        '--color',
        'echo',
        metavar='WHEN',
        type=click.Choice([*TB_COLOR_MODES]),
        callback=lambda ctx, param, value: colormode(value),
        help=(
            'Colorize output; use "always" for colors, "never" for no '
            'colors, or "auto" (default).  '
            'Default can be overridden by the TB_COLORS '
            'environment variable.'
        ),
    )


def silent_option():
    return click.option(
        '-s', '--silent', is_flag=True, help='Do not print to screen.'
    )


def dryrun_option():
    return click.option(
        '-z',
        '--dry-run',
        is_flag=True,
        help='Simulate what would happen, but do nothing.',
    )


def max_tasks_option():
    return click.option(
        '--max-tasks',
        type=int,
        metavar='NUM',
        help='Maximum number of tasks for worker to run.',
    )


def wall_time_option():
    return click.option(
        '--wall-time',
        type=str,
        default=None,
        help=(
            'Maximum time for worker to run.  '
            'Worker terminates when walltime is exceeded or '
            'would be exceeded within task-wall-time.  '
            'Default is unlimited time.'
        ),
    )


def force_option(verb):
    return click.option(
        '--force',
        default=False,
        is_flag=True,
        help=f'{verb} tasks without prompting for confirmation.',
    )


def tree_argument():
    return click.argument('tree', nargs=-1)


def format_indexnode_short(indexnode, *, remove_info, reset_info, record_info):
    from taskblaster.util import color

    state = indexnode.state
    return ' '.join(
        [
            color('remove:', fg='bright_red')
            if remove_info
            else ('unrun: ' if not (reset_info or record_info) else 'reset: '),
            color(state.name, state.color).ljust(17),
            color(indexnode.name),
        ]
    )


def _find_repository():
    try:
        return Repository.find(Path.cwd())
    except Repository.RepositoryError as ex:
        raise click.ClickException(f'{ex}')


def hack_pythonpath(repo):
    sys.path.append(str(repo.project_pythonpath))


def with_repo(func=None, *, lock=True):
    from contextlib import ExitStack

    def makewrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            repo = _find_repository()
            hack_pythonpath(repo)
            with ExitStack() as stack:
                if lock:
                    stack.enter_context(repo)
                return func(*args, **kwargs, repo=repo)

        return wrapper

    if func is None:
        return makewrapper
    else:
        return makewrapper(func)


@click.group()
def tb():
    """Taskblaster, a high-throughput workflow utility.

    Utility to define and run vast quantities of computational tasks,
    organizing inputs and outputs in a directory tree.

    Use the init subcommand to initialize an empty repository.  Then
    write a workflow function and run it to create a directory tree of
    tasks.  Then submit tasks using your favourite high-performance
    computing batch system.
    """


@tb.command()
@with_repo
@click.argument('workflow_class', required=False)
@click.option('--output', '-o', is_flag=False, default='workflow.html')
@click.option('--file', '-f', is_flag=False)
@click.option('--style', '-s', is_flag=False)
@click.option('--browser', '-b', is_flag=True)
def view_workflow(repo, output, file, style, browser, workflow_class=None):
    """Write HTML files from a specified workflow class.

    Example usage:
        tb view-workflow package.workflows.TestWorkflow

    In case workflow cannot be imported from a package, user can also specify
    the file that contains the workflow as:

        tb view-workflow -f workflow.py TestWorkflow

    """
    from taskblaster.view_workflow import view_workflow

    if file:
        from importlib.machinery import SourceFileLoader

        module = SourceFileLoader('main', file).load_module()

        """
            If the workflow_class is omitted, either give options
            if there are many, or choose the only one in the file.
        """
        if workflow_class is None:
            workflow_attributes = []
            for item in module.__dict__.values():
                if hasattr(item, '_is_tb_workflow'):
                    if item._is_tb_workflow:
                        workflow_attributes.append(item.__name__)
            if len(workflow_attributes) > 1:
                raise click.ClickException(
                    'WORKFLOWCLASS expected. Options '
                    f'are {workflow_attributes}.'
                )
            workflow_class = workflow_attributes[-1]

        cls = getattr(module, workflow_class)
    else:
        if workflow_class is None:
            raise click.ClickException('WORKFLOWCLASS expected')
        cls = repo.import_task_function(workflow_class)

    if not output.endswith('.html'):
        raise click.ClickException('Output file needs to be an html file.')

    # Write the workflow to the specified html file
    view_workflow(cls, output=output, style=style)

    # User requested to open a browser
    if browser:
        import webbrowser

        webbrowser.open_new(output)


def workflow_cli_options(func):
    decorators = [
        click.argument('script', type=click.Path(exists=True)),
        dryrun_option(),
        silent_option(),
        with_repo,
    ]
    for deco in reversed(decorators):
        func = deco(func)
    return func


@tb.command()
@workflow_cli_options
def workflow(repo, script, dry_run, silent):
    """Run workflow creating folders for tasks inside tree."""
    repo.run_workflow_script(script, dry_run=dry_run, silent=silent)


@tb.command()
@click.argument(
    'pymodule', default='taskblaster.repository', metavar='[MODULE]'
)
@click.argument('directory', default='.')
def init(pymodule, directory):
    """Initialize repository inside directory.

    The optional MODULE argument can be used to specify a plugin.  A
    plugin is a Python module defining a subclass of the taskblaster
    Repository class.  This can be used to provide a custom JSON
    encoder to store objects not known to taskblaster, and to enable
    parallel workers and subworkers using MPI."""
    root = Path(directory).resolve()
    try:
        Repository.create(root, modulename=pymodule)
    except Repository.RepositoryError as ex:
        raise click.ClickException(ex)
    print(f'Created repository using module "{pymodule}" in "{root}".')


@tb.command()
@with_repo
def info(repo):
    """Print information about repository.

    This prints a brief overview of special files and directories
    associated with the current project."""
    info = repo.info()
    print('\n'.join(info))


def choose_states(ctx, param, value: str):
    # (None means any state)
    if value is None:
        return None

    choice = set(value)
    statecodes = State.statecodes()

    bad_states = choice - set(statecodes)

    if bad_states:
        raise click.BadParameter(
            'States must be among {}; got {}'.format(
                statecodes, ''.join(bad_states)
            )
        )

    return {State(value) for value in choice}


def tag_option():
    return click.option(
        '--tags',
        type=str,
        metavar='TAGS',
        help='Select tasks with any of these tags',
    )


def state_option():
    return click.option(
        '--state',
        '-s',
        type=click.UNPROCESSED,
        callback=choose_states,
        help=(
            'Select only tasks with this state.  State be any of: {}.'.format(
                repr(State.statecodes())
            )
        ),
    )


def failure_option():
    return click.option(
        '--failure',
        '-F',
        type=click.UNPROCESSED,
        help='Select only tasks with failure string matching the string',
    )


def columns_option(listing_cls, morehelp=''):
    column_text = ', '.join(
        f'{column.key}: {column.description}'
        for column in listing_cls.all_columns().values()
    )

    default = listing_cls.default_columns
    help_parts = [
        f'Columns to display: {column_text}. Default: {default}. ',
        morehelp,
    ]

    return click.option(
        '--columns', '-c', help=''.join(help_parts), default=default
    )


@tb.command()
@tree_argument()
@click.option(
    '--parents',
    is_flag=True,
    help='List ancestors of selected tasks outside selection.  '
    'Implies topological sort (default: False).',
    default=False,
)
@columns_option(
    TaskListing,
    morehelp=(
        'Frozen tasks are marked by ❄ and conflicts with C in the info string.'
    ),
)
@state_option()
@click.option(
    '--sort',
    type=click.Choice(['name', 'topo']),
    help="Sort tasks alphabetically ('name') or topologically ('topo').",
)
@echo_mode()
@failure_option()
@with_repo
def ls(repo, tree, columns, state, parents, sort, failure, echo):
    """List tasks under directory TREEs.

    Find tasks inside specified TREEs and collect their dependencies
    whether inside TREE or not.  Then perform the specified actions
    on those tasks and their dependencies."""

    if sort is None:
        sort = 'name'

    if not repo.registry.read_only:
        repo.registry.workers.sync(repo, echo)

    for line in repo.tree(tree, states=state, sort=sort, failure=failure).ls(
        parents=parents, columns=columns
    ):
        echo(line)


@tb.command()
@tree_argument()
@with_repo
@echo_mode()
def stat(repo, tree, echo):
    """Print statistics about selected tasks."""

    # If patterns point to directories, we must recurse into
    # those directories, i.e. <pattern>/*.
    #
    # But we can't just append /* because then we don't match the
    # directory itself.
    #
    # We also can't append * because then we match more things
    # than the user wanted.

    # Here we're doing O(N) work which is not necessary
    # when we're only counting.
    repo.registry.workers.sync(repo, echo)
    echo(repo.tree(tree).stat().tostring())


@tb.command()
@tree_argument()
@with_repo
@echo_mode()
def submit(repo, tree, echo):
    """Mark tasks in TREE and dependencies for execution.

    Only affects new tasks.  To submit a failed task,
    unrun it first."""

    columns = 'sirf'

    listing = repo.listing(columns=columns, fromdir=Path.cwd())

    indexnodes = [*repo.tree(tree).submit()]
    for line in listing.to_string([]):
        echo(line)  # Header

    all_tags = set()
    for indexnode in indexnodes:
        nodeinfo = listing.nodeinfo(
            indexnode, TaskListing.select_columns(columns)
        )
        all_tags |= nodeinfo.tags
        echo(nodeinfo.to_string())

    echo()
    echo(f'Submitted {len(indexnodes)} tasks')
    if all_tags:
        echo(f'Tags included: {",".join(all_tags)}')


def setup_kill_signal_handlers():
    import signal

    def raise_signal(sig, frame):
        raise TaskBlasterInterrupt(f'Interrupted by signal {sig}.')

    for sig in [signal.SIGCONT, signal.SIGTERM]:
        signal.signal(sig, raise_signal)


def _split_tags(ctx, params, tags):
    return set(tags.split(',')) if tags else set()


def required_tags_option():
    return click.option(
        '--require',
        type=str,
        metavar='TAGS',
        callback=_split_tags,
        help='Require worker to pick up only tasks with all the TAGS '
        'specified as comma-separated list.',
    )


def supported_tags_option():
    return click.option(
        '--tags',
        metavar='TAGS',
        type=str,
        callback=_split_tags,
        help='Allow worker to pick up tasks with any of TAGS specified as '
        'comma-separated list.',
    )


def worker_class_option():
    return click.option(
        '--worker-class',
        type=str,
        metavar='WORKER',
        help='Worker class for this worker.  The name must exist in the '
        'resource configuration, see tb workers config.',
    )


@tb.command()
@with_repo(lock=False)
@tree_argument()
@click.option(
    '--subworker-count', type=int, help='Number of MPI subworkers in run.'
)
@click.option(
    '--subworker-size',
    type=int,
    help='Number of processes in each MPI subworker.',
)
@click.option(
    '--greedy',
    is_flag=True,
    help='Run also tasks created while running specified selection.',
)
@worker_class_option()
@supported_tags_option()
@required_tags_option()
@max_tasks_option()
@dryrun_option()
@wall_time_option()
@echo_mode()
def run(
    repo,
    tree,
    subworker_count,
    subworker_size,
    max_tasks,
    greedy,
    worker_class,
    tags,
    require,
    dry_run,
    wall_time,
    echo,
):
    """Launch worker to execute tasks.

    The worker runs tasks in TREE and any dependencies with matching
    tags.  TREE defaults to all queued tasks."""
    from taskblaster.repository import T, WorkerSpecification

    rules = WorkerSpecification()

    worker_classes = repo.get_resources()
    if worker_class is not None:
        rules = rules.merge(worker_classes[worker_class])

    if wall_time is not None:
        wall_time = T(wall_time)

    rules = rules.merge(
        WorkerSpecification(
            tags=tags,
            required_tags=require,
            wall_time=wall_time,
            max_tasks=max_tasks,
            subworker_count=subworker_count,
            subworker_size=subworker_size,
        )
    )

    if dry_run:
        with repo:
            repo.tree(tree).dry_run(rules=rules, echo=echo)
        return

    # Should we queue any selected tasks or only the queued subset?
    # Maybe queue them unless given an option.
    #
    # So: We take tree as an input.  If user used glob patterns,
    # the shell will have expanded them already.  Thus,
    # we take some paths as an input.  They may be tasks
    # or they may have subfolders that are tasks.
    #
    # What we need is to select all subfolders.  It would appear that
    # we can use sqlite's glob functionality for this.
    #
    # Then we need to "submit" those, and then launch a worker selecting
    # only those.
    #
    # So actually, if we received 1000 dirs, we can't just hog them
    # right away.  We could submit them immediately, but then the
    # worker just needs to be able to not return anything *except*
    # something matching one of those 1000 dirs.

    # Workers can be killed in exotic ways; keyboardinterrupt,
    # SIGCONT, SIGTERM, SIGKILL, who knows.  We try to catch
    # the signals and finalize/unlock/etc. gracefully.
    setup_kill_signal_handlers()

    # TODO: Replace with MYQUEUE_ID when we have one:
    myqueue_id = os.getenv('SLURM_JOB_ID', 'N/A')
    repo.run_worker(tree, name=myqueue_id, greedy=greedy, rules=rules)


@tb.command()
@tree_argument()
@with_repo
@state_option()
@failure_option()
@force_option(verb='Unrun')
@echo_mode()
def unrun(tree, repo, state, force, failure, echo):
    """Delete output files from TREE and reset task state to new.

    Unrunning a task also unruns its descendants."""
    # Might be wise to concentrate actual outputs inside a subdir
    # and then rmtree that subdir, except we hate using rmtree because
    # it is kind of dangerous.
    if not tree:
        return

    (unrun_cnt, del_cnt), indexnodes, unrun = repo.tree(
        tree, states=state, failure=failure
    ).select_unrun()

    for reset_info, record_info, remove_info, indexnode in indexnodes:
        echo(
            format_indexnode_short(
                indexnode,
                reset_info=reset_info,
                remove_info=remove_info,
                record_info=record_info,
            )
        )

    ntasks = len(indexnodes)
    if not ntasks:
        echo('No tasks selected.')
        return

    prompt = ''
    if unrun_cnt > 0:
        prompt += (
            f'Unrun the above {unrun_cnt} task{"s" if unrun_cnt > 1 else ""}'
        )
    if del_cnt > 0:
        if unrun_cnt > 0:
            prompt += ' and '
        prompt += (
            f'REMOVE the above {del_cnt} task{"s" if del_cnt > 1 else ""}?'
        )

    if force or echo.are_you_sure(prompt):
        unrun()

        prompt = ''
        if unrun_cnt > 0:
            prompt += (
                f'{unrun_cnt} task{"s" if unrun_cnt > 1 else ""} were unrun'
            )
        if del_cnt > 0:
            if unrun_cnt > 0:
                prompt += ' and '
            prompt += (
                f'{del_cnt} task{"s" if del_cnt > 1 else ""} were removed'
            )
        prompt += '.'
        echo(prompt)
    else:
        echo('Never mind.')


@tb.command()
@tree_argument()
@with_repo
@state_option()
def resolve(tree, repo, state):
    """Mark conflicts as resolved in TREE.

    Change the conflict state to "resolved" for selected tasks with
    conflict state "conflict"."""

    if not tree:
        return

    repo.tree(tree, states=state).resolve_conflict()


@tb.command()
@tree_argument()
@with_repo
@state_option()
def unresolve(tree, repo, state):
    """Mark resolved tasks as in conflict.

    Change the conflict state to "conflict" for selected tasks
    with conlict state "resolved"."""
    if not tree:
        return

    repo.tree(tree, states=state).unresolve_conflict()


@tb.command()
def completion():
    """Print bash command-line completion incantation.

    To enable command-line completion, include the
    script the shell rc file, e.g., ~/.bashrc.

    For shells other than bash, see the documentation of click
    for how to set up command-line completion."""
    import subprocess

    progname = Path(sys.argv[0]).name
    name = progname.replace('-', '_').upper()
    command = 'echo "$(_{}_COMPLETE=bash_source {})"'.format(name, progname)

    subprocess.run(command, shell=True, check=True)


@tb.command()
@tree_argument()
@dryrun_option()
@with_repo
@state_option()
@force_option(verb='Remove')
@echo_mode()
def remove(tree, dry_run, repo, state, force, echo):
    """Delete tasks in TREE entirely.  Caution is advised."""

    if not tree:
        return

    indexnodes, delete = repo.tree(tree, states=state).remove()

    msg = 'would delete:' if dry_run else 'deleting:'
    for indexnode in indexnodes:
        echo(f'{msg} {indexnode.name}')

    ntasks = len(indexnodes)
    if not ntasks:
        echo('No tasks selected')
        return

    prompt = (
        f'WARNING: This permanently removes the above task(s).\nAre '
        f'you certain about deleting the above {ntasks} task(s)?'
    )
    if force and not dry_run:
        delete()
    elif not dry_run and echo.are_you_sure(prompt):
        delete()
    elif not dry_run:
        echo('Never mind.')


@tb.command()
@with_repo
@click.option(
    '--action',
    type=str,
    help='Perform specified action for the selected tasks.  '
    'To associate tasks with actions, see the documentation'
    'for the @tb.actions decorator.',
)
@tree_argument()
def view(repo, action, tree):
    """View detailed information or execute task-specific actions."""
    repo.view(tree, action=action)


@tb.command()
@tree_argument()
@with_repo
def graph(repo, tree):
    """Generate dependency graph.

    This computes the dependency graph of the specified tasks and prints
    it in machine-friendly graphviz format for further processing.
    Examples:

      $ tb graph | dot -T svg > graph.svg  # convert to svg using graphviz\n
      $ tb graph | dot -T pdf > graph.pdf\n
      $ tb graph | display  # open window using imagemagick display command\n
    """
    repo.graph(tree)


def conflict_error(err):
    msg = """\
A task already exists in this directory with different inputs.
You may wish to assign a different name for the task in the workflow,
or delete the old task."""

    # We need also some error handling options, e.g., skip conflicts,
    # or always override, or choosing interactively.
    # Even better, we could generate multiple conflicts and list them
    # at the end.
    return click.ClickException(f'{err}\n{msg}')
