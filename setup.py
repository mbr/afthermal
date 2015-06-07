#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='afthermal',
    version='0.1.dev1',
    description='',
    long_description=read('README.rst'),
    author='Marc Brinkmann',
    author_email='git@marcbrinkmann.de',
    url='http://github.com/mbr/afthermal',
    license='MIT',
    packages=find_packages(exclude=['tests']),
    install_requires=['pyserial', 'six'],
    entry_points={
        'console_scripts': [
            'commandname = package:func',
        ],
        'gui_scripts': [
            'commandname = package:func',
        ]
    }
)
