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


# TODO: Ld all classes using the ClassLder ?
class InstructionDecoder(object):
    def __init__(self, z80):
        self._z80 = z80
        self._instructions = self._z80_instructions()

    def _8_bit_load_instructions(self):
        return [
            LdRR,
            LdPP,
            LdQQ,
            LdRN,
            LdPN,
            LdQN,
            LdRIndirectHL,
            LdRIndirectIX,
            LdRIndirectIY,
            LdIndirectHLR,
            LdIndirectIXR,
            LdIndirectIYR,
            LdIndirectHLN,
            LdIndirectIXN,
            LdIndirectIYN,
            LdAIndirectBC,
            LdAIndirectDE,
            LdAIndirectNN,
            LdIndirectBCA,
            LdIndirectDEA,
            LdIndirectNNA,
            LdAI,
            LdAR,
            LdIA,
            LdRA,
        ]

    def _16_bit_load_instructions(self):
        return [
            LdDDNN,
            LdIXNN,
            LdIYNN,
            LdHLIndirectNN,
            LdDDIndirectNN,
            LdIXIndirectNN,
            LdIYIndirectNN,
            LdIndirectNNHL,
            LdIndirectNNDD,
            LdIndirectNNIX,
            LdIndirectNNIY,
            LdSPHL,
            LdSPIX,
            LdSPIY,
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
            ExAFAF_,
            Exx,
            ExIndirectSPHL,
            ExIndirectSPIX,
            ExIndirectSPIY,
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
            AddAIndirectHL,
            AddAIndirectIX,
            AddAIndirectIY,
            AdcAR,
            AdcAP,
            AdcAQ,
            AdcAN,
            AdcAIndirectHL,
            AdcAIndirectIX,
            AdcAIndirectIY,
            SubAR,
            SubAP,
            SubAQ,
            SubAN,
            SubAIndirectHL,
            SubAIndirectIX,
            SubAIndirectIY,
            SbcAR,
            SbcAP,
            SbcAQ,
            SbcAN,
            SbcAIndirectHL,
            SbcAIndirectIX,
            SbcAIndirectIY,
            AndAR,
            AndAP,
            AndAQ,
            AndAN,
            AndAIndirectHL,
            AndAIndirectIX,
            AndAIndirectIY,
            OrAR,
            OrAP,
            OrAQ,
            OrAN,
            OrAIndirectHL,
            OrAIndirectIX,
            OrAIndirectIY,
            XorAR,
            XorAP,
            XorAQ,
            XorAN,
            XorAIndirectHL,
            XorAIndirectIX,
            XorAIndirectIY,
            CpAR,
            CpAP,
            CpAQ,
            CpAN,
            CpAIndirectHL,
            CpAIndirectIX,
            CpAIndirectIY,
            IncAR,
            IncAP,
            IncAQ,
            IncIndirectHL,
            IncIndirectIX,
            IncIndirectIY,
            DecAR,
            DecAP,
            DecAQ,
            DecIndirectHL,
            DecIndirectIX,
            DecIndirectIY,
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
            RlcIndirectHL,
            RlcIndirectIX,
            RlcIndirectIY,
            RlcIndirectIXR,
            RlcIndirectIYR,
            Rrca,
            RrcR,
            RrcIndirectHL,
            RrcIndirectIX,
            RrcIndirectIY,
            Rla,
            RlR,
            RlIndirectHL,
            RlIndirectIX,
            RlIndirectIY,
            Rra,
            RrR,
            RrIndirectHL,
            RrIndirectIX,
            RrIndirectIY,
            SlaR,
            SlaIndirectHL,
            SlaIndirectIX,
            SlaIndirectIY,
            SllR,
            SllIndirectHL,
            SllIndirectIX,
            SllIndirectIY,
            SraR,
            SraIndirectHL,
            SraIndirectIX,
            SraIndirectIY,
            SrlR,
            SrlIndirectHL,
            SrlIndirectIX,
            SrlIndirectIY,
            Rld,
            Rrd,
        ]

    def _bit_set_and_reset_instructions(self):
        return [
            BitTest,
            BitTestIndirectHL,
            BitTestIndirectIX,
            BitTestIndirectIY,
            BitSet,
            BitSetIndirectHL,
            BitSetIndirectIX,
            BitSetIndirectIY,
            BitSetIndirectIXR,
            BitSetIndirectIYR,
            BitReset,
            BitResetIndirectHL,
            BitResetIndirectIX,
            BitResetIndirectIY,
        ]

    def _jump_instructions(self):
        return [
            JpNN,
            JpCCNN,
            JrE,
            JrSSE,
            JpIndirectHL,
            JpIndirectIX,
            JpIndirectIY,
            DjnzE,
        ]

    def _call_and_return_instructions(self):
        return [
            CallNN,
            CallCCNN,
            Ret,
            RetCC,
            Reti,
            Retn,
            Rst,
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
            Otdr,
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

    def _get_instruction(self, opcode):
        return filter(lambda I: I.regexp.match(self._translate(opcode)), self._instructions).pop()

    def _get_operands(self, Instruction, opcode):
        return map(lambda s: int(s, base=2), Instruction.regexp.match(self._translate(opcode)).groups())

    def decode(self, opcode):
        try:
            Instruction = self._get_instruction(opcode)
        except IndexError:
            invalid_instruction = ' '.join('{:02X}'.format(byte) for byte in opcode)
            raise InvalidInstructionError(
                'Error - Invalid instruction: {0}.'.format(invalid_instruction)
            )

        return Instruction(self._z80), self._get_operands(Instruction, opcode)
