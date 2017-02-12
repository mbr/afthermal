#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from setuptools import setup, find_packages, Extension


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


USE_CYTHON = True
try:
    import Cython
except ImportError:
    USE_CYTHON = False

ext = '.pyx' if USE_CYTHON else '.c'
extensions = [Extension('afthermal.img.floydsteinberg',
                        ['afthermal/img/floydsteinberg' + ext])]

if USE_CYTHON:
    from Cython.Build import cythonize
    extensions = cythonize(extensions)


setup(
    name='afthermal',
    version='0.3.dev1',
    description='adafruit thermal printer driver/library.',
    long_description=read('README.rst'),
    author='Marc Brinkmann',
    author_email='git@marcbrinkmann.de',
    url='http://github.com/mbr/afthermal',
    license='MIT',
    packages=find_packages(exclude=['tests']),
    install_requires=['pyserial', 'six'],
    extras_require={
        'tools': ['click'],
    },
    entry_points={
        'console_scripts': [
            'afthermal = afthermal.cli:main [tools]',
        ],
    },
    ext_modules=extensions,
)
