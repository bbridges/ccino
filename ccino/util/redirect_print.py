import sys


PYTHON_3_4 = sys.version_info[0] == 3 and sys.version_info[1] >= 4


if PYTHON_3_4:
    from contextlib import redirect_stdout
else:
    from contextlib import contextmanager


redirect_print = None


if PYTHON_3_4:
    redirect_print = redirect_stdout
else:
    @contextmanager
    def redirect_stdout(new_target):
        """Redirect stdout to a steam.

        This is meant as a replacement for contextlib.redirect_stdout
        for use before Python 3.4.

        Args:
            new_target: The stream to send stdout text to.
        """

        old_target, sys.stdout = sys.stdout, new_target

        try:
            yield
        finally:
            sys.stdout = old_target

    redirect_print = redirect_stdout
