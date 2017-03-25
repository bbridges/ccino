import sys


PYTHON_3 = sys.version_info[0] == 3


if PYTHON_3:
    import builtins
else:
    import __builtin__


def make_builtin(func):
    """Make a function act like a built-in function in Python.

    This is intended to be used sparingly and really only for adding
    built-in functions so that ccino test scripts don't need to
    import ccino.

    This can be used as decorator.

    Args:
        func: The function to make a built-in

    Returns:
        The same function unmodified.
    """

    if PYTHON_3:
        setattr(builtins, func.__name__, func)
    else:
        setattr(__builtin__, func.__name__, func)

    return func
