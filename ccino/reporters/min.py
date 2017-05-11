from __future__ import absolute_import

from .base import BaseReporter, override


class MinimumReporter(BaseReporter):
    """Reporter with minimal output.

    Only the summary is shown after tests are completed.
    """

    @override
    def end(self, time):
        self.write('\n')
        self.print_summary()
        self.write('\n')
