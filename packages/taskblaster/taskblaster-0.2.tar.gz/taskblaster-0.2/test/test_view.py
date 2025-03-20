from dataclasses import dataclass

import taskblaster as tb


def test_view(simplerepo, tool):
    tool.run()

    with simplerepo:
        simplerepo.view(['tree'])


@tb.workflow
class DummyHelloWf:
    num = tb.var()

    @tb.task
    def hello(self):
        # Task returning str type object. Gets actions from node target.
        return tb.node(hello_task, num=self.num)

    @tb.task
    def fancy_hello(self):
        # Task returning dataclass. Gets actions from returned cls.
        return tb.node(fancy_hello_task, num=self.num)


def add_exclamation(record: tb.TaskView):
    assert isinstance(record.output, str)
    return record.output + '!'


@tb.actions(statement=add_exclamation)
def hello_task(num: int):
    return _hello(num)


def _hello(num: int):
    return f'Hello {num}'


@tb.actions(statement='with_exclamation')
@dataclass
class StringResult:
    content: str

    def with_exclamation(self, taskview):
        # (Hardcoded in the test)
        assert taskview.realized_input == {'num': 42}
        return self.content + '!'

    def tb_encode(self):
        return dict(content=self.content)

    @classmethod
    def tb_decode(cls, dct):
        return cls(**dct)


def fancy_hello_task(num: int):
    return StringResult(_hello(num))


def test_actions(tool):
    num = 42
    tool.workflow(DummyHelloWf(num=num))
    tool.run()
    repo = tool.repo
    with repo:
        repo.view(['tree'])
        results = repo.view(['tree'], action='statement')
    assert len(results) == 2
    for result in results:
        assert result == f'Hello {num}!'
