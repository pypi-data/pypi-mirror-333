import os
import shutil
from pathlib import Path
from subprocess import check_output

from docutils import nodes
from docutils.parsers import rst
from docutils.parsers.rst import directives

from taskblaster.util import workdir

tmpdir = None
venv_str = None

# Mapping into docs/source/_static/ansi.css
_web_colormap = {
    '': '',
    '\033[0;30m': 'ansi-black',
    '\033[0;31m': 'ansi-red',
    '\x1b[31m': 'ansi-red',
    '\033[94m': 'ansi-lightBlue',
    '\x1b[92m': 'ansi-lightGreen',
    '\033[95m': 'ansi-lightPurple',
    '\033[91m': 'ansi-lightRed',
    '\033[96m': 'ansi-lightCyan',
    '\033[33m': 'ansi-yellow',
    '\033[32m': 'ansi-green',
    '\033[0m': '',
    '\033[0;34m': 'ansi-blue',
    '\x1b[93m': 'ansi-yellow',
    '\x1b[36m': 'ansi-black',
    '\x1b[35m': 'ansi-red',
    '\x1b[37m': 'ansi-lightGray',
}


class TBFile(rst.Directive):
    has_content = True

    node_class = nodes.literal_block

    def run(self):
        folder = self.content[0].split(' ')
        if len(folder) > 1:
            folder, target = folder
        else:
            folder = folder[0]
            target = folder
        env = self.state.document.settings.env
        rel_path, path = env.relfn2path(folder)
        rel_path, path2 = env.relfn2path(target)

        shutil.copy(path, tmpdir / Path(path2).name)
        return []


class TBViewWorkflow(rst.Directive):
    has_content = True

    node_class = nodes.literal_block

    def run(self):
        # folder = self.content[0]
        # env = self.state.document.settings.env
        # rel_path, path = env.relfn2path(folder)
        # print('copy', tmpdir / Path(path).name, path)
        # shutil.copy(tmpdir / Path(path).name, path)

        folder = self.content[0]
        confdir = Path(self.state.document.settings.env.app.confdir)
        static_path = self.state.document.settings.env.config.html_static_path[
            0
        ]
        shutil.copy(tmpdir / folder, confdir / static_path)
        print('copy', tmpdir / folder, confdir / static_path)
        return []


class TBInit(rst.Directive):
    has_content = True
    node_class = nodes.literal_block

    def run(self):
        folder = self.content[0]
        assert not Path(folder).is_absolute()
        pth = Path('/tmp/taskblaster') / str(folder) / 'tmprepo'
        from shutil import rmtree

        rmtree(pth, ignore_errors=True)
        pth.mkdir(parents=True)

        global tmpdir
        tmpdir = pth

        return []


class TBVenv(rst.Directive):
    has_content = True
    node_class = nodes.literal_block

    def run(self):
        global venv_str
        if self.content[0] == 'deactivate':
            venv_str = None
            return []
        venv_str = f'. {self.content[0]} &&'
        node = self.node_class('BLOCKTEXT1', f'source {self.content[0]}')
        return [node]


class Tokenizer:
    def __init__(self, txt):
        self.txt = txt
        self.index = 0

    def __iter__(self):
        def next_char():
            if self.index == len(self.txt):
                raise StopIteration
            c = self.txt[self.index]
            self.index += 1
            return c

        color_label = ''
        text = ''
        try:
            while True:
                c = next_char()
                if c == '\033':
                    if text != '':
                        yield text, color_label
                        text = ''
                    ansistr = '' + c
                    while c != 'm':
                        c = next_char()
                        ansistr += c
                    color_label = ansistr
                    continue
                text += c
        except StopIteration:
            if text != '':
                yield text, color_label


class TBShellCommand(rst.Directive):
    has_content = True

    node_class = nodes.literal_block

    no_output = False

    def run(self):
        command = self.content[0]

        if venv_str is not None:
            actual_command = venv_str + command
        else:
            actual_command = command

        with workdir(tmpdir):
            output = check_output(actual_command, encoding='utf-8', shell=True)

        if self.no_output:
            return []

        txt = f'$ {command}\n'

        children = []
        for text, color in Tokenizer(
            output.replace(str(tmpdir.parent), '/home/myuser')
        ):
            node = nodes.inline('', text)
            node['classes'] = [_web_colormap[color]]
            children.append(node)

        node = self.node_class('BLOCKTEXT1', txt, *children)

        return [node]


class TBHiddenShellCommand(TBShellCommand):
    no_output = True


def setup(app):
    os.environ['TB_COLORS'] = 'always'
    app.add_css_file('ansi.css')
    # app.add_js_file('leader-line.min.js')
    print('Setting up tb Sphinx Directives (tbinit, tbfile, tbshellcommand)')

    directives.register_directive('tbinit', TBInit)
    directives.register_directive('tbvenv', TBVenv)
    directives.register_directive('tbfile', TBFile)
    directives.register_directive('tbhiddenshellcommand', TBHiddenShellCommand)
    directives.register_directive('tbshellcommand', TBShellCommand)
    directives.register_directive('tbviewworkflow', TBViewWorkflow)
