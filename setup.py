#!/usr/bin/env python

from setuptools import setup


def load_requirements():
    with open('requirements.txt', 'r') as requirements:
        return requirements.read().split('\n')


setup(
    name='ccino',
    version='0.1-beta.1',
    author='Bradley Bridges',
    url='https://github.com/bloof-bb/ccino',
    packages=['ccino'],
    scripts=['bin/ccino'],
    install_requires=[load_requirements()],
    entry_points='''
        [console_scripts]
        ccino=ccino.cli:cli
    ''',
    license='MIT'
)
