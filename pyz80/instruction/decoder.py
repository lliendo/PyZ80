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

from ..arch import BYTE_SIZE
from .load_8_bit import *
from .load_16_bit import *
from .arithmetic_8_bit import *
from .exchange_and_transfer import *
from .cpu_control import *
from .arithmetic_16_bit import *
from .rotate_and_shift import *
from .bit_set_and_reset import *
from .jump import *
from .call_and_return import *
from .input_output import *


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

    def _exchange_and_transfer_instructions(self):
        return [
            Ex,
            ExAfAf_,
            Exx,
            ExIndirectSpHl,
            ExIndirectSpIx,
            ExIndirectSpIy,
            Ldi,
            Ldir,
            Ldd,
            Lddr,
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

    def _cpu_control_instructions(self):
        return [
            Daa,
            Cpl,
            Neg,
            Ccf,
            Scf,
            Nop,
            Halt,
            Di,
            Ei,
            Im0,
            Im1,
            Im2,
        ]

    def _16_bit_arithmetic_instructions(self):
        return [
            AddHLSS,
            AddIXPP,
            AddIYQQ,
            AdcHLSS,
            SbcHLSS,
            IncSS,
            IncIX,
            IncIY,
            DecSS,
            DecIX,
            DecIY,
        ]

    def _rotate_and_shift_instructions(self):
        return [
            Rlca,
            RlcR,
            RlcIndirectAddressHL,
            RlcIndirectAddressIX,
            RlcIndirectAddressIY,
            RlcIndirectAddressIXR,
            RlcIndirectAddressIYR,
            Rrca,
            RrcR,
            RrcIndirectAddressHL,
            RrcIndirectAddressIX,
            RrcIndirectAddressIY,
            Rla,
            RlR,
            RlIndirectAddressHL,
            RlIndirectAddressIX,
            RlIndirectAddressIY,
            Rra,
            RrR,
            RrIndirectAddressHL,
            RrIndirectAddressIX,
            RrIndirectAddressIY,
            SlaR,
            SlaIndirectAddressHL,
            SlaIndirectAddressIX,
            SlaIndirectAddressIY,
            SllR,
            SllIndirectAddressHL,
            SllIndirectAddressIX,
            SllIndirectAddressIY,
            SraR,
            SraIndirectAddressHL,
            SraIndirectAddressIX,
            SraIndirectAddressIY,
            SrlR,
            SrlIndirectAddressHL,
            SrlIndirectAddressIX,
            SrlIndirectAddressIY,
            Rld,
            Rrd
        ]

    def _bit_set_and_reset_instructions(self):
        return [
            BitTest,
            BitTestIndirectAddressHL,
            BitTestIndirectAddressIX,
            BitTestIndirectAddressIY,
            BitSet,
            BitSetIndirectAddressHL,
            BitSetIndirectAddressIX,
            BitSetIndirectAddressIYRegister,
            BitSetIndirectAddressIXRegister,
            BitSetIndirectAddressIYRegister,
            BitReset,
            BitResetIndirectAddressHL,
            BitResetIndirectAddressIX,
            BitResetIndirectAddressIYRegister,
            BitResetIndirectAddressIXRegister,
            BitResetIndirectAddressIYRegister
        ]

    def _jump_instructions(self):
        return [
            JpNN,
            JpCCNN,
            JrE,
            JrSSE,
            JpIndirectAddressHL,
            JpIndirectAddressIX,
            JpIndirectAddressIY,
            DjnzE
        ]

    def _call_and_return_instructions(self):
        return [
            CallNN,
            CallCCNN,
            Ret,
            RetCC,
            Reti,
            Retn,
            Rst
        ]

    def _input_output_instructions(self):
        return [
            InAIndirectN,
            InRIndirectC,
            InFIndirectN,
            Ini,
            Inir,
            Ind,
            Indr,
            OutAIndirectN,
            OutRIndirectC,
            OutFIndirectN,
            Outi,
            Otir,
            Outd,
            Otdr
        ]

    def _z80_instructions(self):
        return self._8_bit_load_instructions() + \
            self._16_bit_load_instructions() + \
            self._8_bit_arithmetic_instructions() + \
            self._exchange_and_transfer_instructions() + \
            self._cpu_control_instructions() + \
            self._16_bit_arithmetic_instructions() + \
            self._rotate_and_shift_instructions() + \
            self._bit_set_and_reset_instructions() + \
            self._jump_instructions() + \
            self._call_and_return_instructions() + \
            self._input_output_instructions()

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

        n = self._bytes_to_int(bytes)
        return bin(n).lstrip('0b').zfill(len(bytes) * BYTE_SIZE)

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
