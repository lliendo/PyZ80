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


class Arithmetic8Bit(Instruction):

    __metaclass__ = ABCMeta

    def _default_selector(self, selector):
        registers = {
            0b000: self._z80.b,
            0b001: self._z80.c,
            0b010: self._z80.d,
            0b011: self._z80.e,
            0b111: self._z80.a,
        }
 
        return registers[selector]

    def _r_selector(self, selector):
        registers = {
            0b100: self._z80.h,
            0b101: self._z80.l,
        }
 
        return registers[selector]

    def _p_selector(self, selector):
        registers = {
            0b100: self._z80.ixh,
            0b101: self._z80.ixl,
        }

        return registers[selector]

    def _q_selector(self, selector):
        registers = {
            0b100: self._z80.iyh,
            0b101: self._z80.iyl,
        }
 
        return registers[selector]

    def _select_register(self, selector):
        try:
            register = self._default_selector(selector)
        except KeyError:
            register = self._instruction_selector(selector)

        return register


class Add8Bit(Arithmetic8Bit):
    
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

    def _instruction_logic(self, operands):
        add_result = sum(operands)
        self._update_flags(operands, add_result)
        self._z80.a.bits = add_result

    def _update_flags(self, operands, instruction_result):
        self._update_sign_flag(instruction_result)
        self._update_zero_flag(instruction_result)
        self._update_half_carry_flag(operands)
        self._update_overflow_flag(operands)
        self._update_carry_flag(operands)
        self._instruction_flags.reset_add_substract_flag()


class AddAIndirectAddress(Add8Bit):

    __metaclass__ = ABCMeta

    def _instruction_logic(self, address):
        n = self._z80._read_ram(address)
        super(AddAIndirectAddress, self)._instruction_logic([self._z80.a.bits, n])


class AdcAIndirectAddress(Add8Bit):

    __metaclass__ = ABCMeta

    def _instruction_logic(self, address):
        n = self._z80._read_ram(address)
        super(AdcAIndirectAddress, self)._instruction_logic(
            [self._z80.a.bits, n, self._z80.f.carry_flag]
        )


class Sub8Bit(Arithmetic8Bit):

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

    def _instruction_logic(self, operands):
        sub_result = reduce(lambda n, m: n - m, operands)
        self._update_flags(operands, sub_result)
        self._z80.a.bits = sub_result

    def _update_flags(self, operands, instruction_result):
        self._update_sign_flag(instruction_result)
        self._update_zero_flag(instruction_result)
        self._update_half_carry_flag(operands)
        self._update_overflow_flag(operands)
        self._update_carry_flag(operands)
        self._instruction_flags.set_add_substract_flag()


class SubAIndirectAddress(Sub8Bit):

    __metaclass__ = ABCMeta

    def _instruction_logic(self, address):
        n = self._z80._read_ram(address)
        super(SubAIndirectAddress, self)._instruction_logic([self._z80.a.bits, n])


class SbcAIndirectAddress(Sub8Bit):

    __metaclass__ = ABCMeta

    def _instruction_logic(self, address):
        n = self._z80._read_ram(address)
        super(SbcAIndirectAddress, self)._instruction_logic(
            [self._z80.a.bits, n, self._z80.f.carry_flag]
        )


class And8Bit(Arithmetic8Bit):

    __metaclass__ = ABCMeta

    def _instruction_logic(self, operands):
        and_result = reduce(lambda n, m: n & m, operands)
        self._update_flags(operands, and_result)
        self._z80.a.bits = and_result

    def _update_flags(self, operands, instruction_result):
        self._update_sign_flag(instruction_result)
        self._update_zero_flag(instruction_result)
        self._instruction_flags.set_half_carry_flag()
        self._update_parity_flag(operands)
        self._instruction_flags.reset_carry_flag()
        self._instruction_flags.reset_add_substract_flag()


class Or8Bit(Arithmetic8Bit):
 
    __metaclass__ = ABCMeta

   def _instruction_logic(self, operands):
        or_result = reduce(lambda n, m: n | m, operands)
        self._update_flags(operands, or_result)
        self._z80.a.bits = or_result

    def _update_flags(self, operands, instruction_result):
        self._update_sign_flag(instruction_result)
        self._update_zero_flag(instruction_result)
        self._instruction_flags.reset_half_carry_flag()
        self._update_parity_flag(operands)
        self._instruction_flags.reset_carry_flag()
        self._instruction_flags.reset_add_substract_flag()


class Xor8Bit(Arithmetic8Bit):
 
    __metaclass__ = ABCMeta

   def _instruction_logic(self, operands):
        xor_result = reduce(lambda n, m: n ^ m, operands)
        self._update_flags(operands, xor_result)
        self._z80.a.bits = xor_result

    def _update_flags(self, operands, instruction_result):
        self._update_sign_flag(instruction_result)
        self._update_zero_flag(instruction_result)
        self._instruction_flags.reset_half_carry_flag()
        self._update_parity_flag(operands)
        self._instruction_flags.reset_carry_flag()
        self._instruction_flags.reset_add_substract_flag()
