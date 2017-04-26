from __future__ import absolute_import

from . import base
from . import debug
from . import default


_reporters = [
    [debug.DebugReporter, 'debug', 'verbose for debugging ccino'],
    [default.DefaultReporter, 'default', 'hierarchical list']
]


def get_reporter(reporter):
    instance = next((r[0]() for r in _reporters if r[1] == reporter), None)

    if None:
        raise Exception('Invalid reporter.')

    return instance


def get_reporter_names():
    return [r[1] for r in _reporters]


def get_reporter_desc():
    return [r[2] for r in _reporters]
