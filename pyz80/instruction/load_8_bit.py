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
from abc_load_8_bit import *


# The RR, PP, QQ in the class names refer to the different 
# table 'selectors' found in The Undocumented Z80 Documented
# by Sean Young. See page 26.

class LoadRR(LoadRegisterRegister):
    """ LD r, r' """

    regexp = compile_re('^01((?:0|1){3})((?:0|1){3})$')

    def _register_selector(self, selector):
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


class LoadPP(LoadRegisterRegister):
    """ LD p, p' """
    
    regexp = compile_re('^1101110101((?:0|1){3})((?:0|1){3})$')

    def _register_selector(self, selector):
        registers = {
            0b000: self._z80.b,
            0b001: self._z80.c,
            0b010: self._z80.d,
            0b011: self._z80.e,
            0b100: self._z80.ixh,
            0b101: self._z80.ixl,
            0b111: self._z80.a,
        }

        return registers[selector]


class LoadQQ(LoadRegisterRegister):
    """ LD q, q' """

    regexp = compile_re('^1111110101((?:0|1){3})((?:0|1){3})$')

    def _register_selector(self, selector):
        registers = {
            0b000: self._z80.b,
            0b001: self._z80.c,
            0b010: self._z80.d,
            0b011: self._z80.e,
            0b100: self._z80.iyh,
            0b101: self._z80.iyl,
            0b111: self._z80.a,
        }

        return registers[selector]


class LoadRN(LoadRegisterNumber):
    """ LD r, n """

    regexp = compile_re('^00((?:0|1){3})110((?:0|1){8})$')

    def _register_selector(self, selector):
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


class LoadPN(LoadRegisterNumber):
    """ LD p, n """

    regexp = compile_re('^1101110100((?:0|1){3})110((?:0|1){8})$')

    def _register_selector(self, selector):
        registers = {
            0b000: self._z80.b,
            0b001: self._z80.c,
            0b010: self._z80.d,
            0b011: self._z80.e,
            0b100: self._z80.ixh,
            0b101: self._z80.ixl,
            0b111: self._z80.a,
        }

        return registers[selector]


class LoadQN(LoadRegisterNumber):
    """ LD q, n """

    regexp = compile_re('^1111110100((?:0|1){3})110((?:0|1){8})$')

    def _register_selector(self, selector):
        registers = {
            0b000: self._z80.b,
            0b001: self._z80.c,
            0b010: self._z80.d,
            0b011: self._z80.e,
            0b100: self._z80.iyh,
            0b101: self._z80.iyl,
            0b111: self._z80.a,
        }

        return registers[selector]


class LoadRIndirectHL(LoadRegisterIndirectAddress):
    """ LD r, (HL) """

    regexp = compile_re('^01((?:0|1){3})110$')

    def _instruction_logic(self, selector):
        address = self._z80.hl.bits
        self._load_register_from_ram(selector, address)


class LoadRIndirectIX(LoadRegisterIndirectAddress):
    """ LD r, (IX + d) """

    regexp = compile_re('^1101110101((?:0|1){3})110((?:0|1){8})$')

    def _instruction_logic(self, selector, offset):
        address = self._z80.ix.bits + offset
        self._load_register_from_ram(selector, address)


class LoadRIndirectIY(LoadRegisterIndirectAddress):
    """ LD r, (IY + d) """

    regexp = compile_re('^1111110101((?:0|1){3})110((?:0|1){8})$')

    def _instruction_logic(self, selector, offset):
        address = self._z80.iy.bits + offset
        self._load_register_from_ram(selector, address)


class LoadIndirectHLR(LoadIndirectAddressRegister):
    """ LD (HL), r """

    regexp = compile_re('^01110((?:0|1){3})$')

    def _instruction_logic(self, source_selector):
        address = self._z80.hl.bits
        self._load_ram_from_register(source_selector, address)


class LoadIndirectIXR(LoadIndirectAddressRegister):
    """ LD (IX + d), r """

    regexp = compile_re('^1101110101110((?:0|1){3})((?:0|1){8})$')

    def _instruction_logic(self, source_selector, offset):
        address = self._z80.ix.bits + offset
        self._load_ram_from_register(source_selector, address)


class LoadIndirectIYR(LoadIndirectAddressRegister):
    """ LD (IY + d), r """

    regexp = compile_re('^1111110101110((?:0|1){3})((?:0|1){8})$')

    def _regexp(self):
        return compile_re('^1111110101110((?:0|1){3})((?:0|1){8})$')

    def _instruction_logic(self, source_selector, offset):
        address = self._z80.iy.bits + offset
        self._load_ram_from_register(source_selector, address)


class LoadIndirectHLN(Instruction):
    """ LD (HL), n """

    regexp = compile_re('^00110110((?:0|1){8})$')

    def _instruction_logic(self, n):
        self._z80.ram.write(self._z80.hl.bits, n)


class LoadIndirectIXN(Instruction):
    """ LD (IX + d), n """

    regexp = compile_re('^1101110100110110((?:0|1){8})((?:0|1){8})$')

    def _instruction_logic(self, offset, n):
        address = self._z80.ix.bits + offset
        self._z80.ram.write(address, n)


class LoadIndirectIYN(Instruction):
    """ LD (IY + d), n """

    regexp = compile_re('^1111110100110110((?:0|1){8})((?:0|1){8})$')

    def _instruction_logic(self, offset, n):
        address = self._z80.iy.bits + offset
        self._z80.ram.write(address, n)


class LoadAIndirectBC(Instruction):
    """ LD A, (BC) """
    
    regexp = compile_re('^00001010$')

    def _instruction_logic(self):
        self._z80.a.bits = self._z80.ram.read(self._z80.bc.bits)


class LoadAIndirectDE(Instruction):
    """ LD A, (DE) """

    regexp = compile_re('^00011010$')

    def _instruction_logic(self):
        self._z80.a.bits = self._z80.ram.read(self._z80.de.bits)


class LoadAIndirectNN(Instruction):
    """ LD A, (nn) """

    regexp = compile_re('^00111010((?:0|1){8})((?:0|1){8})$')

    def _instruction_logic(self, high_order_byte, low_order_byte):
        address = self._get_address(high_order_byte, low_order_byte)
        self._z80.a.bits = self._z80.ram.read(address)


class LoadIndirectBCA(Instruction):
    """ LD (BC), A """

    regexp = compile_re('^00000010$')

    def _instruction_logic(self):
        self._z80.ram.write(self._z80.bc.bits, self._z80.a.bits)


class LoadIndirectDEA(Instruction):
    """ LD (DE), A """

    regexp = compile_re('^00010010$')

    def _instruction_logic(self):
        self._z80.ram.write(self._z80.de.bits, self._z80.a.bits)


class LoadIndirectNNA(Instruction):
    """ LD (nn), A """

    regexp = compile_re('^00110010((?:0|1){8})((?:0|1){8})$')

    def _instruction_logic(self, high_order_byte, low_order_byte):
        address = self._get_address(high_order_byte, low_order_byte)
        self._z80.ram.write(address, self._z80.a.bits)


class LoadAI(Instruction):
    """ LD A, I """

    regexp = compile_re('^1110110101010111$')

    def _instruction_logic(self):
        self._z80.a.bits = self._z80.i.bits
        self._update_flags()
    
    # TODO: Set parity/overflow flag if iff2 is set.
    def _update_flags(self):
        self._update_sign_flag(self._z80.a.bits)
        self._update_zero_flag(self._z80.a.bits)
        self._z80.f.reset_half_carry_flag()
        self._z80.f.reset_add_substract_flag()


class LoadAR(Instruction):
    """ LD A, R """

    regexp = compile_re('^1110110101011111$')

    def _instruction_logic(self):
        self._z80.a.bits = self._z80.r.bits

    # TODO: Set parity/overflow flag if iff2 is set.
    def _update_flags(self):
        self._update_sign_flag(self._z80.a.bits)
        self._update_zero_flag(self._z80.a.bits)
        self._z80.f.reset_half_carry_flag()
        self._z80.f.reset_add_substract_flag()


class LoadIA(Instruction):
    """ LD I, A """

    regexp = compile_re('^1110110101000111$')

    def _instruction_logic(self):
        self._z80.i.bits = self._z80.a.bits


class LoadRA(Instruction):
    """ LD R, A """

    regexp = compile_re('^1110110101001111$')

    def _instruction_logic(self):
        self._z80.r.bits = self._z80.a.bits
