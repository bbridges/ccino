from __future__ import absolute_import


class Runnable(object):
    def __init__(self):
        self._skip = False

    def run(self, reporter):
        self.execute_func(reporter)

    def execute_func(self, reporter):
        raise Exception('Not implemented')

    def skip(self):
        self._skip = True

    def unskip(self):
        self._skip = False

    @property
    def skipped(self):
        return self._skip
