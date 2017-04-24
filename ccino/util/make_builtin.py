import sys


PYTHON_3 = sys.version_info[0] == 3


if PYTHON_3:
    import builtins
else:
    import __builtin__


def make_builtin(func, name=None):
    """Make a function act like a built-in function in Python.

    This is intended to be used sparingly and really only for adding
    built-in functions so that ccino test scripts don't need to
    import ccino.

    This can be used as decorator.

    Args:
        func: The function to make a built-in

    Keyword Args:
        name: The name to register the function as if needed.

    Returns:
        The same function unmodified.
    """

    if PYTHON_3:
        setattr(builtins, name or func.__name__, func)
    else:
        setattr(__builtin__, name or func.__name__, func)

    return func


def remove_builtin(name):
    """Remove a built-in function.

    Args:
        name: The function to remove
    """

    if PYTHON_3:
        delattr(builtins, name)
    else:
        delattr(__builtin__, name)
