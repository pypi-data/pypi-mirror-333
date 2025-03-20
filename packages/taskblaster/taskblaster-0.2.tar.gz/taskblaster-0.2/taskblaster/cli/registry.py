import click

from taskblaster.cli.main import echo_mode, with_repo
from taskblaster.state import State


@click.group()
def registry():  # noqa: F811
    """View or manipulate registry."""


@registry.command()
@with_repo
def build(repo):
    """Add all tasks in the tree to the registry."""
    import graphlib

    from taskblaster.entry import Entry

    registry = repo.cache.registry

    encoded_tasks = {}
    graph = {}

    import json

    for inputfile in repo.root.glob('tree/**/input.json'):
        print('Reading:', inputfile)
        entry = Entry(inputfile.parent, repo.cache.json_protocol)
        name = str(inputfile.parent.relative_to(repo.tree_path))
        try:
            # The source is not (yet) stored redundantly so we would need
            # to set one and then update it by reapplying workflow,
            # unless we actually store it.
            #
            # has_record will be False which we don't know, but could be
            # updated once the workflow reruns.
            #
            # Alternatively, we could infer it from the existence of a record
            # next to this task.
            #
            # Also, tags will need to be re-applied from the workflow.

            try:
                serialized_handlers = entry.handlersfile.read_text()
            except FileNotFoundError:
                serialized_handlers = '[]'

            encoded_task = repo.cache.json_protocol.load_encoded_task(
                serialized_input=entry.inputfile.read_text(),
                serialized_handler=serialized_handlers,
                name=name,
                source='UNKNOWN_SOURCE',
                has_record=False,
                tags=set(),
            )
        except json.decoder.JSONDecodeError:
            print('Skipping due to JSONDecodeError.')
            continue
        assert encoded_task.name == name

        encoded_tasks[name] = encoded_task
        graph[name] = set(encoded_task._parents)

    # Make sure all parents are there.
    # Delete orphan subtrees.
    while True:
        missing = []
        for name, parents in graph.items():
            for parent in parents:
                if parent not in graph:
                    missing.append(name)
                    missing.append(parent)

        missing = set(missing)
        if not missing:
            break

        for miss in missing:
            print('Removing orphan task', miss)
            if miss in graph:
                del graph[miss]

    sorter = graphlib.TopologicalSorter(graph)

    for name in sorter.static_order():
        encoded_task = encoded_tasks[name]
        action, indexnode = registry.add_or_update(encoded_task=encoded_task)

        if repo.cache.entry(name).has_output():
            state = State.done
        else:
            state = State.new

        registry._update_state(name, state)
        print(action, indexnode.name, indexnode.state)


@registry.command()
@with_repo
def ancestors(repo):
    print(repo.cache.registry.ancestry.graph())


@registry.command()
@with_repo
def ls(repo):
    registry = repo.cache.registry
    for indexnode in registry.index.nodes():
        print(indexnode)


@registry.command()
@with_repo
@echo_mode()
@click.option(
    '--unapply',
    is_flag=True,
    help='Reverse operation: Remove inputs from registry (mostly for testing).'
    '  Does not prompt for confirmation.',
)
def patch_serialized_inputs(repo, echo, unapply):
    """Patch all tasks so inputs are stored in the registry.

    The purpose of this command is to migrate repositories where input
    lives only inside input.json such that the input will be inside
    the registry.  input.json will not be deleted.  The operation
    prompts for confirmation.

    This does not affect tasks that already have inputs stored in registry.
    """

    cache = repo.cache
    registry = cache.registry

    if unapply:
        to_be_patched = [*registry.inputs]

        for name in to_be_patched:
            echo(name)

        def patch_indexnodes():
            for name in to_be_patched:
                del registry.inputs[name]

    else:
        to_be_patched = []

        for indexnode in registry.index.nodes():
            try:
                registry.inputs[indexnode.name]
            except KeyError:
                echo(indexnode.name)
                actual_input = cache.entry(
                    indexnode.name
                ).inputfile.read_text()
                to_be_patched.append((indexnode, actual_input))

        def patch_indexnodes():
            for indexnode, actual_input in to_be_patched:
                echo(f'Patching {indexnode.name}')
                cache.registry.inputs[indexnode.name] = actual_input

    if not to_be_patched:
        echo('Nothing to do.')
        return

    action = 'Unmigrate' if unapply else 'Migrate'
    prompt = f'{action} the above {len(to_be_patched)} tasks?'

    if echo.are_you_sure(prompt):
        patch_indexnodes()
    else:
        echo('Never mind.')
