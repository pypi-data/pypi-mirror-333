def define_subgroups():
    from taskblaster.cli.main import tb
    from taskblaster.cli.registry import registry
    from taskblaster.cli.special import special
    from taskblaster.cli.tags import tag
    from taskblaster.cli.warden import warden
    from taskblaster.cli.workers import workers

    tb.add_command(registry)
    tb.add_command(workers)
    tb.add_command(tag)
    tb.add_command(special)
    tb.add_command(warden)
    return tb


tb = define_subgroups()


cli = tb  # Old alias referenced by pip installations


if __name__ == '__main__':
    tb.main()
