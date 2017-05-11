"""ccino module entry point."""

from __future__ import absolute_import

import sys

from .cli import run


if __name__ == '__main__':
    # Make Click print out 'python -m ccino' instead of '__main__.py'
    # when the ccino module is run
    sys.argv[0] = 'python -m ccino'

    # Run the command line interface
    run()
