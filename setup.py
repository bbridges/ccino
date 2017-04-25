#!/usr/bin/env python

from setuptools import setup, find_packages


def load_requirements():
    with open('requirements.txt', 'r') as requirements:
        return requirements.read().split('\n')


setup(
    name='ccino',
    version='0.1-beta.1',
    author='Bradley Bridges',
    url='https://github.com/bloof-bb/ccino',
    packages=find_packages(),
    include_package_data=True,
    # scripts=['bin/ccino'],
    install_requires=[load_requirements()],
    entry_points='''
        [console_scripts]
        ccino=ccino.cli:run
    ''',
    license='MIT'
)
