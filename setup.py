#!/usr/bin/env python

from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README')) as f:
    README = f.read()

requires = ['python-bitcoinlib']

setup(name='python-altcoinlib',
      version='0.0.1-SNAPSHOT',
      description='This python library provides an easy interface to cryptocurrency data structures and protocol.',
      long_description=README,
      classifiers=[
          "Programming Language :: Python",
      ],
      url='https://github.com/rnicoll/python-altcoinlib',
      keywords='bitcoin,dogecoin',
      packages=find_packages(),
      zip_safe=False,
      install_requires=requires,
      test_suite="altcoin.tests"
     )
