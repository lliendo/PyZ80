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

from ..instruction.jump import *
from .test_z80_base import TestZ80


class TestArithmetic8Bit(TestZ80):

    def test_jp_nn(self):
        """ Test JP nn """

        instruction = JpNN(self._z80)
        address = self._get_random_word()
        high_order_byte, low_order_byte = self._split_word(address)
        instruction.execute([high_order_byte, low_order_byte])
        self.assertEqual(
            self._z80.pc.bits,
            address
        )

    def test_jp_e(self):
        """ Test JR e """

        instruction = JrE(self._z80)
        address = self._get_random_word(upper_limit=0xFFFF - 0xFF)
        self._z80.pc.bits = address
        offset = self._get_random_byte()
        instruction.execute([offset])
        self.assertEqual(
            self._z80.pc.bits,
            address + offset
        )

    def _jp_ss_e_conditions(self):
        return {
            'C':  0b11,
            'NC': 0b10,
            'Z':  0b01,
            'NZ': 0b00
        }

    def test_jp_ss_e_carry_set(self):
        """ Test JP C, e (C set) """

        self._z80.f.set_carry_flag()
        instruction = JrSSE(self._z80)
        address = self._get_random_word(upper_limit=0xFFFF - 0xFF)
        offset = self._get_random_byte()
        self._z80.pc.bits = address
        instruction.execute([self._jp_ss_e_conditions()['C'], offset])
        self.assertEqual(
            self._z80.pc.bits,
            address + offset
        )

    def test_jp_ss_e_not_carry_set(self):
        """ Test JP NC, e (C set) """

        self._z80.f.set_carry_flag()
        instruction = JrSSE(self._z80)
        address = self._get_random_word(upper_limit=0xFFFF - 0xFF)
        offset = self._get_random_byte()
        self._z80.pc.bits = address
        instruction.execute([self._jp_ss_e_conditions()['NC'], offset])
        self.assertEqual(
            self._z80.pc.bits,
            address
        )

    def test_jp_ss_e_carry_reset(self):
        """ Test JP C, e (C reset) """

        instruction = JrSSE(self._z80)
        address = self._get_random_word(upper_limit=0xFFFF - 0xFF)
        offset = self._get_random_byte()
        self._z80.pc.bits = address
        instruction.execute([self._jp_ss_e_conditions()['C'], offset])
        self.assertEqual(
            self._z80.pc.bits,
            address
        )

    def test_jp_ss_e_not_carry_reset(self):
        """ Test JP NC, e (C reset) """

        instruction = JrSSE(self._z80)
        address = self._get_random_word(upper_limit=0xFFFF - 0xFF)
        offset = self._get_random_byte()
        self._z80.pc.bits = address
        instruction.execute([self._jp_ss_e_conditions()['NC'], offset])
        self.assertEqual(
            self._z80.pc.bits,
            address + offset
        )

    def test_jp_ss_e_zero_set(self):
        """ Test JP Z, e (Z set) """

        self._z80.f.set_zero_flag()
        instruction = JrSSE(self._z80)
        address = self._get_random_word(upper_limit=0xFFFF - 0xFF)
        offset = self._get_random_byte()
        self._z80.pc.bits = address
        instruction.execute([self._jp_ss_e_conditions()['Z'], offset])
        self.assertEqual(
            self._z80.pc.bits,
            address + offset
        )

    def test_jp_ss_e_not_zero_set(self):
        """ Test JP NZ, e (Z set) """

        self._z80.f.set_zero_flag()
        instruction = JrSSE(self._z80)
        address = self._get_random_word(upper_limit=0xFFFF - 0xFF)
        offset = self._get_random_byte()
        self._z80.pc.bits = address
        instruction.execute([self._jp_ss_e_conditions()['NZ'], offset])
        self.assertEqual(
            self._z80.pc.bits,
            address
        )

    def test_jp_ss_e_zero_reset(self):
        """ Test JP Z, e (Z reset) """

        instruction = JrSSE(self._z80)

        address = self._get_random_word(upper_limit=0xFFFF - 0xFF)
        offset = self._get_random_byte()
        self._z80.pc.bits = address
        instruction.execute([self._jp_ss_e_conditions()['Z'], offset])
        self.assertEqual(
            self._z80.pc.bits,
            address
        )

    def test_jp_ss_e_not_zero_reset(self):
        """ Test JP NZ, e (Z reset) """

        instruction = JrSSE(self._z80)
        address = self._get_random_word(upper_limit=0xFFFF - 0xFF)
        offset = self._get_random_byte()
        self._z80.pc.bits = address
        instruction.execute([self._jp_ss_e_conditions()['NZ'], offset])
        self.assertEqual(
            self._z80.pc.bits,
            address + offset
        )

    def test_jp_indirect_hl(self):
        """ Test JP (HL) """

        instruction = JpIndirectHL(self._z80)
        address = self._get_random_word()
        jp_address = self._get_random_byte()
        self._z80.ram.write(address, jp_address)
        self._z80.hl.bits = address
        instruction.execute()
        self.assertEqual(
            self._z80.pc.bits,
            jp_address
        )

    def test_jp_indirect_ix(self):
        """ Test JP (IX) """

        instruction = JpIndirectIX(self._z80)
        address = self._get_random_word()
        jp_address = self._get_random_byte()
        self._z80.ram.write(address, jp_address)
        self._z80.ix.bits = address
        instruction.execute()
        self.assertEqual(
            self._z80.pc.bits,
            jp_address
        )

    def test_jp_indirect_iy(self):
        """ Test JP (IY) """

        instruction = JpIndirectIY(self._z80)
        address = self._get_random_word()
        jp_address = self._get_random_byte()
        self._z80.ram.write(address, jp_address)
        self._z80.iy.bits = address
        instruction.execute()
        self.assertEqual(
            self._z80.pc.bits,
            jp_address
        )

    def test_djnz_b_non_zero(self):
        """ Test DJNZ e (B != 0) """

        instruction = DjnzE(self._z80)
        address = self._get_random_word(upper_limit=0xFFFF - 0xFF)
        offset = self._get_random_byte()
        b_bits = self._get_random_byte(upper_limit=0xFF - 1) + 1
        self._z80.pc.bits = address
        self._z80.b.bits = b_bits
        instruction.execute([offset])
        self.assertEqual(
            self._z80.pc.bits,
            address + offset
        )
        self.assertEqual(
            self._z80.b.bits,
            b_bits - 1
        )

    def test_djnz_b_zero(self):
        """ Test DJNZ e (B = 1) """

        instruction = DjnzE(self._z80)
        address = self._get_random_word(upper_limit=0xFFFF - 0xFF)
        offset = self._get_random_byte()
        self._z80.pc.bits = address
        self._z80.b.bits = 1
        instruction.execute([offset])
        self.assertEqual(
            self._z80.pc.bits,
            address
        )
        self.assertEqual(
            self._z80.b.bits,
            0x00
        )
