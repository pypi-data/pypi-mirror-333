from pathlib import Path
from typing import Any

from taskblaster import writes


class Entry:
    """Entry in file-based cache.

    Entry wraps a directory and provides access to functionality
    related to how a task is physically stored inside that directory."""

    inputname = 'input.json'
    updatedinputname = 'updated_input.json'
    outputname = 'output.json'
    handlername = 'handler.json'
    handlerdataname = 'handler_data.json'
    exceptiondataname = 'exception_data.json'
    stacktracetemplate = 'stacktrace.rank{:02d}.err'
    stacktracepattern = 'stacktrace.rank*.err'

    def __init__(self, directory, json_protocol, read_only=False):
        self.directory = Path(directory)
        self.json_protocol = json_protocol
        self.read_only = read_only

    def __repr__(self):
        return f'<Entry({self.directory})>'

    @property
    def inputfile(self) -> Path:
        return self.directory / self.inputname

    @property
    def outputfile(self) -> Path:
        return self.directory / self.outputname

    @property
    def exceptiondatafile(self):
        return self.directory / self.exceptiondataname

    def read_datafied_exception(self):
        try:
            return self.exceptiondatafile.read_text()
        except FileNotFoundError:
            return None

    @property
    def handlersfile(self) -> Path:
        return self.directory / self.handlername

    @property
    def handlersdatafile(self) -> Path:
        """We should never load this file, the handler will. We should always
        make sure to delete it when we delete the handler.json"""
        return self.directory / self.handlerdataname

    @property
    def updatedinputfile(self):
        return self.directory / self.updatedinputname

    @writes
    def delete(self):
        assert self.inputfile.parent == self.directory
        assert self.outputfile.parent == self.directory
        assert self.handlersfile.parent == self.directory

        self.inputfile.unlink(missing_ok=True)
        self.updatedinputfile.unlink(missing_ok=True)
        self.outputfile.unlink(missing_ok=True)
        self.handlersfile.unlink(missing_ok=True)
        self.handlersdatafile.unlink(missing_ok=True)
        self.exceptiondatafile.unlink(missing_ok=True)

        # remove stacktrace files
        for stacktracefile in self.stacktracefiles():
            stacktracefile.unlink()

        try:
            self.directory.rmdir()  # nuke the directory if no files exist
        except OSError:
            pass  # (Directory not empty)

    def stacktracefiles(self):
        for stacktracefile in self.directory.glob(self.stacktracepattern):
            assert stacktracefile.suffix == '.err', (
                "Found a stacktrace that isn't .err file"
            )
            assert self.directory == stacktracefile.parent
            yield stacktracefile

    def read_inputfile(self):
        return self.inputfile.read_text()

    def output(self) -> Any:
        # XXX Remove _hook stuff from Entry and remove this method
        output = self.outputfile.read_text()
        return self._hook.loads(output)

    def has_output(self):
        return self.outputfile.exists()

    @property
    def has_updated_inputs(self):
        return self.updatedinputfile.exists()

    @property
    def updated_serialized_inputs(self):
        """return the text or None if the file is not found."""
        try:
            return self.updatedinputfile.read_text()
        except FileNotFoundError:
            return None

    @property
    def _hook(self):
        return self.json_protocol.outputencoder(self.directory)

    @writes
    def dump_output(self, output):
        jsontext = self._hook.dumps(output)

        # We first write to out.json.part and then rename to out.json.
        # This means if and when out.json exists, it is guaranteed
        # intact.
        tmpfile = self.outputfile.with_suffix('.part')
        tmpfile.write_text(jsontext)
        tmpfile.rename(self.outputfile)
