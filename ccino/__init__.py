"""A Python testing framework inspired by Mocha."""

from __future__ import absolute_import

from .runner import Runner
from .runner import insert_into_globals as _insert_globals
from .version import __version__


main_runner = Runner()

_insert_globals(main_runner)
