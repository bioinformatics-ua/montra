#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup


setup(
    name='emif-fb',
    version='0.1-dev',
    description='EMIF FB',
    long_description=open('README.md', 'r').read(),
    packages=[
        'emif',
    ],
    zip_safe=False,
    #install_requires=[
    #    'mimeparse',
    #    'python-dateutil >= 1.5, != 2.0',
    #],
    tests_require=['mock'],
)
