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

import exceptions
import random
import sys

class DeviceException(Exception) :
    pass

class DeviceNoName(DeviceException) :
    pass

class DeviceInvalidName(DeviceException) :
    pass

class DeviceInvalidAddress(DeviceException) :
    pass

class DeviceNoAddress(DeviceException) :
    pass

class DeviceAddressInUse(DeviceException) :
    pass

class DeviceNotCompliant(DeviceException) :
    def __str__(self) :
        return "Not compliant device."

class Device(object) :
    def __init__(self) :
        self._name = None
        self._address = None

    def read(self, address, *args, **kwargs) :
        return 0xFF

    def write(self, address, *args, **kwargs) :
        pass

    @property
    def name(self) :
        if not self._name :
            e = "Device has no identifier."
            raise DeviceNoName(e)

        return self._name

    @name.setter
    def name(self, name) :
        if type(name) is not str :
            e = "%s is not a valid device identifier." % str(address)
            raise DeviceInvalidName(e)

        self._name = name

    @property
    def address(self) :
        if not self._address :
            e = "Device has no address."
            raise DeviceNoAddress(e)

        return self._address

    @address.setter
    def address(self, address) :
        if (type(address) is not int) or (address < 0x0) or (address > 0xFFFF) :
            e = "%s is not a valid device address." % str(address)
            raise DeviceInvalidAddress(e)

        self._address = address

class DummyDevice(Device) :
    """ Generic device for testing purposes. """

    def read(self) :
        r = random.randint(0x0, 0xFF)
        #print "Reading : 0x%0.2X" % r
        return r

    def write(self, byte) :
        sys.stdout.write(chr(byte))
        #print "[Writing] H : 0x%0.2X, D : %c" % (byte, byte)
