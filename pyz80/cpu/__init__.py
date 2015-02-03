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

from simplefsm.exceptions import FSMRejectedInput
from ..register import Z80ByteRegister, Z80WordRegister, Z80FlagsRegister
from ..fsm import Z80FSMBuilder
from ..ram import Ram
from ..io import DeviceManager
from ..instruction.decoder import InstructionDecoder


class InvalidOpcodeError(Exception):
    pass


class Z80(object):
    def __init__(self):
        self._cpu_halted = False
        self._build_registers()
        self._fsms = Z80FSMBuilder(self).build()
        self._instruction_decoder = InstructionDecoder(self)
        self.ram = Ram()
        self.device_manager = DeviceManager()

    def _build_16_bits_registers(self):
        """
        Builds the following registers :
        bc, de, hl, sp, pc, ix, iy, bc_, de_, hl_
        """

        registers = ['bc', 'de', 'hl']    
        [setattr(self, r, Z80WordRegister()) for r in registers + ['sp', 'pc', 'ix', 'iy']]
        [setattr(self, r + '_', Z80WordRegister()) for r in registers]

    def _build_8_bits_registers(self):
        """
        We keep references for lower & higher parts of 16 bits
        registers.
        """

        self.i = Z80ByteRegister()
        self.r = Z80ByteRegister()
        self.a_ = Z80ByteRegister()
        self.f_ = Z80FlagsRegister()
        self.a = Z80ByteRegister()
        self.f = Z80FlagsRegister()
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

    def _build_cpu_control_registers(self):
        self.iff1 = 0x00
        self.iff2 = 0x00
        self.im = 0x00

    def _build_registers(self):
        self._build_16_bits_registers()
        self._build_8_bits_registers()
        self._build_cpu_control_registers()

    def inc_pc(self):
        self.pc.bits += 1

    # TODO: Implement processor halt & resume mechanism.
    def halt(self):
        self._cpu_halted = True

    def _fetch_opcode(self):
        for fsm in self._fsms:
            try :
                return fsm.run()
            except FSMRejectedInput, e:
                invalid_opcode = ' '.join('{:02X}'.format(s) for s in e._symbol)

        raise InvalidOpcodeError(
            'Error - Invalid opcode : {0}.'.format(invalid_opcode) 
        )

    def load_device(self, D):
        device = D(self.device_manager)
        self.device_manager.add(device)

    def run(self, program=[], address=0x00):
        self.device_manager.run()
        self.ram.load(program, address=address)
        self.pc.bits = address

        while True:
            opcode = self._fetch_opcode()
            instruction, operands = self._instruction_decoder.decode(opcode)
