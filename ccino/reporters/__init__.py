from __future__ import absolute_import

from . import base
from . import debug
from . import default

_reporters = {
    'base': base.BaseReporter,
    'debug': debug.DebugReporter,
    'default': default.DefaultReporter
}


def get_reporter(reporter):
    return _reporters[reporter]()


def get_reporter_names():
    return list(_reporters.keys())
