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


class ExAfAf_(Exchange):
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


class ExIndirectSpHl(Exchange):
    """ EX (SP), HL """

    regexp = compile_re('^11100011$')

    def _instruction_logic(self):
        self._swap_register_with_ram_word(self._z80.sp.bits, self._z80.hl)


class ExIndirectSpIx(Exchange):
    """ EX (SP), IX """

    regexp = compile_re('^1101110111100011$')

    def _instruction_logic(self):
        self._swap_register_with_ram_word(self._z80.sp.bits, self._z80.ix)


class ExIndirectSpIy(Exchange):
    """ EX (SP), IY """

    regexp = compile_re('^1111110111100011$')

    def _instruction_logic(self):
        self._swap_register_with_ram_word(self._z80.sp.bits, self._z80.iy)
