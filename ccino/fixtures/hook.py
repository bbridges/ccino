from __future__ import absolute_import

from ..exceptions import CcinoBail, UnknownSignature
from .runnable import Runnable
from ..util import get_num_args


class Hook(Runnable):
    """Runnable class for preparing test envionrments."""

    def run(self, reporter, options):
        """Run the hook.

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

        super(Hook, self).run(reporter, options)

        if self.skipped:
            return

        # If func has one argument pass this object in.

        num_arguments = get_num_args(self.func)

        if num_arguments > 1:
            raise UnknownSignature()

        try:
            if num_arguments == 0:
                result = self.func()
            else:
                result = self.func(self)
        except Exception as e:
            reporter.base_hook_fail(self)

            # Bail if an error occured (even with the bail option set
            # to False).
            raise CcinoBail()
        else:
            reporter.base_hook_pass(self)
