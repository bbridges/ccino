#!/usr/bin/env python

import os

try:
    from setuptools import setup, find_packages
except:
    raise Exception('setuptools is required for installation')


def join(*paths):
    """Join and normalize several paths.

    Args:
        *paths (List[str]): The paths to join and normalize.

    Returns:
        str: The normalized path.
    """

    return os.path.normpath(os.path.join(*paths))


VERSION_PATH = join(__file__, '..', 'ccino', 'version.py')
REQUIREMENTS_PATH = join(__file__, '..', 'requirements.txt')


def get_version():
    """Get the version number without running version.py.

    Returns:
        str: The current ccino version.
    """

    with open(VERSION_PATH, 'r') as version:
        out = {}

        exec(version.read(), out)

        return out['__version__']


def load_requirements():
    """Get the requirements file in this directory.

    Returns:
        List[str]: A list of pip readable strings.
    """

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
