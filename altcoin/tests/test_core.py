# Copyright (C) 2013-2014 The python-bitcoinlib developers
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

from __future__ import absolute_import, division, print_function, unicode_literals

import unittest

from altcoin.core import *
from bitcoin.core import lx, x

class Test_CAuxPow(unittest.TestCase):
    def test_deserialization(self):
        auxpow_testnet_333786 = CAuxPow.deserialize(x('02000000010000000000000000000000000000000000000000000000000000000000000000ffffffff39030464072cfabe6d6d394c537ad0e73d1f8a57a254b5473715c691cfcde79836c89ae9dc6823e61faa01000000000000001896fc0116000000000000000100f2052a010000001976a914ea89052eb52e70571a62b7fa3a7d764a753516de88ac0000000091dd3d8a296162ca8d7a54bd76344a6f8ee11759db878f892a6e497f458b9bea00000000000000000000020000001db92c00e6354176a5aeb38a2719f659ed91b848479354e9241030691de0cc19b2ae9676a9a93b5d1270a3f243cae979855e3d65691cd6002f8e17c050115306f9acb1546868031df9b7b233'))
        self.assertEqual(auxpow_testnet_333786.nIndex, 0)
        self.assertEqual(auxpow_testnet_333786.nChainIndex, 0)
        self.assertEqual(auxpow_testnet_333786.parentBlockHeader.GetHash(), lx('ea9b8b457f496e2a898f87db5917e18e6f4a3476bd547a8dca6261298a3ddd91'))

class Test_CAltcoinBlockHeader(unittest.TestCase):
    def test_serialization(self):
        auxpow = CAuxPow.deserialize(x('02000000010000000000000000000000000000000000000000000000000000000000000000ffffffff39030464072cfabe6d6d394c537ad0e73d1f8a57a254b5473715c691cfcde79836c89ae9dc6823e61faa01000000000000001896fc0116000000000000000100f2052a010000001976a914ea89052eb52e70571a62b7fa3a7d764a753516de88ac0000000091dd3d8a296162ca8d7a54bd76344a6f8ee11759db878f892a6e497f458b9bea00000000000000000000020000001db92c00e6354176a5aeb38a2719f659ed91b848479354e9241030691de0cc19b2ae9676a9a93b5d1270a3f243cae979855e3d65691cd6002f8e17c050115306f9acb1546868031df9b7b233'))
        testnet_auxpow_block = CAltcoinBlockHeader(nVersion=6422786,
                hashPrevBlock=lx('403615a0bc7b1621bca47657316a396edf6a92a31732f2c1bd787de46a0e2c84'),
                hashMerkleRoot=lx('5435db45daf1f9d923c6d0cdbb8941fdb318622274416d38a0d61ef5360cb38e'),
                nTime=1420930337,
                nBits=0x1e011a1e,
                nNonce=0x0000000,
                auxpow=auxpow)
        serialized = testnet_auxpow_block.serialize()
        testnet_auxpow_block2 = CAltcoinBlockHeader.deserialize(serialized)
        self.assertEqual(testnet_auxpow_block, testnet_auxpow_block2)

    def test_gethash(self):
        """
        Test that the AuxPoW data is NOT included in the hash
        """
        auxpow = CAuxPow.deserialize(x('02000000010000000000000000000000000000000000000000000000000000000000000000ffffffff39030464072cfabe6d6d394c537ad0e73d1f8a57a254b5473715c691cfcde79836c89ae9dc6823e61faa01000000000000001896fc0116000000000000000100f2052a010000001976a914ea89052eb52e70571a62b7fa3a7d764a753516de88ac0000000091dd3d8a296162ca8d7a54bd76344a6f8ee11759db878f892a6e497f458b9bea00000000000000000000020000001db92c00e6354176a5aeb38a2719f659ed91b848479354e9241030691de0cc19b2ae9676a9a93b5d1270a3f243cae979855e3d65691cd6002f8e17c050115306f9acb1546868031df9b7b233'))
        testnet_auxpow_block = CAltcoinBlockHeader(nVersion=6422786,
                hashPrevBlock=lx('403615a0bc7b1621bca47657316a396edf6a92a31732f2c1bd787de46a0e2c84'),
                hashMerkleRoot=lx('5435db45daf1f9d923c6d0cdbb8941fdb318622274416d38a0d61ef5360cb38e'),
                nTime=1420930307,
                nBits=0x1e013977,
                nNonce=0x0000000,
                auxpow=auxpow)
        self.assertEqual(testnet_auxpow_block.GetHash(),
                      lx('394c537ad0e73d1f8a57a254b5473715c691cfcde79836c89ae9dc6823e61faa'))

