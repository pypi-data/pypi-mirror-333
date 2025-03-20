from pathlib import Path

import taskblaster as tb

relpath = Path('somedir/somepath.ext')
reftext = 'potato'


def getpath():
    relpath.parent.mkdir()
    relpath.write_text(reftext)
    return relpath


def readpath(path):
    return path.read_text()


@tb.workflow
class PassPaths:
    @tb.task
    def create(self):
        return tb.node(getpath)

    @tb.task
    def read(self):
        # Here our input should be normalized to an absolute path
        return tb.node(readpath, path=self.create)

    @tb.define
    def definepath(self):
        return relpath


def test_pass_paths(tool):
    tool.workflow(PassPaths())
    tool.run()
    path = tool.peek('create')

    assert path.is_absolute()
    assert 'create' in path.parts
    assert path.read_text() == reftext

    assert tool.peek('read') == reftext
