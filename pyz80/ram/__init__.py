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

from .exceptions import RamInvalidAddress


class Ram(object):
    def __init__(self, size=1024 * 64):
        self._size = size
        self._ram = None
        self.reset()

    @property
    def size(self):
        return self._size

    def read(self, address):
        self._check_address(address)
        return self._ram[address]

    def write(self, address, bits):
        self._check_address(address)
        self._ram[address] = bits

    def _check_address(self, address):
        if (address < 0x0) or (address > self.size - 1):
            raise RamInvalidAddress(address)

    def load(self, opcodes, address=0x0):
        self._check_address(address)

        for opcode in opcodes:
            self.write(address, opcode)
            self._check_address(address)
            address += 1

    def reset(self):
        self._ram = [0x0 for i in range(0, self._size)]
