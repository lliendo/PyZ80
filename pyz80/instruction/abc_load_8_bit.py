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
from . import Instruction


class LoadRegisterRegister(Instruction):

    __metaclass__ = ABCMeta

    def _default_selector(self, selector):
        registers = {
            0b000: self._z80.b,
            0b001: self._z80.c,
            0b010: self._z80.d,
            0b011: self._z80.e,
            0b111: self._z80.a,
        }

        return registers[selector]

    def _r_selector(self, selector):
        registers = {
            0b100: self._z80.h,
            0b101: self._z80.l,
        }

        return registers[selector]

    def _p_selector(self, selector):
        registers = {
            0b100: self._z80.ixh,
            0b101: self._z80.ixl,
        }

        return registers[selector]

    def _q_selector(self, selector):
        registers = {
            0b100: self._z80.iyh,
            0b101: self._z80.iyl,
        }

        return registers[selector]

    def _select_register(self, selector):
        try:
            register = self._default_selector(selector)
        except KeyError:
            register = self._instruction_selector(selector)

        return register

    def _message_log(self, destination_selector, source_selector):
        return 'LD {:} {:}'.format(
            self._select_register(destination_selector).label,
            self._select_register(source_selector).label
        )

    def _instruction_logic(self, destination_selector, source_selector):
        destination_register = self._select_register(destination_selector)
        source_register = self._select_register(source_selector)
        destination_register.bits = source_register.bits


class LoadRegisterNumber(LoadRegisterRegister):

    __metaclass__ = ABCMeta

    def _message_log(self, destination_selector, n):
        return 'LD {:} {:02X}'.format(
            self._select_register(destination_selector).label,
            n
        )

    def _instruction_logic(self, destination_selector, n):
        destination_register = self._select_register(destination_selector)
        destination_register.bits = n


class LoadRegisterIndirectAddress(LoadRegisterRegister):

    __metaclass__ = ABCMeta

    def _instruction_selector(self, selector):
        return self._r_selector(selector)

    def _load_register_from_ram(self, selector, address):
        destination_register = self._select_register(selector)
        destination_register.bits = self._z80.ram.read(address)


class LoadIndirectAddressRegister(LoadRegisterRegister):

    __metaclass__ = ABCMeta

    def _instruction_selector(self, selector):
        return self._r_selector(selector)

    def _load_ram_from_register(self, selector, address):
        source_register = self._select_register(selector)
        self._z80.ram.write(address, source_register.bits)
