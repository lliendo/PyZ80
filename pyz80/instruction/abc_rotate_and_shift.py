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

from . import Instruction
from abc import ABCMeta


class RotateAndShift(Instruction):

    __metaclass__ = ABCMeta

    def __init__(self, *args, **kwargs):
        super(RotateAndShift, self).__init__(*args, **kwargs)
        self._carry_flag = self._z80.f.carry_flag()

    def _instruction_selector(self, selector):
        registers = {
            0b000: self._z80.b,
            0b001: self._z80.c,
            0b010: self._z80.d,
            0b011: self._z80.e,
            0b100: self._z80.h,
            0b101: self._z80.l,
            0b111: self._z80.a,
        }
 
        return registers[selector]

    def _update_flags(self, register):
        self._update_sign_flag(register)
        self._update_zero_flag(register)
        self._update_parity_flag(register)
        self._z80.f.reset_half_carry_flag()
        self._z80.f.reset_add_substract_flag()
        self._update_carry_flag(register)


class RotateLeft(RotateAndShift):

    __metaclass__ = ABCMeta
    
    def _update_carry_flag(self, register):
        if self._msb is 0x01:
            self._z80.f.set_carry_flag()
        else:
            self._z80.f.reset_carry_flag()

    def _instruction_logic(self, register):
        self._msb = register.msb
        register = register.rotate_left()
        self._update_flags(register)

        return register


class RotateRight(RotateAndShift):

    __metaclass__ = ABCMeta

    def _update_carry_flag(self, register):
        if self._lsb is 0x01:
            self._z80.f.set_carry_flag()
        else:
            self._z80.f.reset_carry_flag()

    def _instruction_logic(self, register):
        self._lsb = register.lsb
        register = register.rotate_right()
        self._update_flags(register)

        return register


class RlcIndirectAddress(RotateLeft):

    __metaclass__ = ABCMeta

    def _instruction_logic(self, address):
        register = Z80ByteRegister(bits=self._z80.ram.read(address))
        register = super(RlcIndirectAddress, self)._instruction_logic(register)
        self._z80.write(address, register.bits)

        return register


class RrcIndirectAddress(RotateRight):

    __metaclass__ = ABCMeta

    def _instruction_logic(self, address):
        register = Z80ByteRegister(bits=self._z80.ram.read(address))
        register = super(RrcIndirectAddress, self)._instruction_logic(register)
        self._z80.write(address, register.bits)

        return register


class RlIndirectAddress(RotateLeft):

    __metaclass__ = ABCMeta

    def _instruction_logic(self, address):
        carry_flag = self._z80.f.carry_flag
        register = Z80ByteRegister(bits=self._z80.ram.read(address))
        register = super(RlIndirectAddress, self)._instruction_logic(register)
        self._z80.write(address, register.bits | carry_flag)

        return register


class RrIndirectAddress(RotateRight):

    __metaclass__ = ABCMeta

    def _instruction_logic(self, address):
        carry_flag = self._z80.f.carry_flag
        register = Z80ByteRegister(bits=self._z80.ram.read(address))
        register = super(RrIndirectAddress, self)._instruction_logic(register)
        self._z80.write(address, register.bits | (carry_flag << (register.size - 1)))

        return register


class ShiftLeft(RotateAndShift):

    __metaclass__ = ABCMeta
    
    def _update_carry_flag(self, register):
        if self._msb is 0x01:
            self._z80.f.set_carry_flag()
        else:
            self._z80.f.reset_carry_flag()

    def _instruction_logic(self, register):
        register = register.shift_left()
        self._update_flags(register)

        return register


class SlcIndirectAddress(ShiftLeft):

    __metaclass__ = ABCMeta

    def _instruction_logic(self, address):
        register = Z80ByteRegister(bits=self._z80.ram.read(address))
        register = super(SlcIndirectAddress, self)._instruction_logic(register)
        self._z80.write(address, register.bits)

        return register


class ShiftRight(RotateAndShift):

    __metaclass__ = ABCMeta

    def _update_carry_flag(self, register):
        if self._lsb is 0x01:
            self._z80.f.set_carry_flag()
        else:
            self._z80.f.reset_carry_flag()

    def _instruction_logic(self, register):
        register = register.shift_right()
        self._update_flags(register)

        return register
