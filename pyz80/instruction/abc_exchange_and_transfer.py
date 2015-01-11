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


class Exchange(Instruction):

    __metaclass__ = ABCMeta

    def _swap_registers(self, register, other_register):
        bits = register.bits
        register.bits = other_register.bits
        other_register.bits = bits

    def _swap_register_with_ram_word(self, address, register):
        high_order_byte, low_order_byte = self._z80.ram.read_word(address)
        self._z80.ram.write_word(address, register.higher, register.lower)
        register.higher = high_order_byte
        register.lower = low_order_byte
