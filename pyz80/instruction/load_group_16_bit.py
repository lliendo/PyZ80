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


class LoadDDNN(LoadRegister16Bit):
    """ LD dd, nn """

    def _instruction_regexp(self):
        return '^00((?:0|1){2})0001((?:0|1){8})((?:0|1){8})$'

    def _instruction_logic(self, selector, m, n):
        register = self._register_selector(selector)
        register.higher.bits = m
        register.lower.bits = n


class LoadIXNN(Instruction):
    """ LD IX, nn """

    def _instruction_regexp(self):
        return '^1101110100100001((?:0|1){8})((?:0|1){8})$'

    def _instruction_logic(self, m, n):
        self._z80.ix.higher.bits = m
        self._z80.ix.lower.bits = n


class LoadIYNN(Instruction):
    """ LD IY, nn """

    def _instruction_regexp(self):
        return '^1111110100100001((?:0|1){8})((?:0|1){8})$'

    def _instruction_logic(self, m, n):
        self._z80.iy.higher.bits = m
        self._z80.iy.lower.bits = n


class LoadHLIndirectNN(Instruction):
    """ LD HL, (nn) """

    def _instruction_regexp(self):
        return '^00101010((?:0|1){8})((?:0|1){8})$'

    def _instruction_logic(self, m, n):
        address = self._get_address(m, n)
        self._z80.hl.higher.bits = self._z80.ram.read(address + 1)
        self._z80.hl.lower.bits = self._z80.ram.read(address)


class LoadDDIndirectNN(LoadRegister16Bit):
    """ LD dd, (nn) """

    def _instruction_regexp(self):
        return '^1110110101((?:0|1){2})1011((?:0|1){8})((?:0|1){8})$'

    def _instruction_logic(self, selector, m, n):
        address = self._get_address(m, n)
        register = self._register_selector(selector)
        register.higher.bits = self._z80.ram.read(address + 1)
        register.lower.bits = self._z80.ram.read(address)


class LoadIXIndirectNN(Instruction):
    """ LD IX, (nn) """

    def _instruction_regexp(self):
        return '^1101110100101010((?:0|1){8})((?:0|1){8})$'

    def _instruction_logic(self, m, n):
        address = self._get_address(m, n)
        self._z80.ix.higher.bits = self._z80.ram.read(address + 1)
        self._z80.ix.lower.bits = self._z80.ram.read(address)


class LoadIYIndirectNN(Instruction):
    """ LD IY, (nn) """

    def _instruction_regexp(self):
        return '^1111110100101010((?:0|1){8})((?:0|1){8})$'

    def _instruction_logic(self, m, n):
        address = self._get_address(m, n)
        self._z80.iy.higher.bits = self._z80.ram.read(address + 1)
        self._z80.iy.lower.bits = self._z80.ram.read(address)


class LoadIndirectNNHL(Instruction):
    """ LD (nn), HL """

    def _instruction_regexp(self):
        return '^00100010((?:0|1){8})((?:0|1){8})$'

    def _instruction_logic(self, m, n):
        address = self._get_address(m, n)
        self._z80.ram.write(address + 1, self._z80.h.bits)
        self._z80.ram.write(address, self._z80.l.bits)


class LoadIndirectNNDD(Instruction):
    """ LD (nn), dd """

    def _instruction_regexp(self):
        return '^1110110101((?:0|1){2})0011((?:0|1){8})((?:0|1){8})$'

    def _instruction_logic(self, selector, m, n):
        address = self._get_address(m, n)
        register = self._register_selector(selector)
        self._z80.ram.write(address + 1, register.higher.bits)
        self._z80.ram.write(address, register.lower.bits)


class LoadIndirectNNIX(Instruction):
    """ LD (nn), IX """

    def _instruction_regexp(self):
        return '^1101110100100010((?:0|1){8})((?:0|1){8})$'

    def _instruction_logic(self, m, n):
        address = self._get_address(m, n)
        self._z80.ram.write(address + 1, self._z80.ix.higher.bits)
        self._z80.ram.write(address, self._z80.ix.lower.bits)


class LoadIndirectNNIY(Instruction):
    """ LD (nn), IY """

    def _instruction_regexp(self):
        return '^1111110100100010((?:0|1){8})((?:0|1){8})$'

    def _instruction_logic(self, m, n):
        address = self._get_address(m, n)
        self._z80.ram.write(address + 1, self._z80.iy.higher.bits)
        self._z80.ram.write(address, self._z80.iy.lower.bits)


class LoadSPHL(Instruction):
    """ LD SP, HL """

    def _instruction_regexp(self):
        return '^11111001$'

    def _instruction_logic(self):
        self._z80.sp.bits = self._z80.hl.bits


class LoadSPIX(Instruction):
    """ LD SP, IX """

    def _instruction_regexp(self):
        return '^1101110111111001$'

    def _instruction_logic(self):
        self._z80.sp.bits = self._z80.ix.bits


class LoadSPIY(Instruction):
    """ LD SP, IY """

    def _instruction_regexp(self):
        return '^1111110111111001$'

    def _instruction_logic(self):
        self._z80.sp.bits = self._z80.iy.bits


class Push(Instruction):
    
    __metaclass__ = ABCMeta

    def _register_selector(self, selector):
        # Test if this is valid -> the combine is called each
        # time the dictionary is accessed and not computed on definition.
        # Otherwise use :
        # if selector == 0b11:
        #     return self._z80.a.combine(self._z80.f)

        registers = {
            0b00: self._z80.bc,
            0b01: self._z80.de,
            0b10: self._z80.hl,
            0b11: self._z80.a.combine(self._z80.f),

        }

        return registers[selector]

    def _instruction_logic(self, register):
        self._z80.ram.write(self._z80.sp.bits - 2, register.lower.bits)
        self._z80.ram.write(self._z80.sp.bits - 1, register.higher.bits)
        self._z80.sp.bits -= 2


class PushQQ(Push):
    """ PUSH qq """

    def _instruction_regexp(self):
        return '^11((?:0|1){2})0101$'

    def _instruction_logic(self, selector):
        register = self._register_selector(selector)
        super(PushQQ, self)._instruction_logic(register)


class PushIX(Push):
    """ PUSH IX """

    def _instruction_regexp(self):
        return '^1101110111100101$'

    def _instruction_logic(self):
        super(PushIX, self)._instruction_logic(self._z80.ix)


class PushIY(Push):
    """ PUSH IY """

    def _instruction_regexp(self):
        return '^1111110111100101$'

    def _instruction_logic(self):
        super(PushIY, self)._instruction_logic(self._z80.iy)


class Pop(Instruction):
    
    __metaclass__ = ABCMeta

    def _register_selector(self, selector):
        # Test if this is valid -> the combine is called each
        # time the dictionary is accessed and not computed on definition.
        # Otherwise use :
        # if selector == 0b11:
        #     return self._z80.a.combine(self._z80.f)

        registers = {
            0b00: self._z80.bc,
            0b01: self._z80.de,
            0b10: self._z80.hl,
            0b11: self._z80.a.combine(self._z80.f),

        }

        return registers[selector]

    def _instruction_logic(self, register):
        register.higher.bits = self._z80.ram.read(self._z80.sp.bits + 1)
        register.lower.bits = self._z80.ram.read(self._z80.sp.bits)
        self._z80.sp.bits += 2


class PopQQ(Pop):
    """ POP qq """

    def _instruction_regexp(self):
        return '^11((?:0|1){2})0001$'

    def _instruction_logic(self, selector):
        register = self._register_selector(selector)
        super(PopQQ, self)._instruction_logic(register)


class PopIX(Pop):
    """ POP IX """

    def _instruction_regexp(self):
        return '^1101110111100001$'

    def _instruction_logic(self):
        super(PopIX, self)._instruction_logic(self._z80.ix)


class PopIY(Pop):
    """ POP IY """

    def _instruction_regexp(self):
        return '^1111110111100001$'

    def _instruction_logic(self):
        super(PopIY, self)._instruction_logic(self._z80.iy)
