import inspect
import sys


PYTHON_3 = sys.version_info[0] == 3


def get_func_args(func):
    """Return the names of the arguments of a function.

    This does not differentiate between positional and keyword
    arguments.

    Args:
        func: The function to analyze.

    Returns:
        List of argument names.
    """

    if PYTHON_3:
        signature = inspect.signature(func)

        return [param for param in signature.parameters]
    else:
        argspec = inspect.getargspec(func)

        return argspec.args


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
