import taskblaster as tb


def phonon_results(ok, image_forces):
    return ok


@tb.workflow
class MyWorkflow:
    inputs = tb.var()

    @tb.subworkflow
    def phonon_wf(self):
        return PhononWf(inputs=self.inputs)


@tb.workflow
class MyOtherWorkflow:
    inputs = tb.var()

    @tb.subworkflow
    def phonon_wf(self):
        return PhononWf(inputs=self.inputs)

    @tb.dynamical_workflow_generator({'PL_results': '**'})
    def PL_spectras(self):
        return tb.node(generate_tasks_from_list, inputs=self.phonon_wf.results)


@tb.workflow
class PhononWf:
    inputs = tb.var()

    @tb.task
    def ok(self):
        return tb.node('taskblaster.testing.ok', msg=self.inputs)

    @tb.dynamical_workflow_generator({'collect_image_forces': '**'})
    def calculate_image_forces(self):
        return tb.node(generate_tasks_from_list, inputs=self.ok)

    @tb.task
    def results(self):
        return tb.node(
            phonon_results,
            ok=self.ok,
            image_forces=self.calculate_image_forces.collect_image_forces,
        )


@tb.dynamical_workflow_generator_task
def generate_tasks_from_list(inputs):
    for idx, image in enumerate(inputs):
        yield f'image_{idx}', tb.node('taskblaster.testing.ok', msg=image)


def verify_all_done(tool):
    tool.count(done=10, fail=0, new=0)


"""
In the following two tests we run the same workflow
first in two steps and later in a single go.

These two tests should be equivalent but
test_complex_wf_gen_singlestep fails.
"""


def test_complex_wf_gen_twosteps(tool):
    # MyWorkflow contains first half of testWf
    tool.workflow(MyWorkflow(inputs=['my cat', 'is dead']))

    # Run init task before we add second wf generator
    tool.run('tree/phonon_wf/calculate_image_forces/init')

    # Add second wf generator that depnds on a task that
    # depends on the result object of the first wf generator
    tool.workflow(MyOtherWorkflow(inputs=['my cat', 'is dead']))
    tool.run()
    verify_all_done(tool)


def test_complex_wf_gen_singlestep(tool):
    """
    Now we do exactly the same this as in
    test_complex_wf_gen_twostep but we attempt
    to run the final wf in a single step
    """
    wf = MyOtherWorkflow(inputs=['my cat', 'is dead'])
    # This used to fail with Attribute error, but now is fixed
    tool.workflow(wf)

    tool.run()
    verify_all_done(tool)
