# Copyright (C) 2012-2014 The python-bitcoinlib developers
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

import struct

import bitcoin.core
from bitcoin.core import b2lx, b2x, lx, x
from bitcoin.core.serialize import *

BLOCK_VERSION_DEFAULT = 1 << 0
BLOCK_VERSION_AUXPOW = 1 << 8

class MerkleHash(object):
    __slots__ = ['merkleHash']
  
    def __init__(self, merkleHash=0):
        object.__setattr__(self, 'merkleHash', merkleHash)

    @classmethod
    def stream_deserialize(cls, f):
        merkleHash = ser_read(f,32)
        return cls(merkleHash)

    def stream_serialize(self, f):
        f.write(self.merkleHash)
    def __repr__(self):
        return "lx(%s)" % (b2lx(self.merkleHash))

class CAuxPow(bitcoin.core.CTransaction):
    """
    AuxPoW component of the block header, for chains which support it.
    Note that in the reference client this inherits from CMerkleTx, and
    as this library has no equivalent the CMerkleTx fields are instead
    added directly here.
    """
    __slots__ = ['hashBlock', 'vMerkleBranch', 'nIndex', 'vChainMerkleBranch', 'nChainIndex', 'parentBlockHeader']

    def __init__(self, vin=(), vout=(), nLockTime=0, nVersion=1, hashBlock=0, vMerkleBranch=None, nIndex=0, vChainMerkleBranch=(), nChainIndex=0, parentBlockHeader=None):
        super(CAuxPow, self).__init__(vin, vout, nLockTime, nVersion)
        object.__setattr__(self, 'hashBlock', hashBlock)
        object.__setattr__(self, 'vMerkleBranch', vMerkleBranch)
        object.__setattr__(self, 'nIndex', nIndex)
        object.__setattr__(self, 'vChainMerkleBranch', vChainMerkleBranch)
        object.__setattr__(self, 'nChainIndex', nChainIndex)
        object.__setattr__(self, 'parentBlockHeader', parentBlockHeader)

    @classmethod
    def stream_deserialize(cls, f):
        self = super(CAuxPow, cls).stream_deserialize(f)

        hashBlock = ser_read(f,32)
        vMerkleBranch = uint256VectorSerializer.stream_deserialize(f)
        nIndex = struct.unpack(b"<I", ser_read(f,4))[0]
        vChainMerkleBranch = uint256VectorSerializer.stream_deserialize(f)
        nChainIndex = struct.unpack(b"<I", ser_read(f,4))[0]
        parentBlockHeader = CAltcoinBlockHeader.stream_deserialize(f)

        object.__setattr__(self, 'hashBlock', hashBlock)
        object.__setattr__(self, 'vMerkleBranch', vMerkleBranch)
        object.__setattr__(self, 'nIndex', nIndex)
        object.__setattr__(self, 'vChainMerkleBranch', vChainMerkleBranch)
        object.__setattr__(self, 'nChainIndex', nChainIndex)
        object.__setattr__(self, 'parentBlockHeader', parentBlockHeader)

        return self

    def stream_serialize(self, f):
        super(CAuxPow, self).stream_serialize(f)
        f.write(self.hashBlock)
        uint256VectorSerializer.stream_serialize(self.vMerkleBranch, f)
        f.write(struct.pack(b"<I", self.nIndex))
        uint256VectorSerializer.stream_serialize(self.vChainMerkleBranch, f)
        f.write(struct.pack(b"<I", self.nChainIndex))
        self.parentBlockHeader.stream_serialize(f)

    def __repr__(self):
        return "%s(%r, %r, %i, %i, lx(%s), %r, %i, %r, %i, %r)" % \
                (self.__class__.__name__, self.vin, self.vout, self.nLockTime, self.nVersion, b2lx(self.hashBlock),
                 self.vMerkleBranch, self.nIndex, self.vChainMerkleBranch, self.nChainIndex, self.parentBlockHeader)


class CAltcoinBlockHeader(bitcoin.core.CBlockHeader):
    """A block header with optional AuxPoW support"""
    __slots__ = ['auxpow']

    def __init__(self, nVersion=2, hashPrevBlock=b'\x00'*32, hashMerkleRoot=b'\x00'*32, nTime=0, nBits=0, nNonce=0, auxpow=None):
        super(CAltcoinBlockHeader, self).__init__(nVersion, hashPrevBlock, hashMerkleRoot, nTime, nBits, nNonce)
        object.__setattr__(self, 'auxpow', auxpow)

    @classmethod
    def stream_deserialize(cls, f):
        self = super(CAltcoinBlockHeader, cls).stream_deserialize(f)

        if (self.nVersion & BLOCK_VERSION_AUXPOW):
          auxpow = CAuxPow.stream_deserialize(f)
        else:
          auxpow = None
        object.__setattr__(self, 'auxpow', auxpow)

        return self

    def stream_serialize(self, f):
        super(CAltcoinBlockHeader, self).stream_serialize(f)
        if (self.nVersion & BLOCK_VERSION_AUXPOW):
          self.auxpow.stream_serialize(f)

    @staticmethod
    def calc_difficulty(nBits):
        # FIXME: Handle alternative difficulty calculation methods such as
        # Dogecoin's
        bitcoin.core.CBlockHeader.calc_difficulty(nBits)
    difficulty = property(lambda self: CAltcoinBlockHeader.calc_difficulty(self.nBits))

    def __repr__(self):
        return "%s(%i, lx(%s), lx(%s), %s, 0x%08x, 0x%08x, %s)" % \
                (self.__class__.__name__, self.nVersion, b2lx(self.hashPrevBlock), b2lx(self.hashMerkleRoot),
                 self.nTime, self.nBits, self.nNonce, self.auxpow)

    def GetHash(self):
        """Return the block hash

        Note that this is the hash of the header without any AuxPoW data,
        not the entire serialized block.
        """
        return bitcoin.core.CBlockHeader(nVersion=self.nVersion,
                            hashPrevBlock=self.hashPrevBlock,
                            hashMerkleRoot=self.hashMerkleRoot,
                            nTime=self.nTime,
                            nBits=self.nBits,
                            nNonce=self.nNonce).GetHash()

class CAltcoinBlock(CAltcoinBlockHeader):
    """A block including all transactions in it"""
    __slots__ = ['vtx', 'vMerkleTree']

    def calc_merkle_root(self):
        """Calculate the merkle root

        The calculated merkle root is not cached; every invocation
        re-calculates it from scratch.
        """
        if not len(self.vtx):
            raise ValueError('Block contains no transactions')
        return self.build_merkle_tree_from_txs(self.vtx)[-1]

    def __init__(self, nVersion=2, hashPrevBlock=b'\x00'*32, hashMerkleRoot=b'\x00'*32, nTime=0, nBits=0, nNonce=0, auxpow=None, vtx=()):
        """Create a new block"""
        super(CAltcoinBlock, self).__init__(nVersion, hashPrevBlock, hashMerkleRoot, nTime, nBits, nNonce, auxpow)

        vMerkleTree = tuple(bitcoin.core.CBlock.build_merkle_tree_from_txs(vtx))
        object.__setattr__(self, 'vMerkleTree', vMerkleTree)
        object.__setattr__(self, 'vtx', tuple(CTransaction.from_tx(tx) for tx in vtx))

    @classmethod
    def stream_deserialize(cls, f):
        self = super(CAltcoinBlock, cls).stream_deserialize(f)

        vtx = VectorSerializer.stream_deserialize(bitcoin.core.CTransaction, f)
        vMerkleTree = tuple(bitcoin.core.CBlock.build_merkle_tree_from_txs(vtx))
        object.__setattr__(self, 'vMerkleTree', vMerkleTree)
        object.__setattr__(self, 'vtx', tuple(vtx))

        return self

    def stream_serialize(self, f):
        super(CAltcoinBlock, self).stream_serialize(f)
        VectorSerializer.stream_serialize(CTransaction, self.vtx, f)

    def get_header(self):
        """Return the block header

        Returned header is a new object.
        """
        return CAltcoinBlockHeader(nVersion=self.nVersion,
                            hashPrevBlock=self.hashPrevBlock,
                            hashMerkleRoot=self.hashMerkleRoot,
                            nTime=self.nTime,
                            nBits=self.nBits,
                            nNonce=self.nNonce,
                            auxpow=self.auxpow)
    def __repr__(self):
        return "%s(%i, lx(%s), lx(%s), %s, 0x%08x, 0x%08x, %s, vMerkleTree(%s), vtx(%s))" % \
                (self.__class__.__name__, self.nVersion, b2lx(self.hashPrevBlock), b2lx(self.hashMerkleRoot),
                 self.nTime, self.nBits, self.nNonce, self.auxpow, self.vMerkleTree, self.vtx)

    def GetHash(self):
        """Return the block hash

        Note that this is the hash of the header without any AuxPoW data,
        not the entire serialized block.
        """
        try:
            return self._cached_GetHash
        except AttributeError:
            _cached_GetHash = bitcoin.core.CBlockHeader(nVersion=self.nVersion,
                            hashPrevBlock=self.hashPrevBlock,
                            hashMerkleRoot=self.hashMerkleRoot,
                            nTime=self.nTime,
                            nBits=self.nBits,
                            nNonce=self.nNonce).GetHash()
            object.__setattr__(self, '_cached_GetHash', _cached_GetHash)
            return _cached_GetHash

class CoreDogeMainParams(bitcoin.core.CoreChainParams):
    NAME = 'dogecoin_main'
    GENESIS_BLOCK = CAltcoinBlock.deserialize(x('010000000000000000000000000000000000000000000000000000000000000000000000696ad20e2dd4365c7459b4a4a5af743d5e92c6da3229e6532cd605f6533f2a5b24a6a152f0ff0f1e678601000101000000010000000000000000000000000000000000000000000000000000000000000000ffffffff1004ffff001d0104084e696e746f6e646fffffffff010058850c020000004341040184710fa689ad5023690c80f3a49c8f13f8d45b8c857fbcbc8bc4a8e4d3eb4b10f4d4604fa08dce601aaf0f470216fe1b51850b4acf21b179c45070ac7b03a9ac00000000'))
    SUBSIDY_HALVING_INTERVAL = 100000
    PROOF_OF_WORK_LIMIT = 2**256-1 >> 20

class CoreDogeTestNetParams(CoreDogeMainParams):
    NAME = 'dogecoin_test'
    GENESIS_BLOCK = CAltcoinBlock.deserialize(x('010000000000000000000000000000000000000000000000000000000000000000000000696ad20e2dd4365c7459b4a4a5af743d5e92c6da3229e6532cd605f6533f2a5bb9a7f052f0ff0f1ef7390f000101000000010000000000000000000000000000000000000000000000000000000000000000ffffffff1004ffff001d0104084e696e746f6e646fffffffff010058850c020000004341040184710fa689ad5023690c80f3a49c8f13f8d45b8c857fbcbc8bc4a8e4d3eb4b10f4d4604fa08dce601aaf0f470216fe1b51850b4acf21b179c45070ac7b03a9ac00000000'))

class CoreLtcMainParams(bitcoin.core.CoreChainParams):
    NAME = 'litecoin_main'
    GENESIS_BLOCK = CAltcoinBlock.deserialize(x('010000000000000000000000000000000000000000000000000000000000000000000000d9ced4ed1130f7b7faad9be25323ffafa33232a17c3edf6cfd97bee6bafbdd97b9aa8e4ef0ff0f1ecd513f7c0101000000010000000000000000000000000000000000000000000000000000000000000000ffffffff4804ffff001d0104404e592054696d65732030352f4f63742f32303131205374657665204a6f62732c204170706c65e280997320566973696f6e6172792c2044696573206174203536ffffffff0100f2052a010000004341040184710fa689ad5023690c80f3a49c8f13f8d45b8c857fbcbc8bc4a8e4d3eb4b10f4d4604fa08dce601aaf0f470216fe1b51850b4acf21b179c45070ac7b03a9ac00000000'))
    SUBSIDY_HALVING_INTERVAL = 840000
    PROOF_OF_WORK_LIMIT = 2**256-1 >> 20

class CoreLtcTestNetParams(CoreLtcMainParams):
    NAME = 'litecoin_test'
    GENESIS_BLOCK = CAltcoinBlock.deserialize(x('010000000000000000000000000000000000000000000000000000000000000000000000d9ced4ed1130f7b7faad9be25323ffafa33232a17c3edf6cfd97bee6bafbdd97f6028c4ef0ff0f1e38c3f6160101000000010000000000000000000000000000000000000000000000000000000000000000ffffffff4804ffff001d0104404e592054696d65732030352f4f63742f32303131205374657665204a6f62732c204170706c65e280997320566973696f6e6172792c2044696573206174203536ffffffff0100f2052a010000004341040184710fa689ad5023690c80f3a49c8f13f8d45b8c857fbcbc8bc4a8e4d3eb4b10f4d4604fa08dce601aaf0f470216fe1b51850b4acf21b179c45070ac7b03a9ac00000000'))


available_core_params = {}

def _SelectCoreParams(genesis_block_hash):
    """Select the core chain parameters to use

    Don't use this directly, use bitcoin.SelectParams() instead so both
    consensus-critical and general parameters are set properly.
    """

    global available_core_params
    if genesis_block_hash in available_core_params:
        bitcoin.core.coreparams = available_core_params[genesis_block_hash]
    else:
        raise ValueError('Unknown blockchain %r' % genesis_block_hash)

# Initialise the altcoins list
for params in [
      bitcoin.core.CoreMainParams(),
      bitcoin.core.CoreTestNetParams(),
      bitcoin.core.CoreRegTestParams(),
      CoreLtcMainParams(),
      CoreLtcTestNetParams(),
      CoreDogeMainParams(),
      CoreDogeTestNetParams()
  ]:
  available_core_params[b2lx(params.GENESIS_BLOCK.GetHash())] = params
    

__all__ = (
        'MerkleHash',
        'CAuxPow',
        'CAltcoinBlockHeader',
        'CAltcoinBlock',
        'CoreDogeMainParams',
        'CoreDogeTestNetParams',
        'CoreLtcMainParams',
        'CoreLtcTestNetParams',
        '_SelectCoreParams',
)
