from __future__ import absolute_import

import os
import platform
import sys

import click
import coverage
import yaml

from . import main_runner
from .reporters import get_reporter_names, get_reporter_desc
from .runner import insert_into_globals, insert_into_builtins
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


def to_bool(value):
    if type(value) == 'bool':
        return value

    if str(value) == 'True':
        return True

    if str(value) == 'False':
        return False

    raise ValueError('value must be \'True\' or \'False\' or a bool')


def load_dir(path, recursive):
    loaded = 0

    for inner_path in os.listdir(path):
        inner_path = os.path.join(path, inner_path)

        if os.path.isfile(inner_path) and inner_path.endswith('.py'):
            load_module(inner_path)
            loaded += 1
        elif os.path.isdir(inner_path) and recursive:
            loaded += load_dir(inner_path, recursive)

    return loaded


@click.command(context_settings=settings, options_metavar='[options]')
@click.argument('files', nargs=-1, metavar='[files]',
        type=click.Path(exists=True, resolve_path=True))
# @click.option('--verbose', '-v', count=True, help='Increase verbosity.')
@click.option('--bail', '-b', 'bail', flag_value='True',
        help='Stop running after a test failure.')
@click.option('--no-bail', '-B', 'bail', flag_value='False',
        help='Don\'t stop running after a test failure.')
@click.option('--reporter', '-R', metavar='<name>',
        help='Specify the reporter to use.')
@click.option('--color', '-c', 'color', flag_value='True',
        help='Force color output.')
@click.option('--no-color', '-C', 'color', flag_value='False',
        help='Force no color output.')
@click.option('--recursive', '-r', flag_value='True',
        help='Load in subdirectories.')
@click.option('--no-builtins', 'builtins', flag_value='False',
        help='Don\'t add ccino functions to the builtins.')
@click.option('--config', metavar='<file>',
        type=click.Path(exists=True, resolve_path=True),
        help='Specify the config file.')
@click.option('--no-config', flag_value='True',
        help="Do not use a config file.")
@click.option('--out', metavar='<file>', type=click.Path(resolve_path=True),
        help='Save the output to a file.')
@click.option('--stdout', metavar='<file>', type=click.Path(resolve_path=True),
        help='Save the stdout output to a file.')
# @click.option('--mirror', flag_value='True',
#         help='Also print the output to the console.')
# @click.option('--mirror-stdout', flag_value='True',
#         help='Also print the stdout output to the console.')
@click.option('--exc-context', flag_value='True',
        help='Show context in stack trace if possible.')
@click.option('--cover', flag_value='True',
        help='Output coverage information using coverage.py.')
@click.option('--reporters', is_flag=True, callback=print_reporters,
        expose_value=False, is_eager=True,
        help='List available reporters and exit.')
@click.option('--version', '-V', is_flag=True, callback=print_version,
        expose_value=False, is_eager=True,
        help='Show the current version and exit.')
def run(files, **options):
    open_files = []

    if options['config'] is None:
        options['config'] = DEFAULT_CONFIG

    use_config = options['no_config'] is None or \
            not to_bool(options['no_config'])

    if use_config and os.path.isfile(options['config']):
        config_file = click.open_file(options['config'], 'r+')
        config = yaml.load(config_file.read())

        if files == tuple() and 'source' in config:
            source = config['source']

            files = source if type(source) == 'list' else [source]

        if options['bail'] is None and 'bail' in config:
            options['bail'] = config['bail']

        if options['reporter'] is None and 'reporter' in config:
            options['reporter'] = config['reporter']

        if options['color'] is None and 'color' in config:
            options['color'] = config['color']

        if options['recursive'] is None and 'recursive' in config:
            options['recursive'] = config['recursive']

        if options['out'] is None and 'out' in config:
            options['out'] = config['out']

        if options['stdout'] is None and 'stdout' in config:
            options['stdout'] = config['stdout']

        if options['exc_context'] is None and 'exc_context' in config:
            options['exc_context'] = config['exc_context']

        if options['builtins'] is None and 'builtins' in config:
            options['builtins'] = config['builtins']

        open_files.append(config_file)

    if files == tuple():
        files = ['test']

    if options['bail'] is not None:
        bail = to_bool(options['bail'])

        main_runner.bail(bail)

    if options['reporter'] is not None:
        reporter = check_reporter(options['reporter'])

        main_runner.reporter(reporter)

    if options['color'] is not None:
        use_color = to_bool(options['color'])

        main_runner.color(use_color)

    if options['out'] is not None:
        out = click.open_file(options['out'], 'w')

        main_runner.output(out)
        open_files.append(out)

    if options['stdout'] is not None:
        stdout = click.open_file(options['stdout'], 'w')

        main_runner.stdout(stdout)
        open_files.append(stdout)

    if options['exc_context'] is not None:
        exc_context = to_bool(options['exc_context'])

        main_runner.exc_context(exc_context)

    insert_into_globals(main_runner)

    if options['builtins'] is None:
        insert_into_builtins(main_runner)

    cov = None
    success = True

    if options['cover'] is not None:
        cov = coverage.Coverage()
        cov.start()

    recursive = options['recursive'] is not None and \
            to_bool(options['recursive'])

    loaded = 0

    for path in files:
        if os.path.isfile(path):
            load_module(path)
            loaded += 1
        elif os.path.isdir(path):
            loaded += load_dir(path, recursive)

    if loaded == 0:
        click.echo('No test files found.')
        return

    try:
        success = main_runner.run_tests()
    except Exception as e:
        if cov is not None:
            cov.stop()

        raise Exception('Unknown error while running tests.')
    else:
        if cov is not None:
            cov.stop()
            cov.save()

            cov.html_report()

        if not success:
            sys.exit(1)
    finally:
        for file in open_files:
            file.close()
