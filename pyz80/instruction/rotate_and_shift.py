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


class RlcIndirectHL(RlcIndirectAddress):
    """ RLC (HL) """

    regexp = compile_re('^1100101100000110$')

    def _instruction_logic(self):
        address = self._z80.hl.bits
        super(RlcIndirectHL, self)._instruction_logic(address)


class RlcIndirectIX(RlcIndirectAddress):
    """ RLC (IX + d) """

    regexp = compile_re('^1101110111001011((?:0|1){8})00000110$')

    def _instruction_logic(self, offset):
        address = self._z80.ix.bits + offset
        super(RlcIndirectIX, self)._instruction_logic(address)


class RlcIndirectIY(RlcIndirectAddress):
    """ RLC (IY + d) """

    regexp = compile_re('^1111110111001011((?:0|1){8})00000110$')

    def _instruction_logic(self, offset):
        address = self._z80.iy.bits + offset
        super(RlcIndirectIY, self)._instruction_logic(address)


class RlcIndirectIXR(RlcIndirectAddress):
    """ RLC (IX + d), r """

    regexp = compile_re('^1101110111001011((?:0|1){8})00000((?:0|1){3})$')

    def _instruction_logic(self, offset, selector):
        address = self._z80.ix.bits + offset
        register = self._select_register(selector)
        register.bits = super(RlcIndirectIXR, self)._instruction_logic(address).bits


class RlcIndirectIYR(RlcIndirectAddress):
    """ RLC (IY + d), r """

    regexp = compile_re('^1111110111001011((?:0|1){8})00000((?:0|1){3})$')

    def _instruction_logic(self, offset, selector):
        address = self._z80.iy.bits + offset
        register = self._select_register(selector)
        register.bits = super(RlcIndirectIYR, self)._instruction_logic(address).bits


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


class RrcIndirectHL(RrcIndirectAddress):
    """ RRC (HL) """

    regexp = compile_re('^1100101100001110$')

    def _instruction_logic(self):
        address = self._z80.hl.bits
        super(RrcIndirectHL, self)._instruction_logic(address)


class RrcIndirectIX(RrcIndirectAddress):
    """ RRC (IX + d) """

    regexp = compile_re('^1101110111001011((?:0|1){8})00001110$')

    def _instruction_logic(self, offset):
        address = self._z80.ix.bits + offset
        super(RrcIndirectIX, self)._instruction_logic(address)


class RrcIndirectIY(RrcIndirectAddress):
    """ RRC (IY + d) """

    regexp = compile_re('^1111110111001011((?:0|1){8})00001110$')

    def _instruction_logic(self, offset):
        address = self._z80.iy.bits + offset
        super(RrcIndirectIY, self)._instruction_logic(address)


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


class RlIndirectHL(RlIndirectAddress):
    """ RL (HL) """

    regexp = compile_re('^1100101100010110$')

    def _instruction_logic(self):
        address = self._z80.hl.bits
        super(RlIndirectHL, self)._instruction_logic(address)


class RlIndirectIX(RlIndirectAddress):
    """ RL (IX + d) """

    regexp = compile_re('^1101110111001011((?:0|1){8})00010110$')

    def _instruction_logic(self, offset):
        address = self._z80.ix.bits + offset
        super(RlIndirectIX, self)._instruction_logic(address)


class RlIndirectIY(RlIndirectAddress):
    """ RL (IY + d) """

    regexp = compile_re('^1111110111001011((?:0|1){8})00010110$')

    def _instruction_logic(self, offset):
        address = self._z80.iy.bits + offset
        super(RlIndirectIY, self)._instruction_logic(address)


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


class RrIndirectHL(RrIndirectAddress):
    """ RR (HL) """

    regexp = compile_re('^1100101100011110$')

    def _instruction_logic(self):
        address = self._z80.hl.bits
        super(RrIndirectHL, self)._instruction_logic(address)


class RrIndirectIX(RrIndirectAddress):
    """ RR (IX + d) """

    regexp = compile_re('^1101110111001011((?:0|1){8})00011110$')

    def _instruction_logic(self, offset):
        address = self._z80.ix.bits + offset
        super(RrIndirectIX, self)._instruction_logic(address)


class RrIndirectIY(RrIndirectAddress):
    """ RR (IY + d) """

    regexp = compile_re('^1111110111001011((?:0|1){8})00011110$')

    def _instruction_logic(self, offset):
        address = self._z80.iy.bits + offset
        super(RrIndirectIY, self)._instruction_logic(address)


""" SLA instructions. """

class SlaR(ShiftLeftArithmetic):
    """ SLA r """

    regexp = compile_re('^1100101100100((?:0|1){3})$')

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(SlaR, self)._instruction_logic(register)


class SlaIndirectHL(SlaIndirectAddress):
    """ SLA (HL) """

    regexp = compile_re('^1100101100100110$')

    def _instruction_logic(self):
        super(SlaIndirectHL, self)._instruction_logic(self._z80.hl.bits)


class SlaIndirectIX(SlaIndirectAddress):
    """ SLA (IX + d) """

    regexp = compile_re('^1101110111001011((?:0|1){8})00100110$')

    def _instruction_logic(self, offset):
        address = self._z80.ix.bits + offset
        super(SlaIndirectIX, self)._instruction_logic(address)


class SlaIndirectIY(SlaIndirectAddress):
    """ SLA (IY + d) """

    regexp = compile_re('^1111110111001011((?:0|1){8})00100110$')

    def _instruction_logic(self, offset):
        address = self._z80.iy.bits + offset
        super(SlaIndirectIY, self)._instruction_logic(address)


""" SLL instructions. """

class SllR(ShiftLeftLogical):
    """ SLL r """

    regexp = compile_re('^1100101100110((?:0|1){3})$')

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(SllR, self)._instruction_logic(register)


class SllIndirectHL(SllIndirectAddress):
    """ SLL (HL) """

    regexp = compile_re('^1100101100110110$')

    def _instruction_logic(self):
        super(SllIndirectHL, self)._instruction_logic(self._z80.hl.bits)


class SllIndirectIX(SllIndirectAddress):
    """ SLL (IX + d) """

    regexp = compile_re('^1101110111001011((?:0|1){8})00110110$')

    def _instruction_logic(self, offset):
        address = self._z80.ix.bits + offset
        super(SllIndirectIX, self)._instruction_logic(address)


class SllIndirectIY(SllIndirectAddress):
    """ SLL (IY + d) """

    regexp = compile_re('^1111110111001011((?:0|1){8})00110110$')

    def _instruction_logic(self, offset):
        address = self._z80.iy.bits + offset
        super(SllIndirectIY, self)._instruction_logic(address)


""" SRA instructions. """

class SraR(ShiftRightArithmetic):
    """ SRA r """

    regexp = compile_re('^1100101100101((?:0|1){3})$')

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(SraR, self)._instruction_logic(register)


class SraIndirectHL(SraIndirectAddress):
    """ SRA (HL) """

    regexp = compile_re('^1100101100101110$')

    def _instruction_logic(self):
        super(SraIndirectHL, self)._instruction_logic(self._z80.hl.bits)


class SraIndirectIX(SraIndirectAddress):
    """ SRA (IX + d) """

    regexp = compile_re('^1101110111001011((?:0|1){8})00101110$')

    def _instruction_logic(self, offset):
        address = self._z80.ix.bits + offset
        super(SraIndirectIX, self)._instruction_logic(address)


class SraIndirectIY(SraIndirectAddress):
    """ SRA (IY + d) """

    regexp = compile_re('^1111110111001011((?:0|1){8})00101110$')

    def _instruction_logic(self, offset):
        address = self._z80.iy.bits + offset
        super(SraIndirectIY, self)._instruction_logic(address)


""" SRL instructions. """

class SrlR(ShiftRightLogical):
    """ SRL r """

    regexp = compile_re('^1100101100111((?:0|1){3})$')

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        super(SrlR, self)._instruction_logic(register)


class SrlIndirectHL(SrlIndirectAddress):
    """ SRL (HL) """

    regexp = compile_re('^1100101100111110$')

    def _instruction_logic(self):
        super(SrlIndirectHL, self)._instruction_logic(self._z80.hl.bits)


class SrlIndirectIX(SrlIndirectAddress):
    """ SRL (IX + d) """

    regexp = compile_re('^1101110111001011((?:0|1){8})00111110$')

    def _instruction_logic(self, offset):
        address = self._z80.ix.bits + offset
        super(SrlIndirectIX, self)._instruction_logic(address)


class SrlIndirectIY(SrlIndirectAddress):
    """ SRL (IY + d) """

    regexp = compile_re('^1111110111001011((?:0|1){8})00111110$')

    def _instruction_logic(self, offset):
        address = self._z80.iy.bits + offset
        super(SrlIndirectIY, self)._instruction_logic(address)


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
