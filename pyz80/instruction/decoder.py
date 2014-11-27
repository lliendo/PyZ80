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

from .load_8_bit import *
from .load_16_bit import *
from .arithmetic_8_bit import *


class InvalidInstructionError(Exception):
    pass


class InstructionDecoder(object):
    def __init__(self, z80):
        self._z80 = z80
        self._instructions = self._z80_instructions()

    def _8_bit_load_instructions(self):
        return [
            LoadRegisterRegisterRR,
            LoadRegisterRegisterPP,
            LoadRegisterRegisterQQ,
            LoadRegisterRNumber,
            LoadRegisterPNumber,
            LoadRegisterQNumber,
            LoadRegisterIndirectHL,
            LoadRegisterIndirectIX,
            LoadRegisterIndirectIY,
            LoadIndirectAddressHLRegister,
            LoadIndirectAddressIXRegister,
            LoadIndirectAddressIYRegister,
            LoadIndirectAddressHLNumber,
            LoadIndirectAddressIXNumber,
            LoadIndirectAddressIYNumber,
            LoadAIndirectAddressBC,
            LoadAIndirectAddressDE,
            LoadAIndirectAddressNN,
            LoadIndirectBCRegisterA,
            LoadIndirectDERegisterA,
            LoadIndirectNNRegisterA,
            LoadRegisterARegisterI,
            LoadRegisterARegisterR,
            LoadRegisterIRegisterA,
            LoadRegisterRRegisterA,
        ]

    def _16_bit_load_instructions(self):
        return [
            LoadDDNN,
            LoadIXNN,
            LoadIYNN,
            LoadHLIndirectAddressNN,
            LoadDDIndirectAddressNN,
            LoadIXIndirectAddressNN,
            LoadIYIndirectAddressNN,
            LoadIndirectAddressNNHL,
            LoadIndirectAddressNNDD,
            LoadIndirectAddressNNIX,
            LoadIndirectAddressNNIY,
            LoadSPHL,
            LoadSPIX,
            LoadSPIY,
            PushQQ,
            PushIX,
            PushIY,
            PopQQ,
            PopIX,
            PopIY,
        ]

    def _8_bit_arithmetic_instructions(self):
        return [
            AddAR,
            AddAP,
            AddAQ,
            AddAN,
            AddAIndirectAddressHLRegister,
            AddAIndirectAddressIXRegister,
            AddAIndirectAddressIYRegister,
            AdcAR,
            AdcAP,
            AdcAQ,
            AdcAN,
            AdcAIndirectAddressHLRegister,
            AdcAIndirectAddressIXRegister,
            AdcAIndirectAddressIYRegister,
            SubAR,
            SubAP,
            SubAQ,
            SubAN,
            SubAIndirectAddressHLRegister,
            SubAIndirectAddressIXRegister,
            SubAIndirectAddressIYRegister,
            SbcAR,
            SbcAP,
            SbcAQ,
            SbcAN,
            SbcAIndirectAddressHLRegister,
            SbcAIndirectAddressIXRegister,
            SbcAIndirectAddressIYRegister,
        ]

    def _z80_instructions(self):
        return self._8_bit_load_instructions() + \
            self._16_bit_load_instructions() + self._8_bit_arithmetic_instructions()

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

    def _translate(self, bytes):
        """
        Translates a list of bytes into a padded binary string.
        E.g.
            Given [0xAA, 0xBB, 0xCC, 0xDD]
            then this method will return
            10101010101110111100110011011101
        """

        bits_per_byte = 8
        n = self._bytes_to_int(bytes)
        return bin(n).lstrip('0b').zfill(len(bytes) * bits_per_byte)

    def _get_instruction(self, bytes):
        return filter(lambda I: I.regexp.match(self._translate(bytes)), self._instructions).pop()

    def _get_operands(self, Instruction, bytes):
        return map(lambda s: int(s, base=2), Instruction.regexp.match(self._translate(bytes)).groups())

    def decode(self, bytes):
        try:
            Instruction = self._get_instruction(bytes)
        except IndexError:
            raise InvalidInstruction('Not recognized instruction: {0}'.format(bytes))

        return Instruction(self._z80), self._get_operands(Instruction, bytes)
