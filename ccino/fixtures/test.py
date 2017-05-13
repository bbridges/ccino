from __future__ import absolute_import

from ..exceptions import CcinoBail, TestDidNotRaise, TestDidNotReturn, \
        UnknownSignature
from .runnable import Runnable
from ..util import get_num_args


class Test(Runnable):
    """Runnable class representing a single unit."""

    def run(self, reporter, options):
        """Run the test.

        Args:
            reporter (:obj:`ccino.reporters.base.BaseReporter`): The
                reporter to call for printing.
            options (dict): ccino runner options.

        Raises:
            :obj:`ccino.exceptions.UnknownSignature`: If func has
                an unsupported number of arguments.
            :obj:`ccino.exceptions.CcinoBail`: If the runner needs to
                stop all tests immediately.
        """

        super(Test, self).run(reporter, options)

        if self.skipped:
            reporter.base_test_pending(self)
            return

        bail = options['bail']

        num_arguments = get_num_args(self.func)

        if num_arguments > 1:
            raise UnknownSignature()

        # This custom exception can't be raised by anything else.
        class NoCustomException(Exception):
            pass

        result = None

        catch_exc = NoCustomException
        should_raise = False

        cap_return = False
        return_value = None

        # If the function is supposed to raise an exception, get it.
        if hasattr(self.func, '_raises'):
            catch_exc = self.func._raises
            should_raise = True

        # If the function is supposed to return a specific value, get
        # it.
        elif hasattr(self.func, '_returns') and \
                hasattr(self.func, '_returns_approx'):
            cap_return = True
            return_value = self.func._returns
            returns_approx = self.func._returns_approx

        try:
            # Run func and capture it's returning value.
            try:
                if num_arguments == 0:
                    result = self.func()
                else:
                    result = self.func(self)

            # If the exception is caught and it was supposed to be
            # raised. Leave the outer try block and pass. Uncaught
            # exceptions will cause the test to fail in the outer
            # try block.
            except catch_exc as e: pass
            else:
                # If it should've raised an exception, fail in the
                # outer try block.
                if should_raise:
                    raise TestDidNotRaise()

                # If it should return an approximate value, check it.
                elif cap_return and not returns_approx and \
                        not result == return_value:
                    raise TestDidNotReturn(
                        'Expected test to return {}, actual: {}'
                        .format(return_value, result)
                    )

                # If it should return a specific value, check it.
                elif cap_return and returns_approx and \
                        abs(result - return_value[0]) > return_value[1]:
                    raise TestDidNotReturn(
                        ('Expected test to return approximately {},' +
                        ' actual: {}').format(return_value[0], result)
                    )

        # If an uncaught exception occurs, the test fails.
        except Exception as e:
            reporter.base_test_fail(self)

            if bail:
                raise CcinoBail()

        # If all goes well, the test passes.
        else:
            reporter.base_test_pass(self)
