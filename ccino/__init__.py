from __future__ import absolute_import

from functools import wraps

from .runner import Runner
from .util import make_builtin


EXPORTED_RUNNER_METHODS = [
    'suite',
    'test',
    'suite_setup',
    'suite_teardown',
    'setup',
    'teardown',
    'describe',
    'it'
]

main_runner = Runner()


def insert_into_globals(runner):
    for name in EXPORTED_RUNNER_METHODS:
        globals()[name] = getattr(runner, name)


def insert_into_builtins(runner):
    for name in EXPORTED_RUNNER_METHODS:
        make_builtin(getattr(runner, name), name)


def load_module(module_path):
    load_module(module_path)


insert_into_globals(main_runner)
insert_into_builtins(main_runner)
