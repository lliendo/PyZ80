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
from math import log


class Z80RegisterError(Exception):
    pass


class Z80Register(object):

    __metaclass__ = ABCMeta

    def __init__(self, bits=0x00, size=8):
        self._size = size
        self._lsb_mask = 0x01
        self._msb_mask = self._most_significant_bit_mask()
        self._higher_mask, self._lower_mask = self._build_masks()

        if bits > (self._higher_mask | self._lower_mask):
            self._overflow_cond = True
        else:
            self._overflow_cond = False

        self._bits = self._apply_register_bit_mask(bits)

        self._carry_cond = False
        self._add_substract_cond = False

    def _build_masks(self):
        lower_mask = self._lsb_mask

        for i in range(0, (self.size / 2) - 1):
            lower_mask = (lower_mask << 1) | self._lsb_mask

        higher_mask = lower_mask << (self.size / 2)

        return higher_mask, lower_mask

    def _apply_register_bit_mask(self, n):
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
        Returns True/False if the nth bit is set/reset.
        """
        return (self._bits & self._nth_bit_mask(n)) is not 0x00

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
        self._bits = self._apply_register_bit_mask(n)

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

    def shift_right(self, n):
        self.bits = (self.bits >> n) & (self._higher_mask | self._lower_mask)

    def shift_left(self, n):
        self.bits = (self.bits << n) & (self._higher_mask | self._lower_mask)

    def rotate_right(self, n):
        for i in range(0, n):
            if (self.bits & self._lsb_mask) is not 0x00:
                self.bits = (self.bits >> 1) | self._msb_mask
            else:
                self.bits >>= 1

    def rotate_left(self, n):
        for i in range(0, n):
            if (self.bits & self._msb_mask) is not 0x00:
                self.bits = ((self.bits - self._msb_mask) << 1) | self._lsb_mask
            else:
                self.bits <<= 1

    def combine(self, register, RegisterClass):
        if self.size != register.size:
            raise Z80RegisterError('Can\'t combine registers of different sizes.')

        combined_register = RegisterClass(size=self._size * 2)
        combined_register.higher = self.bits
        combined_register.lower = register.bits

        return combined_register

    def __eq__(self, register):
        return (self.size == register.size) and (self.bits == register.bits)

    # TODO: Add unit test !
    def _add(self, other, RegisterClass):
        # TODO: Is it possible to avoid the 'type' call ?.

        if type(other) is int:
            add_result = self.bits + other
        elif type(other) is RegisterClass:
            add_result = self.bits + other.bits
        else:
            raise Z80RegisterError('Can\'t sum {0} and {1} types.'.format(type(self), type(other)))

        register = RegisterClass(bits=add_result)

        # TODO: Possibly also create & set: carry, add_substract & remaining
        # properties on the register side. This is useful to get overflow,
        # add_substract, carry conditions after an add operator is
        # performed, and avoids re-executing the same code to verify
        # these conditions.

        return register

    @property
    def even(self):
        return self.lsb

    @property
    def signed(self):
        return self.msb

    @property
    def zero(self):
        return self._bits is 0x00

    """
    This set of properties reflect how a register
    is affected after a certain operation and serves as an entry
    point for updating the cpu's flag register.
    """

    @property
    def overflow_cond(self):
        return self._overflow_cond

    @overflow_cond.setter
    def overflow_cond(self, cond):
        self._overflow_cond = cond

    @property
    def carry_cond(self):
        return self._carry_cond

    @carry_cond.setter
    def carry_cond(self, cond):
        self._carry_cond = cond

    @property
    def add_substract_cond(self):
        return self._add_substract_cond

    @add_substract_cond.setter
    def add_substract_cond(self, cond):
        self._add_substract_cond = cond

    def __radd__(self, other):
        return self.__add__(other)


class Z80ByteRegister(Z80Register):
    def __init__(self, bits=0x00, size=8):
        super(Z80ByteRegister, self).__init__(bits=bits, size=size)

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
    def __init__(self, bits=0x00, size=16):
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
class Z80FlagsRegister(Z80Register):
    SIGN_BIT = 7
    ZERO_BIT = 6
    HALF_CARRY_BIT = 4 
    PARITY_BIT = 2
    ADD_BIT = 1
    CARRY_BIT = 0 

    def __init__(self, bits=0x00, size=8):
        super(Z80FlagsRegister, self).__init__(bits=bits, size=size)

    def _set_nth_bit(self, nth_bit):
        self.bits |= self._nth_bit_mask(nth_bit)

    def _reset_nth_bit(self, nth_bit):
        if self.nth_bit(nth_bit):
            self.bits ^= self._nth_bit_mask(nth_bit)
        
    @property
    def sign_flag(self):
        return self.nth_bit(self.SIGN_BIT)

    def set_sign_flag(self):
        self._set_nth_bit(self.SIGN_BIT)

    def reset_sign_flag(self):
        self._reset_nth_bit(self.SIGN_BIT)

    @property
    def zero_flag(self):
        return self.nth_bit(self.ZERO_BIT)

    def set_zero_flag(self):
        self._set_nth_bit(self.ZERO_BIT)

    def reset_zero_flag(self):
        self._reset_nth_bit(self.ZERO_BIT)

    @property
    def half_carry_flag(self):
        return self.nth_bit(self.HALF_CARRY_BIT)

    def set_half_carry_flag(self):
        self._set_nth_bit(self.HALF_CARRY_BIT)

    def reset_half_carry_flag(self):
        self._reset_nth_bit(self.HALF_CARRY_BIT)

    @property
    def parity_flag(self):
        return self.nth_bit(self.PARITY_BIT)

    def set_parity_flag(self):
        self._set_nth_bit(self.PARITY_BIT)

    def reset_parity_flag(self):
        self._reset_nth_bit(self.PARITY_BIT)

    @property
    def add_substract_flag(self):
        return self.nth_bit(self.ADD_BIT)

    def set_add_substract_flag(self):
        self._set_nth_bit(self.ADD_BIT)

    def reset_add_substract_flag(self):
        self._reset_nth_bit(self.ADD_BIT)

    @property
    def carry_flag(self):
        return self.nth_bit(self.CARRY_BIT)

    def set_carry_flag(self):
        self._set_nth_bit(self.CARRY_BIT)

    def reset_carry_flag(self):
        self._reset_nth_bit(self.CARRY_BIT)
