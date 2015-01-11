# Copyright (C) 2011-2015 The python-bitcoinlib developers
# Copyright (C) 2015 The python-altcoinlib developers
#
# This file is part of python-altcoinlib.
#
# It is subject to the license terms in the LICENSE file found in the top-level
# directory of this distribution.
#
# No part of python-altcoinlib, including this file, may be copied, modified,
# propagated, or distributed except according to the terms contained in the
# LICENSE file.

from altcoin.core import CoreDogeMainParams, CoreDogeTestNetParams, _SelectCoreParams
from bitcoin.core import b2lx
import bitcoin

class DogeMainParams(CoreDogeMainParams):
    MESSAGE_START = b'\xc0\xc0\xc0\xc0'
    DEFAULT_PORT = 22556
    RPC_PORT = 22555
    DNS_SEEDS = (('dogecoin.com', 'seed.dogecoin.com'),
                 ('mophides.com', 'seed.mophides.com'),
                 ('dglibrary.org', 'seed.dglibrary.org'),
                 ('dogechain.info', 'seed.dogechain.info'))
    BASE58_PREFIXES = {'PUBKEY_ADDR':30,
                       'SCRIPT_ADDR':22,
                       'SECRET_KEY' :158}

class DogeTestNetParams(CoreDogeTestNetParams):
    MESSAGE_START = b'\xfc\xc1\xb7\xdc'
    DEFAULT_PORT = 44556
    RPC_PORT = 44555
    DNS_SEEDS = (('lionservers.de', 'testdoge-seed-static.lionservers.de'))
    BASE58_PREFIXES = {'PUBKEY_ADDR':113,
                       'SCRIPT_ADDR':196,
                       'SECRET_KEY' :241}

available_params = {}

def SelectParams(genesis_block_hash):
    """Select the chain parameters to use

    genesis_block_hash is the hash of block 0, used to uniquely identify chains
    """
    global available_params
    _SelectCoreParams(genesis_block_hash)
    if genesis_block_hash in available_params:
        bitcoin.params = available_params[genesis_block_hash]
    else:
        raise ValueError('Unknown blockchain %r' % genesis_block_hash)

# Initialise the available_params list
for current_params in [
      # Can't use Bitcoin main net injection because python-bitcoinlib
      # doesn't associate the genesis block with its params
      # bitcoin.MainParams(),
      bitcoin.TestNetParams(),
      DogeMainParams(),
      DogeTestNetParams()
  ]:
  available_params[b2lx(current_params.GENESIS_BLOCK.GetHash())] = current_params


__all__ = (
        'DogeMainParams',
        'DogeTestNetParams',
        'SelectParams',
)