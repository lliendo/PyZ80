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
from abc_rotate_and_shift import *


class Rlca(RotateLeft):
    """ RLCA """

    regexp = compile_re('^$')

    def _update_sign_flag(register):
        pass

    def _update_zero_flag(register):
        pass

    def _update_parity_flag(register):
        pass

    def _instruction_logic(self):
        super(Rlca, self)._instruction_logic(self._z80.a)


class Rla(Rlca):
    """ RLA """

    regexp = compile_re('^$')

    def _update_sign_flag(register):
        pass

    def _update_zero_flag(register):
        pass

    def _update_parity_flag(register):
        pass

    def _instruction_logic(self):
        super(Rla, self)._instruction_logic()
        self._z80.a.bits |= self._carry_flag


class Rrca(RotateRight):
    """ RRCA """

    regexp = compile_re('^$')

    def _update_sign_flag(register):
        pass

    def _update_zero_flag(register):
        pass

    def _update_parity_flag(register):
        pass

    def _instruction_logic(self):
        super(Rrca, self)._instruction_logic(self._z80.a)
    

class Rra(Rrca):
    """ RRA """

    regexp = compile_re('^$')

    def _update_sign_flag(register):
        pass

    def _update_zero_flag(register):
        pass

    def _update_parity_flag(register):
        pass

    def _instruction_logic(self):
        super(Rra, self)._instruction_logic()
        # This is wrong because it alters the a register AFTER
        # flags are tested & updated.
        self._z80.a.bits |= (self._carry_flag << (self._z80.a.size - 1))


""" RLC instructions. """

# TODO: Update _update_flags() method !
class RlcR(RotateLeft):
    """ RLC r """

    regexp = compile_re('^$')

    def _instruction_logic(self, selector):
        register = self._instruction_selector(selector)
        super(RlcR, self)._instruction_logic(register)


class RlcIndirectAddressHL(RlcIndirectAddress):
    """ RLC (HL) """

    regexp = compile_re('^$')

    def _instruction_logic(self):
        super(RlcIndirectAddressHL, self)._instruction_logic(self._z80.hl.bits)


class RlcIndirectAddressIX(RlcIndirectAddress):
    """ RLC (IX + d) """

    regexp = compile_re('^$')

    def _instruction_logic(self, offset):
        address = self._z80.ix.bits + offset
        super(RlcIndirectAddressIX, self)._instruction_logic(address)


class RlcIndirectAddressIY(RlcIndirectAddress):
    """ RLC (IY + d) """

    regexp = compile_re('^$')

    def _instruction_logic(self, offset):
        address = self._z80.iy.bits + offset
        super(RlcIndirectAddressIY, self)._instruction_logic(address)


class RlcIndirectAddressIXR(RlcIndirectAddress):
    """ RLC (IX + d), r """

    regexp = compile_re('^$')

    def _instruction_logic(self, offset, selector):
        address = self._z80.ix.bits + offset
        register = self._instruction_selector(selector)
        register.bits = super(RlcIndirectAddressIXR, self)._instruction_logic(address).bits


class RlcIndirectAddressIYR(RlcIndirectAddress):
    """ RLC (IY + d), r """

    regexp = compile_re('^$')

    def _instruction_logic(self, offset, selector):
        address = self._z80.iy.bits + offset
        register = self._instruction_selector(selector)
        register.bits = super(RlcIndirectAddressIYR, self)._instruction_logic(address).bits


""" RL instructions. """

# TODO: Update _update_flags() method !
class RlR(Rlcr):
    """ RL r """

    regexp = compile_re('^$')

    def _instruction_logic(self, selector):
        # carry_flag = self._z80.f.carry_flag()
        super(RlR, self)._instruction_logic(selector)
        register.bits |= self._carry_flag


class RlIndirectAddressHL(RlIndirectAddress):
    """ RL (HL) """

    regexp = compile_re('^$')

    def _instruction_logic(self):
        super(RlIndirectAddressHL, self)._instruction_logic(self._z80.hl.bits)


class RlIndirectAddressIX(RlIndirectAddress):
    """ RL (IX + d) """

    regexp = compile_re('^$')

    def _instruction_logic(self, offset):
        address = self._z80.ix.bits + offset
        super(RlIndirectAddressIX, self)._instruction_logic(address)


class RlIndirectAddressIY(RlIndirectAddress):
    """ RL (IY + d) """

    regexp = compile_re('^$')

    def _instruction_logic(self, offset):
        address = self._z80.iy.bits + offset
        super(RlIndirectAddressIY, self)._instruction_logic(address)


class RlIndirectAddressIXR(RlIndirectAddress):
    """ RL (IX + d), r """

    regexp = compile_re('^$')

    def _instruction_logic(self, offset, selector):
        address = self._z80.ix.bits + offset
        register = self._instruction_selector(selector)
        register.bits = super(RlIndirectAddressIXR, self)._instruction_logic(address).bits


class RlIndirectAddressIYR(RlIndirectAddress):
    """ RL (IY + d), r """

    regexp = compile_re('^$')

    def _instruction_logic(self, offset, selector):
        address = self._z80.iy.bits + offset
        register = self._instruction_selector(selector)
        register.bits = super(RlIndirectAddressIYR, self)._instruction_logic(address).bits


""" RRC instructions. """

# TODO: Update _update_flags() method !
class RrcR(RotateRight):
    """ RRC r """

    regexp = compile_re('^$')

    def _instruction_logic(self, selector):
        register = self._instruction_selector(selector)
        super(RrcR, self)._instruction_logic(register)


class RrcIndirectAddressHL(RrcIndirectAddress):
    """ RRC (HL) """

    regexp = compile_re('^$')

    def _instruction_logic(self):
        super(RrcIndirectAddressHL, self)._instruction_logic(self._z80.hl.bits)


class RrcIndirectAddressIX(RrcIndirectAddress):
    """ RRC (IX + d) """

    regexp = compile_re('^$')

    def _instruction_logic(self, offset):
        address = self._z80.ix.bits + offset
        super(RrcIndirectAddressIX, self)._instruction_logic(address)


class RrcIndirectAddressIY(RrcIndirectAddress):
    """ RRC (IY + d) """

    regexp = compile_re('^$')

    def _instruction_logic(self, offset):
        address = self._z80.iy.bits + offset
        super(RrcIndirectAddressIY, self)._instruction_logic(address)


class RrcIndirectAddressIXR(RrcIndirectAddress):
    """ RRC (IX + d), r """

    regexp = compile_re('^$')

    def _instruction_logic(self, offset, selector):
        address = self._z80.ix.bits + offset
        register = self._instruction_selector(selector)
        register.bits = super(RrcIndirectAddressIXR, self)._instruction_logic(address).bits


class RrcIndirectAddressIYR(RrcIndirectAddress):
    """ RRC (IY + d), r """

    regexp = compile_re('^$')

    def _instruction_logic(self, offset, selector):
        address = self._z80.iy.bits + offset
        register = self._instruction_selector(selector)
        register.bits = super(RrcIndirectAddressIYR, self)._instruction_logic(address).bits


""" RR instructions. """

# TODO: Update _update_flags() method !
class RrR(Rrcr):
    """ RR r """

    regexp = compile_re('^$')

    def _instruction_logic(self, selector):
        # carry_flag = self._z80.f.carry_flag()
        super(RrR, self)._instruction_logic(selector)
        register.bits |= self._carry_flag


class RrIndirectAddressHL(RrIndirectAddress):
    """ RR (HL) """

    regexp = compile_re('^$')

    def _instruction_logic(self):
        super(RrIndirectAddressHL, self)._instruction_logic(self._z80.hl.bits)


class RrIndirectAddressIX(RrIndirectAddress):
    """ RR (IX + d) """

    regexp = compile_re('^$')

    def _instruction_logic(self, offset):
        address = self._z80.ix.bits + offset
        super(RrIndirectAddressIX, self)._instruction_logic(address)


class RrIndirectAddressIY(RrIndirectAddress):
    """ RR (IY + d) """

    regexp = compile_re('^$')

    def _instruction_logic(self, offset):
        address = self._z80.iy.bits + offset
        super(RrIndirectAddressIY, self)._instruction_logic(address)


class RrIndirectAddressIXR(RrIndirectAddress):
    """ RR (IX + d), r """

    regexp = compile_re('^$')

    def _instruction_logic(self, offset, selector):
        address = self._z80.ix.bits + offset
        register = self._instruction_selector(selector)
        register.bits = super(RrIndirectAddressIXR, self)._instruction_logic(address).bits


class RrIndirectAddressIYR(RrIndirectAddress):
    """ RR (IY + d), r """

    regexp = compile_re('^$')

    def _instruction_logic(self, offset, selector):
        address = self._z80.iy.bits + offset
        register = self._instruction_selector(selector)
        register.bits = super(RrIndirectAddressIYR, self)._instruction_logic(address).bits


# class SlaR(ShiftLeft):
#     """ SLA r """
# 
#     regexp = compile_re('^$')
# 
#     def _instruction_logic(self, selector):
#         register = self._instruction_selector(selector)
#         super(SlaR, self)._instruction_logic(register)
# 
# 
# class SlaIndirectAddressHL(SlaIndirectAddress):
#     """ SLA (HL) """
# 
#     regexp = compile_re('^$')
# 
#     def _instruction_logic(self):
#         super(SlaIndirectAddressHL, self)._instruction_logic(self._z80.hl.bits)
# 
# 
# class SlcIndirectAddressIX(SlcIndirectAddress):
#     """ SLC (IX + d) """
# 
#     regexp = compile_re('^$')
# 
#     def _instruction_logic(self, offset):
#         address = self._z80.ix.bits + offset
#         super(SlcIndirectAddressIX, self)._instruction_logic(address)
# 
# 
# class SlcIndirectAddressIY(SlcIndirectAddress):
#     """ SLC (IY + d) """
# 
#     regexp = compile_re('^$')
# 
#     def _instruction_logic(self, offset):
#         address = self._z80.iy.bits + offset
#         super(SlcIndirectAddressIY, self)._instruction_logic(address)
