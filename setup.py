#!/usr/bin/env python
from setuptools import setup
import codecs
import os
import re

with open("requirements.txt") as f:
    required = f.read().splitlines()


with codecs.open(
        os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'nexo',
            '__init__.py'
        ), 'r', 'latin1') as fp:
    try:
        version = re.findall(r"^__version__ = '([^']+)'\r?$", fp.read(), re.M)[0]
    except IndexError:
        raise RuntimeError('Unable to determine version.')

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='python-nexo',
    version=version,
    packages=['nexo'],
    description='Nexo Pro REST API python implementation',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/guilyx/python-nexo',
    author='Erwin Lejeune',
    license='MIT',
    author_email='erwin.lejeune15@gmail.com',
    install_requires=required,
    keywords='nexo crypto exchange rest api bitcoin ethereum btc eth neo',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)