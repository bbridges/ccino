from __future__ import absolute_import

import sys

from .hook import Hook
from .reporters import get_reporter, get_reporter_names
from .root import RootSuite
from .suite import Suite
from .test import Test
from .util import load_module, redirect_print, make_builtin
from .util.decorator_wraps import combine_args_self
from .util.timer import Timer


def _get_options_checker(options):
    def check_options(key, default):
        return key in options and getattr(options, key) or default

    return check_options


class Runner(object):
    def __init__(self, **options):
        self._root = RootSuite()
        self._current_suite = self._root

        check_options = _get_options_checker(options)

        self._verbosity = check_options('verbosity', 0)
        self._bail = check_options('bail', False)
        self._color = check_options('color', None)
        self._exc_context = check_options('exc_context', False)
        self._reporter = check_options('reporter', 'default')
        self._output = check_options('output', sys.stdout)
        self._stdout = check_options('stdout', sys.stdout)

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

    def color(self, use_color=None):
        self._color = use_color

    def output(self, stream):
        self._output = stream

    def stdout(self, stream):
        self._stdout = stream

    def exc_context(self, show=True):
        self._exc_context = show

    def run_tests(self):
        reporter = get_reporter(self._reporter)

        reporter.output(self._output)
        reporter.color(self._color)
        reporter.exc_context(self._exc_context)

        reporter.base_start()

        t = Timer()
        t.start()

        with redirect_print(self._stdout):
            self._root.run(reporter)

        t.stop()

        reporter.base_end(t.get_time())

        return reporter.num_failures == 0

    describe = suite
    it = test
    # before = suite_setup
    # after = suite_teardown
    # before_each = setup
    # after_each = teardown


EXPORTED_RUNNER_METHODS = [
    'suite',
    'test',
    'suite_setup',
    'suite_teardown',
    'setup',
    'teardown',
    'describe',
    'it'
]


def insert_into_globals(runner):
    for name in EXPORTED_RUNNER_METHODS:
        globals()[name] = getattr(runner, name)


def insert_into_builtins(runner):
    for name in EXPORTED_RUNNER_METHODS:
        make_builtin(getattr(runner, name), name)
