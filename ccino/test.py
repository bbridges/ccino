from __future__ import absolute_import

from .exceptions import CcinoBail
from .runnable import Runnable
from .util import get_num_args


class Test(Runnable):
    def run(self, reporter, options):
        super(Test, self).run(reporter, options)

        if self.skipped:
            reporter.base_test_pending(self)
            return

        bail = options['bail']

        num_arguments = get_num_args(self.func)
        result = None

        if num_arguments > 1:
            raise Exception('Number of function arguments not supported')

        try:
            if num_arguments == 0:
                result = self.func()
            else:
                result = self.func(self)
        except Exception as e:
            reporter.base_test_fail(self)

            if bail:
                raise CcinoBail()
        else:
            if hasattr(self.func, '_returns'):
                return_value = self.func._returns

                if self.func._returns_approx and \
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
