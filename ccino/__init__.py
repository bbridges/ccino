from __future__ import absolute_import

from .runner import Runner, insert_into_globals, insert_into_builtins
from .version import __version__


main_runner = Runner()

insert_into_globals(main_runner)
