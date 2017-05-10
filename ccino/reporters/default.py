from __future__ import absolute_import

from .base import BaseReporter, CHECK_SYMBOL


class DefaultReporter(BaseReporter):
    def start(self):
        self.write('\n')

    def suite_start(self, suite):
        if not suite.name == 'root':
            self.write('  ' * self.num_open_suites + suite.name + '\n')

    def test_pass(self, test):
        padding = '  ' * (self.num_open_suites + 1)
        check = self.terminal.green(CHECK_SYMBOL)
        desc = self.terminal.bright_black(test.desc)

        message = padding + check + ' ' + desc + '\n'

        self.write(message)

    def test_fail(self, test):
        padding = '  ' * (self.num_open_suites + 1)
        number = self.terminal.red('{:d})'.format(self.num_failures - 1))
        desc = self.terminal.red(test.desc)

        self.write(padding + number + ' ' + desc + '\n')

    def test_pending(self, test):
        self.write('  ' * (self.num_open_suites) + '- ' + test.desc + '\n')

    def end(self, time):
        self.write('\n')

        self.print_summary()

        self.write('\n')
