from __future__ import absolute_import

import platform
import sys

import click

from . import main_runner
from .reporters import get_reporter_names, get_reporter_desc
from .util import load_module
from .version import __version__


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


def click_exception(message):
    click.echo(err=True)

    raise click.ClickException(message)


@click.command(context_settings=settings, options_metavar='[options]')
@click.argument('files', nargs=-1, metavar='[files]',
        type=click.Path(exists=True, resolve_path=True))
@click.option('--bail', '-b', count=True,
        help='Stop running after a test failure.')
@click.option('--reporter', '-R', metavar='<name>',
        help='Specify the reporter to use.')
@click.option('--recursive', '-r', count=True,
        help='Load in subdirectories.')
@click.option('--config', metavar='<file>', help='Specify the config file.')
@click.option('--save', is_flag=True,
        help='Save the current options in the calling directory.')
@click.option('--reporters', is_flag=True, callback=print_reporters,
        expose_value=False, is_eager=True,
        help='List available reporters and exit.')
@click.option('--version', '-V', is_flag=True, callback=print_version,
        expose_value=False, is_eager=True,
        help='Show the current version and exit.')
def run(files, **options):
    pass
