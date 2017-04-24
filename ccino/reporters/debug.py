from __future__ import absolute_import

from .base import BaseReporter


class DebugReporter(BaseReporter):
    def start(self):
        self.write('starting tests\n')

    def suite_start(self, suite):
        self.write('\n' + '  ' * self.num_open_suites + 'entering suite \'{:s}\'\n'.format(suite.name))

    def suite_end(self, suite):
        self.write('  ' * (self.num_open_suites + 1) + 'exiting suite \'{:s}\'\n\n'.format(suite.name))

    def test_pass(self, test):
        self.write('  ' * (self.num_open_suites + 1) + 'test \'{:s}\' passed\n'.format(test.desc))

    def test_fail(self, test):
        self.write('  ' * (self.num_open_suites + 1) + 'test \'{:s}\' failed ({:d})\n'.format(test.desc, self.num_failures - 1))

    def test_pending(self, test):
        self.write('  ' * self.num_open_suites + 'test \'{:s}\' pending\n'.format(test.desc))

    def hook_pass(self, hook):
        self.write('  ' * (self.num_open_suites + 1) + 'ran hook \'{:s}\'\n'.format(hook.desc))

    def hook_fail(self, hook):
        self.write('  ' * (self.num_open_suites + 1) + 'hook \'{:s}\' failed ({:d})\n'.format(hook.desc, self.num_failures - 1))

    def end(self, time):
        self.write('stopped running tests, took {:012.6f} seconds\n'.format(time))

        # self.print_summary()
