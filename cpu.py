""" 
    This file is part of PyZ80.

    PyZ80 is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    PyZ80 is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with PyZ80.  If not, see <http://www.gnu.org/licenses/>.
"""

from cli import *
from z80 import Z80
from ram import *
from device import *
from logger import *

import exceptions
import os

class InvalidOpcode(Exception) :
    pass

class NoRAM(Exception) :
    pass

class InvalidLogFile(Exception) :
    pass

class CPU(object) :
    def __init__(self) :
        self.devices = None
        self.ram = None
        self.z80 = Z80()

    def _read_program(self, path) :
        fd = open(path)
        opcodes = fd.read()

        try :
            opcodes = map(lambda opcode : ord(opcode), opcodes)
        except TypeError :
            raise InvalidOpcode

        print "%d bytes read." % len(opcodes)
        return opcodes

    def plug_device(self, device) :
        if not isinstance(device, Device) :
            raise DeviceNotCompliant(device)

        device.name
        device.address
        self.z80.plug_device(device)

    def plug_ram(self, ram) :
        if not isinstance(ram, Ram) :
            raise RamNotCompliant

        self.ram = ram

    def load(self, path, address) :
        program = self._read_program(path)
        self.ram.load(program, address)

    def run(self) :
        cli_options = parse_cli_options()

        try :
            self.z80.logger = Logger(cli_options["trace_log"])
        except IOError :
            raise InvalidLogFile("Couldn't not open '%s' logfile" % cli_options["trace_log"])

        for program, address in cli_options["programs"] :
            self.load(program, address)

        if not self.ram :
            raise NoRAM("No RAM module present.")

        self.z80.plug_ram(self.ram)
        self.z80.run(cli_options["start_address"])

if __name__ == "__main__" :
    # Ram & devices.
    ram64KiB = Ram64KiB()
    dummy_device = DummyDevice()
    dummy_device.name = "DUMMY_DEVICE"
    dummy_device.address = 0xFF
    
    # Computer.
    computer = CPU()

    try :
        computer.plug_ram(ram64KiB)
        computer.plug_device(dummy_device)
        computer.run()

    except Exception, e :
        print e
