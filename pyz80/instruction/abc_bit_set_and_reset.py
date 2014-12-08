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

from abc import ABCMeta
from . import Instruction


class Bit(Instruction):

    __metaclass__ = ABCMeta

    def _instruction_selector(self, selector):
        registers = {
            0b000: self._z80.b,
            0b001: self._z80.c,
            0b010: self._z80.d,
            0b011: self._z80.e,
            0b100: self._z80.h,
            0b101: self._z80.l,
            0b111: self._z80.a,
        }
 
        return registers[selector]

    def _nth_bit_mask(self, n):
        return 0x01 << n

    def nth_bit(self, bits, n):
        nth_bit = 0x00

        if (bits & self._nth_bit_mask(n)) is not 0x00:
            nth_bit = 0x01

        return nth_bit
