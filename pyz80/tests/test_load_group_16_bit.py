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
        """ Test LD dd, nn """

        registers = {
            '00': self._z80.bc,
            '01': self._z80.de,
            '10': self._z80.hl,
            '11': self._z80.sp,
        }
    
        instruction = LoadDDNN(self._z80)

        for destination in registers.keys():
            nn = self._get_random_word()
            opcode = ['00{0}0001'.format(destination)] + list(self._word_to_bin(nn))
            instruction.execute(self._opcode_to_int(*opcode))
            self.assertEqual(registers[destination].bits, nn)

    def test_load_ix_nn(self):
        """ Test LD IX, nn """

        instruction = LoadIXNN(self._z80)
        nn = self._get_random_word()
        opcode = ['11011101', '00100001'] + list(self._word_to_bin(nn))
        instruction.execute(self._opcode_to_int(*opcode))
        self.assertEqual(self._z80.ix.bits, nn)

    def test_load_iy_nn(self):
        """ Test LD IY, nn """

        instruction = LoadIYNN(self._z80)
        nn = self._get_random_word()
        opcode = ['11111101', '00100001'] + list(self._word_to_bin(nn))
        instruction.execute(self._opcode_to_int(*opcode))
        self.assertEqual(self._z80.iy.bits, nn)

    def test_load_hl_indirect_nn(self):
        """ Test LD HL, (nn) """

        instruction = LoadHLIndirectAddressNN(self._z80)
        address = self._get_random_word()
        nn = self._get_random_word()
        self._load_ram_with_word(address, nn)
        opcode = ['00101010'] + list(self._word_to_bin(address))
        instruction.execute(self._opcode_to_int(*opcode))
        self.assertEqual(self._z80.hl.bits, nn)

    def test_load_dd_indirect_nn(self):
        registers = {
            '00': self._z80.bc,
            '01': self._z80.de,
            '10': self._z80.hl,
            '11': self._z80.sp,
        }

        instruction = LoadDDIndirectAddressNN(self._z80)

        for destination in registers.keys():
            address = self._get_random_word()
            nn = self._get_random_word()
            self._load_ram_with_word(address, nn)
            opcode = ['11101101', '01{0}1011'.format(destination)] + list(self._word_to_bin(address))
            instruction.execute(self._opcode_to_int(*opcode))
            self.assertEqual(registers[destination].bits, nn)

    def test_load_ix_indirect_nn(self):
        """ Test LD IX, (nn) """

        instruction = LoadIXIndirectAddressNN(self._z80)
        address = self._get_random_word()
        nn = self._get_random_word()
        self._load_ram_with_word(address, nn)
        opcode = ['11011101', '00101010'] + list(self._word_to_bin(address))
        instruction.execute(self._opcode_to_int(*opcode))
        self.assertEqual(self._z80.ix.bits, nn)

    def test_load_iy_indirect_nn(self):
        """ Test LD IY, (nn) """
        
        instruction = LoadIYIndirectAddressNN(self._z80)
        address = self._get_random_word()
        nn = self._get_random_word()
        self._load_ram_with_word(address, nn)
        opcode = ['11111101', '00101010'] + list(self._word_to_bin(address))
        instruction.execute(self._opcode_to_int(*opcode))
        self.assertEqual(self._z80.iy.bits, nn)

    def test_load_indirect_nn_hl(self):
        """ Test LD (nn), HL """

        instruction = LoadIndirectAddressNNHL(self._z80)
        address = self._get_random_word()
        nn = self._get_random_word()
        self._z80.hl.bits = nn
        opcode = ['00100010'] + list(self._word_to_bin(address))
        instruction.execute(self._opcode_to_int(*opcode))
        self.assertEqual(self._read_ram_word(address), nn)

    def test_load_indirect_nn_dd(self):
        """ Test LD (nn), dd """

        registers = {
            '00': self._z80.bc,
            '01': self._z80.de,
            '10': self._z80.hl,
            '11': self._z80.sp,
        }

        instruction = LoadIndirectAddressNNDD(self._z80)

        for destination in registers.keys():
            address = self._get_random_word()
            nn = self._get_random_word()
            registers[destination].bits = nn
            opcode = ['11101101', '01{0}0011'.format(destination)] + list(self._word_to_bin(address))
            instruction.execute(self._opcode_to_int(*opcode))
            self.assertEqual(self._read_ram_word(address), nn)

    def test_load_indirect_nn_ix(self):
        """ Test LD (nn), IX """

        instruction = LoadIndirectAddressNNIX(self._z80)
        address = self._get_random_word()
        nn = self._get_random_word()
        self._z80.ix.bits = nn
        opcode = ['11011101', '00100010'] + list(self._word_to_bin(address))
        instruction.execute(self._opcode_to_int(*opcode))
        self.assertEqual(self._read_ram_word(address), nn)

    def test_load_indirect_nn_iy(self):
        """ Test LD (nn), IY """

        instruction = LoadIndirectAddressNNIY(self._z80)
        address = self._get_random_word()
        nn = self._get_random_word()
        self._z80.iy.bits = nn
        opcode = ['11111101', '00100010'] + list(self._word_to_bin(address))
        instruction.execute(self._opcode_to_int(*opcode))
        self.assertEqual(self._read_ram_word(address), nn)

    def test_load_sp_hl(self):
        """ Test LD SP, HL """

        instruction = LoadSPHL(self._z80)
        nn = self._get_random_word()
        self._z80.hl.bits = nn
        opcode = ['11111001']
        instruction.execute(self._opcode_to_int(*opcode))
        self.assertEqual(self._z80.sp.bits, self._z80.hl.bits)

    def test_load_sp_ix(self):
        """ Test LD SP, IX """

        instruction = LoadSPIX(self._z80)
        nn = self._get_random_word()
        self._z80.ix.bits = nn
        opcode = ['11011101', '11111001']
        instruction.execute(self._opcode_to_int(*opcode))
        self.assertEqual(self._z80.sp.bits, self._z80.ix.bits)

    def test_load_sp_iy(self):
        """ Test LD SP, IY """

        instruction = LoadSPIY(self._z80)
        nn = self._get_random_word()
        self._z80.iy.bits = nn
        opcode = ['11111101', '11111001']
        instruction.execute(self._opcode_to_int(*opcode))
        self.assertEqual(self._z80.sp.bits, self._z80.iy.bits)

    def test_push_qq(self):
        """ Test PUSH qq """

        registers = {
            '00': self._z80.bc,
            '01': self._z80.de,
            '10': self._z80.hl,
            '11': self._z80.af,
        }

        instruction = PushQQ(self._z80)

        for destination in registers.keys():
            self._z80.sp.bits = self._get_random_word()
            nn = self._get_random_word()
            registers[destination].bits = nn
            opcode = ['11{0}0101'.format(destination)]
            instruction.execute(self._opcode_to_int(*opcode))
            self.assertEqual(self._read_ram_word(self._z80.sp.bits), nn)

    def test_push_ix(self):
        """ Test PUSH IX """

        instruction = PushIX(self._z80)
        self._z80.sp.bits = self._get_random_word()
        nn = self._get_random_word()
        self._z80.ix.bits = nn
        opcode = ['11011101', '11100101']
        instruction.execute(self._opcode_to_int(*opcode))
        self.assertEqual(self._read_ram_word(self._z80.sp.bits), nn)

    def test_push_iy(self):
        """ Test PUSH IY """

        instruction = PushIY(self._z80)
        self._z80.sp.bits = self._get_random_word()
        nn = self._get_random_word()
        self._z80.iy.bits = nn
        opcode = ['11111101', '11100101']
        instruction.execute(self._opcode_to_int(*opcode))
        self.assertEqual(self._read_ram_word(self._z80.sp.bits), nn)
