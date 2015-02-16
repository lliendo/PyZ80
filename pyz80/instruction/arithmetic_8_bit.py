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

    def _message_log(self, selector):
        register = self._select_register(selector)
        return 'ADD A, {:}'.format(register.label)

    def _instruction_selector(self, selector):
        return self._r_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(AddAR, self)._instruction_logic([self._z80.a.bits, register.bits])


class AddAP(Add8Bit):
    """ ADD A, p """

    regexp = compile_re('^1101110110000((?:0|1){3})$')

    def _message_log(self, selector):
        register = self._select_register(selector)
        return 'ADD A, {:}'.format(register.label)

    def _instruction_selector(self, selector):
        return self._p_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(AddAP, self)._instruction_logic([self._z80.a.bits, register.bits])


class AddAQ(Add8Bit):
    """ ADD A, q """

    regexp = compile_re('^1111110110000((?:0|1){3})$')

    def _message_log(self, selector):
        register = self._select_register(selector)
        return 'ADD A, {:}'.format(register.label)

    def _instruction_selector(self, selector):
        return self._q_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(AddAQ, self)._instruction_logic([self._z80.a.bits, register.bits])


class AddAN(Add8Bit):
    """ ADD A, n """

    regexp = compile_re('^11000110((?:0|1){8})$')

    def _message_log(self, n):
        return 'ADD A, {:02X}'.format(n)

    def _instruction_logic(self, n):
        super(AddAN, self)._instruction_logic([self._z80.a.bits, n])


class AddAIndirectHL(AddAIndirectAddress):
    """ ADD A, (HL) """

    regexp = compile_re('^10000110$')

    def _message_log(self):
        return 'ADD A, (HL)'

    def _instruction_logic(self):
        address = self._z80.hl.bits
        super(AddAIndirectHL, self)._instruction_logic(address)


class AddAIndirectIX(AddAIndirectAddress):
    """ ADD A, (IX + d) """

    regexp = compile_re('^1101110110000110((?:0|1){8})$')

    def _message_log(self, offset):
        return 'ADD A, (IX + {:02X})'.format(offset)

    def _instruction_logic(self, offset):
        address = self._z80.ix.bits + offset
        super(AddAIndirectIX, self)._instruction_logic(address)


class AddAIndirectIY(AddAIndirectAddress):
    """ ADD A, (IY + d) """

    regexp = compile_re('^1111110110000110((?:0|1){8})$')

    def _message_log(self, offset):
        return 'ADD A, (IY + {:02X})'.format(offset)

    def _instruction_logic(self, offset):
        address = self._z80.iy.bits + offset
        super(AddAIndirectIY, self)._instruction_logic(address)


""" ADC instructions. """

class AdcAR(Add8Bit):
    """ ADC A, r """

    regexp = compile_re('^10001((?:0|1){3})$')

    def _message_log(self, selector):
        register = self._select_register(selector)
        return 'ADC A, {:}'.format(register.label)

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

    def _message_log(self, selector):
        register = self._select_register(selector)
        return 'ADC A, {:}'.format(register.label)

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

    def _message_log(self, selector):
        register = self._select_register(selector)
        return 'ADC A, {:}'.format(register.label)

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

    def _message_log(self, n):
        return 'ADC A, {:02X}'.format(n)

    def _instruction_logic(self, n):
        super(AdcAN, self)._instruction_logic(
            [self._z80.a.bits, n, self._z80.f.carry_flag]
        )


class AdcAIndirectHL(AdcAIndirectAddress):
    """ ADC A, (HL) """

    regexp = compile_re('^10001110$')

    def _message_log(self):
        return 'ADC A, (HL)'

    def _instruction_logic(self):
        address = self._z80.hl.bits
        super(AdcAIndirectHL, self)._instruction_logic(address)


class AdcAIndirectIX(AdcAIndirectAddress):
    """ ADC A, (IX + d) """

    regexp = compile_re('^1101110110001110((?:0|1){8})$')

    def _message_log(self, offset):
        return 'ADC A, (IX + {:02X})'.format(offset)

    def _instruction_logic(self, offset):
        address = self._z80.ix.bits + offset
        super(AdcAIndirectIX, self)._instruction_logic(address)


class AdcAIndirectIY(AdcAIndirectAddress):
    """ ADC A, (IY + d) """

    regexp = compile_re('^1111110110001110((?:0|1){8})$')

    def _message_log(self, offset):
        return 'ADC A, (IY + {:02X})'.format(offset)

    def _instruction_logic(self, offset):
        address = self._z80.iy.bits + offset
        super(AdcAIndirectIY, self)._instruction_logic(address)


""" SUB instructions. """

class SubAR(Sub8Bit):
    """ SUB A, r """

    regexp = compile_re('^10010((?:0|1){3})$')

    def _message_log(self, selector):
        register = self._select_register(selector)
        return 'SUB A, {:}'.format(register.label)

    def _instruction_selector(self, selector):
        return self._r_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(SubAR, self)._instruction_logic([self._z80.a.bits, register.bits])


class SubAP(Sub8Bit):
    """ SUB A, p """

    regexp = compile_re('^1101110110010((?:0|1){3})$')

    def _message_log(self, selector):
        register = self._select_register(selector)
        return 'SUB A, {:}'.format(register.label)

    def _instruction_selector(self, selector):
        return self._p_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(SubAP, self)._instruction_logic([self._z80.a.bits, register.bits])


class SubAQ(Sub8Bit):
    """ SUB A, q """

    regexp = compile_re('^1111110110010((?:0|1){3})$')

    def _message_log(self, selector):
        register = self._select_register(selector)
        return 'SUB A, {:}'.format(register.label)

    def _instruction_selector(self, selector):
        return self._q_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(SubAQ, self)._instruction_logic([self._z80.a.bits, register.bits])


class SubAN(Sub8Bit):
    """ SUB A, n """

    regexp = compile_re('^11010110((?:0|1){8})$')

    def _message_log(self, n):
        return 'SUB A, {:02X}'.format(n)

    def _instruction_logic(self, n):
        super(SubAN, self)._instruction_logic([self._z80.a.bits, n])


class SubAIndirectHL(SubAIndirectAddress):
    """ SUB A, (HL) """

    regexp = compile_re('^10010110$')

    def _message_log(self):
        return 'SUB A, (HL)'

    def _instruction_logic(self):
        address = self._z80.hl.bits
        super(SubAIndirectHL, self)._instruction_logic(address)


class SubAIndirectIX(SubAIndirectAddress):
    """ SUB A, (IX + d) """

    regexp = compile_re('^1101110110010110((?:0|1){8})$')

    def _message_log(self, offset):
        return 'SUB A, (IX + {:02X})'.format(offset)

    def _instruction_logic(self, offset):
        address = self._z80.ix.bits + offset
        super(SubAIndirectIX, self)._instruction_logic(address)


class SubAIndirectIY(SubAIndirectAddress):
    """ SUB A, (IY + d) """

    regexp = compile_re('^1111110110010110((?:0|1){8})$')

    def _message_log(self, offset):
        return 'SUB A, (IY + {:02X})'.format(offset)

    def _instruction_logic(self, offset):
        address = self._z80.iy.bits + offset
        super(SubAIndirectIY, self)._instruction_logic(address)


""" SBC instructions. """

class SbcAR(Sub8Bit):
    """ SBC A, r """

    regexp = compile_re('^10011((?:0|1){3})$')

    def _message_log(self, selector):
        register = self._select_register(selector)
        return 'SBC A, {:}'.format(register.label)

    def _instruction_selector(self, selector):
        return self._r_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(SbcAR, self)._instruction_logic([self._z80.a.bits, register.bits])


class SbcAP(Sub8Bit):
    """ SBC A, p """

    regexp = compile_re('^1101110110011((?:0|1){3})$')

    def _message_log(self, selector):
        register = self._select_register(selector)
        return 'SBC A, {:}'.format(register.label)

    def _instruction_selector(self, selector):
        return self._p_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(SbcAP, self)._instruction_logic([self._z80.a.bits, register.bits])


class SbcAQ(Sub8Bit):
    """ SBC A, q """

    regexp = compile_re('^1111110110011((?:0|1){3})$')

    def _message_log(self, selector):
        register = self._select_register(selector)
        return 'SBC A, {:}'.format(register.label)

    def _instruction_selector(self, selector):
        return self._q_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(SbcAQ, self)._instruction_logic([self._z80.a.bits, register.bits])


class SbcAN(Sub8Bit):
    """ SBC A, n """

    regexp = compile_re('^11011110((?:0|1){8})$')

    def _message_log(self, n):
        return 'SBC A, {:02X}'.format(n)

    def _instruction_logic(self, n):
        super(SbcAN, self)._instruction_logic([self._z80.a.bits, n])


class SbcAIndirectHL(SbcAIndirectAddress):
    """ SBC A, (HL) """

    regexp = compile_re('^10011110$')

    def _message_log(self):
        return 'SBC A, (HL)'

    def _instruction_logic(self):
        address = self._z80.hl.bits
        super(SbcAIndirectHL, self)._instruction_logic(address)


class SbcAIndirectIX(SbcAIndirectAddress):
    """ SBC A, (IX + d) """

    regexp = compile_re('^1101110110011110((?:0|1){8})$')

    def _message_log(self, offset):
        return 'SBC A, (IX + {:02X})'.format(offset)

    def _instruction_logic(self, offset):
        address = self._z80.ix.bits + offset
        super(SbcAIndirectIX, self)._instruction_logic(address)


class SbcAIndirectIY(SbcAIndirectAddress):
    """ SBC A, (IY + d) """

    regexp = compile_re('^1111110110011110((?:0|1){8})$')

    def _message_log(self, offset):
        return 'SBC A, (IY + {:02X})'.format(offset)

    def _instruction_logic(self, offset):
        address = self._z80.iy.bits + offset
        super(SbcAIndirectIY, self)._instruction_logic(address)


""" AND instructions. """

class AndAR(And8Bit):
    """ AND A, r """

    regexp = compile_re('^10100((?:0|1){3})$')

    def _message_log(self, selector):
        register = self._select_register(selector)
        return 'AND A, {:}'.format(register.label)

    def _instruction_selector(self, selector):
        return self._r_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(AndAR, self)._instruction_logic([self._z80.a.bits, register.bits])


class AndAP(And8Bit):
    """ AND A, p """

    regexp = compile_re('^1101110110100((?:0|1){3})$')

    def _message_log(self, selector):
        register = self._select_register(selector)
        return 'AND A, {:}'.format(register.label)

    def _instruction_selector(self, selector):
        return self._p_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(AndAP, self)._instruction_logic([self._z80.a.bits, register.bits])


class AndAQ(And8Bit):
    """ AND A, q """

    regexp = compile_re('^1111110110100((?:0|1){3})$')

    def _message_log(self, selector):
        register = self._select_register(selector)
        return 'AND A, {:}'.format(register.label)

    def _instruction_selector(self, selector):
        return self._q_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(AndAQ, self)._instruction_logic([self._z80.a.bits, register.bits])


class AndAN(And8Bit):
    """ AND A, n """

    regexp = compile_re('^11100110((?:0|1){8})$')

    def _message_log(self, n):
        return 'AND A, {:02X}'.format(n)

    def _instruction_logic(self, n):
        super(AndAN, self)._instruction_logic([self._z80.a.bits, n])


class AndAIndirectHL(AndAIndirectAddress):
    """ AND A, (HL) """

    regexp = compile_re('^10100110$')

    def _message_log(self):
        return 'AND A, (HL)'

    def _instruction_logic(self):
        address = self._z80.hl.bits
        super(AndAIndirectHL, self)._instruction_logic(address)


class AndAIndirectIX(AndAIndirectAddress):
    """ AND A, (IX + d) """

    regexp = compile_re('^1101110110100110((?:0|1){8})$')

    def _message_log(self, offset):
        return 'AND A, (IX + {:02X})'.format(offset)

    def _instruction_logic(self, offset):
        address = self._z80.ix.bits + offset
        super(AndAIndirectIX, self)._instruction_logic(address)


class AndAIndirectIY(AndAIndirectAddress):
    """ AND A, (IY + d) """

    regexp = compile_re('^1111110110100110((?:0|1){8})$')

    def _message_log(self, offset):
        return 'AND A, (IY + {:02X})'.format(offset)

    def _instruction_logic(self, offset):
        address = self._z80.iy.bits + offset
        super(AndAIndirectIY, self)._instruction_logic(address)


""" OR instructions. """

class OrAR(Or8Bit):
    """ OR A, r """

    regexp = compile_re('^10110((?:0|1){3})$')

    def _message_log(self, selector):
        register = self._select_register(selector)
        return 'OR A, {:}'.format(register.label)

    def _instruction_selector(self, selector):
        return self._r_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(OrAR, self)._instruction_logic([self._z80.a.bits, register.bits])


class OrAP(Or8Bit):
    """ OR A, p """

    regexp = compile_re('^1101110110110((?:0|1){3})$')

    def _message_log(self, selector):
        register = self._select_register(selector)
        return 'OR A, {:}'.format(register.label)

    def _instruction_selector(self, selector):
        return self._p_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(OrAP, self)._instruction_logic([self._z80.a.bits, register.bits])


class OrAQ(Or8Bit):
    """ OR A, q """

    regexp = compile_re('^1111110110110((?:0|1){3})$')

    def _message_log(self, selector):
        register = self._select_register(selector)
        return 'OR A, {:}'.format(register.label)

    def _instruction_selector(self, selector):
        return self._q_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(OrAQ, self)._instruction_logic([self._z80.a.bits, register.bits])


class OrAN(Or8Bit):
    """ OR A, n """

    regexp = compile_re('^11110110((?:0|1){8})$')

    def _message_log(self, n):
        return 'OR A, {:02X}'.format(n)

    def _instruction_logic(self, n):
        super(OrAN, self)._instruction_logic([self._z80.a.bits, n])


class OrAIndirectHL(OrAIndirectAddress):
    """ OR A, (HL) """

    regexp = compile_re('^10110110$')

    def _message_log(self):
        return 'OR (HL)'

    def _instruction_logic(self):
        address = self._z80.hl.bits
        super(OrAIndirectHL, self)._instruction_logic(address)


class OrAIndirectIX(OrAIndirectAddress):
    """ OR A, (IX + d) """

    regexp = compile_re('^1101110110110110((?:0|1){8})$')

    def _message_log(self, offset):
        return 'OR A, (IX + {:02X})'.format(offset)

    def _instruction_logic(self, offset):
        address = self._z80.ix.bits + offset
        super(OrAIndirectIX, self)._instruction_logic(address)


class OrAIndirectIY(OrAIndirectAddress):
    """ OR A, (IY + d) """

    regexp = compile_re('^1111110110110110((?:0|1){8})$')

    def _message_log(self, offset):
        return 'OR A, (IY + {:02X})'.format(offset)

    def _instruction_logic(self, offset):
        address = self._z80.iy.bits + offset
        super(OrAIndirectIY, self)._instruction_logic(address)


""" XOR instructions. """

class XorAR(Xor8Bit):
    """ XOR A, r """

    regexp = compile_re('^10101((?:0|1){3})$')

    def _message_log(self, selector):
        register = self._select_register(selector)
        return 'XOR A, {:}'.format(register.label)

    def _instruction_selector(self, selector):
        return self._r_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(XorAR, self)._instruction_logic([self._z80.a.bits, register.bits])


class XorAP(Xor8Bit):
    """ XOR A, p """

    regexp = compile_re('^1101110110101((?:0|1){3})$')

    def _message_log(self, selector):
        register = self._select_register(selector)
        return 'XOR A, {:}'.format(register.label)

    def _instruction_selector(self, selector):
        return self._p_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(XorAP, self)._instruction_logic([self._z80.a.bits, register.bits])


class XorAQ(Xor8Bit):
    """ XOR A, q """

    regexp = compile_re('^1111110110101((?:0|1){3})$')

    def _message_log(self, selector):
        register = self._select_register(selector)
        return 'XOR A, {:}'.format(register.label)

    def _instruction_selector(self, selector):
        return self._q_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(XorAQ, self)._instruction_logic([self._z80.a.bits, register.bits])


class XorAN(Xor8Bit):
    """ XOR A, n """

    regexp = compile_re('^11101110((?:0|1){8})$')

    def _message_log(self, n):
        return 'XOR A, {:02X}'.format(n)

    def _instruction_logic(self, n):
        super(XorAN, self)._instruction_logic([self._z80.a.bits, n])


class XorAIndirectHL(XorAIndirectAddress):
    """ XOR A, (HL) """

    regexp = compile_re('^10101110$')

    def _message_log(self):
        return 'XOR A, (HL)'

    def _instruction_logic(self):
        address = self._z80.hl.bits
        super(XorAIndirectHL, self)._instruction_logic(address)


class XorAIndirectIX(XorAIndirectAddress):
    """ XOR A, (IX + d) """

    regexp = compile_re('^1101110110101110((?:0|1){8})$')

    def _message_log(self, offset):
        return 'XOR A, (IX + {:02X})'.format(offset)

    def _instruction_logic(self, offset):
        address = self._z80.ix.bits + offset
        super(XorAIndirectIX, self)._instruction_logic(address)


class XorAIndirectIY(XorAIndirectAddress):
    """ XOR A, (IY + d) """

    regexp = compile_re('^1111110110101110((?:0|1){8})$')

    def _message_log(self, offset):
        return 'XOR A, (IY + {:02X})'.format(offset)

    def _instruction_logic(self, offset):
        address = self._z80.iy.bits + offset
        super(XorAIndirectIY, self)._instruction_logic(address)


""" CP instructions. """

class CpAR(Cp8Bit):
    """ CP A, r """

    regexp = compile_re('^10111((?:0|1){3})$')

    def _message_log(self, selector):
        register = self._select_register(selector)
        return 'CP A, {:}'.format(register.label)

    def _instruction_selector(self, selector):
        return self._r_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(CpAR, self)._instruction_logic([self._z80.a.bits, register.bits])


class CpAP(Cp8Bit):
    """ CP A, p """

    regexp = compile_re('^1101110110111((?:0|1){3})$')

    def _message_log(self, selector):
        register = self._select_register(selector)
        return 'CP A, {:}'.format(register.label)

    def _instruction_selector(self, selector):
        return self._p_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(CpAP, self)._instruction_logic([self._z80.a.bits, register.bits])


class CpAQ(Cp8Bit):
    """ CP A, q """

    regexp = compile_re('^1111110110111((?:0|1){3})$')

    def _message_log(self, selector):
        register = self._select_register(selector)
        return 'CP A, {:}'.format(register.label)

    def _instruction_selector(self, selector):
        return self._q_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(CpAQ, self)._instruction_logic([self._z80.a.bits, register.bits])


class CpAN(Cp8Bit):
    """ CP A, n """

    regexp = compile_re('^11111110((?:0|1){8})$')

    def _message_log(self, n):
        return 'CP A, {:02X}'.format(n)

    def _instruction_logic(self, n):
        super(CpAN, self)._instruction_logic([self._z80.a.bits, n])


class CpAIndirectHL(CpAIndirectAddress):
    """ CP A, (HL) """

    regexp = compile_re('^10111110$')

    def _message_log(self):
        return 'CP A, (HL)'

    def _instruction_logic(self):
        address = self._z80.hl.bits
        super(CpAIndirectHL, self)._instruction_logic(address)


class CpAIndirectIX(CpAIndirectAddress):
    """ CP A, (IX + d) """

    regexp = compile_re('^1101110110111110((?:0|1){8})$')

    def _message_log(self, offset):
        return 'CP A, (IX + {:02X})'.format(offset)

    def _instruction_logic(self, offset):
        address = self._z80.ix.bits + offset
        super(CpAIndirectIX, self)._instruction_logic(address)


class CpAIndirectIY(CpAIndirectAddress):
    """ CP A, (IY + d) """

    regexp = compile_re('^1111110110111110((?:0|1){8})$')

    def _message_log(self, offset):
        return 'CP A, (IY + {:02X})'.format(offset)

    def _instruction_logic(self, offset):
        address = self._z80.iy.bits + offset
        super(CpAIndirectIY, self)._instruction_logic(address)


""" INC instructions. """

class IncAR(Inc8Bit):
    """ INC A, r """

    regexp = compile_re('^00((?:0|1){3})100$')

    def _message_log(self, selector):
        register = self._select_register(selector)
        return 'INC A, {:}'.format(register.label)

    def _instruction_selector(self, selector):
        return self._r_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(IncAR, self)._instruction_logic([self._z80.a.bits, 1])


class IncAP(Inc8Bit):
    """ INC A, p """

    regexp = compile_re('^1101110100((?:0|1){3})100$')

    def _message_log(self, selector):
        register = self._select_register(selector)
        return 'INC A, {:}'.format(register.label)

    def _instruction_selector(self, selector):
        return self._p_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(IncAP, self)._instruction_logic([self._z80.a.bits, 1])


class IncAQ(Inc8Bit):
    """ INC A, q """

    regexp = compile_re('^1111110100((?:0|1){3})100$')

    def _message_log(self, selector):
        register = self._select_register(selector)
        return 'INC A, {:}'.format(register.label)

    def _instruction_selector(self, selector):
        return self._q_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(IncAQ, self)._instruction_logic([self._z80.a.bits, 1])


class IncIndirectHL(IncIndirectAddress):
    """ INC (HL) """

    regexp = compile_re('^00110100$')

    def _message_log(self):
        return 'INC (HL)'

    def _instruction_logic(self):
        address = self._z80.hl.bits
        super(IncIndirectHL, self)._instruction_logic(address)


class IncIndirectIX(IncIndirectAddress):
    """ INC (IX + d) """

    regexp = compile_re('^1101110100110100((?:0|1){8})$')

    def _message_log(self, offset):
        return 'INC (IX + {:02X})'.format(offset)

    def _instruction_logic(self, offset):
        address = self._z80.ix.bits + offset
        super(IncIndirectIX, self)._instruction_logic(address)


class IncIndirectIY(IncIndirectAddress):
    """ INC (IY + d) """

    regexp = compile_re('^1111110100110100((?:0|1){8})$')

    def _message_log(self, offset):
        return 'INC (IY + {:02X})'.format(offset)

    def _instruction_logic(self, offset):
        address = self._z80.iy.bits + offset
        super(IncIndirectIY, self)._instruction_logic(address)


""" DEC instructions. """

class DecAR(Dec8Bit):
    """ DEC A, r """

    regexp = compile_re('^00((?:0|1){3})101$')

    def _message_log(self, selector):
        register = self._select_register(selector)
        return 'DEC A, {:}'.format(register.label)

    def _instruction_selector(self, selector):
        return self._r_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(DecAR, self)._instruction_logic([self._z80.a.bits, 1])


class DecAP(Dec8Bit):
    """ DEC A, p """

    regexp = compile_re('^1101110100((?:0|1){3})101$')

    def _message_log(self, selector):
        register = self._select_register(selector)
        return 'DEC A, {:}'.format(register.label)

    def _instruction_selector(self, selector):
        return self._p_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(DecAP, self)._instruction_logic([self._z80.a.bits, 1])


class DecAQ(Dec8Bit):
    """ DEC A, q """

    regexp = compile_re('^1111110100((?:0|1){3})101$')

    def _message_log(self, selector):
        register = self._select_register(selector)
        return 'DEC A, {:}'.format(register.label)

    def _instruction_selector(self, selector):
        return self._q_selector(selector)

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(DecAQ, self)._instruction_logic([self._z80.a.bits, 1])


class DecIndirectHL(DecIndirectAddress):
    """ DEC (HL) """

    regexp = compile_re('^00110101$')

    def _message_log(self):
        return 'DEC (HL)'

    def _instruction_logic(self):
        address = self._z80.hl.bits
        super(DecIndirectHL, self)._instruction_logic(address)


class DecIndirectIX(DecIndirectAddress):
    """ DEC (IX + d) """

    regexp = compile_re('^1101110100110101((?:0|1){8})$')

    def _message_log(self, offset):
        return 'DEC (IX + {:02X})'.format(offset)

    def _instruction_logic(self, offset):
        address = self._z80.ix.bits + offset
        super(DecIndirectIX, self)._instruction_logic(address)


class DecIndirectIY(DecIndirectAddress):
    """ DEC (IY + d) """

    regexp = compile_re('^1111110100110101((?:0|1){8})$')

    def _message_log(self, offset):
        return 'DEC (IY + {:02X})'.format(offset)

    def _instruction_logic(self, offset):
        address = self._z80.iy.bits + offset
        super(DecIndirectIY, self)._instruction_logic(address)
