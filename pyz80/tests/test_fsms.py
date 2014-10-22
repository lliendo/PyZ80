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
from itertools import product
from mock import patch
from ..fsm import Z80FSM, Z80FSMBuilder
from ..cpu import Z80


class TestZ80ByteRegister(TestCase):
    def setUp(self):
        self._z80_fsm_builder = Z80FSMBuilder(Z80())

    def _get_ignore_byte(self):
        return randint(0x00, 0xFF)

    def _test_fsm_accepts_opcode(self, fsm, opcode):
        with patch.object(Z80FSM, 'read_symbol', side_effect=iter(opcode)):
            try:
                fsm.run()
            except StopIteration:
                self.assertEqual(fsm._accepted_symbols, opcode)

    def _test_fsm_accepts_opcodes(self, fsm, opcodes):
        [self._test_fsm_accepts_opcode(fsm, list(opcode)) for opcode in opcodes]

    def test_non_prefix_one_byte_fsm(self):
        fsm = self._z80_fsm_builder._build_non_prefix_fsm()
        opcodes, _, _ = self._z80_fsm_builder._non_prefix_fsm_bytes()
        [self._test_fsm_accepts_opcode(fsm, [opcode]) for opcode in opcodes]

    def test_non_prefix_two_bytes_fsm(self):
        fsm = self._z80_fsm_builder._build_non_prefix_fsm()
        _, non_prefix_two_bytes, _ = self._z80_fsm_builder._non_prefix_fsm_bytes()
        opcodes = [i for i in product(non_prefix_two_bytes, [self._get_ignore_byte()])]
        self._test_fsm_accepts_opcodes(fsm, opcodes)

    def test_non_prefix_three_bytes_fsm(self):
        fsm = self._z80_fsm_builder._build_non_prefix_fsm()
        _, _, non_prefix_three_bytes = self._z80_fsm_builder._non_prefix_fsm_bytes()
        opcodes = [i for i in product(non_prefix_three_bytes, [self._get_ignore_byte()], [self._get_ignore_byte()])]
        self._test_fsm_accepts_opcodes(fsm, opcodes)

    def test_cb_fsm(self):
        fsm = self._z80_fsm_builder._build_cb_fsm()
        cb_fsm_bytes = self._z80_fsm_builder._cb_fsm_bytes()
        opcodes = [i for i in product([0xCB], cb_fsm_bytes)]
        self._test_fsm_accepts_opcodes(fsm, opcodes)

    def test_ed_two_bytes_fsm(self):
        fsm = self._z80_fsm_builder._build_ed_fsm()
        ed_two_bytes, _ = self._z80_fsm_builder._ed_fsm_bytes()
        opcodes = [i for i in product([0xED], ed_two_bytes)]
        self._test_fsm_accepts_opcodes(fsm, opcodes)

    def test_ed_four_bytes_fsm(self):
        fsm = self._z80_fsm_builder._build_ed_fsm()
        _, ed_four_bytes = self._z80_fsm_builder._ed_fsm_bytes()
        opcodes = [i for i in product([0xED], ed_four_bytes, [self._get_ignore_byte()], [self._get_ignore_byte()])]
        self._test_fsm_accepts_opcodes(fsm, opcodes)

    def test_dd_two_fsm(self):
        fsm = self._z80_fsm_builder._build_dd_fsm()
        dd_two_bytes, _, _= self._z80_fsm_builder._dd_fsm_bytes()
        opcodes = [i for i in product([0xDD], dd_two_bytes)]
        self._test_fsm_accepts_opcodes(fsm, opcodes)

    def test_dd_three_fsm(self):
        fsm = self._z80_fsm_builder._build_dd_fsm()
        _, dd_three_bytes, _= self._z80_fsm_builder._dd_fsm_bytes()
        opcodes = [i for i in product([0xDD], dd_three_bytes, [self._get_ignore_byte()])]
        self._test_fsm_accepts_opcodes(fsm, opcodes)

    def test_dd_four_fsm(self):
        fsm = self._z80_fsm_builder._build_dd_fsm()
        _, _, dd_four_bytes= self._z80_fsm_builder._dd_fsm_bytes()
        opcodes = [i for i in product([0xDD], dd_four_bytes, [self._get_ignore_byte()], [self._get_ignore_byte()])]
        self._test_fsm_accepts_opcodes(fsm, opcodes)

    def test_fd_two_fsm(self):
        fsm = self._z80_fsm_builder._build_fd_fsm()
        fd_two_bytes, _, _= self._z80_fsm_builder._fd_fsm_bytes()
        opcodes = [i for i in product([0xFD], fd_two_bytes)]
        self._test_fsm_accepts_opcodes(fsm, opcodes)

    def test_fd_three_fsm(self):
        fsm = self._z80_fsm_builder._build_fd_fsm()
        _, fd_three_bytes, _= self._z80_fsm_builder._fd_fsm_bytes()
        opcodes = [i for i in product([0xFD], fd_three_bytes, [self._get_ignore_byte()])]
        self._test_fsm_accepts_opcodes(fsm, opcodes)

    def test_fd_four_fsm(self):
        fsm = self._z80_fsm_builder._build_fd_fsm()
        _, _, fd_four_bytes= self._z80_fsm_builder._fd_fsm_bytes()
        opcodes = [i for i in product([0xFD], fd_four_bytes, [self._get_ignore_byte()], [self._get_ignore_byte()])]
        self._test_fsm_accepts_opcodes(fsm, opcodes)

    def test_ddcb_fsm(self):
        fsm = self._z80_fsm_builder._build_ddcb_fsm()
        ddcb = self._z80_fsm_builder._ddcb_fsm_bytes()
        opcodes = [i for i in product([0xDD], [0xCB], [self._get_ignore_byte()], ddcb)]
        self._test_fsm_accepts_opcodes(fsm, opcodes)

    def test_fdcb_fsm(self):
        fsm = self._z80_fsm_builder._build_fdcb_fsm()
        fdcb = self._z80_fsm_builder._fdcb_fsm_bytes()
        opcodes = [i for i in product([0xFD], [0xCB], [self._get_ignore_byte()], fdcb)]
        self._test_fsm_accepts_opcodes(fsm, opcodes)
