from __future__ import absolute_import

from .base import BaseReporter, override


class DebugReporter(BaseReporter):
    """Debug reporter for debugging ccino.

    This reporter is verbose and prints something for each base print
    method. A summary is not printed in the end.

    This is not intended for regular use.
    """

    @override
    def start(self):
        self.write('starting tests\n')

    @override
    def suite_start(self, suite):
        padding = '  ' * self.num_open_suites

        self.write('\n' + padding + 'entering suite \'' + suite.name + '\'\n')

    @override
    def suite_end(self, suite):
        padding = '  ' * (self.num_open_suites + 1)

        self.write(padding + 'exiting suite \'' + suite.name + '\'\n\n')

    @override
    def test_pass(self, test):
        padding = '  ' * (self.num_open_suites + 1)

        self.write(padding + 'test \'' + test.desc + '\' passed\n')

    @override
    def test_fail(self, test):
        padding = '  ' * (self.num_open_suites + 1)
        num = '({:d})'.format(self.num_failures - 1)

        self.write(padding + 'test \'' + test.desc + '\' failed ' + num + '\n')

    @override
    def test_pending(self, test):
        padding = '  ' * (self.num_open_suites + 1)

        self.write(padding + 'test \'' + test.desc + '\' pending\n')

    @override
    def hook_pass(self, hook):
        padding = '  ' * (self.num_open_suites + 1)

        self.write(padding + 'ran hook \'{:s}\'\n'.format(hook.desc))

    @override
    def hook_fail(self, hook):
        padding = '  ' * (self.num_open_suites + 1)
        num = '({:d})'.format(self.num_failures - 1)

        self.write(padding + 'hook \'' + hook.desc + '\' failed ' + num + '\n')

    @override
    def end(self, time):
        summary = 'stopped running tests, took {:012.6f} seconds\n' \
                .format(time)

        self.write(summary)
