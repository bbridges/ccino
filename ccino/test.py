from __future__ import absolute_import

from .exceptions import CcinoBail, TestDidNotRaise, TestDidNotReturn
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

        class NoCustomException(Exception):
            pass

        catch_exc = NoCustomException
        should_raise = False

        cap_return = False
        return_value = None


        if hasattr(self.func, '_raises'):
            catch_exc = self.func._raises
            should_raise = True

        elif hasattr(self.func, '_returns') and \
                hasattr(self.func, '_returns_approx'):
            cap_return = True
            return_value = self.func._returns
            returns_approx = self.func._returns_approx

        try:
            try:
                if num_arguments == 0:
                    result = self.func()
                else:
                    result = self.func(self)
            except catch_exc as e: pass
            else:
                if should_raise:
                    raise TestDidNotRaise()

                elif cap_return and not returns_approx and \
                        not result == return_value:
                    raise TestDidNotReturn(
                        'Expected test to return {}, actual: {}'
                        .format(return_value, result)
                    )
                elif cap_return and returns_approx and \
                        abs(result - return_value[0]) > return_value[1]:
                    raise TestDidNotReturn(
                        ('Expected test to return approximately {},' +
                        ' actual: {}').format(return_value[0], result)
                    )
        except Exception as e:
            reporter.base_test_fail(self)

            if bail:
                raise CcinoBail()
        else:
            reporter.base_test_pass(self)
