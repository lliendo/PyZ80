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

from itertools import product
from ..instruction.load_group_16_bit import *
from .test_z80_base import TestZ80


class TestLoadInstructions(TestZ80):
    def __init__(self, *args, **kwargs):
        super(TestLoadInstructions, self).__init__(*args, **kwargs)

    def test_load_register_nn(self):
        registers = {
            '00': 'bc',
            '01': 'de',
            '10': 'hl',
            '11': 'sp',
        }
    
        instruction = LoadDDNN(self._z80)

        for destination in registers.keys():
            nn = self._get_random_word()
            opcode = ['00{0}0001'.format(destination)] + list(self._word_to_bin(nn))
            instruction.execute(self._opcode_to_int(*opcode))
            self.assertEqual(getattr(self._z80, registers[destination]).bits, nn)

    def test_load_ix_nn(self):
        instruction = LoadIXNN(self._z80)
        nn = self._get_random_word()
        opcode = ['1101110100100001'] + list(self._word_to_bin(nn))
        instruction.execute(self._opcode_to_int(*opcode))
        self.assertEqual(self._z80.ix.bits, nn)

    def test_load_iy_nn(self):
        instruction = LoadIYNN(self._z80)
        nn = self._get_random_word()
        opcode = ['1111110100100001'] + list(self._word_to_bin(nn))
        instruction.execute(self._opcode_to_int(*opcode))
        self.assertEqual(self._z80.iy.bits, nn)

    def _load_ram_with_16_bit_value(self, address, value):
        n, m = self._word_to_bin(value)
        self._z80.ram.write(address + 1, self._bin_to_int(n))
        self._z80.ram.write(address, self._bin_to_int(m))
