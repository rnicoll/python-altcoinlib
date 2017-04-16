#!/usr/bin/env python

from setuptools import setup, find_packages
import os

from altcoin import __version__

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README')) as f:
    README = f.read()

requires = ['python-bitcoinlib>=0.7.0']

setup(name='python-altcoinlib',
      version=__version__,
      description='This python library provides an easy interface to cryptocurrency data structures and protocol.',
      long_description=README,
      classifiers=[
          "Programming Language :: Python",
          "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
      ],
      url='https://github.com/rnicoll/python-altcoinlib',
      keywords='bitcoin,litecoin,dogecoin',
      packages=find_packages(),
      zip_safe=False,
      install_requires=requires,
      test_suite="altcoin.tests"
     )
