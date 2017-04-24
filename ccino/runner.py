from __future__ import absolute_import

import sys

from .hook import Hook
from .reporters import get_reporter, get_reporter_names
from .root import RootSuite
from .suite import Suite
from .test import Test
from .util import load_module, redirect_print
from .util.decorator_wraps import combine_args_self
from .util.timer import Timer

class Runner(object):
    def __init__(self):
        self._root = RootSuite()
        self._current_suite = self._root

        self._reporter = 'default'
        self._output = None
        self._stdout = None

    @combine_args_self
    def suite(self, func, name=None):
        curr_suite =  self._current_suite

        suite = Suite(func, name)
        curr_suite.add_suite(suite)

        self._current_suite = suite

        suite.load()

        self._current_suite = curr_suite

    @combine_args_self
    def test(self, func, desc=None):
        test = Test(func, desc)
        self._current_suite.add_test(test)

    @combine_args_self
    def suite_setup(self, func, desc=None):
        hook = Hook(func, desc)
        self._current_suite.add_suite_setup(hook)

    @combine_args_self
    def suite_teardown(self, func, desc=None):
        hook = Hook(func, desc)
        self._current_suite.add_suite_teardown(hook)

    @combine_args_self
    def setup(self, func, desc=None):
        hook = Hook(func, desc)
        self._current_suite.add_setup(hook)

    @combine_args_self
    def teardown(self, func, desc=None):
        hook = Hook(func, desc)
        self._current_suite.add_teardown(hook)

    def reporter(self, reporter):
        if not reporter in get_reporter_names():
            raise Exception('Unknown reporter')

        self._reporter = reporter

    def output(self, stream):
        self._output = stream

    def stdout(self, stream):
        self._stdout = stream

    def run_tests(self):
        reporter = get_reporter(self._reporter)

        if self._output:
            reporter.output(self._output)

        def test_pass(test):
            reporter.test_pass_b

        reporter.base_start()
        reporter.start()

        t = Timer()
        t.start()

        if not self._stdout == None:
            with redirect_print(self._stdout):
                self._root.run(reporter)
        else:
            self._root.run(reporter)

        t.stop()

        reporter.base_end(t.get_time())
        reporter.end(t.get_time())

    describe = suite
    it = test
    # before = suite_setup
    # after = suite_teardown
    # before_each = setup
    # after_each = teardown
