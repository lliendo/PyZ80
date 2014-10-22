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

from abc import ABCMeta, abstractmethod
from . import Instruction


class LoadRegisterRegister(Instruction):

    __metaclass__ = ABCMeta

    def _instruction_logic(self, destination_selector, source_selector):
        destination_register = self._register_selector(destination_selector)
        source_register = self._register_selector(source_selector)
        destination_register.bits = source_register.bits


# The RR, PP, QQ in the class names refer to the different 
# table 'selectors' found in The Undocumented Z80 Documented
# by Sean Young. See page 26.

class LoadRegisterRegisterRR(LoadRegisterRegister):
    """ LD r, r' """

    def _instruction_regexp(self):
        return '^01((?:0|1){3})((?:0|1){3})$'

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


class LoadRegisterRegisterPP(LoadRegisterRegister):
    """ LD p, p' """

    def _instruction_regexp(self):
        return '^1101110101((?:0|1){3})((?:0|1){3})$'

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


class LoadRegisterRegisterQQ(LoadRegisterRegister):
    """ LD q, q' """

    def _instruction_regexp(self):
        return '^1111110101((?:0|1){3})((?:0|1){3})$'

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


class LoadRegisterNumber(Instruction):
    __metaclass__ = ABCMeta

    def _instruction_logic(self, destination_selector, bits):
        destination_register = self._register_selector(destination_selector)
        destination_register.bits = bits


# The R, P, Q in the class names refer to the different 
# table 'selectors' found in The Undocumented Z80 Documented
# by Sean Young. See page 26.

class LoadRegisterRNumber(LoadRegisterNumber):
    """ LD r, n """

    def _instruction_regexp(self):
        return '^00((?:0|1){3})110((?:0|1){8})$'

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


class LoadRegisterPNumber(LoadRegisterNumber):
    """ LD p, n """

    def _instruction_regexp(self):
        return '^1101110100((?:0|1){3})110((?:0|1){8})$'

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


class LoadRegisterQNumber(LoadRegisterNumber):
    """ LD q, n """

    def _instruction_regexp(self):
        return '^1111110100((?:0|1){3})110((?:0|1){8})$'

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


class LoadRegisterIndirectAddress(Instruction):

    __metaclass__ = ABCMeta

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

    def _load_register_from_ram(self, selector, address):
        destination_register = self._register_selector(selector)
        destination_register.bits = self._z80.ram.read(address)


class LoadRegisterIndirectHL(LoadRegisterIndirectAddress):
    """ LD r, (HL) """

    def _instruction_regexp(self):
        return '^01((?:0|1){3})110$'

    def _instruction_logic(self, selector):
        address = self._z80.hl.bits
        self._load_register_from_ram(selector, address)


class LoadRegisterIndirectIX(LoadRegisterIndirectAddress):
    """ LD r, (IX + d) """

    def _instruction_regexp(self):
        return '^1101110101((?:0|1){3})110((?:0|1){8})$'

    def _instruction_logic(self, selector, offset):
        address = self._z80.ix.bits + offset
        self._load_register_from_ram(selector, address)


class LoadRegisterIndirectIY(LoadRegisterIndirectAddress):
    """ LD r, (IY + d) """

    def _instruction_regexp(self):
        return '^1111110101((?:0|1){3})110((?:0|1){8})$'

    def _instruction_logic(self, selector, offset):
        address = self._z80.iy.bits + offset
        self._load_register_from_ram(selector, address)


class LoadIndirectAddressRegister(Instruction):

    __metaclass__ = ABCMeta

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

    def _load_ram_from_register(self, selector, address):
        source_register = self._register_selector(selector)
        self._z80.ram.write(address, source_register.bits)


class LoadIndirectAddressHLRegister(LoadIndirectAddressRegister):
    """ LD (HL), r """

    def _instruction_regexp(self):
        return '^01110((?:0|1){3})$'

    def _instruction_logic(self, source_selector):
        address = self._z80.hl.bits
        self._load_ram_from_register(source_selector, address)


class LoadIndirectAddressIXRegister(LoadIndirectAddressRegister):
    """ LD (IX + d), r """

    def _instruction_regexp(self):
        return '^1101110101110((?:0|1){3})((?:0|1){8})$'

    def _instruction_logic(self, source_selector, offset):
        address = self._z80.ix.bits + offset
        self._load_ram_from_register(source_selector, address)


class LoadIndirectAddressIYRegister(LoadIndirectAddressRegister):
    """ LD (IY + d), r """

    def _instruction_regexp(self):
        return '^1111110101110((?:0|1){3})((?:0|1){8})$'

    def _instruction_logic(self, source_selector, offset):
        address = self._z80.iy.bits + offset
        self._load_ram_from_register(source_selector, address)


class LoadIndirectAddressHLNumber(Instruction):
    """ LD (HL), n """

    def _instruction_regexp(self):
        return '^00110110((?:0|1){8})$'

    def _instruction_logic(self, n):
        self._z80.ram.write(self._z80.hl.bits, n)


class LoadIndirectAddressIXNumber(Instruction):
    """ LD (IX + d), n """

    def _instruction_regexp(self):
        return '^1101110100110110((?:0|1){8})((?:0|1){8})$'

    def _instruction_logic(self, offset, n):
        address = self._z80.ix.bits + offset
        self._z80.ram.write(address, n)


class LoadIndirectAddressIYNumber(Instruction):
    """ LD (IY + d), n """

    def _instruction_regexp(self):
        return '^1111110100110110((?:0|1){8})((?:0|1){8})$'

    def _instruction_logic(self, offset, n):
        address = self._z80.iy.bits + offset
        self._z80.ram.write(address, n)


class LoadAIndirectAddressBC(Instruction):
    """ LD A, (BC) """

    def _instruction_regexp(self):
        return '^00001010$'

    def _instruction_logic(self):
        self._z80.a.bits = self._z80.ram.read(self._z80.bc.bits)


class LoadAIndirectAddressDE(Instruction):
    """ LD A, (DE) """

    def _instruction_regexp(self):
        return '^00011010$'

    def _instruction_logic(self):
        self._z80.a.bits = self._z80.ram.read(self._z80.de.bits)


class LoadAIndirectAddressNN(Instruction):
    """ LD A, (nn) """

    def _instruction_regexp(self):
        return '^00111010((?:0|1){8})((?:0|1){8})$'

    def _instruction_logic(self, high_order_byte, low_order_byte):
        address = self._get_address(high_order_byte, low_order_byte)
        self._z80.a.bits = self._z80.ram.read(address)


class LoadIndirectBCRegisterA(Instruction):
    """ LD (BC), A """

    def _instruction_regexp(self):
        return '^00000010$'

    def _instruction_logic(self):
        self._z80.ram.write(self._z80.bc.bits, self._z80.a.bits)


class LoadIndirectDERegisterA(Instruction):
    """ LD (DE), A """

    def _instruction_regexp(self):
        return '^00010010$'

    def _instruction_logic(self):
        self._z80.ram.write(self._z80.de.bits, self._z80.a.bits)


class LoadIndirectNNRegisterA(Instruction):
    """ LD (nn), A """

    def _instruction_regexp(self):
        return '^00110010((?:0|1){8})((?:0|1){8})$'

    def _instruction_logic(self, high_order_byte, low_order_byte):
        address = self._get_address(high_order_byte, low_order_byte)
        self._z80.ram.write(address, self._z80.a.bits)


# TODO: The flags register is affected by this instruction.
class LoadRegisterARegisterI(Instruction):
    """ LD A, I """

    def _instruction_regexp(self):
        return '^1110110101010111$'

    def _instruction_logic(self):
        self._z80.a.bits = self._z80.i.bits


# TODO: The flags register is affected by this instruction.
class LoadRegisterARegisterR(Instruction):
    """ LD A, R """

    def _instruction_regexp(self):
        return '^1110110101011111$'

    def _instruction_logic(self):
        self._z80.a.bits = self._z80.r.bits


class LoadRegisterIRegisterA(Instruction):
    """ LD I, A """

    def _instruction_regexp(self):
        return '^1110110101000111$'

    def _instruction_logic(self):
        self._z80.i.bits = self._z80.a.bits


class LoadRegisterRRegisterA(Instruction):
    """ LD R, A """

    def _instruction_regexp(self):
        return '^1110110101001111$'

    def _instruction_logic(self):
        self._z80.r.bits = self._z80.a.bits
