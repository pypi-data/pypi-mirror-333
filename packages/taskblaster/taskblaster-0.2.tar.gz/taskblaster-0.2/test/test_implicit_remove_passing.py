import taskblaster as tb


@tb.workflow
class BranchAfterIfGetsImplicitRemove:
    @tb._if(true='truebranch')
    @tb.define
    def task(self):
        return True

    @tb.branch('truebranch')
    @tb.define
    def implicit_task(self):
        return 'asd'


def test_branch_after_if_gets_implicit_remove(tool):
    tool.workflow(BranchAfterIfGetsImplicitRemove())
    tool.count(new=1)
    tool.run()
    tool.workflow(BranchAfterIfGetsImplicitRemove())
    tool.count(done=1, new=1)
    tool.run()
    tool.count(done=2)
    # Make sure the task as implicit_remove pointing to the task
    assert tool.input('implicit_task') == {
        '__tb_implicit_remove__': [['task', True]],
        'obj': 'asd',
    }


@tb.workflow
class SubSubWorkflow:
    @tb.define
    def task(self):
        return 'task'


@tb.workflow
class BranchingSubworkflow:
    obj = tb.var()

    @tb._if(true='truebranch')
    @tb.define
    def entry_task(self):
        return True

    @tb.branch('truebranch')
    @tb.define
    def implicit_subwf_task(self):
        return self.obj

    @tb.branch('truebranch')
    @tb.subworkflow
    def subsubwf(self):
        return SubSubWorkflow()


@tb.workflow
class BranchSubworkflowAfterIfGetsImplicitRemoveAtEntry:
    @tb._if(true='truebranch')
    @tb.define
    def task(self):
        return True

    @tb.branch('truebranch')
    @tb.subworkflow
    def implicit_subworkflow(self):
        return BranchingSubworkflow(obj=self.task)


def test_branch_subworkflow_after_if_gets_implicit_remove_at_entry(tool):
    tool.workflow(BranchSubworkflowAfterIfGetsImplicitRemoveAtEntry())
    tool.count(new=1)
    tool.run()
    tool.count(done=1)
    tool.workflow(BranchSubworkflowAfterIfGetsImplicitRemoveAtEntry())
    tool.count(done=1, new=1)
    tool.run()
    tool.count(done=2)
    tool.workflow(BranchSubworkflowAfterIfGetsImplicitRemoveAtEntry())
    tool.count(done=2, new=2)
    tool.run()
    tool.count(done=4)
    tool.ls()
    assert tool.input('task') == {'obj': True}
    assert tool.input('implicit_subworkflow/entry_task') == {
        '__tb_implicit_remove__': [['task', True]],
        'obj': True,
    }
    assert tool.input('implicit_subworkflow/implicit_subwf_task') == {
        '__tb_implicit_remove__': [
            ['task', True],
            ['implicit_subworkflow/entry_task', True],
        ],
        'obj': True,
    }
    assert tool.input('implicit_subworkflow/subsubwf/task') == {
        '__tb_implicit_remove__': [
            ['task', True],
            ['implicit_subworkflow/entry_task', True],
        ],
        'obj': 'task',
    }


@tb.dynamical_workflow_generator_task
def dwgtask(data):
    yield 'task1', tb.node('define', obj=1)
    yield 'task2', tb.node('define', obj=2)


@tb.workflow
class WorkflowGeneratorInAnIf:
    @tb._if(true='truebranch')
    @tb.define
    def task(self):
        return True

    @tb.branch('truebranch')
    @tb.dynamical_workflow_generator({'results': '**'})
    def dwg(self):
        return tb.node(dwgtask, data=self.task)


def test_unrunning_new_dynamical_workflow_generator(tool):
    tool.workflow(WorkflowGeneratorInAnIf())
    tool.count(new=1)
    tool.run()
    tool.count(done=1)
    tool.workflow(WorkflowGeneratorInAnIf())
    tool.count(new=2, done=1)
    tool.unrun('tree/task')
    tool.count(new=1, done=0)


def test_workflow_generator_in_if_gets_implicit_remove(tool):
    tool.workflow(WorkflowGeneratorInAnIf())
    tool.count(new=1)
    tool.run()
    tool.count(done=1)
    tool.workflow(WorkflowGeneratorInAnIf())
    tool.count(done=1, new=2)
    tool.run()
    tool.count(done=5, new=0)
    tool.ls()
    tasks = ['dwg/init', 'dwg/results', 'dwg/task1', 'dwg/task2', 'task']
    results = [
        {
            '__tb_implicit_remove__': [['task', True]],
            '__tb_result_tasks__': {'results': '**'},
            'data': True,
        },
        {
            '__tb_implicit__': [['dwg/init', None]],
            '__tb_implicit_remove__': [['task', True]],
            'obj': {'task1': 1, 'task2': 2},
        },
        {'obj': 1},
        {'obj': 2},
        {'obj': True},
    ]
    for task, result in zip(tasks, results):
        assert tool.input(task) == result


@tb.workflow
class NoImplicitDependenciesToSuperWorkflow:
    @tb._if(true='truebranch')
    @tb.task
    def task(self):
        return tb.node('define', obj=True)

    @tb.branch('truebranch')
    @tb.subworkflow
    def subwf(self):
        return BranchingSubworkflow(obj=self.truebranchtask)

    @tb.branch('truebranch')
    @tb.task
    def truebranchtask(self):
        return tb.node('define', obj='tbt')


def test_no_implicit_dependencies_to_super_workflow(tool):
    tool.workflow(NoImplicitDependenciesToSuperWorkflow())
    tool.count(new=1)
    tool.run()
    tool.count(done=1)
    tool.workflow(NoImplicitDependenciesToSuperWorkflow())
    tool.count(done=1, new=2)
    tool.run()
    tool.count(done=3, new=0)
    tool.workflow(NoImplicitDependenciesToSuperWorkflow())
    tool.ls()
    # XXX Actually CHECK
