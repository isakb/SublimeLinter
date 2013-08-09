from base_linter import BaseLinter

CONFIG = {
    'language': 'CoffeeScript',
    'executable': 'coffeelint',
    'lint_args': ['-s', '--csv']
}


class Linter(BaseLinter):

    def _get_lint_args(self, view, code, filename):
        args = BaseLinter._get_lint_args(self, view, code, filename)
        config_file = view.settings().get('coffeelint_config_file')
        if config_file:
            return args + ['-f', config_file]
        else:
            return args

    def parse_errors(self, view, errors, lines, errorUnderlines,
                     violationUnderlines, warningUnderlines, errorMessages,
                     violationMessages, warningMessages):

        splitlines = errors.splitlines()
        if splitlines[0] == 'path,lineNumber,lineNumberEnd,level,message':
            # v 0.5.7:
            splitlines = splitlines[1::]
            getLineParts = lambda p: (p[0], p[1], p[3], ''.join(p[4::]))
        else:
            # v0.5.6:
            getLineParts = lambda p: (p[0], p[1], p[2], ''.join(p[3::]))
        for line in splitlines:
            filename, line, level, message = getLineParts(line.split(','))
            if not line:
                line = 0
            messages = warningMessages if level == 'warn' else errorMessages
            self.add_message(int(line), lines, message, messages)
