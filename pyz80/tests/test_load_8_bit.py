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

from itertools import product
from ..instruction.load_8_bit import *
from .test_z80_base import TestZ80


class TestLoadInstructions(TestZ80):

    def _r_registers(self):
        return {
            0b000: self._z80.b,
            0b001: self._z80.c,
            0b010: self._z80.d,
            0b011: self._z80.e,
            0b100: self._z80.h,
            0b101: self._z80.l,
            0b111: self._z80.a,
        }

    def _p_registers(self):
        registers = self._r_registers()
        registers.update({
            0b100: self._z80.ixh,
            0b101: self._z80.ixl,
        })

        return registers

    def _q_registers(self):
        registers = self._r_registers()
        registers.update({
            0b100: self._z80.iyh,
            0b101: self._z80.iyl,
        })

        return registers

    def test_load_register_register_rr(self):
        """ Test LD r, r' """

        instruction = LoadRR(self._z80)

        for (destination_selector, source_selector) in product(self._r_registers().keys(), self._r_registers().keys()):
            self._load_z80_registers(
                [self._r_registers()[destination_selector], self._r_registers()[source_selector]]
            )
            instruction.execute([destination_selector, source_selector])
            self.assertEqual(
                self._r_registers()[destination_selector],
                self._r_registers()[source_selector]
            )

    def test_load_register_register_pp(self):
        """ Test LD p, p' """

        instruction = LoadPP(self._z80)

        for (destination_selector, source_selector) in product(self._p_registers().keys(), self._p_registers().keys()):
            self._load_z80_registers(
                [self._p_registers()[destination_selector], self._p_registers()[source_selector]]
            )
            instruction.execute([destination_selector, source_selector])
            self.assertEqual(
                self._p_registers()[destination_selector],
                self._p_registers()[source_selector]
            )

    def test_load_register_register_qq(self):
        """ Test LD q, q' """

        instruction = LoadQQ(self._z80)

        for (destination_selector, source_selector) in product(self._q_registers().keys(), self._q_registers().keys()):
            self._load_z80_registers(
                [self._q_registers()[destination_selector], self._q_registers()[source_selector]]
            )
            instruction.execute([destination_selector, source_selector])
            self.assertEqual(
                self._q_registers()[destination_selector],
                self._q_registers()[source_selector]
            )

    def test_load_register_r_number(self):
        """ Test LD r, n """

        instruction = LoadRN(self._z80)

        for selector, register in self._r_registers().iteritems():
            byte = self._get_random_byte()
            instruction.execute([selector, byte])
            self.assertEqual(
                register.bits,
                byte
            )

    def test_load_register_p_number(self):
        """ Test LD p, n """

        instruction = LoadPN(self._z80)

        for selector, register in self._p_registers().iteritems():
            byte = self._get_random_byte()
            instruction.execute([selector, byte])
            self.assertEqual(
                register.bits,
                byte
            )

    def test_load_register_q_number(self):
        """ Test LD q, n """

        instruction = LoadQN(self._z80)

        for selector, register in self._q_registers().iteritems():
            byte = self._get_random_byte()
            instruction.execute([selector, byte])
            self.assertEqual(
                register.bits,
                byte
            )

    def test_load_register_indirect_hl(self):
        """ Test LD r, (HL) """

        instruction = LoadRIndirectHL(self._z80)

        for selector, register in self._r_registers().iteritems():
            byte = self._get_random_byte()
            address = self._get_random_word()
            self._z80.ram.write(address, byte)
            self._z80.hl.bits = address
            instruction.execute([selector])
            self.assertEqual(
                register.bits,
                byte
            )

    def test_load_register_indirect_ix(self):
        """ Test LD r, (IX + d) """

        instruction = LoadRIndirectIX(self._z80)

        for selector, register in self._r_registers().iteritems():
            byte = self._get_random_byte()
            address = self._get_random_word(upper_limit=0xFFFF - 0xFF)
            offset = self._get_random_byte()
            self._z80.ram.write(address + offset, byte)
            self._z80.ix.bits = address
            instruction.execute([selector, offset])
            self.assertEqual(
                register.bits,
                byte
            )

    def test_load_register_indirect_iy(self):
        """ Test LD r, (IY + d) """

        instruction = LoadRIndirectIY(self._z80)

        for selector, register in self._r_registers().iteritems():
            byte = self._get_random_byte()
            address = self._get_random_word(upper_limit=0xFFFF - 0xFF)
            offset = self._get_random_byte()
            self._z80.ram.write(address + offset, byte)
            self._z80.iy.bits = address
            instruction.execute([selector, offset])
            self.assertEqual(
                register.bits,
                byte
            )

    def test_load_indirect_address_hl_register(self):
        """ Test LD (HL), r """

        instruction = LoadRIndirectHL(self._z80)

        for selector, register in self._r_registers().iteritems():
            address = self._get_random_word()
            register.bits = self._get_random_byte()
            self._z80.hl.bits = address
            instruction.execute([selector])
            self.assertEqual(
                register.bits,
                self._z80.ram.read(address)
            )

    def test_load_indirect_address_ix_register(self):
        """ Test LD (IX + d), r """

        instruction = LoadIndirectIXR(self._z80)

        for selector, register in self._r_registers().iteritems():
            address = self._get_random_word(upper_limit=0xFFFF - 0xFF)
            offset = self._get_random_byte()
            register.bits = self._get_random_byte()
            self._z80.ix.bits = address
            instruction.execute([selector, offset])
            self.assertEqual(
                register.bits,
                self._z80.ram.read(address + offset)
            )

    def test_load_indirect_address_iy_register(self):
        """ Test LD (IY + d), r """

        instruction = LoadIndirectIYR(self._z80)

        for selector, register in self._r_registers().iteritems():
            address = self._get_random_word(upper_limit=0xFFFF - 0xFF)
            offset = self._get_random_byte()
            register.bits = self._get_random_byte()
            self._z80.iy.bits = address
            instruction.execute([selector, offset])
            self.assertEqual(
                register.bits,
                self._z80.ram.read(address + offset)
            )

    def test_load_indirect_address_hl_number(self):
        """ Test LD (HL), n """

        instruction = LoadIndirectHLN(self._z80)
        byte = self._get_random_byte()
        address = self._get_random_word()
        self._z80.hl.bits = address
        instruction.execute([byte])
        self.assertEqual(
            self._z80.ram.read(address),
            byte
        )

    def test_load_indirect_address_ix_number(self):
        """ Test LD (IX + d), n """

        instruction = LoadIndirectIXN(self._z80)
        byte = self._get_random_byte()
        address = self._get_random_word(upper_limit=0xFFFF - 0xFF)
        offset = self._get_random_byte()
        self._z80.ix.bits = address
        instruction.execute([offset, byte])
        self.assertEqual(
            self._z80.ram.read(address + offset),
            byte
        )

    def test_load_indirect_address_iy_number(self):
        """ Test LD (IY + d), n """

        instruction = LoadIndirectIYN(self._z80)
        byte = self._get_random_byte()
        address = self._get_random_word(upper_limit=0xFFFF - 0xFF)
        offset = self._get_random_byte()
        self._z80.iy.bits = address
        instruction.execute([offset, byte])
        self.assertEqual(
            self._z80.ram.read(address + offset),
            byte
        )

    def test_load_a_indirect_address_bc(self):
        """ Test LD A, (BC) """

        instruction = LoadAIndirectBC(self._z80)
        byte = self._get_random_byte()
        address = self._get_random_word()
        self._z80.ram.write(address, byte)
        self._z80.bc.bits = address
        instruction.execute()
        self.assertEqual(
            self._z80.a.bits,
            byte
        )

    def test_load_a_indirect_address_de(self):
        """ Test LD A, (DE) """

        instruction = LoadAIndirectDE(self._z80)
        byte = self._get_random_byte()
        address = self._get_random_word()
        self._z80.ram.write(address, byte)
        self._z80.de.bits = address
        instruction.execute()
        self.assertEqual(
            self._z80.a.bits,
            byte
        )

    def test_load_a_indirect_address_nn(self):
        """ Test LD A, (nn) """

        instruction = LoadAIndirectNN(self._z80)
        address = self._get_random_word()
        high_order_byte, low_order_byte = self._split_word(address)
        instruction.execute([high_order_byte, low_order_byte])
        self.assertEqual(
            self._z80.a.bits,
            self._z80.ram.read(address)
        )

    def test_load_indirect_bc_register_a(self):
        """ Test LD (BC), A """

        instruction = LoadIndirectBCA(self._z80)
        byte = self._get_random_byte()
        address = self._get_random_word()
        self._z80.a.bits = byte
        self._z80.bc.bits = address
        instruction.execute()
        self.assertEqual(
            self._z80.ram.read(address),
            self._z80.a.bits
        )

    def test_load_indirect_de_register_a(self):
        """ Test LD (DE), A """

        instruction = LoadIndirectDEA(self._z80)
        byte = self._get_random_byte()
        address = self._get_random_word()
        self._z80.a.bits = byte
        self._z80.de.bits = address
        instruction.execute()
        self.assertEqual(
            self._z80.ram.read(address),
            self._z80.a.bits
        )

    def test_load_indirect_nn_register_a(self):
        """ Test LD (nn), A """

        instruction = LoadIndirectNNA(self._z80)
        address = self._get_random_word()
        high_order_byte, low_order_byte = self._split_word(address)
        instruction.execute([high_order_byte, low_order_byte])
        self.assertEqual(
            self._z80.ram.read(address),
            self._z80.a.bits
        )

    def test_load_register_a_register_i(self):
        """ Test LD A, I """

        instruction = LoadAI(self._z80)
        byte = self._get_random_byte()
        self._z80.i.bits = byte
        instruction.execute()
        self.assertEqual(
            self._z80.a.bits,
            self._z80.i.bits
        )

    def test_load_register_a_register_r(self):
        """ Test LD A, R """

        instruction = LoadAR(self._z80)
        byte = self._get_random_byte()
        self._z80.r.bits = byte
        instruction.execute()
        self.assertEqual(
            self._z80.a.bits,
            self._z80.r.bits
        )

    def test_load_register_i_register_a(self):
        """ Test LD I, A """

        instruction = LoadIA(self._z80)
        byte = self._get_random_byte()
        self._z80.a.bits = byte
        instruction.execute()
        self.assertEqual(
            self._z80.i.bits,
            self._z80.a.bits
        )

    def test_load_register_r_register_a(self):
        """ Test LD R, A """

        instruction = LoadRA(self._z80)
        byte = self._get_random_byte()
        self._z80.a.bits = byte
        instruction.execute()
        self.assertEqual(
            self._z80.r.bits,
            self._z80.a.bits
        )
