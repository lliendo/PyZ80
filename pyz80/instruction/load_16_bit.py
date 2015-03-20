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


class LdDDNN(LdRegister16Bit):
    """ LD dd, nn """

    regexp = compile_re('^00((?:0|1){2})0001((?:0|1){8})((?:0|1){8})$')

    def _message_log(self, selector, high_order_byte, low_order_byte):
        register = self._select_register(selector)
        address = self._get_address(high_order_byte, low_order_byte)
        return 'LD {:}, {:02X}'.format(register.label, address)

    def _instruction_logic(self, selector, high_order_byte, low_order_byte):
        register = self._select_register(selector)
        register.higher.bits = high_order_byte
        register.lower.bits = low_order_byte


class LdIXNN(Instruction):
    """ LD IX, nn """

    regexp = compile_re('^1101110100100001((?:0|1){8})((?:0|1){8})$')

    def _message_log(self, high_order_byte, low_order_byte):
        n = self._get_address(high_order_byte, low_order_byte)
        return 'LD IX, {:02X}'.format(n)

    def _instruction_logic(self, high_order_byte, low_order_byte):
        self._z80.ix.higher.bits = high_order_byte
        self._z80.ix.lower.bits = low_order_byte


class LdIYNN(Instruction):
    """ LD IY, nn """

    regexp = compile_re('^1111110100100001((?:0|1){8})((?:0|1){8})$')

    def _message_log(self, high_order_byte, low_order_byte):
        n = self._get_address(high_order_byte, low_order_byte)
        return 'LD IY, {:02X}'.format(n)

    def _instruction_logic(self, high_order_byte, low_order_byte):
        self._z80.iy.higher.bits = high_order_byte
        self._z80.iy.lower.bits = low_order_byte


class LdHLIndirectNN(Instruction):
    """ LD HL, (nn) """

    regexp = compile_re('^00101010((?:0|1){8})((?:0|1){8})$')

    def _message_log(self, high_order_byte, low_order_byte):
        address = self._get_address(high_order_byte, low_order_byte)
        return 'LD HL, ({:02X})'.format(address)

    def _instruction_logic(self, high_order_byte, low_order_byte):
        address = self._get_address(high_order_byte, low_order_byte)
        self._z80.hl.higher.bits, self._z80.hl.lower.bits = self._z80.ram.read_word(address)


class LdDDIndirectNN(LdRegister16Bit):
    """ LD dd, (nn) """

    regexp = compile_re('^1110110101((?:0|1){2})1011((?:0|1){8})((?:0|1){8})$')

    def _message_log(self, selector, high_order_byte, low_order_byte):
        address = self._get_address(high_order_byte, low_order_byte)
        register = self._select_register(selector)
        return 'LD {:}, ({:02X})'.format(register.label, address)

    def _instruction_logic(self, selector, high_order_byte, low_order_byte):
        address = self._get_address(high_order_byte, low_order_byte)
        register = self._select_register(selector)
        register.higher.bits, register.lower.bits = self._z80.ram.read_word(address)


class LdIXIndirectNN(Instruction):
    """ LD IX, (nn) """

    regexp = compile_re('^1101110100101010((?:0|1){8})((?:0|1){8})$')

    def _message_log(self, high_order_byte, low_order_byte):
        address = self._get_address(high_order_byte, low_order_byte)
        return 'LD IX, ({:02X})'.format(address)

    def _instruction_logic(self, high_order_byte, low_order_byte):
        address = self._get_address(high_order_byte, low_order_byte)
        self._z80.ix.higher.bits, self._z80.ix.lower.bits = self._z80.ram.read_word(address)


class LdIYIndirectNN(Instruction):
    """ LD IY, (nn) """

    regexp = compile_re('^1111110100101010((?:0|1){8})((?:0|1){8})$')

    def _message_log(self, high_order_byte, low_order_byte):
        address = self._get_address(high_order_byte, low_order_byte)
        return 'LD IY, ({:02X})'.format(address)

    def _instruction_logic(self, high_order_byte, low_order_byte):
        address = self._get_address(high_order_byte, low_order_byte)
        self._z80.iy.higher.bits, self._z80.iy.lower.bits = self._z80.ram.read_word(address)


class LdIndirectNNHL(Instruction):
    """ LD (nn), HL """

    regexp = compile_re('^00100010((?:0|1){8})((?:0|1){8})$')

    def _message_log(self, high_order_byte, low_order_byte):
        address = self._get_address(high_order_byte, low_order_byte)
        return 'LD ({:02X}), HL'.format(address)

    def _instruction_logic(self, high_order_byte, low_order_byte):
        address = self._get_address(high_order_byte, low_order_byte)
        self._z80.ram.write_word(address, self._z80.h.bits, self._z80.l.bits)


class LdIndirectNNDD(LdRegister16Bit):
    """ LD (nn), dd """

    regexp = compile_re('^1110110101((?:0|1){2})0011((?:0|1){8})((?:0|1){8})$')

    def _message_log(self, selector, high_order_byte, low_order_byte):
        address = self._get_address(high_order_byte, low_order_byte)
        register = self._select_register(selector)
        return 'LD ({:02X}), {:}'.format(address, register.label)

    def _instruction_logic(self, selector, high_order_byte, low_order_byte):
        address = self._get_address(high_order_byte, low_order_byte)
        register = self._select_register(selector)
        self._z80.ram.write_word(address, register.higher.bits, register.lower.bits)


class LdIndirectNNIX(Instruction):
    """ LD (nn), IX """

    regexp = compile_re('^1101110100100010((?:0|1){8})((?:0|1){8})$')

    def _message_log(self, high_order_byte, low_order_byte):
        return 'LD ({:02X}), IX'.format(self._get_address(high_order_byte, low_order_byte))

    def _instruction_logic(self, high_order_byte, low_order_byte):
        address = self._get_address(high_order_byte, low_order_byte)
        self._z80.ram.write_word(address, self._z80.ix.higher.bits, self._z80.ix.lower.bits)


class LdIndirectNNIY(Instruction):
    """ LD (nn), IY """

    regexp = compile_re('^1111110100100010((?:0|1){8})((?:0|1){8})$')

    def _message_log(self, high_order_byte, low_order_byte):
        address = self._get_address(high_order_byte, low_order_byte)
        return 'LD ({:02X}), IY'.format(address)

    def _instruction_logic(self, high_order_byte, low_order_byte):
        address = self._get_address(high_order_byte, low_order_byte)
        self._z80.ram.write_word(address, self._z80.iy.higher.bits, self._z80.iy.lower.bits)


class LdSPHL(Instruction):
    """ LD SP, HL """

    regexp = compile_re('^11111001$')

    def _message_log(self):
        return 'LD SP, HL'

    def _instruction_logic(self):
        self._z80.sp.bits = self._z80.hl.bits


class LdSPIX(Instruction):
    """ LD SP, IX """

    regexp = compile_re('^1101110111111001$')

    def _message_log(self):
        return 'LD SP, IX'

    def _instruction_logic(self):
        self._z80.sp.bits = self._z80.ix.bits


class LdSPIY(Instruction):
    """ LD SP, IY """

    regexp = compile_re('^1111110111111001$')

    def _message_log(self):
        return 'LD SP, IY'

    def _instruction_logic(self):
        self._z80.sp.bits = self._z80.iy.bits


class PushQQ(Push):
    """ PUSH qq """

    regexp = compile_re('^11((?:0|1){2})0101$')

    def _message_log(self, selector):
        register = self._select_register(selector)
        return 'PUSH {:}'.format(register.label)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(PushQQ, self)._instruction_logic(register)


class PushIX(Push):
    """ PUSH IX """

    regexp = compile_re('^1101110111100101$')

    def _message_log(self):
        return 'PUSH IX'

    def _instruction_logic(self):
        super(PushIX, self)._instruction_logic(self._z80.ix)


class PushIY(Push):
    """ PUSH IY """

    regexp = compile_re('^1111110111100101$')

    def _message_log(self):
        return 'PUSH IY'

    def _instruction_logic(self):
        super(PushIY, self)._instruction_logic(self._z80.iy)


class PopQQ(Pop):
    """ POP qq """

    regexp = compile_re('^11((?:0|1){2})0001$')

    def _message_log(self, selector):
        register = self._select_register(selector)
        return 'POP {:}'.format(register.label)

    def _instruction_logic(self, selector):
        higher_register, lower_register = self._select_register(selector)
        super(PopQQ, self)._instruction_logic(higher_register, lower_register)


class PopIX(Pop):
    """ POP IX """

    regexp = compile_re('^1101110111100001$')

    def _message_log(self, selector):
        return 'POP IX'

    def _instruction_logic(self):
        super(PopIX, self)._instruction_logic(self._z80.ix.higher, self._z80.ix.lower)


class PopIY(Pop):
    """ POP IY """

    regexp = compile_re('^1111110111100001$')

    def _message_log(self, selector):
        return 'POP IY'

    def _instruction_logic(self):
        super(PopIY, self)._instruction_logic(self._z80.iy.higher, self._z80.iy.lower)
