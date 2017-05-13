from __future__ import absolute_import

from ..exceptions import AlreadyRunnableException


class Runnable(object):
    """Base class that ccino runnable objects inherit from.

    Subclasses should override the run method (and should call this
    class' run method as well) so they can provide functionality.

    This class checks to make sure a function cannot be assigned to
    multiple Runnable objects.
    """

    def __init__(self, func, parent=None, name=None):
        """Create a new Runnable.

        Args:
            func (Callable): The function to run.

        Keyword Args:
            parent (:obj:`ccino.fixtures.Runnable` or :obj:`None`):
                The parent runnable.
            name (str): The name of the runnable.

        Raises:
            :obj:`ccino.exceptions.AlreadyRunnableException`: If a
                runnable has already been made with func.
        """

        if func is not None:
            if hasattr(func, '_is_runnable') and \
                    func._is_runnable == True:
                raise AlreadyRunnableException()

            func._is_runnable = True

        self._func = func
        self._parent = parent
        self._name = name or func.__name__

        self._skip = False

    def run(self, reporter, options):
        """Run the runnable.

        Note:
            This function simply checks if the function has a
            ``'_skip'`` attribute and does not actually run the
            function. This needs to be overriden for actual
            functionality.

        Args:
            reporter (:obj:`ccino.reporters.base.BaseReporter`): The
                reporter to call for printing.
            options (dict): ccino runner options.
        """

        if not self.skipped and hasattr(self.func, '_skip') and \
                self.func._skip == True:
            self.skip()

    def skip(self):
        """Skip the runnable."""
        self._skip = True

    @property
    def func(self):
        """Callable: The function to be exectuted on run."""
        return self._func

    @property
    def parent(self):
        """:obj:`ccino.fixtures.Runnable` or :obj:`None`: The parent
        runnable.
        """

        return self._parent

    @parent.setter
    def parent(self, runnable):
        self._parent = runnable

    @property
    def name(self):
        """str: The name of the runnable."""
        return self._name

    @property
    def skipped(self):
        """bool: Whether or not the runnable has been skipped."""
        return self._skip
