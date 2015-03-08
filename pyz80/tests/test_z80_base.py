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

    def _bin_to_int(self, n):
        return int(n, base=2)

    def _opcode_to_int(self, opcode):
        return map(lambda o: self._bin_to_int(o), opcode)

    def _int_to_bin(self, n, padding=BYTE_SIZE):
        return '{0}'.format(bin(n).lstrip('0b').zfill(padding))

    def _word_to_bin(self, n):
        word = self._int_to_bin(n, padding=WORD_SIZE)
        return word[:WORD_SIZE / 2], word[WORD_SIZE / 2:]

    def _write_ram_word(self, address, value):
        n, m = self._word_to_bin(value)
        self._z80.ram.write(address + 1, self._bin_to_int(n))
        self._z80.ram.write(address, self._bin_to_int(m))

    def _read_ram_word(self, address):
        return self._z80.ram.read(address) + self._z80.ram.read(address + 1) * 256

    def _decode_and_execute_opcode(self, opcode):
        bytes = self._opcode_to_int(opcode)
        instruction, operands = InstructionDecoder(self._z80).decode(bytes)
        return instruction.execute(operands)
