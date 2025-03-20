import taskblaster as tb


def initialize(number):
    return number


def is_even(number):
    return number % 2 == 0


def three_n_plus_one(number):
    return 3 * number + 1


def divide_by_two(number):
    return number // 2


def stop_iteration(number):
    return number == 1


def extract_sequence(data):
    return data


@tb.workflow
class CollatzIteration:
    number = tb.var()

    @tb._if(true='even_branch', false='odd_branch')
    @tb.task
    def IsEven(self):
        return tb.node(is_even, number=self.number)

    @tb.branch('even_branch')
    @tb.jump('result')
    @tb.task
    def even_task(self):
        return tb.node(divide_by_two, number=self.number)

    @tb.branch('odd_branch')
    @tb.jump('result')
    @tb.task
    def odd_task(self):
        return tb.node(three_n_plus_one, number=self.number)

    @tb.branch('result')
    @tb.fixedpoint
    @tb.task
    def result(self):
        return tb.node(
            'define',
            obj=self.Phi(even_branch=self.even_task, odd_branch=self.odd_task),
        )


@tb.workflow
class CollatzSequence:
    number = tb.var()

    @tb.jump('collatz_loop')
    @tb.task
    def initialize(self):
        return tb.node(initialize, number=self.number)

    @tb.branch('collatz_loop', loop=True)
    @tb.subworkflow
    def iteration(self):
        return CollatzIteration(
            number=self.Phi(
                entry=self.initialize, collatz_loop=self.iteration.result
            )
        )

    @tb.branch('collatz_loop', loop=True)
    @tb._if(true='finish', false='collatz_loop')
    @tb.task
    def stop_iteration(self):
        return tb.node(stop_iteration, number=self.iteration.result)

    @tb.branch('finish')
    @tb.task
    def gather_sequence(self):
        return tb.node(extract_sequence, data=self.iteration.result)


def test_dynamic_subworkflow_on_dynamic_workflow(tool):
    def iterate():
        wf = CollatzSequence(number=5)
        tool.workflow(wf)
        tool.run()

    for done, new in [
        [2, 2],
        [5, 0],
        [6, 2],
        [9, 0],
        [10, 2],
        [13, 0],
        [14, 2],
        [17, 0],
        [18, 2],
        [21, 0],
        [22, 0],
        [22, 0],
    ]:
        iterate()
        tool.count(new=new, fail=0, cancel=0, done=done)
