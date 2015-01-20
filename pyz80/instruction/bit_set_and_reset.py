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
from abc_bit_set_and_reset import Bit


""" BIT instructions. """

class BitTest(Bit):
    """ BIT b, r """

    regexp = compile_re('^1100101101((?:0|1){3})((?:0|1){3})$')

    def _instruction_logic(self, n, selector):
        register = self._select_register(selector)
        self._update_flags(n, register.bits)

    def _update_flags(self, n, bits):
        if (self.nth_bit(bits) is 0x01) and (n is 7):
            self._set_sign_flag()
        else:
            self._reset_sign_flag()

        self._update_zero_flag(self.nth_bit(bits))
        self._set_half_carry_flag()
        self._reset_add_substract_flag()


class BitTestIndirectAddressHL(BitTest):
    """ BIT b, (HL) """

    regexp = compile_re('^1100101101((?:0|1){3})110$')

    def _instruction_logic(self, n, selector):
        bits = self._z80.ram.read(self._z80.hl.bits)
        self._update_flags(n, bits)


class BitTestIndirectAddressIX(BitTest):
    """ BIT b, (IX + d) """

    regexp = compile_re('^1101110111001011((?:0|1){8})01((?:0|1){3})110$')

    def _instruction_logic(self, offset, n):
        bits = self._z80.ram.read(self._z80.ix.bits + offset)
        self._update_flags(n, bits)


class BitTestIndirectAddressIY(BitTest):
    """ BIT b, (IY + d) """

    regexp = compile_re('^1111110111001011((?:0|1){8})01((?:0|1){3})110$')

    def _instruction_logic(self, offset, n):
        bits = self._z80.ram.read(self._z80.iy.bits + offset)
        self._update_flags(n, bits)


""" SET instructions. """

class BitSet(Bit):
    """ SET b, r """

    regexp = compile_re('^1100101111((?:0|1){3})((?:0|1){3})$')

    def _instruction_logic(self, bit, selector):
        register = self._select_register(selector)
        register.set_nth_bit(bit)


class BitSetIndirectAddressHL(Bit):
    """ SET b, (HL) """

    regexp = compile_re('^1100101111((?:0|1){3})110$')

    def set_nth_bit(self, bits, n):
        return bits | self._nth_bit_mask(n)

    def _instruction_logic(self, n):
        bits = self._z80.ram.read(self._z80.hl.bits)
        self._z80.ram.write(address, self.set_nth_bit(bits, n))


class BitSetIndirectAddressIX(BitSetIndirectAddressHL):
    """ SET b, (IX + d) """

    regexp = compile_re('^1101110111001011((?:0|1){8})11((?:0|1){3})110$')

    def _instruction_logic(self, offset, n):
        address = self._z80.ix.bits + offset
        bits = self._z80.ram.read(address)
        self._z80.ram.write(address, self.set_nth_bit(bits, n))


class BitSetIndirectAddressIYRegister(BitSetIndirectAddressHL):
    """ SET b, (IY + d) """

    regexp = compile_re('^1111110111001011((?:0|1){8})11((?:0|1){3})110$')

    def _instruction_logic(self, offset, n):
        address = self._z80.iy.bits + offset
        bits = self._z80.ram.read(address)
        self._z80.ram.write(address, self.set_nth_bit(bits, n))


class BitSetIndirectAddressIXRegister(Bit):
    """ SET b, (IX + d), r """

    regexp = compile_re('^1101110111001011((?:0|1){8})11((?:0|1){3})((?:0|1){3})$')

    def _instruction_logic(self, n, offset, selector):
        register = self._select_register(selector)
        address = self._z80.ix.bits + offset
        register.bits = self._z80.ram.read(address)
        register.set_nth_bit(n)
        self._z80.ram.write(address, register.bits)


class BitSetIndirectAddressIYRegister(Bit):
    """ SET b, (IY + d), r """

    regexp = compile_re('^1111110111001011((?:0|1){8})11((?:0|1){3})((?:0|1){3})$')

    def _instruction_logic(self, n, offset, selector):
        register = self._select_register(selector)
        address = self._z80.iy.bits + offset
        register.bits = self._z80.ram.read(address)
        register.set_nth_bit(n)
        self._z80.ram.write(address, register.bits)


""" RESET instructions. """

class BitReset(Bit):
    """ RESET b, r """

    regexp = compile_re('^1000101111((?:0|1){3})((?:0|1){3})$')

    def _instruction_logic(self, bit, selector):
        register = self._select_register(selector)
        register.reset_nth_bit(bit)


class BitResetIndirectAddressHL(Bit):
    """ RESET b, (HL) """

    regexp = compile_re('^1000101111((?:0|1){3})110$')

    def reset_nth_bit(self, n):
        if self.nth_bit(bits, n) is 0x01:
            return n ^ self._nth_bit_mask(n)

        return n

    def _instruction_logic(self, n):
        bits = self._z80.ram.read(self._z80.hl.bits)
        self._z80.ram.write(address, self.reset_nth_bit(bits, n))


class BitResetIndirectAddressIX(BitResetIndirectAddressHL):
    """ RESET b, (IX + d) """

    regexp = compile_re('^1001110111001011((?:0|1){8})11((?:0|1){3})110$')

    def _instruction_logic(self, offset, n):
        address = self._z80.ix.bits + offset
        bits = self._z80.ram.read(address)
        self._z80.ram.write(address, self.reset_nth_bit(bits, n))


class BitResetIndirectAddressIYRegister(BitResetIndirectAddressHL):
    """ RESET b, (IY + d) """

    regexp = compile_re('^1011110111001011((?:0|1){8})11((?:0|1){3})110$')

    def _instruction_logic(self, offset, n):
        address = self._z80.iy.bits + offset
        bits = self._z80.ram.read(address)
        self._z80.ram.write(address, self.reset_nth_bit(bits, n))


class BitResetIndirectAddressIXRegister(Bit):
    """ RESET b, (IX + d), r """

    regexp = compile_re('^1001110111001011((?:0|1){8})11((?:0|1){3})((?:0|1){3})$')

    def _instruction_logic(self, n, offset, selector):
        register = self._select_register(selector)
        address = self._z80.ix.bits + offset
        register.bits = self._z80.ram.read(address)
        register.reset_nth_bit(n)
        self._z80.ram.write(address, register.bits)


class BitResetIndirectAddressIYRegister(Bit):
    """ RESET b, (IY + d), r """

    regexp = compile_re('^1011110111001011((?:0|1){8})11((?:0|1){3})((?:0|1){3})$')

    def _instruction_logic(self, n, offset, selector):
        register = self._select_register(selector)
        address = self._z80.iy.bits + offset
        register.bits = self._z80.ram.read(address)
        register.reset_nth_bit(n)
        self._z80.ram.write(address, register.bits)
