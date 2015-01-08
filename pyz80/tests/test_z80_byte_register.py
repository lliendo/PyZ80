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
from ..register import Z80ByteRegister


class TestZ80ByteRegister(TestCase):
    def setUp(self):
        self._bit_pattern = 0b11111010
        self._higher_bit_pattern = 0b1111
        self._lower_bit_pattern = 0b1010

    def test_lower_bits(self):
        register = Z80ByteRegister(bits=self._bit_pattern)
        self.assertEqual(register.lower, self._lower_bit_pattern)

    def test_higher_bits(self):
        register = Z80ByteRegister(bits=self._bit_pattern)
        self.assertEqual(register.higher, self._higher_bit_pattern)

    def test_set_lower_bits(self):
        register = Z80ByteRegister(bits=self._bit_pattern)
        register.lower = self._higher_bit_pattern
        self.assertEqual(register.lower, self._higher_bit_pattern)
        self.assertEqual(register.higher, self._higher_bit_pattern)

    def test_set_higher_bits(self):
        register = Z80ByteRegister(bits=self._bit_pattern)
        register.higher = self._lower_bit_pattern
        self.assertEqual(register.higher, self._lower_bit_pattern)
        self.assertEqual(register.lower, self._lower_bit_pattern)

    def test_rotate_left(self):
        register = Z80ByteRegister(bits=self._bit_pattern)
        [register.rotate_left() for i in range(0, 4)]
        self.assertEqual(register.lower, self._higher_bit_pattern)
        self.assertEqual(register.higher, self._lower_bit_pattern)

    def test_rotate_right(self):
        register = Z80ByteRegister(bits=self._bit_pattern)
        [register.rotate_right() for i in range(0, 4)]
        self.assertEqual(register.lower, self._higher_bit_pattern)
        self.assertEqual(register.higher, self._lower_bit_pattern)

    def test_shift_left(self):
        register = Z80ByteRegister(bits=self._bit_pattern)
        [register.shift_left() for i in range(0, 4)]
        self.assertEqual(register.lower, 0b0)
        self.assertEqual(register.higher, self._lower_bit_pattern)

    def test_shift_right(self):
        register = Z80ByteRegister(bits=self._bit_pattern)
        [register.shift_right() for i in range(0, 4)]
        self.assertEqual(register.higher, 0b0)
        self.assertEqual(register.lower, self._higher_bit_pattern)

    def test_combine_registers(self):
        register = Z80ByteRegister(bits=self._bit_pattern)
        another_register = Z80ByteRegister(bits=self._bit_pattern)
        combined_register = register.combine(another_register)
        self.assertEqual(combined_register.bits, 0b1111101011111010)
        self.assertEqual(combined_register.size, register.size * 2)

    def test_register_equality(self):
        self.assertEqual(
            Z80ByteRegister(bits=self._bit_pattern),
            Z80ByteRegister(bits=self._bit_pattern)
        )

    def test_msb_bit(self):
        register = Z80ByteRegister(bits=0xA0)
        self.assertTrue(register.msb)
        register.bits = 0x40
        self.assertFalse(register.msb)

    def test_lsb_bit(self):
        register = Z80ByteRegister(bits=0x5)
        self.assertTrue(register.lsb)
        register.bits = 0x4
        self.assertFalse(register.lsb)
