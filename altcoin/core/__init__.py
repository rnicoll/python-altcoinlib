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

class CAuxPow(CTransaction):
    __slots__ = ['vChainMerkleBranch', 'nChainIndex', 'parentBlockHeader']

    def __init__(self, vin=(), vout=(), nLockTime=0, nVersion=1, vChainMerkleBranch=(), nChainIndex=0, parentBlockHeader=None):
        super(CBlock, self).__init__(vin, vout, nLockTime, nVersion)
        object.__setattr__(self, 'vin', vChainMerkleBranch)
        object.__setattr__(self, 'nChainIndex', nChainIndex)
        object.__setattr__(self, 'parentBlockHeader', parentBlockHeader)

    @classmethod
    def stream_deserialize(cls, f):
        self = super(CTransaction, cls).stream_deserialize(f)
        # nVersion = this->nVersion;
        # READWRITE(vChainMerkleBranch);
        # READWRITE(nChainIndex);
        return cls(vin, vout, nLockTime, nVersion)

    def stream_serialize(self, f):
        super(CTransaction, cls).stream_serialize(f)
        # nVersion = this->nVersion;
        # READWRITE(vChainMerkleBranch);
        # READWRITE(nChainIndex);


class CAltcoinBlockHeader(CBlockHeader):
    """A block header with optional AuxPoW support"""
    __slots__ = ['auxpow']

    def __init__(self, nVersion=2, hashPrevBlock=b'\x00'*32, hashMerkleRoot=b'\x00'*32, nTime=0, nBits=0, nNonce=0, auxPow=None):
        object.__setattr__(self, 'nVersion', nVersion)
        assert len(hashPrevBlock) == 32
        object.__setattr__(self, 'hashPrevBlock', hashPrevBlock)
        assert len(hashMerkleRoot) == 32
        object.__setattr__(self, 'hashMerkleRoot', hashMerkleRoot)
        object.__setattr__(self, 'nTime', nTime)
        object.__setattr__(self, 'nBits', nBits)
        object.__setattr__(self, 'nNonce', nNonce)
        object.__setattr__(self, 'auxpow', auxpow)

    @classmethod
    def stream_deserialize(cls, f):
        self = super(CBlockHeader, cls).stream_deserialize(f)
        nVersion = struct.unpack(b"<i", ser_read(f,4))[0]
        hashPrevBlock = ser_read(f,32)
        hashMerkleRoot = ser_read(f,32)
        nTime = struct.unpack(b"<I", ser_read(f,4))[0]
        nBits = struct.unpack(b"<I", ser_read(f,4))[0]
        nNonce = struct.unpack(b"<I", ser_read(f,4))[0]
        # FIXME: Parse auxpow
        # object.__setattr__(self, 'auxpow', auxpow)
        return self

    def stream_serialize(self, f):
        super(CBlockHeader, cls).stream_serialize(f)
        # Write out the AuxPow

    @staticmethod
    def calc_difficulty(nBits):
        # FIXME: Handle alternative difficulty calculation methods such as
        # Dogecoin's
        CBlockHeader.calc_difficulty(nBits)
    difficulty = property(lambda self: CAltcoinBlockHeader.calc_difficulty(self.nBits))

    def __repr__(self):
        return "%s(%i, lx(%s), lx(%s), %s, 0x%08x, 0x%08x)" % \
                (self.__class__.__name__, self.nVersion, b2lx(self.hashPrevBlock), b2lx(self.hashMerkleRoot),
                 self.nTime, self.nBits, self.nNonce)

class CAltcoinBlock(CAltcoinBlockHeader, CBlock):
    """A block including all transactions in it"""
    __slots__ = ['vtx', 'vMerkleTree']

    def __init__(self, nVersion=2, hashPrevBlock=b'\x00'*32, hashMerkleRoot=b'\x00'*32, nTime=0, nBits=0, nNonce=0, vtx=()):
        """Create a new block"""
        super(CAltcoinBlockHeader, self).__init__(nVersion, hashPrevBlock, hashMerkleRoot, nTime, nBits, nNonce)

        vMerkleTree = tuple(CBlock.build_merkle_tree_from_txs(vtx))
        object.__setattr__(self, 'vMerkleTree', vMerkleTree)
        object.__setattr__(self, 'vtx', tuple(CTransaction.from_tx(tx) for tx in vtx))

    @classmethod
    def stream_deserialize(cls, f):
        self = super(CAltcoinBlockHeader, cls).stream_deserialize(f)

        vtx = VectorSerializer.stream_deserialize(CTransaction, f)
        vMerkleTree = tuple(CBlock.build_merkle_tree_from_txs(vtx))
        object.__setattr__(self, 'vMerkleTree', vMerkleTree)
        object.__setattr__(self, 'vtx', tuple(vtx))

        return self

    def stream_serialize(self, f):
        super(CAltcoinBlockHeader, self).stream_serialize(f)
        VectorSerializer.stream_serialize(CTransaction, self.vtx, f)

    def get_header(self):
        """Return the block header

        Returned header is a new object.
        """
        return CBlockHeader(nVersion=self.nVersion,
                            hashPrevBlock=self.hashPrevBlock,
                            hashMerkleRoot=self.hashMerkleRoot,
                            nTime=self.nTime,
                            nBits=self.nBits,
                            nNonce=self.nNonce,
                            auxpow=self.auxpow)

class CoreDogeMainParams(CoreChainParams):
    NAME = 'dogecoin_main'
    GENESIS_BLOCK = CAltcoinBlock.deserialize(x('010000000000000000000000000000000000000000000000000000000000000000000000696ad20e2dd4365c7459b4a4a5af743d5e92c6da3229e6532cd605f6533f2a5b24a6a152f0ff0f1e678601000101000000010000000000000000000000000000000000000000000000000000000000000000ffffffff1004ffff001d0104084e696e746f6e646fffffffff010058850c020000004341040184710fa689ad5023690c80f3a49c8f13f8d45b8c857fbcbc8bc4a8e4d3eb4b10f4d4604fa08dce601aaf0f470216fe1b51850b4acf21b179c45070ac7b03a9ac00000000'))
    SUBSIDY_HALVING_INTERVAL = 100000
    PROOF_OF_WORK_LIMIT = 2**256-1 >> 32

class CoreDogeTestNetParams(CoreDogeMainParams):
    NAME = 'dogecoin_test'
    GENESIS_BLOCK = CAltcoinBlock.deserialize(x('010000000000000000000000000000000000000000000000000000000000000000000000696ad20e2dd4365c7459b4a4a5af743d5e92c6da3229e6532cd605f6533f2a5bb9a7f052f0ff0f1ef7390f000101000000010000000000000000000000000000000000000000000000000000000000000000ffffffff1004ffff001d0104084e696e746f6e646fffffffff010058850c020000004341040184710fa689ad5023690c80f3a49c8f13f8d45b8c857fbcbc8bc4a8e4d3eb4b10f4d4604fa08dce601aaf0f470216fe1b51850b4acf21b179c45070ac7b03a9ac00000000'))

ALTCOIN_PARAMS = [
    CoreMainParams(),
    CoreTestNetParams(),
    CoreRegTestParams(),
    CoreDogeMainParams(),
    CoreDogeTestNetParams()
]
ALTCOINS = {}

def _SelectAltcoinCoreParams(genesis_block_hash):
    global ALTCOINS

    """Select the core chain parameters to use

    Don't use this directly, use bitcoin.SelectParams() instead so both
    consensus-critical and general parameters are set properly.
    """
    global coreparams
    if genesis_block_hash in ALTCOINS:
        coreparams = ALTCOINS[genesis_block_hash]
    else
        raise ValueError('Unknown blockchain %r' % genesis_block_hash)

# Initialise the altcoins list
for params in ALTCOIN_PARAMS:
  ALTCOINS[b2lx(params.GENESIS_BLOCK.GetHash())] = params

