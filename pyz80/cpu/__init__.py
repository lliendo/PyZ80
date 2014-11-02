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

    def _build_16_bits_registers(self):
        """
        Builds the following registers :
        bc, de, hl, sp, pc, ix, iy, bc_, de_, hl_
        """

        registers = ['af', 'bc', 'de', 'hl']    
        [setattr(self, r, Z80WordRegister()) for r in registers + ['sp', 'pc', 'ix', 'iy']]
        [setattr(self, r + '_', Z80WordRegister()) for r in registers]

    def _build_8_bits_registers(self):
        """
        We keep references for lower & higher parts of 16 bits
        registers.
        """

        self.i = Z80ByteRegister()
        self.r = Z80ByteRegister()
        self.a_ = self.af_.higher
        self.f_ = self.af_.lower
        self.a = self.af.higher
        self.f = self.af.lower
        self.b = self.bc.higher
        self.c = self.bc.lower
        self.d = self.de.higher
        self.e = self.de.lower
        self.h = self.hl.higher
        self.l = self.hl.lower
        self.ixh = self.ix.higher
        self.ixl = self.ix.lower
        self.iyh = self.iy.higher
        self.iyl = self.iy.lower

    def _build_registers(self):
        self._build_16_bits_registers()
        self._build_8_bits_registers()
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
