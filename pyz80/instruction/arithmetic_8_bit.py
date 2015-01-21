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


class AddAIndirectHLR(AddAIndirectAddress):
    """ ADD A, (HL) """

    regexp = compile_re('^10000110$')

    def _instruction_logic(self):
        address = self._z80.hl.bits
        super(AddAIndirectAddressHLRegister, self)._instruction_logic(address)


class AddAIndirectIXR(AddAIndirectAddress):
    """ ADD A, (IX + d) """

    regexp = compile_re('^1101110110000110((?:0|1){8})$')

    def _instruction_logic(self, offset):
        address = self._z80.ix.bits + offset
        super(AddAIndirectAddressIXRegister, self)._instruction_logic(address)


class AddAIndirectIYR(AddAIndirectAddress):
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


class AdcAIndirectHLR(AdcAIndirectAddress):
    """ ADC A, (HL) """

    regexp = compile_re('^10001110$')

    def _instruction_logic(self):
        address = self._z80.hl.bits
        super(AdcAIndirectAdcressHLRegister, self)._instruction_logic(address)


class AdcAIndirectIXR(AdcAIndirectAddress):
    """ ADC A, (IX + d) """

    regexp = compile_re('^1101110110001110((?:0|1){8})$')

    def _instruction_logic(self, offset):
        address = self._z80.ix.bits + offset
        super(AdcAIndirectAddressIXRegister, self)._instruction_logic(address)


class AdcAIndirectIYR(AdcAIndirectAddress):
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


class SubAIndirectHLR(SubAIndirectAddress):
    """ SUB A, (HL) """

    regexp = compile_re('^10010110$')

    def _instruction_logic(self):
        address = self._z80.hl.bits
        super(SubAIndirectAddressHLRegister, self)._instruction_logic(address)


class SubAIndirectIXR(SubAIndirectAddress):
    """ SUB A, (IX + d) """

    regexp = compile_re('^1101110110010110((?:0|1){8})$')

    def _instruction_logic(self, offset):
        address = self._z80.ix.bits + offset
        super(SubAIndirectAddressIXRegister, self)._instruction_logic(address)


class SubAIndirectIYR(SubAIndirectAddress):
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


class SbcAIndirectHLR(SbcAIndirectAddress):
    """ SBC A, (HL) """

    regexp = compile_re('^10011110$')

    def _instruction_logic(self):
        address = self._z80.hl.bits
        super(SbcAIndirectAddressHLRegister, self)._instruction_logic(address)


class SbcAIndirectIXR(SbcAIndirectAddress):
    """ SBC A, (IX + d) """

    regexp = compile_re('^1101110110011110((?:0|1){8})$')

    def _instruction_logic(self, offset):
        address = self._z80.ix.bits + offset
        super(SbcAIndirectAddressIXRegister, self)._instruction_logic(address)


class SbcAIndirectIYR(SbcAIndirectAddress):
    """ SBC A, (IY + d) """

    regexp = compile_re('^1111110110011110((?:0|1){8})$')

    def _instruction_logic(self, offset):
        address = self._z80.iy.bits + offset
        super(SbcAIndirectAddressIYRegister, self)._instruction_logic(address)


""" AND instructions. """

class AndAR(And8Bit):
    """ AND A, r """
    
    regexp = compile_re('^10100((?:0|1){3})$')

    def _instruction_selector(self, selector):
        return self._r_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(AndAR, self)._instruction_logic([self._z80.a.bits, register.bits])


class AndAP(And8Bit):
    """ AND A, p """

    regexp = compile_re('^1101110110100((?:0|1){3})$')

    def _instruction_selector(self, selector):
        return self._p_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(AndAP, self)._instruction_logic([self._z80.a.bits, register.bits])


class AndAQ(And8Bit):
    """ AND A, q """

    regexp = compile_re('^1111110110100((?:0|1){3})$')

    def _instruction_selector(self, selector):
        return self._q_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(AndAQ, self)._instruction_logic([self._z80.a.bits, register.bits])


class AndAN(And8Bit):
    """ AND A, n """

    regexp = compile_re('^11100110((?:0|1){8})$')

    def _instruction_logic(self, n):
        super(AndAN, self)._instruction_logic([self._z80.a.bits, n])


class AndAIndirectHLR(AndAIndirectAddress):
    """ AND A, (HL) """

    regexp = compile_re('^10100110$')

    def _instruction_logic(self):
        address = self._z80.hl.bits
        super(AndAIndirectAddressHLRegister, self)._instruction_logic(address)


class AndAIndirectIXR(AndAIndirectAddress):
    """ AND A, (IX + d) """

    regexp = compile_re('^1101110110100110((?:0|1){8})$')

    def _instruction_logic(self, offset):
        address = self._z80.ix.bits + offset
        super(AndAIndirectAddressIXRegister, self)._instruction_logic(address)


class AndAIndirectIYR(AndAIndirectAddress):
    """ AND A, (IY + d) """

    regexp = compile_re('^1111110110100110((?:0|1){8})$')

    def _instruction_logic(self, offset):
        address = self._z80.iy.bits + offset
        super(AndAIndirectAddressIYRegister, self)._instruction_logic(address)


""" OR instructions. """

class OrAR(Or8Bit):
    """ OR A, r """
    
    regexp = compile_re('^10110((?:0|1){3})$')

    def _instruction_selector(self, selector):
        return self._r_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(OrAR, self)._instruction_logic([self._z80.a.bits, register.bits])


class OrAP(Or8Bit):
    """ OR A, p """

    regexp = compile_re('^1101110110110((?:0|1){3})$')

    def _instruction_selector(self, selector):
        return self._p_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(OrAP, self)._instruction_logic([self._z80.a.bits, register.bits])


class OrAQ(Or8Bit):
    """ OR A, q """

    regexp = compile_re('^1111110110110((?:0|1){3})$')

    def _instruction_selector(self, selector):
        return self._q_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(OrAQ, self)._instruction_logic([self._z80.a.bits, register.bits])


class OrAN(Or8Bit):
    """ OR A, n """

    regexp = compile_re('^11110110((?:0|1){8})$')

    def _instruction_logic(self, n):
        super(OrAN, self)._instruction_logic([self._z80.a.bits, n])


class OrAIndirectHLR(OrAIndirectAddress):
    """ OR A, (HL) """

    regexp = compile_re('^10110110$')

    def _instruction_logic(self):
        address = self._z80.hl.bits
        super(OrAIndirectAddressHLRegister, self)._instruction_logic(address)


class OrAIndirectIXR(OrAIndirectAddress):
    """ OR A, (IX + d) """

    regexp = compile_re('^1101110110110110((?:0|1){8})$')

    def _instruction_logic(self, offset):
        address = self._z80.ix.bits + offset
        super(OrAIndirectAddressIXRegister, self)._instruction_logic(address)


class OrAIndirectIYR(OrAIndirectAddress):
    """ OR A, (IY + d) """

    regexp = compile_re('^1111110110110110((?:0|1){8})$')

    def _instruction_logic(self, offset):
        address = self._z80.iy.bits + offset
        super(OrAIndirectAddressIYRegister, self)._instruction_logic(address)


""" XOR instructions. """

class XorAR(Xor8Bit):
    """ XOR A, r """
    
    regexp = compile_re('^10101((?:0|1){3})$')

    def _instruction_selector(self, selector):
        return self._r_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(XorAR, self)._instruction_logic([self._z80.a.bits, register.bits])


class XorAP(Xor8Bit):
    """ XOR A, p """

    regexp = compile_re('^1101110110101((?:0|1){3})$')

    def _instruction_selector(self, selector):
        return self._p_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(XorAP, self)._instruction_logic([self._z80.a.bits, register.bits])


class XorAQ(Xor8Bit):
    """ XOR A, q """

    regexp = compile_re('^1111110110101((?:0|1){3})$')

    def _instruction_selector(self, selector):
        return self._q_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(XorAQ, self)._instruction_logic([self._z80.a.bits, register.bits])


class XorAN(Xor8Bit):
    """ XOR A, n """

    regexp = compile_re('^11101110((?:0|1){8})$')

    def _instruction_logic(self, n):
        super(XorAN, self)._instruction_logic([self._z80.a.bits, n])


class XorAIndirectHLR(XorAIndirectAddress):
    """ XOR A, (HL) """

    regexp = compile_re('^10101110$')

    def _instruction_logic(self):
        address = self._z80.hl.bits
        super(XorAIndirectAddressHLRegister, self)._instruction_logic(address)


class XorAIndirectIXR(XorAIndirectAddress):
    """ XOR A, (IX + d) """

    regexp = compile_re('^1101110110101110((?:0|1){8})$')

    def _instruction_logic(self, offset):
        address = self._z80.ix.bits + offset
        super(XorAIndirectAddressIXRegister, self)._instruction_logic(address)


class XorAIndirectIYR(XorAIndirectAddress):
    """ XOR A, (IY + d) """

    regexp = compile_re('^1111110110101110((?:0|1){8})$')

    def _instruction_logic(self, offset):
        address = self._z80.iy.bits + offset
        super(XorAIndirectAddressIYRegister, self)._instruction_logic(address)


""" CP instructions. """

class CpAR(Cp8Bit):
    """ CP A, r """
    
    regexp = compile_re('^10111((?:0|1){3})$')

    def _instruction_selector(self, selector):
        return self._r_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(CpAR, self)._instruction_logic([self._z80.a.bits, register.bits])


class CpAP(Cp8Bit):
    """ CP A, p """

    regexp = compile_re('^1101110110111((?:0|1){3})$')

    def _instruction_selector(self, selector):
        return self._p_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(CpAP, self)._instruction_logic([self._z80.a.bits, register.bits])


class CpAQ(Cp8Bit):
    """ CP A, q """

    regexp = compile_re('^1111110110111((?:0|1){3})$')

    def _instruction_selector(self, selector):
        return self._q_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(CpAQ, self)._instruction_logic([self._z80.a.bits, register.bits])


class CpAN(Cp8Bit):
    """ CP A, n """

    regexp = compile_re('^11111110((?:0|1){8})$')

    def _instruction_logic(self, n):
        super(CpAN, self)._instruction_logic([self._z80.a.bits, n])


class CpAIndirectHLR(CpAIndirectAddress):
    """ CP A, (HL) """

    regexp = compile_re('^10111110$')

    def _instruction_logic(self):
        address = self._z80.hl.bits
        super(CpAIndirectAddressHLRegister, self)._instruction_logic(address)


class CpAIndirectIXR(CpAIndirectAddress):
    """ CP A, (IX + d) """

    regexp = compile_re('^1101110110111110((?:0|1){8})$')

    def _instruction_logic(self, offset):
        address = self._z80.ix.bits + offset
        super(CpAIndirectAddressIXRegister, self)._instruction_logic(address)


class CpAIndirectIYR(CpAIndirectAddress):
    """ CP A, (IY + d) """

    regexp = compile_re('^1111110110111110((?:0|1){8})$')

    def _instruction_logic(self, offset):
        address = self._z80.iy.bits + offset
        super(CpAIndirectAddressIYRegister, self)._instruction_logic(address)


""" INC instructions. """

class IncAR(Inc8Bit):
    """ INC A, r """
    
    regexp = compile_re('^00((?:0|1){3})100$')

    def _instruction_selector(self, selector):
        return self._r_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(IncAR, self)._instruction_logic([self._z80.a.bits, 1])


class IncAP(Inc8Bit):
    """ INC A, p """

    regexp = compile_re('^1101110100((?:0|1){3})100$')

    def _instruction_selector(self, selector):
        return self._p_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(IncAP, self)._instruction_logic([self._z80.a.bits, 1])


class IncAQ(Inc8Bit):
    """ INC A, q """

    regexp = compile_re('^1111110100((?:0|1){3})100$')

    def _instruction_selector(self, selector):
        return self._q_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(IncAQ, self)._instruction_logic([self._z80.a.bits, 1])


class IncIndirectHLR(IncIndirectAddress):
    """ INC (HL) """

    regexp = compile_re('^00110100$')

    def _instruction_logic(self):
        address = self._z80.hl.bits
        super(IncAIndirectAddressHLRegister, self)._instruction_logic(address)


class IncIndirectIXR(IncIndirectAddress):
    """ INC (IX + d) """

    regexp = compile_re('^1101110100110100((?:0|1){8})$')

    def _instruction_logic(self, offset):
        address = self._z80.ix.bits + offset
        super(IncAIndirectAddressIXRegister, self)._instruction_logic(address)


class IncIndirectIYR(IncIndirectAddress):
    """ INC (IY + d) """

    regexp = compile_re('^1111110100110100((?:0|1){8})$')

    def _instruction_logic(self, offset):
        address = self._z80.iy.bits + offset
        super(IncAIndirectAddressIYRegister, self)._instruction_logic(address)


""" DEC instructions. """

class DecAR(Dec8Bit):
    """ DEC A, r """
    
    regexp = compile_re('^00((?:0|1){3})101$')

    def _instruction_selector(self, selector):
        return self._r_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(DecAR, self)._instruction_logic([self._z80.a.bits, 1])


class DecAP(Dec8Bit):
    """ DEC A, p """

    regexp = compile_re('^1101110100((?:0|1){3})101$')

    def _instruction_selector(self, selector):
        return self._p_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(DecAP, self)._instruction_logic([self._z80.a.bits, 1])


class DecAQ(Dec8Bit):
    """ DEC A, q """

    regexp = compile_re('^1111110100((?:0|1){3})101$')

    def _instruction_selector(self, selector):
        return self._q_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(DecAQ, self)._instruction_logic([self._z80.a.bits, 1])


class DecIndirectHLR(DecIndirectAddress):
    """ DEC (HL) """

    regexp = compile_re('^00110101$')

    def _instruction_logic(self):
        address = self._z80.hl.bits
        super(DecAIndirectAddressHLRegister, self)._instruction_logic(address)


class DecIndirectIXR(DecIndirectAddress):
    """ DEC (IX + d) """

    regexp = compile_re('^1101110100110101((?:0|1){8})$')

    def _instruction_logic(self, offset):
        address = self._z80.ix.bits + offset
        super(DecAIndirectAddressIXRegister, self)._instruction_logic(address)


class DecIndirectIYR(DecIndirectAddress):
    """ DEC (IY + d) """

    regexp = compile_re('^1111110100110101((?:0|1){8})$')

    def _instruction_logic(self, offset):
        address = self._z80.iy.bits + offset
        super(DecAIndirectAddressIYRegister, self)._instruction_logic(address)
