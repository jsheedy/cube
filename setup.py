#!/usr/bin/env python

try:
    from setuptools import setup
    test_extras = {
        'test_suite': 'cube.test',
    }
except ImportError:
    from distutils.core import setup
    test_extras = {}


setup(
    name='cube-engine',
    version='0.0.1',
    author='jsheedy',
    author_email='joseph.sheedy@gmail.com',
    description=( 'Cube 3D Engine'),
    platforms='any',
    packages=[
        'cube',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
    **test_extras
)
