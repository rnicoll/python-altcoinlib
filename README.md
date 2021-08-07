# python-altcoinlib

This Python 3 library provides a wrapper around Peter Todd's python-bitcoinlib,
extending it in order to add altcoin support (initially Dogecoin). Please
consult python-bitcoinlib's documentation for an API overview.

## Requirements

This is intended to work with Python 3. You will hit issues if you try to use Python 2.
As a hint, if you are on Ubuntu, you may want to install the `python-is-python3` package
to ensure Python 3 is the default.

You will need to install python-bitcoinlib first, from https://github.com/petertodd/python-bitcoinlib
To do this you should clone the repository to a new folder, then run its setup.py. For example:

```
git clone https://github.com/petertodd/python-bitcoinlib.git
cd python-bitcoinlib
sudo ./setup.py install
```

## Installation

To install the library, run `setup.py`, as in `sudo ./setup.py install`.

## Unit tests

Under altcoin/tests are unit tests based on data extracted from Dogecoin blockchains. To
run the tests:

python -m unittest discover
python3 -m unittest discover
