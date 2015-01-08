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
from abc_jump import Jp


class CallNN(Instruction):
    """ CALL nn """

    regexp = compile_re('^11001101((?:0|1){8})((?:0|1){8})$')

    def _instruction_logic(self, high_order_byte, low_order_byte):
        self._z80.ram.write(self._z80.sp.bits - 1, self._z80.pc.higher.bits)
        self._z80.ram.write(self._z80.sp.bits - 2, self._z80.pc.lower.bits)
        self._z80.sp.bits -= 2
        self._z80.pc.bits = self._get_address(high_order_byte, low_order_byte)


class CallCCNN(CallNN, Jp):
    """ CALL cc, nn """

    regexp = compile_re('^11((?:0|1){3})100((?:0|1){8})((?:0|1){8})$')

    def _instruction_logic(self, selector, high_order_byte, low_order_byte):
        if self._condition_applies(selector):
            super(self, CallCCNN)._instruction_logic(high_order_byte, low_order_byte)


class Ret(Instruction):
    """ RET """

    regexp = compile_re('^11001001$')

    def _instruction_logic(self):
        self._z80.pc.lower.bits = self._z80.ram.read(self._z80.sp.bits)
        self._z80.pc.higher.bits = self._z80.ram.read(self._z80.sp.bits + 1)
        self._z80.sp.bits += 2


class RetCC(Ret, Jp):
    """ RET cc """

    regexp = compile_re('^11((?:0|1){3})000$')

    def _instruction_logic(self, selector):
        if self._condition_applies(selector):
            super(self, RetCC)._instruction_logic()


class Reti(Ret):
    """ RETI """

    regexp = compile_re('^1110110101001101$')

    def _instruction_logic(self):
        super(self, Reti)._instruction_logic()
        self._z80.iff1 = self._z80.iff2


class Retn(Reti):
    """ RETN """

    regexp = compile_re('^1110110101000101$')


class Rst(Instruction):
    """ RST p """

    regexp = compile_re('^11((?:0|1){3})111$')

    def _address_selector(self, selector):
        addresses = {
            0b000: 0x00,
            0b001: 0x08,
            0b010: 0x10,
            0b011: 0x18,
            0b100: 0x20,
            0b101: 0x28,
            0b110: 0x30,
            0b111: 0x38,
        }

        return addresses[selector]

    def _instruction_logic(self, selector):
        self._z80.ram.write(self._z80.sp.bits - 1, self._z80.pc.higher.bits)
        self._z80.ram.write(self._z80.sp.bits - 2, self._z80.pc.lower.bits)
        self._z80.sp.bits -= 2
        self._z80.pc.bits = self._address_selector(selector)
