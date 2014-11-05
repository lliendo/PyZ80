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
from abc_load_16_bit import *


class LoadDDNN(LoadRegister16Bit):
    """ LD dd, nn """

    regexp = compile_re('^00((?:0|1){2})0001((?:0|1){8})((?:0|1){8})$')

    def _instruction_logic(self, selector, m, n):
        register = self._register_selector(selector)
        register.higher.bits = m
        register.lower.bits = n


class LoadIXNN(Instruction):
    """ LD IX, nn """

    regexp = compile_re('^1101110100100001((?:0|1){8})((?:0|1){8})$')

    def _instruction_logic(self, m, n):
        self._z80.ix.higher.bits = m
        self._z80.ix.lower.bits = n


class LoadIYNN(Instruction):
    """ LD IY, nn """

    regexp = compile_re('^1111110100100001((?:0|1){8})((?:0|1){8})$')

    def _instruction_logic(self, m, n):
        self._z80.iy.higher.bits = m
        self._z80.iy.lower.bits = n


class LoadHLIndirectAddressNN(Instruction):
    """ LD HL, (nn) """

    regexp = compile_re('^00101010((?:0|1){8})((?:0|1){8})$')

    def _instruction_logic(self, m, n):
        address = self._get_address(m, n)
        self._z80.hl.higher.bits = self._z80.ram.read(address + 1)
        self._z80.hl.lower.bits = self._z80.ram.read(address)


class LoadDDIndirectAddressNN(LoadRegister16Bit):
    """ LD dd, (nn) """

    regexp = compile_re('^1110110101((?:0|1){2})1011((?:0|1){8})((?:0|1){8})$')

    def _instruction_logic(self, selector, m, n):
        address = self._get_address(m, n)
        register = self._register_selector(selector)
        register.higher.bits = self._z80.ram.read(address + 1)
        register.lower.bits = self._z80.ram.read(address)


class LoadIXIndirectAddressNN(Instruction):
    """ LD IX, (nn) """

    regexp = compile_re('^1101110100101010((?:0|1){8})((?:0|1){8})$')

    def _instruction_logic(self, m, n):
        address = self._get_address(m, n)
        self._z80.ix.higher.bits = self._z80.ram.read(address + 1)
        self._z80.ix.lower.bits = self._z80.ram.read(address)


class LoadIYIndirectAddressNN(Instruction):
    """ LD IY, (nn) """

    regexp = compile_re('^1111110100101010((?:0|1){8})((?:0|1){8})$')

    def _instruction_logic(self, m, n):
        address = self._get_address(m, n)
        self._z80.iy.higher.bits = self._z80.ram.read(address + 1)
        self._z80.iy.lower.bits = self._z80.ram.read(address)


class LoadIndirectAddressNNHL(Instruction):
    """ LD (nn), HL """

    regexp = compile_re('^00100010((?:0|1){8})((?:0|1){8})$')

    def _instruction_logic(self, m, n):
        address = self._get_address(m, n)
        self._z80.ram.write(address + 1, self._z80.h.bits)
        self._z80.ram.write(address, self._z80.l.bits)


class LoadIndirectAddressNNDD(LoadRegister16Bit):
    """ LD (nn), dd """

    regexp = compile_re('^1110110101((?:0|1){2})0011((?:0|1){8})((?:0|1){8})$')

    def _instruction_logic(self, selector, m, n):
        address = self._get_address(m, n)
        register = self._register_selector(selector)
        self._z80.ram.write(address + 1, register.higher.bits)
        self._z80.ram.write(address, register.lower.bits)


class LoadIndirectAddressNNIX(Instruction):
    """ LD (nn), IX """

    regexp = compile_re('^1101110100100010((?:0|1){8})((?:0|1){8})$')

    def _instruction_logic(self, m, n):
        address = self._get_address(m, n)
        self._z80.ram.write(address + 1, self._z80.ix.higher.bits)
        self._z80.ram.write(address, self._z80.ix.lower.bits)


class LoadIndirectAddressNNIY(Instruction):
    """ LD (nn), IY """

    regexp = compile_re('^1111110100100010((?:0|1){8})((?:0|1){8})$')

    def _instruction_logic(self, m, n):
        address = self._get_address(m, n)
        self._z80.ram.write(address + 1, self._z80.iy.higher.bits)
        self._z80.ram.write(address, self._z80.iy.lower.bits)


class LoadSPHL(Instruction):
    """ LD SP, HL """

    regexp = compile_re('^11111001$')

    def _instruction_logic(self):
        self._z80.sp.bits = self._z80.hl.bits


class LoadSPIX(Instruction):
    """ LD SP, IX """

    regexp = compile_re('^1101110111111001$')

    def _instruction_logic(self):
        self._z80.sp.bits = self._z80.ix.bits


class LoadSPIY(Instruction):
    """ LD SP, IY """

    regexp = compile_re('^1111110111111001$')

    def _instruction_logic(self):
        self._z80.sp.bits = self._z80.iy.bits


class PushQQ(Push):
    """ PUSH qq """

    regexp = compile_re('^11((?:0|1){2})0101$')

    def _instruction_logic(self, selector):
        register = self._register_selector(selector)
        super(PushQQ, self)._instruction_logic(register)


class PushIX(Push):
    """ PUSH IX """

    regexp = compile_re('^1101110111100101$')

    def _instruction_logic(self):
        super(PushIX, self)._instruction_logic(self._z80.ix)


class PushIY(Push):
    """ PUSH IY """

    regexp = compile_re('^1111110111100101$')

    def _instruction_logic(self):
        super(PushIY, self)._instruction_logic(self._z80.iy)


class PopQQ(Pop):
    """ POP qq """

    regexp = compile_re('^11((?:0|1){2})0001$')

    def _instruction_logic(self, selector):
        register = self._register_selector(selector)
        super(PopQQ, self)._instruction_logic(register)


class PopIX(Pop):
    """ POP IX """

    regexp = compile_re('^1101110111100001$')

    def _instruction_logic(self):
        super(PopIX, self)._instruction_logic(self._z80.ix)


class PopIY(Pop):
    """ POP IY """

    regexp = compile_re('^1111110111100001$')

    def _instruction_logic(self):
        super(PopIY, self)._instruction_logic(self._z80.iy)
