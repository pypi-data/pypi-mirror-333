class MissingMyqueue(Exception):
    pass


def myqueue(dry_run=False):
    try:
        import myqueue  # noqa: F401
    except ModuleNotFoundError:
        raise MissingMyqueue()

    from myqueue.config import Configuration
    from myqueue.queue import Queue

    # XXX depends on pwd does it not?  Should probably depend on workflow
    # location.
    try:
        config = Configuration.read()
    except ValueError:
        raise MissingMyqueue()

    return Queue(config=config, dry_run=dry_run)


def submit_manytasks(tasks, dry_run, max_mq_tasks=None):
    from myqueue.submitting import submit

    with myqueue(dry_run=dry_run) as queue:
        submit(queue, tasks, max_tasks=max_mq_tasks)


def mq_walltime(resources) -> int:
    from myqueue.resources import Resources

    # Would be best not to do this, but we cannot
    # generally parse myqueue resource strings.
    # We could also avoid it and instead build the
    # myqueue resource string from our own walltime etc.
    return Resources.from_string(resources).tmax


def mq_worker_task(directory, rules):
    from myqueue.task import create_task

    args = ['run']

    if rules.max_tasks is not None:
        args.append(f'--max-tasks={rules.max_tasks:d}')
    if rules.subworker_size is not None:
        args.append(f'--subworker-size={rules.subworker_size:d}')
    if rules.subworker_count is not None:
        args.append(f'--subworker-count={rules.subworker_count:d}')

    # If we have no walltime, set walltime a little bit lower than
    # whatever time myqueue says the job will have.
    wall_time = rules.wall_time
    if wall_time is None and rules.resources is not None:
        wall_time = int(0.85 * mq_walltime(rules.resources))

    if wall_time is not None:
        args.append(f'--wall-time={wall_time}s')

    # XXX We should avoid passing a worker name, or at least
    # avoid that the worker loads all the worker info when it
    # starts running.
    if rules.name:
        args.append(f'--worker-class={rules.name}')

    if rules.tags:
        txt = ','.join(rules.tags)
        args.append(f'--tags={txt}')

    if rules.required_tags:
        txt = ','.join(rules.required_tags)
        args.append(f'--require={txt}')

    return create_task(
        cmd='taskblaster',
        name='worker',
        args=args,
        deps=[],
        resources=rules.resources,
        folder=directory,
    )
