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

from ..cli import CLI
from ..cpu import Z80


class PyZ80LauncherError(Exception):
    pass


class PyZ80Launcher(object):
    def __init__(self):
        self._cli = CLI()
        self._z80_cpu = Z80()

    def _read_program(self):
        try:
            fd = open(self._cli.program_path, 'rb')
            return [int(opcode) for opcode in fd.read()]
        except IOError:
            raise PyZ80LauncherError(
                'Error - File: {0} does not exist.'.format(self._cli.program_path)
            )
        except TypeError:
            raise PyZ80LauncherError(
                'Error - Invalid program opcode in: {0}.'.format(self._cli.program_path)
            )

    def _read_address(self):
        try:
            return int(self._cli.address)
        except ValueError:
            raise PyZ80LauncherError(
                'Error - {0} is not a valid address.'.format(self._cli.address)
            )

    def run(self):
        self._z80_cpu.run(
            program=self._read_program(), address=self._read_address()
        )
