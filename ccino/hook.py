from __future__ import absolute_import

from .runnable import Runnable
from .util import get_num_args


class Hook(Runnable):
    def __init__(self, func, desc=None):
        super(Hook, self).__init__()

        self._func = func
        self._desc = desc or func.__name__

    def execute_func(self, reporter):
        if self._skip:
            return

        num_arguments = get_num_args(self._func)

        if num_arguments > 1:
            raise Exception('Number of function arguments not supported')

        try:
            if num_arguments == 0:
                result = self._func()
            else:
                result = self._func(self)
        except Exception as e:
            reporter.base_hook_fail(self)
        else:
            reporter.base_hook_pass(self)
