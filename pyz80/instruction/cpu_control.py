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

from re import compile as compile_re
from . import Instruction, NotImplemented


# TODO: Implement !
class Daa(Instruction):
    """ DAA """

    regexp = compile_re('^00100111$')

    def _message_log(self):
        return 'DAA'

    def _update_flags(self):
        pass

    def _instruction_logic(self):
        raise NotImplemented


class Cpl(Instruction):
    """ CPL """

    regexp = compile_re('^00101111$')

    def _message_log(self):
        return 'CPL'

    def _update_flags(self):
        self._z80.f.set_half_carry_flag()
        self._z80.f.set_add_substract_flag()

    def _instruction_logic(self):
        self._z80.a.invert()
        self._update_flags()


class Neg(Instruction):
    """ NEG """

    regexp = compile_re('^1110110101000100$')

    def _message_log(self):
        return 'NEG'

    def _update_flags(self, instruction_result):
        self._update_sign_flag(instruction_result)
        self._update_zero_flag(instruction_result)
        self._update_half_carry_flag(self._z80.a.bits.lower)
        self._update_overflow_flag(self._z80.a.bits)
        self._update_carry_flag(self._z80.a.bits)
        self._z80.f.set_add_substract_flag()

    # TODO: Is this behavior correct ?
    # Half carry will always be 1 because 0x00 is always less than
    # lower z80.a nibble. The only exception is when z80.a is also 0x00.
    def _half_carry(self, lower_nibble):
        return 0x00 < lower_nibble

    def _overflow(self, bits):
        return bits is 0x80

    def _carry(self, bits):
        return bits is not 0x00

    def _instruction_logic(self):
        neg_result = 0x00 - self._z80.a.bits
        self._update_flags(neg_result)
        self._z80.a.bits = neg_result


class Ccf(Instruction):
    """ CCF """

    regexp = compile_re('^00111111$')

    def _message_log(self):
        return 'CCF'

    def _update_flags(self):
        if self._z80.f.carry_flag is not 0x00:
            self._z80.f.set_half_carry_flag()
            self._z80.f.reset_carry_flag()
        else:
            self._z80.f.reset_half_carry_flag()
            self._z80.f.set_carry_flag()

        self._z80.f.reset_add_substract_flag()

    def _instruction_logic(self):
        self._update_flags()


class Scf(Instruction):
    """ SCF """

    regexp = compile_re('^00110111$')

    def _message_log(self):
        return 'SCF'

    def _update_flags(self):
        self._z80.f.reset_half_carry_flag()
        self._z80.f.reset_add_substract_flag()
        self._z80.f.set_carry_flag()

    def _instruction_logic(self):
        self._update_flags()


class Nop(Instruction):
    """ NOP """

    regexp = compile_re('^00000000$')

    def _message_log(self):
        return 'NOP'

    def _instruction_logic(self):
        pass


class Halt(Instruction):
    """ HALT """

    regexp = compile_re('^01110110$')

    def _message_log(self):
        return 'HALT'

    def _instruction_logic(self):
        self._z80.halt()


class Di(Instruction):
    """ DI """

    regexp = compile_re('^11110011$')

    def _message_log(self):
        return 'DI'

    def _instruction_logic(self):
        self._z80.iff1, self._z80.iff2 = 0x00, 0x00


class Ei(Instruction):
    """ EI """

    regexp = compile_re('^11111011$')

    def _message_log(self):
        return 'EI'

    def _instruction_logic(self):
        self._z80.iff1, self._z80.iff2 = 0x01, 0x01


class Im0(Instruction):
    """ IM 0 """

    regexp = compile_re('^1110110101000110$')

    def _message_log(self):
        return 'IM 0'

    def _instruction_logic(self):
        self._z80.im = 0x00


class Im1(Instruction):
    """ IM 1 """

    regexp = compile_re('^1110110101010110$')

    def _message_log(self):
        return 'IM 1'

    def _instruction_logic(self):
        self._z80.im = 0x01


class Im2(Instruction):
    """ IM 2 """

    regexp = compile_re('^1110110101011110$')

    def _message_log(self):
        return 'IM 2'

    def _instruction_logic(self):
        self._z80.im = 0x02
