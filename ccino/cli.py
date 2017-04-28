from __future__ import absolute_import

import os
import platform
import sys

import click

from . import main_runner
from .reporters import get_reporter_names, get_reporter_desc
from .util import load_module
from .version import __version__


DEFAULT_CONFIG = 'ccino.yml'
DEFAULT_REPORTER = 'default'


settings = {
    'help_option_names': ['-h', '--help'],
}


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return

    click.echo('ccino version {} ({} {})'.format(__version__,
            platform.python_implementation(), platform.python_version()))
    ctx.exit()


def print_reporters(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return

    reporters = zip(get_reporter_names(), get_reporter_desc())

    r_list = '\n    '.join([r[0] + ' - ' + r[1] for r in reporters])
    message = '\n    ' + r_list + '\n'

    click.echo(message)
    ctx.exit()


def check_reporter(name):
    name = name.lower()

    reporters = get_reporter_names()

    script = sys.argv[0]

    if not script.startswith('python'):
        script = os.path.basename(script)

    if not name in reporters:
        msg = '"{}"" not found. Use "{} --reporters" to list all reporters.' \
                .format(name, script)

        raise click.BadParameter(msg, param_hint='"reporter"')

    return name


@click.command(context_settings=settings, options_metavar='[options]')
@click.argument('files', nargs=-1, metavar='[files]',
        type=click.Path(exists=True, resolve_path=True))
@click.option('--bail', '-b', 'bail', flag_value='True',
        help='Stop running after a test failure. TODO')
@click.option('--no-bail', '-B', 'bail', flag_value='False',
        help='Don\'t stop running after a test failure. TODO')
@click.option('--reporter', '-R', metavar='<name>',
        help='Specify the reporter to use.')
@click.option('--no-color', '-C', 'color', flag_value='False',
        help='Force no color output. TODO')
@click.option('--recursive', '-r', count=True,
        help='Load in subdirectories. TODO')
@click.option('--config', metavar='<path>', type=click.Path(resolve_path=True),
        default=DEFAULT_CONFIG, help='Specify the config file.')
@click.option('--save', is_flag=True,
        help='Save the current options in the config file. TODO')
@click.option('--out', metavar='<file>', type=click.Path(resolve_path=True),
        help='Save the output to a file. TODO')
@click.option('--stdout', metavar='<file>', type=click.Path(resolve_path=True),
        help='Save the stdout output to a file. TODO')
@click.option('--mirror', flag_value='True',
        help='Also print the output to the console. TODO')
@click.option('--mirror-stdout', flag_value='True',
        help='Also print the stdout output to the console. TODO')
@click.option('--cover', flag_value='True',
        help='Output coverage information using coverage.py. TODO')
@click.option('--reporters', is_flag=True, callback=print_reporters,
        expose_value=False, is_eager=True,
        help='List available reporters and exit.')
@click.option('--version', '-V', is_flag=True, callback=print_version,
        expose_value=False, is_eager=True,
        help='Show the current version and exit.')
def run(files, **options):
    pass
