from __future__ import absolute_import

from .exceptions import CcinoBail
from .runnable import Runnable
from .util import get_num_args


class Hook(Runnable):
    def run(self, reporter, options):
        super(Hook, self).run(reporter, options)

        if self.skipped:
            return

        num_arguments = get_num_args(self.func)

        if num_arguments > 1:
            raise Exception('Number of function arguments not supported')

        try:
            if num_arguments == 0:
                result = self.func()
            else:
                result = self.func(self)
        except Exception as e:
            reporter.base_hook_fail(self)

            raise CcinoBail()
        else:
            reporter.base_hook_pass(self)
