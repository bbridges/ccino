from __future__ import print_function

import sys
import traceback


PYTHON_3 = sys.version_info[0] == 3


if PYTHON_3:
    from io import StringIO
else:
    from StringIO import StringIO


import colorama
import blessings


from ..hook import Hook
from ..test import Test


class BaseReporter(object):
    def __init__(self):
        self._stream = None
        self._mirror = False

    def output(self, stream):
        self._stream = stream

    def write(self, string):
        if self._stream:
            self._stream.write(string)

        if not self._stream or self._mirror:
            print(string, end='')

    def mirror(self, on=True):
        self._mirror = on

    def base_start(self):
        self.num_suites = 0
        self.num_open_suites = 0
        self.num_tests = 0
        self.num_passes = 0
        self.num_pending = 0
        self.num_failures = 0

        self.open_suites = []
        self.errors = []

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

        err_out = StringIO()

        traceback.print_exc(file=err_out)

        self.errors.append((test, err_out.getvalue()))

        self.test_fail(test)

    def base_test_pending(self, test):
        self.num_pending += 1

        self.test_pending(test)

    def base_hook_pass(self, hook):
        self.hook_pass(hook)

    def base_hook_fail(self, hook):
        self.num_failures += 1

        err_out = StringIO()

        traceback.print_exc(file=err_out)

        self.errors.append((hook, err_out.getvalue()))

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
        for i in range(self.num_failures):
            runnable = self.errors[i][0]
            error = self.errors[i][1]

            desc = ''

            if isinstance(runnable, Test): pass


            self.write('\n  {:d}) {:s}\n'.format(i, desc))

            self.write('\n' + error + '\n')
