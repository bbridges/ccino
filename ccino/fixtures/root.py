from __future__ import absolute_import

from .suite import Suite


class RootSuite(Suite):
    """Root suite for a ccino Runner.

    Note:
        Only one of these should exist.
    """

    def __init__(self):
        """Create a new RootSuite."""
        super(RootSuite, self).__init__(None, None, 'root')

    @property
    def is_root(self):
        """bool: This is always True for a RootSuite."""
        return True
