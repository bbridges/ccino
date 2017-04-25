#!/usr/bin/env python

import click


settings = {
    'help_option_names': ['-h', '--help'],
}


@click.command(context_settings=settings)
@click.argument('files', nargs=-1)
def run(files):
    pass
