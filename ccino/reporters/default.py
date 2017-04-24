from __future__ import absolute_import

from .base import BaseReporter


class DefaultReporter(BaseReporter):
    def start(self):
        self.write('\n')

    def suite_start(self, suite):
        if not suite.name == 'root':
            self.write('  ' * self.num_open_suites + suite.name + '\n')

    def test_pass(self, test):
        self.write('  ' * (self.num_open_suites + 1) + '✓ ' + test.desc + '\n')

    def test_fail(self, test):
        self.write('  ' * (self.num_open_suites + 1) + '{:d}) {:s}\n'.format(self.num_failures - 1, test.desc))

    def test_pending(self, test):
        self.write('  ' * (self.num_open_suites) + '- ' + test.desc + '\n')

    def end(self, time):
        self.print_summary()
