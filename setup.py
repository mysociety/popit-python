#!/usr/bin/env python

from setuptools import setup

setup(name='PopIt-Python',
    version='0.1.10',
    description='Python bindings to connect to the PopIt API',
        long_description=open('README', 'rt').read(),
    author='mySociety',
    author_email='modules@mysociety.org',
    url='https://github.com/mysociety/popit-python',
    py_modules=['popit_api'],
    install_requires=['requests==0.14.2','slumber']
)
