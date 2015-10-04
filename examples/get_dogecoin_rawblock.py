#!/usr/bin/env python3

# Copyright (C) 2015 The python-altcoinlib developers
#
# This file is part of python-altcoinlib.
#
# It is subject to the license terms in the LICENSE file found in the top-level
# directory of this distribution.
#
# No part of python-bitcoinlib, including this file, may be copied, modified,
# propagated, or distributed except according to the terms contained in the
# LICENSE file.

"""Take a list of blocks and deserializes them"""

import sys

from altcoin.core import CAltcoinBlock
from bitcoin.core import x

for block in sys.argv[1:]:
    print (CAltcoinBlock.deserialize(x(block)))
