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

from ..instruction.arithmetic_8_bit import *
from .test_z80_base import TestZ80


class TestLoadInstructions(TestZ80):
    def __init__(self, *args, **kwargs):
        super(TestLoadInstructions, self).__init__(*args, **kwargs)

    def test_add_a_r_sign_flag_is_set(self):
        """ Test ADD A, r (sign set) """

        self._z80.a.bits = 127
        self._z80.b.bits = 1
        opcode = ['10000000']
        self._decode_and_execute_opcode(opcode)
        self.assertEqual(self._z80.f.sign_flag, True)

    def test_add_a_r_sign_flag_is_reset(self):
        """ Test ADD A, r (sign reset) """

        self._z80.a.bits = 126
        self._z80.b.bits = 1
        opcode = ['10000000']
        self._decode_and_execute_opcode(opcode)
        self.assertEqual(self._z80.f.sign_flag, False)

    def test_add_a_r_overflow_is_set(self):
        """ Test ADD A, r (overflow set) """

        self._z80.a.bits = 120
        self._z80.b.bits = 105
        opcode = ['10000000']
        self._decode_and_execute_opcode(opcode)
        self.assertEqual(self._z80.f.parity_flag, True)

    def test_add_a_r_carry_is_set(self):
        """ Test ADD A, r (carry set) """

        self._z80.a.bits = 255
        self._z80.b.bits = 1
        opcode = ['10000000']
        self._decode_and_execute_opcode(opcode)
        self.assertEqual(self._z80.f.carry_flag, True)

    def test_add_a_r_carry_is_reset(self):
        """ Test ADD A, r (carry reset) """

        self._z80.a.bits = 254
        self._z80.b.bits = 1
        opcode = ['10000000']
        self._decode_and_execute_opcode(opcode)
        self.assertEqual(self._z80.f.carry_flag, False)
