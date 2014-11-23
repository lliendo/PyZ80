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

from abc import ABCMeta, abstractmethod
from . import Instruction


# TODO: Rename this class with a more appropiate name.
class LoadRegister16Bit(Instruction):

    __metaclass__ = ABCMeta

    def _register_selector(self, selector):
        registers = {
            0b00: self._z80.bc,
            0b01: self._z80.de,
            0b10: self._z80.hl,
            0b11: self._z80.sp,
        }

        return registers[selector]


class Push(Instruction):
    
    __metaclass__ = ABCMeta

    def _register_selector(self, selector):
        registers = {
            0b00: self._z80.bc,
            0b01: self._z80.de,
            0b10: self._z80.hl,
        }

        if selector == 0b11:
            register = self._z80.a.combine(self._z80.f)
        else:
            register = registers[selector]

        return register

    def _instruction_logic(self, register):
        self._z80.ram.write(self._z80.sp.bits - 2, register.lower.bits)
        self._z80.ram.write(self._z80.sp.bits - 1, register.higher.bits)
        self._z80.sp.bits -= 2


class Pop(Instruction):
    
    __metaclass__ = ABCMeta

    def _register_selector(self, selector):
        registers = {
            0b00: self._z80.bc,
            0b01: self._z80.de,
            0b10: self._z80.hl,
        }
        
        if selector == 0b11:
            higher_register = self._z80.a
            lower_register = self._z80.f
        else:
            higher_register = registers[selector].higher
            lower_register = registers[selector].lower

        return higher_register, lower_register

    def _instruction_logic(self, higher_register, lower_register):
        higher_register.bits = self._z80.ram.read(self._z80.sp.bits + 1)
        lower_register.bits = self._z80.ram.read(self._z80.sp.bits)
        self._z80.sp.bits += 2
