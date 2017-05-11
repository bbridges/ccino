from __future__ import absolute_import

from .runnable import Runnable


class Suite(Runnable):
    def __init__(self, func, parent, name=None):
        super(Suite, self).__init__(func, parent, name)

        self._func = func

        self._tests = []
        self._suite_setups = []
        self._suite_teardowns = []
        self._setups = []
        self._teardowns = []

    def add_test(self, test):
        self._tests.append(test)

    def add_suite(self, suite):
        self._tests.append(suite)

    def add_suite_setup(self, hook):
        self._suite_setups.append(hook)

    def add_suite_teardown(self, hook):
        self._suite_teardowns.append(hook)

    def add_setup(self, hook):
        self._setups.append(hook)

    def add_teardown(self, hook):
        self._teardowns.append(hook)

    def run(self, reporter, bail):
        super(Suite, self).run(reporter, bail)

        reporter.base_suite_start(self)

        if not self.skipped:
            for suite_setup in self._suite_setups:
                suite_setup.run(reporter, bail)

        for test in self._tests:
            is_suite = isinstance(test, Suite)

            open_suites = [self]

            while open_suites[-1].parent is not None:
                open_suites.append(open_suites[-1].parent)

            if not is_suite and not self.skipped:
                for suite in reversed(open_suites):
                    for setup in suite._setups:
                        setup.run(reporter, bail)

            if self.skipped:
                test.skip()

            test.run(reporter, bail)

            if not is_suite and not self.skipped:
                for suite in reversed(open_suites):
                    for teardown in suite._teardowns:
                        teardown.run(reporter, bail)

        if not self.skipped:
            for suite_teardown in self._suite_teardowns:
                suite_teardown.run(reporter, bail)

        reporter.base_suite_end(self)

    def load(self):
        self._func()

    @property
    def is_root(self):
        return False
