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

from unittest import TestCase
from random import randint
from ..cpu import Z80


class TestZ80(TestCase):
    def setUp(self):
        self._z80 = Z80()

    def _get_random_byte(self, upper_limit=0xFF):
        return randint(0x00, upper_limit)

    def _get_random_word(self, upper_limit=0xFFFF):
        return randint(0x00, upper_limit)

    def _load_z80_registers(self, registers):
        for r in registers:
            getattr(self._z80, r).bits = self._get_random_byte()

    def _bin_to_int(self, n):
        return int(n, base=2)

    def _opcode_to_int(self, *opcode):
        # return map(lambda o: int(o, base=2), opcode)
        return map(lambda o: self._bin_to_int(o), opcode)

    def _int_to_bin(self, n, padding=8):
        return '{0}'.format(bin(n).lstrip('0b').zfill(padding))

    def _word_to_bin(self, n):
        word = self._int_to_bin(n, padding=16)
        return word[:8], word[8:]
