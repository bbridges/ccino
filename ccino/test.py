from __future__ import absolute_import

from .exceptions import CcinoBail
from .runnable import Runnable
from .util import get_num_args


class Test(Runnable):
    def __init__(self, func, parent, name=None):
        super(Test, self).__init__(func, parent, name)

        self._func = func

    def run(self, reporter, bail):
        if self._skip:
            reporter.base_test_pending(self)
            return

        num_arguments = get_num_args(self._func)
        result = None

        if num_arguments > 1:
            raise Exception('Number of function arguments not supported')

        try:
            if num_arguments == 0:
                result = self._func()
            else:
                result = self._func(self)
        except Exception as e:
            reporter.base_test_fail(self)

            if bail:
                raise CcinoBail()
        else:
            if hasattr(self._func, '_returns'):
                return_value = self._func._returns

                if self._func._returns_approx and \
                        abs(result - return_value[0]) > return_value[1]:
                    try:
                        raise Exception(
                            'Expected test to return approximately {return},' +
                            ' actual: {}'.format(return_value[0], result)
                        )
                    except Exception as e:
                        reporter.base_test_fail(self)

                        if bail:
                            raise CcinoBail()

                elif not result == return_value:
                    e = Exception(
                        'Expected test to return {}, actual: {}'
                        .format(return_value, result)
                    )

                    reporter.base_test_fail(self)

                    if bail:
                        raise CcinoBail()
                else:
                    reporter.base_test_pass(self)
            else:
                reporter.base_test_pass(self)
