# -*- coding: utf-8 -*-

"""
This file is part of PyZ80.

PyZ80 is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

PyZ80 is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
Lesser GNU General Public License for more details.

You should have received a copy of the Lesser GNU General Public License
along with PyZ80. If not, see <http://www.gnu.org/licenses/>.

Copyright 2014 Lucas Liendo.
"""

from .load_group_8_bit import (
    LoadRegisterRegisterRR, LoadRegisterRegisterPP,
    LoadRegisterRegisterQQ, LoadRegisterRNumber,
    LoadRegisterPNumber, LoadRegisterQNumber,
    LoadIndirectAddressHLRegister, LoadIndirectAddressIXRegister,
    LoadIndirectAddressIYRegister, LoadIndirectAddressHLNumber,
    LoadIndirectAddressIXNumber, LoadIndirectAddressIYNumber,
    LoadAIndirectAddressBC, LoadAIndirectAddressDE, LoadAIndirectAddressNN,
    LoadRegisterIndirectHL, LoadRegisterIndirectIX, LoadRegisterIndirectIY
)


class InstructionDecoder(object):
    """
    This object is responsible to filter the instruction that
    is going to be executed and fetch its operands.
    """
    def __init__(self, z80):
        self._z80 = z80
        self._instructions = self._build_instructions()

    def _build_instructions(self):
        instructions = self._build_8_bit_load_group()

        return instructions

    def _build_8_bit_load_group(self):
        return [
            LoadRegisterRegisterRR(self._z80),
            LoadRegisterRegisterPP(self._z80),
            LoadRegisterRegisterQQ(self._z80),
            LoadRegisterRNumber(self._z80),
            LoadRegisterPNumber(self._z80),
            LoadRegisterQNumber(self._z80),
        ]

    def decode(self, bytes):
        return filter(lambda i: i.regexp_match(bytes), self._instructions).pop()
