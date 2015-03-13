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
from ..cpu import Z80
from ..instruction.decoder import InstructionDecoder
from ..io import DeviceManager
from ..ram import Ram
from ..arch import BYTE_SIZE, WORD_SIZE


class TestZ80(TestCase):
    def setUp(self):
        self.longmessage = True
        self._z80 = Z80(
            ram=Ram(), device_manager=DeviceManager(),
            trace_fd=None
        )

    def _get_random_byte(self, upper_limit=0xFF):
        return randint(0x00, upper_limit)

    def _get_random_word(self, upper_limit=0xFFFF):
        return randint(0x00, upper_limit)

    def _load_z80_registers(self, registers):
        for r in registers:
            r.bits = self._get_random_byte()

    def _write_ram_word(self, address, word):
        high_order_byte, low_order_byte = self._split_word(word)
        self._z80.ram.write(address + 1, high_order_byte)
        self._z80.ram.write(address, low_order_byte)

    def _read_ram_word(self, address):
        high_order_byte = self._z80.ram.read(address + 1)
        low_order_byte = self._z80.ram.read(address)
        return self._compose_word(high_order_byte, low_order_byte)

    def _compose_word(self, high_order_byte, low_order_byte, word_size=WORD_SIZE):
        return (high_order_byte << (WORD_SIZE / 2)) + low_order_byte

    def _split_word(self, word, word_size=WORD_SIZE):
        high_order_byte = (word & 0xFF00) >> (WORD_SIZE / 2)
        low_order_byte = word & 0xFF
        return high_order_byte, low_order_byte
