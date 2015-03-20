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

from ..instruction.jump import *
from .test_z80_base import TestZ80


# TODO: A lot of repeated code. Refactor me !
class TestJump(TestZ80):
    """ Tests all jump instructions. """

    def _jp_conditions(self):
        # PO = Parity odd (parity flag is reset).
        # PE = Parity even (parity flag is set).
        # P = Plus (sign flag is reset).
        # M = Minus (sign flag is set).

        return {
            'NZ': 0b000,
            'Z':  0b001,
            'NC': 0b010,
            'C':  0b011,
            'PO': 0b100,
            'PE': 0b101,
            'P':  0b110,
            'M':  0b111
        }

    def test_jp_nn(self):
        """ Test JP nn """

        instruction = JpNN(self._z80)
        address = self._get_random_word()
        high_order_byte, low_order_byte = self._split_word(address)
        instruction.execute([high_order_byte, low_order_byte])
        self.assertEqual(
            self._z80.pc.bits,
            address,
            msg='PC = {:02X}, address = {:02X}'.format(
                self._z80.pc.bits,
                address
            )
        )

    def test_jp_nz_nn_zero_set(self):
        """ Test JP NZ, nn (Z set) """

        self._z80.f.set_zero_flag()
        instruction = JpCCNN(self._z80)
        address = self._get_random_word()
        jp_address = self._get_random_word()
        high_order_byte, low_order_byte = self._split_word(jp_address)
        self._z80.pc.bits = address
        instruction.execute([self._jp_conditions()['NZ'], high_order_byte, low_order_byte])
        self.assertEqual(
            self._z80.pc.bits,
            address,
            msg='PC = {:02X}, address = {:02X}, jp_address = {:02X}'.format(
                self._z80.pc.bits,
                address,
                jp_address
            )
        )

    def test_jp_nz_nn_zero_reset(self):
        """ Test JP NZ, nn (Z reset) """

        instruction = JpCCNN(self._z80)
        address = self._get_random_word()
        jp_address = self._get_random_word()
        high_order_byte, low_order_byte = self._split_word(jp_address)
        self._z80.pc.bits = address
        instruction.execute([self._jp_conditions()['NZ'], high_order_byte, low_order_byte])
        self.assertEqual(
            self._z80.pc.bits,
            jp_address,
            msg='PC = {:02X}, address = {:02X}, jp_address = {:02X}'.format(
                self._z80.pc.bits,
                address,
                jp_address
            )
        )

    def test_jp_z_nn_zero_set(self):
        """ Test JP Z, nn (Z set) """

        self._z80.f.set_zero_flag()
        instruction = JpCCNN(self._z80)
        address = self._get_random_word()
        jp_address = self._get_random_word()
        high_order_byte, low_order_byte = self._split_word(jp_address)
        self._z80.pc.bits = address
        instruction.execute([self._jp_conditions()['Z'], high_order_byte, low_order_byte])
        self.assertEqual(
            self._z80.pc.bits,
            jp_address,
            msg='PC = {:02X}, address = {:02X}, jp_address = {:02X}'.format(
                self._z80.pc.bits,
                address,
                jp_address
            )
        )

    def test_jp_z_nn_zero_reset(self):
        """ Test JP Z, nn (Z reset) """

        instruction = JpCCNN(self._z80)
        address = self._get_random_word()
        jp_address = self._get_random_word()
        high_order_byte, low_order_byte = self._split_word(jp_address)
        self._z80.pc.bits = address
        instruction.execute([self._jp_conditions()['Z'], high_order_byte, low_order_byte])
        self.assertEqual(
            self._z80.pc.bits,
            address,
            msg='PC = {:02X}, address = {:02X}, jp_address = {:02X}'.format(
                self._z80.pc.bits,
                address,
                jp_address
            )
        )

    def test_jp_nc_nn_carry_set(self):
        """ Test JP NC, nn (C set) """

        self._z80.f.set_carry_flag()
        instruction = JpCCNN(self._z80)
        address = self._get_random_word()
        jp_address = self._get_random_word()
        high_order_byte, low_order_byte = self._split_word(jp_address)
        self._z80.pc.bits = address
        instruction.execute([self._jp_conditions()['NC'], high_order_byte, low_order_byte])
        self.assertEqual(
            self._z80.pc.bits,
            address,
            msg='PC = {:02X}, address = {:02X}, jp_address = {:02X}'.format(
                self._z80.pc.bits,
                address,
                jp_address
            )
        )

    def test_jp_nc_nn_carry_reset(self):
        """ Test JP NC, nn (C reset) """

        instruction = JpCCNN(self._z80)
        address = self._get_random_word()
        jp_address = self._get_random_word()
        high_order_byte, low_order_byte = self._split_word(jp_address)
        self._z80.pc.bits = address
        instruction.execute([self._jp_conditions()['NC'], high_order_byte, low_order_byte])
        self.assertEqual(
            self._z80.pc.bits,
            jp_address,
            msg='PC = {:02X}, address = {:02X}, jp_address = {:02X}'.format(
                self._z80.pc.bits,
                address,
                jp_address
            )
        )

    def test_jp_c_nn_carry_set(self):
        """ Test JP C, nn (C set) """

        self._z80.f.set_carry_flag()
        instruction = JpCCNN(self._z80)
        address = self._get_random_word()
        jp_address = self._get_random_word()
        high_order_byte, low_order_byte = self._split_word(jp_address)
        self._z80.pc.bits = address
        instruction.execute([self._jp_conditions()['C'], high_order_byte, low_order_byte])
        self.assertEqual(
            self._z80.pc.bits,
            jp_address,
            msg='PC = {:02X}, address = {:02X}, jp_address = {:02X}'.format(
                self._z80.pc.bits,
                address,
                jp_address
            )
        )

    def test_jp_c_nn_carry_reset(self):
        """ Test JP C, nn (C reset) """

        instruction = JpCCNN(self._z80)
        address = self._get_random_word()
        jp_address = self._get_random_word()
        high_order_byte, low_order_byte = self._split_word(jp_address)
        self._z80.pc.bits = address
        instruction.execute([self._jp_conditions()['C'], high_order_byte, low_order_byte])
        self.assertEqual(
            self._z80.pc.bits,
            address,
            msg='PC = {:02X}, address = {:02X}, jp_address = {:02X}'.format(
                self._z80.pc.bits,
                address,
                jp_address
            )
        )

    def test_jp_po_nn_parity_set(self):
        """ Test JP PO, nn (P set) """

        self._z80.f.set_parity_flag()
        instruction = JpCCNN(self._z80)
        address = self._get_random_word()
        jp_address = self._get_random_word()
        high_order_byte, low_order_byte = self._split_word(jp_address)
        self._z80.pc.bits = address
        instruction.execute([self._jp_conditions()['PO'], high_order_byte, low_order_byte])
        self.assertEqual(
            self._z80.pc.bits,
            address,
            msg='PC = {:02X}, address = {:02X}, jp_address = {:02X}'.format(
                self._z80.pc.bits,
                address,
                jp_address
            )
        )

    def test_jp_po_nn_parity_reset(self):
        """ Test JP PO, nn (P reset) """

        instruction = JpCCNN(self._z80)
        address = self._get_random_word()
        jp_address = self._get_random_word()
        high_order_byte, low_order_byte = self._split_word(jp_address)
        self._z80.pc.bits = address
        instruction.execute([self._jp_conditions()['PO'], high_order_byte, low_order_byte])
        self.assertEqual(
            self._z80.pc.bits,
            jp_address,
            msg='PC = {:02X}, address = {:02X}, jp_address = {:02X}'.format(
                self._z80.pc.bits,
                address,
                jp_address
            )
        )

    def test_jp_pe_nn_parity_set(self):
        """ Test JP PE, nn (P set) """

        self._z80.f.set_parity_flag()
        instruction = JpCCNN(self._z80)
        address = self._get_random_word()
        jp_address = self._get_random_word()
        high_order_byte, low_order_byte = self._split_word(jp_address)
        self._z80.pc.bits = address
        instruction.execute([self._jp_conditions()['PE'], high_order_byte, low_order_byte])
        self.assertEqual(
            self._z80.pc.bits,
            jp_address,
            msg='PC = {:02X}, address = {:02X}, jp_address = {:02X}'.format(
                self._z80.pc.bits,
                address,
                jp_address
            )
        )

    def test_jp_pe_nn_parity_reset(self):
        """ Test JP PE, nn (P reset) """

        instruction = JpCCNN(self._z80)
        address = self._get_random_word()
        jp_address = self._get_random_word()
        high_order_byte, low_order_byte = self._split_word(jp_address)
        self._z80.pc.bits = address
        instruction.execute([self._jp_conditions()['PE'], high_order_byte, low_order_byte])
        self.assertEqual(
            self._z80.pc.bits,
            address,
            msg='PC = {:02X}, address = {:02X}, jp_address = {:02X}'.format(
                self._z80.pc.bits,
                address,
                jp_address
            )
        )

    def test_jp_p_nn_sign_set(self):
        """ Test JP P, nn (S set) """

        self._z80.f.set_sign_flag()
        instruction = JpCCNN(self._z80)
        address = self._get_random_word()
        jp_address = self._get_random_word()
        high_order_byte, low_order_byte = self._split_word(jp_address)
        self._z80.pc.bits = address
        instruction.execute([self._jp_conditions()['P'], high_order_byte, low_order_byte])
        self.assertEqual(
            self._z80.pc.bits,
            address,
            msg='PC = {:02X}, address = {:02X}, jp_address = {:02X}'.format(
                self._z80.pc.bits,
                address,
                jp_address
            )
        )

    def test_jp_p_nn_sign_reset(self):
        """ Test JP P, nn (S reset) """

        instruction = JpCCNN(self._z80)
        address = self._get_random_word()
        jp_address = self._get_random_word()
        high_order_byte, low_order_byte = self._split_word(jp_address)
        self._z80.pc.bits = address
        instruction.execute([self._jp_conditions()['P'], high_order_byte, low_order_byte])
        self.assertEqual(
            self._z80.pc.bits,
            jp_address,
            msg='PC = {:02X}, address = {:02X}, jp_address = {:02X}'.format(
                self._z80.pc.bits,
                address,
                jp_address
            )
        )

    def test_jp_m_nn_sign_set(self):
        """ Test JP M, nn (S set) """

        self._z80.f.set_sign_flag()
        instruction = JpCCNN(self._z80)
        address = self._get_random_word()
        jp_address = self._get_random_word()
        high_order_byte, low_order_byte = self._split_word(jp_address)
        self._z80.pc.bits = address
        instruction.execute([self._jp_conditions()['M'], high_order_byte, low_order_byte])
        self.assertEqual(
            self._z80.pc.bits,
            jp_address,
            msg='PC = {:02X}, address = {:02X}, jp_address = {:02X}'.format(
                self._z80.pc.bits,
                address,
                jp_address
            )
        )

    def test_jp_m_nn_sign_reset(self):
        """ Test JP M, nn (S reset) """

        instruction = JpCCNN(self._z80)
        address = self._get_random_word()
        jp_address = self._get_random_word()
        high_order_byte, low_order_byte = self._split_word(jp_address)
        self._z80.pc.bits = address
        instruction.execute([self._jp_conditions()['M'], high_order_byte, low_order_byte])
        self.assertEqual(
            self._z80.pc.bits,
            address,
            msg='PC = {:02X}, address = {:02X}, jp_address = {:02X}'.format(
                self._z80.pc.bits,
                address,
                jp_address
            )
        )

    def test_jp_e(self):
        """ Test JR e """

        instruction = JrE(self._z80)
        address = self._get_random_word(upper_limit=0xFFFF - 0xFF)
        self._z80.pc.bits = address
        offset = self._get_random_byte()
        instruction.execute([offset])
        self.assertEqual(
            self._z80.pc.bits,
            address + offset,
            msg='PC = {:02X}, address = {:02X}, offset = {:02X}'.format(
                self._z80.pc.bits,
                address,
                offset
            )
        )

    def test_jp_c_e_carry_set(self):
        """ Test JP C, e (C set) """

        self._z80.f.set_carry_flag()
        instruction = JrSSE(self._z80)
        address = self._get_random_word(upper_limit=0xFFFF - 0xFF)
        offset = self._get_random_byte()
        self._z80.pc.bits = address
        instruction.execute([self._jp_conditions()['C'], offset])
        self.assertEqual(
            self._z80.pc.bits,
            address + offset,
            msg='PC = {:02X}, address = {:02X}, offset = {:02X}'.format(
                self._z80.pc.bits,
                address,
                offset
            )
        )

    def test_jp_nc_e_carry_set(self):
        """ Test JP NC, e (C set) """

        self._z80.f.set_carry_flag()
        instruction = JrSSE(self._z80)
        address = self._get_random_word(upper_limit=0xFFFF - 0xFF)
        offset = self._get_random_byte()
        self._z80.pc.bits = address
        instruction.execute([self._jp_conditions()['NC'], offset])
        self.assertEqual(
            self._z80.pc.bits,
            address,
            msg='PC = {:02X}, address = {:02X}, offset = {:02X}'.format(
                self._z80.pc.bits,
                address,
                offset
            )
        )

    def test_jp_c_e_carry_reset(self):
        """ Test JP C, e (C reset) """

        instruction = JrSSE(self._z80)
        address = self._get_random_word(upper_limit=0xFFFF - 0xFF)
        offset = self._get_random_byte()
        self._z80.pc.bits = address
        instruction.execute([self._jp_conditions()['C'], offset])
        self.assertEqual(
            self._z80.pc.bits,
            address,
            msg='PC = {:02X}, address = {:02X}, offset = {:02X}'.format(
                self._z80.pc.bits,
                address,
                offset
            )
        )

    def test_jp_nc_e_carry_reset(self):
        """ Test JP NC, e (C reset) """

        instruction = JrSSE(self._z80)
        address = self._get_random_word(upper_limit=0xFFFF - 0xFF)
        offset = self._get_random_byte()
        self._z80.pc.bits = address
        instruction.execute([self._jp_conditions()['NC'], offset])
        self.assertEqual(
            self._z80.pc.bits,
            address + offset,
            msg='PC = {:02X}, address = {:02X}, offset = {:02X}'.format(
                self._z80.pc.bits,
                address,
                offset
            )
        )

    def test_jp_z_e_zero_set(self):
        """ Test JP Z, e (Z set) """

        self._z80.f.set_zero_flag()
        instruction = JrSSE(self._z80)
        address = self._get_random_word(upper_limit=0xFFFF - 0xFF)
        offset = self._get_random_byte()
        self._z80.pc.bits = address
        instruction.execute([self._jp_conditions()['Z'], offset])
        self.assertEqual(
            self._z80.pc.bits,
            address + offset,
            msg='PC = {:02X}, address = {:02X}, offset = {:02X}'.format(
                self._z80.pc.bits,
                address,
                offset
            )
        )

    def test_jp_nz_e_zero_set(self):
        """ Test JP NZ, e (Z set) """

        self._z80.f.set_zero_flag()
        instruction = JrSSE(self._z80)
        address = self._get_random_word(upper_limit=0xFFFF - 0xFF)
        offset = self._get_random_byte()
        self._z80.pc.bits = address
        instruction.execute([self._jp_conditions()['NZ'], offset])
        self.assertEqual(
            self._z80.pc.bits,
            address,
            msg='PC = {:02X}, address = {:02X}, offset = {:02X}'.format(
                self._z80.pc.bits,
                address,
                offset
            )
        )

    def test_jp_z_e_zero_reset(self):
        """ Test JP Z, e (Z reset) """

        instruction = JrSSE(self._z80)
        address = self._get_random_word(upper_limit=0xFFFF - 0xFF)
        offset = self._get_random_byte()
        self._z80.pc.bits = address
        instruction.execute([self._jp_conditions()['Z'], offset])
        self.assertEqual(
            self._z80.pc.bits,
            address,
            msg='PC = {:02X}, address = {:02X}, offset = {:02X}'.format(
                self._z80.pc.bits,
                address,
                offset
            )
        )

    def test_jp_nz_e_zero_reset(self):
        """ Test JP NZ, e (Z reset) """

        instruction = JrSSE(self._z80)
        address = self._get_random_word(upper_limit=0xFFFF - 0xFF)
        offset = self._get_random_byte()
        self._z80.pc.bits = address
        instruction.execute([self._jp_conditions()['NZ'], offset])
        self.assertEqual(
            self._z80.pc.bits,
            address + offset,
            msg='PC = {:02X}, address = {:02X}, offset = {:02X}'.format(
                self._z80.pc.bits,
                address,
                offset
            )
        )

    def test_jp_indirect_hl(self):
        """ Test JP (HL) """

        instruction = JpIndirectHL(self._z80)
        address = self._get_random_word()
        jp_address = self._get_random_byte()
        self._z80.ram.write(address, jp_address)
        self._z80.hl.bits = address
        instruction.execute()
        self.assertEqual(
            self._z80.pc.bits,
            jp_address,
            msg='PC = {:02X}, address = {:02X}, jp_address = {:02X}'.format(
                self._z80.pc.bits,
                address,
                jp_address
            )
        )

    def test_jp_indirect_ix(self):
        """ Test JP (IX) """

        instruction = JpIndirectIX(self._z80)
        address = self._get_random_word()
        jp_address = self._get_random_byte()
        self._z80.ram.write(address, jp_address)
        self._z80.ix.bits = address
        instruction.execute()
        self.assertEqual(
            self._z80.pc.bits,
            jp_address,
            msg='PC = {:02X}, address = {:02X}, jp_address = {:02X}'.format(
                self._z80.pc.bits,
                address,
                jp_address
            )
        )

    def test_jp_indirect_iy(self):
        """ Test JP (IY) """

        instruction = JpIndirectIY(self._z80)
        address = self._get_random_word()
        jp_address = self._get_random_byte()
        self._z80.ram.write(address, jp_address)
        self._z80.iy.bits = address
        instruction.execute()
        self.assertEqual(
            self._z80.pc.bits,
            jp_address,
            msg='PC = {:02X}, address = {:02X}, jp_address = {:02X}'.format(
                self._z80.pc.bits,
                address,
                jp_address
            )
        )

    def test_djnz_b_non_zero(self):
        """ Test DJNZ e (B != 0) """

        instruction = DjnzE(self._z80)
        address = self._get_random_word(upper_limit=0xFFFF - 0xFF)
        offset = self._get_random_byte()
        b_bits = self._get_random_byte(upper_limit=0xFF - 1) + 1
        self._z80.pc.bits = address
        self._z80.b.bits = b_bits
        instruction.execute([offset])
        self.assertEqual(
            self._z80.pc.bits,
            address + offset,
            msg='PC = {:02X}, address = {:02X}, offset = {:02X}, B = {:02X}, b_bits = {:02X}'.format(
                self._z80.pc.bits,
                address,
                offset,
                self._z80.b.bits,
                b_bits
            )
        )
        self.assertEqual(
            self._z80.b.bits,
            b_bits - 1,
            msg='PC = {:02X}, address = {:02X}, offset = {:02X}, B = {:02X}, b_bits = {:02X}'.format(
                self._z80.pc.bits,
                address,
                offset,
                self._z80.b.bits,
                b_bits
            )
        )

    def test_djnz_b_zero(self):
        """ Test DJNZ e (B = 1) """

        instruction = DjnzE(self._z80)
        address = self._get_random_word(upper_limit=0xFFFF - 0xFF)
        offset = self._get_random_byte()
        self._z80.pc.bits = address
        self._z80.b.bits = 1
        instruction.execute([offset])
        self.assertEqual(
            self._z80.pc.bits,
            address,
            msg='PC = {:02X}, address = {:02X}, offset = {:02X}, B = {:02X}'.format(
                self._z80.pc.bits,
                address,
                offset,
                self._z80.b.bits
            )
        )
        self.assertEqual(
            self._z80.b.bits,
            0x00,
            msg='PC = {:02X}, address = {:02X}, offset = {:02X}, B = {:02X}'.format(
                self._z80.pc.bits,
                address,
                offset,
                self._z80.b.bits
            )
        )
