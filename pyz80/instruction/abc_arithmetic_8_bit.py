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


class Add8Bit(Instruction):
    
    __metaclass__ = ABCMeta
    
    def _overflow(self, operands, bits=Instruction.BYTE_SIZE):
        bitmask = self._bitmask(bits=bits)
        overflow_condition = False
        msbs = [self._msb(operand) for operand in operands]

        """
        If operands have the same sign we check
        if the addtion results in a change of sign.
        """
        if not reduce(lambda n, m: n ^ m, msbs):
            sum_msb = self._msb(sum(operands) & bitmask)

            if operands[0] ^ sum_msb:
                overflow_condition = True

        return overflow_condition

    def _carry(self, operands, bits=Instruction.BYTE_SIZE):
        bitmask = self._bitmask(bits=bits)
        return reduce(lambda n, m: (n & bitmask) + (m & bitmask), operands) > bitmask

    def _instruction_logic(self, selector):
        register = self._register_selector(selector)
        add_result = self._z80.a.bits + register.bits
        self._update_flags([self._z80.a.bits, register.bits], add_result)
        self._z80.a.bits = add_result

    def _update_flags(self, operands, instruction_result):
        self._update_sign_flag(instruction_result)
        self._update_zero_flag(instruction_result)
        self._update_half_carry_flag(operands)
        self._update_overflow_flag(operands)
        self._update_carry_flag(operands)
        self._instruction_flags.reset_add_substract_flag()


class Sub8Bit(Instruction):

    __metaclass__ = ABCMeta

    def _overflow(self, operands, bits=Instruction.BYTE_SIZE):
        bitmask = _bitmask(bits=bits)
        overflow_condition = False
        msbs = [self._msb(operand) for operand in operands]

        """
        If operands have different signs we check
        if the substraction results in a change of sign.
        """
        if not reduce(lambda n, m: n ^ m, msbs):
            substraction_msb = self._msb(reduce(lambda n, m: n - m, operands) & bitmask)

            if operands[0] ^ substraction_msb:
                overflow_condition = True

        return overflow_condition

    def _carry(self, operands, bits=Instruction.BYTE_SIZE):
        return any([operands[i] < operands[i + 1] for i in range(0, len(operands) - 1)])

    def _instruction_logic(self, selector):
        register = self._register_selector(selector)
        sub_result = self._z80.a.bits - register.bits
        self._update_flags([self._z80.a.bits, register.bits], sub_result)
        self._z80.a.bits = sub_result

    def _update_flags(self, operands, instruction_result):
        self._update_sign_flag(instruction_result)
        self._update_zero_flag(instruction_result)
        self._update_half_carry_flag(operands)
        self._update_overflow_flag(operands)
        self._update_carry_flag(operands)
        self._instruction_flags.set_add_substract_flag()


class AddAIndirectAddress(Add8Bit):

    __metaclass__ = ABCMeta

    def _instruction_logic(self, address):
        n = self._z80._read_ram(address)
        add_result = self._z80.a.bits + n
        self._update_flags(self._z80.a.bits, n, add_result)
        self._z80.a.bits = add_result
