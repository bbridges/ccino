from __future__ import absolute_import


class Runnable(object):
    def __init__(self, func, parent, name=None):
        self._parent = parent
        self._name = name or func.__name__

        self._skip = False

    def run(self, reporter, bail):
        raise NotImplementedError()

    def skip(self):
        self._skip = True

    def unskip(self):
        self._skip = False

    @property
    def parent(self):
        return self._parent

    @property
    def name(self):
        return self._name

    @property
    def skipped(self):
        return self._skip
