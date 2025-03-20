import taskblaster as tb


@tb.workflow
class Base:
    a1 = tb.var()

    @tb.task
    def task1(self):
        return tb.node('define', obj=self.a1)


@tb.workflow
class Nested(Base):
    a2 = tb.var()

    @tb.task
    def task2(self):
        return tb.node('define', obj=self.a2)

    @tb.task
    def task3(self):
        return tb.node('define', obj=self.task1)


def hello(msg):
    return f'hello {msg}'


@tb.workflow
class NestedMore(Nested):
    a2 = tb.var(default='a2default')
    a3 = tb.var()

    @tb.task
    def task3(self):
        return tb.node('define', obj=[self.task4, self.a3])

    @tb.task
    def task4(self):
        return tb.node('define', obj=self.a2)


def test_workflow_subclass(tool):
    """Test that inputvars and tasks are inherited by workflow subclass.

    This is mostly to test the inputvars since those are not implemented
    using functions on the class, therefore it is not trivial that it works.
    """
    tool.workflow(Nested(a1='a1', a2='a2'))
    tool.run()
    assert tool.peek('task1') == 'a1'
    assert tool.peek('task2') == 'a2'
    assert tool.peek('task3') == 'a1'


def test_doublesubclass_constructor():
    workflow = NestedMore(a1='a1value', a3='a3value')

    # Variously inherited/overridden vars:
    assert workflow.a1.getvalue() == 'a1value'
    assert workflow.a2.getvalue() == 'a2default'
    assert workflow.a3.getvalue() == 'a3value'


def test_doublesubclass_attrs():
    classvars = set(tb.inherited_classvars(NestedMore))

    # Classvars also include __class__ and __ge__ etc. etc.
    assert classvars >= {'a1', 'a2', 'a3', 'task1', 'task2', 'task3', 'task4'}


def test_workflow_doublesubclass(tool):
    tool.workflow(NestedMore(a1='a1value', a3='a3value'))
    tool.run()
    # Inherited two levels down:
    assert tool.peek('task1') == 'a1value'

    # task2 works on a2 which in the NestedMore subclass has default value:
    assert tool.peek('task2') == 'a2default'

    assert tool.peek('task4') == 'a2default'

    # task3 is overridden with to depend on task4, which
    # exists only in the NestedMore class:
    assert tool.peek('task3') == ['a2default', 'a3value']
