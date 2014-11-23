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

from re import compile as compile_re
from abc_arithmetic_8_bit import *


class AddAR(Add8Bit):
    """ ADD A, r """
    
    regexp = compile_re('^10000((?:0|1){3})$')

    def _register_selector(self, selector):
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


class AddAP(Add8Bit):
    """ ADD A, p """

    regexp = compile_re('^1101110110000((?:0|1){3})$')

    def _register_selector(self, selector):
        registers = {
            0b000: self._z80.b,
            0b001: self._z80.c,
            0b010: self._z80.d,
            0b011: self._z80.e,
            0b100: self._z80.ixh,
            0b101: self._z80.ixl,
            0b111: self._z80.a,
        }
 
        return registers[selector]


class AddAQ(Add8Bit):
    """ ADD A, q """

    regexp = compile_re('^1111110110000((?:0|1){3})$')

    def _register_selector(self, selector):
        registers = {
            0b000: self._z80.b,
            0b001: self._z80.c,
            0b010: self._z80.d,
            0b011: self._z80.e,
            0b100: self._z80.iyh,
            0b101: self._z80.iyl,
            0b111: self._z80.a,
        }
 
        return registers[selector]


class AddAN(Add8Bit):
    """ ADD A, n """

    regexp = compile_re('^11000110((?:0|1){8})$')

    def _instruction_logic(self, n):
        add_result = self._z80.a.bits + n
        self._update_flags(self._z80.a.bits, n, add_result)
        self._z80.a.bits = add_result


class AddAIndirectAddressHLRegister(AddAIndirectAddress):
    """ ADD A, (HL) """

    regexp = compile_re('^10000110$')

    def _instruction_logic(self):
        address = self._z80.hl.bits
        super(AddAIndirectAddressHLRegister, self)._instruction_logic(address)


class AddAIndirectAddressIXRegister(AddAIndirectAddress):
    """ ADD A, (IX + d) """

    regexp = compile_re('^1101110110000110((?:0|1){8})$')

    def _instruction_logic(self, offset):
        address = self._z80.ix.bits + offset
        super(AddAIndirectAddressIXRegister, self)._instruction_logic(address)


class AddAIndirectAddressIYRegister(AddAIndirectAddress):
    """ ADD A, (IY + d) """

    regexp = compile_re('^1111110110000110((?:0|1){8})$')

    def _instruction_logic(self, offset):
        address = self._z80.iy.bits + offset
        super(AddAIndirectAddressIYRegister, self)._instruction_logic(address)
