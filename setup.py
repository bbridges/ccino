#!/usr/bin/env python

import os

from setuptools import setup, find_packages


def join(*args):
    return os.path.normpath(os.path.join(*args))


VERSION_PATH = join(__file__, '..', 'ccino', 'version.py')
REQUIREMENTS_PATH = join(__file__, '..', 'requirements.txt')

def get_version():
    with open(VERSION_PATH, 'r') as version:
        out = {}

        exec(version.read(), out)

        return out['__version__']


def load_requirements():
    with open(REQUIREMENTS_PATH, 'r') as requirements:
        return requirements.read().split('\n')


setup(
    name='ccino',
    version=get_version(),
    author='Bradley Bridges',
    url='https://github.com/bloof-bb/ccino',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[load_requirements()],
    entry_points='''
        [console_scripts]
        ccino=ccino.cli:run
    ''',
    license='MIT'
)
