#!/usr/bin/env python3

# Copyright (C) 2015 The python-altcoinlib developers
#
# This file is part of python-altcoinlib
#
# It is subject to the license terms in the LICENSE file found in the top-level
# directory of this distribution.
#
# No part of python-bitcoinlib, including this file, may be copied, modified,
# propagated, or distributed except according to the terms contained in the
# LICENSE file.

"""Pull the latest block in from a Litecoin testnet client"""

import sys
import os.path

import altcoin
from altcoin.rpc import AltcoinProxy
from bitcoin.core import lx

altcoin.SelectParams('f5ae71e26c74beacc88382716aced69cddf3dffff24f384e1808905e0188f68f')

rpc = AltcoinProxy(service_port=19332, btc_conf_file=os.path.expanduser('~/.litecoin/litecoin.conf'))
best_block_hash = rpc.getblockchaininfo()['bestblockhash']
print rpc.getblock(lx(best_block_hash))
