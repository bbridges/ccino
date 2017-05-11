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
    """Format seconds in a short string.

    Args:
        seconds (float): The seconds to format.

    Returns:
        str: The formatted string.
    """

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


def override(func):
    """Override a BaseReporter method.

    This will put the appropriate doc in the function so it does not
    have to be repeated.

    Args:
        func (Callable): The overriding function.

    Returns:
        Callable: The same function with updated doc.
    """

    doc = getattr(BaseReporter, func.__name__).__doc__

    func.__doc__ = doc

    return func


class BaseReporter(object):
    """The base reporter in which all others derive from.

    This is not intended to be used as a normal reporter, however
    doing so will not cause an error, simply nothing will be
    outputted.

    Other reporters need to subclass this and provide functionality
    for the printing methods:
        ``start``
        ``suite_start``
        ``suite_end``
        ``test_pass``
        ``test_fail``
        ``test_pending``
        ``hook_pass``
        ``hook_fail``
        ``end``

    When overriding those methods they should have an ``override``
    decorator with them to attached the original doc from this class.

    For printing subclasses should use the ``write`` method and
    should not print directly.

    Attributes:
        num_suites (int): The total number of suites reported.
        num_open_suites (int): The number of open suites.
        num_tests (int): The total number of tests reported.
        num_passes (int): The total number of tests passed.
        num_pending (int): The total number of tests pending.
        num_failures (int): The total number of test failures.
        open_suites (List[`ccino.suite.Suite`]): The list of open
            suites.
        errors (List[str]): The list of error tracebacks.
    """

    def __init__(self):
        """Create a new BaseReporter.

        For most purposes this does not need to be subclassed.
        Variable initialization should happen in an overriding
        ``start`` method.
        """

        self._stream = sys.stdout
        self._mirror = False
        self._force_color = False
        self._exc_context = False

        self._terminal = None

        self.num_suites = 0
        self.num_open_suites = 0
        self.num_tests = 0
        self.num_passes = 0
        self.num_pending = 0
        self.num_failures = 0

        self.open_suites = []
        self.errors = []

    def color(self, use_color=None):
        """Force color output.

        A value of None will make the reporter print color to
        terminals but not to files.

        Keyword Args:
            use_color (:obj:`str` or :obj:`None`): Whether or not to
                force color output. Defaults to None.
        """

        if use_color == False:
            self._force_color = None
        elif use_color == True:
            self._force_color = True
        elif use_color == None:
            self._force_color = False
        else:
            raise TypeError('use_color must be bool or None')

    def output(self, stream):
        """Specify the output stream.

        Args:
            stream (:obj:`io.IOBase`): The output stream.
        """

        self._stream = stream

    def write(self, string):
        """Write to the output stream.

        Args:
            string (str): The string to output.
        """

        if self._stream:
            self._stream.write(string)

    def mirror(self, on=True):
        """Mirror the output to stdout.

        Keyword Args:
            on (bool): Whether or not to mirror. Defaults to True.
        """

        self._mirror = on

    def exc_context(self, show=True):
        """Print traceback context if possible.

        Keyword Args:
            show (bool): Whether or not to mirror. Defaults to True.
        """

        self._exc_context = show

    def _get_last_exception(self):
        """Get the last exception in a formatted traceback.

        The tracebacks here read backwards from normal Python
        tracebacks, i.e. the deepest calling frame appears at the
        top.

        The tracebacks are formatted similarly to NodeJS tracebacks.

        Returns:
            str: The formatted traceback.
        """

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
        """Handle starting tests."""

        self._terminal = blessings.Terminal(
            stream=self._stream, force_styling=self._force_color
        )

        self.start()

    def base_suite_start(self, suite):
        """Handle a starting suite.

        Args:
            suite (:obj:`ccino.suite.Suite`): The suite that started.
        """

        if not suite.is_root:
            self.num_suites += 1
            self.num_open_suites += 1

            self.open_suites.append(suite.name)

        self.suite_start(suite)

    def base_suite_end(self, suite):
        """Handle an ending suite.

        Args:
            suite (:obj:`ccino.suite.Suite`): The suite that ended.
        """

        self.num_open_suites -= 1

        if not suite.is_root:
            self.open_suites.pop()

        self.suite_end(suite)

    def base_test_pass(self, test):
        """Handle a passing test.

        Args:
            suite (:obj:`ccino.test.Test`): The test that passed.
        """

        self.num_passes += 1

        self.test_pass(test)

    def base_test_fail(self, test):
        """Handle a failing test.

        Args:
            suite (:obj:`ccino.test.Test`): The test that failed.
        """

        self.num_failures += 1

        self.errors.append((test, self._get_last_exception()))

        self.test_fail(test)

    def base_test_pending(self, test):
        """Handle a pending test.

        Args:
            suite (:obj:`ccino.test.Test`): The test that is pending.
        """

        self.num_pending += 1

        self.test_pending(test)

    def base_hook_pass(self, hook):
        """Handle a passing hook.

        Args:
            suite (:obj:`ccino.hook.Hook`): The hook that passed.
        """

        self.hook_pass(hook)

    def base_hook_fail(self, hook):
        """Handle a failing hook.

        Args:
            suite (:obj:`ccino.hook.Hook`): The hook that failed.
        """

        self.num_failures += 1

        self.errors.append((test, self._get_last_exception()))

        self.hook_fail(hook)

    def base_end(self, time):
        """Handle ending tests.

        Args:
            time (float): Amount of time elapsed.
        """

        self.time = time

        self.end(time)

    def start(self):
        """Print before all tests."""

        pass

    def suite_start(self, suite):
        """Print when a suite starts.

        Args:
            suite (:obj:`ccino.suite.Suite`): The suite that started.
        """

        pass

    def suite_end(self, suite):
        """Print when a suite ends.

        Args:
            suite (:obj:`ccino.suite.Suite`): The suite that ended.
        """

        pass

    def test_pass(self, test):
        """Print when a test passes.

        Args:
            suite (:obj:`ccino.test.Test`): The test that passed.
        """

        pass

    def test_fail(self, test):
        """Print when a test fails.

        Args:
            suite (:obj:`ccino.test.Test`): The test that failed.
        """

        pass

    def test_pending(self, test):
        """Print when a test is pending.

        Args:
            suite (:obj:`ccino.test.Test`): The test that is pending.
        """

        pass

    def hook_pass(self, hook):
        """Print when a hook passes.

        Args:
            suite (:obj:`ccino.hook.Hook`): The hook that passed.
        """

        pass

    def hook_fail(self, hook):
        """Print when a hook fails.

        Args:
            suite (:obj:`ccino.hook.Hook`): The hook that failed.
        """

        pass

    def end(self, time):
        """Print after all tests are finished.

        Args:
            time (float): Amount of time elapsed.
        """

        pass

    def print_summary(self):
        """Print out a summary for all tests run."""

        # If any tests passed, print out how many and how long they
        # took.
        if self.num_passes:
            passes = self.terminal.green(
                '  {:d} passing'.format(self.num_passes)
            )

            time = self.terminal.bright_black(
                '({:s})'.format(format_seconds_short(self.time))
            )

            self.write(passes + ' ' + time + '\n')

        # If any tests are pending, print out how many.
        if self.num_pending:
            self.write(self.terminal.cyan(
                '  {:d} passing\n'.format(self.num_pending)
            ))

        # If any tests failed, print out how many.
        if self.num_failures:
            self.write(self.terminal.red(
                '  {:d} failing\n'.format(self.num_failures)
            ))

        # Print out exceptions in the order they happened.
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
        """:obj:`blessings.Terminal`: The terminal instance
        associated with the output stream.
        """

        return self._terminal
