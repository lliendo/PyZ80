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
from ..cpu import Z80


class TestZ80(TestCase):
    def setUp(self):
        self._z80 = Z80()

    def test_8_bit_register_properties(self):
        registers = [
            'a', 'b', 'c', 'd', 'e', 'f', 'h', 'l',
            'i', 'r', 'ixl', 'ixh', 'iyl', 'iyh'
        ]
        [self.assertTrue(hasattr(self._z80, r)) for r in registers]

    def test_16_bit_register_properties(self):
        registers = ['bc', 'de', 'hl', 'sp', 'pc', 'ix', 'iy']
        [self.assertTrue(hasattr(self._z80, r)) for r in registers]
