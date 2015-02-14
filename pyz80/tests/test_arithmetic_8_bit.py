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

from ..instruction.arithmetic_8_bit import *
from .test_z80_base import TestZ80


class TestArithmetic8Bit(TestZ80):

    def _default_registers(self):
        return {
            0b000: self._z80.b,
            0b001: self._z80.c,
            0b010: self._z80.d,
            0b011: self._z80.e,
            0b111: self._z80.a,
        }

    def _r_registers(self):
        return {
            0b100: self._z80.h,
            0b101: self._z80.l,
        }

    def _p_registers(self):
        return {
            0b100: self._z80.ixh,
            0b101: self._z80.ixl,
        }

    def _q_registers(self):
        return {
            0b100: self._z80.iyh,
            0b101: self._z80.iyl,
        }

    """ ADD tests. """

    def _add_a_x(self, instruction, selector, register):
        self._z80.a.bits = self._get_random_byte()
        register.bits = self._get_random_byte()
        instruction_result = (self._z80.a.bits + register.bits) & 0xFF
        instruction.execute([selector])
        self.assertEqual(
            self._z80.a.bits,
            instruction_result,
            msg='A = {:02X}, {:} = {:02X}'.format(self._z80.a.bits, register.label, register.bits)
        )

    def test_add_a_r(self):
        """ Test ADD A, r """

        instruction = AddAR(self._z80)
        registers = dict(self._default_registers(), **self._r_registers())

        for selector, register in registers.iteritems():
            self._add_a_x(instruction, selector, register)


    def test_add_a_p(self):
        """ Test ADD A, p """

        instruction = AddAP(self._z80)
        registers = dict(self._default_registers(), **self._p_registers())

        for selector, register in registers.iteritems():
            self._add_a_x(instruction, selector, register)

    def test_add_a_q(self):
        """ Test ADD A, q """

        instruction = AddAQ(self._z80)
        registers = dict(self._default_registers(), **self._q_registers())

        for selector, register in registers.iteritems():
            self._add_a_x(instruction, selector, register)

    def test_add_a_n(self):
        """ Test ADD A, n """

        instruction = AddAN(self._z80)
        self._z80.a.bits = self._get_random_byte()
        n = self._get_random_byte()
        instruction_result = (self._z80.a.bits + n) & 0xFF
        instruction.execute([n])
        self.assertEqual(
            self._z80.a.bits,
            instruction_result,
            msg='A = {:02X}, N = {:02X}'.format(self._z80.a.bits, n)
        )

    def test_add_a_indirect_hl(self):
        """ Test ADD A, (HL) """

        instruction = AddAIndirectHL(self._z80)
        address = self._get_random_word(upper_limit=0xFFFF - 0xFF)
        n = self._get_random_byte()
        self._z80.ram.write(address, n)
        self._z80.hl.bits = address
        self._z80.a.bits = self._get_random_byte()
        instruction_result = (self._z80.a.bits + n) & 0xFF
        instruction.execute()
        self.assertEqual(
            self._z80.a.bits,
            instruction_result,
            msg='A = {:02X}, (HL) = {:02X}'.format(self._z80.a.bits, n)
        )

    def test_add_a_indirect_ix(self):
        """ Test ADD A, (IX + d) """

        instruction = AddAIndirectIX(self._z80)
        address = self._get_random_word(upper_limit=0xFFFF - 0xFF)
        offset = self._get_random_byte()
        n = self._get_random_byte()
        self._z80.ram.write(address + offset, n)
        self._z80.ix.bits = address
        self._z80.a.bits = self._get_random_byte()
        instruction_result = (self._z80.a.bits + n) & 0xFF
        instruction.execute([offset])
        self.assertEqual(
            self._z80.a.bits,
            instruction_result,
            msg='A = {:02X}, (IX + d) = {:02X}'.format(self._z80.a.bits, n)
        )

    def test_add_a_indirect_iy(self):
        """ Test ADD A, (IY + d) """

        instruction = AddAIndirectIY(self._z80)
        address = self._get_random_word(upper_limit=0xFFFF - 0xFF)
        offset = self._get_random_byte()
        n = self._get_random_byte()
        self._z80.ram.write(address + offset, n)
        self._z80.iy.bits = address
        self._z80.a.bits = self._get_random_byte()
        instruction_result = (self._z80.a.bits + n) & 0xFF
        instruction.execute([offset])
        self.assertEqual(
            self._z80.a.bits,
            instruction_result,
            msg='A = {:02X}, (IY + d) = {:02X}'.format(self._z80.a.bits, n)
        )

    """ ADC tests. """

    def _adc_a_x(self, instruction, selector, register, error_message):
        self._z80.a.bits = self._get_random_byte()
        register.bits = self._get_random_byte()
        instruction_result = (self._z80.a.bits + register.bits + self._z80.f.carry_flag) & 0xFF
        instruction.execute([selector])
        self.assertEqual(self._z80.a.bits, instruction_result, msg=error_message)

    def _test_adc_a_r(self, error_message):
        instruction = AdcAR(self._z80)
        registers = dict(self._default_registers(), **self._r_registers())

        for selector, register in registers.iteritems():
            self._adc_a_x(instruction, selector, register, error_message)

    def test_adc_a_r_carry_set(self):
        """ Test ADC A, r (carry set) """

        self._z80.f.set_carry_flag()
        self._test_adc_a_r('A = {:02X}, {:} = {:02X}. Carry is set')

    def test_adc_a_r_carry_reset(self):
        """ Test ADC A, r (carry reset) """

        self._z80.f.reset_carry_flag()
        self._test_adc_a_r('A = {:02X}, {:} = {:02X}. Carry is reset')

    def _test_adc_a_p(self, error_message):
        instruction = AdcAP(self._z80)
        registers = dict(self._default_registers(), **self._p_registers())

        for selector, register in registers.iteritems():
            self._adc_a_x(instruction, selector, register, error_message)

    def test_adc_a_p_carry_set(self):
        """ Test ADC A, p (carry set) """

        self._z80.f.set_carry_flag()
        self._test_adc_a_p('A = {:02X}, {:} = {:02X}. Carry is set')

    def test_adc_a_p_carry_reset(self):
        """ Test ADC A, p (carry reset) """

        self._z80.f.reset_carry_flag()
        self._test_adc_a_p('A = {:02X}, {:} = {:02X}. Carry is reset')

    def _test_adc_a_q(self, error_message):
        instruction = AdcAQ(self._z80)
        registers = dict(self._default_registers(), **self._q_registers())

        for selector, register in registers.iteritems():
            self._adc_a_x(instruction, selector, register, error_message)

    def test_adc_a_q_carry_set(self):
        """ Test ADC A, q (carry set) """

        self._z80.f.set_carry_flag()
        self._test_adc_a_q('A = {:02X}, {:} = {:02X}. Carry is set')

    def test_adc_a_q_carry_reset(self):
        """ Test ADC A, q (carry reset) """

        self._z80.f.reset_carry_flag()
        self._test_adc_a_q('A = {:02X}, {:} = {:02X}. Carry is reset')

    def _test_adc_n(self, error_message):
        instruction = AdcAN(self._z80)
        self._z80.a.bits = self._get_random_byte()
        n = self._get_random_byte()
        instruction_result = (self._z80.a.bits + n + self._z80.f.carry_flag) & 0xFF
        instruction.execute([n])
        self.assertEqual(self._z80.a.bits, instruction_result, msg=error_message)

    def test_adc_a_n_carry_set(self):
        """ Test ADC A, n (carry set) """

        self._z80.f.set_carry_flag()
        self._test_adc_n('A = {:02X}, N = {:02X}. Carry is set')

    def test_adc_a_n_carry_reset(self):
        """ Test ADC A, n (carry reset) """

        self._z80.f.reset_carry_flag()
        self._test_adc_n('A = {:02X}, {:} = {:02X}. Carry is reset')
