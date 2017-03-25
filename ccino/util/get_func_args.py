import inspect
import sys


PYTHON_3 = sys.version_info[0] == 3


def get_num_args(func):
    """Return the number of arguments of a function.

    Args:
        func: The function to analyze.

    Returns:
        Number of arguments.
    """

    if PYTHON_3:
        signature = inspect.signature(func)

        return len(signature.parameters)
    else:
        argspec = inspect.getargspec(func)

        return len(argspec.args)
