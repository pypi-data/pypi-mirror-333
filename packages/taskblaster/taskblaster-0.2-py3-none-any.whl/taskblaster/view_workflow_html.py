DEFAULT_STYLE = {
    'hide-branch-labels': False,
    'hide-main-workflow': False,
    'hide-task-name': False,
    'task_width': '200px',
    'task-display': 'inline-block',
    'branch-end-socket': 'right',
    'task_height': '87px',
    'center-branch': False,
    'wf_width': '70%',
    'display-parameters': None,
    'branch-arrow-target': 'branchcontent',
    'arrow-path': 'fluid',
    'branch-arrow-size': '10',
    'arrow-size': '3',
    'workflowtitle-font-size': '2em',
    'workflowinput-font-size': '1em',
    'taskname-font-size': '1.5em',
    'taskimport-font-size': '1.5em',
    'startSocketGravity': '[0, 20]',
    'endSocketGravity': '[0, -20]',
    'customcss': [],
    'branch-startSocketGravity': '[80,0]',
    'branch-endSocketGravity': '[80,0]',
    'taskparameter-font-size': '1em',
    'colors': {
        'background': '#d3eaff',
        'workflowinput': 'rgb(135,214,146)',
        'branchbackground': '#eee',
        'branchcontentbackground': '#eff2ff',
        'branchtitle': '#e2edf7',
        'taskbody': 'rgb(136,204,215)',
        'iftaskbody': 'rgb(214,135,204)',
        'parameterarrow': 'rgb(0,255,0)',
        'jumparrow': 'rgb(0,0,0)',
        'iftruearrow': 'rgb(0,255,0)',
        'iffalsearrow': 'rgb(255,0,0)',
    },
}

wf_width = '90%'

CENTER_BRANCH = """display: flex;
                align-items: center;
                justify-content: center;"""


class ViewWorkflowTemplate:
    def __init__(self, style):
        self.style = style

    @property
    def head(self):
        style = self.style
        colors = style['colors']
        customcss = '\n'.join(style['customcss'])
        return f"""<html>
    <head>
        <script src="https://anseki.github.io/leader-line/js/libs-d4667dd-211118164156.js"></script>
        <style>
             .workflow {{
                display: block;
                width: {style['wf_width']};
                background-color: {colors['background']};
                padding: 25px;
                border-top-left-radius: 20px;
                z-index: -20;
            }}
            .mainworkflow {{
                visibility: {
            'collapse' if style['hide-main-workflow'] else 'visible'
        };
            }}
            .subworkflow {{
                display: block;
                border: 1px;
                padding: 30px;
                border-top-left-radius: 20px;
                filter: brightness(90%);
                z-index: 1;
            }}
            .workflowheader {{
                border-bottom-style: solid;
                border-bottom-width: 2px;
            }}
            .workflowtitle {{
                font-size: {style['workflowtitle-font-size']};
            }}
            .workflowinputs {{
                height: 30px;
                display: inline-block;
                align: center;
            }}
            .workflowinput {{
                padding: 5px;
                display: inline-block;
                background-color: {colors['workflowinput']};
                border-radius: 10px;
                border-width: 2px;
                height: 15px;
                margin: 5px;
                margin-top: 3px;
                border-style: solid;
                font-size: {style['workflowinput-font-size']};
            }}
            .workflowbody {{
                visibility: visible;
            }}
            .branchlist {{
                display: block;
            }}
            .branch {{
                justify-content: center;
            }}
            .branchtitle {{
                visibility: {
            'collapse' if style['hide-branch-labels'] else 'visible'
        };
                display: block;
                background-color: {colors['branchtitle']};
                border-bottom-style: solid;
                border-bottom-width: 1px;
            }}
            .branchcontent {{
                {
            'display: inline-block;'
            if not style['center-branch']
            else CENTER_BRANCH
        }
                background-color: {colors['branchcontentbackground']};
            }}
            .task {{
                display: {style['task-display']};
                margin: 2em;
            }}
            .iftaskbody {{
                display: inline-block;
                #border-top-right-radius: 10px;
                border-top-right-radius: 5px;
                border-bottom-right-radius: 50px;
                border-bottom-left-radius: 50px;
                background-color: {colors['iftaskbody']};
                border-style: solid;
                border-width: 2px;
                width: {style['task_width']};
                height: {style['task_height']};
                padding: 0px;
                z-index: 1;
                margin: auto;
            }}
            .taskbody {{
                position: relative;
                display: inline-block;
                #border-top-right-radius: 10px;
                border-top-right-radius: 5px;
                background-color: {colors['taskbody']};
                border-style: solid;
                border-width: 2px;
                width: {style['task_width']};
                height: {style['task_height']};
                padding: 0px;
                z-index: 0;
                margin: auto;
            }}
            .taskparameter-line {{
                display: block;
                padding: 0px;
                border: 0px;
                margin: 0px;
                height: calc({style['taskparameter-font-size']} + 10px);
                border: 0px;
                z-index: 3;
                position: relative;
            }}
            .taskparameters {{
                position: relative;
                display: inline;
                z-index: 2;
                border: 0px;
                #border-bottom: 2px;
                #border-bottom-style: solid;
                width: auto;
                height: calc({style['taskparameter-font-size']} + 10px);
                margin: 0px;
                padding: 0px;
            }}
            .taskparameter, .first-taskparameter {{
                background-color: {colors['taskbody']};
                display: inline-block;
                margin: 0px;
                padding: 2px;
                padding-left: 5px;
                padding-right: 5px;
                border: 0px;
                height: calc(1em + 3px);
                border-right-style: solid;
                border-right-width: 2px;
                border-top-style: solid;
                border-top-width: 2px;
                border-left-style: solid;
                border-left-width: 2px;
                border-top-left-radius: 3px;
                border-top-right-radius: 3px;
                border-bottom-style: solid;
                border-bottom-width: 2px;
                border-bottom-color: {colors['taskbody']};
                font-size: {style['taskparameter-font-size']};
                font-style: normal;
            }}
            .first-taskparameter {{
            }}
            .taskparameter-terminator {{
                grid-column: end;
                display: inline;
                margin: 0px;
                border: 0px;
                padding: 0px;
                height: calc({style['taskparameter-font-size']} + 3px);
                width: 20px;
            }}
            .taskname {{
                visibility: {
            'collapse' if style['hide-task-name'] else 'visible'
        };
                display: inline;
                font-weight: bold;
                font-size: {style['taskname-font-size']};
                padding: 2px;
                text-align: center;
                margin: 0px;
            }}
            .taskimport {{
                position: relative;
                top: 20px;
                font-style: italic;
                text-align: center;
                font-size: {style['taskimport-font-size']};
            }}
            .taskfooter {{
                display: block;
                text-align: center;
                width: 100%;
            }}
            .taskoutput {{
                font-size: 10px;
                text-align: center;
            }}
            .ifcolor {{
                background-color: {colors['iftaskbody']};
                border-bottom-color: {colors['iftaskbody']};
            }}
{customcss}
             .leader-line {{
                z-index: 10;
             }}
        </style>
    </head>
    <body>
    <div style="clear: both; overflow: hidden;">
"""

    @property
    def tail(self):
        return """
    </div>
    </body>
</html>
"""


LEADER_LINE = """
    line = new LeaderLine(
        document.getElementById('{frm}'),
        {beforeto}document.getElementById('{to}'){afterto},
        {{color: '{color}' }}
        );
    line.setOptions({{startSocket: '{startSocket}', endSocket: '{endSocket}',
                      dash: {dash}, size: {size},
        startSocketGravity: {startSocketGravity},
                endSocketGravity: {endSocketGravity}, 'path': '{arrow_path}',
                      dropShadow: {dropShadow}
                    }});
        """
