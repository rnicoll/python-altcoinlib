# Copyright (C) 2011 Sam Rushing
# Copyright (C) 2012-2014 The python-bitcoinlib developers
# Copyright (C) 2015 The python-altcoinlib developers
#
# This file is part of python-bitcoinlib.
#
# It is subject to the license terms in the LICENSE file found in the top-level
# directory of this distribution.
#
# No part of python-bitcoinlib, including this file, may be copied, modified,
# propagated, or distributed except according to the terms contained in the
# LICENSE file.

import ctypes
import ctypes.util
import sys

from bitcoin.core.key import CECKey, _ssl

# CECKey with added support for key generation
class AltcoinECKey(CECKey):
    def __init__(self):
	CECKey.__init__(self)

    def __del__(self):
        CECKey.__del__(self)

    def get_secretbytes(self):
        global _ssl

        secret = _ssl.EC_KEY_get0_private_key(self.k)
        mb = ctypes.create_string_buffer(32)
        size = _ssl.BN_bn2bin(secret, mb)
        if size == 32:
          return mb.raw
        else:
          # Move the data into a zero-padded buffer of 32 bytes
          padding = 32 - size
          new_buffer = ctypes.create_string_buffer(32)
          for idx in range(0, padding):
              new_buffer[idx] = "\x00"
          for idx in range(padding, 32):
              new_buffer[idx] = mb[idx - padding]
          return new_buffer.raw

    def generate(self):
        global _ssl

        _ssl.EC_KEY_generate_key(self.k)
        return self.k

__all__ = (
        'AltcoinECKey',
)
