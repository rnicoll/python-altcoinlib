# Copyright (C) 2007 Jan-Klaas Kollhof
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

"""Genericised cryptocurrency reference client RPC support"""

from __future__ import absolute_import, division, print_function,\
    unicode_literals

from altcoin.core import CAltcoinBlock
from bitcoin.rpc import unhexlify, JSONRPCError, Proxy
from bitcoin.core import b2lx

DEFAULT_HTTP_TIMEOUT = 30


class AltcoinProxy(Proxy):
    def __init__(self, service_url=None,
                 service_port=None,
                 btc_conf_file=None,
                 timeout=DEFAULT_HTTP_TIMEOUT,
                 **kwargs):
        """Create a proxy to a bitcoin-like RPC service

        Unlike RawProxy data is passed as objects, rather than JSON. (not yet
        fully implemented) Assumes Bitcoin Core version >= 0.9; older versions
        mostly work, but there are a few incompatibilities.

        If service_url is not specified the username and password are read out
        of the file btc_conf_file. If btc_conf_file is not specified
        ~/.bitcoin/bitcoin.conf or equivalent is used by default. The default
        port is set according to the chain parameters in use: mainnet, testnet,
        or regtest.

        Usually no arguments to Proxy() are needed; the local bitcoind will be
        used.

        timeout - timeout in seconds before the HTTP interface times out
        """
        super(Proxy, self).__init__(service_url=service_url,
                                    service_port=service_port,
                                    btc_conf_file=btc_conf_file,
                                    timeout=timeout,
                                    **kwargs)

    def getblock(self, block_hash):
        """Get block <block_hash>

        Raises IndexError if block_hash is not valid.
        """
        try:
            block_hash = b2lx(block_hash)
        except TypeError:
            raise TypeError(
                '%s.getblock(): block_hash must be bytes; got %r instance' %
                (self.__class__.__name__, block_hash.__class__))
        try:
            r = self._call('getblock', block_hash, False)
        except JSONRPCError as ex:
            raise IndexError('%s.getblock(): %s (%d)' %
                             (self.__class__.__name__, ex.error['message'],
                              ex.error['code']))
        return CAltcoinBlock.deserialize(unhexlify(r))

__all__ = (
    'AltcoinProxy',
)
