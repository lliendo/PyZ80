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

from abc import ABCMeta, abstractmethod
from ..register import Z80FlagsRegister


class Instruction(object):
    
    __metaclass__ = ABCMeta
    instruction_regexp = None

    def __init__(self, z80):
        self._z80 = z80
        self._instruction_flags = Z80FlagsRegister(bits=self._z80.f.bits)

    @abstractmethod
    def _instruction_logic(self, *operands):
        pass

    def execute(self, operands):
        self._instruction_logic(*operands)
        return self._instruction_flags
        # self._update_flags()

    def _get_address(self, ho_byte, lo_byte):
        """
        Given high and a low order byte this method returns
        an address which is the composition of the high and low
        order bytes.
        """
        base = 256
        return (ho_byte * base) + lo_byte
