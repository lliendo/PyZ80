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
from abc import ABCMeta
from abc_arithmetic_16_bit import Add16Bit, Sub16Bit
from . import Instruction


class AddHLSS(Add16Bit):
    """ ADD HL, ss """

    regexp = compile_re('^00((?:0|1){2})1001$')

    def _message_log(self, selector):
        register = self._select_register(selector)
        return 'ADD HL, {0}'.format(register.label)

    def _instruction_selector(self, selector):
        return self._ss_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(AddHLSS, self)._instruction_logic([self._z80.a.bits, register.bits])

    def _update_flags(self, operands, instruction_result):
        self._update_half_carry_flag(operands)
        self._update_carry_flag(operands)
        self._z80.f.reset_add_substract_flag()


class AddIXPP(AddHLSS):
    """ ADD IX, pp """

    regexp = compile_re('^1101111000((?:0|1){2})1001$')

    def _instruction_selector(self, selector):
        return self.__selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(AddIXPP, self)._instruction_logic([self._z80.ix.bits, register.bits])


class AddIYQQ(AddHLSS):
    """ ADD IY, qq """

    regexp = compile_re('^1111111000((?:0|1){2})1001$')

    def _instruction_selector(self, selector):
        return self._pp_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(AddIYQQ, self)._instruction_logic([self._z80.iy.bits, register.bits])


class AdcHLSS(Add16Bit):
    """ ADC HL, ss """

    regexp = compile_re('^1110110101((?:0|1){2})1010$')

    def _instruction_selector(self, selector):
        return self._ss_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(AdcHLSS, self)._instruction_logic(
            [self._z80.a.bits, register.bits, self._z80.f.carry_flag]
        )

    def _update_flags(self, operands, instruction_result):
        self._update_sign_flag(instruction_result)
        self._update_zero_flag(instruction_result)
        self._update_half_carry_flag(operands)
        self._update_carry_flag(operands)
        self._update_overflow_flag(operands)
        self._z80.f.reset_add_substract_flag()


class SbcHLSS(Sub16Bit):
    """ SUB HL, ss """

    regexp = compile_re('^1110110101((?:0|1){2})0010$')

    def _instruction_selector(self, selector):
        return self._ss_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(SbcHLSS, self)._instruction_logic(
            [self._z80.a.bits, register.bits, self._z80.f.carry_flag]
        )

    def _update_flags(self, operands, instruction_result):
        self._update_sign_flag(instruction_result)
        self._update_zero_flag(instruction_result)
        self._update_half_carry_flag(operands)
        self._update_carry_flag(operands)
        self._update_overflow_flag(operands)
        self._z80.f.set_add_substract_flag()


class IncSS(Instruction):
    """ INC ss """

    regexp = compile_re('^00((?:0|1){2})0011$')

    def _instruction_selector(self, selector):
        return self._ss_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        register.bits += 1


class IncIX(Instruction):
    """ INC IX """

    regexp = compile_re('^1101110100100011$')

    def _instruction_logic(self, selector):
        self._z80.ix.bits += 1


class IncIY(Instruction):
    """ INC IY """

    regexp = compile_re('^1111110100100011$')

    def _instruction_logic(self, selector):
        self._z80.iy.bits += 1


class DecSS(Instruction):
    """ DEC ss """

    regexp = compile_re('^00((?:0|1){2})1011$')

    def _instruction_selector(self, selector):
        return self._ss_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        register.bits += 1


class DecIX(Instruction):
    """ DEC IX """

    regexp = compile_re('^1101110100101011$')

    def _instruction_logic(self, selector):
        self._z80.ix.bits += 1


class DecIY(Instruction):
    """ DEC IY """

    regexp = compile_re('^1111110100101011$')

    def _instruction_logic(self, selector):
        self._z80.iy.bits += 1
