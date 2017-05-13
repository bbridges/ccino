from __future__ import absolute_import

from ..exceptions import UnknownSignature
from .runnable import Runnable
from ..util import get_num_args


class Suite(Runnable):
    """Runnable class that contains tests, hooks, and other suites.

    Tests are added with the ``add_test`` method, hooks are added
    with the ``add_suite_setup``, ``add_suite_teardown``,
    ``add_setup``, and ``add_teardown`` methods, and suites are added
    with the ``add_suite`` method.
    """

    def __init__(self, func, parent=None, name=None):
        """Create a new Suite.

        Args:
            func (Callable): The function to run.

        Keyword Args:
            parent (:obj:`ccino.fixtures.Runnable` or :obj:`None`):
                The parent runnable.
            name (str): The name of the suite.

        Raises:
            :obj:`ccino.exceptions.AlreadyRunnableException`: If a
                runnable has already been made with func.
        """

        super(Suite, self).__init__(func, parent, name)

        self._func = func

        self._tests = []
        self._suite_setups = []
        self._suite_teardowns = []
        self._setups = []
        self._teardowns = []

    def add_test(self, test):
        """Add a test to the suite.

        Each test will have all setup and teardown hooks run before
        and when the suite is run.

        Args:
            test (:obj:`ccino.fixtures.Test`): The test to add.
        """

        test.parent = self
        self._tests.append(test)

    def add_suite_setup(self, hook):
        """Add a suite setup Hook to the suite.

        This will run at the beginning of the run sequence.

        Args:
            hook (:obj:`ccino.fixtures.Hook`): The hook to add.
        """

        hook.parent = self
        self._suite_setups.append(hook)

    def add_suite_teardown(self, hook):
        """Add a suite teardown Hook to the suite.

        This will run at the end of the run sequence.

        Args:
            hook (:obj:`ccino.fixtures.Hook`): The hook to add.
        """

        hook.parent = self
        self._suite_teardowns.append(hook)

    def add_setup(self, hook):
        """Add a setup Hook to the suite.

        This will run before each test in the suite.

        Args:
            hook (:obj:`ccino.fixtures.Hook`): The hook to add.
        """

        hook.parent = self
        self._setups.append(hook)

    def add_teardown(self, hook):
        """Add a teardown Hook to the suite.

        This will run after each test in the suite.

        Args:
            hook (:obj:`ccino.fixtures.Hook`): The hook to add.
        """

        hook.parent = self
        self._teardowns.append(hook)

    def add_suite(self, suite):
        """Add a another suite inside the suite.

        The suites will with the tests.

        Args:
            hook (:obj:`ccino.fixtures.Suite`): The suite to add.
        """

        suite.parent = self
        self._tests.append(suite)

    def run(self, reporter, options):
        """Run the suite.

        The running order is the following:
        1. Suite setup hooks are run in the order they are added.
        2. If the suite contains no tests go to 8.
        3. If the next test is a suite, run it and go to 7.
        4. Setup hooks are run in the order they are added starting
           with the highest level suites.
        5. The test is run.
        6. Teardown hooks are run in the order they are added
           starting with the highest level suites.
        7. Read in the next test and go to 3.
        8. Suite teardown hooks are run in the order they are added.

        Args:
            reporter (:obj:`ccino.reporters.base.BaseReporter`): The
                reporter to call for printing.
            options (dict): ccino runner options.

        Raises:
            :obj:`ccino.exceptions.UnknownSignature`: If a test
                inside has an unsupported number of function
                arguments.
            :obj:`ccino.exceptions.CcinoBail`: If the runner needs to
                stop all tests immediately.
        """

        super(Suite, self).run(reporter, options)

        reporter.base_suite_start(self)

        if not self.skipped:
            for suite_setup in self._suite_setups:
                suite_setup.run(reporter, options)

        for test in self._tests:
            is_suite = isinstance(test, Suite)

            open_suites = [self]

            while open_suites[-1].parent is not None:
                open_suites.append(open_suites[-1].parent)

            if not is_suite and not self.skipped:
                for suite in reversed(open_suites):
                    for setup in suite._setups:
                        setup.run(reporter, options)

            if self.skipped:
                test.skip()

            test.run(reporter, options)

            if not is_suite and not self.skipped:
                for suite in reversed(open_suites):
                    for teardown in suite._teardowns:
                        teardown.run(reporter, options)

        if not self.skipped:
            for suite_teardown in self._suite_teardowns:
                suite_teardown.run(reporter, options)

        reporter.base_suite_end(self)

    def load(self):
        """Run func to allow fixtures to be added inside.

        Raises:
            :obj:`ccino.exceptions.UnknownSignature`: If func has
                an unsupported number of arguments.
        """

        num_arguments = get_num_args(self.func)

        if num_arguments > 1:
            raise UnknownSignature()

        if num_arguments == 0:
            result = self.func()
        else:
            result = self.func(self)

    @property
    def is_root(self):
        """bool: True if this is the root suite, otherwise False."""
        return False
