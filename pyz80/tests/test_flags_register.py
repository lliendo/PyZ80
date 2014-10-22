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
from ..register import Z80FlagsRegister


class TestZ80Flags(TestCase):
    def setUp(self):
        self._flags_register = Z80FlagsRegister()

    def test_sign_flag(self):
        self.assertEqual(self._flags_register.sign_flag, False)
        self._flags_register.set_sign_flag()
        self.assertEqual(self._flags_register.sign_flag, True)
        self._flags_register.reset_sign_flag()
        self.assertEqual(self._flags_register.sign_flag, False)
        self.assertEqual(self._flags_register.zero_flag, False)
        self.assertEqual(self._flags_register.half_carry_flag, False)
        self.assertEqual(self._flags_register.parity_flag, False)
        self.assertEqual(self._flags_register.add_substract_flag, False)
        self.assertEqual(self._flags_register.carry_flag, False)
    
    def test_zero_flag(self):
        self.assertEqual(self._flags_register.zero_flag, False)
        self._flags_register.set_zero_flag()
        self.assertEqual(self._flags_register.zero_flag, True)
        self._flags_register.reset_zero_flag()
        self.assertEqual(self._flags_register.zero_flag, False)
        self.assertEqual(self._flags_register.sign_flag, False)
        self.assertEqual(self._flags_register.half_carry_flag, False)
        self.assertEqual(self._flags_register.parity_flag, False)
        self.assertEqual(self._flags_register.add_substract_flag, False)
        self.assertEqual(self._flags_register.carry_flag, False)

    def test_half_carry_flag(self):
        self.assertEqual(self._flags_register.half_carry_flag, False)
        self._flags_register.set_half_carry_flag()
        self.assertEqual(self._flags_register.half_carry_flag, True)
        self._flags_register.reset_half_carry_flag()
        self.assertEqual(self._flags_register.half_carry_flag, False)
        self.assertEqual(self._flags_register.zero_flag, False)
        self.assertEqual(self._flags_register.sign_flag, False)
        self.assertEqual(self._flags_register.parity_flag, False)
        self.assertEqual(self._flags_register.add_substract_flag, False)
        self.assertEqual(self._flags_register.carry_flag, False)

    def test_parity_flag(self):
        self.assertEqual(self._flags_register.parity_flag, False)
        self._flags_register.set_parity_flag()
        self.assertEqual(self._flags_register.parity_flag, True)
        self._flags_register.reset_parity_flag()
        self.assertEqual(self._flags_register.parity_flag, False)
        self.assertEqual(self._flags_register.zero_flag, False)
        self.assertEqual(self._flags_register.half_carry_flag, False)
        self.assertEqual(self._flags_register.sign_flag, False)
        self.assertEqual(self._flags_register.add_substract_flag, False)
        self.assertEqual(self._flags_register.carry_flag, False)

    def test_add_substract_flag(self):
        self.assertEqual(self._flags_register.add_substract_flag, False)
        self._flags_register.set_add_substract_flag()
        self.assertEqual(self._flags_register.add_substract_flag, True)
        self._flags_register.reset_add_substract_flag()
        self.assertEqual(self._flags_register.add_substract_flag, False)
        self.assertEqual(self._flags_register.zero_flag, False)
        self.assertEqual(self._flags_register.half_carry_flag, False)
        self.assertEqual(self._flags_register.parity_flag, False)
        self.assertEqual(self._flags_register.sign_flag, False)
        self.assertEqual(self._flags_register.carry_flag, False)

    def test_carry_flag(self):
        self.assertEqual(self._flags_register.carry_flag, False)
        self._flags_register.set_carry_flag()
        self.assertEqual(self._flags_register.carry_flag, True)
        self._flags_register.reset_carry_flag()
        self.assertEqual(self._flags_register.carry_flag, False)
        self.assertEqual(self._flags_register.zero_flag, False)
        self.assertEqual(self._flags_register.half_carry_flag, False)
        self.assertEqual(self._flags_register.parity_flag, False)
        self.assertEqual(self._flags_register.add_substract_flag, False)
        self.assertEqual(self._flags_register.sign_flag, False)
