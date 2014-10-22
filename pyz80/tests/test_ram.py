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

from nose.tools import raises
from unittest import TestCase
from ..ram import Ram
from ..ram.exceptions import RamInvalidAddress


class TestRam(TestCase):
    def setUp(self):
        self._ram_module = Ram()

    @raises(RamInvalidAddress)
    def test_write_behind_upper_limit_fails(self):
        self._ram_module.write(0xFFFF + 1, 0x1)

    @raises(RamInvalidAddress)
    def test_write_behind_lower_limit_fails(self):
        self._ram_module.write(0x0 - 1, 0x1)

    @raises(RamInvalidAddress)
    def test_read_behind_upper_limit_fails(self):
        self._ram_module.read(0xFFFF + 1)

    @raises(RamInvalidAddress)
    def test_read_behind_lower_limit_fails(self):
        self._ram_module.read(0x0 - 1)

    def test_read_write(self):
        address = 0x25
        value = 0xFF
        self._ram_module.write(address, value)
        self.assertEqual(self._ram_module.read(address), 0xFF)

    def test_load(self):
        address = 0xFFFF / 2
        values = [0xFF for i in range(0, 2)]

    def test_load_fails(self):
        address = 0xFFFF - 1
        values = [0xFF for i in range(0, 2)]
        self._ram_module.load(values, address)
