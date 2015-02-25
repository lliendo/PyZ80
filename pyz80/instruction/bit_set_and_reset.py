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
from ..instruction import Instruction
from ..register import Z80ByteRegister


""" BIT instructions. """

class BitTest(Instruction):
    """ BIT b, r """

    regexp = compile_re('^1100101101((?:0|1){3})((?:0|1){3})$')

    def _instruction_selector(self, selector):
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

    def _message_log(self, nth_bit, selector):
        register = self._select_register(selector)
        return 'BIT {:}, {:}'.format(nth_bit, register.label)

    def _instruction_logic(self, nth_bit, selector):
        register = self._select_register(selector)
        self._update_flags(nth_bit, register.bits)

    def _update_flags(self, nth_bit, register):
        self._update_sign_flag(register.bits)

        if register.nth_bit(nth_bit) == 0x00:
            self._set_zero_flag()
            self._set_parity_flag()
        else:
            self._reset_zero_flag()
            self._reset_parity_flag()

        self._update_zero_flag(register.bits)
        self._set_half_carry_flag()
        self._reset_add_substract_flag()


class BitTestIndirectHL(BitTest):
    """ BIT b, (HL) """

    regexp = compile_re('^1100101101((?:0|1){3})110$')

    def _message_log(self, nth_bit):
        return 'BIT {:}, (HL)'.format(nth_bit)

    def _instruction_logic(self, nth_bit):
        register = Z80ByteRegister(bits=self._z80.ram.read(self._z80.hl.bits))
        self._update_flags(nth_bit, register)


class BitTestIndirectIX(BitTest):
    """ BIT b, (IX + d) """

    regexp = compile_re('^1101110111001011((?:0|1){8})01((?:0|1){3})110$')

    def _message_log(self, offset, n):
        return 'BIT {:}, (IX + {:})'.format(n, offset)

    def _instruction_logic(self, offset, nth_bit):
        address = self._z80.ix.bits + offset
        register = Z80ByteRegister(bits=self._z80.ram.read(address))
        self._update_flags(nth_bit, register)


class BitTestIndirectIY(BitTest):
    """ BIT b, (IY + d) """

    regexp = compile_re('^1111110111001011((?:0|1){8})01((?:0|1){3})110$')

    def _message_log(self, offset, nth_bit):
        return 'BIT {:}, (IY + {:})'.format(nth_bit, offset)

    def _instruction_logic(self, offset, nth_bit):
        address = self._z80.iy.bits + offset
        register = Z80ByteRegister(bits=self._z80.ram.read(address))
        self._update_flags(nth_bit, register)


""" SET instructions. """

class BitSet(BitTest):
    """ SET b, r """

    regexp = compile_re('^1100101111((?:0|1){3})((?:0|1){3})$')

    def _message_log(self, nth_bit, selector):
        register = self._select_register(selector)
        return 'SET {:}, {:}'.format(nth_bit, register.label)

    def _instruction_logic(self, nth_bit, selector):
        register = self._select_register(selector)
        register.set_nth_bit(nth_bit)


class BitSetIndirectHL(BitTest):
    """ SET b, (HL) """

    regexp = compile_re('^1100101111((?:0|1){3})110$')

    def _message_log(self, nth_bit):
        return 'SET {:}, (HL)'.format(nth_bit)

    def _instruction_logic(self, nth_bit):
        register = Z80ByteRegister(bits=self._z80.ram.read(self._z80.hl.bits))
        register.set_nth_bit(nth_bit)
        self._z80.ram.write(self._z80.hl.bits, register.bits)


class BitSetIndirectIX(BitSetIndirectHL):
    """ SET b, (IX + d) """

    regexp = compile_re('^1101110111001011((?:0|1){8})11((?:0|1){3})110$')

    def _message_log(self, offset, nth_bit):
        return 'SET {:}, (IX + {:02X})'.format(nth_bit, offset)

    def _instruction_logic(self, offset, nth_bit):
        address = self._z80.ix.bits + offset
        register = Z80ByteRegister(bits=self._z80.ram.read(address))
        register.set_nth_bit(nth_bit)
        self._z80.ram.write(address, register.bits)


class BitSetIndirectIY(BitSetIndirectHL):
    """ SET b, (IY + d) """

    regexp = compile_re('^1111110111001011((?:0|1){8})11((?:0|1){3})110$')

    def _message_log(self, offset, nth_bit):
        return 'SET {:}, (IY + {:02X})'.format(nth_bit, offset)

    def _instruction_logic(self, offset, nth_bit):
        address = self._z80.iy.bits + offset
        register = Z80ByteRegister(bits=self._z80.ram.read(address))
        register.set_nth_bit(nth_bit)
        self._z80.ram.write(address, register.bits)


class BitSetIndirectIXR(BitTest):
    """ SET b, (IX + d), r """

    regexp = compile_re('^1101110111001011((?:0|1){8})11((?:0|1){3})((?:0|1){3})$')

    def _message_log(self, offset, nth_bit, selector):
        register = self._select_register(selector)
        return 'SET {:}, (IX + {:02X})'.format(nth_bit, offset, register.label)

    def _instruction_logic(self, offset, nth_bit, selector):
        register = self._select_register(selector)
        address = self._z80.ix.bits + offset
        register.bits = self._z80.ram.read(address)
        register.set_nth_bit(nth_bit)
        self._z80.ram.write(address, register.bits)


class BitSetIndirectIYR(BitTest):
    """ SET b, (IY + d), r """

    regexp = compile_re('^1111110111001011((?:0|1){8})11((?:0|1){3})((?:0|1){3})$')

    def _message_log(self, offset, nth_bit, selector):
        register = self._select_register(selector)
        return 'SET {:}, (IY + {:02X})'.format(nth_bit, offset, register.label)

    def _instruction_logic(self, offset, nth_bit, selector):
        register = self._select_register(selector)
        address = self._z80.iy.bits + offset
        register.bits = self._z80.ram.read(address)
        register.set_nth_bit(nth_bit)
        self._z80.ram.write(address, register.bits)


""" RES instructions. """

class BitReset(BitTest):
    """ RES b, r """

    regexp = compile_re('^1100101110((?:0|1){3})((?:0|1){3})$')

    def _message_log(self, nth_bit, selector):
        register = self._select_register(selector)
        return 'RES {:}, {:}'.format(nth_bit, register.label)

    def _instruction_logic(self, nth_bit, selector):
        register = self._select_register(selector)
        register.reset_nth_bit(nth_bit)


class BitResetIndirectHL(BitTest):
    """ RES b, (HL) """

    regexp = compile_re('^1100101110((?:0|1){3})110$')

    def _message_log(self, nth_bit):
        return 'RES {:}, (HL)'.format(nth_bit)

    def _instruction_logic(self, nth_bit):
        register = Z80ByteRegister(bits=self._z80.ram.read(self._z80.hl.bits))
        register.reset_nth_bit(nth_bit)
        self._z80.ram.write(self._z80.hl.bits, register.bits)


class BitResetIndirectIX(BitResetIndirectHL):
    """ RES b, (IX + d) """

    regexp = compile_re('^1101110111001011((?:0|1){8})10((?:0|1){3})110$')

    def _message_log(self, offset, nth_bit):
        return 'RES {:}, (IX + {:02X})'.format(nth_bit, offset)

    def _instruction_logic(self, offset, nth_bit):
        address = self._z80.ix.bits + offset
        register = Z80ByteRegister(bits=self._z80.ram.read(address))
        register.reset_nth_bit(nth_bit)
        self._z80.ram.write(address, register.bits)


class BitResetIndirectIY(BitResetIndirectHL):
    """ RES b, (IY + d) """

    regexp = compile_re('^1111110111001011((?:0|1){8})10((?:0|1){3})110$')

    def _message_log(self, offset, nth_bit):
        return 'RES {:}, (IY + {:02X})'.format(nth_bit, offset)

    def _instruction_logic(self, offset, nth_bit):
        address = self._z80.iy.bits + offset
        register = Z80ByteRegister(bits=self._z80.ram.read(address))
        register.reset_nth_bit(nth_bit)
        self._z80.ram.write(address, register.bits)
