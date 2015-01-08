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

import bitcoin.core

class DogeMainParams(bitcoin.core.CoreDogeMainParams):
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

class DogeTestNetParams(bitcoin.core.CoreDogeTestNetParams):
    MESSAGE_START = b'\xfc\xc1\xb7\xdc'
    DEFAULT_PORT = 44556
    RPC_PORT = 44555
    DNS_SEEDS = (('lionservers.de', 'testdoge-seed-static.lionservers.de'))
    BASE58_PREFIXES = {'PUBKEY_ADDR':113,
                       'SCRIPT_ADDR':196,
                       'SECRET_KEY' :241}

def SelectAltcoinParams(genesis_block_hash):
    """Select the chain parameters to use

    name is one of 'mainnet', 'testnet', or 'regtest'

    Default chain is 'mainnet'
    """
    global params
    bitcoin.core._SelectCoreParams(name, coin)
    if coin == 'BTC':
        if name == 'mainnet':
            params = bitcoin.core.coreparams = MainParams()
        elif name == 'testnet':
            params = bitcoin.core.coreparams = TestNetParams()
        elif name == 'regtest':
            params = bitcoin.core.coreparams = RegTestParams()
        else:
            raise ValueError('Unknown Bitcoin chain %r' % name)
    elif coin == 'DOGE':
        if name == 'mainnet':
            params = bitcoin.core.coreparams = DogeMainParams()
        elif name == 'testnet':
            params = bitcoin.core.coreparams = DogeTestNetParams()
        else:
            raise ValueError('Unknown Dogecoin chain %r' % name)
    else:
        raise ValueError('Unknown coin %r' % coin)
