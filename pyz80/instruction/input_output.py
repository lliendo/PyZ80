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
from . import Instruction


""" Input instructions. """

class InAIndirectN(Instruction):
    """ IN A, (n) """

    regexp = compile_re('^11011011((?:0|1){8})$')

    def _instruction_logic(self, address):
        self._z80.a.bits = self._z80.device_manager.read(address)


class InRIndirectC(Instruction):
    """ IN r, (C) """

    regexp = compile_re('^1110110101((?:0|1){3})000$')

    def _select_register(self, selector):
        registers = {
            0b000: self._z80.b,
            0b001: self._z80.c,
            0b010: self._z80.d,
            0b011: self._z80.e,
            0b100: self._z80.h,
            0b101: self._z80.l,
            0b111: self._z80.a
        }

        return registers[selector]

    def _update_flags(self, input_byte):
        self._update_sign_flag(input_byte)
        self._update_zero_flag(input_byte)
        self._z80.f.reset_half_carry_flag()
        self._update_parity_flag(input_byte)
        self._z80.f.reset_add_substract_flag()

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        register.bits = self._z80.device_manager.read(self._z80.c)


class InFIndirectN(Instruction):
    """ IN F, (n) """

    regexp = compile_re('^1110110101110000$')

    def _instruction_logic(self, address):
        self._z80.f.bits = self._z80.device_manager.read(address)


class Ini(Instruction):
    """ INI """

    regexp = compile_re('^1110110110100010$')

    def _parity(self, input_byte):
        return ((input_byte + ((self._z80.c.bits + 1) & 0xFF)) & 0x07) ^ self._z80.b.bits

    def _add_substract(self, input_byte):
        return Z80register(bits=input_byte).msb

    def _carry(self, input_byte):
        return (input_byte + ((self._z80.c.bits + 1) & 0xFF)) > 0xFF

    def _half_carry(self, input_byte):
        return self._carry(input_byte)

    def _update_flags(self, input_byte):
        self._update_sign_flag(self.z80.b.bits)
        self._update_zero_flag(self.z80.b.bits)
        self._update_half_carry(input_byte)
        self._update_parity_flag(input_byte)
        self._update_carry_flag(input_byte)
        self._update_add_substract(input_byte)
        
    def _read(self):
        input_byte = self._z80.device_manager.read(self._z80.c.bits)
        self._z80.ram.write(self._z80.hl.bits, input_byte)
        self._z80.hl.bits += 1
        self._z80.b.bits -= 1

        return input_byte

    def _instruction_logic(self):
        input_byte = self._read()
        self._update_flags(input_byte)


class Inir(Ini):
    """ INIR """

    regexp = compile_re('^1110110110110010$')

    def _update_flags(self, input_byte):
        self._z80.f.reset_sign_flag()
        self._z80.f.set_zero_flag()
        self._update_half_carry(input_byte)
        self._update_parity_flag(input_byte)
        self._update_carry_flag(input_byte)
        self._update_add_substract(input_byte)

    def _instruction_logic(self):
        while self._z80.b.bits > 0x00:
            input_byte = self._read()

        self._update_flags(input_byte)


class Ind(Instruction):
    """ IND """

    regexp = compile_re('^1110110110101010$')

    def _parity(self, input_byte):
        return ((input_byte + ((self._z80.c.bits - 1) & 0xFF)) & 0x07) ^ self._z80.b.bits

    def _add_substract(self, input_byte):
        return Z80register(bits=input_byte).msb

    def _carry(self, input_byte):
        return (input_byte + ((self._z80.c.bits - 1) & 0xFF)) > 0xFF

    def _half_carry(self, input_byte):
        return self._carry(input_byte)

    def _update_flags(self, input_byte):
        self._update_sign_flag(self.z80.b.bits)
        self._update_zero_flag(self.z80.b.bits)
        self._update_half_carry(input_byte)
        self._update_parity_flag(input_byte)
        self._update_carry_flag(input_byte)
        self._update_add_substract(input_byte)

    def _read(self):
        input_byte = self._z80.device_manager.read(self._z80.c.bits)
        self._z80.ram.write(self._z80.hl.bits, input_byte)
        self._z80.hl.bits -= 1
        self._z80.b.bits -= 1

    def _instruction_logic(self):
        input_byte = self._read()
        self._update_flags(input_byte)


class Indr(Ind):
    """ INDR """

    regexp = compile_re('^1110110110111010$')

    def _update_flags(self, input_byte):
        self._z80.f.reset_sign_flag()
        self._z80.f.set_zero_flag()
        self._update_half_carry(input_byte)
        self._update_parity_flag(input_byte)
        self._update_carry_flag(input_byte)
        self._update_add_substract(input_byte)

    def _instruction_logic(self):
        while self._z80.b.bits > 0x00:
            input_byte = self._read()
        
        self._update_flags(input_byte)


""" Output instructions. """

class OutAIndirectN(Instruction):
    """ OUT (n), A """

    regexp = compile_re('^11010011((?:0|1){8})$')

    def _instruction_logic(self, address):
        self._z80.device_manager.write(address, self._z80.a.bits)


class OutRIndirectC(InRIndirectC):
    """ OUT (C), r """

    regexp = compile_re('^1110110101((?:0|1){3})001$')

    def _instruction_logic(self, selector):
        register = self._select_register(selector)
        self._z80.device_manager.write(self._z80.c.bits, register.bits)


class OutFIndirectN(Instruction):
    """ OUT (C), 0 """

    regexp = compile_re('^1110110101110001$')

    def _instruction_logic(self, address):
        self._z80.device_manager.write(self._z80.c.bits, 0x00)


class Outi(Instruction):
    """ OUTI """

    regexp = compile_re('^1110110110100011$')

    def _parity(self, output_byte):
        return ((output_byte + self._z80.l.bits) & 0x07) ^ self._z80.b.bits

    def _add_substract(self, output_byte):
        return Z80Register(bits=output_byte).msb

    def _carry(self, output_byte):
        return (output_byte + self._z80.l.bits) > 0xFF

    def _half_carry(self, output_byte):
        return self._carry(output_byte)

    def _update_flags(self, output_byte):
        self._update_sign_flag(self.z80.b.bits)
        self._update_zero_flag(self.z80.b.bits)
        self._update_half_carry(output_byte)
        self._update_parity_flag(output_byte)
        self._update_carry_flag(output_byte)
        self._update_add_substract(output_byte)

    def _write(self):
        output_byte = self._z80.ram.read(self._z80.hl.bits)
        self._z80.device_manager.write(self._z80.c.bits, output_byte)
        self._z80.hl.bits += 1
        self._z80.b.bits -= 1

        return output_byte

    def _instruction_logic(self):
        output_byte = self._write()
        self._update_flags(output_byte)


class Otir(Outi):
    """ OTIR """

    regexp = compile_re('^1110110110110011$')

    def _update_flags(self, output_byte):
        self._z80.f.reset_sign_flag()
        self._z80.f.set_zero_flag()
        self._update_half_carry(output_byte)
        self._update_parity_flag(output_byte)
        self._update_carry_flag(output_byte)
        self._update_add_substract(output_byte)

    def _instruction_logic(self):
        while self._z80.b.bits > 0x00:
            output_byte = self._write()

        self._update_flags(output_byte)


class Outd(Outi):
    """ OUTD """

    regexp = compile_re('^1110110110101011$')

    def _write(self):
        output_byte = self._z80.ram.read(self._z80.hl.bits)
        self._z80.device_manager.write(self._z80.c.bits, output_byte)
        self._z80.hl.bits -= 1
        self._z80.b.bits -= 1

        return output_byte

    def _instruction_logic(self):
        output_byte = self._write()
        self._update_flags(output_byte)


class Otdr(Outd):
    """ OTDR """

    regexp = compile_re('^1110110110111011$')

    def _instruction_logic(self):
        while self._z80.b.bits > 0x00:
            output_byte = self._write()
        
        self._update_flags(output_byte)
