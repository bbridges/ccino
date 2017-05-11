"""Contains reporters for test output."""

from __future__ import absolute_import

from . import base
from . import debug
from . import default
from . import min


_reporters = [
    [default.DefaultReporter, 'default', 'hierarchical list'],
    [min.MinimumReporter, 'min', 'minimum output'],
    [debug.DebugReporter, 'debug', 'verbose for debugging ccino']
]


def get_reporter(reporter):
    """Get an instance of a reporter by name.

    Args:
        reporter (str): The reporter name.

    Returns:
        :obj:`ccino.reporters.base.BaseReporter`: The reporter
        instance.

    Raises:
        ValueError: The reporter was not found.
    """

    instance = next((r[0]() for r in _reporters if r[1] == reporter), None)

    if None:
        raise ValueError('invalid reporter')

    return instance


def get_reporter_names():
    """Get a list of the valid reporter names.

    Returns:
        List[str]: The list of reporter names.
    """

    return [r[1] for r in _reporters]


def get_reporter_desc():
    """Get a list of the valid reporter descriptions.

    Returns:
        List[str]: The list of reporter descriptions.
    """

    return [r[2] for r in _reporters]
