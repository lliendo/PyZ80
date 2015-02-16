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

from sys import stdout
from ..cli import CLI
from ..cpu import Z80
from ..class_loader import ClassLoader
from ..io import Device


class PyZ80LauncherError(Exception):
    pass


class PyZ80Launcher(object):
    def __init__(self):
        self._cli = CLI()
        self._z80_cpu = Z80(trace_fd=self._open_trace())

    def _open_trace(self):
        trace_fd = None

        if self._cli.trace == True:
            trace_fd = stdout

        return trace_fd

    def _read_program(self):
        try:
            with open(self._cli.program_path, 'rb') as fd:
                program = [ord(opcode) for opcode in fd.read()]
        except IOError:
            raise PyZ80LauncherError(
                'Error - File: {0} does not exist.'.format(self._cli.program_path)
            )
        except TypeError:
            raise PyZ80LauncherError(
                'Error - Invalid program opcode in: {0}.'.format(self._cli.program_path)
            )

        return program

    def _read_address(self):
        try:
            return int(self._cli.address, base=16)
        except ValueError:
            raise PyZ80LauncherError(
                'Error - {0} is not a valid hex address.'.format(self._cli.address)
            )

    def _check_device(self, D):
        if not issubclass(D, Device):
            raise PyZ80LauncherError(
                'Error - {0} device must inherit from \'Device\' class.'.format(D.__name__)
            )

        return D

    def _load_devices(self):
        if self._cli.devices_module_path:
            device_classes = ClassLoader(self._cli.devices_module_path).get_classes()
            [self._z80.load_device(self._check_device(D)) for D in device_classes]

    def run(self):
        self._load_devices()
        self._z80_cpu.run(
            program=self._read_program(), address=self._read_address()
        )
