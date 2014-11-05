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
from . import Instruction


class LoadRegisterRegister(Instruction):

    __metaclass__ = ABCMeta

    def _instruction_logic(self, destination_selector, source_selector):
        destination_register = self._register_selector(destination_selector)
        source_register = self._register_selector(source_selector)
        destination_register.bits = source_register.bits


class LoadRegisterNumber(Instruction):
    __metaclass__ = ABCMeta

    def _instruction_logic(self, destination_selector, bits):
        destination_register = self._register_selector(destination_selector)
        destination_register.bits = bits


class LoadRegisterIndirectAddress(Instruction):

    __metaclass__ = ABCMeta

    def _register_selector(self, selector):
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

    def _load_register_from_ram(self, selector, address):
        destination_register = self._register_selector(selector)
        destination_register.bits = self._z80.ram.read(address)


class LoadIndirectAddressRegister(Instruction):

    __metaclass__ = ABCMeta

    def _register_selector(self, selector):
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

    def _load_ram_from_register(self, selector, address):
        source_register = self._register_selector(selector)
        self._z80.ram.write(address, source_register.bits)
