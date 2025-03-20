import taskblaster as tb


def test_simple_branching(tool):
    def test_basics():
        main_wf(6)
        tool.count(new=4)
        tool.run()
        tool.count(done=4, new=0)
        main_wf(6)
        tool.count(done=4, new=3)
        tool.run()
        tool.count(done=7)

    def main_wf(n=6):
        from taskblaster.testing import RelaxWorkflow

        def make_workflow(inputs, msg='input msg'):
            def workflow(rn):
                for name, atoms in inputs:
                    rn2 = rn.with_subdirectory(name)
                    wf = RelaxWorkflow(atoms=(atoms, msg))
                    rn2.run_workflow(wf)

            return workflow

        inputs = [('mag_example', n), ('nonmag_example', 1)]
        tool.workflow_function(make_workflow(inputs))

    test_basics()
    tool.unrun()
    # Now everything should work as the first time
    test_basics()

    # test unrun
    tool.unrun('tree/nonmag_example/check_magnetic_state')
    tool.count(done=4, new=1)
    tool.run()
    tool.count(done=5)
    main_wf(6)
    tool.count(done=5, new=2)
    tool.run()
    tool.count(done=7)

    # test conflict
    main_wf(8)
    tool.check_conflict(conflicts=1, resolved=0)
    tool.resolve_conflict()
    tool.check_conflict(0, 1)
    tool.unrun('tree/mag_example/relax')
    tool.check_conflict(0, 0)
    tool.count(done=4, new=2)
    tool.run()
    tool.count(done=6)

    main_wf(8)
    tool.count(done=6, new=1)

    tool.run()
    tool.count(done=6, new=1)  # Cannot run because of conflict
    tool.resolve_conflict()
    tool.run()
    tool.count(done=7)


def test_loop(tool):
    from taskblaster.testing import RelaxWorkflowLoop

    def run_wf(n=3):
        tool.workflow(RelaxWorkflowLoop(atoms=(n, 'test3')))

    # Test a simple loop
    run_wf()
    tool.count(new=3)
    nn = 2
    # Do tb run, tb workflow until no more tasks are generated.
    # I suppose this should be done automatically in the future
    for i in range(3):
        tool.run()
        tool.count(done=3 + 2 * i)
        run_wf()
        if i == 2:
            nn = 1
        tool.count(done=3 + 2 * i, new=nn)
    tool.run()
    tool.count(done=8)

    # Test conflict
    run_wf(n=2)
    tool.check_conflict(1, 0)
    tool.count(done=8)
    tool.unrun('tree/prepare_atoms')

    # Now tasks that were genersated in the loop should have been removed
    # and we should be back at the beginning
    run_wf(n=2)
    tool.count(new=3)

    # Now loop converged after two steps
    tool.run()
    tool.count(done=3)
    run_wf(n=2)
    tool.count(done=3, new=2)
    tool.run()
    tool.count(done=5)
    run_wf(n=2)
    tool.count(done=5, new=1)
    tool.run()
    tool.count(done=6)


def test_combined(tool):
    """Simple test of combined wf. Should test to unrun etc once
    simple loop passes
    """
    from taskblaster.testing import CombinedWorkflow

    def main_wf():
        tool.workflow(CombinedWorkflow(atoms=(6, 'nonmag_example')))

    main_wf()
    tool.count(new=5)
    tool.run(greedy=True)

    # run tb workflow and tb run until all tasks have been generated
    for i in range(5):
        # Check so that tasks are done
        tool.count(done=3 + 2 * i, new=2)

        # Upon running tb workflow again new tasks are generated
        main_wf()
        tool.count(done=3 + 2 * i, new=4)
        tool.run(greedy=True)

    # Check so that tasks are done
    tool.count(done=13, new=2)
    # generate new tasks
    main_wf()
    tool.count(done=13, new=2)

    tool.run(greedy=True)
    tool.count(done=15)


@tb.workflow
class CancelWorkflow:
    obj = tb.var(default='test_cancel')

    @tb.task
    def fail(self):
        return tb.node('taskblaster.testing.fail', msg=self.obj)

    @tb.task
    def passed(self):
        return tb.node('taskblaster.testing.ok', msg=self.obj)

    @tb.subworkflow
    def sw1(self):
        return SubWorkflow(inp=self.fail, inp2=self.passed)


def is_true(inp):
    return True


@tb.workflow
class SubWorkflow:
    inp = tb.var()
    inp2 = tb.var()

    @tb.branch('entry')
    @tb._if(true='b1', false='b2')
    @tb.task
    def is_true(self):
        return tb.node(is_true, inp=self.inp2)

    @tb.branch('b1')
    @tb.jump('external')
    @tb.task
    def one(self):
        return tb.node('taskblaster.testing.ok', msg=self.inp)

    @tb.branch('b2')
    @tb.jump('external')
    @tb.task
    def two(self):
        return tb.node('taskblaster.testing.ok', msg=self.inp)

    @tb.fixedpoint
    @tb.branch('external')
    @tb.task
    def results(self):
        return tb.node(
            'taskblaster.testing.ok', msg=self.Phi(b1=self.one, b2=self.two)
        )


def test_cancel_dynamic(tool):
    tool.workflow(CancelWorkflow())
    tool.run(greedy=True)
    tool.workflow(CancelWorkflow())
    tool.run(greedy=True)
    tool.count(done=2, fail=1, cancel=2)
