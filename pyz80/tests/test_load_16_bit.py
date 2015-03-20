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

from ..instruction.load_16_bit import *
from .test_z80_base import TestZ80


class TestLoadInstructions(TestZ80):

    def _registers(self):
        return {
            0b00: self._z80.bc,
            0b01: self._z80.de,
            0b10: self._z80.hl,
            0b11: self._z80.sp,
        }

    def test_load_register_nn(self):
        """ Test LD dd, nn """

        instruction = LdDDNN(self._z80)

        for selector, register in self._registers().iteritems():
            word = self._get_random_word()
            high_order_byte, low_order_byte = self._split_word(word)
            instruction.execute([selector, high_order_byte, low_order_byte])
            self.assertEqual(
                register.bits,
                word
            )

    def test_load_ix_nn(self):
        """ Test LD IX, nn """

        instruction = LdIXNN(self._z80)
        word = self._get_random_word()
        high_order_byte, low_order_byte = self._split_word(word)
        instruction.execute([high_order_byte, low_order_byte])
        self.assertEqual(
            self._z80.ix.bits,
            word
        )

    def test_load_iy_nn(self):
        """ Test LD IY, nn """

        instruction = LdIYNN(self._z80)
        word = self._get_random_word()
        high_order_byte, low_order_byte = self._split_word(word)
        instruction.execute([high_order_byte, low_order_byte])
        self.assertEqual(
            self._z80.iy.bits,
            word
        )

    def test_load_hl_indirect_nn(self):
        """ Test LD HL, (nn) """

        instruction = LdHLIndirectNN(self._z80)
        address = self._get_random_word()
        word = self._get_random_word()
        high_order_byte, low_order_byte = self._split_word(address)
        self._write_ram_word(address, word)
        instruction.execute([high_order_byte, low_order_byte])
        self.assertEqual(
            self._z80.hl.bits,
            word
        )


    def test_load_dd_indirect_nn(self):
        """ Test LD dd, (nn) """

        instruction = LdDDIndirectNN(self._z80)

        for selector, register in self._registers().iteritems():
            address = self._get_random_word()
            word = self._get_random_word()
            high_order_byte, low_order_byte = self._split_word(address)
            self._write_ram_word(address, word)
            instruction.execute([selector, high_order_byte, low_order_byte])
            self.assertEqual(
                register.bits,
                word
            )

    def test_load_ix_indirect_nn(self):
        """ Test LD IX, (nn) """

        instruction = LdIXIndirectNN(self._z80)
        address = self._get_random_word()
        word = self._get_random_word()
        self._write_ram_word(address, word)
        high_order_byte, low_order_byte = self._split_word(address)
        instruction.execute([high_order_byte, low_order_byte])
        self.assertEqual(
            self._z80.ix.bits,
            word
        )

    def test_load_iy_indirect_nn(self):
        """ Test LD IY, (nn) """

        instruction = LdIYIndirectNN(self._z80)
        address = self._get_random_word()
        word = self._get_random_word()
        self._write_ram_word(address, word)
        high_order_byte, low_order_byte = self._split_word(address)
        instruction.execute([high_order_byte, low_order_byte])
        self.assertEqual(
            self._z80.iy.bits,
            word
        )

    def test_load_indirect_nn_hl(self):
        """ Test LD (nn), HL """

        instruction = LdIndirectNNHL(self._z80)
        address = self._get_random_word()
        word = self._get_random_word()
        self._z80.hl.bits = word
        high_order_byte, low_order_byte = self._split_word(address)
        instruction.execute([high_order_byte, low_order_byte])
        self.assertEqual(
            self._read_ram_word(address),
            word
        )

    def test_load_indirect_nn_dd(self):
        """ Test LD (nn), dd """

        instruction = LdIndirectNNDD(self._z80)

        for selector, register in self._registers().iteritems():
            address = self._get_random_word()
            word = self._get_random_word()
            high_order_byte, low_order_byte = self._split_word(address)
            register.bits = word
            instruction.execute([selector, high_order_byte, low_order_byte])
            self.assertEqual(
                self._read_ram_word(address),
                word
            )

    def test_load_indirect_nn_ix(self):
        """ Test LD (nn), IX """

        instruction = LdIndirectNNIX(self._z80)
        address = self._get_random_word()
        word = self._get_random_word()
        high_order_byte, low_order_byte = self._split_word(address)
        self._z80.ix.bits = word
        instruction.execute([high_order_byte, low_order_byte])
        self.assertEqual(
            self._read_ram_word(address),
            word
        )

    def test_load_indirect_nn_iy(self):
        """ Test LD (nn), IY """

        instruction = LdIndirectNNIY(self._z80)
        address = self._get_random_word()
        word = self._get_random_word()
        high_order_byte, low_order_byte = self._split_word(address)
        self._z80.iy.bits = word
        instruction.execute([high_order_byte, low_order_byte])
        self.assertEqual(
            self._read_ram_word(address),
            word
        )

    def test_load_sp_hl(self):
        """ Test LD SP, HL """

        instruction = LdSPHL(self._z80)
        word = self._get_random_word()
        self._z80.hl.bits = word
        instruction.execute()
        self.assertEqual(
            self._z80.sp.bits,
            self._z80.hl.bits
        )

    def test_load_sp_ix(self):
        """ Test LD SP, IX """

        instruction = LdSPIX(self._z80)
        word = self._get_random_word()
        self._z80.hl.bits = word
        instruction.execute()
        self.assertEqual(
            self._z80.sp.bits,
            self._z80.ix.bits
        )

    def test_load_sp_iy(self):
        """ Test LD SP, IY """

        instruction = LdSPIY(self._z80)
        word = self._get_random_word()
        self._z80.hl.bits = word
        instruction.execute()
        self.assertEqual(
            self._z80.sp.bits,
            self._z80.iy.bits
        )

    def test_push_qq(self):
        """ Test PUSH qq """

        registers = {
            0b00: self._z80.bc,
            0b01: self._z80.de,
            0b10: self._z80.hl,
            # 0b11: self._z80.af,
        }

        instruction = PushQQ(self._z80)

        for selector, register in registers.iteritems():
            address = self._get_random_word()
            self._z80.sp.bits = address
            word = self._get_random_word()
            register.bits = word
            instruction.execute([selector])
            self.assertEqual(
                self._read_ram_word(self._z80.sp.bits),
                word
            )
            self.assertEqual(
                self._z80.sp.bits,
                address - 2
            )

    def test_push_ix(self):
        """ Test PUSH IX """

        instruction = PushIX(self._z80)
        address = self._get_random_word()
        self._z80.sp.bits = address
        word = self._get_random_word()
        self._z80.ix.bits = word
        instruction.execute([])
        self.assertEqual(
            self._read_ram_word(self._z80.sp.bits),
            word
        )
        self.assertEqual(
            self._z80.sp.bits,
            address - 2
        )

    def test_push_iy(self):
        """ Test PUSH IY """

        instruction = PushIY(self._z80)
        address = self._get_random_word()
        self._z80.sp.bits = address
        word = self._get_random_word()
        self._z80.iy.bits = word
        instruction.execute([])
        self.assertEqual(
            self._read_ram_word(self._z80.sp.bits),
            word
        )
        self.assertEqual(
            self._z80.sp.bits,
            address - 2
        )

    def test_pop_qq(self):
        """ Test POP qq """

        registers = {
            0b00: self._z80.bc,
            0b01: self._z80.de,
            0b10: self._z80.hl,
            # 0b11: self._z80.af,
        }

        instruction = PopQQ(self._z80)

        for selector, register in registers.iteritems():
            address = self._get_random_word()
            self._z80.sp.bits = address
            word = self._get_random_word()
            self._write_ram_word(self._z80.sp.bits, word)
            instruction.execute([selector])
            self.assertEqual(
                register.bits,
                word
            )
            self.assertEqual(
                self._z80.sp.bits,
                address + 2
            )

    def test_pop_ix(self):
        """ Test POP IX """

        instruction = PopIX(self._z80)
        address = self._get_random_word()
        self._z80.sp.bits = address
        word = self._get_random_word()
        self._write_ram_word(self._z80.sp.bits, word)
        instruction.execute()
        self.assertEqual(
            self._z80.ix.bits,
            word
        )
        self.assertEqual(
            self._z80.sp.bits,
            address + 2
        )

    def test_pop_iy(self):
        """ Test POP IY """

        instruction = PopIY(self._z80)
        address = self._get_random_word()
        self._z80.sp.bits = address
        word = self._get_random_word()
        self._write_ram_word(self._z80.sp.bits, word)
        instruction.execute()
        self.assertEqual(
            self._z80.iy.bits,
            word
        )
        self.assertEqual(
            self._z80.sp.bits,
            address + 2
        )
