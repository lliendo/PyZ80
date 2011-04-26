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

class RamException(Exception) :
    pass

class RamInvalidAddress(RamException) :
    pass

class RamNotCompliant(RamException) :
    def __str__(self) :
        return "Not compliant RAM."

class Ram(object) :
    def __init__(self, size) :
        self._size = size
        self._ram = self.reset()

    @property
    def size(self) :
        """
        Returns the size of the RAM object.
        """
        return self._size

    def read(self, address) :
        return 0x0

    def write(self, address, byte) :
        pass

    def load(self, opcodes, address=0x0) :
        pass

    def reset(self) :
        """
        Clears the RAM object.
        """
        ram = []

        for i in range(0, self._size) :
            ram.append(0)

        return ram

class Ram64KiB(Ram) :
    """ 
    This class represents a 64 KiB RAM module.
    """
    _invalid_address = "Invalid RAM address"

    def __init__(self) :
        size = 65536
        super(Ram64KiB, self).__init__(size)

    def read(self, address) :
        """
        Reads a byte at address.
        """
        self._check_address(address)
        return self._ram[address]

    def write(self, address, byte) :
        """
        Writes a byte at address.
        """
        self._check_address(address)
        self._ram[address] = byte

    # Esto a un decorador.
    def _check_address(self, address) :
        if (address < 0x0) or (address > self.size) :
            raise RamInvalidAddress(self._invalid_address)

        return 0

    def load(self, opcodes, address=0x0) :
        """
        Loads a program (sequence of opcodes)
        starting a address.
        """
        #if address + len(opcodes) > 0xFFFF :
        #    raise 

        for opcode in opcodes :
            self._ram[address] = opcode
            address += 1

    ## Debug.
    #def ram_info(self) :
    #    print "Size       : " + str(len(self.ram)) + "\n"
    #    print "RAM output : "
    #    
    #    for i in range(0, pow(2, self.size)) :
    #        print "0x%0.2X at : %0.5d" % (self.ram[i], i)

    def dump_ram_range(self, start_addr, end_addr) :
        print "----------------------------"
        print "RAM dump (0x%0.2X - 0x%0.2X)" % (start_addr, end_addr)
        while start_addr <= end_addr :
            print "0x%0.2X at : 0x%X" % (self._ram[start_addr], start_addr)
            start_addr += 1

        print "----------------------------\n"
