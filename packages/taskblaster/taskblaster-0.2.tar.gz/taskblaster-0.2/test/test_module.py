import pytest

from taskblaster import TBUserError
from taskblaster.repository import Repository

depending_err = 'depending on branch not yet visited'


# fixtures
@pytest.fixture
def modulerepo(testdir):
    # Unlocked repository
    return Repository.create(testdir, modulename='utilities.mymodule')


@pytest.fixture
def tool(modulerepo):
    from conftest import Tool

    return Tool(modulerepo)


@pytest.fixture
def moduleworkflow(modulerepo):
    from utilities.mymodule import MyModuleWorkflow

    return prepare_workflow(modulerepo, MyModuleWorkflow())


@pytest.fixture
def subworkflowworkflow(modulerepo):
    from utilities.mymodule import SubworkflowAccessTest

    return prepare_workflow(modulerepo, SubworkflowAccessTest())


# verify functions
def prepare_workflow(repo, workflow):
    with repo:
        rn = repo.runner()
        rn.run_workflow(workflow)
    return workflow


def verify_single_task(moduleworkflow, task, tool):
    tool.run(f'tree/{task}')
    try:
        tool.count(fail=0)
        tool.count(at_least=True, done=1)
    except AssertionError:
        prop = moduleworkflow
        paths = task.split('/')
        for i, idx in enumerate(paths):
            prop = getattr(prop, idx)
            if i < len(paths) - 1:
                prop = prop.get_node()

        purpose = prop.declaration.unbound_meth.__doc__
        if purpose.startswith('Expected to fail'):
            return
        raise Exception(
            f'A test task {task} failed. It was testing: {purpose}'
        )


# workflow integration tests
@pytest.mark.parametrize(
    'task',
    [
        'first/sub/testtask',
        'first/sub/testtask',
        'first/sub/testtask',
        'pass1/A',
        'pass1/B',
        'pass2/A',
        'pass2/B',
        'second/sub/failing_task',
    ],
)
def test_subworkflows(subworkflowworkflow, task, tool):
    tool.count(new=8)
    verify_single_task(subworkflowworkflow, task, tool)


def test_outoforderworkflow(modulerepo):
    from utilities.mymodule import OutOfOrderAccess

    with modulerepo:
        rn = modulerepo.runner()
        workflow = OutOfOrderAccess()
        with pytest.raises(TBUserError, match=depending_err):
            rn.run_workflow(workflow)


def test_outoforderworkflow2(modulerepo, tool):
    from utilities.mymodule import OutOfOrderAccess2

    with modulerepo:
        rn = modulerepo.runner()
        workflow = OutOfOrderAccess2()
        rn.run_workflow(workflow)

    tool.run()

    with modulerepo:
        rn = modulerepo.runner()
        workflow = OutOfOrderAccess2()
        with pytest.raises(TBUserError, match=depending_err):
            rn.run_workflow(workflow)


@pytest.mark.parametrize(
    'task',
    [
        'method_call_from_task',
        'test_method_call_from_task',
        'static_method_call',
        'test_static_method_call',
        'class_method_as_a_task',
        'test_class_method_a_task',
        'direct_class_method_as_task',
        'return_object_task',
        'use_object_task',
        'use_object_task_property',
        'return_dict',
        'index_dict',
        'test_call_function',
        'test_nested_function_call',
        'test_task_in_subworkflow',
        'call_subworkflow_return_value',
    ],
)
def test_custom_module(moduleworkflow, task, tool):
    # Verify that initial count matches
    tool.count(new=18)

    verify_single_task(moduleworkflow, task, tool)
