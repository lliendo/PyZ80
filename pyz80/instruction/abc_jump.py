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


class Jp(Instruction):

    __metaclass__ = ABCMeta

    def _get_signed_offset(self, offset):
        address = offset

        if (offset & 0x80) is 0x01:
            address = -(offset & 0x7F)
            
        return address
        
    def _condition_applies(self, condition):
        condition_holds = False
        jump_conditions = {
            0b000: not self._z80.f.zero_flag(),
            0b001: self._z80.f.zero_flag(),
            0b010: not self._z80.f.carry_flag(),
            0b011: self._z80.f.carry_flag(),
            0b100: not self._z80.f.parity_flag(),
            0b101: self._z80.f.parity_flag(),
            0b110: not self._z80.f.sign_flag(),
            0b111: self._z80.f.sign_flag(),
        }
        
        if jump_conditions[condition] is 0x01:
            condition_holds = True

        return condition_holds


class JpIndirectAddress(Instruction):
    
    __metaclass__ = ABCMeta

    def _instruction_logic(self, address):
        self._z80.pc.bits = self._z80.ram.read(address)
