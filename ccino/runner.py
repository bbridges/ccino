from __future__ import absolute_import

import sys

from .exceptions import CcinoBail
from .reporters import get_reporter, get_reporter_names
from .fixtures import Test, Hook, Suite
from .fixtures.root import RootSuite
from .util import load_module, redirect_print, make_builtin
from .util.decorator_wraps import combine_args_self
from .util.timer import Timer


def _get_options_checker(options):
    """Get a function to check options with a default value.

    Returns:
        Callable: The function to check options with defaults.
    """

    def check_options(key, default):
        return key in options and getattr(options, key) or default

    return check_options


class Runner(object):
    """Class that runs ccino tests.

    ccino internally uses this to run its tests and this is exposed
    as well for outside use.
    """

    def __init__(self, **options):
        """Create a new Runner object.

        Args:
            **options: Specified options to use for the runner.
        """

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
        """Returns a decorator for adding a new suite.

        Keyword Args:
            name (str): Name of the suite.

        Returns:
            Callable: The decorator.
        """

        curr_suite = self._current_suite

        suite = Suite(func, curr_suite, name)
        curr_suite.add_suite(suite)

        self._current_suite = suite

        suite.load()

        self._current_suite = curr_suite

        return func

    @combine_args_self
    def test(self, func, desc=None):
        """Returns a decorator for adding a new test.

        Keyword Args:
            name (str): Name of the test.

        Returns:
            Callable: The decorator.
        """

        test = Test(func, name=desc)
        self._current_suite.add_test(test)

        return func

    @combine_args_self
    def suite_setup(self, func, desc=None):
        """Returns a decorator for adding a new suite setup hook.

        Keyword Args:
            name (str): Name of the hook.

        Returns:
            Callable: The decorator.
        """

        hook = Hook(func, name=desc)
        self._current_suite.add_suite_setup(hook)

        return func

    @combine_args_self
    def suite_teardown(self, func, desc=None):
        """Returns a decorator for adding a new suite teardown hook.

        Keyword Args:
            name (str): Name of the hook.

        Returns:
            Callable: The decorator.
        """

        hook = Hook(func, name=desc)
        self._current_suite.add_suite_teardown(hook)

        return func

    @combine_args_self
    def setup(self, func, desc=None):
        """Returns a decorator for adding a new suite hook.

        Keyword Args:
            name (str): Name of the hook.

        Returns:
            Callable: The decorator.
        """

        hook = Hook(func, name=desc)
        self._current_suite.add_setup(hook)

        return func

    @combine_args_self
    def teardown(self, func, desc=None):
        """Returns a decorator for adding a new teardown hook.

        Keyword Args:
            name (str): Name of the hook.

        Returns:
            Callable: The decorator.
        """

        hook = Hook(func, name=desc)
        self._current_suite.add_teardown(hook)

        return func

    @combine_args_self
    def skip(self, func, condition=True):
        """Returns a decorator for skipping a fixture.

        Keyword Args:
            condition (bool): Whether the fixture should be skipped.

        Returns:
            Callable: The decorator.
        """

        if condition:
            func._skip = True

        return func

    @combine_args_self
    def raises(self, func, exception):
        """Returns a decorator for expecting a test exception.

        Args:
            excpetion (Exception): The expected exception.

        Returns:
            Callable: The decorator.
        """

        func._raises = exception

        return func

    @combine_args_self
    def returns(self, func, value, approx=None):
        """Returns a decorator for expecting a test return value.

        Args:
            value (Object): The expected return value.

        Keyword Args:
            approx (float): Tolerance for numeric return values.

        Returns:
            Callable: The decorator.
        """

        if approx is None:
            func._returns = value
            func._returns_approx = False
        else:
            func._returns = [value, approx]
            func._returns_approx = True

        return func

    def bail(self, stop=True):
        """Stop the tests from running on failure.

        Keyword Args:
            stop (bool): Whether the runnner should bail.
        """

        self._bail = stop

    def reporter(self, reporter):
        """Specify the reporter to use.

        Args:
            reporter (str): The reporter to use.
        """

        if not reporter in get_reporter_names():
            raise Exception('Unknown reporter')

        self._reporter = reporter

    def color(self, use_color=None):
        """Specify if colors should be used.

        A value of None will effectively set this to auto.

        Keyword Args:
            use_color (bool): Whether or not to use color.
        """

        self._color = use_color

    def output(self, stream):
        """Specify the output stream.

        Args:
            stream (:obj:`io.IOBase`): The output stream.
        """

        self._output = stream

    def stdout(self, stream):
        """Specify the stdout output stream.

        Args:
            stream (:obj:`io.IOBase`): The stdout output stream.
        """

        self._stdout = stream

    def exc_context(self, show=True):
        """Specify if exception should show the lines.

        Keyword Args:
            show (bool): Wether or not to show the lines.
        """

        self._exc_context = show

    def run_tests(self):
        """Run the root suite.

        Returns:
            bool: If there were any failures.
        """

        reporter = get_reporter(self._reporter)

        reporter.output(self._output)
        reporter.color(self._color)
        reporter.exc_context(self._exc_context)

        reporter.base_start()

        t = Timer()
        t.start()

        try:
            with redirect_print(self._stdout):
                self._root.run(reporter, dict(
                    bail=self._bail
                ))

        except CcinoBail as e: pass

        t.stop()

        reporter.base_end(t.get_time())

        return reporter.num_failures == 0

    describe = suite
    it = test
    before = suite_setup
    after = suite_teardown
    before_each = setup
    after_each = teardown


EXPORTED_RUNNER_METHODS = [
    'suite',
    'test',
    'suite_setup',
    'suite_teardown',
    'setup',
    'teardown',
    'describe',
    'it',
    'before',
    'after',
    'before_each',
    'after_each',
    'skip',
    'raises',
    'returns'
]


def insert_into_globals(runner):
    """Insert a runner's methods into the globals.

    Args:
        runner (obj:`ccino.Runner`): The runner.
    """

    for name in EXPORTED_RUNNER_METHODS:
        globals()[name] = getattr(runner, name)


def insert_into_builtins(runner):
    """Insert a runner's methods into the builtins.

    Args:
        runner (obj:`ccino.Runner`): The runner.
    """

    for name in EXPORTED_RUNNER_METHODS:
        make_builtin(getattr(runner, name), name)
