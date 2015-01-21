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
from abc_exchange_and_transfer import *
from . import Instruction


class Ex(Exchange):
    """ EX DE, HL """

    regexp = compile_re('^11101011$')

    def _instruction_logic(self):
        self._swap_registers(self._z80.de, self._z80.hl)


class ExAFAF_(Exchange):
    """ EX AF, AF' """

    regexp = compile_re('^00001000$')

    def _instruction_logic(self):
        self._swap_registers(self._z80.a, self._z80.a_)
        self._swap_registers(self._z80.f, self._z80.f_)


class Exx(Exchange):
    """ EXX """

    regexp = compile_re('^11011001$')

    def _instruction_logic(self):
        self._swap_registers(self._z80.bc, self._z80.bc_)
        self._swap_registers(self._z80.de, self._z80.de_)
        self._swap_registers(self._z80.hl, self._z80.hl_)


class ExIndirectSPHL(Exchange):
    """ EX (SP), HL """

    regexp = compile_re('^11100011$')

    def _instruction_logic(self):
        self._swap_register_with_ram_word(self._z80.sp.bits, self._z80.hl)


class ExIndirectSPIX(Exchange):
    """ EX (SP), IX """

    regexp = compile_re('^1101110111100011$')

    def _instruction_logic(self):
        self._swap_register_with_ram_word(self._z80.sp.bits, self._z80.ix)


class ExIndirectSPIY(Exchange):
    """ EX (SP), IY """

    regexp = compile_re('^1111110111100011$')

    def _instruction_logic(self):
        self._swap_register_with_ram_word(self._z80.sp.bits, self._z80.iy)


class Ldi(Instruction):
    """ LDI """

    regexp = compile_re('^1110110110100000$')

    def _parity(self, instruction_result):
        return instruction_result != 0x00

    def _update_flags(self):
        self._z80.f.reset_half_carry_flag()
        self._update_parity_flag(self._z80.bc)
        self._z80.f.reset_add_substract_flag()

    def _move_byte(self):
        self._z80.ram.write(self._z80.de, self._z80.ram.read(self._z80.hl))
        self._z80.de.bits += 1
        self._z80.hl.bits += 1
        self._z80.bc.bits -= 1

    def _instruction_logic(self):
        self._move_byte()
        self._update_flags()


class Ldir(Ldi):
    """ LDIR """

    regexp = compile_re('^1110110110110000$')

    def _update_flags(self):
        self._z80.f.reset_half_carry_flag()
        self._z80.f.reset_parity_flag()
        self._z80.f.reset_add_substract_flag()

    def _instruction_logic(self):
        while self._z80.bc.bits > 0x00:
            self._move_byte()

        self._update_flags()


class Ldd(Ldi):
    """ LDD """

    regexp = compile_re('^1110110110101000$')

    def _move_byte(self):
        self._z80.ram.write(self._z80.de, self._z80.ram.read(self._z80.hl))
        self._z80.de.bits -= 1
        self._z80.hl.bits -= 1
        self._z80.bc.bits -= 1

    def _instruction_logic(self):
        self._move_byte()
        self._update_flags()


class Lddr(Ldd):
    """ LDDR """

    regexp = compile_re('^1110110110111000$')

    def _update_flags(self):
        self._z80.f.reset_half_carry_flag()
        self._z80.f.reset_parity_flag()
        self._z80.f.reset_add_substract_flag()

    def _instruction_logic(self):
        while self._z80.bc.bits > 0x00:
            self._move_byte()

        self._update_flags()
