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
from abc_rotate_and_shift import *


""" RLC instructions. """

class Rlca(RotateLeftWithCarry):
    """ RLCA """

    regexp = compile_re('^00000111$')

    def _update_sign_flag(register):
        pass

    def _update_zero_flag(register):
        pass

    def _update_parity_flag(register):
        pass

    def _instruction_logic(self):
        super(Rlca, self)._instruction_logic(self._z80.a)


class RlcR(RotateLeftWithCarry):
    """ RLC r """

    regexp = compile_re('^1100101100000((?:0|1){3})$')

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(RlcR, self)._instruction_logic(register)


class RlcIndirectAddressHL(RlcIndirectAddress):
    """ RLC (HL) """

    regexp = compile_re('^1100101100000110$')

    def _instruction_logic(self):
        address = self._z80.hl.bits
        super(RlcIndirectAddressHL, self)._instruction_logic(address)


class RlcIndirectAddressIX(RlcIndirectAddress):
    """ RLC (IX + d) """

    regexp = compile_re('^1101110111001011((?:0|1){8})00000110$')

    def _instruction_logic(self, offset):
        address = self._z80.ix.bits + offset
        super(RlcIndirectAddressIX, self)._instruction_logic(address)


class RlcIndirectAddressIY(RlcIndirectAddress):
    """ RLC (IY + d) """

    regexp = compile_re('^1111110111001011((?:0|1){8})00000110$')

    def _instruction_logic(self, offset):
        address = self._z80.iy.bits + offset
        super(RlcIndirectAddressIY, self)._instruction_logic(address)


class RlcIndirectAddressIXR(RlcIndirectAddress):
    """ RLC (IX + d), r """

    regexp = compile_re('^1101110111001011((?:0|1){8})00000((?:0|1){3})$')

    def _instruction_logic(self, offset, selector):
        address = self._z80.ix.bits + offset
        register = self._select_register(selector)
        register.bits = super(RlcIndirectAddressIXR, self)._instruction_logic(address).bits


class RlcIndirectAddressIYR(RlcIndirectAddress):
    """ RLC (IY + d), r """

    regexp = compile_re('^1111110111001011((?:0|1){8})00000((?:0|1){3})$')

    def _instruction_logic(self, offset, selector):
        address = self._z80.iy.bits + offset
        register = self._select_register(selector)
        register.bits = super(RlcIndirectAddressIYR, self)._instruction_logic(address).bits


""" RRC instructions. """

class Rrca(RotateRightWithCarry):
    """ RRCA """

    regexp = compile_re('^00001111$')

    def _update_sign_flag(register):
        pass

    def _update_zero_flag(register):
        pass

    def _update_parity_flag(register):
        pass

    def _instruction_logic(self):
        super(Rrca, self)._instruction_logic(self._z80.a)


class RrcR(RotateRightWithCarry):
    """ RRC r """

    regexp = compile_re('^1100101100001((?:0|1){3})$')

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(RrcR, self)._instruction_logic(register)


class RrcIndirectAddressHL(RrcIndirectAddress):
    """ RRC (HL) """

    regexp = compile_re('^1100101100001110$')

    def _instruction_logic(self):
        address = self._z80.hl.bits
        super(RrcIndirectAddressHL, self)._instruction_logic(address)


class RrcIndirectAddressIX(RrcIndirectAddress):
    """ RRC (IX + d) """

    regexp = compile_re('^1101110111001011((?:0|1){8})00001110$')

    def _instruction_logic(self, offset):
        address = self._z80.ix.bits + offset
        super(RrcIndirectAddressIX, self)._instruction_logic(address)


class RrcIndirectAddressIY(RrcIndirectAddress):
    """ RRC (IY + d) """

    regexp = compile_re('^1111110111001011((?:0|1){8})00001110$')

    def _instruction_logic(self, offset):
        address = self._z80.iy.bits + offset
        super(RrcIndirectAddressIY, self)._instruction_logic(address)


""" RL instructions. """

class Rla(RotateLeftThroughCarry):
    """ RLA """

    regexp = compile_re('^00010111$')

    def _update_sign_flag(register):
        pass

    def _update_zero_flag(register):
        pass

    def _update_parity_flag(register):
        pass

    def _instruction_logic(self):
        super(Rla, self)._instruction_logic(self._z80.a)


class RlR(RotateLeftThroughCarry):
    """ RL r """

    regexp = compile_re('^1100101100010((?:0|1){3})$')

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(RlR, self)._instruction_logic(register)


class RlIndirectAddressHL(RlIndirectAddress):
    """ RL (HL) """

    regexp = compile_re('^1100101100010110$')

    def _instruction_logic(self):
        address = self._z80.hl.bits
        super(RlIndirectAddressHL, self)._instruction_logic(address)


class RlIndirectAddressIX(RlIndirectAddress):
    """ RL (IX + d) """

    regexp = compile_re('^1101110111001011((?:0|1){8})00010110$')

    def _instruction_logic(self, offset):
        address = self._z80.ix.bits + offset
        super(RlIndirectAddressIX, self)._instruction_logic(address)


class RlIndirectAddressIY(RlIndirectAddress):
    """ RL (IY + d) """

    regexp = compile_re('^1111110111001011((?:0|1){8})00010110$')

    def _instruction_logic(self, offset):
        address = self._z80.iy.bits + offset
        super(RlIndirectAddressIY, self)._instruction_logic(address)


""" RR instructions. """

class Rra(RotateRightThroughCarry):
    """ RRA """

    regexp = compile_re('^00011111$')

    def _update_sign_flag(register):
        pass

    def _update_zero_flag(register):
        pass

    def _update_parity_flag(register):
        pass

    def _instruction_logic(self):
        super(Rra, self)._instruction_logic(self._z80.a)


class RrR(RotateRightThroughCarry):
    """ RR r """

    regexp = compile_re('^1100101100011((?:0|1){3})$')

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(RrR, self)._instruction_logic(register)


class RrIndirectAddressHL(RrIndirectAddress):
    """ RR (HL) """

    regexp = compile_re('^1100101100011110$')

    def _instruction_logic(self):
        address = self._z80.hl.bits
        super(RrIndirectAddressHL, self)._instruction_logic(address)


class RrIndirectAddressIX(RrIndirectAddress):
    """ RR (IX + d) """

    regexp = compile_re('^1101110111001011((?:0|1){8})00011110$')

    def _instruction_logic(self, offset):
        address = self._z80.ix.bits + offset
        super(RrIndirectAddressIX, self)._instruction_logic(address)


class RrIndirectAddressIY(RrIndirectAddress):
    """ RR (IY + d) """

    regexp = compile_re('^1111110111001011((?:0|1){8})00011110$')

    def _instruction_logic(self, offset):
        address = self._z80.iy.bits + offset
        super(RrIndirectAddressIY, self)._instruction_logic(address)


""" SLA instructions. """

class SlaR(ShiftLeftArithmetic):
    """ SLA r """

    regexp = compile_re('^1100101100100((?:0|1){3})$')

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(SlaR, self)._instruction_logic(register)


class SlaIndirectAddressHL(SlaIndirectAddress):
    """ SLA (HL) """

    regexp = compile_re('^1100101100100110$')

    def _instruction_logic(self):
        super(SlaIndirectAddressHL, self)._instruction_logic(self._z80.hl.bits)


class SlaIndirectAddressIX(SlaIndirectAddress):
    """ SLA (IX + d) """

    regexp = compile_re('^1101110111001011((?:0|1){8})00100110$')

    def _instruction_logic(self, offset):
        address = self._z80.ix.bits + offset
        super(SlaIndirectAddressIX, self)._instruction_logic(address)


class SlaIndirectAddressIY(SlaIndirectAddress):
    """ SLA (IY + d) """

    regexp = compile_re('^1111110111001011((?:0|1){8})00100110$')

    def _instruction_logic(self, offset):
        address = self._z80.iy.bits + offset
        super(SlaIndirectAddressIY, self)._instruction_logic(address)


""" SLL instructions. """

class SllR(ShiftLeftLogical):
    """ SLL r """

    regexp = compile_re('^1100101100110((?:0|1){3})$')

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(SllR, self)._instruction_logic(register)


class SllIndirectAddressHL(SllIndirectAddress):
    """ SLL (HL) """

    regexp = compile_re('^1100101100110110$')

    def _instruction_logic(self):
        super(SllIndirectAddressHL, self)._instruction_logic(self._z80.hl.bits)


class SllIndirectAddressIX(SllIndirectAddress):
    """ SLL (IX + d) """

    regexp = compile_re('^1101110111001011((?:0|1){8})00110110$')

    def _instruction_logic(self, offset):
        address = self._z80.ix.bits + offset
        super(SllIndirectAddressIX, self)._instruction_logic(address)


class SllIndirectAddressIY(SllIndirectAddress):
    """ SLL (IY + d) """

    regexp = compile_re('^1111110111001011((?:0|1){8})00110110$')

    def _instruction_logic(self, offset):
        address = self._z80.iy.bits + offset
        super(SllIndirectAddressIY, self)._instruction_logic(address)


""" SRA instructions. """

class SraR(ShiftRightArithmetic):
    """ SRA r """

    regexp = compile_re('^1100101100101((?:0|1){3})$')

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(SraR, self)._instruction_logic(register)


class SraIndirectAddressHL(SraIndirectAddress):
    """ SRA (HL) """

    regexp = compile_re('^1100101100101110$')

    def _instruction_logic(self):
        super(SraIndirectAddressHL, self)._instruction_logic(self._z80.hl.bits)


class SraIndirectAddressIX(SraIndirectAddress):
    """ SRA (IX + d) """

    regexp = compile_re('^1101110111001011((?:0|1){8})00101110$')

    def _instruction_logic(self, offset):
        address = self._z80.ix.bits + offset
        super(SraIndirectAddressIX, self)._instruction_logic(address)


class SraIndirectAddressIY(SraIndirectAddress):
    """ SRA (IY + d) """

    regexp = compile_re('^1111110111001011((?:0|1){8})00101110$')

    def _instruction_logic(self, offset):
        address = self._z80.iy.bits + offset
        super(SraIndirectAddressIY, self)._instruction_logic(address)


""" SRL instructions. """

class SrlR(ShiftRightLogical):
    """ SRL r """

    regexp = compile_re('^1100101100111((?:0|1){3})$')

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(SrlR, self)._instruction_logic(register)


class SrlIndirectAddressHL(SrlIndirectAddress):
    """ SRL (HL) """

    regexp = compile_re('^1100101100111110$')

    def _instruction_logic(self):
        super(SrlIndirectAddressHL, self)._instruction_logic(self._z80.hl.bits)


class SrlIndirectAddressIX(SrlIndirectAddress):
    """ SRL (IX + d) """

    regexp = compile_re('^1101110111001011((?:0|1){8})00111110$')

    def _instruction_logic(self, offset):
        address = self._z80.ix.bits + offset
        super(SrlIndirectAddressIX, self)._instruction_logic(address)


class SrlIndirectAddressIY(SrlIndirectAddress):
    """ SRL (IY + d) """

    regexp = compile_re('^1111110111001011((?:0|1){8})00111110$')

    def _instruction_logic(self, offset):
        address = self._z80.iy.bits + offset
        super(SrlIndirectAddressIY, self)._instruction_logic(address)


""" RLD & RRD instructions. """

class Rld():
    """ RLD """

    regexp = compile_re('^1110110101101111$')

    def _update_carry_flag(register):
        pass

    def _instruction_logic(self):
        r = Z80ByteRegister(bits=self._z80.ram.read(self._z80.hl.bits))
        lower_a = self._z80.a.lower
        self._z80.a.lower = r.higher
        r.higher = r.lower
        r.lower = lower_a
        self._z80.ram.write(self._z80.hl.bits, r.bits)
        self._update_flags(self._z80.a)


class Rrd():
    """ RRD """

    regexp = compile_re('^1110110101100111$')

    def _update_carry_flag(register):
        pass

    def _instruction_logic(self):
        r = Z80ByteRegister(bits=self._z80.ram.read(self._z80.hl.bits))
        lower_r = r.lower
        r.lower = r.higher
        r.higher = self._z80.a.lower
        self._z80.a.lower = lower_r
        self._z80.ram.write(self._z80.hl.bits, r.bits)
        self._update_flags(self._z80.a)
