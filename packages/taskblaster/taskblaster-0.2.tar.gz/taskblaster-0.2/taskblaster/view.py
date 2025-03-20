from taskblaster.state import State


def printlines_indented(string, *, indent):
    for line in string.split('\n'):
        spaces = ' ' * indent
        print(f'{spaces}{line}')


def view_node(repo, indexnode):
    cache = repo.cache
    name = indexnode.name
    entry = cache.entry(name)
    encoded_task = cache.encoded_task(name)

    node = cache.json_protocol.deserialize_node(
        encoded_task.serialized_input, name
    )
    depth = cache.registry.topological_depth[name]
    try:
        source = cache.registry.sources[name]
    except KeyError:
        source = '<missing, we will need to migrate>'
    if source == '':
        source = '<root workflow>'

    state = State(indexnode.state)

    print(f'name: {name}')
    print(f'  location:        {entry.directory}')
    print(f'  state:           {state.name}')
    print(f'  target:          {node.target}(…)')
    print(f'  wait for:        {indexnode.awaitcount} dependencies')
    print(f'  depth:           {depth}')
    print(f'  source workflow: {source}')

    frozen_why = cache.registry.frozentasks.get_tags(name)
    if frozen_why:
        reasons = ' '.join(sorted(frozen_why))
    else:
        reasons = '(not frozen)'
    print(f'  frozen by: {reasons}')
    print()

    print_handled_inputs(entry)
    print_handler_info(encoded_task, entry, cache.json_protocol)
    print_parents(encoded_task.parents)
    print_input(encoded_task.serialized_input)

    if state == State.done:
        output = entry.output()
    else:
        output = None

    print_output(state, output)
    print_runinfo(cache.registry.workers.get_runinfo(name))

    if node.target != 'fixedpoint':
        try:
            targetfunc = repo.import_task_function(node.target)
        except ModuleNotFoundError as err:
            print(f'Cannot import {node.target}: {err}')
        else:
            print_custom_actions(targetfunc, output)


def print_parents(parents):
    print('  parents:')
    if parents:
        for parent in parents:
            print(f'    {parent}')
    else:
        print('    <task has no dependencies>')
    print()


def print_input(serialized_input):
    print('  input:')
    printlines_indented(serialized_input, indent=4)
    print()


def print_handled_inputs(entry):
    print('  latest handled inputs:')
    print('    ', entry.updated_serialized_inputs)
    print()


def print_handler_info(encoded_task, entry, codec):
    print('  handlers:')
    if entry.handlersfile.exists():
        printlines_indented(encoded_task.serialized_handlers, indent=4)
    else:
        print('     <None>')
    if entry.handlersdatafile.exists():
        handler_data = codec.loads_task_buf(
            entry.handlersdatafile.read_text(), encoded_task.name
        )
        printlines_indented(f'attempts: {handler_data.count}', indent=4)
        print()
        printlines_indented(
            f'handler data: {handler_data.__class__.__name__}', indent=2
        )
        for idx, data in enumerate(handler_data.updated_params):
            printlines_indented(f'updates {idx}: {data}', indent=4)
    else:
        print()
        printlines_indented('handler data:', indent=2)
        printlines_indented('<None>', indent=4)
    print()


def print_output(state, output):
    print('  output:')
    if state == State.done:
        outputstring = repr(output)
        printlines_indented(outputstring, indent=4)
    else:
        print('    <task not finished yet>')
    print()


def print_custom_actions(function, output):
    from taskblaster.util import get_task_actions

    actions = get_task_actions(function, output)
    if actions:
        print('  actions:')
        for action, function in actions.items():
            origin = f'{function.__name__}() from [{function.__module__}]'
            print(f'    {action}: {origin}')
            if function.__doc__ is not None:
                line = function.__doc__.strip().split('\n')[0]
                print(f'      {line}')
    else:
        print('No custom actions defined for this task.')
    print()


def print_runinfo(runinfo):
    if runinfo is None:
        print('Task has no run information')
        return

    print('Run information:')
    print(f'    Worker name: {runinfo.subworkerid}')
    print(f'    Start time: {runinfo.start_time}')
    print(f'    End time: {runinfo.end_time}')
    print(f'    Duration: {runinfo.duration}')
    print(f'    Error: {runinfo.exception}')
    print()
