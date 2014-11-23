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
from abc_arithmetic_8_bit import Add8Bit, Sub8Bit


class Add16Bit(Add8Bit):
    
    __metaclass__ = ABCMeta

    def _overflow(self, operands):
        return super(Add16Bit, self)._overflow(operands, bits=WORD_SIZE)

    def _carry(self, operands):
        return super(Add16Bit, self)._carry(operands, bits=WORD_SIZE)

    def _half_carry(self, operands):
        return super(Add16Bit, self)._half_carry(operands, bits=WORD_SIZE)


class Sub16Bit(Sub8Bit):

    __metaclass__ = ABCMeta

    def _overflow(self, operands):
        return super(Sub16Bit, self)._overflow(operands, bits=WORD_SIZE)

    def _carry(self, operands):
        return super(Sub16Bit, self)._carry(operands, bits=WORD_SIZE)

    def _half_carry(self, operands):
        return super(Sub16Bit, self)._half_carry(operands, bits=WORD_SIZE)
