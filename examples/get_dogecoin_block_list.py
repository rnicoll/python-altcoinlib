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

"""Take a list of block heights and return block from Dogecoin testnet client"""

import sys
from os.path import expanduser

import altcoin
from altcoin.rpc import AltcoinProxy

altcoin.SelectParams(
    'bb0a78264637406b6360aad926284d544d7049f45189db5664f3c4d07350559e')

rpc = AltcoinProxy(service_port=44555,
                   btc_conf_file=expanduser('~/.dogecoin/dogecoin.conf'))

for block_height in sys.argv[1:]:
    print (rpc.getblock(rpc.getblockhash(int(block_height))))
