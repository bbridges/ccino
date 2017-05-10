from __future__ import division

import sys
import traceback

import blessings

from ..hook import Hook
from ..test import Test


WINDOWS = sys.platform == 'win32'


CHECK_SYMBOL = u'\u2713' if not WINDOWS else u'\u221A'
ERROR_SYMBOL = u'\u2716' if not WINDOWS else u'\u00D7'


def format_seconds_short(seconds):
    round_n = lambda n: int(round(n))

    if seconds >= 3600:
        return str(round_n(seconds / 3600)) + 'h'

    if seconds >= 60:
        return str(round_n(seconds / 60)) + 'm'

    if seconds >= 1:
        return str(round_n(seconds)) + 's'

    if seconds >= 1e-3:
        return str(round_n(seconds * 1e3)) + 'ms'

    return str(max(round_n(seconds * 1e6), 1)) + u'\u00B5s'


class BaseReporter(object):
    def __init__(self):
        self._stream = sys.stdout
        self._mirror = False
        self._force_color = False
        self._exc_context = False

        self._terminal = None

    def color(self, use_color=None):
        if use_color == False:
            self._force_color = None
        elif use_color == True:
            self._force_color = True
        elif use_color == None:
            self._force_color = False
        else:
            raise TypeError('use_color must be bool or None')

    def output(self, stream):
        self._stream = stream

    def write(self, string):
        if self._stream:
            self._stream.write(string)

    def mirror(self, on=True):
        self._mirror = on

    def exc_context(self, show=True):
        self._exc_context = show

    def _get_last_exception(self):
        info = sys.exc_info()

        exc = self.terminal.red(
            ''.join(traceback.format_exception_only(*info[0:2]))
        )

        tb = traceback.extract_tb(info[2])
        tb_msg = ''

        for trace in reversed(tb):
            tb_msg += ' at {:s} ({:s}:{:d})\n'.format(
                trace[2], trace[0], trace[1]
            )

            if self._exc_context and trace[3] is not None:
                tb_msg += '   {:s}\n'.format(trace[3])

        tb_msg = self.terminal.bright_black(tb_msg)

        return exc + tb_msg

    def base_start(self):
        self.num_suites = 0
        self.num_open_suites = 0
        self.num_tests = 0
        self.num_passes = 0
        self.num_pending = 0
        self.num_failures = 0

        self.open_suites = []
        self.errors = []

        self._terminal = blessings.Terminal(
            stream=self._stream, force_styling=self._force_color
        )

        self.start()

    def base_suite_start(self, suite):
        if not suite.is_root:
            self.num_suites += 1
            self.num_open_suites += 1

            self.open_suites.append(suite.name)

        self.suite_start(suite)

    def base_suite_end(self, suite):
        self.num_open_suites -= 1

        if not suite.is_root:
            self.open_suites.pop()

        self.suite_end(suite)

    def base_test_pass(self, test):
        self.num_passes += 1

        self.test_pass(test)

    def base_test_fail(self, test):
        self.num_failures += 1

        self.errors.append((test, self._get_last_exception()))

        self.test_fail(test)

    def base_test_pending(self, test):
        self.num_pending += 1

        self.test_pending(test)

    def base_hook_pass(self, hook):
        self.hook_pass(hook)

    def base_hook_fail(self, hook):
        self.num_failures += 1

        self.errors.append((test, self._get_last_exception()))

        self.hook_fail(hook)

    def base_end(self, time):
        self.time = time

        self.end(time)

    def start(self):
        pass

    def suite_start(self, suite):
        pass

    def suite_end(self, suite):
        pass

    def test_pass(self, test):
        pass

    def test_fail(self, test):
        pass

    def test_pending(self, test):
        pass

    def hook_pass(self, hook):
        pass

    def hook_fail(self, hook):
        pass

    def end(self, time):
        pass

    def print_summary(self):
        if self.num_passes:
            passes = self.terminal.green(
                '  {:d} passing'.format(self.num_passes)
            )

            time = self.terminal.bright_black(
                '({:s})'.format(format_seconds_short(self.time))
            )

            self.write(passes + ' ' + time + '\n')

        if self.num_pending:
            self.write(self.terminal.cyan(
                '  {:d} passing\n'.format(self.num_pending)
            ))

        if self.num_failures:
            self.write(self.terminal.red(
                '  {:d} failing\n'.format(self.num_failures)
            ))

        for i in range(self.num_failures):
            runnable = self.errors[i][0]
            error = self.errors[i][1]

            desc = ''

            if isinstance(runnable, Test):
                desc = runnable.desc

            number = '{:d})'.format(self.num_failures)

            self.write('\n  ' + number + ' ' + desc + '\n')

            self.write('     ' + error.replace('\n', '\n     '))

    @property
    def terminal(self):
        return self._terminal
