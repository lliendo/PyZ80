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
from . import Instruction
from abc_jump import *


class JpNN(Instruction):
    """ JP nn """

    regexp = compile_re('^11000011((?:0|1){8})((?:0|1){8})$')

    def _message_log(self, high_order_byte, low_order_byte):
        address = self._get_address(high_order_byte, low_order_byte)
        return 'JP {:02X}'.format(address)

    def _instruction_logic(self, high_order_byte, low_order_byte):
        self._z80.pc.bits = self._get_address(high_order_byte, low_order_byte)


class JpCCNN(Jp):
    """ JP cc, nn """

    regexp = compile_re('^11((?:0|1){3})010((?:0|1){8})((?:0|1){8})$')

    def _message_log(self, high_order_byte, low_order_byte):
        address = self._get_address(high_order_byte, low_order_byte)
        return 'JP {:02X}, {:02X}'.format(address)

    def _instruction_logic(self, selector, high_order_byte, low_order_byte):
        if self._condition_applies(selector):
            self._z80.pc.bits = self._get_address(high_order_byte, low_order_byte)


class JrE(Jp):
    """ JR e """

    regexp = compile_re('^00011000((?:0|1){8})$')

    def _message_log(self, offset):
        return 'JR {:02X}'.format(offset)

    def _instruction_logic(self, offset):
        self._z80.pc.bits += _get_signed_offset(offset)


class JrSSE(Jp):
    """ JR ss, e """

    regexp = compile_re('^001((?:0|1){2})000((?:0|1){8})$')

    def _message_log(self, selector, offset):
        return 'JR {:02X}, {:02X}'.format(selector, offset)

    def _instruction_logic(self, selector, offset):
        if self._condition_applies(selector):
            self._z80.pc.bits += self._get_signed_offset(offset)


class JpIndirectHL(JpIndirectAddress):
    """ JP (HL) """

    regexp = compile_re('^11101001$')

    def _message_log(self):
        return 'JP (HL)'

    def _instruction_logic(self):
        super(self, JpIndirectHL)._instruction_logic(self._z80.hl.bits)


class JpIndirectIX(JpIndirectAddress):
    """ JP (IX) """

    regexp = compile_re('^1101110111101001$')

    def _message_log(self):
        return 'JP (IX)'

    def _instruction_logic(self):
        super(self, JpIndirectIX)._instruction_logic(self._z80.ix.bits)


class JpIndirectIY(JpIndirectAddress):
    """ JP (IY) """

    regexp = compile_re('^1111110111101001$')

    def _message_log(self):
        return 'JP (IY)'

    def _instruction_logic(self):
        super(self, JpIndirectIY)._instruction_logic(self._z80.iy.bits)


class DjnzE(Jp):
    """ DJNZ e """

    regexp = compile_re('^00010000((?:0|1){8})$')

    def _message_log(self, offset):
        return 'DJNZ {:02X}'.format(offset)

    def _instruction_logic(self, offset):
        self._z80.b -= 1

        if self._z80.b.bits is not 0x00:
            self._z80.pc.bits += self._get_signed_offset(offset)
