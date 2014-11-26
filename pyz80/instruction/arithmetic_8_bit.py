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
from abc_arithmetic_8_bit import *


""" ADD instructions. """

class AddAR(Add8Bit):
    """ ADD A, r """
    
    regexp = compile_re('^10000((?:0|1){3})$')

    def _instruction_selector(self, selector):
        return self._r_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(AddAR, self)._instruction_logic([self._z80.a.bits, register.bits])


class AddAP(Add8Bit):
    """ ADD A, p """

    regexp = compile_re('^1101110110000((?:0|1){3})$')

    def _instruction_selector(self, selector):
        return self._p_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(AddAP, self)._instruction_logic([self._z80.a.bits, register.bits])


class AddAQ(Add8Bit):
    """ ADD A, q """

    regexp = compile_re('^1111110110000((?:0|1){3})$')

    def _instruction_selector(self, selector):
        return self._q_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(AddAQ, self)._instruction_logic([self._z80.a.bits, register.bits])


class AddAN(Add8Bit):
    """ ADD A, n """

    regexp = compile_re('^11000110((?:0|1){8})$')

    def _instruction_logic(self, n):
        super(AddAN, self)._instruction_logic([self._z80.a.bits, n])


class AddAIndirectAddressHLRegister(AddAIndirectAddress):
    """ ADD A, (HL) """

    regexp = compile_re('^10000110$')

    def _instruction_logic(self):
        address = self._z80.hl.bits
        super(AddAIndirectAddressHLRegister, self)._instruction_logic(address)


class AddAIndirectAddressIXRegister(AddAIndirectAddress):
    """ ADD A, (IX + d) """

    regexp = compile_re('^1101110110000110((?:0|1){8})$')

    def _instruction_logic(self, offset):
        address = self._z80.ix.bits + offset
        super(AddAIndirectAddressIXRegister, self)._instruction_logic(address)


class AddAIndirectAddressIYRegister(AddAIndirectAddress):
    """ ADD A, (IY + d) """

    regexp = compile_re('^1111110110000110((?:0|1){8})$')

    def _instruction_logic(self, offset):
        address = self._z80.iy.bits + offset
        super(AddAIndirectAddressIYRegister, self)._instruction_logic(address)


""" ADC instructions. """

class AdcAR(Add8Bit):
    """ ADC A, r """
    
    regexp = compile_re('^10001((?:0|1){3})$')

    def _instruction_selector(self, selector):
        return self._r_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(AdcAR, self)._instruction_logic(
            [self._z80.a.bits, register.bits, self._z80.f.carry_flag]
        )


class AdcAP(Add8Bit):
    """ ADC A, p """

    regexp = compile_re('^1101110110001((?:0|1){3})$')

    def _instruction_selector(self, selector):
        return self._p_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(AdcAP, self)._instruction_logic(
            [self._z80.a.bits, register.bits, self._z80.f.carry_flag]
        )


class AdcAQ(Add8Bit):
    """ ADC A, q """

    regexp = compile_re('^1111110110001((?:0|1){3})$')

    def _instruction_selector(self, selector):
        return self._q_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(AdcAQ, self)._instruction_logic(
            [self._z80.a.bits, register.bits, self._z80.f.carry_flag]
        )


class AdcAN(Add8Bit):
    """ ADC A, n """

    regexp = compile_re('^11001110((?:0|1){8})$')

    def _instruction_logic(self, n):
        super(AdcAN, self)._instruction_logic(
            [self._z80.a.bits, n, self._z80.f.carry_flag]
        )


class AdcAIndirectAddressHLRegister(AdcAIndirectAddress):
    """ ADC A, (HL) """

    regexp = compile_re('^10001110$')

    def _instruction_logic(self):
        address = self._z80.hl.bits
        super(AdcAIndirectAdcressHLRegister, self)._instruction_logic(address)


class AdcAIndirectAddressIXRegister(AdcAIndirectAddress):
    """ ADC A, (IX + d) """

    regexp = compile_re('^1101110110001110((?:0|1){8})$')

    def _instruction_logic(self, offset):
        address = self._z80.ix.bits + offset
        super(AdcAIndirectAddressIXRegister, self)._instruction_logic(address)


class AdcAIndirectAddressIYRegister(AdcAIndirectAddress):
    """ ADC A, (IY + d) """

    regexp = compile_re('^1111110110001110((?:0|1){8})$')

    def _instruction_logic(self, offset):
        address = self._z80.iy.bits + offset
        super(AdcAIndirectAddressIYRegister, self)._instruction_logic(address)


""" SUB instructions. """

class SubAR(Sub8Bit):
    """ SUB A, r """
    
    regexp = compile_re('^10010((?:0|1){3})$')

    def _instruction_selector(self, selector):
        return self._r_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(SubAR, self)._instruction_logic([self._z80.a.bits, register.bits])


class SubAP(Sub8Bit):
    """ SUB A, p """

    regexp = compile_re('^1101110110010((?:0|1){3})$')

    def _instruction_selector(self, selector):
        return self._p_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(SubAP, self)._instruction_logic([self._z80.a.bits, register.bits])


class SubAQ(Sub8Bit):
    """ SUB A, q """

    regexp = compile_re('^1111110110010((?:0|1){3})$')

    def _instruction_selector(self, selector):
        return self._q_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(SubAQ, self)._instruction_logic([self._z80.a.bits, register.bits])


class SubAN(Sub8Bit):
    """ SUB A, n """

    regexp = compile_re('^11010110((?:0|1){8})$')

    def _instruction_logic(self, n):
        super(SubAN, self)._instruction_logic([self._z80.a.bits, n])


class SubAIndirectAddressHLRegister(SubAIndirectAddress):
    """ SUB A, (HL) """

    regexp = compile_re('^10010110$')

    def _instruction_logic(self):
        address = self._z80.hl.bits
        super(SubAIndirectAddressHLRegister, self)._instruction_logic(address)


class SubAIndirectAddressIXRegister(SubAIndirectAddress):
    """ SUB A, (IX + d) """

    regexp = compile_re('^1101110110010110((?:0|1){8})$')

    def _instruction_logic(self, offset):
        address = self._z80.ix.bits + offset
        super(SubAIndirectAddressIXRegister, self)._instruction_logic(address)


class SubAIndirectAddressIYRegister(SubAIndirectAddress):
    """ SUB A, (IY + d) """

    regexp = compile_re('^1111110110010110((?:0|1){8})$')

    def _instruction_logic(self, offset):
        address = self._z80.iy.bits + offset
        super(SubAIndirectAddressIYRegister, self)._instruction_logic(address)


""" SBC instructions. """

class SbcAR(Sub8Bit):
    """ SBC A, r """
    
    regexp = compile_re('^10011((?:0|1){3})$')

    def _instruction_selector(self, selector):
        return self._r_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(SbcAR, self)._instruction_logic([self._z80.a.bits, register.bits])


class SbcAP(Sub8Bit):
    """ SBC A, p """

    regexp = compile_re('^1101110110011((?:0|1){3})$')

    def _instruction_selector(self, selector):
        return self._p_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(SbcAP, self)._instruction_logic([self._z80.a.bits, register.bits])


class SbcAQ(Sub8Bit):
    """ SBC A, q """

    regexp = compile_re('^1111110110011((?:0|1){3})$')

    def _instruction_selector(self, selector):
        return self._q_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(SbcAQ, self)._instruction_logic([self._z80.a.bits, register.bits])


class SbcAN(Sub8Bit):
    """ SBC A, n """

    regexp = compile_re('^11011110((?:0|1){8})$')

    def _instruction_logic(self, n):
        super(SbcAN, self)._instruction_logic([self._z80.a.bits, n])


class SbcAIndirectAddressHLRegister(SbcAIndirectAddress):
    """ SBC A, (HL) """

    regexp = compile_re('^10011110$')

    def _instruction_logic(self):
        address = self._z80.hl.bits
        super(SbcAIndirectAddressHLRegister, self)._instruction_logic(address)


class SbcAIndirectAddressIXRegister(SbcAIndirectAddress):
    """ SBC A, (IX + d) """

    regexp = compile_re('^1101110110011110((?:0|1){8})$')

    def _instruction_logic(self, offset):
        address = self._z80.ix.bits + offset
        super(SbcAIndirectAddressIXRegister, self)._instruction_logic(address)


class SbcAIndirectAddressIYRegister(SbcAIndirectAddress):
    """ SBC A, (IY + d) """

    regexp = compile_re('^1111110110011110((?:0|1){8})$')

    def _instruction_logic(self, offset):
        address = self._z80.iy.bits + offset
        super(SbcAIndirectAddressIYRegister, self)._instruction_logic(address)
