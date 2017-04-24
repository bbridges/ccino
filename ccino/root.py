from __future__ import absolute_import

from .suite import Suite


class RootSuite(Suite):
    def __init__(self):
        super(RootSuite, self).__init__(None, 'root')

    @property
    def is_root(self):
        return True

    @property
    def level(self):
        return 0
