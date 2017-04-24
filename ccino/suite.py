from __future__ import absolute_import

from .runnable import Runnable


class Suite(Runnable):
    def __init__(self, func, name=None):
        super(Suite, self).__init__()

        self._func = func
        self._name = name or func.__name__

        self._tests = []
        self._suite_setups = []
        self._suite_teardowns = []
        self._setups = []
        self._teardowns = []

    def add_test(self, test):
        self._tests.append(test)

    def add_suite(self, suite):
        self._tests.append(suite)

        for setup in self._setups:
            suite.add_setup(setup)

        for teardown in self._teardowns:
            suite.add_teardown(teardown)

    def add_suite_setup(self, hook):
        self._suite_setups.append(hook)

    def add_suite_teardown(self, hook):
        self._suite_teardowns.append(hook)

    def add_setup(self, hook):
        self._setups.append(hook)

        for test in self._tests:
            is_suite = isinstance(test, Suite)

            if is_suite:
                test.add_setup(hook)

    def add_teardown(self, hook):
        self._teardowns.append(hook)

        for test in self._tests:
            is_suite = isinstance(test, Suite)

            if is_suite:
                test.add_teardown(hook)

    def execute_func(self, reporter):
        reporter.base_suite_start(self)

        for suite_setup in self._suite_setups:
            suite_setup.run(reporter)

        for test in self._tests:
            is_suite = isinstance(test, Suite)

            if not is_suite:
                for setup in self._setups:
                    setup.run(reporter)

            test.run(reporter)

            if not is_suite:
                for teardown in self._teardowns:
                    teardown.run(reporter)

        for suite_teardown in self._suite_teardowns:
            suite_teardown.run(reporter)

        reporter.base_suite_end(self)

    def load(self):
        self._func()

    @property
    def is_root(self):
        return False

    @property
    def name(self):
        return self._name
