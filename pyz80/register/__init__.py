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

from abc import ABCMeta
from ..arch import BYTE_SIZE, WORD_SIZE


class Z80RegisterError(Exception):
    pass


class Z80Register(object):

    __metaclass__ = ABCMeta

    def __init__(self, bits=0x00, size=BYTE_SIZE):
        self._size = size
        self._lsb_mask = 0x01
        self._msb_mask = self._most_significant_bit_mask()
        self._higher_mask, self._lower_mask = self._build_masks()
        self._bits = self._apply_bit_mask(bits)

    def _build_masks(self):
        lower_mask = self._lsb_mask

        for i in range(0, (self.size / 2) - 1):
            lower_mask = (lower_mask << 1) | self._lsb_mask

        higher_mask = lower_mask << (self.size / 2)

        return higher_mask, lower_mask

    def _apply_bit_mask(self, n):
        return n & (self._higher_mask | self._lower_mask)

    def _nth_bit_mask(self, n):
        """
        Returns a bit mask for the nth bit of the register.
        This method is used as a helper to test if a bit of
        the register is set or reset.
        """
        return self._lsb_mask << n

    def nth_bit(self, n):
        """
        Returns 0x01/0x00 if the nth bit is set/reset.
        """
        nth_bit = 0x00

        if (self._bits & self._nth_bit_mask(n)) is not 0x00:
            nth_bit = 0x01

        return nth_bit

    def set_nth_bit(self, nth_bit):
        self._bits |= self._nth_bit_mask(nth_bit)

    def reset_nth_bit(self, nth_bit):
        if self.nth_bit(nth_bit) is 0x01:
           self._bits ^= self._nth_bit_mask(nth_bit)

    def _most_significant_bit_mask(self):
        return self._nth_bit_mask(self._size - 1)

    @property
    def msb(self):
        return self.nth_bit(self.size - 1)

    @property
    def lsb(self):
        return self.nth_bit(0)

    @property
    def bits(self):
        return self._bits

    @bits.setter
    def bits(self, n):
        self._bits = self._apply_bit_mask(n)

    @property
    def size(self):
        return self._size

    @property
    def lower(self):
        pass

    @lower.setter
    def lower(self, n):
        pass

    @property
    def higher(self):
        pass

    @higher.setter
    def higher(self, n):
        pass

    def shift_right(self):
        self.bits = (self.bits >> 1) & (self._higher_mask | self._lower_mask)
        return self

    def shift_left(self):
        self.bits = (self.bits << 1) & (self._higher_mask | self._lower_mask)
        return self

    def rotate_right(self):
        if (self.bits & self._lsb_mask) is not 0x00:
            self.bits = (self.bits >> 1) | self._msb_mask
        else:
            self.bits >>= 1

        return self

    def rotate_left(self):
        if (self.bits & self._msb_mask) is not 0x00:
            self.bits = ((self.bits - self._msb_mask) << 1) | self._lsb_mask
        else:
            self.bits <<= 1

        return self

    def combine(self, register, RegisterClass):
        if self.size != register.size:
            raise Z80RegisterError('Can\'t combine registers of different sizes.')

        combined_register = RegisterClass(size=self._size * 2)
        combined_register.higher = self.bits
        combined_register.lower = register.bits

        return combined_register

    def __eq__(self, register):
        return (self.size == register.size) and (self.bits == register.bits)

    # TODO: Add test.
    def _add(self, other, RegisterClass):
        if type(other) is int:
            add_result = self.bits + other
        elif type(other) is RegisterClass:
            add_result = self.bits + other.bits
        else:
            raise Z80RegisterError('Can\'t sum {0} and {1} types.'.format(type(self), type(other)))

        return RegisterClass(bits=add_result)

    def __radd__(self, other):
        return self.__add__(other)


class Z80ByteRegister(Z80Register):
    @property
    def lower(self):
        return self.bits & self._lower_mask

    @lower.setter
    def lower(self, n):
        self.bits = (self.higher << (self.size / 2)) | n

    @property
    def higher(self):
        return (self.bits & self._higher_mask) >> (self.size / 2)

    @higher.setter
    def higher(self, n):
        self.bits = (n << (self.size / 2)) | self.lower

    def combine(self, register):
        return super(Z80ByteRegister, self).combine(register, Z80WordRegister)

    def __add__(self, other):
        return self._add(other, Z80ByteRegister)


class Z80WordRegister(Z80Register):
    def __init__(self, bits=0x00, size=WORD_SIZE):
        super(Z80WordRegister, self).__init__(bits=bits, size=size)
        self._lower = Z80ByteRegister()
        self._higher = Z80ByteRegister()
        self.bits = bits

    @property
    def bits(self):
        return (self.higher.bits << (self.size / 2)) | self.lower.bits

    @bits.setter
    def bits(self, n):
        self.lower.bits = n & self._lower_mask
        self.higher.bits = (n & self._higher_mask) >> (self.size / 2)

    @property
    def lower(self):
        return self._lower

    @lower.setter
    def lower(self, n):
        self.lower.bits = n

    @property
    def higher(self):
        return self._higher

    @higher.setter
    def higher(self, n):
        self._higher.bits = n

    def __add__(self, other):
        return self._add(other, Z80WordRegister)


# TODO: Add undocumented flags properties.
class Z80FlagsRegister(Z80ByteRegister):
    SIGN_BIT = 7
    ZERO_BIT = 6
    HALF_CARRY_BIT = 4 
    PARITY_BIT = 2
    ADD_BIT = 1
    CARRY_BIT = 0 

    @property
    def sign_flag(self):
        return self.nth_bit(self.SIGN_BIT)

    def set_sign_flag(self):
        self.set_nth_bit(self.SIGN_BIT)

    def reset_sign_flag(self):
        self.reset_nth_bit(self.SIGN_BIT)

    @property
    def zero_flag(self):
        return self.nth_bit(self.ZERO_BIT)

    def set_zero_flag(self):
        self.set_nth_bit(self.ZERO_BIT)

    def reset_zero_flag(self):
        self.reset_nth_bit(self.ZERO_BIT)

    @property
    def half_carry_flag(self):
        return self.nth_bit(self.HALF_CARRY_BIT)

    def set_half_carry_flag(self):
        self.set_nth_bit(self.HALF_CARRY_BIT)

    def reset_half_carry_flag(self):
        self.reset_nth_bit(self.HALF_CARRY_BIT)

    @property
    def parity_flag(self):
        return self.nth_bit(self.PARITY_BIT)

    def set_parity_flag(self):
        self.set_nth_bit(self.PARITY_BIT)

    def reset_parity_flag(self):
        self.reset_nth_bit(self.PARITY_BIT)

    @property
    def add_substract_flag(self):
        return self.nth_bit(self.ADD_BIT)

    def set_add_substract_flag(self):
        self.set_nth_bit(self.ADD_BIT)

    def reset_add_substract_flag(self):
        self.reset_nth_bit(self.ADD_BIT)

    @property
    def carry_flag(self):
        return self.nth_bit(self.CARRY_BIT)

    def set_carry_flag(self):
        self.set_nth_bit(self.CARRY_BIT)

    def reset_carry_flag(self):
        self.reset_nth_bit(self.CARRY_BIT)
