import shutil
from pathlib import Path

import click

import taskblaster.cli.main as cli
from taskblaster.cli.main import state_option
from taskblaster.heuristics import repair_registry
from taskblaster.listing import BaseListing, column, format_line_from_columns
from taskblaster.repository import Repository


@click.group()
def special():  # noqa: F811
    """More rare special commands."""


@special.command()
@click.argument('old')
@click.argument('new')
@cli.tree_argument()
@click.option(
    '--force',
    is_flag=True,
    type=str,
    default=False,
    help='Rename targets without prompting for confirmation.',
)
@cli.echo_mode()
@cli.with_repo
def rename_import_path(repo, old, new, tree, force, echo):
    """Rename import path for tasks.

    Replace OLD import paths with NEW ones.  OLD and NEW are function
    import paths as specified to tb.node().  The primary use of this
    command is to keep the repository up to date when a function has
    been moved or renamed during refactoring.

    No attempt is made to ensure that the new and old functions are
    equivalent or to otherwise invalidate tasks, so caution is advised."""

    paths, rename_fcn = repo.rename_import_path(tree, old, new)
    if len(paths) == 0:
        echo('No matches to rename.')
        return
    for path in paths:
        echo(f'Task {path} {old} -> {new}')

    prompt = (
        f'Are you sure you want to rename following {len(paths)} '
        'task import paths?'
    )
    if force:
        rename_fcn()
    elif echo.are_you_sure(prompt):
        rename_fcn()
    else:
        echo('Never mind.')


@special.command()
@cli.with_repo
@cli.echo_mode()
def make_directories(repo, echo):
    """Create all directories which exists currently in the registry"""
    tree = repo.tree()
    folders = []
    for indexnode in tree.nodes():
        path = repo.tree_path / indexnode.name
        folders.append(path)
        echo(f'path: {path}')

    if echo.are_you_sure(
        f'Create {len(folders)} director'
        + ('ies' if len(folders) > 1 else 'y')
    ):
        for folder in folders:
            folder.mkdir(exist_ok=True, parents=True)
    else:
        echo('Never mind.')


@special.command()
@click.argument('newrepopath')
@cli.tree_argument()
@cli.echo_mode()
@state_option()
@click.option(
    '--tags',
    type=str,
    metavar='TAGS',
    help='Only clone tasks (and their ancestors) if it has one of these flags',
)
@cli.with_repo
def clone_sub_tree(repo, newrepopath, tree, echo, tags, state):
    """Clone TREE as new repository.

    Tasks in TREE and their ancestors are collected and copied as a
    new standalone repository.

    Usage example::
    tb special clone-sub-tree PATH_TO_NEW_REPO tree/subtree --tags=mytag

    This would clone all tasks in tree/subtree with tag mytag to new repo.
    Note that the path to the new repo cannot be inside the current repo.
    """
    newrepopath = Path(newrepopath).resolve()

    if newrepopath.is_relative_to(repo.root):
        raise click.ClickException(
            'Target repository cannot be inside the'
            'current repository (note that the'
            'target is the first argument,'
            ' followed by TREE argument.'
        )

    # Make sure the repository does not exist
    try:
        Repository.find(newrepopath)
    except Repository.RepositoryError as ex:
        echo(ex)
    else:
        raise click.ClickException(
            f'Target repository exists at {newrepopath}.'
        )

    pymodulefile = repo.root / repo._magic_dirname / repo._py_filename
    pymodulename = pymodulefile.read_text().strip()
    echo(f'module {pymodulename}')

    try:
        newrepo = Repository.create(newrepopath, modulename=pymodulename)
    except Repository.RepositoryError as ex:
        raise click.ClickException(ex)

    echo(f'Cloning {tree} to {newrepopath}')

    if tags is None:
        tags = set()
    else:
        tags = set(tags.split(','))
        echo(
            'Cloning only nodes (and their ancestors)'
            f'which have at least one of {tags}.'
        )

    tree = repo.tree(tree, tags=tags, states=state)
    new_registry = newrepo.registry

    with newrepo:
        for indexnode in tree.nodes_topological():
            encoded_task = repo.cache.encoded_task(indexnode.name)
            new_registry._add(encoded_task, force_state=indexnode.state)

            old_path = repo.tree_path / indexnode.name
            if old_path.exists():
                shutil.copytree(old_path, newrepo.tree_path / indexnode.name)


@special.command()
@cli.echo_mode()
def heuristics(echo):
    """Perform heuristics to registry to find out possible inconsistencies.

    Currently peforms following check:
       * Ensures that topological_depth table meets all FOREIGN_KEY conditions
         to registry table. This is for older taskblaster versions, before
         the FOREIGN_KEY constraint was introduced.
    """
    echo('Running heuristics')

    repair_registry(echo, dry_run=True)


@special.command()
@click.option(
    '--force',
    is_flag=True,
    type=str,
    default=False,
    help='Repair registry without prompting for confirmation.',
)
@cli.echo_mode()
def repair(echo, force):
    """Repairs the registry from (relatively) safe errors.

    There errors include things, such as foreign key mismatches of
    auxilliary tables (used only for speed and listings).

    To see full list of repairs, see::

        tb special heuristics --help
    """

    echo('Repairing database.')
    repair_registry(echo, dry_run=False, force=force)


@special.command()
@cli.with_repo
@cli.echo_mode()
def task_name_hash(repo, echo):
    echo(repo.registry.index.task_name_hash())


def _freezelike_command(command, mode, help):
    @special.command(name=command, help=help)
    @cli.tree_argument()
    @cli.with_repo
    @cli.echo_mode()
    def func(repo, tree, echo):
        if not tree:
            return

        registry = repo.registry
        for indexnode in repo.tree(tree).nodes():
            name = indexnode.name
            echo(f'{command} {name}')
            if mode == 'freeze':
                registry.freeze(name, why='manual')
            elif mode == 'unfreeze':
                registry.unfreeze(name, why='manual')
            else:
                raise ValueError(mode)

    return func


freeze = _freezelike_command(
    'freeze',
    'freeze',
    help='Freeze tasks in TREE.  The freeze recursively affects all task '
    'descendants.',
)
unfreeze = _freezelike_command(
    'unfreeze',
    'unfreeze',
    help='Unfreeze tasks in TREE.  This affects only tasks that were '
    'frozen due to the corresponding tb freeze command.  To unfreeze tasks '
    'that are frozen due to a conflict, resolve the conflict.',
)


@special.command()
@cli.with_repo(lock=False)
# @click.option(
#    '-N', '--max-tasks', type=int,
#    help='Maximum number of tasks to create.')
@cli.echo_mode()
@cli.tree_argument()
def workflow(repo, tree, echo):
    """Run whole workflow or parts of it.

    Without TREE, run master workflow.

    With TREE, rerun the source workflow of every task in TREE."""

    # We should somehow namespace the master workflow so user can
    # add experimental stuff without interfering with production stuff.

    # We could allow an "add" command so there can be different workflow files,
    # or we can allow tb_main() to yield multiple things.

    # Actions:
    #
    # 1) Check selected workflows for up-to-date-ness (dry-run)
    # 2) Check & update selection
    # 3) "Non-destructive" update (e.g. only add new)
    # 4) Clean orphans?
    #
    # Specifications:
    #
    # 1) Everything
    # 2) Specific workflows only
    # 3) Glob
    #
    # Recursion modes:
    #
    # 1) Tree (subdirectory)
    # 2) Ancestors
    # 3) Descendants

    if tree:
        with repo:
            _workflow_tree(repo, repo.tree(tree), echo)
    else:
        _workflow_main(repo)  # use echo


def _workflow_tree(repo, tree, echo):
    registry = repo.registry

    # What if the selection would include a workflow that did not generate
    # any tasks?  I think taskless workflows are not currently possible
    # but a user could conceivably add an empty workflow first and add
    # tasks to it later.

    # First get the workflows of all selected tasks:
    workflownames = {
        registry.sources[indexnode.name] for indexnode in tree.nodes()
    }
    workflows = {name: registry.workflows[name] for name in workflownames}

    print(workflows)

    graph = {}
    for name, workflow in workflows.items():
        graph[name] = set()
        # We are only going to loop through those sources that are
        # part of the selection.
        if workflow.source in workflownames:
            graph[name].add(workflow.source)

    # Root workflow is its own source, eliminate cycle:
    if '' in graph:
        graph[''].remove('')

    print('GRAPH')
    print(graph)

    # There's the question of whether a specified workflow should be
    # validated wrt. its source, or whether we should only validate "down".
    # We should probably validate a workflow wrt. its source, generally.
    # We don't do that right now.

    from taskblaster import TB_STRICT

    assert TB_STRICT

    import graphlib

    sorter = graphlib.TopologicalSorter(graph)
    for workflow_name in sorter.static_order():
        workflow = workflows[workflow_name]
        workflow_obj, refs = repo.cache.json_protocol.decode_workflow(workflow)

        # We need to recreate implicit dependencies when loading back,
        # otherwise this update will delete them.

        # Apparently implicit dependency is inherited through any number
        # of subworkflow layers.  We should probably avoid that.
        # Maybe we should first update how we handle implicit dependencies
        # before this work can continue.

        rn = repo.runner().with_subdirectory(workflow_name)
        # This may recurse very deep, so we should somehow skip repeats.
        rn.run_workflow(
            workflow_obj,
            add_workflows_to_registry=True,
            source=workflow.source,
        )
        print(workflow_obj)
        print('REFS')
        print(refs)
        # workflow_data = self.registry.workflows{workflow_name]
        # print(workflow_name)
        # Here we effetively have name == directory which may require
        # an additional special case for e.g. totree.

    # for indexnode in tree.nodes():
    #    workflowname = repo.registry.sources[indexnode.name]
    #    if workflowname in seen:
    #        continue
    #    workflowdata = repo.registry.workflows[workflowname]
    #    workflows_seen[workflowname] = workflowdata

    # For each "seen" workflow, we need to rerun that workflow.
    # But if we also saw its source workflow, then we need to rerun
    # the source workflow which could change the outcome.


@special.command()
@cli.workflow_cli_options
def run_workflow_clobber_implicit(repo, script, dry_run, silent):
    """Run workflow and overwrite implicit dependencies willy-nilly.

    This command resolves a conflict by overwriting the original input
    with the new (conflicting) input for any selected tasks with conflicts.

    Please be careful: Abusing this command can make results
    non-reproducible.  It should be used to resolve conflicts arising
    from internal format changes, or fixes where an input must be
    changed although the resulting computation is the same.

    This command only affects selected tasks that have unresolved conflicts.
    """

    repo.run_workflow_script(
        script,
        dry_run=dry_run,
        silent=silent,
        clobber_implicit_deps=True,
    )


def _workflow_main(repo):
    try:
        import main
    except ImportError:
        raise click.ClickException(
            'No master workflow file <project root>/src/main.py'
        )

    try:
        tb_main = main.tb_main
    except AttributeError:
        raise click.ClickException(
            '<project root>/src/main.py dose not define tb_main().'
        )

    workflow = tb_main()
    rn = repo.runner()

    with repo:
        # For now we drop all workflows.
        # To solve this we'd need more intelligent "remove"
        repo.registry.workflows.clear()

        # Currently source='' means the root workflow.  Maybe clearer to use
        # another magic string.
        rn.run_workflow(workflow, add_workflows_to_registry=True, source='')


class WorkflowListing(BaseListing):
    default_columns = 'ni'

    def __init__(self, workflowdata):
        self.workflowdata = workflowdata

    @column('n', 24)
    def name(self):
        # Format as directory
        name = self.workflowdata.name
        if name == '':
            name = '<root>'
        return name

    @column('i', 24)
    def importpath(self):
        return self.workflowdata.importpath

    @column('I', 30)
    def serialized_input(self):
        # We could/should also have a column for the decoded workflow
        return self.workflowdata.serialized_input

    @column('S', 16)
    def source(self):
        return self.workflowdata.source


@special.command()
@cli.with_repo
@cli.echo_mode()
@cli.columns_option(WorkflowListing)
# @tree_argument()
def lsw(repo, columns, echo):
    workflows = [*repo.registry.workflows.values()]
    actual_columns = WorkflowListing.select_columns(columns)

    for line in WorkflowListing.header(actual_columns):
        echo(line)

    for workflow in workflows:
        listing = WorkflowListing(workflow)
        line = format_line_from_columns(listing, actual_columns)
        echo(line)
