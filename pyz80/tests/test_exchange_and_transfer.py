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

from ..instruction.exchange_and_transfer import *
from .test_z80_base import TestZ80


class TestExchangeAndTransfer(TestZ80):

    def test_ex(self):
        """ Test EX DE, HL """

        instruction = Ex(self._z80)
        de_bits = self._get_random_word()
        hl_bits = self._get_random_word()
        self._z80.de.bits = de_bits
        self._z80.hl.bits = hl_bits
        instruction.execute()
        self.assertEqual(
            self._z80.de.bits,
            hl_bits,
            msg='DE = {:02X}, HL bits = {:02X}'.format(self._z80.de.bits, hl_bits)
        )
        self.assertEqual(
            self._z80.hl.bits,
            de_bits,
            msg='HL = {:02X}, DE bits = {:02X}'.format(self._z80.hl.bits, de_bits)
        )

    def test_ex_af_af_(self):
        """ Test EX AF, AF' """

        instruction = ExAFAF_(self._z80)
        a_bits = self._get_random_byte()
        f_bits = self._get_random_byte()
        a__bits = self._get_random_byte()
        f__bits = self._get_random_byte()
        self._z80.a.bits = a_bits
        self._z80.f.bits = f_bits
        self._z80.a_.bits = a__bits
        self._z80.f_.bits = f__bits
        instruction.execute()
        self.assertEqual(
            self._z80.a.bits,
            a__bits,
            msg='A = {:02X}, A\' bits = {:02X} '.format(self._z80.a.bits, a__bits)
        )
        self.assertEqual(
            self._z80.f.bits,
            f__bits,
            msg='F = {:02X}, F\' bits = {:02X} '.format(self._z80.f.bits, f__bits)
        )
        self.assertEqual(
            self._z80.a_.bits,
            a_bits,
            msg='A\' = {:02X}, A bits = {:02X} '.format(self._z80.a_.bits, a_bits)
        )
        self.assertEqual(
            self._z80.f_.bits,
            f_bits,
            msg='F\' = {:02X}, F bits = {:02X} '.format(self._z80.f_.bits, f_bits)
        )

    def test_exx(self):
        """ Test EXX """

        instruction = Exx(self._z80)
        bc_bits = self._get_random_word()
        de_bits = self._get_random_word()
        hl_bits = self._get_random_word()
        bc__bits = self._get_random_word()
        de__bits = self._get_random_word()
        hl__bits = self._get_random_word()
        self._z80.bc.bits = bc_bits
        self._z80.de.bits = de_bits
        self._z80.hl.bits = hl_bits
        self._z80.bc_.bits = bc__bits
        self._z80.de_.bits = de__bits
        self._z80.hl_.bits = hl__bits
        instruction.execute()
        self.assertEqual(
            self._z80.bc.bits,
            bc__bits,
            msg='BC = {:02X}, BC\' bits = {:02X}'.format(self._z80.bc.bits, bc__bits)
        )
        self.assertEqual(
            self._z80.de.bits,
            de__bits,
            msg='DE = {:02X}, DE\' bits = {:02X}'.format(self._z80.de.bits, de__bits)
        )
        self.assertEqual(
            self._z80.hl.bits,
            hl__bits,
            msg='HL = {:02X}, HL\' bits = {:02X}'.format(self._z80.hl.bits, hl__bits)
        )

        self.assertEqual(
            self._z80.bc_.bits,
            bc_bits,
            msg='BC\' = {:02X}, BC bits = {:02X}'.format(self._z80.bc_.bits, bc_bits)
        )
        self.assertEqual(
            self._z80.de_.bits,
            de_bits,
            msg='DE\' = {:02X}, DE bits = {:02X}'.format(self._z80.de_.bits, de_bits)
        )
        self.assertEqual(
            self._z80.hl_.bits,
            hl_bits,
            msg='HL\' = {:02X}, HL bits = {:02X}'.format(self._z80.hl_.bits, hl_bits)
        )

    def test_ex_indirect_sp_hl(self):
        """ Test EX (SP), HL """

        instruction = ExIndirectSPHL(self._z80)
        sp_bits = self._get_random_word()
        hl_bits = self._get_random_word()
        word = self._get_random_word()
        self._load_ram_with_word(sp_bits, word)
        self._z80.sp.bits = sp_bits
        self._z80.hl.bits = hl_bits
        instruction.execute()
        some_value = self._read_ram_word(sp_bits)
        self.assertEqual(
            self._read_ram_word(sp_bits),
            hl_bits,
            msg='Ram word = {:02X}, HL bits = {:02X}'.format(self._read_ram_word(sp_bits), hl_bits)
        )
        self.assertEqual(
            self._z80.hl.bits,
            word,
            msg='HL = {:02X}, Word bits = {:02X}'.format(self._z80.hl.bits, word)
        )

    def test_ex_indirect_sp_ix(self):
        """ Test EX (SP), IX """

        instruction = ExIndirectSPIX(self._z80)
        sp_bits = self._get_random_word()
        ix_bits = self._get_random_word()
        word = self._get_random_word()
        self._load_ram_with_word(sp_bits, word)
        self._z80.sp.bits = sp_bits
        self._z80.ix.bits = ix_bits
        instruction.execute()
        some_value = self._read_ram_word(sp_bits)
        self.assertEqual(
            self._read_ram_word(sp_bits),
            ix_bits,
            msg='Ram word = {:02X}, IX bits = {:02X}'.format(self._read_ram_word(sp_bits), ix_bits)
        )
        self.assertEqual(
            self._z80.ix.bits,
            word,
            msg='IX = {:02X}, Word bits = {:02X}'.format(self._z80.ix.bits, word)
        )

    def test_ex_indirect_sp_iy(self):
        """ Test EX (SP), IY """

        instruction = ExIndirectSPIY(self._z80)
        sp_bits = self._get_random_word()
        iy_bits = self._get_random_word()
        word = self._get_random_word()
        self._load_ram_with_word(sp_bits, word)
        self._z80.sp.bits = sp_bits
        self._z80.iy.bits = iy_bits
        instruction.execute()
        some_value = self._read_ram_word(sp_bits)
        self.assertEqual(
            self._read_ram_word(sp_bits),
            iy_bits,
            msg='Ram word = {:02X}, IX bits = {:02X}'.format(self._read_ram_word(sp_bits), iy_bits)
        )
        self.assertEqual(
            self._z80.iy.bits,
            word,
            msg='IX = {:02X}, Word bits = {:02X}'.format(self._z80.iy.bits, word)
        )
