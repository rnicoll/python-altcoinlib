#!/usr/bin/env python3

# Copyright (C) 2015 The python-altcoinlib developers
#
# This file is part of python-bitcoinalt.
#
# It is subject to the license terms in the LICENSE file found in the top-level
# directory of this distribution.
#
# No part of python-bitcoinlib, including this file, may be copied, modified,
# propagated, or distributed except according to the terms contained in the
# LICENSE file.

"""Burns any Dogecoin inputs below 1 DOGE"""

import sys
import os.path

import altcoin
from altcoin.rpc import AltcoinProxy
from bitcoin.core import *
from bitcoin.core.script import *

def burn_txins(rpc, quantity, txins):
    burn_script = CScript(
        [
            OP_RETURN, 'I <3 Dogecoin'
        ]
    )

    burn_quantity = quantity / 2.0 # We burn half, and give half to the miners
    # Sign and relay a transaction burning the inputs
    txouts = [CTxOut(burn_quantity, burn_script)]
    tx = CMutableTransaction(txins, txouts)
    tx_signed = rpc.signrawtransaction(tx)
    if not tx_signed['complete']:
        raise Error('Transaction came back without all inputs signed.')
    rpc.sendrawtransaction(tx_signed['tx'])
    print 'Burnt ' + str(quantity / COIN) + ' DOGE in TX ID ' + b2lx(tx_signed['tx'].GetHash())

# Select Dogecoin test network
altcoin.SelectParams('bb0a78264637406b6360aad926284d544d7049f45189db5664f3c4d07350559e')

rpc = AltcoinProxy(service_port=44555, btc_conf_file=os.path.expanduser('~/.dogecoin/dogecoin.conf'))
txins = []
quantity = 0
for txout in rpc.listunspent(0):
    if txout['amount'] <= COIN:
        txins.append(CMutableTxIn(txout['outpoint']))
        quantity += txout['amount']
        if len(txins) > 100:
            burn_txins(rpc, quantity, txins)
            txins = []
            quantity = 0

if len(txins) > 0:
    burn_txins(rpc, quantity, txins)
