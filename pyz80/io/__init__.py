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
from Queue import Queue
from threading import Thread


class DeviceManagerError(Exception):
    pass


class Device(Thread):

    __metaclass__ = ABCMeta
    address = None

    def __init__(self, device_manager):
        super(Device, self).__init__()
        self._input = Queue()
        self._output = Queue()
        self._device_manager = device_manager

    @abstractmethod
    def run(self):
        pass

    def _read(self, block=False, timeout=0):
        return self._input.get(block, timeout)

    def _write(self, data, block=False, timeout=0):
        self._output.put(data, block, timeout)


class DeviceManager(object):
    def __init__(self):
        self._devices = []

    def _get_device(self, address):
        try:
            device = [d for d in self._devices if d.address == address].pop()
        except IndexError:
            raise DeviceManagerError(
                'Error - No device at address : {0}'.format(address)
            )

        return device

    def add(self, device):
        try:
            registered_device = self._get_device(device.address)
        except DeviceManagerError:
            self._devices.append(device)

        if registered_device:
            raise DeviceManagerError(
                'Error - A device is already registered at address : {0}'.format(device.address)
            )

    def read(self, address, block=False, timeout=0):
        return self._get_device(address).output.get(block, timeout)

    def write(self, address, data, block=False, timeout=0):
        self._get_device(address).input.put(data, block, timeout)

    def run(self):
        [d.start() for d in self._devices]
        [d.join() for d in self._devices]


class InterruptManager(object):
    def __init__(self, z80):
        self._z80

    def nmi(self):
        # No state at all is held for non maskable interrupts.
        pass

    def int(self, address, data):
        # Maskable interrupts hold a line state.
        pass
