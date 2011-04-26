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

from optparse import OptionParser
import exceptions
import os

""" This file defines some helper functions that
    simplify the CLI argument options. """

class CLIException(Exception) :
    pass

def validate_file(path) :
    """ Validates that path is a file and exists. """

    if not os.path.isfile(path) :
        raise CLIException("'%s' does not exist or is not file." % path)

    return path

def validate_address(address) :
    """ Validates an hexadecimal address. """

    try :
        if (int(address, 16) < 0x0) or (int(address, 16) > 0xFFFF) :
            raise CLIException("Address out of range.")

    except ValueError :
        raise CLIException("Invalid address.")

    return int(address, 16)

def parse_cli_options() :
    """ Returns a dictionary with options read from the CLI. """

    parser = OptionParser()
    parser.add_option("-t", "--trace-log", default="/dev/null", \
                        help="Log execution trace to specified file. Default logfile is /dev/null.")
    parser.add_option("-s", "--start-address", default="0x0000", \
                        help="Start execution at specified address. Default is 0x0000.")
    parser.add_option("-p", "--programs", default=None, \
                        help="Load program/s. PROGRAM_1:ADDRESS_1[, PROGRAM_2:ADDRESS_2[, ...]]")
    options, _ = parser.parse_args()

    programs = map(lambda x : (validate_file(x.split(":") [0]), \
    validate_address(x.split(":") [1])), options.programs.split(","))

    return {"programs" : programs, \
    "trace_log" : options.trace_log, \
    "start_address" : validate_address(options.start_address)}
