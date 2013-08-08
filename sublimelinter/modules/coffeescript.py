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

        for line in errors.splitlines():
            parts = line.split(',')
            filename, line, level = parts[0:3]
            message = ''.join(parts[3::])
            if not line:
                line = 0
            messages = warningMessages if level == 'warn' else errorMessages
            self.add_message(int(line), lines, message, messages)
