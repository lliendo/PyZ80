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
from re import compile as compile_re


class Instruction(object):
    
    __metaclass__ = ABCMeta

    def __init__(self, z80):
        self._z80 = z80
        self._compiled_regexp = compile_re(self._instruction_regexp())

    @abstractmethod
    def _instruction_logic(self, *args):
        pass

    def _update_flags(self):
        pass

    @abstractmethod
    def _instruction_regexp(self):
        pass

    def regexp_match(self, bytes):
        return self._compiled_regexp.match(self._decode(bytes))

    def execute(self, bytes):
        operands = map(lambda s: int(s, base=2), self.regexp_match(bytes).groups())
        self._instruction_logic(*operands)
        self._update_flags()

    def _bytes_to_int(self, bytes):
        """
        Translates a list of bytes into an integer value.
        E.g.
            Given [0xAA, 0xCC]
            then this method will return
            43724
        """

        base = 256
        return sum([byte * pow(base, n) for n, byte in enumerate(reversed(bytes))])

    def _decode(self, bytes):
        """
        Translates a list of bytes into a padded binary string.
        E.g.
            Given [0xAA, 0xBB, 0xCC, 0xDD]
            then this method will return
            10101010101110111100110011011101
        """

        # TODO: Delete this commented code later on but before committing.
        # base = 256
        # bits = 8
        # n = sum([byte * pow(base, n) for n, byte in enumerate(reversed(bytes))])
        bits_per_byte = 8
        n = self._bytes_to_int(bytes)
        return bin(n).lstrip('0b').zfill(len(bytes) * bits_per_byte)

    def _get_address(self, ho_byte, lo_byte):
        """
        Given high and a low order byte this method returns
        an address which is the composition of the high and low
        order bytes.
        """
        return self._bytes_to_int([ho_byte, lo_byte])

    # TODO: Not necessary.
    # def _get_displaced_address(self, ho_byte, lo_byte, offset):
    #     """
    #     Similar to _get_address method plus an offset.
    #     """
    #     return self._compose_address(ho_byte, lo_byte) + offset

    def _sign_flag_update(self):
        pass

    def _zero_flag_update(self):
        pass

    def _carry_flag_update(self):
        pass

    def _add_substract_flag_update(self):
        pass

    def _parity_flag_update(self):
        pass

    def _overflow_flag_update(self, bits=8):
        pass

    def _half_carry_flag_update(self, bits=8):
        pass
