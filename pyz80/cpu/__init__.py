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

from ..register import Z80Register, Z80ByteRegister, Z80WordRegister, Z80FlagsRegister
from ..fsm import Z80FSMBuilder
from ..ram import Ram
from ..instruction.decoder import InstructionDecoder


class Z80(object):
    def __init__(self, address=0x00):
        self._build_registers()
        self.ram = Ram()
        self._fsms = Z80FSMBuilder(self).build()
        self._instruction_decoder = InstructionDecoder(self)
        self.pc.bits = address

    def _build_8_bits_registers(self):
        """
        Builds the following registers :
        a, f, i, r, a_, f_
        """
        [setattr(self, r, Z80ByteRegister()) for r in ['a', 'i', 'r']]
        [setattr(self, r, Z80FlagsRegister()) for r in ['f', 'f_']]
        setattr(self, 'a_', Z80ByteRegister())

    def _build_16_bits_registers(self):
        """
        Builds the following registers :
        bc, de, hl, sp, pc, ix, iy, bc_, de_, hl_
        """
        registers = ['bc', 'de', 'hl']    
        [setattr(self, r, Z80WordRegister()) for r in registers + ['sp', 'pc', 'ix', 'iy']]
        [setattr(self, r + '_', Z80WordRegister()) for r in registers]

    def _build_registers_properties(self):
        """
        We keep references for lower & higher parts of 16 bits
        registers.
        """
        setattr(self, 'b', getattr(self, 'bc').higher)
        setattr(self, 'c', getattr(self, 'bc').lower)
        setattr(self, 'd', getattr(self, 'de').higher)
        setattr(self, 'e', getattr(self, 'de').lower)
        setattr(self, 'h', getattr(self, 'hl').higher)
        setattr(self, 'l', getattr(self, 'hl').lower)
        setattr(self, 'ixh', getattr(self, 'ix').higher)
        setattr(self, 'ixl', getattr(self, 'ix').lower)
        setattr(self, 'iyh', getattr(self, 'iy').higher)
        setattr(self, 'iyl', getattr(self, 'iy').lower)

    def _build_registers(self):
        self._build_8_bits_registers()
        self._build_16_bits_registers()
        self._build_registers_properties()
        # TODO: Still missing iff1, iff2 & im registers.

    def inc_pc(self):
        self.pc.bits += 1

    def _fetch_opcode(self):
        for fsm in self._fsms:
            try :
                return fsm.run()
            except FSMRejectedInput:
                pass

        raise Z80InvalidOpcode()

    def run(self):
        while True:
            opcode = self._fetch_opcode()
            instruction = self._instruction_decoder.decode(opcode)
            instruction.execute(opcode)
