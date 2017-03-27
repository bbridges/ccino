from __future__ import absolute_import

from functools import wraps
from inspect import isfunction

from .get_func_args import get_func_args


def combine_args(dec):
    """Wrap a decorator so it doesn't have to return another.

    This decorator simplies others and makes the other decorator able
    to accept the function to be wrapped and the other aguments
    entered at the same time.

    The input decorator must accept a function as its first argument.
    This is the function that will be wrapped. After this, it may
    accept as many positional or keyword arguments as needed. If the
    function can be called with only one argument (the function),
    then the decorator can be used without parenthesis or with empty
    parenthesis with the Python decorator notation before the
    function definition as seen in the examples below.

    Args:
        dec: The decorator to wrap.

    Returns:
        The wrapped decorator.

    Examples:
        >>> @combine_args
        >>> def wrap(func, one=1, two=2):
        >>>     func()
        >>>
        >>>     print('one: ' + str(one))
        >>>     print('two: ' + str(two))
        >>>
        >>> @wrap
        >>> def a():
        >>>     print('in a()')
        in a()
        one: 1
        two: 2
        >>> @wrap()
        >>> def a():
        >>>     print('in b()')
        in b()
        one: 1
        two: 2
        >>> @wrap('cat')
        >>> def c():
        >>>     print('in c()')
        in c()
        one: cat
        two: 2
        >>> @wrap(one='cat')
        >>> def d():
        >>>     print('in d()')
        in d()
        one: cat
        two: 2
    """

    @wraps(dec)
    def wrapped_dec(*args, **kwargs):
        # If the function was provided, return the decorator with all
        # the arguments.
        #
        # Otherwise, return another decorator which
        # accepts the function and then returns the original
        # decorator with all the arguments.

        if (len(args) > 0 and isfunction(args[0])) or \
                get_func_args(dec)[0] in kwargs:
            return dec(*args, **kwargs)

        def inner_wrap(func):
            added_args = (func, ) + args

            return dec(*added_args, **kwargs)

        return inner_wrap

    return wrapped_dec
