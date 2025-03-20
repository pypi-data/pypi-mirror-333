import taskblaster as tb


# utilities
def prepare_branching_wf(tool, msg='hi'):
    def run_wf():
        tool.workflow(GeneratedBranchedWorkflow(msg=msg))

    run_wf()
    tool.run()
    # XXX re-apply the workflow to update the tasks and dependencies
    run_wf()
    tool.run()


def detailed_unrun(tool, unrun_target, states: str, state_values: list):
    before = tool.task_hash()
    changes = tool.unrun(unrun_target)
    assert [changes[s] for s in states] == state_values
    tool.run()
    assert before == tool.task_hash()


# workflows to test features


@tb.workflow
class BranchingAndRecord:
    msg = tb.var(default='hi')

    @staticmethod
    def is_true():
        return True

    @staticmethod
    def a(msg):
        return msg

    @tb.task
    def ok(self):
        return tb.node(BranchingAndRecord.a, msg=self.msg)

    @tb._if(true='newbranch')
    @tb.task
    def if_task(self):
        return tb.node(BranchingAndRecord.is_true)

    @tb.branch('newbranch')
    @tb.task(has_record=True)
    def task_with_record(self):
        return tb.node(BranchingAndRecord.a, msg=self.ok)

    @tb.branch('newbranch')
    @tb.task
    def task_without_record(self):
        return tb.node(BranchingAndRecord.a, msg=self.ok)


@tb.workflow
class GeneratedBranchedWorkflow:
    msg = tb.var(default='hi')

    @staticmethod
    @tb.dynamical_workflow_generator_task
    def generate_branched(inputs, msg):
        for i, inp in enumerate(inputs):
            wf = BranchingAndRecord(msg=msg)
            name = str(i)
            yield name, wf

    @tb.dynamical_workflow_generator(
        {'all_records': '*/*.record', 'all_results': '**'}
    )
    def generate_wfs_from_list(self):
        return tb.node(
            GeneratedBranchedWorkflow.generate_branched,
            inputs=['test'],
            msg=self.msg,
        )


@tb.workflow
class CanDependOnFailedPrequel:
    @staticmethod
    def a(name: str):
        return f'My cat rules. {name}.'

    @staticmethod
    def b(name: str):
        raise ValueError(name)

    @staticmethod
    def c(record1=None, record2=None, *, expected_states):
        record1.inputs

        records = {'record1': record1, 'record2': record2}
        if record1.state == 'd':
            records['record1'] = record1.output
        assert record1.state == expected_states[0]

        if record2.state == 'd':
            records['record2'] = record1.output
        assert record2.state == expected_states[1]

        return records

    @tb.task
    def first_dependency(self):
        return tb.node(
            CanDependOnFailed.a,
            name='I am the first task dependency',
        )

    @tb.task
    def pass1(self):
        return tb.node(CanDependOnFailed.a, name=self.first_dependency)

    @tb.task
    def fail1(self):
        return tb.node(CanDependOnFailed.b, name=self.first_dependency)

    @tb.task
    def depends_on_one_failed(self):
        return tb.node(
            CanDependOnFailed.c,
            record1=self.pass1,
            record2=self.fail1,
            expected_states=['d', 'F'],
        )


@tb.workflow
class CanDependOnFailed:
    @staticmethod
    def a(name: str):
        return f'My cat rules. {name}.'

    @staticmethod
    def b(name: str):
        raise ValueError(name)

    @staticmethod
    def c(record1=None, record2=None, *, expected_states):
        record1.inputs

        records = {'record1': record1, 'record2': record2}
        if record1.state == 'd':
            records['record1'] = record1.output
        assert record1.state == expected_states[0]

        if record2.state == 'd':
            records['record2'] = record1.output
        assert record2.state == expected_states[1]

        return records

    @tb.task
    def first_dependency(self):
        return tb.node(
            CanDependOnFailed.a,
            name='I am the first task dependency',
        )

    @tb.task(has_record=True)
    def pass1(self):
        return tb.node(
            CanDependOnFailed.a,
            name=self.first_dependency,
        )

    @tb.task(has_record=True)
    def pass2(self):
        return tb.node(
            CanDependOnFailed.a,
            name='PASS2 AGAIN',
        )

    @tb.task(has_record=True)
    def fail1(self):
        return tb.node(
            CanDependOnFailed.b,
            name=self.first_dependency,
        )

    @tb.task(has_record=True)
    def fail2(self):
        return tb.node(
            CanDependOnFailed.b,
            name='FAIL2 AGAIN',
        )

    @tb.task
    def depends_on_one_failed(self):
        return tb.node(
            CanDependOnFailed.c,
            record1=tb.record(self.pass1),
            record2=tb.record(self.fail1),
            expected_states=['d', 'F'],
        )

    @tb.task
    def depends_on_both_failed(self):
        return tb.node(
            CanDependOnFailed.c,
            record1=tb.record(self.fail1),
            record2=tb.record(self.fail2),
            expected_states=['F', 'F'],
        )

    @tb.task
    def depends_on_both_pass(self):
        return tb.node(
            CanDependOnFailed.c,
            record1=tb.record(self.pass1),
            record2=tb.record(self.pass2),
            expected_states=['d', 'd'],
        )

    @tb.task
    def dependancy_failed(self):
        return tb.node(
            CanDependOnFailed.a,
            name=self.depends_on_one_failed['record1'],
        )


@tb.workflow
class GeneratedWorkflow:
    @staticmethod
    @tb.dynamical_workflow_generator_task
    def generate_can_fail(inputs):
        for i, inp in enumerate(inputs):
            wf = CanDependOnFailed()
            name = str(i)
            yield name, wf

    @tb.dynamical_workflow_generator({'all_records': '*/*.record'})
    def generate_wfs_from_list(self):
        return tb.node(GeneratedWorkflow.generate_can_fail, inputs=['test'])


@tb.workflow
class SimpleWFNoRecord:
    @staticmethod
    def ok(msg):
        return msg

    @tb.task
    def task1(self):
        return tb.node(SimpleWFNoRecord.ok, msg='hi')


@tb.workflow
class SimpleWFWithRecord:
    @tb.task(has_record=True)
    def task1(self):
        return tb.node(SimpleWFNoRecord.ok, msg='hi')


def test_update_record(tool):
    """
    Changing a task from a normal task to a task with record
    should not change the state of the task. I.e. if the task
    was done adding a record should just add a new task task.record
    but the state of the task should still be done
    """

    # First run a wf with a single task which does not have a record
    tool.workflow(SimpleWFNoRecord())
    tool.run()
    # make sure the task passed
    tool.count(done=1, fail=0)

    # Now add a record to the task
    tool.workflow(SimpleWFWithRecord())

    # The actual task should still be done, but it should now have
    # a record
    tool.count(done=1, fail=0, new=1)

    # running again should mark the record as done
    tool.run()
    tool.count(done=2, fail=0)


# tests for workflows
def test_dependsonfailed(tool):
    tool.workflow(CanDependOnFailed())

    tool.run()
    tool.count(done=11, fail=2)

    # assert nothing has changed when trying to unrun a record
    changes = tool.unrun('tree/fail2.record')
    assert not all(changes.values())
    detailed_unrun(tool, 'tree/pass1', 'nd', [5, -5])
    detailed_unrun(tool, 'tree/fail1', 'ndF', [5, -4, -1])
    detailed_unrun(tool, 'tree/first_dependency', 'ndF', [9, -8, -1])
    detailed_unrun(tool, 'tree/fail2', 'ndF', [3, -2, -1])
    detailed_unrun(tool, 'tree/depends_on_one_failed', 'nd', [2, -2])


def test_dependsonfailed_afterthefact(tool):
    tool.workflow(CanDependOnFailedPrequel())

    tool.run()
    tool.count(done=2, cancel=1, fail=1)

    tool.unrun('tree/depends_on_one_failed')
    tool.count(new=1, done=2, cancel=0, fail=1)

    tool.workflow(CanDependOnFailed())
    tool.count(new=10, done=2, cancel=0, fail=1)

    tool.run()
    tool.count(done=11, fail=2)

    # assert nothing has changed when trying to unrun a record
    changes = tool.unrun('tree/fail2.record')
    assert not all(changes.values())
    detailed_unrun(tool, 'tree/pass1', 'nd', [5, -5])
    detailed_unrun(tool, 'tree/fail1', 'ndF', [5, -4, -1])
    detailed_unrun(tool, 'tree/first_dependency', 'ndF', [9, -8, -1])
    detailed_unrun(tool, 'tree/fail2', 'ndF', [3, -2, -1])
    detailed_unrun(tool, 'tree/depends_on_one_failed', 'nd', [2, -2])
    changes = tool.remove('tree/fail1')
    assert [changes[s] for s in 'dF'] == [-4, -1]


def test_wf_gen_with_failed(tool):
    tool.workflow(GeneratedWorkflow())
    tool.run(tree='tree/generate_wfs_from_list/init')

    assert (1, 5) == tool.get_dependencies(
        'generate_wfs_from_list/all_records'
    )
    tool.run()
    tool.count(done=13, fail=2)


def test_wf_gen_with_branching(tool):
    # run wf
    prepare_branching_wf(tool)
    # There is one task with record so results "all_records"
    # should have three dependencies (the record and the init)
    # and the if statement
    assert (3, 3) == tool.get_dependencies(
        'generate_wfs_from_list/all_records'
    )

    # There are in total 5 generated tasks so "all_results"
    # should have five dependency (generated tasks + init)
    assert (6, 6) == tool.get_dependencies(
        'generate_wfs_from_list/all_results'
    )


def test_wf_gen_with_branching2(tool):
    """
    Same as test_wf_gen_with_branching but runs the wf step by step
    This produces an awaitcount mismatch for the results tasks
    """

    def run_wf():
        tool.workflow(GeneratedBranchedWorkflow())

    run_wf()
    tool.run('tree/generate_wfs_from_list/init')
    tool.run('tree/generate_wfs_from_list/0/if_task')
    # again reapply workflow to resolve dependencies
    run_wf()

    tool.run()

    tool.ls()
    tool.command('view tree/generate_wfs_from_list/all_results')

    # There is one task with record so results "all_records"
    # should have three dependencies (record + init + if)
    assert (3, 3) == tool.get_dependencies(
        'generate_wfs_from_list/all_records'
    )

    # There are in total 4 generated tasks so "all_results"
    # should have six dependency (generated tasks + init + if)
    assert (6, 6) == tool.get_dependencies(
        'generate_wfs_from_list/all_results'
    )


def test_wf_gen_with_branching_and_frozen(tool):
    # run wf
    prepare_branching_wf(tool)

    # change input and cause conflict.
    # this should freeze the conflicted task
    # and all its descendants. In the current wf
    # this means that all tasks should be frozen
    tool.workflow(GeneratedBranchedWorkflow(msg='hi2'))
    with tool.repo:
        frozen = tool.frozen_tasks()

    # Calculate total number of tasks
    with tool.repo as repo:
        numberoftasks = sum(repo.tree().stat().counts.values())
    # assert all tasks are frozen
    assert len(frozen) == numberoftasks


def test_unrun_wf_gen_with_branching(tool):
    # run wf
    prepare_branching_wf(tool)
    # unrun wf generator
    print(tool.unrun('tree/generate_wfs_from_list'))
    tool.ls()
