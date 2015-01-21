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
    def __init__(self, *args, **kwargs):
        super(TestLoadInstructions, self).__init__(*args, **kwargs)

    def test_load_register_register_rr(self):
        """ Test LD r, r' """

        registers = {
            '000': self._z80.b,
            '001': self._z80.c,
            '010': self._z80.d,
            '011': self._z80.e,
            '100': self._z80.h,
            '101': self._z80.l,
            '111': self._z80.a,
        }

        for (destination, source) in product(registers.keys(), registers.keys()):
            self._load_z80_registers([registers[destination], registers[source]])
            opcode = ['01{0}{1}'.format(destination, source)]
            self._decode_and_execute_opcode(opcode)
            self.assertEqual(registers[destination].bits, registers[source].bits)

    def test_load_register_register_pp(self):
        """ Test LD p, p' """

        registers = {
            '000': self._z80.b,
            '001': self._z80.c,
            '010': self._z80.d,
            '011': self._z80.e,
            '100': self._z80.ixh,
            '101': self._z80.ixl,
            '111': self._z80.a,
        }

        for (destination, source) in product(registers.keys(), registers.keys()):
            self._load_z80_registers([registers[destination], registers[source]])
            opcode = ['11011101', '01{0}{1}'.format(destination, source)]
            self._decode_and_execute_opcode(opcode)
            self.assertEqual(registers[destination].bits, registers[source].bits)

    def test_load_register_register_qq(self):
        """ Test LD q, q' """

        registers = {
            '000': self._z80.b,
            '001': self._z80.c,
            '010': self._z80.d,
            '011': self._z80.e,
            '100': self._z80.iyh,
            '101': self._z80.iyl,
            '111': self._z80.a,
        }

        for (destination, source) in product(registers.keys(), registers.keys()):
            self._load_z80_registers([registers[destination], registers[source]])
            opcode = ['11111101', '01{0}{1}'.format(destination, source)]
            self._decode_and_execute_opcode(opcode)
            self.assertEqual(registers[destination].bits, registers[source].bits)

    def test_load_register_r_number(self):
        """ Test LD r, n """

        registers = {
            '000': self._z80.b,
            '001': self._z80.c,
            '010': self._z80.d,
            '011': self._z80.e,
            '100': self._z80.h,
            '101': self._z80.l,
            '111': self._z80.a,
        }

        for destination in registers.keys():
            n = self._int_to_bin(self._get_random_byte())
            opcode = ['00{0}110'.format(destination), '{0}'.format(n)]
            self._decode_and_execute_opcode(opcode)
            self.assertEqual(registers[destination].bits, int(n, base=2))

    def test_load_register_p_number(self):
        """ Test LD p, n """

        registers = {
            '000': self._z80.b,
            '001': self._z80.c,
            '010': self._z80.d,
            '011': self._z80.e,
            '100': self._z80.ixh,
            '101': self._z80.ixl,
            '111': self._z80.a,
        }

        for destination in registers.keys():
            n = self._int_to_bin(self._get_random_byte())
            opcode = ['11011101', '00{0}110'.format(destination), '{0}'.format(n)]
            self._decode_and_execute_opcode(opcode)
            self.assertEqual(registers[destination].bits, int(n, base=2))

    def test_load_register_q_number(self):
        """ Test LD q, n """

        registers = {
            '000': self._z80.b,
            '001': self._z80.c,
            '010': self._z80.d,
            '011': self._z80.e,
            '100': self._z80.iyh,
            '101': self._z80.iyl,
            '111': self._z80.a,
        }

        for destination in registers.keys():
            n = self._int_to_bin(self._get_random_byte())
            opcode = ['11111101', '00{0}110'.format(destination), '{0}'.format(n)]
            self._decode_and_execute_opcode(opcode)
            self.assertEqual(registers[destination].bits, int(n, base=2))

    def test_load_register_indirect_hl(self):
        """ Test LD r, (HL) """

        registers = {
            '000': self._z80.b,
            '001': self._z80.c,
            '010': self._z80.d,
            '011': self._z80.e,
            '100': self._z80.h,
            '101': self._z80.l,
            '111': self._z80.a,
        }

        for destination in registers.keys():
            n = self._get_random_byte()
            address = self._get_random_word()
            self._z80.ram.write(address, n)
            self._z80.hl.bits = address
            opcode = ['01{0}110'.format(destination)]
            self._decode_and_execute_opcode(opcode)
            self.assertEqual(registers[destination].bits, n)

    def test_load_register_indirect_ix(self):
        """ Test LD r, (IX + d) """

        registers = {
            '000': self._z80.b,
            '001': self._z80.c,
            '010': self._z80.d,
            '011': self._z80.e,
            '100': self._z80.h,
            '101': self._z80.l,
            '111': self._z80.a,
        }

        for destination in registers.keys():
            n = self._get_random_byte()
            address = self._get_random_word(upper_limit=0xFFFF - 0xFF)
            offset = self._get_random_byte()
            self._z80.ram.write(address + offset, n)
            self._z80.ix.bits = address
            opcode = ['11011101', '01{0}110'.format(destination), \
                self._int_to_bin(offset)]
            self._decode_and_execute_opcode(opcode)
            self.assertEqual(registers[destination].bits, n)

    def test_load_register_indirect_iy(self):
        """ Test LD r, (IY + d) """

        registers = {
            '000': self._z80.b,
            '001': self._z80.c,
            '010': self._z80.d,
            '011': self._z80.e,
            '100': self._z80.h,
            '101': self._z80.l,
            '111': self._z80.a,
        }

        for destination in registers.keys():
            n = self._get_random_byte()
            address = self._get_random_word(upper_limit=0xFFFF - 0xFF)
            offset = self._get_random_byte()
            self._z80.ram.write(address + offset, n)
            self._z80.iy.bits = address
            opcode = ['11111101', '01{0}110'.format(destination), \
                self._int_to_bin(offset)]
            self._decode_and_execute_opcode(opcode)
            self.assertEqual(registers[destination].bits, n)


    def test_load_indirect_address_hl_register(self):
        """ Test LD (HL), r """

        registers = {
            '000': self._z80.b,
            '001': self._z80.c,
            '010': self._z80.d,
            '011': self._z80.e,
            '100': self._z80.h,
            '101': self._z80.l,
            '111': self._z80.a,
        }

        for source in registers.keys():
            address = self._get_random_word()
            registers[source].bits = self._get_random_byte()
            self._z80.hl.bits = address
            opcode = ['01110{0}'.format(source)]
            self._decode_and_execute_opcode(opcode)
            self.assertEqual(registers[source].bits, self._z80.ram.read(address))

    def test_load_indirect_address_ix_register(self):
        """ Test LD (IX + d), r """

        registers = {
            '000': self._z80.b,
            '001': self._z80.c,
            '010': self._z80.d,
            '011': self._z80.e,
            '100': self._z80.h,
            '101': self._z80.l,
            '111': self._z80.a,
        }

        for source in registers.keys():
            address = self._get_random_word(upper_limit=0xFFFF - 0xFF)
            offset = self._get_random_byte()
            registers[source].bits = self._get_random_byte()
            self._z80.ix.bits = address
            opcode = ['11011101', '01110{0}'.format(source), \
                self._int_to_bin(offset)]
            self._decode_and_execute_opcode(opcode)
            self.assertEqual(
                registers[source].bits,
                self._z80.ram.read(address + offset)
            )

    def test_load_indirect_address_iy_register(self):
        """ Test LD (IY + d), r """

        registers = {
            '000': self._z80.b,
            '001': self._z80.c,
            '010': self._z80.d,
            '011': self._z80.e,
            '100': self._z80.h,
            '101': self._z80.l,
            '111': self._z80.a,
        }

        for source in registers.keys():
            address = self._get_random_word(upper_limit=0xFFFF - 0xFF)
            offset = self._get_random_byte()
            registers[source].bits = self._get_random_byte()
            self._z80.iy.bits = address
            opcode = ['11111101', '01110{0}'.format(source), \
                self._int_to_bin(offset)]
            self._decode_and_execute_opcode(opcode)
            self.assertEqual(
                registers[source].bits,
                self._z80.ram.read(address + offset)
            )

    def test_load_indirect_address_hl_number(self):
        """ Test LD (HL), n """

        n = self._get_random_byte()
        address = self._get_random_word()
        self._z80.hl.bits = address
        opcode = ['00110110', self._int_to_bin(n)]
        self._decode_and_execute_opcode(opcode)
        self.assertEqual(self._z80.ram.read(address), n)

    def test_load_indirect_address_ix_number(self):
        """ Test LD (IX + d), n """

        n = self._get_random_byte()
        address = self._get_random_word(upper_limit=0xFFFF - 0xFF)
        offset = self._get_random_byte()
        self._z80.ix.bits = address
        opcode = ['11011101', '00110110', \
            self._int_to_bin(offset), self._int_to_bin(n)]
        self._decode_and_execute_opcode(opcode)
        self.assertEqual(self._z80.ram.read(address + offset), n)

    def test_load_indirect_address_iy_number(self):
        """ Test LD (IY + d), n """

        n = self._get_random_byte()
        address = self._get_random_word(upper_limit=0xFFFF - 0xFF)
        offset = self._get_random_byte()
        self._z80.iy.bits = address
        opcode = ['11111101', '00110110', \
            self._int_to_bin(offset), self._int_to_bin(n)]
        self._decode_and_execute_opcode(opcode)
        self.assertEqual(self._z80.ram.read(address + offset), n)

    def test_load_a_indirect_address_bc(self):
        """ Test LD A, (BC) """

        n = self._get_random_byte()
        address = self._get_random_word()
        self._z80.ram.write(address, n)
        self._z80.bc.bits = address
        opcode = ['00001010']
        self._decode_and_execute_opcode(opcode)
        self.assertEqual(self._z80.a.bits, n)
 
    def test_load_a_indirect_address_de(self):
        """ Test LD A, (DE) """

        n = self._get_random_byte()
        address = self._get_random_word()
        self._z80.ram.write(address, n)
        self._z80.de.bits = address
        opcode = ['00011010']
        self._decode_and_execute_opcode(opcode)
        self.assertEqual(self._z80.a.bits, n)

    def test_load_a_indirect_address_nn(self):
        """ Test LD A, (nn) """

        m = self._get_random_byte()
        n = self._get_random_byte()
        address = int(self._int_to_bin(m) + self._int_to_bin(n), base=2)
        opcode = ['00111010', self._int_to_bin(m), self._int_to_bin(n)]
        self._decode_and_execute_opcode(opcode)
        self.assertEqual(self._z80.a.bits, self._z80.ram.read(address))

    def test_load_indirect_bc_register_a(self):
        """ Test LD (BC), A """

        n = self._get_random_byte()
        address = self._get_random_word()
        self._z80.a.bits = n
        self._z80.bc.bits = address
        opcode = ['00000010']
        self._decode_and_execute_opcode(opcode)
        self.assertEqual(self._z80.ram.read(address), self._z80.a.bits)

    def test_load_indirect_de_register_a(self):
        """ Test LD (DE), A """

        n = self._get_random_byte()
        address = self._get_random_word()
        self._z80.a.bits = n
        self._z80.de.bits = address
        opcode = ['00010010']
        self._decode_and_execute_opcode(opcode)
        self.assertEqual(self._z80.ram.read(address), self._z80.a.bits)

    def test_load_indirect_nn_register_a(self):
        """ Test LD (nn), A """

        m = self._get_random_byte()
        n = self._get_random_byte()
        address = int(self._int_to_bin(m) + self._int_to_bin(n), base=2)
        opcode = ['00110010', self._int_to_bin(m), self._int_to_bin(n)]
        self._decode_and_execute_opcode(opcode)
        self.assertEqual(self._z80.ram.read(address), self._z80.a.bits)

    def test_load_register_a_register_i(self):
        """ Test LD A, I """

        n = self._get_random_byte()
        self._z80.i.bits = n
        opcode = ['11101101', '01010111']
        self._decode_and_execute_opcode(opcode)
        self.assertEqual(self._z80.a.bits, self._z80.i.bits)

    def test_load_register_a_register_r(self):
        """ Test LD A, R """

        n = self._get_random_byte()
        self._z80.r.bits = n
        opcode = ['11101101', '01011111']
        self._decode_and_execute_opcode(opcode)
        self.assertEqual(self._z80.a.bits, self._z80.r.bits)

    def test_load_register_i_register_a(self):
        """ Test LD I, A """

        n = self._get_random_byte()
        self._z80.a.bits = n
        opcode = ['11101101', '01000111']
        self._decode_and_execute_opcode(opcode)
        self.assertEqual(self._z80.i.bits, self._z80.a.bits)

    def test_load_register_r_register_a(self):
        """ Test LD R, A """

        n = self._get_random_byte()
        self._z80.a.bits = n
        opcode = ['11101101', '01001111']
        self._decode_and_execute_opcode(opcode)
        self.assertEqual(self._z80.r.bits, self._z80.a.bits)
