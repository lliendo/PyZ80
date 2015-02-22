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

from .test_z80_base import TestZ80
from ..instruction.decoder import InstructionDecoder


class TestLoadInstructions(TestZ80):
    def test_instruction_unique_regexps(self):
        instruction_decoder = InstructionDecoder(None)
        regexps = map(lambda i: i.regexp.pattern, instruction_decoder._z80_instructions())
        self.assertEqual(len(regexps), len(set(regexps)))
