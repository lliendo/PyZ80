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

from abc import ABCMeta, abstractmethod
from ..register import Z80FlagsRegister
from ..arch import NIBBLE_SIZE, BYTE_SIZE


class Instruction(object):
    
    __metaclass__ = ABCMeta
    instruction_regexp = None
    log_message = ''

    def __init__(self, z80, log_fd=None):
        self._z80 = z80
        self._log_fd = log_fd

    @abstractmethod
    def _instruction_logic(self, *operands):
        pass

    def _translate_logging_args(self, *args):
        """
        Each instruction should implement this method in order
        to be able to logged properly.
        """
        return args

    def _log(self, *args):
        try:
            logging_args = self._translate_logging_args(*args)
            self._log_fd.write(self.log_message.format(*logging_args) + '\n')
        except AttributeError:
            pass

    def execute(self, operands):
        self._instruction_logic(*operands)
        self._log(*operands)
        # return self._instruction_flags

    def _get_address(self, high_order_byte, low_order_byte):
        """
        Given high and a low order byte this method returns
        an address which is the composition of the high and low
        order bytes.
        """
        base = 256
        return (high_order_byte * base) + low_order_byte

    def _msb(self, n, bits=BYTE_SIZE):
        return (n >> (bits - 1)) & 0x01

    def _bitmask(self, bits=BYTE_SIZE):
        return int(pow(2, bits) - 1)

    def _parity(self, n):
        parity_even = True
        ones_count = len(filter(lambda s: s is '1', bin(n).lstrip('0b')))

        if ones_count & 0x01:
            parity_even = False

        return parity_even

    def _zero(self, n, bits=BYTE_SIZE):
        return (n & self._bitmask(bits=bits)) is 0x00

    def _sign(self, n, bits=BYTE_SIZE):
        return self._msb(n, bits=bits)

    def _half_carry(self, operands, bits=BYTE_SIZE):
        return self._carry(operands, bits=((bits / NIBBLE_SIZE) - 1) * NIBBLE_SIZE)

    def _update_overflow_flag(self, operands):
        if self._overflow(operands):
            self._z80.f.set_parity_flag()
        else:
            self._z80.f.reset_parity_flag()

    def _update_carry_flag(self, operands):
        if self._carry(operands):
            self._z80.f.set_carry_flag()
        else:
            self._z80.f.reset_carry_flag()

    def _update_half_carry_flag(self, operands):
        if self._half_carry(operands):
            self._z80.f.set_half_carry_flag()
        else:
            self._z80.f.reset_half_carry_flag()

    def _update_sign_flag(self, instruction_result):
        if self._sign(instruction_result):
            self._z80.f.set_sign_flag()
        else:
            self._z80.f.reset_sign_flag()

    def _update_zero_flag(self, instruction_result):
        if self._zero(instruction_result):
            self._z80.f.set_zero_flag()
        else:
            self._z80.f.reset_zero_flag()

    def _update_parity_flag(self, instruction_result):
        if self._parity(instruction_result):
            self._z80.f.set_parity_flag()
        else:
            self._z80.f.reset_parity_flag()

    def _update_add_substract_flag(self, instruction_result):
        if self._add_substract(instruction_result):
            self._z80.f.set_add_substract_flag()
        else:
            self._z80.f.reset_add_substract_flag()
