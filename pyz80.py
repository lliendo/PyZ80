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

    Copyright 2010-2011 Lucas Liendo.
"""

from cpu import *

def main() :
    # Ram & devices.
    ram64KiB = Ram64KiB()
    dummy_device = DummyDevice()
    dummy_device.name = "DUMMY_DEVICE"
    dummy_device.address = 0x1
    
    # Computer.
    computer = CPU()

    try :
        computer.plug_ram(ram64KiB)
        computer.plug_device(dummy_device)
        computer.run()
    except Exception, e :
        print e

if __name__ == "__main__" :
    main()
