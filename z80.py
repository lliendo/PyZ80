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

from z80_helper import *
from ram import Ram
from device import Device

import exceptions

class UnknownOpcode(Exception) :
    pass

class Z80(object) :
    def __init__(self) :
        # Z80 registers.
        self.registers = {"a" : 0x0, 
        "f" : 0x0,
        "b" : 0x0,
        "c" : 0x0,
        "d" : 0x0,
        "e" : 0x0,
        "h" : 0x0,
        "l" : 0x0,
        "w" : 0x0,
        "z" : 0x0,
        "a_" : 0x0, 
        "f_" : 0x0,
        "b_" : 0x0,
        "c_" : 0x0,
        "d_" : 0x0,
        "e_" : 0x0,
        "h_" : 0x0,
        "l_" : 0x0,
        "w_" : 0x0,
        "z_" : 0x0,
        "sp" : 0xFFFF, 
        "pc" : 0x0,
        "ir" : 0x0,
        "ix" : 0x0,
        "iy" : 0x0,
        "i" : 0x0,
        "r" : 0x0,
        "iff1" : 0x0,
        "iff2" : 0x0,
        "im" : 0x0,
        }

        self.ram = None
        self.devices = None
        self._logger = None
        self._bdos_extension = False

        self.cb_opcodes = {0x0 : (self._rlc_r, ("b",), 1),
        0x01 : (self._rlc_r, ("c",), 1),
        0x02 : (self._rlc_r, ("d",), 1),
        0x03 : (self._rlc_r, ("e",), 1),
        0x04 : (self._rlc_r, ("h",), 1),
        0x05 : (self._rlc_r, ("l",), 1),
        0x06 : (self._rlc_addr_rr, ("hl",), 1),
        0x07 : (self._rlc_r, ("a",), 1),
        0x08 : (self._rrc_r, ("b",), 1),
        0x09 : (self._rrc_r, ("c",), 1),
        0x0A : (self._rrc_r, ("d",), 1),
        0x0B : (self._rrc_r, ("e",), 1),
        0x0C : (self._rrc_r, ("h",), 1),
        0x0D : (self._rrc_r, ("l",), 1),
        0x0E : (self._rrc_addr_rr, ("hl",), 1),
        0x0F : (self._rrc_r, ("a",), 1),

        0x10 : (self._rl_r, ("b",), 1),
        0x11 : (self._rl_r, ("c",), 1),
        0x12 : (self._rl_r, ("d",), 1),
        0x13 : (self._rl_r, ("e",), 1),
        0x14 : (self._rl_r, ("h",), 1),
        0x15 : (self._rl_r, ("l",), 1),
        0x16 : (self._rl_addr_rr, ("hl",), 1),
        0x17 : (self._rl_r, ("a",), 1),
        0x18 : (self._rr_r, ("b",), 1),
        0x19 : (self._rr_r, ("c",), 1),
        0x1A : (self._rr_r, ("d",), 1),
        0x1B : (self._rr_r, ("e",), 1),
        0x1C : (self._rr_r, ("h",), 1),
        0x1D : (self._rr_r, ("l",), 1),
        0x1E : (self._rr_addr_rr, ("hl",), 1),
        0x1F : (self._rr_r, ("a",), 1),

        0x20 : (self._sla_r, ("b",), 1),
        0x21 : (self._sla_r, ("c",), 1),
        0x22 : (self._sla_r, ("d",), 1),
        0x23 : (self._sla_r, ("e",), 1),
        0x24 : (self._sla_r, ("h",), 1),
        0x25 : (self._sla_r, ("l",), 1),
        0x26 : (self._sla_addr_rr, ("hl",), 1),
        0x27 : (self._sla_r, ("a",), 1),
        0x28 : (self._sra_r, ("b",), 1),
        0x29 : (self._sra_r, ("c",), 1),
        0x2A : (self._sra_r, ("d",), 1),
        0x2B : (self._sra_r, ("e",), 1),
        0x2C : (self._sra_r, ("h",), 1),
        0x2D : (self._sra_r, ("l",), 1),
        0x2E : (self._sra_addr_rr, ("hl",), 1),
        0x2F : (self._sra_r, ("a",), 1),

        0x30 : (self._sll_r, ("b",), 1),
        0x31 : (self._sll_r, ("c",), 1),
        0x32 : (self._sll_r, ("d",), 1),
        0x33 : (self._sll_r, ("e",), 1),
        0x34 : (self._sll_r, ("h",), 1),
        0x35 : (self._sll_r, ("l",), 1),
        0x36 : (self._sll_addr_rr, ("hl",), 1),
        0x37 : (self._sll_r, ("a",), 1),
        0x38 : (self._srl_r, ("b",), 1),
        0x39 : (self._srl_r, ("c",), 1),
        0x3A : (self._srl_r, ("d",), 1),
        0x3B : (self._srl_r, ("e",), 1),
        0x3C : (self._srl_r, ("h",), 1),
        0x3D : (self._srl_r, ("l",), 1),
        0x3E : (self._srl_addr_rr, ("hl",), 1),
        0x3F : (self._srl_r, ("a",), 1),

        0x40 : (self._bit_n_r, (0x1, "b",), 1),
        0x41 : (self._bit_n_r, (0x1, "c",), 1),
        0x42 : (self._bit_n_r, (0x1, "d",), 1),
        0x43 : (self._bit_n_r, (0x1, "e",), 1),
        0x44 : (self._bit_n_r, (0x1, "h",), 1),
        0x45 : (self._bit_n_r, (0x1, "l",), 1),
        0x46 : (self._bit_n_addr_rr, (0x1, "hl",), 1),
        0x47 : (self._bit_n_r, (0x1, "a",), 1),
        0x48 : (self._bit_n_r, (0x2, "b",), 1),
        0x49 : (self._bit_n_r, (0x2, "c",), 1),
        0x4A : (self._bit_n_r, (0x2, "d",), 1),
        0x4B : (self._bit_n_r, (0x2, "e",), 1),
        0x4C : (self._bit_n_r, (0x2, "h",), 1),
        0x4D : (self._bit_n_r, (0x2, "l",), 1),
        0x4E : (self._bit_n_addr_rr, (0x2, "hl",), 1),
        0x4F : (self._bit_n_r, (0x2, "a",), 1),

        0x50 : (self._bit_n_r, (0x4, "b",), 1),
        0x51 : (self._bit_n_r, (0x4, "c",), 1),
        0x52 : (self._bit_n_r, (0x4, "d",), 1),
        0x53 : (self._bit_n_r, (0x4, "e",), 1),
        0x54 : (self._bit_n_r, (0x4, "h",), 1),
        0x55 : (self._bit_n_r, (0x4, "l",), 1),
        0x56 : (self._bit_n_addr_rr, (0x4, "hl",), 1),
        0x57 : (self._bit_n_r, (0x4, "a",), 1),
        0x58 : (self._bit_n_r, (0x8, "b",), 1),
        0x59 : (self._bit_n_r, (0x8, "c",), 1),
        0x5A : (self._bit_n_r, (0x8, "d",), 1),
        0x5B : (self._bit_n_r, (0x8, "e",), 1),
        0x5C : (self._bit_n_r, (0x8, "h",), 1),
        0x5D : (self._bit_n_r, (0x8, "l",), 1),
        0x5E : (self._bit_n_addr_rr, (0x8, "hl",), 1),
        0x5F : (self._bit_n_r, (0x8, "a",), 1),

        0x60 : (self._bit_n_r, (0x10, "b",), 1),
        0x61 : (self._bit_n_r, (0x10, "c",), 1),
        0x62 : (self._bit_n_r, (0x10, "d",), 1),
        0x63 : (self._bit_n_r, (0x10, "e",), 1),
        0x64 : (self._bit_n_r, (0x10, "h",), 1),
        0x65 : (self._bit_n_r, (0x10, "l",), 1),
        0x66 : (self._bit_n_addr_rr, (0x10, "hl",), 1),
        0x67 : (self._bit_n_r, (0x10, "a",), 1),
        0x68 : (self._bit_n_r, (0x20, "b",), 1),
        0x69 : (self._bit_n_r, (0x20, "c",), 1),
        0x6A : (self._bit_n_r, (0x20, "d",), 1),
        0x6B : (self._bit_n_r, (0x20, "e",), 1),
        0x6C : (self._bit_n_r, (0x20, "h",), 1),
        0x6D : (self._bit_n_r, (0x20, "l",), 1),
        0x6E : (self._bit_n_addr_rr, (0x20, "hl",), 1),
        0x6F : (self._bit_n_r, (0x20, "a",), 1),

        0x70 : (self._bit_n_r, (0x40, "b",), 1),
        0x71 : (self._bit_n_r, (0x40, "c",), 1),
        0x72 : (self._bit_n_r, (0x40, "d",), 1),
        0x73 : (self._bit_n_r, (0x40, "e",), 1),
        0x74 : (self._bit_n_r, (0x40, "h",), 1),
        0x75 : (self._bit_n_r, (0x40, "l",), 1),
        0x76 : (self._bit_n_addr_rr, (0x40, "hl",), 1),
        0x77 : (self._bit_n_r, (0x40, "a",), 1),
        0x78 : (self._bit_n_r, (0x80, "b",), 1),
        0x79 : (self._bit_n_r, (0x80, "c",), 1),
        0x7A : (self._bit_n_r, (0x80, "d",), 1),
        0x7B : (self._bit_n_r, (0x80, "e",), 1),
        0x7C : (self._bit_n_r, (0x80, "h",), 1),
        0x7D : (self._bit_n_r, (0x80, "l",), 1),
        0x7E : (self._bit_n_addr_rr, (0x80, "hl",), 1),
        0x7F : (self._bit_n_r, (0x80, "a",), 1),

        0x80 : (self._res_n_r, (0xFE, "b",), 1),
        0x81 : (self._res_n_r, (0xFE, "c",), 1),
        0x82 : (self._res_n_r, (0xFE, "d",), 1),
        0x83 : (self._res_n_r, (0xFE, "e",), 1),
        0x84 : (self._res_n_r, (0xFE, "h",), 1),
        0x85 : (self._res_n_r, (0xFE, "l",), 1),
        0x86 : (self._res_n_addr_rr, (0xFE, "hl",), 1),
        0x87 : (self._res_n_r, (0xFE, "a",), 1),
        0x88 : (self._res_n_r, (0xFD, "b",), 1),
        0x89 : (self._res_n_r, (0xFD, "c",), 1),
        0x8A : (self._res_n_r, (0xFD, "d",), 1),
        0x8B : (self._res_n_r, (0xFD, "e",), 1),
        0x8C : (self._res_n_r, (0xFD, "h",), 1),
        0x8D : (self._res_n_r, (0xFD, "l",), 1),
        0x8E : (self._res_n_addr_rr, (0xFD, "hl",), 1),
        0x8F : (self._res_n_r, (0xFD, "a",), 1),

        0x90 : (self._res_n_r, (0xFB, "b",), 1),
        0x91 : (self._res_n_r, (0xFB, "c",), 1),
        0x92 : (self._res_n_r, (0xFB, "d",), 1),
        0x93 : (self._res_n_r, (0xFB, "e",), 1),
        0x94 : (self._res_n_r, (0xFB, "h",), 1),
        0x95 : (self._res_n_r, (0xFB, "l",), 1),
        0x96 : (self._res_n_addr_rr, (0xFB, "hl",), 1),
        0x97 : (self._res_n_r, (0xFB, "a",), 1),
        0x98 : (self._res_n_r, (0xF7, "b",), 1),
        0x99 : (self._res_n_r, (0xF7, "c",), 1),
        0x9A : (self._res_n_r, (0xF7, "d",), 1),
        0x9B : (self._res_n_r, (0xF7, "e",), 1),
        0x9C : (self._res_n_r, (0xF7, "h",), 1),
        0x9D : (self._res_n_r, (0xF7, "l",), 1),
        0x9E : (self._res_n_addr_rr, (0xF7, "hl",), 1),
        0x9F : (self._res_n_r, (0xF7, "a",), 1),

        0xA0 : (self._res_n_r, (0xEF, "b",), 1),
        0xA1 : (self._res_n_r, (0xEF, "c",), 1),
        0xA2 : (self._res_n_r, (0xEF, "d",), 1),
        0xA3 : (self._res_n_r, (0xEF, "e",), 1),
        0xA4 : (self._res_n_r, (0xEF, "h",), 1),
        0xA5 : (self._res_n_r, (0xEF, "l",), 1),
        0xA6 : (self._res_n_addr_rr, (0xEF, "hl",), 1),
        0xA7 : (self._res_n_r, (0xEF, "a",), 1),
        0xA8 : (self._res_n_r, (0xDF, "b",), 1),
        0xA9 : (self._res_n_r, (0xDF, "c",), 1),
        0xAA : (self._res_n_r, (0xDF, "d",), 1),
        0xAB : (self._res_n_r, (0xDF, "e",), 1),
        0xAC : (self._res_n_r, (0xDF, "h",), 1),
        0xAD : (self._res_n_r, (0xDF, "l",), 1),
        0xAE : (self._res_n_addr_rr, (0xDF, "hl",), 1),
        0xAF : (self._res_n_r, (0xDF, "a",), 1),

        0xB0 : (self._res_n_r, (0xBF, "b",), 1),
        0xB1 : (self._res_n_r, (0xBF, "c",), 1),
        0xB2 : (self._res_n_r, (0xBF, "d",), 1),
        0xB3 : (self._res_n_r, (0xBF, "e",), 1),
        0xB4 : (self._res_n_r, (0xBF, "h",), 1),
        0xB5 : (self._res_n_r, (0xBF, "l",), 1),
        0xB6 : (self._res_n_addr_rr, (0xBF, "hl",), 1),
        0xB7 : (self._res_n_r, (0xBF, "a",), 1),
        0xB8 : (self._res_n_r, (0x7F, "b",), 1),
        0xB9 : (self._res_n_r, (0x7F, "c",), 1),
        0xBA : (self._res_n_r, (0x7F, "d",), 1),
        0xBB : (self._res_n_r, (0x7F, "e",), 1),
        0xBC : (self._res_n_r, (0x7F, "h",), 1),
        0xBD : (self._res_n_r, (0x7F, "l",), 1),
        0xBE : (self._res_n_addr_rr, (0x7F, "hl",), 1),
        0xBF : (self._res_n_r, (0x7F, "a",), 1),

        0xC0 : (self._set_n_r, (0x1, "b",), 1),
        0xC1 : (self._set_n_r, (0x1, "c",), 1),
        0xC2 : (self._set_n_r, (0x1, "d",), 1),
        0xC3 : (self._set_n_r, (0x1, "e",), 1),
        0xC4 : (self._set_n_r, (0x1, "h",), 1),
        0xC5 : (self._set_n_r, (0x1, "l",), 1),
        0xC6 : (self._set_n_addr_rr, (0x1, "hl",), 1),
        0xC7 : (self._set_n_r, (0x1, "a",), 1),
        0xC8 : (self._set_n_r, (0x2, "b",), 1),
        0xC9 : (self._set_n_r, (0x2, "c",), 1),
        0xCA : (self._set_n_r, (0x2, "d",), 1),
        0xCB : (self._set_n_r, (0x2, "e",), 1),
        0xCC : (self._set_n_r, (0x2, "h",), 1),
        0xCD : (self._set_n_r, (0x2, "l",), 1),
        0xCE : (self._set_n_addr_rr, (0x2, "hl",), 1),
        0xCF : (self._set_n_r, (0x2, "a",), 1),

        0xD0 : (self._set_n_r, (0x4, "b",), 1),
        0xD1 : (self._set_n_r, (0x4, "c",), 1),
        0xD2 : (self._set_n_r, (0x4, "d",), 1),
        0xD3 : (self._set_n_r, (0x4, "e",), 1),
        0xD4 : (self._set_n_r, (0x4, "h",), 1),
        0xD5 : (self._set_n_r, (0x4, "l",), 1),
        0xD6 : (self._set_n_addr_rr, (0x4, "hl",), 1),
        0xD7 : (self._set_n_r, (0x4, "a",), 1),
        0xD8 : (self._set_n_r, (0x8, "b",), 1),
        0xD9 : (self._set_n_r, (0x8, "c",), 1),
        0xDA : (self._set_n_r, (0x8, "d",), 1),
        0xDB : (self._set_n_r, (0x8, "e",), 1),
        0xDC : (self._set_n_r, (0x8, "h",), 1),
        0xDD : (self._set_n_r, (0x8, "l",), 1),
        0xDE : (self._set_n_addr_rr, (0x8, "hl",), 1),
        0xDF : (self._set_n_r, (0x8, "a",), 1),

        0xE0 : (self._set_n_r, (0x10, "b",), 1),
        0xE1 : (self._set_n_r, (0x10, "c",), 1),
        0xE2 : (self._set_n_r, (0x10, "d",), 1),
        0xE3 : (self._set_n_r, (0x10, "e",), 1),
        0xE4 : (self._set_n_r, (0x10, "h",), 1),
        0xE5 : (self._set_n_r, (0x10, "l",), 1),
        0xE6 : (self._set_n_addr_rr, (0x10, "hl",), 1),
        0xE7 : (self._set_n_r, (0x10, "a",), 1),
        0xE8 : (self._set_n_r, (0x20, "b",), 1),
        0xE9 : (self._set_n_r, (0x20, "c",), 1),
        0xEA : (self._set_n_r, (0x20, "d",), 1),
        0xEB : (self._set_n_r, (0x20, "e",), 1),
        0xEC : (self._set_n_r, (0x20, "h",), 1),
        0xED : (self._set_n_r, (0x20, "l",), 1),
        0xEE : (self._set_n_addr_rr, (0x20, "hl",), 1),
        0xEF : (self._set_n_r, (0x20, "a",), 1),

        0xF0 : (self._set_n_r, (0x40, "b",), 1),
        0xF1 : (self._set_n_r, (0x40, "c",), 1),
        0xF2 : (self._set_n_r, (0x40, "d",), 1),
        0xF3 : (self._set_n_r, (0x40, "e",), 1),
        0xF4 : (self._set_n_r, (0x40, "h",), 1),
        0xF5 : (self._set_n_r, (0x40, "l",), 1),
        0xF6 : (self._set_n_addr_rr, (0x40, "hl",), 1),
        0xF7 : (self._set_n_r, (0x40, "a",), 1),
        0xF8 : (self._set_n_r, (0x80, "b",), 1),
        0xF9 : (self._set_n_r, (0x80, "c",), 1),
        0xFA : (self._set_n_r, (0x80, "d",), 1),
        0xFB : (self._set_n_r, (0x80, "e",), 1),
        0xFC : (self._set_n_r, (0x80, "h",), 1),
        0xFD : (self._set_n_r, (0x80, "l",), 1),
        0xFE : (self._set_n_addr_rr, (0x80, "hl",), 1),
        0xFF : (self._set_n_r, (0x80, "a",), 1),
        }

        self.ddcb_opcodes = {0x0 : (self._rlc_indx_d_r, ("ix", "b",), 3),
        0x01 : (self._rlc_indx_d_r, ("ix", "c",), 3), 
        0x02 : (self._rlc_indx_d_r, ("ix", "d",), 3), 
        0x03 : (self._rlc_indx_d_r, ("ix", "e",), 3), 
        0x04 : (self._rlc_indx_d_r, ("ix", "h",), 3), 
        0x05 : (self._rlc_indx_d_r, ("ix", "l",), 3), 
        0x06 : (self._rlc_indx_d, ("ix",), 3), 
        0x07 : (self._rlc_indx_d_r, ("ix", "a",), 3), 
        0x08 : (self._rrc_indx_d_r, ("ix", "b",), 3), 
        0x09 : (self._rrc_indx_d_r, ("ix", "c",), 3), 
        0x0A : (self._rrc_indx_d_r, ("ix", "d",), 3), 
        0x0B : (self._rrc_indx_d_r, ("ix", "e",), 3), 
        0x0C : (self._rrc_indx_d_r, ("ix", "h",), 3), 
        0x0D : (self._rrc_indx_d_r, ("ix", "l",), 3), 
        0x0E : (self._rrc_indx_d, ("ix",), 3), 
        0x0F : (self._rrc_indx_d_r, ("ix", "a",), 3), 
        
        0x10 : (self._rl_indx_d_r, ("ix", "b",), 3), 
        0X11 : (self._rl_indx_d_r, ("ix", "c",), 3), 
        0x12 : (self._rl_indx_d_r, ("ix", "d",), 3), 
        0x13 : (self._rl_indx_d_r, ("ix", "e",), 3), 
        0x14 : (self._rl_indx_d_r, ("ix", "h",), 3), 
        0x15 : (self._rl_indx_d_r, ("ix", "l",), 3), 
        0x16 : (self._rl_indx_d, ("ix",), 3), 
        0x17 : (self._rl_indx_d_r, ("ix", "a",), 3), 
        0x18 : (self._rr_indx_d_r, ("ix", "b",), 3), 
        0x19 : (self._rr_indx_d_r, ("ix", "c",), 3), 
        0x1A : (self._rr_indx_d_r, ("ix", "d",), 3), 
        0x1B : (self._rr_indx_d_r, ("ix", "e",), 3), 
        0x1C : (self._rr_indx_d_r, ("ix", "h",), 3), 
        0x1D : (self._rr_indx_d_r, ("ix", "l",), 3), 
        0x1E : (self._rr_indx_d, ("ix",), 3), 
        0x1F : (self._rr_indx_d_r, ("ix", "a",), 3), 

        0x20 : (self._sla_indx_d_r, ("ix", "b",), 3), 
        0x21 : (self._sla_indx_d_r, ("ix", "c",), 3), 
        0x22 : (self._sla_indx_d_r, ("ix", "d",), 3), 
        0x23 : (self._sla_indx_d_r, ("ix", "e",), 3), 
        0x24 : (self._sla_indx_d_r, ("ix", "h",), 3), 
        0x25 : (self._sla_indx_d_r, ("ix", "l",), 3), 
        0x26 : (self._sla_indx_d, ("ix",), 3), 
        0x27 : (self._sla_indx_d_r, ("ix", "a",), 3), 
        0x28 : (self._sra_indx_d_r, ("ix", "b",), 3), 
        0x29 : (self._sra_indx_d_r, ("ix", "c",), 3), 
        0x2A : (self._sra_indx_d_r, ("ix", "d",), 3), 
        0x2B : (self._sra_indx_d_r, ("ix", "e",), 3), 
        0x2C : (self._sra_indx_d_r, ("ix", "h",), 3), 
        0x2D : (self._sra_indx_d_r, ("ix", "l",), 3), 
        0x2E : (self._sra_indx_d, ("ix",), 3), 
        0x2F : (self._sra_indx_d_r, ("ix", "a",), 3), 

        0x30 : (self._sll_indx_d_r, ("ix", "b",), 3), 
        0x31 : (self._sll_indx_d_r, ("ix", "c",), 3), 
        0x32 : (self._sll_indx_d_r, ("ix", "d",), 3), 
        0x33 : (self._sll_indx_d_r, ("ix", "e",), 3), 
        0x34 : (self._sll_indx_d_r, ("ix", "h",), 3), 
        0x35 : (self._sll_indx_d_r, ("ix", "l",), 3), 
        0x36 : (self._sll_indx_d, ("ix",), 3), 
        0x37 : (self._sll_indx_d_r, ("ix", "a"), 3), 
        0x38 : (self._srl_indx_d_r, ("ix", "b",), 3), 
        0x39 : (self._srl_indx_d_r, ("ix", "c",), 3), 
        0x3A : (self._srl_indx_d_r, ("ix", "d",), 3), 
        0x3B : (self._srl_indx_d_r, ("ix", "e",), 3), 
        0x3C : (self._srl_indx_d_r, ("ix", "h",), 3), 
        0x3D : (self._srl_indx_d_r, ("ix", "l",), 3), 
        0x3E : (self._srl_indx_d, ("ix",), 3), 
        0x3F : (self._srl_indx_d_r, ("ix", "a",), 3), 

        0x40 : (self._bit_n_indx_d, (0x1, "ix",), 3), 
        0x41 : (self._bit_n_indx_d, (0x1, "ix",), 3), 
        0x42 : (self._bit_n_indx_d, (0x1, "ix",), 3), 
        0x43 : (self._bit_n_indx_d, (0x1, "ix",), 3), 
        0x44 : (self._bit_n_indx_d, (0x1, "ix",), 3), 
        0x45 : (self._bit_n_indx_d, (0x1, "ix",), 3), 
        0x46 : (self._bit_n_indx_d, (0x1, "ix",), 3), 
        0x47 : (self._bit_n_indx_d, (0x1, "ix",), 3), 
        0x48 : (self._bit_n_indx_d, (0x2, "ix",), 3), 
        0x49 : (self._bit_n_indx_d, (0x2, "ix",), 3), 
        0x4A : (self._bit_n_indx_d, (0x2, "ix",), 3), 
        0x4B : (self._bit_n_indx_d, (0x2, "ix",), 3), 
        0x4C : (self._bit_n_indx_d, (0x2, "ix",), 3), 
        0x4D : (self._bit_n_indx_d, (0x2, "ix",), 3), 
        0x4E : (self._bit_n_indx_d, (0x2, "ix",), 3), 
        0x4F : (self._bit_n_indx_d, (0x2, "ix",), 3), 

        0x50 : (self._bit_n_indx_d, (0x4, "ix",), 3), 
        0x51 : (self._bit_n_indx_d, (0x4, "ix",), 3), 
        0x52 : (self._bit_n_indx_d, (0x4, "ix",), 3), 
        0x53 : (self._bit_n_indx_d, (0x4, "ix",), 3), 
        0x54 : (self._bit_n_indx_d, (0x4, "ix",), 3), 
        0x55 : (self._bit_n_indx_d, (0x4, "ix",), 3), 
        0x56 : (self._bit_n_indx_d, (0x4, "ix",), 3), 
        0x57 : (self._bit_n_indx_d, (0x4, "ix",), 3), 
        0x58 : (self._bit_n_indx_d, (0x8, "ix",), 3), 
        0x59 : (self._bit_n_indx_d, (0x8, "ix",), 3), 
        0x5A : (self._bit_n_indx_d, (0x8, "ix",), 3), 
        0x5B : (self._bit_n_indx_d, (0x8, "ix",), 3), 
        0x5C : (self._bit_n_indx_d, (0x8, "ix",), 3), 
        0x5D : (self._bit_n_indx_d, (0x8, "ix",), 3), 
        0x5E : (self._bit_n_indx_d, (0x8, "ix",), 3), 
        0x5F : (self._bit_n_indx_d, (0x8, "ix",), 3), 

        0x60 : (self._bit_n_indx_d, (0x10, "ix",), 3),
        0x61 : (self._bit_n_indx_d, (0x10, "ix",), 3),
        0x62 : (self._bit_n_indx_d, (0x10, "ix",), 3),
        0x63 : (self._bit_n_indx_d, (0x10, "ix",), 3),
        0x64 : (self._bit_n_indx_d, (0x10, "ix",), 3),
        0x65 : (self._bit_n_indx_d, (0x10, "ix",), 3),
        0x66 : (self._bit_n_indx_d, (0x10, "ix",), 3),
        0x67 : (self._bit_n_indx_d, (0x10, "ix",), 3),
        0x68 : (self._bit_n_indx_d, (0x20, "ix",), 3),
        0x69 : (self._bit_n_indx_d, (0x20, "ix",), 3),
        0x6A : (self._bit_n_indx_d, (0x20, "ix",), 3),
        0x6B : (self._bit_n_indx_d, (0x20, "ix",), 3),
        0x6C : (self._bit_n_indx_d, (0x20, "ix",), 3),
        0x6D : (self._bit_n_indx_d, (0x20, "ix",), 3),
        0x6E : (self._bit_n_indx_d, (0x20, "ix",), 3),
        0x6F : (self._bit_n_indx_d, (0x20, "ix",), 3),
        
        0x70 : (self._bit_n_indx_d, (0x40, "ix",), 3),
        0x71 : (self._bit_n_indx_d, (0x40, "ix",), 3),
        0x72 : (self._bit_n_indx_d, (0x40, "ix",), 3),
        0x73 : (self._bit_n_indx_d, (0x40, "ix",), 3),
        0x74 : (self._bit_n_indx_d, (0x40, "ix",), 3),
        0x75 : (self._bit_n_indx_d, (0x40, "ix",), 3),
        0x76 : (self._bit_n_indx_d, (0x40, "ix",), 3),
        0x77 : (self._bit_n_indx_d, (0x40, "ix",), 3),
        0x78 : (self._bit_n_indx_d, (0x80, "ix",), 3),
        0x79 : (self._bit_n_indx_d, (0x80, "ix",), 3),
        0x7A : (self._bit_n_indx_d, (0x80, "ix",), 3),
        0x7B : (self._bit_n_indx_d, (0x80, "ix",), 3),
        0x7C : (self._bit_n_indx_d, (0x80, "ix",), 3),
        0x7D : (self._bit_n_indx_d, (0x80, "ix",), 3),
        0x7E : (self._bit_n_indx_d, (0x80, "ix",), 3),
        0x7F : (self._bit_n_indx_d, (0x80, "ix",), 3),

        0x80 : (self._res_n_indx_d_r, (0xFE, "ix", "b",), 3), 
        0x81 : (self._res_n_indx_d_r, (0xFE, "ix", "c",), 3), 
        0x82 : (self._res_n_indx_d_r, (0xFE, "ix", "d",), 3), 
        0x83 : (self._res_n_indx_d_r, (0xFE, "ix", "e",), 3), 
        0x84 : (self._res_n_indx_d_r, (0xFE, "ix", "h",), 3), 
        0x85 : (self._res_n_indx_d_r, (0xFE, "ix", "l",), 3), 
        0x86 : (self._res_n_indx_d, (0xFE, "ix",), 3), 
        0x87 : (self._res_n_indx_d_r, (0xFE, "ix", "a",), 3), 
        0x88 : (self._res_n_indx_d_r, (0xFD, "ix", "b",), 3), 
        0x89 : (self._res_n_indx_d_r, (0xFD, "ix", "c",), 3), 
        0x8A : (self._res_n_indx_d_r, (0xFD, "ix", "d",), 3), 
        0x8B : (self._res_n_indx_d_r, (0xFD, "ix", "e",), 3), 
        0x8C : (self._res_n_indx_d_r, (0xFD, "ix", "h",), 3), 
        0x8D : (self._res_n_indx_d_r, (0xFD, "ix", "l",), 3), 
        0x8E : (self._res_n_indx_d, (0xFD, "ix",), 3), 
        0x8F : (self._res_n_indx_d_r, (0xFD, "ix", "a",), 3), 

        0x90 : (self._res_n_indx_d_r, (0xFB, "ix", "b",), 3),
        0x91 : (self._res_n_indx_d_r, (0xFB, "ix", "c",), 3),
        0x92 : (self._res_n_indx_d_r, (0xFB, "ix", "d",), 3),
        0x93 : (self._res_n_indx_d_r, (0xFB, "ix", "e",), 3),
        0x94 : (self._res_n_indx_d_r, (0xFB, "ix", "h",), 3),
        0x95 : (self._res_n_indx_d_r, (0xFB, "ix", "l",), 3),
        0x96 : (self._res_n_indx_d, (0xFB, "ix",), 3),
        0x97 : (self._res_n_indx_d_r, (0xFB, "ix", "a",), 3),
        0x98 : (self._res_n_indx_d_r, (0xF7, "ix", "b",), 3),
        0x99 : (self._res_n_indx_d_r, (0xF7, "ix", "c",), 3),
        0x9A : (self._res_n_indx_d_r, (0xF7, "ix", "d",), 3),
        0x9B : (self._res_n_indx_d_r, (0xF7, "ix", "e",), 3),
        0x9C : (self._res_n_indx_d_r, (0xF7, "ix", "h",), 3),
        0x9D : (self._res_n_indx_d_r, (0xF7, "ix", "l",), 3),
        0x9E : (self._res_n_indx_d, (0xF7, "ix",), 3),
        0x9F : (self._res_n_indx_d_r, (0xF7, "ix", "a",), 3),
        
        0xA0 : (self._res_n_indx_d_r, (0xEF, "ix", "b",), 3),
        0xA1 : (self._res_n_indx_d_r, (0xEF, "ix", "c",), 3),
        0xA2 : (self._res_n_indx_d_r, (0xEF, "ix", "d",), 3),
        0xA3 : (self._res_n_indx_d_r, (0xEF, "ix", "e",), 3),
        0xA4 : (self._res_n_indx_d_r, (0xEF, "ix", "h",), 3),
        0xA5 : (self._res_n_indx_d_r, (0xEF, "ix", "l",), 3),
        0xA6 : (self._res_n_indx_d, (0xEF, "ix",), 3),
        0xA7 : (self._res_n_indx_d_r, (0xEF, "ix", "a",), 3),
        0xA8 : (self._res_n_indx_d_r, (0xDF, "ix", "b",), 3),
        0xA9 : (self._res_n_indx_d_r, (0xDF, "ix", "c",), 3),
        0xAA : (self._res_n_indx_d_r, (0xDF, "ix", "d",), 3),
        0xAB : (self._res_n_indx_d_r, (0xDF, "ix", "e",), 3),
        0xAC : (self._res_n_indx_d_r, (0xDF, "ix", "h",), 3),
        0xAD : (self._res_n_indx_d_r, (0xDF, "ix", "l",), 3),
        0xAE : (self._res_n_indx_d, (0xDF, "ix",), 3),
        0xAF : (self._res_n_indx_d_r, (0xDF, "ix", "a",), 3),

        0xB0 : (self._res_n_indx_d_r, (0xBF, "ix", "b",), 3),
        0xB1 : (self._res_n_indx_d_r, (0xBF, "ix", "c",), 3),
        0xB2 : (self._res_n_indx_d_r, (0xBF, "ix", "d",), 3),
        0xB3 : (self._res_n_indx_d_r, (0xBF, "ix", "e",), 3),
        0xB4 : (self._res_n_indx_d_r, (0xBF, "ix", "h",), 3),
        0xB5 : (self._res_n_indx_d_r, (0xBF, "ix", "l",), 3),
        0xB6 : (self._res_n_indx_d, (0xBF, "ix",), 3),
        0xB7 : (self._res_n_indx_d_r, (0xBF, "ix", "a",), 3),
        0xB8 : (self._res_n_indx_d_r, (0x7F, "ix", "b",), 3),
        0xB9 : (self._res_n_indx_d_r, (0x7F, "ix", "c",), 3),
        0xBA : (self._res_n_indx_d_r, (0x7F, "ix", "d",), 3),
        0xBB : (self._res_n_indx_d_r, (0x7F, "ix", "e",), 3),
        0xBC : (self._res_n_indx_d_r, (0x7F, "ix", "h",), 3),
        0xBD : (self._res_n_indx_d_r, (0x7F, "ix", "l",), 3),
        0xBE : (self._res_n_indx_d, (0x7F, "ix",), 3),
        0xBF : (self._res_n_indx_d_r, (0x7F, "ix", "a",), 3),

        0xC0 : (self._set_n_indx_d_r, (0x1, "ix", "b",), 3), 
        0xC1 : (self._set_n_indx_d_r, (0x1, "ix", "c",), 3), 
        0xC2 : (self._set_n_indx_d_r, (0x1, "ix", "d",), 3), 
        0xC3 : (self._set_n_indx_d_r, (0x1, "ix", "e",), 3), 
        0xC4 : (self._set_n_indx_d_r, (0x1, "ix", "h",), 3), 
        0xC5 : (self._set_n_indx_d_r, (0x1, "ix", "l",), 3), 
        0xC6 : (self._set_n_indx_d, (0x1, "ix",), 3), 
        0xC7 : (self._set_n_indx_d_r, (0x1, "ix", "a",), 3), 
        0xC8 : (self._set_n_indx_d_r, (0x2, "ix", "b",), 3), 
        0xC9 : (self._set_n_indx_d_r, (0x2, "ix", "c",), 3), 
        0xCA : (self._set_n_indx_d_r, (0x2, "ix", "d",), 3), 
        0xCB : (self._set_n_indx_d_r, (0x2, "ix", "e",), 3), 
        0xCC : (self._set_n_indx_d_r, (0x2, "ix", "h",), 3), 
        0xCD : (self._set_n_indx_d_r, (0x2, "ix", "l",), 3), 
        0xCE : (self._set_n_indx_d, (0x2, "ix",), 3), 
        0xCF : (self._set_n_indx_d_r, (0x2, "ix", "a",), 3), 

        0xD0 : (self._set_n_indx_d_r, (0x4, "ix", "b",), 3),
        0xD1 : (self._set_n_indx_d_r, (0x4, "ix", "c",), 3),
        0xD2 : (self._set_n_indx_d_r, (0x4, "ix", "d",), 3),
        0xD3 : (self._set_n_indx_d_r, (0x4, "ix", "e",), 3),
        0xD4 : (self._set_n_indx_d_r, (0x4, "ix", "h",), 3),
        0xD5 : (self._set_n_indx_d_r, (0x4, "ix", "l",), 3),
        0xD6 : (self._set_n_indx_d, (0x4, "ix",), 3),
        0xD7 : (self._set_n_indx_d_r, (0x4, "ix", "a",), 3),
        0xD8 : (self._set_n_indx_d_r, (0x8, "ix", "b",), 3),
        0xD9 : (self._set_n_indx_d_r, (0x8, "ix", "c",), 3),
        0xDA : (self._set_n_indx_d_r, (0x8, "ix", "d",), 3),
        0xDB : (self._set_n_indx_d_r, (0x8, "ix", "e",), 3),
        0xDC : (self._set_n_indx_d_r, (0x8, "ix", "h",), 3),
        0xDD : (self._set_n_indx_d_r, (0x8, "ix", "l",), 3),
        0xDE : (self._set_n_indx_d, (0x8, "ix",), 3),
        0xDF : (self._set_n_indx_d_r, (0x8, "ix", "a",), 3),

        0xE0 : (self._set_n_indx_d_r, (0x10, "ix", "b",), 3),
        0xE1 : (self._set_n_indx_d_r, (0x10, "ix", "c",), 3),
        0xE2 : (self._set_n_indx_d_r, (0x10, "ix", "d",), 3),
        0xE3 : (self._set_n_indx_d_r, (0x10, "ix", "e",), 3),
        0xE4 : (self._set_n_indx_d_r, (0x10, "ix", "h",), 3),
        0xE5 : (self._set_n_indx_d_r, (0x10, "ix", "l",), 3),
        0xE6 : (self._set_n_indx_d, (0x10, "ix",), 3),
        0xE7 : (self._set_n_indx_d_r, (0x10, "ix", "a",), 3),
        0xE8 : (self._set_n_indx_d_r, (0x20, "ix", "b",), 3),
        0xE9 : (self._set_n_indx_d_r, (0x20, "ix", "c",), 3),
        0xEA : (self._set_n_indx_d_r, (0x20, "ix", "d",), 3),
        0xEB : (self._set_n_indx_d_r, (0x20, "ix", "e",), 3),
        0xEC : (self._set_n_indx_d_r, (0x20, "ix", "h",), 3),
        0xED : (self._set_n_indx_d_r, (0x20, "ix", "l",), 3),
        0xEE : (self._set_n_indx_d, (0x20, "ix",), 3),
        0xEF : (self._set_n_indx_d_r, (0x20, "ix", "a",), 3),

        0xF0 : (self._set_n_indx_d_r, (0x40, "ix", "b",), 3),
        0xF1 : (self._set_n_indx_d_r, (0x40, "ix", "c",), 3),
        0xF2 : (self._set_n_indx_d_r, (0x40, "ix", "d",), 3),
        0xF3 : (self._set_n_indx_d_r, (0x40, "ix", "e",), 3),
        0xF4 : (self._set_n_indx_d_r, (0x40, "ix", "h",), 3),
        0xF5 : (self._set_n_indx_d_r, (0x40, "ix", "l",), 3),
        0xF6 : (self._set_n_indx_d, (0x40, "ix",), 3),
        0xF7 : (self._set_n_indx_d_r, (0x40, "ix", "a",), 3),
        0xF8 : (self._set_n_indx_d_r, (0x80, "ix", "b",), 3),
        0xF9 : (self._set_n_indx_d_r, (0x80, "ix", "c",), 3),
        0xFA : (self._set_n_indx_d_r, (0x80, "ix", "d",), 3),
        0xFB : (self._set_n_indx_d_r, (0x80, "ix", "e",), 3),
        0xFC : (self._set_n_indx_d_r, (0x80, "ix", "h",), 3),
        0xFD : (self._set_n_indx_d_r, (0x80, "ix", "l",), 3),
        0xFE : (self._set_n_indx_d, (0x80, "ix",), 3),
        0xFF : (self._set_n_indx_d_r, (0x80, "ix", "a",), 3),
        }

        self.dd_opcodes = {0x09 : (self._add_rr_rr, ("ix", "bc",), 1),

        0x19 : (self._add_rr_rr, ("ix", "de",), 1),

        0x21 : (self._ld_rr_nn, ("ix",), 3),
        0x22 : (self._ld_addr_nn_rr, ("ix",), 3),
        0x23 : (self._inc_rr, ("ix",), 1),
        0x24 : (self._inc_r, ("ixh",), 1),
        0x25 : (self._dec_r, ("ixh",), 1),
        0x26 : (self._ld_r_n, ("ixh",), 2),
        0x29 : (self._add_rr_rr, ("ix", "ix",), 1),
        0x2A : (self._ld_rr_addr_nn, ("ix",), 3),
        0x2B : (self._dec_rr, ("ix",), 1),
        0x2C : (self._inc_r, ("ixl",), 1),
        0x2D : (self._dec_r, ("ixl",), 1),
        0x2E : (self._ld_r_n, ("ixl",), 2),

        0x34 : (self._inc_addr_indx_d, ("ix",), 2),
        0x35 : (self._dec_addr_indx_d, ("ix",), 2),
        0x36 : (self._ld_addr_indx_d_n, ("ix",), 3),
        0x39 : (self._add_rr_rr, ("ix", "sp",), 1),

        0x44 : (self._ld_r_r, ("b", "ixh",), 1),
        0x45 : (self._ld_r_r, ("b", "ixl",), 1),
        0x46 : (self._ld_r_addr_indx_d, ("b", "ix",), 2),
        0x4C : (self._ld_r_r, ("c", "ixh",), 1),
        0x4D : (self._ld_r_r, ("c", "ixl",), 1),
        0x4E : (self._ld_r_addr_indx_d, ("c", "ix",), 2),

        0x54 : (self._ld_r_r, ("d", "ixh",), 1),
        0x55 : (self._ld_r_r, ("d", "ixl",), 1),
        0x56 : (self._ld_r_addr_indx_d, ("d", "ix",), 2),
        0x5C : (self._ld_r_r, ("e", "ixh",), 1),
        0x5D : (self._ld_r_r, ("e", "ixl",), 1),
        0x5E : (self._ld_r_addr_indx_d, ("e", "ix",), 2),

        0x60 : (self._ld_r_r, ("ixh", "b",), 1),
        0x61 : (self._ld_r_r, ("ixh", "c",), 1),
        0x62 : (self._ld_r_r, ("ixh", "d",), 1),
        0x63 : (self._ld_r_r, ("ixh", "e",), 1),
        0x64 : (self._ld_r_r, ("ixh", "ixh",), 1),
        0x65 : (self._ld_r_r, ("ixh", "ixl",), 1),
        0x66 : (self._ld_r_addr_indx_d, ("h", "ix",), 2),
        0x67 : (self._ld_r_r, ("ixh", "a",), 1),
        0x68 : (self._ld_r_r, ("ixl", "b",), 1),
        0x69 : (self._ld_r_r, ("ixl", "c",), 1),
        0x6A : (self._ld_r_r, ("ixl", "d",), 1),
        0x6B : (self._ld_r_r, ("ixl", "e",), 1),
        0x6C : (self._ld_r_r, ("ixl", "ixh",), 1),
        0x6D : (self._ld_r_r, ("ixl", "ixl",), 1),
        0x6E : (self._ld_r_addr_indx_d, ("l", "ix",), 2),
        0x6F : (self._ld_r_r, ("ixl", "a",), 1),

        0x70 : (self._ld_addr_indx_d_r, ("ix", "b",), 2), 
        0x71 : (self._ld_addr_indx_d_r, ("ix", "c",), 2), 
        0x72 : (self._ld_addr_indx_d_r, ("ix", "d",), 2), 
        0x73 : (self._ld_addr_indx_d_r, ("ix", "e",), 2), 
        0x74 : (self._ld_addr_indx_d_r, ("ix", "h",), 2), 
        0x75 : (self._ld_addr_indx_d_r, ("ix", "l",), 2), 
        0x77 : (self._ld_addr_indx_d_r, ("ix", "a",), 2), 
        0x7C : (self._ld_r_r, ("a", "ixh",), 1),
        0x7D : (self._ld_r_r, ("a", "ixl",), 1),
        0x7E : (self._ld_r_addr_indx_d, ("a", "ix",), 2),

        0x84 : (self._add_r_r, ("a", "ixh",), 1),
        0x85 : (self._add_r_r, ("a", "ixl",), 1),
        0x86 : (self._add_r_addr_indx_d, ("a", "ix",), 2),
        0x8C : (self._adc_r_r, ("a", "ixh"), 1),
        0x8D : (self._adc_r_r, ("a", "ixl"), 1),
        0x8E : (self._adc_r_addr_indx_d, ("a", "ix",), 2),

        0x94 : (self._sub_r, ("ixh",), 1),
        0x95 : (self._sub_r, ("ixl",), 1),
        0x96 : (self._sub_addr_indx_d, ("ix",), 2),
        0x9C : (self._sbc_r_r, ("a", "ixh",), 1),
        0x9D : (self._sbc_r_r, ("a", "ixl",), 1),
        0x9E : (self._sbc_r_addr_indx_d, ("a", "ix",), 2),

        0xA4 : (self._and_r, ("ixh",), 1),
        0xA5 : (self._and_r, ("ixl",), 1),
        0xA6 : (self._and_addr_indx_d, ("ix",), 2),
        0xAC : (self._xor_r, ("ixh",), 1),
        0xAD : (self._xor_r, ("ixl",), 1),
        0xAE : (self._xor_addr_indx_d, ("ix",), 2),

        0xB4 : (self._or_r, ("ixh",), 1),
        0xB5 : (self._or_r, ("ixl",), 1),
        0xB6 : (self._or_addr_indx_d, ("ix",), 2),
        0xBC : (self._cp_r, ("ixh",), 1),
        0xBD : (self._cp_r, ("ixl",), 1),
        0xBE : (self._cp_addr_indx_d, ("ix",), 2),

        0xCB : self.ddcb_opcodes,

        0xE1 : (self._pop_rr, ("ix",), 1),
        0xE3 : (self._ex_addr_sp_rr, ("ix",), 1),
        0xE5 : (self._push_rr, ("ix",), 1),
        }

        self.ed_opcodes = {0x40 : (self._in_r_addr_r, ("b", "c",), 1),
        0x41 : (self._out_addr_r_r, ("c", "b",), 2),
        0x42 : (self._sbc_rr_rr, ("hl", "bc",), 1),
        0x43 : (self._ld_addr_nn_rr, ("bc",), 3),
        0x44 : (self._neg, (), 1),
        0x45 : (self._retn, (), 1),
        0x46 : (self._im, (0x0,), 1),
        0x47 : (self._ld_r_r, ("i", "a",), 1),
        0x48 : (self._in_r_addr_r, ("c", "c",), 1),
        0x49 : (self._out_addr_r_r, ("c", "c",), 2),
        0x4A : (self._adc_rr_rr, ("hl", "bc",), 1),
        0x4B : (self._ld_rr_addr_nn, ("bc",), 3),
        0x4C : (self._neg, (), 1),
        0x4D : (self._reti, (), 1),
        0x4E : (self._im, (0x0,), 1),
        0x4F : (self._ld_r_r, ("r", "a",), 1),

        0x50 : (self._in_r_addr_r, ("d", "c",), 1),
        0x51 : (self._out_addr_r_r, ("c", "d",), 2),
        0x52 : (self._sbc_rr_rr, ("hl", "de",), 1),
        0x53 : (self._ld_addr_nn_rr, ("de",), 3),
        0x54 : (self._neg, (), 1),
        0x55 : (self._retn, (), 1),
        0x56 : (self._im, (0x1,), 1),
        0x57 : (self._ld_r_r, ("a", "i",), 1),
        0x58 : (self._in_r_addr_r, ("e", "c",), 1),
        0x59 : (self._out_addr_r_r, ("c", "e",), 2),
        0x5A : (self._adc_rr_rr, ("hl", "de",), 1),
        0x5B : (self._ld_rr_addr_nn, ("de",), 3),
        0x5C : (self._neg, (), 1),
        0x5D : (self._retn, (), 1),
        0x5E : (self._im, (0x2,), 1),
        0x5F : (self._ld_r_r, ("a", "r",), 1),

        0x60 : (self._in_r_addr_r, ("h", "c",), 1),
        0x61 : (self._out_addr_r_r, ("c", "h",), 2),
        0x62 : (self._sbc_rr_rr, ("hl", "hl",), 1),
        0x63 : (self._ld_addr_nn_rr, ("hl",), 3),
        0x64 : (self._neg, (), 1),
        0x65 : (self._retn, (), 1),
        0x66 : (self._im, (0x0,), 1),
        0x67 : (self._rrd, (), 1),
        0x68 : (self._in_r_addr_r, ("l", "c",), 1),
        0x69 : (self._out_addr_r_r, ("c", "l",), 2),
        0x6A : (self._adc_rr_rr, ("hl", "hl",), 1),
        0x6B : (self._ld_rr_addr_nn, ("hl",), 3),
        0x6C : (self._neg, (), 1),
        0x6D : (self._retn, (), 1),
        0x6E : (self._im, (0x0,), 1),
        0x6F : (self._rld, (), 1),

        0x70 : (self._in_r_addr_r, ("f", "c",), 1),
        0x71 : (self._out_addr_r_n, ("c", 0,), 2),
        0x72 : (self._sbc_rr_rr, ("hl", "sp",), 1),
        0x73 : (self._ld_addr_nn_rr, ("sp",), 3),
        0x74 : (self._neg, (), 1),
        0x75 : (self._retn, (), 1),
        0x76 : (self._im, (0x1,), 1),
        0x78 : (self._in_r_addr_r, ("a", "c",), 1),
        0x79 : (self._out_addr_r_r, ("c", "a",), 2),
        0x7A : (self._adc_rr_rr, ("hl", "sp",), 1),
        0x7B : (self._ld_rr_addr_nn, ("sp",), 3),
        0x7C : (self._neg, (), 1),
        0x7D : (self._retn, (), 1),
        0x7E : (self._im, (0x2,), 1),

        0xA0 : (self._ldi, (), 1),
        0xA1 : (self._cpi, (), 1),
        0xA2 : (self._ini, (), 1),
        0xA3 : (self._outi, (), 1),
        0xA8 : (self._ldd, (), 1), # Test
        0xA9 : (self._cpd, (), 1), # Test
        0xAA : (self._ind, (), 1), # Test
        0xAB : (self._outd, (), 1), # Test

        0xB0 : (self._ldir, (), 1), # Test
        0xB1 : (self._cpir, (), 1), # Test
        0xB2 : (self._inir, (), 1), # Test
        0xB3 : (self._otir, (), 1), # Test
        0xB8 : (self._lddr, (), 1), # Test
        0xB9 : (self._cpdr, (), 1), # Impl.
        0xBA : (self._indr, (), 1), # Impl.
        0xBB : (self._otdr, (), 1), # Impl.
        }

        self.fdcb_opcodes = {0x0 : (self._rlc_indx_d_r, ("iy", "b",), 3),
        0x01 : (self._rlc_indx_d_r, ("iy", "c",), 3), 
        0x02 : (self._rlc_indx_d_r, ("iy", "d",), 3), 
        0x03 : (self._rlc_indx_d_r, ("iy", "e",), 3), 
        0x04 : (self._rlc_indx_d_r, ("iy", "h",), 3), 
        0x05 : (self._rlc_indx_d_r, ("iy", "l",), 3), 
        0x06 : (self._rlc_indx_d, ("iy",), 3), 
        0x07 : (self._rlc_indx_d_r, ("iy", "a",), 3), 
        0x08 : (self._rrc_indx_d_r, ("iy", "b",), 3), 
        0x09 : (self._rrc_indx_d_r, ("iy", "c",), 3), 
        0x0A : (self._rrc_indx_d_r, ("iy", "d",), 3), 
        0x0B : (self._rrc_indx_d_r, ("iy", "e",), 3), 
        0x0C : (self._rrc_indx_d_r, ("iy", "h",), 3), 
        0x0D : (self._rrc_indx_d_r, ("iy", "l",), 3), 
        0x0E : (self._rrc_indx_d, ("iy",), 3),
        0x0F : (self._rrc_indx_d_r, ("iy", "a",), 3), 
        
        0x10 : (self._rl_indx_d_r, ("iy", "b",), 3), 
        0X11 : (self._rl_indx_d_r, ("iy", "c",), 3), 
        0x12 : (self._rl_indx_d_r, ("iy", "d",), 3), 
        0x13 : (self._rl_indx_d_r, ("iy", "e",), 3), 
        0x14 : (self._rl_indx_d_r, ("iy", "h",), 3), 
        0x15 : (self._rl_indx_d_r, ("iy", "l",), 3), 
        0x16 : (self._rl_indx_d, ("iy",), 3),
        0x17 : (self._rl_indx_d_r, ("iy", "a",), 3), 
        0x18 : (self._rr_indx_d_r, ("iy", "b",), 3), 
        0x19 : (self._rr_indx_d_r, ("iy", "c",), 3), 
        0x1A : (self._rr_indx_d_r, ("iy", "d",), 3), 
        0x1B : (self._rr_indx_d_r, ("iy", "e",), 3), 
        0x1C : (self._rr_indx_d_r, ("iy", "h",), 3), 
        0x1D : (self._rr_indx_d_r, ("iy", "l",), 3), 
        0x1E : (self._rr_indx_d, ("iy",), 3), 
        0x1F : (self._rr_indx_d_r, ("iy", "a",), 3),

        0x20 : (self._sla_indx_d_r, ("iy", "b",), 3), 
        0x21 : (self._sla_indx_d_r, ("iy", "c",), 3), 
        0x22 : (self._sla_indx_d_r, ("iy", "d",), 3), 
        0x23 : (self._sla_indx_d_r, ("iy", "e",), 3), 
        0x24 : (self._sla_indx_d_r, ("iy", "h",), 3), 
        0x25 : (self._sla_indx_d_r, ("iy", "l",), 3), 
        0x26 : (self._sla_indx_d, ("iy",), 3), 
        0x27 : (self._sla_indx_d_r, ("iy", "a",), 3), 
        0x28 : (self._sra_indx_d_r, ("iy", "b",), 3), 
        0x29 : (self._sra_indx_d_r, ("iy", "c",), 3), 
        0x2A : (self._sra_indx_d_r, ("iy", "d",), 3), 
        0x2B : (self._sra_indx_d_r, ("iy", "e",), 3), 
        0x2C : (self._sra_indx_d_r, ("iy", "h",), 3), 
        0x2D : (self._sra_indx_d_r, ("iy", "l",), 3), 
        0x2E : (self._sra_indx_d, ("iy",), 3), 
        0x2F : (self._sra_indx_d_r, ("iy", "a",), 3), 

        0x30 : (self._sll_indx_d_r, ("iy", "b",), 3), 
        0x31 : (self._sll_indx_d_r, ("iy", "c",), 3), 
        0x32 : (self._sll_indx_d_r, ("iy", "d",), 3), 
        0x33 : (self._sll_indx_d_r, ("iy", "e",), 3), 
        0x34 : (self._sll_indx_d_r, ("iy", "h",), 3), 
        0x35 : (self._sll_indx_d_r, ("iy", "l",), 3), 
        0x36 : (self._sll_indx_d, ("iy",), 3), 
        0x37 : (self._sll_indx_d_r, ("iy", "a",), 3), 
        0x38 : (self._srl_indx_d_r, ("iy", "b",), 3), 
        0x39 : (self._srl_indx_d_r, ("iy", "c",), 3), 
        0x3A : (self._srl_indx_d_r, ("iy", "d",), 3), 
        0x3B : (self._srl_indx_d_r, ("iy", "e",), 3), 
        0x3C : (self._srl_indx_d_r, ("iy", "h",), 3), 
        0x3D : (self._srl_indx_d_r, ("iy", "l",), 3), 
        0x3E : (self._srl_indx_d, ("iy",), 3), 
        0x3F : (self._srl_indx_d_r, ("iy", "a",), 3), 

        0x40 : (self._bit_n_indx_d, (0x1, "iy",), 3), 
        0x41 : (self._bit_n_indx_d, (0x1, "iy",), 3), 
        0x42 : (self._bit_n_indx_d, (0x1, "iy",), 3), 
        0x43 : (self._bit_n_indx_d, (0x1, "iy",), 3), 
        0x44 : (self._bit_n_indx_d, (0x1, "iy",), 3), 
        0x45 : (self._bit_n_indx_d, (0x1, "iy",), 3), 
        0x46 : (self._bit_n_indx_d, (0x1, "iy",), 3), 
        0x47 : (self._bit_n_indx_d, (0x1, "iy",), 3), 
        0x48 : (self._bit_n_indx_d, (0x2, "iy",), 3), 
        0x49 : (self._bit_n_indx_d, (0x2, "iy",), 3), 
        0x4A : (self._bit_n_indx_d, (0x2, "iy",), 3), 
        0x4B : (self._bit_n_indx_d, (0x2, "iy",), 3), 
        0x4C : (self._bit_n_indx_d, (0x2, "iy",), 3), 
        0x4D : (self._bit_n_indx_d, (0x2, "iy",), 3), 
        0x4E : (self._bit_n_indx_d, (0x2, "iy",), 3), 
        0x4F : (self._bit_n_indx_d, (0x2, "iy",), 3), 

        0x50 : (self._bit_n_indx_d, (0x4, "iy",), 3), 
        0x51 : (self._bit_n_indx_d, (0x4, "iy",), 3), 
        0x52 : (self._bit_n_indx_d, (0x4, "iy",), 3), 
        0x53 : (self._bit_n_indx_d, (0x4, "iy",), 3), 
        0x54 : (self._bit_n_indx_d, (0x4, "iy",), 3), 
        0x55 : (self._bit_n_indx_d, (0x4, "iy",), 3), 
        0x56 : (self._bit_n_indx_d, (0x4, "iy",), 3), 
        0x57 : (self._bit_n_indx_d, (0x4, "iy",), 3), 
        0x58 : (self._bit_n_indx_d, (0x8, "iy",), 3), 
        0x59 : (self._bit_n_indx_d, (0x8, "iy",), 3), 
        0x5A : (self._bit_n_indx_d, (0x8, "iy",), 3), 
        0x5B : (self._bit_n_indx_d, (0x8, "iy",), 3), 
        0x5C : (self._bit_n_indx_d, (0x8, "iy",), 3), 
        0x5D : (self._bit_n_indx_d, (0x8, "iy",), 3), 
        0x5E : (self._bit_n_indx_d, (0x8, "iy",), 3), 
        0x5F : (self._bit_n_indx_d, (0x8, "iy",), 3), 

        0x60 : (self._bit_n_indx_d, (0x10, "iy",), 3),
        0x61 : (self._bit_n_indx_d, (0x10, "iy",), 3),
        0x62 : (self._bit_n_indx_d, (0x10, "iy",), 3),
        0x63 : (self._bit_n_indx_d, (0x10, "iy",), 3),
        0x64 : (self._bit_n_indx_d, (0x10, "iy",), 3),
        0x65 : (self._bit_n_indx_d, (0x10, "iy",), 3),
        0x66 : (self._bit_n_indx_d, (0x10, "iy",), 3),
        0x67 : (self._bit_n_indx_d, (0x10, "iy",), 3),
        0x68 : (self._bit_n_indx_d, (0x20, "iy",), 3),
        0x69 : (self._bit_n_indx_d, (0x20, "iy",), 3),
        0x6A : (self._bit_n_indx_d, (0x20, "iy",), 3),
        0x6B : (self._bit_n_indx_d, (0x20, "iy",), 3),
        0x6C : (self._bit_n_indx_d, (0x20, "iy",), 3),
        0x6D : (self._bit_n_indx_d, (0x20, "iy",), 3),
        0x6E : (self._bit_n_indx_d, (0x20, "iy",), 3),
        0x6F : (self._bit_n_indx_d, (0x20, "iy",), 3),
        
        0x70 : (self._bit_n_indx_d, (0x40, "iy",), 3),
        0x71 : (self._bit_n_indx_d, (0x40, "iy",), 3),
        0x72 : (self._bit_n_indx_d, (0x40, "iy",), 3),
        0x73 : (self._bit_n_indx_d, (0x40, "iy",), 3),
        0x74 : (self._bit_n_indx_d, (0x40, "iy",), 3),
        0x75 : (self._bit_n_indx_d, (0x40, "iy",), 3),
        0x76 : (self._bit_n_indx_d, (0x40, "iy",), 3),
        0x77 : (self._bit_n_indx_d, (0x40, "iy",), 3),
        0x78 : (self._bit_n_indx_d, (0x80, "iy",), 3),
        0x79 : (self._bit_n_indx_d, (0x80, "iy",), 3),
        0x7A : (self._bit_n_indx_d, (0x80, "iy",), 3),
        0x7B : (self._bit_n_indx_d, (0x80, "iy",), 3),
        0x7C : (self._bit_n_indx_d, (0x80, "iy",), 3),
        0x7D : (self._bit_n_indx_d, (0x80, "iy",), 3),
        0x7E : (self._bit_n_indx_d, (0x80, "iy",), 3),
        0x7F : (self._bit_n_indx_d, (0x80, "iy",), 3),

        0x80 : (self._res_n_indx_d_r, (0xFE, "iy", "b",), 3), 
        0x81 : (self._res_n_indx_d_r, (0xFE, "iy", "c",), 3), 
        0x82 : (self._res_n_indx_d_r, (0xFE, "iy", "d",), 3), 
        0x83 : (self._res_n_indx_d_r, (0xFE, "iy", "e",), 3), 
        0x84 : (self._res_n_indx_d_r, (0xFE, "iy", "h",), 3), 
        0x85 : (self._res_n_indx_d_r, (0xFE, "iy", "l",), 3), 
        0x86 : (self._res_n_indx_d, (0xFE, "iy",), 3), 
        0x87 : (self._res_n_indx_d_r, (0xFE, "iy", "a",), 3), 
        0x88 : (self._res_n_indx_d_r, (0xFD, "iy", "b",), 3), 
        0x89 : (self._res_n_indx_d_r, (0xFD, "iy", "c",), 3), 
        0x8A : (self._res_n_indx_d_r, (0xFD, "iy", "d",), 3), 
        0x8B : (self._res_n_indx_d_r, (0xFD, "iy", "e",), 3), 
        0x8C : (self._res_n_indx_d_r, (0xFD, "iy", "h",), 3), 
        0x8D : (self._res_n_indx_d_r, (0xFD, "iy", "l",), 3), 
        0x8E : (self._res_n_indx_d, (0xFD, "iy",), 3), 
        0x8F : (self._res_n_indx_d_r, (0xFD, "iy", "a",), 3), 

        0x90 : (self._res_n_indx_d_r, (0xFB, "iy", "b",), 3),
        0x91 : (self._res_n_indx_d_r, (0xFB, "iy", "c",), 3),
        0x92 : (self._res_n_indx_d_r, (0xFB, "iy", "d",), 3),
        0x93 : (self._res_n_indx_d_r, (0xFB, "iy", "e",), 3),
        0x94 : (self._res_n_indx_d_r, (0xFB, "iy", "h",), 3),
        0x95 : (self._res_n_indx_d_r, (0xFB, "iy", "l",), 3),
        0x96 : (self._res_n_indx_d, (0xFB, "iy",), 3),
        0x97 : (self._res_n_indx_d_r, (0xFB, "iy", "a",), 3),
        0x98 : (self._res_n_indx_d_r, (0xF7, "iy", "b",), 3),
        0x99 : (self._res_n_indx_d_r, (0xF7, "iy", "c",), 3),
        0x9A : (self._res_n_indx_d_r, (0xF7, "iy", "d",), 3),
        0x9B : (self._res_n_indx_d_r, (0xF7, "iy", "e",), 3),
        0x9C : (self._res_n_indx_d_r, (0xF7, "iy", "h",), 3),
        0x9D : (self._res_n_indx_d_r, (0xF7, "iy", "l",), 3),
        0x9E : (self._res_n_indx_d, (0xF7, "iy",), 3),
        0x9F : (self._res_n_indx_d_r, (0xF7, "iy", "a",), 3),
        
        0xA0 : (self._res_n_indx_d_r, (0xEF, "iy", "b",), 3),
        0xA1 : (self._res_n_indx_d_r, (0xEF, "iy", "c",), 3),
        0xA2 : (self._res_n_indx_d_r, (0xEF, "iy", "d",), 3),
        0xA3 : (self._res_n_indx_d_r, (0xEF, "iy", "e",), 3),
        0xA4 : (self._res_n_indx_d_r, (0xEF, "iy", "h",), 3),
        0xA5 : (self._res_n_indx_d_r, (0xEF, "iy", "l",), 3),
        0xA6 : (self._res_n_indx_d, (0xEF, "iy",), 3),
        0xA7 : (self._res_n_indx_d_r, (0xEF, "iy", "a",), 3),
        0xA8 : (self._res_n_indx_d_r, (0xDF, "iy", "b",), 3),
        0xA9 : (self._res_n_indx_d_r, (0xDF, "iy", "c",), 3),
        0xAA : (self._res_n_indx_d_r, (0xDF, "iy", "d",), 3),
        0xAB : (self._res_n_indx_d_r, (0xDF, "iy", "e",), 3),
        0xAC : (self._res_n_indx_d_r, (0xDF, "iy", "h",), 3),
        0xAD : (self._res_n_indx_d_r, (0xDF, "iy", "l",), 3),
        0xAE : (self._res_n_indx_d, (0xDF, "iy",), 3),
        0xAF : (self._res_n_indx_d_r, (0xDF, "iy", "a",), 3),

        0xB0 : (self._res_n_indx_d_r, (0xBF, "iy", "b",), 3),
        0xB1 : (self._res_n_indx_d_r, (0xBF, "iy", "c",), 3),
        0xB2 : (self._res_n_indx_d_r, (0xBF, "iy", "d",), 3),
        0xB3 : (self._res_n_indx_d_r, (0xBF, "iy", "e",), 3),
        0xB4 : (self._res_n_indx_d_r, (0xBF, "iy", "h",), 3),
        0xB5 : (self._res_n_indx_d_r, (0xBF, "iy", "l",), 3),
        0xB6 : (self._res_n_indx_d, (0xBF, "iy",), 3),
        0xB7 : (self._res_n_indx_d_r, (0xBF, "iy", "a",), 3),
        0xB8 : (self._res_n_indx_d_r, (0x7F, "iy", "b",), 3),
        0xB9 : (self._res_n_indx_d_r, (0x7F, "iy", "c",), 3),
        0xBA : (self._res_n_indx_d_r, (0x7F, "iy", "d",), 3),
        0xBB : (self._res_n_indx_d_r, (0x7F, "iy", "e",), 3),
        0xBC : (self._res_n_indx_d_r, (0x7F, "iy", "h",), 3),
        0xBD : (self._res_n_indx_d_r, (0x7F, "iy", "l",), 3),
        0xBE : (self._res_n_indx_d, (0x7F, "iy",), 3),
        0xBF : (self._res_n_indx_d_r, (0x7F, "iy", "a",), 3),

        0xC0 : (self._set_n_indx_d_r, (0x1, "iy", "b",), 3), 
        0xC1 : (self._set_n_indx_d_r, (0x1, "iy", "c",), 3), 
        0xC2 : (self._set_n_indx_d_r, (0x1, "iy", "d",), 3), 
        0xC3 : (self._set_n_indx_d_r, (0x1, "iy", "e",), 3), 
        0xC4 : (self._set_n_indx_d_r, (0x1, "iy", "h",), 3), 
        0xC5 : (self._set_n_indx_d_r, (0x1, "iy", "l",), 3), 
        0xC6 : (self._set_n_indx_d, (0x1, "iy",), 3), 
        0xC7 : (self._set_n_indx_d_r, (0x1, "iy", "a",), 3), 
        0xC8 : (self._set_n_indx_d_r, (0x2, "iy", "b",), 3), 
        0xC9 : (self._set_n_indx_d_r, (0x2, "iy", "c",), 3), 
        0xCA : (self._set_n_indx_d_r, (0x2, "iy", "d",), 3), 
        0xCB : (self._set_n_indx_d_r, (0x2, "iy", "e",), 3), 
        0xCC : (self._set_n_indx_d_r, (0x2, "iy", "h",), 3), 
        0xCD : (self._set_n_indx_d_r, (0x2, "iy", "l",), 3), 
        0xCE : (self._set_n_indx_d, (0x2, "iy",), 3), 
        0xCF : (self._set_n_indx_d_r, (0x2, "iy", "a",), 3), 

        0xD0 : (self._set_n_indx_d_r, (0x4, "iy", "b",), 3),
        0xD1 : (self._set_n_indx_d_r, (0x4, "iy", "c",), 3),
        0xD2 : (self._set_n_indx_d_r, (0x4, "iy", "d",), 3),
        0xD3 : (self._set_n_indx_d_r, (0x4, "iy", "e",), 3),
        0xD4 : (self._set_n_indx_d_r, (0x4, "iy", "h",), 3),
        0xD5 : (self._set_n_indx_d_r, (0x4, "iy", "l",), 3),
        0xD6 : (self._set_n_indx_d, (0x4, "iy",), 3),
        0xD7 : (self._set_n_indx_d_r, (0x4, "iy", "a",), 3),
        0xD8 : (self._set_n_indx_d_r, (0x8, "iy", "b",), 3),
        0xD9 : (self._set_n_indx_d_r, (0x8, "iy", "c",), 3),
        0xDA : (self._set_n_indx_d_r, (0x8, "iy", "d",), 3),
        0xDB : (self._set_n_indx_d_r, (0x8, "iy", "e",), 3),
        0xDC : (self._set_n_indx_d_r, (0x8, "iy", "h",), 3),
        0xDD : (self._set_n_indx_d_r, (0x8, "iy", "l",), 3),
        0xDE : (self._set_n_indx_d, (0x8, "iy",), 3),
        0xDF : (self._set_n_indx_d_r, (0x8, "iy", "a",), 3),

        0xE0 : (self._set_n_indx_d_r, (0x10, "iy", "b",), 3),
        0xE1 : (self._set_n_indx_d_r, (0x10, "iy", "c",), 3),
        0xE2 : (self._set_n_indx_d_r, (0x10, "iy", "d",), 3),
        0xE3 : (self._set_n_indx_d_r, (0x10, "iy", "e",), 3),
        0xE4 : (self._set_n_indx_d_r, (0x10, "iy", "h",), 3),
        0xE5 : (self._set_n_indx_d_r, (0x10, "iy", "l",), 3),
        0xE6 : (self._set_n_indx_d, (0x10, "iy",), 3),
        0xE7 : (self._set_n_indx_d_r, (0x10, "iy", "a",), 3),
        0xE8 : (self._set_n_indx_d_r, (0x20, "iy", "b",), 3),
        0xE9 : (self._set_n_indx_d_r, (0x20, "iy", "c",), 3),
        0xEA : (self._set_n_indx_d_r, (0x20, "iy", "d",), 3),
        0xEB : (self._set_n_indx_d_r, (0x20, "iy", "e",), 3),
        0xEC : (self._set_n_indx_d_r, (0x20, "iy", "h",), 3),
        0xED : (self._set_n_indx_d_r, (0x20, "iy", "l",), 3),
        0xEE : (self._set_n_indx_d, (0x20, "iy",), 3),
        0xEF : (self._set_n_indx_d_r, (0x20, "iy", "a",), 3),

        0xF0 : (self._set_n_indx_d_r, (0x40, "iy", "b",), 3),
        0xF1 : (self._set_n_indx_d_r, (0x40, "iy", "c",), 3),
        0xF2 : (self._set_n_indx_d_r, (0x40, "iy", "d",), 3),
        0xF3 : (self._set_n_indx_d_r, (0x40, "iy", "e",), 3),
        0xF4 : (self._set_n_indx_d_r, (0x40, "iy", "h",), 3),
        0xF5 : (self._set_n_indx_d_r, (0x40, "iy", "l",), 3),
        0xF6 : (self._set_n_indx_d, (0x40, "iy",), 3),
        0xF7 : (self._set_n_indx_d_r, (0x40, "iy", "a",), 3),
        0xF8 : (self._set_n_indx_d_r, (0x80, "iy", "b",), 3),
        0xF9 : (self._set_n_indx_d_r, (0x80, "iy", "c",), 3),
        0xFA : (self._set_n_indx_d_r, (0x80, "iy", "d",), 3),
        0xFB : (self._set_n_indx_d_r, (0x80, "iy", "e",), 3),
        0xFC : (self._set_n_indx_d_r, (0x80, "iy", "h",), 3),
        0xFD : (self._set_n_indx_d_r, (0x80, "iy", "l",), 3),
        0xFE : (self._set_n_indx_d, (0x80, "iy",), 3),
        0xFF : (self._set_n_indx_d_r, (0x80, "iy", "a",), 3),
        }

        self.fd_opcodes = {0x09 : (self._add_rr_rr, ("iy", "bc",), 1),

        0x19 : (self._add_rr_rr, ("iy", "de",), 1),

        0x21 : (self._ld_rr_nn, ("iy",), 3),
        0x22 : (self._ld_addr_nn_rr, ("iy",), 3),
        0x23 : (self._inc_rr, ("iy",), 1),
        0x24 : (self._inc_r, ("iyh",), 1),
        0x25 : (self._dec_r, ("iyh",), 1),
        0x26 : (self._ld_r_n, ("iyh",), 2),
        0x29 : (self._add_rr_rr, ("iy", "iy",), 1),
        0x2A : (self._ld_rr_addr_nn, ("iy",), 3),
        0x2B : (self._dec_rr, ("iy",), 1),
        0x2C : (self._inc_r, ("iyl",), 1),
        0x2D : (self._dec_r, ("iyl",), 1),
        0x2E : (self._ld_r_n, ("iyl",), 2),

        0x34 : (self._inc_addr_indx_d, ("iy",), 2),
        0x35 : (self._dec_addr_indx_d, ("iy",), 2),
        0x36 : (self._ld_addr_indx_d_n, ("iy",), 3),
        0x39 : (self._add_rr_rr, ("iy", "sp",), 1),

        0x44 : (self._ld_r_r, ("b", "iyh",), 1),
        0x45 : (self._ld_r_r, ("b", "iyl",), 1),
        0x46 : (self._ld_r_addr_indx_d, ("b", "iy",), 2),
        0x4C : (self._ld_r_r, ("c", "iyh",), 1),
        0x4D : (self._ld_r_r, ("c", "iyl",), 1),
        0x4E : (self._ld_r_addr_indx_d, ("c", "iy",), 2),

        0x54 : (self._ld_r_r, ("d", "iyh",), 1),
        0x55 : (self._ld_r_r, ("d", "iyl",), 1),
        0x56 : (self._ld_r_addr_indx_d, ("d", "iy",), 2),
        0x5C : (self._ld_r_r, ("e", "iyh",), 1),
        0x5D : (self._ld_r_r, ("e", "iyl",), 1),
        0x5E : (self._ld_r_addr_indx_d, ("e", "iy",), 2),

        0x60 : (self._ld_r_r, ("iyh", "b",), 1),
        0x61 : (self._ld_r_r, ("iyh", "c",), 1),
        0x62 : (self._ld_r_r, ("iyh", "d",), 1),
        0x63 : (self._ld_r_r, ("iyh", "e",), 1),
        0x64 : (self._ld_r_r, ("iyh", "iyh",), 1),
        0x65 : (self._ld_r_r, ("iyh", "iyl",), 1),
        0x66 : (self._ld_r_addr_indx_d, ("h", "iy",), 2),
        0x67 : (self._ld_r_r, ("iyh", "a",), 1),
        0x68 : (self._ld_r_r, ("iyl", "b",), 1),
        0x69 : (self._ld_r_r, ("iyl", "c",), 1),
        0x6A : (self._ld_r_r, ("iyl", "d",), 1),
        0x6B : (self._ld_r_r, ("iyl", "e",), 1),
        0x6C : (self._ld_r_r, ("iyl", "iyh",), 1),
        0x6D : (self._ld_r_r, ("iyl", "iyl",), 1),
        0x6E : (self._ld_r_addr_indx_d, ("l", "iy",), 2),
        0x6F : (self._ld_r_r, ("iyl", "a",), 1),

        0x70 : (self._ld_addr_indx_d_r, ("iy", "b",), 2), 
        0x71 : (self._ld_addr_indx_d_r, ("iy", "c",), 2), 
        0x72 : (self._ld_addr_indx_d_r, ("iy", "d",), 2), 
        0x73 : (self._ld_addr_indx_d_r, ("iy", "e",), 2), 
        0x74 : (self._ld_addr_indx_d_r, ("iy", "h",), 2), 
        0x75 : (self._ld_addr_indx_d_r, ("iy", "l",), 2), 
        0x77 : (self._ld_addr_indx_d_r, ("iy", "a",), 2), 
        0x7C : (self._ld_r_r, ("a", "iyh",), 1),
        0x7D : (self._ld_r_r, ("a", "iyl",), 1),
        0x7E : (self._ld_r_addr_indx_d, ("a", "iy",), 2),

        0x84 : (self._add_r_r, ("a", "iyh",), 1),
        0x85 : (self._add_r_r, ("a", "iyl",), 1),
        0x86 : (self._add_r_addr_indx_d, ("a", "iy",), 2),
        0x8C : (self._adc_r_r, ("a", "iyh"), 1),
        0x8D : (self._adc_r_r, ("a", "iyl"), 1),
        0x8E : (self._adc_r_addr_indx_d, ("a", "iy",), 2),

        0x94 : (self._sub_r, ("iyh",), 1),
        0x95 : (self._sub_r, ("iyl",), 1),
        0x96 : (self._sub_addr_indx_d, ("iy",), 2),
        0x9C : (self._sbc_r_r, ("a", "iyh",), 1),
        0x9D : (self._sbc_r_r, ("a", "iyl",), 1),
        0x9E : (self._sbc_r_addr_indx_d, ("a", "iy",), 2),

        0xA4 : (self._and_r, ("iyh",), 1),
        0xA5 : (self._and_r, ("iyl",), 1),
        0xA6 : (self._and_addr_indx_d, ("iy",), 2),
        0xAC : (self._xor_r, ("iyh",), 1),
        0xAD : (self._xor_r, ("iyl",), 1),
        0xAE : (self._xor_addr_indx_d, ("iy",), 2),

        0xB4 : (self._or_r, ("iyh",), 1),
        0xB5 : (self._or_r, ("iyl",), 1),
        0xB6 : (self._or_addr_indx_d, ("iy",), 2),
        0xBC : (self._cp_r, ("iyh",), 1),
        0xBD : (self._cp_r, ("iyl",), 1),
        0xBE : (self._cp_addr_indx_d, ("iy",), 2),

        0xCB : self.fdcb_opcodes,

        0xE1 : (self._pop_rr, ("iy",), 1),
        0xE3 : (self._ex_addr_sp_rr, ("iy",), 1),
        0xE5 : (self._push_rr, ("iy",), 1),
        0xE9 : None,
        
        0xF9 : (self._ld_rr_rr, ("sp", "hl",), 1)
        }

        self.unprefixed_opcodes = {0x0 : (self._nop, (), 1),
        0x01 : (self._ld_rr_nn, ("bc",), 3),
        0x02 : (self._ld_addr_rr_r, ("bc", "a",), 1),
        0x03 : (self._inc_rr, ("bc",), 1),
        0x04 : (self._inc_r, ("b",), 1),
        0x05 : (self._dec_r, ("b",), 1),
        0x06 : (self._ld_r_n, ("b",), 2),
        0x07 : (self._rlca, (), 1),
        0x08 : (self._ex_rr_rr_, ("af", "af",), 1),
        0x09 : (self._add_rr_rr, ("hl", "bc",), 1),
        0x0A : (self._ld_r_addr_rr, ("a", "bc",), 1),
        0x0B : (self._dec_rr, ("bc",), 1),
        0x0C : (self._inc_r, ("c",), 1),
        0x0D : (self._dec_r, ("c",), 1),
        0x0E : (self._ld_r_n, ("c",), 2),
        0x0F : (self._rrca, (), 1),
        
        0x10 : (self._djnz, (), 2),
        0X11 : (self._ld_rr_nn, ("de",), 3),
        0x12 : (self._ld_addr_rr_r, ("de", "a",), 1),
        0x13 : (self._inc_rr, ("de",), 1),
        0x14 : (self._inc_r, ("d",), 1),
        0x15 : (self._dec_r, ("d",), 1),
        0x16 : (self._ld_r_n, ("d",), 2),
        0x17 : (self._rla, (), 1),
        0x18 : (self._jr_cc, (self._dummy_true,), 0),
        0x19 : (self._add_rr_rr, ("hl", "de",), 1),
        0x1A : (self._ld_r_addr_rr, ("a", "de",), 1),
        0x1B : (self._dec_rr, ("de",), 1),
        0x1C : (self._inc_r, ("e",), 1),
        0x1D : (self._dec_r, ("e",), 1),
        0x1E : (self._ld_r_n, ("e",), 2),
        0x1F : (self._rra, (), 1),

        0x20 : (self._jr_not_cc, (self._test_zero_flag,), 0),
        0x21 : (self._ld_rr_nn, ("hl",), 3),
        0x22 : (self._ld_addr_nn_rr, ("hl",), 3),
        0x23 : (self._inc_rr, ("hl",), 1),
        0x24 : (self._inc_r, ("h",), 1),
        0x25 : (self._dec_r, ("h",), 1),
        0x26 : (self._ld_r_n, ("h",), 2),
        0x27 : (self._daa, (), 1),
        0x28 : (self._jr_cc, (self._test_zero_flag,), 0),
        0x29 : (self._add_rr_rr, ("hl", "hl",), 1),
        0x2A : (self._ld_rr_addr_nn, ("hl",), 3),
        0x2B : (self._dec_rr, ("hl",), 1),
        0x2C : (self._inc_r, ("l",), 1),
        0x2D : (self._dec_r, ("l",), 1),
        0x2E : (self._ld_r_n, ("l",), 2),
        0x2F : (self._cpl, (), 1),

        0x30 : (self._jr_not_cc, (self._test_carry_flag,), 0),
        0x31 : (self._ld_rr_nn, ("sp",), 3),
        0x32 : (self._ld_addr_nn_r, ("a",), 3),
        0x33 : (self._inc_rr, ("sp",), 1),
        0x34 : (self._inc_addr_rr, ("hl",), 1),
        0x35 : (self._dec_addr_rr, ("hl",), 1),
        0x36 : (self._ld_addr_rr_n, ("hl",), 2),
        0x37 : (self._scf, (), 1),
        0x38 : (self._jr_cc, (self._test_carry_flag,), 0),
        0x39 : (self._add_rr_rr, ("hl", "sp",), 1),
        0x3A : (self._ld_r_addr_nn, ("a",), 3),
        0x3B : (self._dec_rr, ("sp",), 1),
        0x3C : (self._inc_r, ("a",), 1),
        0x3D : (self._dec_r, ("a",), 1),
        0x3E : (self._ld_r_n, ("a",), 2),
        0x3F : (self._ccf, (), 1),

        0x40 : (self._ld_r_r, ("b", "b",), 1),
        0x41 : (self._ld_r_r, ("b", "c",), 1),
        0x42 : (self._ld_r_r, ("b", "d",), 1),
        0x43 : (self._ld_r_r, ("b", "e",), 1),
        0x44 : (self._ld_r_r, ("b", "h",), 1),
        0x45 : (self._ld_r_r, ("b", "l",), 1),
        0x46 : (self._ld_r_addr_rr, ("b", "hl",), 1),
        0x47 : (self._ld_r_r, ("b", "a",), 1),
        0x48 : (self._ld_r_r, ("c", "b",), 1),
        0x49 : (self._ld_r_r, ("c", "c",), 1),
        0x4A : (self._ld_r_r, ("c", "d",), 1),
        0x4B : (self._ld_r_r, ("c", "e",), 1),
        0x4C : (self._ld_r_r, ("c", "h",), 1),
        0x4D : (self._ld_r_r, ("c", "l",), 1),
        0x4E : (self._ld_r_addr_rr, ("c", "hl",), 1),
        0x4F : (self._ld_r_r, ("c", "a",), 1),

        0x50 : (self._ld_r_r, ("d", "b",), 1),
        0x51 : (self._ld_r_r, ("d", "c",), 1),
        0x52 : (self._ld_r_r, ("d", "d",), 1),
        0x53 : (self._ld_r_r, ("d", "e",), 1),
        0x54 : (self._ld_r_r, ("d", "h",), 1),
        0x55 : (self._ld_r_r, ("d", "l",), 1),
        0x56 : (self._ld_r_addr_rr, ("d", "hl",), 1),
        0x57 : (self._ld_r_r, ("d", "a",), 1),
        0x58 : (self._ld_r_r, ("e", "b",), 1),
        0x59 : (self._ld_r_r, ("e", "c",), 1),
        0x5A : (self._ld_r_r, ("e", "d",), 1),
        0x5B : (self._ld_r_r, ("e", "e",), 1),
        0x5C : (self._ld_r_r, ("e", "h",), 1),
        0x5D : (self._ld_r_r, ("e", "l",), 1),
        0x5E : (self._ld_r_addr_rr, ("e", "hl",), 1),
        0x5F : (self._ld_r_r, ("e", "a",), 1),

        0x60 : (self._ld_r_r, ("h", "b",), 1),
        0x61 : (self._ld_r_r, ("h", "c",), 1),
        0x62 : (self._ld_r_r, ("h", "d",), 1),
        0x63 : (self._ld_r_r, ("h", "e",), 1),
        0x64 : (self._ld_r_r, ("h", "h",), 1),
        0x65 : (self._ld_r_r, ("h", "l",), 1),
        0x66 : (self._ld_r_addr_rr, ("h", "hl",), 1),
        0x67 : (self._ld_r_r, ("h", "a",), 1),
        0x68 : (self._ld_r_r, ("l", "b",), 1),
        0x69 : (self._ld_r_r, ("l", "c",), 1),
        0x6A : (self._ld_r_r, ("l", "d",), 1),
        0x6B : (self._ld_r_r, ("l", "e",), 1),
        0x6C : (self._ld_r_r, ("l", "h",), 1),
        0x6D : (self._ld_r_r, ("l", "l",), 1),
        0x6E : (self._ld_r_addr_rr, ("l", "hl",), 1),
        0x6F : (self._ld_r_r, ("l", "a",), 1),
        
        0x70 : (self._ld_addr_rr_r, ("hl", "b",), 1),
        0x71 : (self._ld_addr_rr_r, ("hl", "c",), 1),
        0x72 : (self._ld_addr_rr_r, ("hl", "d",), 1),
        0x73 : (self._ld_addr_rr_r, ("hl", "e",), 1),
        0x74 : (self._ld_addr_rr_r, ("hl", "h",), 1),
        0x75 : (self._ld_addr_rr_r, ("hl", "l",), 1),
        0x76 : (self._halt, ()),
        0x77 : (self._ld_addr_rr_r, ("hl", "a",), 1),
        0x78 : (self._ld_r_r, ("a", "b",), 1),
        0x79 : (self._ld_r_r, ("a", "c",), 1),
        0x7A : (self._ld_r_r, ("a", "d",), 1),
        0x7B : (self._ld_r_r, ("a", "e",), 1),
        0x7C : (self._ld_r_r, ("a", "h",), 1),
        0x7D : (self._ld_r_r, ("a", "l",), 1),
        0x7E : (self._ld_r_addr_rr, ("a", "hl",), 1),
        0x7F : (self._ld_r_r, ("a", "a",), 1),

        0x80 : (self._add_r_r, ("a", "b",), 1), 
        0x81 : (self._add_r_r, ("a", "c",), 1), 
        0x82 : (self._add_r_r, ("a", "d",), 1), 
        0x83 : (self._add_r_r, ("a", "e",), 1), 
        0x84 : (self._add_r_r, ("a", "h",), 1), 
        0x85 : (self._add_r_r, ("a", "l",), 1), 
        0x86 : (self._add_r_addr_rr, ("a", "hl",), 1),
        0x87 : (self._add_r_r, ("a", "a",), 1),
        0x88 : (self._adc_r_r, ("a", "b",), 1), 
        0x89 : (self._adc_r_r, ("a", "c",), 1), 
        0x8A : (self._adc_r_r, ("a", "d",), 1), 
        0x8B : (self._adc_r_r, ("a", "e",), 1), 
        0x8C : (self._adc_r_r, ("a", "h",), 1), 
        0x8D : (self._adc_r_r, ("a", "l",), 1), 
        0x8E : (self._adc_r_addr_rr, ("a", "hl",), 1), 
        0x8F : (self._adc_r_r, ("a", "a",), 1),

        0x90 : (self._sub_r, ("b",), 1), 
        0x91 : (self._sub_r, ("c",), 1),
        0x92 : (self._sub_r, ("d",), 1),
        0x93 : (self._sub_r, ("e",), 1),
        0x94 : (self._sub_r, ("h",), 1),
        0x95 : (self._sub_r, ("l",), 1),
        0x96 : (self._sub_addr_rr, ("hl",), 1),
        0x97 : (self._sub_r, ("a",), 1),
        0x98 : (self._sbc_r_r, ("a", "b",), 1),
        0x99 : (self._sbc_r_r, ("a", "c",), 1),
        0x9A : (self._sbc_r_r, ("a", "d",), 1),
        0x9B : (self._sbc_r_r, ("a", "e",), 1),
        0x9C : (self._sbc_r_r, ("a", "h",), 1),
        0x9D : (self._sbc_r_r, ("a", "l",), 1),
        0x9E : (self._sbc_r_addr_rr, ("a", "hl",), 1),
        0x9F : (self._sbc_r_r, ("a", "a",), 1),
        
        0xA0 : (self._and_r, ("b",), 1),      
        0xA1 : (self._and_r, ("c",), 1),      
        0xA2 : (self._and_r, ("d",), 1),      
        0xA3 : (self._and_r, ("e",), 1),      
        0xA4 : (self._and_r, ("h",), 1),      
        0xA5 : (self._and_r, ("l",), 1),      
        0xA6 : (self._and_addr_rr, ("hl",), 1),      
        0xA7 : (self._and_r, ("a",), 1),      
        0xA8 : (self._xor_r, ("b",), 1),      
        0xA9 : (self._xor_r, ("c",), 1),      
        0xAA : (self._xor_r, ("d",), 1),      
        0xAB : (self._xor_r, ("e",), 1),      
        0xAC : (self._xor_r, ("h",), 1),      
        0xAD : (self._xor_r, ("l",), 1),      
        0xAE : (self._xor_addr_rr, ("hl",), 1),      
        0xAF : (self._xor_r, ("a",), 1),

        0xB0 : (self._or_r, ("b",), 1),
        0xB1 : (self._or_r, ("c",), 1),
        0xB2 : (self._or_r, ("d",), 1),
        0xB3 : (self._or_r, ("e",), 1),
        0xB4 : (self._or_r, ("h",), 1),
        0xB5 : (self._or_r, ("l",), 1),
        0xB6 : (self._or_addr_rr, ("hl",), 1),
        0xB7 : (self._or_r, ("a",), 1),
        0xB8 : (self._cp_r, ("b",), 1),
        0xB9 : (self._cp_r, ("c",), 1),
        0xBA : (self._cp_r, ("d",), 1),
        0xBB : (self._cp_r, ("e",), 1),
        0xBC : (self._cp_r, ("h",), 1),
        0xBD : (self._cp_r, ("l",), 1),
        0xBE : (self._cp_addr_rr, ("hl",), 1),
        0xBF : (self._cp_r, ("a",), 1),

        0xC0 : (self._ret_not_cc, (self._test_zero_flag,), 0),
        0xC1 : (self._pop_rr, ("bc",), 1),
        0xC2 : (self._jp_not_cc, (self._test_zero_flag,), 0),
        0xC3 : (self._jp_cc, (self._dummy_true,), 0),
        0xC4 : (self._call_not_cc, (self._test_zero_flag,), 0),
        0xC5 : (self._push_rr, ("bc",), 1),
        0xC6 : (self._add_r_n, ("a",), 2),
        0xC7 : (self._rst, (0x0,), 0),
        0xC8 : (self._ret_cc, (self._test_zero_flag,), 0),
        0xC9 : (self._ret_cc, (self._dummy_true,), 0),
        0xCA : (self._jp_cc, (self._test_zero_flag,), 0),
        0xCB : self.cb_opcodes, # Ingress to self.cb_prefix.
        0xCC : (self._call_cc, (self._test_zero_flag,), 0),
        0xCD : (self._call_cc, (self._dummy_true,), 0),
        0xCE : (self._adc_r_n, ("a",), 2),
        0xCF : (self._rst, (0x8,), 0),

        0xD0 : (self._ret_not_cc, (self._test_carry_flag,), 0),
        0xD1 : (self._pop_rr, ("de",), 1),
        0xD2 : (self._jp_not_cc, (self._test_carry_flag,), 0),
        0xD3 : (self._out_addr_n_r, ("a",), 2),
        0xD4 : (self._call_not_cc, (self._test_carry_flag,), 0),
        0xD5 : (self._push_rr, ("de",), 1),
        0xD6 : (self._sub_n, (), 2),
        0xD7 : (self._rst, (0x10,), 0),
        0xD8 : (self._ret_cc, (self._test_carry_flag,), 0),
        0xD9 : (self._exx, (), 1),
        0xDA : (self._jp_cc, (self._test_carry_flag,), 0),
        0xDB : (self._in_r_addr_r, ("a",), 1),
        0xDC : (self._call_cc, (self._test_carry_flag,), 0),
        0xDD : self.dd_opcodes, # Ingress to self.dd_prefix. 
        #0xDE : (self._sbc_r_n, ("a",), 1),
        0xDE : (self._sbc_r_n, ("a",), 2),
        0xDF : (self._rst, (0x18,), 0),

        0xE0 : (self._ret_not_cc, (self._test_parity_overflow_flag,), 0),
        0xE1 : (self._pop_rr, ("hl",), 1),
        0xE2 : (self._jp_not_cc, (self._test_parity_overflow_flag,), 0),
        0xE3 : (self._ex_addr_sp_rr, ("hl",), 1),
        0xE4 : (self._call_not_cc, (self._test_parity_overflow_flag,), 0),
        0xE5 : (self._push_rr, ("hl",), 1),
        0xE6 : (self._and_n, (), 2),
        0xE7 : (self._rst, (0x20,), 0),
        0xE8 : (self._ret_cc, (self._test_parity_overflow_flag,), 0),
        0xE9 : (self._jp_rr, ("hl",), 0),
        0xEA : (self._jp_cc, (self._test_parity_overflow_flag,), 0),
        0xEB : (self._ex_rr_rr, ("de", "hl",), 1),
        0xEC : (self._call_cc, (self._test_parity_overflow_flag,), 0),
        0xED : self.ed_opcodes, # Ingress to self.ed_prefix. 
        0xEE : (self._xor_n, (), 2),
        0xEF : (self._rst, (0x28,), 0),

        0xF0 : (self._ret_not_cc, (self._test_sign_flag,), 0),
        0xF1 : (self._pop_rr, ("af",), 1),
        0xF2 : (self._jp_not_cc, (self._test_sign_flag,), 0),
        0xF3 : (self._di, (), 1),
        0xF4 : (self._call_not_cc, (self._test_sign_flag,), 0),
        0xF5 : (self._push_rr, ("af",), 1),
        0xF6 : (self._or_n, (), 2),
        0xF7 : (self._rst, (0x30,), 0),
        0xF8 : (self._ret_cc, (self._test_sign_flag,), 0),
        0xF9 : (self._ld_rr_rr, ("sp", "hl",), 1),
        0xFA : (self._jp_cc, (self._test_sign_flag,), 0),
        0xFB : (self._ei, (), 1),
        0xFC : (self._call_cc, (self._test_sign_flag,), 0),
        0xFD : self.fd_opcodes, # Ingress to self.fd_prefix.
        0xFE : (self._cp_n, (), 2),
        0xFF : (self._rst, (0x38,), 0),
        }

        # Selector.
        self.opcodes = None

        # Debug.
        #self._force_flag_register(0x15)
        self._trace = ""

    def _force_flag_register(self, byte) :
        """
        Force the f register to byte.
        This method is used ONLY for testing purposes.
        """
        self._write_r("f", byte)

    @property
    def logger(self) :
        return self._logger

    @logger.setter
    def logger(self, logger) :
        self._logger = logger

    @property
    def bdos_extension(self) :
        return self._bdos_extension

    @bdos_extension.setter
    def bdos_extension(self, value) :
        self._bdos_extension = value

    def plug_ram(self, ram) :
        if not self.ram :
            self.ram = ram
        else :
            raise RAMModulePresent

    def plug_device(self, device) :
        if not self.devices :
            self.devices = {}
            
        if not self.devices.has_key(device.address) :
            self.devices[device.address] = device
            print "Device : %s successfully plugged" % device.name
        else :
            raise DeviceAddressInUse(device.name)

    def _log_instruction_trace(self, trace) :
        self._log_trace(trace, left_justify=22)

    def _log_trace(self, trace, left_justify=1) :
        self._trace = "%s %s" % (self._trace, trace.ljust(left_justify))

    def _print_trace(self) :
        self._logger.write(self._trace)
        self._trace = ""

    def _dummy_true(self) :
        return True

    def _log_trace_header(self) :
        self._log_trace("\n PC     Instruction            A     SZYHXPNC  B    C    D    E    H    L    IR     IX     IY     SP     A'    SZYHXPNC'  B'   C'   D'   E'   H'   L'  \n")

    def _fetch_instruction(self) :
        """ Fetches & stores the current instruction into the IR register. """

        addr = compose_word(*self._read_rr("pc"))
        self._write_rr("ir", self.ram.read(addr))

    def _fetch_instruction_ahead(self) :
        """
        Fetches & stores the instruction which is 2 bytes ahead
        into the IR register. This method is only used when
        processing the DDCB or FDCB instructions.
        """
        addr = compose_word(*self._read_rr("pc")) + 2
        self._write_rr("ir", self.ram.read(addr))

    def _test_sign_flag(self) :
        """ Tests the sign flag (S) of the f register.     
            returns: 1 if set, otherwise 0. 
        """

        if self.registers["f"] & 0x80 :
            return 1

        return 0

    def _set_sign_flag(self) :
        """ Sets the sign flag (S) of the f register. """
        
        self.registers["f"] |= 0x80

    def _reset_sign_flag(self) :
        """ Resets the sign flag (S) of the f register. """

        if self._test_sign_flag() :        
            self.registers["f"] ^= 0x80

    def _test_zero_flag(self) :
        """ Tests the zero flag (Z) of the f register. 
            returns: 1 if set, otherwise 0. 
        """

        if self.registers["f"] & 0x40 :
            return 1

        return 0

    def _set_zero_flag(self) :
        """ Sets the zero flag (Z) of the f register. """

        self.registers["f"] |= 0x40

    def _reset_zero_flag(self) :
        """ Resets the zero flag (Z) of the f register. """

        if self._test_zero_flag() :        
            self.registers["f"] ^= 0x40

    def _test_half_carry_flag(self) :
        """ Tests the half carry flag (H) of the f register. 
            returns: 1 if set, otherwise 0. 
        """

        if self.registers["f"] & 0x10 :
            return 1

        return 0

    def _set_half_carry_flag(self) :
        """ Sets the half carry flag (H) of the f register. """

        self.registers["f"] |= 0x10

    def _reset_half_carry_flag(self) :
        """ Resets the half carry flag (H) of the f register. """

        if self._test_half_carry_flag() :        
            self.registers["f"] ^= 0x10

    def _test_parity_overflow_flag(self) :
        """ Tests the parity/overflow (P) flag of the f register. 
            returns: 1 if set, otherwise 0. 
        """

        if self.registers["f"] & 0x4 :
            return 1

        return 0

    def _set_parity_overflow_flag(self) :
        """ Sets the parity/overflow (P) of the f register. """

        self.registers["f"] |= 0x4

    def _reset_parity_overflow_flag(self) :
        """ Resets the parity/overflow (P) of the f register. """

        if self._test_parity_overflow_flag() :        
            self.registers["f"] ^= 0x4

    def _test_add_substract_flag(self) :
        """ Tests the add/substract (N) flag of the f register. 
            returns: 1 if set, otherwise 0. 
        """

        if self.registers["f"] & 0x2 :
            return 1

        return 0

    def _set_add_substract_flag(self) :
        """ Sets the add/substract (N) of the f register. """

        self.registers["f"] |= 0x2

    def _reset_add_substract_flag(self) :
        """ Resets the add/substract (N) of the f register. """

        if self._test_add_substract_flag() :        
            self.registers["f"] ^= 0x2

    def _test_carry_flag(self) :
        """ Tests the carry flag (C) of the f register. 
            returns: 1 if set, otherwise 0. 
        """

        if self.registers["f"] & 0x1 :
            return 1

        return 0

    def _set_carry_flag(self) :
        """ Sets the carry flag (C) of the f register. """

        self.registers["f"] |= 0x1

    def _reset_carry_flag(self) :
        """ Resets the carry flag (C) of the f register. """

        if self._test_carry_flag() :        
            self.registers["f"] ^= 0x1

    def _read_ix_iy_byte(self, r) :
        """
        Reads a byte from either ixh, ixl, iyh or iyl registers.
        """
        ho_byte, lo_byte = self._read_rr(r[:2])
        if (r == "ixh") or (r == "iyh") :
            return ho_byte

        return lo_byte

    def _write_ix_iy_byte(self, r, byte) :
        """
        Writes byte on either ixh, ixl, iyx or iyl registers.
        """
        if (r == "ixh") or (r == "iyh") :
            lo_byte = self._read_ix_iy_byte(r[:2] + "l")
            self._write_rr(r[:2], compose_word(byte, lo_byte))
            return

        ho_byte = self._read_ix_iy_byte(r[:2] + "h")
        self._write_rr(r[:2], compose_word(ho_byte, byte))

    def _write_r(self, r, byte) :
        """
        Writes the r register.
        """
        ix_iy_registers = ["ixh", "ixl", "iyh", "iyl"]
        if r in ix_iy_registers :
            self._write_ix_iy_byte(r, byte)
            return

        self.registers[r] = byte & 0xFF

    def _write_rr(self, rr, word) :
        """ Writes the rr register pair with word.
            :params:
                rr: The rr register pair to write to.
                word: The word to write to register pair.
        """

        if self.registers.has_key(rr) :
            self.registers[rr] = word & 0xFFFF
        else :
            ho_byte, lo_byte = decompose_word(word)
            self._write_r(rr[0], ho_byte)
            self._write_r(rr[1], lo_byte)

    def _read_r(self, r) :
        """ Reads the r register.
            :params:
                r: The r register to read.
        """

        ix_iy_registers = ["ixh", "ixl", "iyh", "iyl"]
        if r in ix_iy_registers :
            return self._read_ix_iy_byte(r)

        return self.registers[r]

    def _read_rr(self, rr) :
        """ Reads the rr register. 
            :params:
                rr: The rr register pair to read from. 
        """

        if self.registers.has_key(rr) :
            return decompose_word(self.registers[rr])

        return self._read_r(rr[0]), self._read_r(rr[1])

    def _read_n(self) :
        """ Reads a byte from RAM. The address of byte
        is relative to the current value of the PC
        (program counter).
        """

        addr = compose_word(*self._read_rr("pc"))
        return self.ram.read(addr + 1)

    def _read_nn(self) :
        """ Reads a word from RAM. The address of word
        is relative to the current value of the PC
        (program counter).
        """

        addr = compose_word(*self._read_rr("pc"))
        return self.ram.read(addr + 2), self.ram.read(addr + 1)

    def _read_n_ram(self, ho_addr, lo_addr) :
        """ Reads a byte from RAM.
            :params:
                ho_addr: High order address byte.
                lo_addr: Low order address byte.
        """

        addr = compose_word(ho_addr, lo_addr)
        return self.ram.read(addr)

    def _read_nn_ram(self, ho_addr, lo_addr) :
        """ Reads a word from RAM.
            :params:
                ho_addr: High order address byte.
                lo_addr: Low order address byte.

            :return:
                A tuple containing the high and low order byte
                of the word.
        """

        word = compose_word(ho_addr, lo_addr) + 1
        ho_byte = self._read_n_ram(*decompose_word(word))
        lo_byte = self._read_n_ram(ho_addr, lo_addr)
        return ho_byte, lo_byte

    def _write_n_ram(self, byte, ho_addr, lo_addr) :
        """ Writes a byte to RAM.
            :params:
                byte: The byte to write.
                ho_addr: High order address byte.
                lo_addr: Low order address byte.
        """

        self.ram.write(compose_word(ho_addr,lo_addr), byte)

    def _write_nn_ram(self, ho_byte, lo_byte, ho_addr, lo_addr) :
        """ Writes a word to RAM.
            :params:
                ho_byte: High order byte to write.
                lo_byte: Low order byte to write.
                ho_addr: High order address byte.
                lo_addr: Low order address byte.
        """

        word = compose_word(ho_addr, lo_addr) + 1
        self._write_n_ram(ho_byte, *decompose_word(word))
        self._write_n_ram(lo_byte, ho_addr, lo_addr)

    def _read_nn_stack(self) :
        """ Pops a word from the stack. 
        
            :return:
                
        """

        ho_addr, lo_addr = self._read_rr("sp")
        self._inc_n_sp(2)

        return self._read_nn_ram(ho_addr, lo_addr)

    def _write_nn_stack(self, ho_byte, lo_byte) :
        """ Pushes a word onto the stack.
            :params:
                ho_byte: High order byte to push.
                lo_byte: Low order byte to push.
        """

        ho_addr, lo_addr = self._read_rr("sp")
        addr = compose_word(ho_addr, lo_addr)
        self._write_n_ram(ho_byte, *decompose_word(addr - 1))
        self._write_n_ram(lo_byte, *decompose_word(addr - 2))
        self._dec_n_sp(2)

    def _inc_pc(self) :
        """ Increments the program counter by one. """

        self._inc_n_pc(1)

    def _inc_n_pc(self, n) :
        """ Increments the program counter by n.
            :params:
                n: The increment.
        """

        ho_addr, lo_addr = self._read_rr("pc")
        self._write_rr("pc", compose_word(ho_addr, lo_addr) + n)

    def _dec_n_pc(self, n) :
        """ Decrements the program counter by n.
            :params:
                n: The decrement.
        """

        ho_addr, lo_addr = self._read_rr("pc")
        self._write_rr("pc", compose_word(ho_addr, lo_addr) - n)

    def _inc_n_sp(self, n) :
        """ Increments the stack pointer by n.
            :params:
                n: The increment.
        """

        ho_addr, lo_addr = self._read_rr("sp")
        self._write_rr("sp", compose_word(ho_addr, lo_addr) + n)

    def _dec_n_sp(self, n) :
        """ Decrements the stack pointer by n.
            :params:
                n: The decrement.
        """

        ho_addr, lo_addr = self._read_rr("sp")
        self._write_rr("sp", compose_word(ho_addr, lo_addr) - n)

    def _registers_status(self) :
        a  = self._read_r("a")
        a_ = self._read_r("a_")
        b  = self._read_r("b")
        b_ = self._read_r("b_")
        c  = self._read_r("c")
        c_ = self._read_r("c_")
        d  = self._read_r("d")
        d_ = self._read_r("d_")
        e  = self._read_r("e")
        e_ = self._read_r("e_")
        f  = binary(self._read_r("f"))
        f_ = binary(self._read_r("f_"))
        h  = self._read_r("h")
        h_ = self._read_r("h_")
        l  = self._read_r("l")
        l_ = self._read_r("l_")
        ir = compose_word(*self._read_rr("ir"))
        ix = compose_word(*self._read_rr("ix"))
        iy = compose_word(*self._read_rr("iy"))
        pc = compose_word(*self._read_rr("pc"))
        sp = compose_word(*self._read_rr("sp"))

        return "0x%0.2X  %s  0x%0.2X 0x%0.2X 0x%0.2X 0x%0.2X 0x%0.2X 0x%0.2X 0x%0.4X 0x%0.4X 0x%0.4X 0x%0.4X 0x%0.2X  %s   0x%0.2X 0x%0.2X 0x%0.2X 0x%0.2X 0x%0.2X 0x%0.2X" % (a, f, b, c, d, e, \
        h, l, ir, ix, iy, sp, a_, f_, b_, c_, d_, e_, h_, l_)

    def run(self, start_address) :
        """
        Starts the execution of a program located at
        start_address.
        """

        if self._bdos_extension :
            self._bdos_patch()

        self._log_trace_header()
        self._print_trace()
        self._write_rr("pc", start_address)

        # Note : When the program counter reaches 0xFFFF we
        # start all over again. This is not a bug, (as the
        # pc is 16 bits long, when we reach 0xFFFF pc is under
        # an overflow condition and holds 0x0).

        while self._read_r("pc") <= 0xFFFF :
            self._log_trace("0x%0.4X" % compose_word(*self._read_rr("pc")))
            self._fetch_opcode()
            self._execute_opcode()
            self._inc_n_pc(self.opcodes[self._read_r("ir")] [2])
            self._print_trace()
            self._interrupt_handler()

    def _fetch_opcode(self) :
        """ Fetches an opcode and stores it in the instruction register. """

        self.opcodes = self.unprefixed_opcodes
        self._fetch_instruction()

        if (self._read_r("ir") == 0xCB) or (self._read_r("ir") == 0xED) \
        or (self._read_r("ir") == 0xDD) or (self._read_r("ir") == 0xFD) :
            self.opcodes = self.opcodes [self._read_r("ir")]
            self._inc_pc()
            self._fetch_instruction()

            if (self._read_r("ir") == 0xCB) :
                self.opcodes = self.opcodes [self._read_r("ir")]
                self._fetch_instruction_ahead()

    def _execute_opcode(self) :
        """
        Execute opcode. If opcode is invalid or 
        not implemented an UnknownOpcode exception is raised.
        """

        try :
            operands = self.opcodes[self._read_r("ir")] [1]
            self.opcodes[self._read_r("ir")] [0] (*operands)
            self._log_trace(self._registers_status())

        except KeyError :
            #self.ram.dump_ram_range(self._read_r("pc") - 2, self._read_r("pc") + 2)
            print "0x%0.4X" % self._read_r("pc")
            raise UnknownOpcode("Unknown opcode : 0x%0.2X" % self._read_r("ir"))

    def _interrupt_handler(self) :
        pass

    def _adc_flag_tests(self, n, m) :
        # Affects : S, Z, H, P, C
        # Resets : N.
        l = n + m
        self._test_and_set_sign_flag(l)
        self._test_and_set_zero_flag(l)
        self._test_and_set_half_carry_on_add(n, m)
        self._test_and_set_overflow_flag(n, m)
        self._test_and_set_carry_flag(l)
        self._reset_add_substract_flag()

    def _adc_r_addr_indx_d(self, r, rr) :
        """
        ADC r, (rr + d).
        """
        self._log_instruction_trace("ADC %s, (%s + 0x%0.2X)" % \
            (r, rr, self._read_n()))
        ho_base_addr, lo_base_addr = self._read_rr(rr)
        ho_addr, lo_addr = compute_indexed_address(ho_base_addr, \
            lo_base_addr, self._read_n())
        byte = self._read_r(r) + self._read_n_ram(ho_addr, lo_addr) + \
            self._test_carry_flag()
        self._adc_flag_tests(self._read_r(r), \
            self._read_n_ram(ho_addr, lo_addr) + self._test_carry_flag())
        self._write_r(r, byte)

    def _adc_r_addr_rr(self, r, rr) :
        """
        ADC r, (rr).
        """
        self._log_instruction_trace("ADC %s, (%s)" % (r, rr))
        byte = self._read_r(r) + self._read_n_ram(*(self._read_rr(rr))) + \
            self._test_carry_flag()
        self._adc_flag_tests(self._read_r(r), \
            self._read_n_ram(*(self._read_rr(rr))) + self._test_carry_flag())
        self._write_r(r, byte)

    def _adc_r_n(self, r) :
        """
        ADC r, n. Add r and n with carry.
        """
        self._log_instruction_trace("ADC %s, 0x%0.2X" % (r, self._read_n()))
        byte = self._read_r(r) + self._read_n() + self._test_carry_flag()
        self._adc_flag_tests(self._read_r(r), \
            self._read_n() + self._test_carry_flag())
        self._write_r(r, byte)

    def _adc_r_r(self, r1, r2) :
        """
        ADC r, r'. Add r1 and r2 with carry.
        """
        self._log_instruction_trace("ADC %s, %s" % (r1, r2))
        byte = self._read_r(r1) + self._read_r(r2) + \
            self._test_carry_flag()
        self._adc_flag_tests(self._read_r(r1), self._read_r(r2) + \
            self._test_carry_flag())
        self._write_r(r1, byte)

    def _adc_word(self, n, m) :
        # Affects : S, Z, H, P, C
        # Resets : N.
        l = n + m
        self._test_and_set_sign_flag_word(l)
        self._test_and_set_zero_flag_word(l)
        self._test_and_set_half_carry_on_add_word(n, m)
        self._test_and_set_overflow_flag_word(n, m)
        self._test_and_set_carry_flag_word(l)
        self._reset_add_substract_flag()

    def _adc_rr_rr(self, rr1, rr2) :
        self._log_instruction_trace("ADC %s, %s" % (rr1, rr2))
        word_rr1 = compose_word(*self._read_rr(rr1))
        word_rr2 = compose_word(*self._read_rr(rr2)) + self._test_carry_flag()
        self._adc_word(word_rr1, word_rr2)
        self._write_rr(rr1, word_rr1 + word_rr2)

    def _add_flag_tests(self, n, m) :
        # Affects : S, Z, H, P, C
        # Resets : N.
        add = n + m
        self._test_and_set_sign_flag(add)
        self._test_and_set_zero_flag(add)
        self._test_and_set_half_carry_on_add(n, m)
        self._test_and_set_overflow_flag(n, m)
        self._test_and_set_carry_flag(add)
        self._reset_add_substract_flag()

    def _add_r_addr_indx_d(self, r, rr) :
        self._log_instruction_trace("ADD %s, (%s + 0x%0.2X)" % (r, rr, \
        self._read_n()))
        ho_base_addr, lo_base_addr = self._read_rr(rr)
        ho_addr, lo_addr = compute_indexed_address(ho_base_addr, \
        lo_base_addr, self._read_n())
        self._add_flag_tests(self._read_r(r), self._read_n_ram(ho_addr, lo_addr))
        self._write_r(r, self._read_r(r) + self._read_n_ram(ho_addr, lo_addr))

    def _add_r_addr_rr(self, r, rr) :
        """
        ADD r, (rr). Add accumulator with indirectly addressed 
        memory location (rr).
        """
        self._log_instruction_trace("ADD %s, (%s)" % (r, rr))
        self._add_flag_tests(self._read_r(r), self._read_n_ram(*self._read_rr(rr)))
        self._write_r(r, self._read_r(r) + self._read_n_ram(*self._read_rr(rr)))

    def _add_r_n(self, r) :
        self._log_instruction_trace("ADD %s, 0x%0.2X" % (r, self._read_n()))
        self._add_flag_tests(self._read_r(r), self._read_n())
        self._write_r(r, self._read_r(r) + self._read_n())

    def _add_r_r(self, r1, r2) :
        self._log_instruction_trace("ADD %s, %s" % (r1, r2))
        self._add_flag_tests(self._read_r(r1), self._read_r(r2))
        self._write_r(r1, self._read_r(r1) + self._read_r(r2))

    def _add_rr_r(self, rr, r) :
        # Affects : C
        # Resets : N
        # Sets : H (H is set by a carry from bit 11)
        self._log_instruction_trace("ADD %s, %s" % (rr, r))
        word = compose_word(*(self._read_rr(rr))) + self._read_r(r)

        if test_word_overflow(word) :
            self._set_carry_flag()
        else :
            self._reset_carry_flag()

        self._reset_add_substract_flag()
        self._write_rr(rr, word)

    def _add_word(self, n, m) :
        # Affects : H, C
        # Resets : N.
        add = n + m
        self._test_and_set_half_carry_on_add_word(n, m)
        self._test_and_set_carry_flag_word(add)
        self._reset_add_substract_flag()

    def _add_rr_rr(self, rr1, rr2) :
        self._log_instruction_trace("ADD %s, %s" % (rr1, rr2))
        word_rr1 = compose_word(*self._read_rr(rr1))
        word_rr2 = compose_word(*self._read_rr(rr2))
        self._add_word(word_rr1, word_rr2)
        self._write_rr(rr1, word_rr1 + word_rr2)

    def _and_flag_tests(self, n) :
        self._test_and_set_sign_flag(n)
        self._test_and_set_zero_flag(n)
        self._test_and_set_parity_flag(n)
        self._set_half_carry_flag()
        self._reset_add_substract_flag()
        self._reset_carry_flag()

    def _and_addr_indx_d(self, rr) :
        self._log_instruction_trace("AND (%s + 0x%0.2X)" % (rr, self._read_n()))
        ho_base_addr, lo_base_addr = self._read_rr(rr)
        ho_addr, lo_addr = compute_indexed_address(ho_base_addr, \
            lo_base_addr, self._read_n())
        byte = self._read_r("a") & self._read_n_ram(ho_addr, lo_addr)
        self._and_flag_tests(byte)
        self._write_r("a", byte)

    def _and_addr_rr(self, rr) :
        self._log_instruction_trace("AND (%s)" % rr)
        byte = self._read_r("a") & self._read_n_ram(*self._read_rr(rr))
        self._and_flag_tests(byte)
        self._write_r("a", byte)

    def _and_n(self) :
        """
        AND n. Logical AND accumulator with n.
        """
        self._log_instruction_trace("AND 0x%0.2X" % self._read_n())
        byte = self._read_r("a") & self._read_n()
        self._and_flag_tests(byte)
        self._write_r("a", byte)

    def _and_r(self, r) :
        """
        AND r. Logical AND accumulator with register r.
        """
        self._log_instruction_trace("AND %s" % r)
        byte = self._read_r("a") & self._read_r(r)
        self._and_flag_tests(byte)
        self._write_r("a", byte)

    def _bit_flag_tests(self, n, test_bit) :
        # Affects : Z.
        # Sets : H.
        # Resets : N.
        if n :
            self._reset_zero_flag()

            if test_bit == 0x80 :
                self._set_sign_flag()
        else :
            self._set_zero_flag()

        self._set_half_carry_flag()
        self._reset_add_substract_flag()

    def _bdos(self, r, rr) :
        c = self._read_r(r)
        self._bdos_system_calls[c] (*self._read_rr(rr))

    def _bdos_c_writestr(self, ho_addr, lo_addr) :
        self._log_instruction_trace("BDOS WRITESTR")
        c = self._read_n_ram(ho_addr, lo_addr)
        s = ""

        while chr(c) != '$' :
            s += s.join(chr(c))
            addr = compose_word(ho_addr, lo_addr) + 1
            ho_addr, lo_addr = decompose_word(addr)
            c = self._read_n_ram(ho_addr, lo_addr)

        print s

    def _bdos_patch(self) :
        self._write_n_ram(0xED, 0x00, 0x05)
        self._write_n_ram(0x0E, 0x00, 0x06)
        self._write_n_ram(0xC9, 0x00, 0x07)

        self.ed_opcodes[0x0E] = (self._bdos, ("c", "de",), 1)

        self._bdos_system_calls = {9 : self._bdos_c_writestr,
        }

    def _bit_n_indx_d(self, n, rr) :
        """
        BIT n, (rr + d). Test bit n of byte pointed by (rr + d).
        """
        self._log_instruction_trace("BIT 0x%0.2X, (%s + 0x%0.2X)" % (n, rr, self._read_n()))
        ho_base_addr, lo_base_addr = self._read_rr(rr)
        ho_addr, lo_addr = compute_indexed_address(ho_base_addr, \
            lo_base_addr, self._read_n())
        self._bit_flag_tests(self._read_n_ram(ho_addr, lo_addr) & n, n)

    def _bit_n_addr_rr(self, n, rr) :
        """
        BIT n, (rr). Test bit n of byte pointed by rr.
        """
        self._log_instruction_trace("BIT 0x%0.2X, (%s)" % (n, rr))
        self._bit_flag_tests(self._read_n_ram(*self._read_rr(rr)) & n, n)

    def _bit_n_r(self, n, r) :
        """
        BIT n, r. Test bit n of register r.
        """
        self._log_instruction_trace("BIT 0x%0.2X, %s" % (n, r))
        self._bit_flag_tests(self._read_r(r) & n, n)

    def _call(self) :
        ho_byte, lo_byte = self._read_nn()
        self._inc_n_pc(3)
        self._write_nn_stack(*self._read_rr("pc"))
        self._write_rr("pc", compose_word(ho_byte, lo_byte))

    def _call_cc(self, cc) :
        """
        CALL cc, nn. Call subroutine on cc (condition).
        """

        if cc == self._test_zero_flag :
            trace = "CALL Z, 0x%0.2X" % compose_word(*self._read_nn())
        elif cc == self._test_carry_flag :
            trace = "CALL C, 0x%0.2X" % compose_word(*self._read_nn())
        elif cc == self._test_parity_overflow_flag :
            trace = "CALL PE, 0x%0.2X" % compose_word(*self._read_nn())
        elif cc == self._test_sign_flag :
            trace = "CALL M, 0x%0.2X" % compose_word(*self._read_nn())
        else :
            trace = "CALL 0x%0.2X" % compose_word(*self._read_nn())

        self._log_instruction_trace(trace)

        if cc() :
            self._call()
            return
        
        self._inc_n_pc(3)

    def _call_not_cc(self, cc) :
        """
        CALL cc, nn. Call subroutine on NOT cc (condition).
        """

        if cc == self._test_zero_flag :
            trace = "CALL NZ, 0x%0.2X" % compose_word(*self._read_nn())
        elif cc == self._test_carry_flag :
            trace = "CALL NC, 0x%0.2X" % compose_word(*self._read_nn())
        elif cc == self._test_parity_overflow_flag :
            trace = "CALL PO, 0x%0.2X" % compose_word(*self._read_nn())
        elif cc == self._test_sign_flag :
            trace = "CALL P, 0x%0.2X" % compose_word(*self._read_nn())
        else :
            trace = "CALL 0x%0.2X" % compose_word(*self._read_nn())

        self._log_instruction_trace(trace)

        if not cc() :
            self._call()
            return 
        
        self._inc_n_pc(3)

    def _ccf(self) :
        """
        CCF. Complement carry flag.
        """
        # Sets : C, H.
        # Resets : N.
        self._log_instruction_trace("CCF")

        if self._test_carry_flag() :
            self._reset_carry_flag()
        else :
            self._set_carry_flag()

        if self._test_half_carry_flag() :
            self._reset_half_carry_flag()
        else :
            self._set_half_carry_flag()

        self._reset_add_substract_flag()

    def _cp_flag_tests(self, n, m) :
        l = n - m
        self._test_and_set_sign_flag(l)
        self._test_and_set_zero_flag(l)
        self._test_and_set_half_carry_on_substract(n, m)
        #self._test_and_set_overflow_flag(n, m)
        self._test_and_set_overflow_flag(n, m, "SUB")
        self._test_and_set_carry_flag(l)
        self._set_add_substract_flag()

    def _cp_addr_indx_d(self, rr) :
        self._log_instruction_trace("CP (%s + 0x%0.2X)" % (rr, self._read_n()))
        ho_base_addr, lo_base_addr = self._read_rr(rr)
        ho_addr, lo_addr = compute_indexed_address(ho_base_addr, \
            lo_base_addr, self._read_n())
        self._cp_flag_tests(self._read_r("a"), self._read_n_ram(ho_addr, lo_addr))

    def _cp_addr_rr(self, rr) :
        self._log_instruction_trace("CP (%s)" % rr)
        self._cp_flag_tests(self._read_r("a"), self._read_n_ram(*self._read_rr(rr)))

    def _cpd(self) :
        """ CPD. Compare with decrement. """

        a = self._read_r("a")
        byte = self._read_n_ram(*self._read_rr("hl"))
        self._test_and_set_sign_flag(a - byte)
        self._test_and_set_half_carry_on_substract(a, byte)
        self._write_rr("hl", compose_word(*self._read_rr("hl")) - 1)
        self._write_rr("bc", compose_word(*self._read_rr("bc")) - 1)

        if compose_word(*self._read_rr("bc")) == 0 :
            self._reset_parity_overflow_flag()
        else :
            self._set_parity_overflow_flag()

        if a == self._read_n_ram(*self._read_rr("hl")) :
            self._set_zero_flag()

        self._set_add_substract_flag()

    def _cpi(self) :
        """ CPI. Compare with increment. """

        self._log_instruction_trace("CPI")
        a = self._read_r("a")
        byte = self._read_n_ram(*self._read_rr("hl"))
        self._test_and_set_sign_flag(a - byte)
        self._test_and_set_half_carry_on_substract(a, byte)
        self._write_rr("hl", compose_word(*self._read_rr("hl")) + 1)
        self._write_rr("bc", compose_word(*self._read_rr("bc")) - 1)

        if compose_word(*self._read_rr("bc")) :
            self._set_parity_overflow_flag()
        else :
            self._reset_parity_overflow_flag()

        if a == self._read_n_ram(*self._read_rr("hl")) :
            self._set_zero_flag()

        self._set_add_substract_flag()

    def _cpir(self) :
        """ CPIR. Compare block with increment. """
        self._test_and_set_sign_flag(self._read_r("a") - \
            self._read_n_ram(*self._read_rr("hl")))
        self._test_and_set_half_carry_on_substract(self._read_r("a"), \
            self._read_n_ram(*self._read_rr("hl")))
        self._write_rr("hl", compose_word(*self._read_rr("hl")) + 1)
        self._write_rr("bc", compose_word(*self._read_rr("bc")) - 1)

        if not ((self._read_rr("bc") == 0) and \
        (self._read_r("a") == self._read_n_ram(*self._read_rr("hl")))) :
            self._inc_n_pc(2)

    def _cpdr(self) :
        pass
            
    def _cpl(self) :
        """
        CPL. Complement accumulator.
        """
        # Sets : H, N.
        self._log_instruction_trace("CPL")
        self._write_r("a", ones_complement_byte(self._read_r("a")))

        # Flags sets & resets.
        self._set_half_carry_flag()
        self._set_add_substract_flag()

    def _cp_n (self) :
        self._log_instruction_trace("CP 0x%0.2X" % self._read_n())
        self._cp_flag_tests(self._read_r("a"), self._read_n())

    def _cp_r (self, r) :
        self._log_instruction_trace("CP %s" % r)
        self._cp_flag_tests(self._read_r("a"), self._read_r(r))

    def _daa(self) :
        """
        DAA. Decimal adjust accumulator.
        """
        # Affects : S, Z, H, P, C.
        self._log_instruction_trace("DAA")
        daa_table = {"000" : [(0x0, 0x9, 0x0, 0x9, 0x00, 0),
                              (0x0, 0x8, 0xA, 0xF, 0x06, 0),
                              (0xA, 0xF, 0x0, 0x9, 0x60, 1),
                              (0x9, 0xF, 0xA, 0xF, 0x66, 1)],
        "001" : [(0x0, 0x9, 0x0, 0x3, 0x06, 0),
                 (0xA, 0xF, 0x0, 0x3, 0x66, 1)],
        "010" : [(0x0, 0x2, 0x0, 0x9, 0x60, 1),
                 (0x0, 0x2, 0xA, 0xF, 0x66, 1)],
        "011" : [(0x0, 0x3, 0x0, 0x3, 0x66, 1)],
        "100" : [(0x0, 0x9, 0x0, 0x9, 0x00, 0)],
        "101" : [(0x0, 0x8, 0x6, 0xF, 0xFA, 0)],
        "110" : [(0x7, 0xF, 0x0, 0x9, 0xA0, 1)],
        "111" : [(0x6, 0xF, 0x6, 0xF, 0x9A, 1)]}

        ho_nibble, lo_nibble = decompose_byte(self._read_r("a"))
        # nch holds the concatenation of the N, C and H flags.
        # Then we use nch to access the daa_table.
        nch = "%d%d%d" % (self._test_add_substract_flag(), \
            self._test_carry_flag(), self._test_half_carry_flag())
        daa = daa_table [nch]
        stop = False
        i = 0

        while not stop :
            if (ho_nibble >= daa [i] [0] and ho_nibble <= daa [i] [1]) \
            and (lo_nibble >= daa [i] [2] and lo_nibble <= daa [i] [3]) :
                # Set/reset half carry flag.
                self._test_and_set_half_carry_on_add(self._read_r("a"),\
                    daa [i] [4])
                
                # Set/reset carry flag.
                if daa [i] [5] :
                    self._set_carry_flag()
                else :
                    self._reset_carry_flag()

                self._write_r("a", self._read_r("a") + daa [i] [4])
                stop = True
            else :
                i += 1

        self._test_and_set_sign_flag(self._read_r("a"))
        self._test_and_set_zero_flag(self._read_r("a"))
        self._test_and_set_parity_flag(self._read_r("a"))

    def _dec_flag_tests(self, n, m) :
        # Affects : S, Z, H, V. 
        # Sets : N.
        l = n - m
        self._test_and_set_sign_flag(l)
        self._test_and_set_zero_flag(l)
        self._test_and_set_half_carry_on_substract(n, m)
        self._test_and_set_overflow_flag(n, m)
        self._set_add_substract_flag()

    def _dec_addr_indx_d(self, rr) :
        self._log_instruction_trace("DEC (%r + 0x%0.2X)" % (rr, self._read_n()))
        ho_base_addr, lo_base_addr = self._read_rr(rr)
        ho_addr, lo_addr = compute_indexed_address(ho_base_addr, \
            lo_base_addr, self._read_n())
        self._dec_flag_tests(self._read_n_ram(self, ho_addr, lo_addr), 1)
        self._write_n_ram(self._read_n_ram(self, ho_addr, lo_addr) - 1, \
            ho_addr, lo_addr)

    def _dec_addr_rr(self, rr) :
        """
        DEC (rr). Decrement byte at location pointed by rr.
        """
        self._log_instruction_trace("DEC (%s)" % rr)
        self._dec_flag_tests(self._read_n_ram(*self._read_rr(rr)), 1)
        self._write_n_ram(self._read_n_ram(*self._read_rr(rr)) - 1, \
        ho_addr, lo_addr)

    def _dec_rr(self, rr) :
        """
        DEC rr. Decrement register pair rr.
        """
        self._log_instruction_trace("DEC %s" % rr)
        ho_byte, lo_byte = self._read_rr(rr)
        self._write_rr(rr, compose_word(ho_byte, lo_byte) - 1)

    def _dec_r(self, r) :
        self._log_instruction_trace("DEC %s" % r)
        self._dec_flag_tests(self._read_r(r), 1)
        self._write_r(r, self._read_r(r) - 1)

    def _di(self) :
        """
        DI. Disable interrupts.
        """
        self._log_instruction_trace("DI")
        self._write_r("iff1", 0x0)
        self._write_r("iff2", 0x0)

    def _djnz(self) :
        """
        DJNZ. Decrement b and jump n relative on non zero.
        """
        self._log_instruction_trace("DJNZ")
        self._write_r("b", self._read_r("b") - 1)

        if self._read_r("b") :
            ho_base_addr, lo_base_addr = self._read_rr("pc")
            ho_addr, lo_addr = compute_indexed_address(ho_base_addr, \
                lo_base_addr, self._read_n())
            self._write_rr("pc", compose_word(ho_addr, lo_addr))

    def _ei(self) :
        """
        EI. Enable interrupts.
        """
        self._log_instruction_trace("EI")
        self._write_r("iff1", 0x1)
        self._write_r("iff2", 0x1)

    def _ex_addr_sp_rr(self, rr) :
        """
        EX (sp), rr. 
        """
        self._log_instruction_trace("EX (sp), %s" % rr)
        ho_byte_sp, lo_byte_sp = self._read_nn_stack()
        ho_byte, lo_byte = self._read_rr(rr)
        self._write_nn_stack(ho_byte, lo_byte)
        self._write_rr(rr, compose_word(ho_byte_sp, lo_byte_sp))

    def _ex_rr_rr(self, rr1, rr2) :
        """
        EX rr, rr. Exchange rr1 with rr2 register.
        """
        self._log_instruction_trace("EX %s, %s" % (rr1, rr2))
        ho_byte_rr1, lo_byte_rr1 = self._read_rr(rr1)
        ho_byte_rr2, lo_byte_rr2 = self._read_rr(rr2)
        self._write_rr(rr1, compose_word(ho_byte_rr2, lo_byte_rr2))
        self._write_rr(rr2, compose_word(ho_byte_rr1, lo_byte_rr1))

    def _ex_rr_rr_(self, rr, rr_) :
        """
        EX rr, rr'. Exchange rr with alternate registers.
        """
        self._log_instruction_trace("EX %s %s'" % (rr, rr_))
        r = self._read_r(rr[0])
        self._write_r(rr[0], self._read_r(rr_[0] + "_"))
        self._write_r(rr_[0] + "_", r)
        r = self._read_r(rr[1])
        self._write_r(rr[1], self._read_r(rr_[1] + "_"))
        self._write_r(rr_[1] + "_", r)

    def _exx(self) :
        """
        EXX. Exchange alternate registers.
        """
        self._log_instruction_trace("EXX")
        registers = ["b", "c", "d", "e", "h", "l"]

        for register in registers :
            r = self._read_r(register)
            self._write_r(register, self._read_r(register + "_"))
            self._write_r(register + "_", r)

    def _halt(self) :
        """
        HALT. Halt the CPU.
        """
        self._log_instruction_trace("HALT")
        exit()

    def _im(self, n) :
        """
        IM. Set interrupt mode n.
        """
        self._log_instruction_trace("IM 0x%0.2%" % n)
        self._write_r("im", n)

    def _read_io_port(self, addr) :
        try :
            return self.devices[addr].read()
        except KeyError :
            return 0x0

    def _write_io_port(self, addr, byte) :
        try :
            self.devices[addr].write(byte)
        except KeyError :
            pass

    def _in_r_addr_n(self, r) :
        self._log_instruction_trace("IN %s, (0x%0.2X)" % (r, self._read_n()))
        addr = self._read_n()
        self._write_r(r, self._read_io_port(addr))

    def _in_r_addr_r(self, r1, r2) :
        self._log_instruction_trace("IN %s, (%s)" % (r1, r2))
        addr = self._read_r(rr2)
        self._write_r(r1, self._read_io_port(addr))

    def _inc_flag_tests(self, n, m) :
        # Affects : S, Z, H, V. 
        # Resets : N.
        l = n + m
        self._test_and_set_sign_flag(l)
        self._test_and_set_zero_flag(l)
        self._test_and_set_half_carry_on_add(n, m)
        self._test_and_set_overflow_flag(n, m)
        self._reset_add_substract_flag()

    def _inc_addr_indx_d(self, rr) :
        """
        INC (rr + d). Increment byte at location pointed by rr + d.
        rr should be IX or IY.
        """
        self._log_instruction_trace("INC (%s + 0x%0.2X)" % (rr, self._read_n()))
        ho_base_addr, lo_base_addr = self._read_rr(rr)
        ho_addr, lo_addr = compute_indexed_address(ho_base_addr, \
            lo_base_addr, self._read_n())
        self._inc_flag_tests(self._read_n_ram(ho_addr, lo_addr), 1)
        self._write_n_ram(self._read_n_ram(ho_addr, lo_addr) + 1, \
            ho_addr, lo_addr)
        
    def _inc_addr_rr(self, rr) :
        """
        INC (rr). Increment byte at location pointed by rr.
        """
        self._log_instruction_trace("INC (%s)" % rr)
        ho_addr, lo_addr = self._read_rr(rr)
        self._inc_flag_tests(self._read_n_ram(ho_addr, lo_addr), 1)
        self._write_n_ram(self._read_n_ram(ho_addr, lo_addr) + 1, \
            ho_addr, lo_addr)

    def _inc_rr(self, rr) :
        """
        INC rr. Increment register pair rr.
        """
        self._log_instruction_trace("INC %s" % rr)
        ho_byte, lo_byte = self._read_rr(rr)
        self._write_rr(rr, compose_word(ho_byte, lo_byte) + 1)

    def _ind(self) :
        """ IND. Input with decrement. """

        ho_addr, lo_addr = self._read_rr("hl")
        self._write_n_ram(self._read_io_port(self._read_r("c")), \
            ho_addr, lo_addr)
        self._write_r("b", self._read_r("b") - 1)
        self._write_rr("hl", compose_word(*self._read_rr("hl")) - 1)

        if self._read_r("b") == 0 :
            self._set_zero_flag()
        else :
            self._reset_zero_flag()

        self._set_add_substract_flag()

    def _indr(self) :
        pass

    def _ini(self) :
        """ INI. Input with increment. """

        self._log_instruction_trace("INI")
        ho_addr, lo_addr = self._read_rr("hl")
        self._write_n_ram(self._read_io_port(self._read_r("c")), \
            ho_addr, lo_addr)
        self._write_r("b", self._read_r("b") - 1)
        self._write_rr("hl", compose_word(*self._read_rr("hl")) + 1)

        if self._read_r("b") :
            self._reset_zero_flag()
        else :
            self._set_zero_flag()

        self._set_add_substract_flag()

    def _inir(self) :
        in_byte = self._read_io_port(self._read_r("c")) 
        ho_addr, lo_addr = self._read_rr("hl")
        self._write_n_ram(ho_addr, lo_addr)
        self._write_r("b", self._read_r("b") - 1)
        self._write_rr("hl", compose_word(*self._read_rr("hl")) + 1)

        if self._read_r("b") == 0 :
            self._set_zero_flag()
            self._set_add_substract_flag()
            self._inc_n_pc(2)

    def _inc_r(self, r) :
        """
        INC r. Increment register r.
        """
        self._log_instruction_trace("INC %s" % r)
        self._inc_flag_tests(self._read_r(r), 1)
        self._write_r(r, self._read_r(r) + 1)

    def _jp_cc(self, cc) :
        if cc == self._test_zero_flag :
            trace = "JP Z, 0x%0.2X" % compose_word(*self._read_nn())
        elif cc == self._test_carry_flag :
            trace = "JP C, 0x%0.2X" % compose_word(*self._read_nn())
        elif cc == self._test_parity_overflow_flag :
            trace = "JP PE, 0x%0.2X" % compose_word(*self._read_nn())
        elif cc == self._test_sign_flag :
            trace = "JP M, 0x%0.2X" % compose_word(*self._read_nn())
        else :
            trace = "JP 0x%0.2X" % compose_word(*self._read_nn())

        self._log_instruction_trace(trace)

        if cc() :
            self._write_rr("pc", compose_word(*self._read_nn()))
            return

        self._inc_n_pc(3)

    def _jp_not_cc(self, cc) :
        if cc == self._test_zero_flag :
            trace = "JP NZ, 0x%0.2X" % compose_word(*self._read_nn())
        elif cc == self._test_carry_flag :
            trace = "JP NC, 0x%0.2X" % compose_word(*self._read_nn())
        elif cc == self._test_parity_overflow_flag :
            trace = "JP PO, 0x%0.2X" % compose_word(*self._read_nn())
        elif cc == self._test_sign_flag :
            trace = "JP P, 0x%0.2X" % compose_word(*self._read_nn())
        else :
            trace = "JP 0x%0.2X" % compose_word(*self._read_nn())

        self._log_instruction_trace(trace)

        if not cc() :
            self._write_rr("pc", compose_word(*self._read_nn()))
            return

        self._inc_n_pc(3)

    def _jp_rr(self, rr) :
        self._log_instruction_trace("JP %s" % rr)
        self._write_rr("pc", *self._read_rr(rr))

    def _jr(self) :
        ho_base_addr, lo_base_addr = self._read_rr("pc")
        ho_addr, lo_addr = compute_indexed_address(ho_base_addr, \
        lo_base_addr, self._read_n())
        self._write_rr("pc", compose_word(ho_addr, lo_addr))

    def _jr_cc(self, cc) :
        """
        JR n, cc. Jump n relative on cc (condition).
        """
        if cc == self._test_zero_flag :
            trace = "JR Z, 0x%0.2X" % compose_word(*self._read_nn())
        elif cc == self._test_carry_flag :
            trace = "JR C, 0x%0.2X" % compose_word(*self._read_nn())
        elif cc == self._test_parity_overflow_flag :
            trace = "JR PE, 0x%0.2X" % compose_word(*self._read_nn())
        elif cc == self._test_sign_flag :
            trace = "JR M, 0x%0.2X" % compose_word(*self._read_nn())
        else :
            trace = "JR 0x%0.2X" % compose_word(*self._read_nn())

        self._log_instruction_trace(trace)

        if cc() :
            self._jr()

        self._inc_n_pc(2)

    def _jr_not_cc(self, cc) :
        """
        JR n, cc. Jump n relative on NOT cc (condition).
        """
        if cc == self._test_zero_flag :
            trace = "JR NZ, 0x%0.2X" % compose_word(*self._read_nn())
        elif cc == self._test_carry_flag :
            trace = "JR NC, 0x%0.2X" % compose_word(*self._read_nn())
        elif cc == self._test_parity_overflow_flag :
            trace = "JR PO, 0x%0.2X" % compose_word(*self._read_nn())
        elif cc == self._test_sign_flag :
            trace = "JR P, 0x%0.2X" % compose_word(*self._read_nn())
        else :
            trace = "JR 0x%0.2X" % compose_word(*self._read_nn())

        self._log_instruction_trace(trace)

        if not cc() :
            self._jr()

        self._inc_n_pc(2)

    def _ld_addr_indx_d_n(self, rr) :
        """
        LD (rr + d), n. rr is either IX or IY. Load indexed addressed
        memory location (rr + d) with immediate data n.
        """
        n, d = self._read_nn()
        self._log_instruction_trace("LD (%s + 0x%0.2X), 0x%0.2X" % (rr, d, n))
        ho_base_addr, lo_base_addr = self._read_rr(rr)
        ho_addr, lo_addr = compute_indexed_address(ho_base_addr, \
            lo_base_addr, d)
        self._write_n_ram(n, ho_addr, lo_addr)

    def _ld_addr_indx_d_r(self, rr, r) :
        """
        LD (rr + d), r. rr is either IX or IY. Load indexed addressed
        memory location (rr + d) from register r.
        """
        self._log_instruction_trace("LD (%s + 0x%0.2X), %s" % (rr, self._read_n(), r))
        ho_base_addr, lo_base_addr = self._read_rr(rr)
        ho_addr, lo_addr = compute_indexed_address(ho_base_addr, \
            lo_base_addr, self._read_n())
        self._write_n_ram(self._read_r(r), ho_addr, lo_addr)

    def _ld_addr_nn_r(self, r) :
        self._log_instruction_trace("LD (0x%0.2X), %s" % \
            (compose_word(*self._read_nn()), r))
        ho_addr, lo_addr = self._read_nn()
        self._write_n_ram(self._read_r(r), ho_addr, lo_addr)

    def _ld_addr_nn_rr(self, rr) :
        """
        LD (nn), rr. Load memory locations addressed by nn from
        register pair rr.
        """
        self._log_instruction_trace("LD (0x%0.2X), %s" % \
            (compose_word(*self._read_nn()), rr))
        ho_addr, lo_addr = self._read_nn()
        ho_byte, lo_byte = self._read_rr(rr)
        self._write_nn_ram(ho_byte, lo_byte, ho_addr, lo_addr)

    def _ld_addr_rr_n(self, rr) :
        """
        LD (rr), n. Load inmediate data n into the indirectly
        addressed memory location (rr).
        """
        self._log_instruction_trace("LD (%s), 0x%0.2X" % (rr, self._read_n()))
        ho_byte, lo_byte = self._read_rr(rr)
        self._write_n_ram(self._read_n(), ho_byte, lo_byte)

    def _ld_addr_rr_r(self, rr, r) :
        """
        LD (rr), r. Load indirectly addressed memory location (rr)
        from r register.
        """
        self._log_instruction_trace("LD (%s), %s" % (rr, r))
        ho_byte, lo_byte = self._read_rr(rr)
        self._write_n_ram(self._read_r(r), ho_byte, lo_byte)

    def _ldd(self) :
        """
        LDD. Block load with decrement.
        """
        self._log_instruction_trace("LDD")
        byte = self._read_n_ram(*self._read_rr("hl"))
        self._write_n_ram(byte, *self._read_rr("de"))
        self._write_rr("de", compose_word(*self._read_rr("de")) - 1)
        self._write_rr("hl", compose_word(*self._read_rr("hl")) - 1)
        self._write_rr("bc", compose_word(*self._read_rr("bc")) - 1)

        if compose_word(*self._read_rr("bc")) :
            self._set_parity_overflow_flag()
        else :
            self._reset_parity_overflow_flag()

        # Flags sets & resets.
        self._reset_half_carry_flag()
        self._reset_add_substract_flag()

    def _lddr(self) :
        """
        LDDR. Repeating block load with decrement.
        """
        self._log_instruction_trace("LDDR")
        byte = self._read_n_ram(*self._read_rr("hl"))
        self._write_n_ram(byte, *self._read_rr("de"))
        self._write_rr("de", compose_word(*self._read_rr("de")) - 1)
        self._write_rr("hl", compose_word(*self._read_rr("hl")) - 1)
        self._write_rr("bc", compose_word(*self._read_rr("bc")) - 1)

        if compose_word(*self._read_rr("bc")) :
            self._dec_n_pc(2)
        else :
            # Flags sets & resets.
            self._reset_half_carry_flag()
            self._reset_parity_overflow_flag()
            self._reset_add_substract_flag()

    def _ldi(self) :
        """
        LDI. Block load with increment.
        """
        self._log_instruction_trace("LDI")
        byte = self._read_n_ram(*self._read_rr("hl"))
        self._write_n_ram(byte, *self._read_rr("de"))
        self._write_rr("de", compose_word(*self._read_rr("de")) + 1)
        self._write_rr("hl", compose_word(*self._read_rr("hl")) + 1)
        self._write_rr("bc", compose_word(*self._read_rr("bc")) - 1)

        if compose_word(*self._read_rr("bc")) :
            self._set_parity_overflow_flag()
        else :
            self._reset_parity_overflow_flag()

        # Flags sets & resets.
        self._reset_half_carry_flag()
        self._reset_add_substract_flag()

    def _ldir(self) :
        """
        LDIR. Repeating block load with increment.
        """
        self._log_instruction_trace("LDIR")
        byte = self._read_n_ram(*self._read_rr("hl"))
        self._write_n_ram(byte, *self._read_rr("de"))
        self._write_rr("de", compose_word(*self._read_rr("de")) + 1)
        self._write_rr("hl", compose_word(*self._read_rr("hl")) + 1)
        self._write_rr("bc", compose_word(*self._read_rr("bc")) - 1)

        if compose_word(*self._read_rr("bc")) :
            self._dec_n_pc(2)
        else :
            # Flags sets & resets.
            self._reset_half_carry_flag()
            self._reset_parity_overflow_flag()
            self._reset_add_substract_flag()

    def _ld_r_addr_indx_d(self, r, rr) :
        self._log_instruction_trace("LD %s, (%s + 0x%0.2X)" % \
            (r, rr, self._read_n()))
        ho_base_addr, lo_base_addr = self._read_rr(rr)
        ho_addr, lo_addr = compute_indexed_address(ho_base_addr, \
        lo_base_addr, self._read_n())
        self._write_r(r, self._read_n_ram(ho_addr, lo_addr))

    def _ld_r_addr_nn(self, r) :
        """
        LD r, (nn). Load register r from memory location (nn).
        """
        self._log_instruction_trace("LD %s, (0x%0.2X)" % \
            (r, compose_word(*(self._read_nn()))))
        ho_byte, lo_byte = self._read_nn()
        self._write_r(r, self._read_n_ram(ho_byte, lo_byte))

    def _ld_r_addr_rr(self, r, rr) :
        """
        LD r, (rr). Load register r from the memory location
        indirectly addressed by the rr register pair.
        """
        self._log_instruction_trace("LD %s, (%s)" % (r, rr))
        ho_byte, lo_byte = self._read_rr(rr)
        self._write_r(r, self._read_n_ram(*self._read_rr(rr)))

    def _ld_r_n(self, r) :
        """
        LD r, n. Load register r with inmediate data n.
        """
        self._log_instruction_trace("LD %s, 0x%0.2X" % (r, self._read_n()))
        self._write_r(r, self._read_n())

    def _ld_rr_addr_nn(self, rr) :
        """
        LD rr, (nn). Load register pair rr from memory locations
        addressed by nn.
        """
        self._log_instruction_trace("LD %s, (0x%0.2X)" % (rr, \
            compose_word(*self._read_nn())))
        ho_addr, lo_addr = self._read_nn()
        ho_byte, lo_byte = self._read_nn_ram(ho_addr, lo_addr)
        self._write_rr(rr, compose_word(ho_byte, lo_byte))

    def _ld_rr_nn(self, rr) :
        """
        LD rr, nn. Load register pair rr with inmediate data nn.
        """
        self._log_instruction_trace("LD %s, 0x%0.2X" % (rr, \
            compose_word(*self._read_nn())))
        self._write_rr(rr, compose_word(*self._read_nn()))

    def _ld_rr_rr(self, rr1, rr2) :
        """
        LD rr1, rr2. Load register pair rr1 from register rr2.
        """
        self._log_instruction_trace("LD %s, %s" % (rr1, rr2))
        ho_byte, lo_byte = self._read_rr(rr2)
        self._write_rr(rr1, compose_word(ho_byte, lo_byte))

    def _ld_r_r(self, r1, r2) :
        """
        LD r1, r2. Load register r1 from register r2.
        """
        self._log_instruction_trace("LD %s, %s" % (r1, r2))
        self._write_r(r1, self._read_r(r2))

    def _neg(self) :
        """ NEG. Negates the accumulator. """

        # Affects : S, Z, H, P, C. 
        # Sets : N.
        self._log_instruction_trace("NEG")

        if self._read_r("a") == 0x0 :
            self._set_carry_flag()
        else :
            self._reset_carry_flag()

        if self._read_r("a") == 0x80 :
            self._set_parity_overflow_flag()
        else :
            self._reset_parity_overflow_flag()

        self._write_r("a", twos_complement_byte(self._read_r("a")))
        self._test_and_set_sign_flag(self._read_r("a"))
        self._test_and_set_zero_flag(self._read_r("a"))
        self._set_add_substract_flag()

    def _nop(self) :
        """ NOP. No operation. """
        self._log_instruction_trace("NOP")

    def _or_flag_tests(self, n) :
        self._test_and_set_sign_flag(n)
        self._test_and_set_zero_flag(n)
        self._test_and_set_parity_flag(n)
        self._reset_half_carry_flag()
        self._reset_add_substract_flag()
        self._reset_carry_flag()

    def _or_addr_indx_d(self, rr) :
        """
        OR (rr + d).
        """
        self._log_instruction_trace("OR (%s + 0x%0.2X)" % \
            (rr, self._read_n()))
        ho_base_addr, lo_base_addr = self._read_rr()
        ho_addr, lo_addr = compute_indexed_address(ho_base_addr, \
            lo_base_addr, self._read_n())
        self._or_flag_tests(self._read_r("a") | \
            self._read_n_ram(ho_addr, lo_addr))
        self._write_r("a", self._read_r("a") | \
        self._read_n_ram(ho_addr, lo_addr))

    def _or_addr_rr(self, rr) :
        """
        OR (rr).
        """
        self._log_instruction_trace("OR (%s)" % rr)
        self._or_flag_tests(self._read_r("a") | \
            self._read_n_ram(*self._read_rr(rr)))
        self._write_r("a", self._read_r("a") | \
            self._read_n_ram(*self._read_rr(rr)))

    def _or_n(self) :
        self._log_instruction_trace("OR 0x%0.2X" % self._read_n())
        self._or_flag_tests(self._read_r("a") | self._read_n())
        self._write_r("a", self._read_r("a") | self._read_n())

    def _or_r(self, r) :
        self._log_instruction_trace("OR %s" % r)
        self._or_flag_tests(self._read_r("a") | self._read_r(r))
        self._write_r("a", self._read_r("a") | self._read_r(r))

    def _otdr(self) :
        pass

    def _otir(self) :
        out_byte = self._read_n_ram(*self._read_rr(rr))
        self._write_io_port(self._read_r("c"), out_byte)
        self._write_r("b", self._read_r("b") - 1)
        self._write_rr("hl", compose_word(*self._read_rr("hl")) + 1)

        if self._read_r("b") == 0 :
            self._set_zero_flag()
            self._set_add_substract_flag()
            self._inc_n_pc(2)

    def _out_addr_n_r(self, r) :
        self._log_instruction_trace("OUT (0x%0.2X), %s" % (self._read_n(), r))
        self._write_io_port(self._read_n(), self._read_r(r))

    def _out_addr_r_n(self, r, n) :
        self._log_instruction_trace("OUT (%s), 0x%0.2X" % (r, n))
        self._write_io_port(self._read_r(r), n)

    def _out_addr_r_r(self, r1, r2) :
        self._log_instruction_trace("OUT (%s), %s" % (r1, r2))
        self._write_io_port(self._read_r(r1), self._read_r(r2))

    def _outd(self) :
        """ OUTD. Output with decrement. """

        self._log_instruction_trace("OUTD")
        out_byte = self._read_n_ram(*self._read_rr("hl"))
        self._write_io_port(self._read_r("c"), out_byte)
        self._write_r("b", self._read_r("b") - 1)
        self._write_rr("hl", compose_word(*self._read_rr("hl")) + 1)

        if self._read_r("b") :
            self._reset_zero_flag()
        else :
            self._set_zero_flag()

        self._set_add_substract_flag()

    def _outi(self) :
        """ OUTI. Output with increment. """

        self._log_instruction_trace("OUTI")
        out_byte = self._read_n_ram(*self._read_rr("hl"))
        self._write_io_port(self._read_r("c"), out_byte)
        self._write_r("b", self._read_r("b") - 1)
        self._write_rr("hl", compose_word(*self._read_rr("hl")) + 1)

        if self._read_r("b") :
            self._reset_zero_flag()
        else :
            self._set_zero_flag()

        self._set_add_substract_flag()

    def _pop_rr(self, rr) :
        """
        POP rr. Pop register pair rr from stack.
        """
        self._log_instruction_trace("POP %s" % rr)
        ho_byte, lo_byte = self._read_nn_stack()
        self._write_rr(rr, compose_word(ho_byte, lo_byte))

    def _push_rr(self, rr) :
        """ PUSH rr. Pushes rr register pair onto stack. """

        self._log_instruction_trace("PUSH %s" % rr)
        ho_byte, lo_byte = self._read_rr(rr)
        self._write_nn_stack(ho_byte, lo_byte)

    def _res_n_addr_rr(self, n, rr) :
        """ RES n, (rr). Resets bit n of r register. """

        self._log_instruction_trace("RES 0x%0.2X, (%s)" % (n, rr))
        byte = self._read_n_ram(*(self._read_rr(rr))) & n
        self._write_r(r, byte)

    def _res_n_indx_d(self, n, rr) :
        self._log_instruction_trace("RES 0x%0.2X, (%s + 0x%0.2X)" % \
            (n, rr, self._read_n()))
        ho_base_addr, lo_base_addr = self._read_rr(rr)
        ho_addr, lo_addr = compute_indexed_address(ho_base_addr, \
            lo_base_addr, self._read_n())
        self._write_n_ram(self._read_n_ram(ho_addr, lo_addr) & n, \
            ho_addr, lo_addr)
   
    def _res_n_indx_d_r(self, n, rr, r) :
        """
        RES n, (rr + d), r. 
        """
        self._log_instruction_trace("RES 0x%0.2X, (%s + 0x%0.2X), %s" % \
            (n, rr, self._read_n(), r))
        ho_base_addr, lo_base_addr = self._read_rr(rr)
        ho_addr, lo_addr = compute_indexed_address(ho_base_addr, \
            lo_base_addr, self._read_n())
        self._write_r(r, self._read_r(r) & n)
        self._write_n_ram(self._read_r(r) & n, ho_addr, lo_addr)

    def _res_n_r(self, n, r) :
        """ RES n, r. Resets bit n of r. """

        self._log_instruction_trace("RES 0x%0.2X, %s" % (n, r))
        self._write_r(r, self._read_r(r) & n)

    def _ret_cc(self, cc) :
        self._log_instruction_trace("RET")

        if cc() :
            ho_addr, lo_addr = self._read_nn_stack()
            self._write_rr("pc", compose_word(ho_addr, lo_addr))
            return

        self._inc_pc()

    def _reti(self) :
        """ RETI. Return from interrupt. """

        self._log_instruction_trace("RETI")
        self._write_rr("pc", compose_word(*self._read_nn_stack()))

    def _retn(self) :
        """ RETN. Return from non-maskable interrupt. """

        self._log_instruction_trace("RETN")
        self._write_rr("pc", compose_word(*self._read_nn_stack()))
        self._write_r("iff1", self._read_r("iff2"))

    def _ret_not_cc(self, cc) :
        self._log_instruction_trace("RET")

        if not cc() :
            ho_addr, lo_addr = self._read_nn_stack()
            self._write_rr("pc", compose_word(ho_addr, lo_addr))
            return

        self._inc_pc()

    def _rl_flag_tests(self, n) :
        self._test_and_set_sign_flag(n)
        self._test_and_set_zero_flag(n)
        self._test_and_set_parity_flag(n)
        self._reset_half_carry_flag()
        self._reset_add_substract_flag()

    def _rl_addr_rr(self, rr) :
        """
        RL (rr). Rotate left through carry operand r.
        """
        # Affects : S, Z, P, C.
        # Resets : H, N.
        self._log_instruction_trace("RL (%s)" % rr)
        ho_addr, lo_addr = self._read_rr(rr)
        byte = self._read_n_ram(ho_addr, lo_addr)

        if self._test_carry_flag() :
            self._write_n_ram(rotate_left_byte(byte, 1) | 0x1, \
                ho_addr, lo_addr)
        else :
            self._write_n_ram(rotate_left_byte(byte, 1) & 0xFE, \
                ho_addr, lo_addr)

        if byte & 0x80 :
            self._set_carry_flag()
        else :
            self._reset_carry_flag()

        self._rl_flag_tests(self._read_n_ram(ho_addr, lo_addr))

    def _rl_indx_d(self, rr) :
        """
        RL (rr + d). Rotate left through carry operand r &
        store result at address (rr + d).
        """
        # Affects : S, Z, P, C.
        # Resets : H, N.
        self._log_instruction_trace("RL (%s + 0x%0.2X)" % (rr, self._read_n()))
        ho_base_addr, lo_base_addr = self._read_rr(rr)
        ho_addr, lo_addr = compute_indexed_address(ho_base_addr, \
            lo_base_addr, self._read_n())
        byte = self._read_n_ram(ho_addr, lo_addr)

        if self._test_carry_flag() :
            self._write_n_ram(rotate_left_byte(byte, 1) | 0x1, \
                ho_addr, lo_addr)
        else :
            self._write_n_ram(rotate_left_byte(byte, 1) & 0xFE, \
                ho_addr, lo_addr)

        if byte & 0x80 :
            self._set_carry_flag()
        else :
            self._reset_carry_flag()

        self._rl_flag_tests(self._read_n_ram(ho_addr, lo_addr))

    def _rl_indx_d_r(self, rr, r) :
        """
        RL (rr + d), r. Rotate left through carry operand r &
        store result at address (rr + d).
        """
        # Affects : S, Z, P, C.
        # Resets : H, N.
        self._log_instruction_trace("RL (%s + 0x%0.2X), %s" % (rr, self._read_n(), r))
        ho_base_addr, lo_base_addr = self._read_rr(rr)
        ho_addr, lo_addr = compute_indexed_address(ho_base_addr, \
            lo_base_addr, self._read_n())
        byte = self._read_r(r)
        self._write_r(r, rotate_left_byte(self._read_r(r), 1))

        if self._test_carry_flag() :
            self._write_r(r, self._read_r(r) | 0x1)
        else :
            self._write_r(r, self._read_r(r) & 0xFE)

        self._write_n_ram(self._read_r(r), ho_addr, lo_addr)

        if byte & 0x80 :
            self._set_carry_flag()
        else :
            self._reset_carry_flag()

        # WARNING !!! Probar este cambio. 
        #self._write_n_ram(self._read_r(r), ho_addr, lo_addr)

        self._rl_flag_tests(self._read_r(r))

    def _rl_r(self, r) :
        """
        RL r. Rotate left through carry operand r.
        """
        # Affects : S, Z, P, C.
        # Resets : H, N.
        self._log_instruction_trace("RL %s" % r)
        byte = self._read_r(r)
        self._write_r(r, rotate_left_byte(self._read_r(r), 1))
        
        if self._test_carry_flag() :
            self._write_r(r, self._read_r(r) | 0x1)
        else :
            self._write_r(r, self._read_r(r) & 0xFE)

        if byte & 0x80 :
            self._set_carry_flag()
        else :
            self._reset_carry_flag()

        self._rl_flag_tests(self._read_r(r))

    def _rla(self) :
        """
        RLA. Rotate accumulator left through carry flag.
        """
        # Affects : C.
        # Resets : H, N.
        self._log_instruction_trace("RLA")
        self._write_r("a", rotate_left_byte(self._read_r("a"), 1))
        lsb = self._read_r("a") & 0x1
        carry_flag = self._test_carry_flag()

        if lsb :
            self._set_carry_flag()
        else :
            self._reset_carry_flag()

        if carry_flag :
            self._write_r("a", self._read_r("a") | 0x1)

        self._reset_half_carry_flag()
        self._reset_add_substract_flag()

    def _rlc_addr_rr(self, rr) :
        """
        RLC (rr). Rotate the byte (pointed by (rr)) left with branch carry.
        Store back the result to that location.
        """
        # Affects : S, Z, P, C.
        # Resets : H, N.
        self._log_instruction_trace("RLC (%s)" % rr)

        if self._read_n_ram(*self._read_rr(rr)) & 0x8 :
            self._set_carry_flag()
        else :
            self._reset_carry_flag()

        byte = self._read_n_ram(*self._read_rr(rr))
        byte = rotate_left_byte(byte, 1)
        self._write_n_ram(byte, *self._read_rr(rr))

        # Flag tests.
        self._test_and_set_sign_flag(byte)
        self._test_and_set_zero_flag(byte)
        self._test_and_set_parity_flag(byte)

        # Flag sets & resets.
        self._reset_half_carry_flag()
        self._reset_add_substract_flag()

    def _rlc_indx_d(self, rr) :
        """
        RLC (rr + d). Rotate byte at (rr + d) left with branch carry &
        store result at address (rr + d).
        """
        # Affects : S, Z, P, C.
        # Resets : H, N.
        self._log_instruction_trace("RLC (%s + %d)" % (rr, self._read_n()))
        ho_base_addr, lo_base_addr = self._read_rr(rr)
        ho_addr, lo_addr = compute_indexed_address(ho_base_addr, \
            lo_base_addr, self._read_n())

        if self._read_n_ram(ho_addr, lo_addr) & 0x8 :
            self._set_carry_flag()
        else :
            self._reset_carry_flag()

        byte = self._read_n_ram(ho_addr, lo_addr)
        byte = rotate_left_byte(byte, 1)
        self._write_n_ram(byte, ho_addr, lo_addr)

        # Flag tests.
        self._test_and_set_sign_flag(byte)
        self._test_and_set_zero_flag(byte)
        self._test_and_set_parity_flag(byte)

        # Flag sets & resets.
        self._reset_half_carry_flag()
        self._reset_add_substract_flag()

    def _rlc_indx_d_r(self, rr, r) :
        """
        RLC (rr + d), r. Rotate register r left with branch carry &
        store result at address (rr + d).
        """
        # Affects : S, Z, P, C.
        # Resets : H, N.
        self._log_instruction_trace("RLC (%s + 0x%0.2X), %s" % (rr, self._read_n(), r))

        if self._read_r(r) & 0x8 :
            self._set_carry_flag()
        else :
            self._reset_carry_flag()

        ho_base_addr, lo_base_addr = self._read_rr(rr)
        ho_addr, lo_addr = compute_indexed_address(ho_base_addr, \
            lo_base_addr, self._read_n())
        self._write_r(r, rotate_left_byte(self._read_r(r), 1))
        self._write_n_ram(self._read_r(r), ho_addr, lo_addr)

        # Flag tests.
        self._test_and_set_sign_flag(self._read_r(r))
        self._test_and_set_zero_flag(self._read_r(r))
        self._test_and_set_parity_flag(self._read_r(r))

        # Flag sets & resets.
        self._reset_half_carry_flag()
        self._reset_add_substract_flag()

    def _rlc_r(self, r) :
        """
        RLC r. Rotate register r left with branch carry.
        """
        # Affects : S, Z, P, C.
        # Resets : H, N.
        self._log_instruction_trace("RLC %s" % r)

        if self._read_r(r) & 0x8 :
            self._set_carry_flag()
        else :
            self._reset_carry_flag()

        self._write_r(r, rotate_left_byte(self._read_r(r), 1))

        # Flag tests.
        self._test_and_set_sign_flag(self._read_r(r))
        self._test_and_set_zero_flag(self._read_r(r))
        self._test_and_set_parity_flag(self._read_r(r))

        # Flag sets & resets.
        self._reset_half_carry_flag()
        self._reset_add_substract_flag()

    def _rlca(self) :
        """
        RLCA. Rotate accumulator left with branch carry.
        """
        # Affects : C.
        # Resets : H, N.
        self._log_instruction_trace("RLCA")
        self._write_r("a", rotate_left_byte(self._read_r("a"), 1))

        if self._read_r("a") & 0x1 :
            self._set_carry_flag()
        else :
            self._reset_carry_flag()

        # Flags sets & resets.
        self._reset_half_carry_flag()
        self._reset_add_substract_flag()

    def _rr_addr_rr(self, rr) :
        """
        RR (rr). Rotate right r through carry.
        """
        # Affects : S, Z, P, C.
        # Resets : H, N.
        self._log_instruction_trace("RR (%s)" % rr)
        ho_addr, lo_addr = self._read_rr(rr)
        byte = self._read_n_ram(ho_addr, lo_addr)

        if self._test_carry_flag() :
            self._write_n_ram(rotate_right_byte(byte, 1) | 0x80, \
                ho_addr, lo_addr)
        else :
            self._write_n_ram(rotate_right_byte(byte, 1) & 0x7F, \
                ho_addr, lo_addr)

        if byte & 0x1 :
            self._set_carry_flag()
        else :
            self._reset_carry_flag()

        # Flag tests.
        self._test_and_set_sign_flag(self._read_n_ram(ho_addr, lo_addr))
        self._test_and_set_zero_flag(self._read_n_ram(ho_addr, lo_addr))
        self._test_and_set_parity_flag(self._read_n_ram(ho_addr, lo_addr))

        # Flag sets & resets.
        self._reset_half_carry_flag()
        self._reset_add_substract_flag()

    def _rr_indx_d(self, rr) :
        """
        RR (rr + d). Rotate right through carry operand r &
        store result at address (rr + d).
        """
        # Affects : S, Z, P, C.
        # Resets : H, N.

        self._log_instruction_trace("RR (%s + 0x%0.2X)" % (rr, self._read_n()))
        ho_base_addr, lo_base_addr = self._read_rr(rr)
        ho_addr, lo_addr = compute_indexed_address(ho_base_addr, \
            lo_base_addr, self._read_n())
        byte = self._read_n_ram(ho_addr, lo_addr)

        if self._test_carry_flag() :
            self._write_n_ram(rotate_right_byte(byte, 1) | 0x80, \
                ho_addr, lo_addr)
        else :
            self._write_n_ram(rotate_right_byte(byte, 1) & 0x7F, \
                ho_addr, lo_addr)

        if byte & 0x1 :
            self._set_carry_flag()
        else :
            self._reset_carry_flag()

        # Flag tests.
        self._test_and_set_sign_flag(self._read_n_ram(ho_addr, lo_addr))
        self._test_and_set_zero_flag(self._read_n_ram(ho_addr, lo_addr))
        self._test_and_set_parity_flag(self._read_n_ram(ho_addr, lo_addr))

        # Flag sets & resets.
        self._reset_half_carry_flag()
        self._reset_add_substract_flag()

    def _rr_indx_d_r(self, rr, r) :
        """
        RR (rr + d), r. Rotate right through carry operand r &
        store result at address (rr + d).
        """
        # Affects : S, Z, P, C.
        # Resets : H, N.

        self._log_instruction_trace("RR (%s + 0x%0.2X), %s" % (rr, self._read_n(), r))
        ho_base_addr, lo_base_addr = self._read_rr(rr)
        ho_addr, lo_addr = compute_indexed_address(ho_base_addr, \
            lo_base_addr, self._read_n())
        byte = self._read_r(r)
        self._write_r(r, rotate_right_byte(self._read_r(r), 1))

        if self._test_carry_flag() :
            self._write_r(r, self._read_r(r) | 0x80)
        else :
            self._write_r(r, self._read_r(r) & 0x7F)

        if byte & 0x1 :
            self._set_carry_flag()
        else :
            self._reset_carry_flag()

        self._write_n_ram(self._read_r(r), ho_addr, lo_addr)

        # Flag tests.
        self._test_and_set_sign_flag(self._read_r(r))
        self._test_and_set_zero_flag(self._read_r(r))
        self._test_and_set_parity_flag(self._read_r(r))

        # Flag sets & resets.
        self._reset_half_carry_flag()
        self._reset_add_substract_flag()

    def _rr_r(self, r) :
        """
        RR r. Rotate right r through carry.
        """
        # Affects : S, Z, P, C.
        # Resets : H, N.
        self._log_instruction_trace("RR %s" % r)
        byte = self._read_r(r)
        self._write_r(r, rotate_right_byte(self._read_r(r), 1))

        if self._test_carry_flag() :
            self._write_r(r, self._read_r(r) | 0x80)
        else :
            self._write_r(r, self._read_r(r) & 0x7F)

        if byte & 0x1 :
            self._set_carry_flag()
        else :
            self._reset_carry_flag()

        # Flag tests.
        self._test_and_set_sign_flag(self._read_r(r))
        self._test_and_set_zero_flag(self._read_r(r))
        self._test_and_set_parity_flag(self._read_r(r))

        # Flag sets & resets.
        self._reset_half_carry_flag()
        self._reset_add_substract_flag()

    def _rra(self) :
        """
        RRA. Rotate accumulator right through carry flag.
        """
        # Affects : C.
        # Resets : H, N.
        self._log_instruction_trace("RRA")
        self._write_r("a", rotate_right_byte(self._read_r("a"), 1))
        lsb = self._read_r("a") & 0x1
        carry_flag = self._test_carry_flag()

        if lsb :
            self._set_carry_flag()
        else :
            self._reset_carry_flag()

        if carry_flag :
            self._write_r("a", self._read_r("a") | 0x1)

        # Flags sets & resets.
        self._reset_half_carry_flag()
        self._reset_add_substract_flag()

    def _rrc_addr_rr(self, rr) :
        """
        RRC (rr). Rotate the byte (pointed by (rr)) right with branch carry.
        Store back the result to that location.
        """
        # Affects : S, Z, P, C.
        # Resets : H, N.
        self._log_instruction_trace("RRC (%s)" % rr)

        if self._read_n_ram(*self._read_rr(rr)) & 0x1 :
            self._set_carry_flag()
        else :
            self._reset_carry_flag()

        byte = self._read_n_ram(*self._read_rr(rr))
        byte = rotate_right_byte(byte, 1)
        self._write_n_ram(byte, *self._read_rr(rr))

        # Flag tests.
        self._test_and_set_sign_flag(byte)
        self._test_and_set_zero_flag(byte)
        self._test_and_set_parity_flag(byte)

        # Flag sets & resets.
        self._reset_half_carry_flag()
        self._reset_add_substract_flag()

    def _rrc_indx_d(self, rr) :
        """
        RRC (rr + d). Rotate byte at (rr + d) right with branch carry &
        store result at (rr + d) location.
        """
        # Affects : S, Z, P, C.
        # Resets : H, N.
        self._log_instruction_trace("RRC (%s + 0x%0.2X)" % (rr, self._read_n()))
        ho_base_addr, lo_base_addr = self._read_rr(rr)
        ho_addr, lo_addr = compute_indexed_address(ho_base_addr, \
            lo_base_addr, self._read_n())

        if self._read_n_ram(ho_addr, lo_addr) & 0x1 :
            self._set_carry_flag()
        else :
            self._reset_carry_flag()

        byte = self._read_n_ram(ho_addr, lo_addr)
        byte = rotate_right_byte(byte, 1)
        self._write_n_ram(byte, ho_addr, lo_addr)

        # Flag tests.
        self._test_and_set_sign_flag(byte)
        self._test_and_set_zero_flag(byte)
        self._test_and_set_parity_flag(byte)

        # Flag sets & resets.
        self._reset_half_carry_flag()
        self._reset_add_substract_flag()

    def _rrc_indx_d_r(self, r) :
        """
        RRC (rr + d), r. Rotate register r right with branch carry &
        store result at (rr + d) location.
        """
        # Affects : S, Z, P, C.
        # Resets : H, N.
        self._log_instruction_trace("RRC (%s + 0x%0.2X), %s" % (rr, self._read_n(), r))

        if self._read_r(r) & 0x1 :
            self._set_carry_flag()
        else :
            self._reset_carry_flag()

        ho_base_addr, lo_base_addr = self._read_rr(rr)
        ho_addr, lo_addr = compute_indexed_address(ho_base_addr, \
            lo_base_addr, self._read_n())
        self._write_r(r, rotate_right_byte(self._read_r(r), 1))
        self._write_n_ram(self._read_r(r), ho_addr, lo_addr)

        # Flag tests.
        self._test_and_set_sign_flag(self._read_r(r))
        self._test_and_set_zero_flag(self._read_r(r))
        self._test_and_set_parity_flag(self._read_r(r))

        # Flag sets & resets.
        self._reset_half_carry_flag()
        self._reset_add_substract_flag()

    def _rrc_r(self, r) :
        """
        RRC r. Rotate right with branch carry.
        """
        # Affects : S, Z, P, C.
        # Resets : H, N.
        self._log_instruction_trace("RRC %s" % r)

        if self._read_r(r) & 0x1 :
            self._set_carry_flag()
        else :
            self._reset_carry_flag()

        self._write_r(r, rotate_right_byte(self._read_r(r), 1))

        # Flag tests.
        self._test_and_set_sign_flag(self._read_r(r))
        self._test_and_set_zero_flag(self._read_r(r))
        self._test_and_set_parity_flag(self._read_r(r))

        # Flag sets & resets.
        self._reset_half_carry_flag()
        self._reset_add_substract_flag()

    def _rrca(self) :
        """
        RRCA. Rotate accumulator right with branch carry.
        """
        # Affects : C.
        # Resets : H, N.
        self._log_instruction_trace("RRCA")

        if self._read_r("a") & 0x1 :
            self._set_carry_flag()
        else :
            self._reset_carry_flag()

        self._write_r("a", rotate_right_byte(self._read_r("a"), 1))

        # Flag sets & resets.
        self._reset_half_carry_flag()
        self._reset_add_substract_flag()

    def _rld(self) :
        """
        RLD. Rotate left decimal.
        """
        self._log_instruction_trace("RLD")
        byte = self._read_n_ram(*self._read_rr("hl"))
        ho_nibble, lo_nibble = decompose_byte(byte)
        ho_a, lo_a = decompose_byte(self._read_r("a"))
        self._write_r("a", compose_byte(ho_a, ho_nibble))
        self._write_n_ram(compose_byte(lo_nibble, lo_a), *self._read_rr("hl"))

    def _rrd(self) :
        """
        RRD. Rotate right decimal.
        """
        self._log_instruction_trace("RRD")
        byte = self._read_n_ram(*self._read_rr("hl"))
        ho_nibble, lo_nibble = decompose_byte(byte)
        ho_a, lo_a = decompose_byte(self._read_r("a"))
        self._write_r("a", compose_byte(ho_a, lo_nibble))
        self._write_n_ram(compose_byte(lo_a, ho_nibble), *self._read_rr("hl"))

    def _rst(self, lo_addr) :
        """
        RST. Restart at lo_addr.
        """
        self._log_instruction_trace("RST 0x%0.2X" % lo_addr)
        self._write_nn_stack(*self._read_rr("pc"))
        self._write_rr("pc", compose_word(0x0, lo_addr))

    #def _sbc_flag_tests(self, n, m) :
    #    # Affects : S, Z, H, P, C
    #    # Sets : N.
    #    l = n - m
    #    self._test_and_set_sign_flag(l)
    #    self._test_and_set_zero_flag(l)
    #    self._test_and_set_half_carry_on_substract(n, m)
    #    #self._test_and_set_overflow_flag(n, m)
    #    self._test_and_set_carry_flag(l)
    #    self._set_add_substract_flag()

    def _sbc_r_addr_indx_d(self, r, rr) :
        self._log_instruction_trace("SBC %s, (%s + 0x%0.2X)" % \
            (r, rr, self._read_n()))
        ho_base_addr, lo_base_addr = self._read_rr(rr)
        ho_addr, lo_addr = compute_indexed_address(ho_base_addr, \
            lo_base_addr, self._read_n())
        byte = self._read_r(r) - self._read_n_ram(ho_addr, lo_addr) - \
            self._test_carry_flag()

        #self._sbc_flag_tests(self._read_r(r), \
        #    self._read_n_ram(ho_addr, lo_addr) - self._test_carry_flag())

        ## Flag tests.
        self._test_and_set_sign_flag(byte)
        self._test_and_set_zero_flag(byte)
        self._test_and_set_half_carry_on_substract(self._read_r(r), \
            self._read_n_ram(ho_addr, lo_addr) - self._test_carry_flag())
        self._test_and_set_overflow_flag(self._read_r(r), \
            self._read_n_ram(ho_addr, lo_addr) - self._test_carry_flag(), "SUB")
        self._test_and_set_carry_flag(byte)

        # Flags sets & resets.
        self._set_add_substract_flag()
        self._write_r(r, byte)

    def _sbc_r_addr_rr(self, r, rr) :
        self._log_instruction_trace("SBC %s, 0x%0.2X" % (r, rr))
        byte = self._read_r(r) - self._read_n_ram(*self._read_rr(rr)) - \
            self._test_carry_flag()

        #self._sbc_flag_tests(self._read_r(r), \
        #    self._read_n_ram(*self._read_rr(rr)) - self._test_carry_flag())

        # Flag tests.
        self._test_and_set_sign_flag(byte)
        self._test_and_set_zero_flag(byte)
        self._test_and_set_half_carry_on_substract(self._read_r(r), \
            self._read_n_ram(*self._read_rr(rr)) - self._test_carry_flag())
        self._test_and_set_overflow_flag(self._read_r(r), \
            self._read_n_ram(*self._read_rr(rr)) - self._test_carry_flag(), "SUB")
        self._test_and_set_carry_flag(byte)

        # Flags sets & resets.
        self._set_add_substract_flag()
        self._write_r(r, byte)

    def _sbc_r_n(self, r) :
        self._log_instruction_trace("SBC %s, 0x%0.2X" % (r, self._read_n()))
        byte = self._read_r(r) - self._read_n() - self._test_carry_flag()

        #self._sbc_flag_tests(self._read_r(r), \
        #    self._read_n() - self._test_carry_flag())

        # Flag tests.
        self._test_and_set_sign_flag(byte)
        self._test_and_set_zero_flag(byte)
        self._test_and_set_half_carry_on_substract(self._read_r(r), \
            self._read_n() - self._test_carry_flag())
        self._test_and_set_overflow_flag(self._read_r(r), \
            self._read_n() - self._test_carry_flag(), "SUB")
        self._test_and_set_carry_flag(byte)

        # Flags sets & resets.
        self._set_add_substract_flag()
        self._write_r(r, byte)

    def _sbc_r_r(self, r1, r2) :
        self._log_instruction_trace("SBC %s, %s" % (r1, r2))
        byte = self._read_r(r1) - self._read_r(r2) - self._test_carry_flag()

        #self._sbc_flag_tests(self._read_r(r1), \
        #    self._read_r(r2) - self._test_carry_flag())

        # Flag tests.
        self._test_and_set_sign_flag(byte)
        self._test_and_set_zero_flag(byte)
        self._test_and_set_half_carry_on_substract(self._read_r(r1), \
            self._read_r(r2) - self._test_carry_flag())
        self._test_and_set_overflow_flag(self._read_r(r1), \
            self._read_r(r2) - self._test_carry_flag(), "SUB")
        self._test_and_set_carry_flag(byte)

        # Flags sets & resets.
        self._set_add_substract_flag()
        self._write_r(r1, byte)

    def _sbc_word_flag_tests(self, n, m) :
        # Affects : S, Z, H, P, C
        # Resets : N.
        sub = n - m
        self._test_and_set_sign_flag_word(sub)
        self._test_and_set_zero_flag_word(sub)
        self._test_and_set_half_carry_on_substract_word(n, m)
        self._test_and_set_overflow_flag_word(n, m, "SUB")
        self._test_and_set_carry_flag_word(sub)
        self._set_add_substract_flag()

    def _sbc_rr_rr(self, rr1, rr2) :
        self._log_instruction_trace("SBC %s, %s" % (rr1, rr2))
        word_rr1 = compose_word(*self._read_rr(rr1))
        word_rr2 = compose_word(*self._read_rr(rr2))
        carry = self._test_carry_flag()
        self._sbc_word_flag_tests(word_rr1, word_rr2 - carry)
        self._write_rr(rr1, sub_words(word_rr1, word_rr2, carry))

    def _scf(self) :
        """
        SCF. Set carry flag.
        """
        # Sets : C.
        # Resets : H, N.
        self._log_instruction_trace("SCF")
        self._set_carry_flag()
        self._reset_half_carry_flag()
        self._reset_add_substract_flag()

    def _set_n_addr_rr(self, n, rr) :
        """
        SET n, (rr). Sets bit n of r.
        """
        self._log_instruction_trace("SET 0x%0.2X, (%s)" % (n, rr))
        byte = self._read_n_ram(*self._read_rr(rr)) | n
        self._write_r(r, byte)

    def _set_n_indx_d(self, n, rr) :
        """
        SET n, (rr + d).
        """
        self._log_instruction_trace("SET 0x%0.2X, (%s + 0x%0.2X)" % (n, rr, self._read_n()))
        ho_base_addr, lo_base_addr = self._read_rr(rr)
        ho_addr, lo_addr = compute_indexed_address(ho_base_addr, \
            lo_base_addr, self._read_n())
        self._write_n_ram(self._read_n_ram(ho_addr, lo_addr) | n, \
            ho_addr, lo_addr)

    def _set_n_indx_d_r(self, n, rr, r) :
        """
        SET n, (rr + d), r. 
        """
        self._log_instruction_trace("SET 0x%0.2X, (%s + 0x%0.2X), %s" % (n, rr, self._read_n(), r))
        ho_base_addr, lo_base_addr = self._read_rr(rr)
        ho_addr, lo_addr = compute_indexed_address(ho_base_addr, \
            lo_base_addr, self._read_n())
        self._write_r(r, self._read_r(r) | n)
        self._write_n_ram(self._read_r(r) | n, ho_addr, lo_addr)

    def _set_n_r(self, n, r) :
        """
        SET n, r. Sets bit n of r.
        """
        self._log_instruction_trace("SET 0x%0.2X, %s" % (n, r))
        self._write_r(r, self._read_r(r) | n)

    def _sla_addr_rr(self, rr) :
        """
        SLA (rr). Arithmetic shift left r.
        """
        # Affects : S, Z, P, C.
        # Resets : H, N.
        self._log_instruction_trace("SLA (%s)" % rr)
        ho_addr, lo_addr = self._read_rr(rr)
        byte = self._read_n_ram(ho_addr, lo_addr)

        if byte & 0x80 :
            self._set_carry_flag()
        else :
            self._reset_carry_flag()
        
        self._write_n_ram(shift_left_byte(byte, 1), ho_addr, lo_addr)

        # Flag tests.
        self._test_and_set_sign_flag(self._read_n_ram(ho_addr, lo_addr))
        self._test_and_set_zero_flag(self._read_n_ram(ho_addr, lo_addr))
        self._test_and_set_parity_flag(self._read_n_ram(ho_addr, lo_addr))

        # Flag sets & resets.
        self._reset_half_carry_flag()
        self._reset_add_substract_flag()

    def _sla_indx_d_r(self, rr, r) :
        """
        SLA (rr + d), r. Arithmetic shift left r &
        store result at address (rr + d).
        """
        # Affects : S, Z, P, C.
        # Resets : H, N.
        self._log_instruction_trace("SLA (%s + 0x%0.2X), %s" % (rr, \
            self._read_n(), r))
        ho_base_addr, lo_base_addr = self._read_rr(rr)
        ho_addr, lo_addr = compute_indexed_address(ho_base_addr, \
            lo_base_addr, self._read_n())

        if self._read_r(r) & 0x80 :
            self._set_carry_flag()
        else :
            self._reset_carry_flag()

        self._write_r(r, shift_left_byte(self._read_r(r), 1))
        self._write_n_ram(self._read_r(r), ho_addr, lo_addr)

        # Flag tests.
        self._test_and_set_sign_flag(self._read_r(r))
        self._test_and_set_zero_flag(self._read_r(r))
        self._test_and_set_parity_flag(self._read_r(r))

        # Flag sets & resets.
        self._reset_half_carry_flag()
        self._reset_add_substract_flag()

    def _sla_indx_d(self, rr) :
        """
        SLA (rr + d). Arithmetic shift left r &
        store result at address (rr + d).
        """
        # Affects : S, Z, P, C.
        # Resets : H, N.
        self._log_instruction_trace("SLA (%s + 0x%0.2X)" % (rr, self._read_n()))
        ho_base_addr, lo_base_addr = self._read_rr(rr)
        ho_addr, lo_addr = compute_indexed_address(ho_base_addr, \
            lo_base_addr, self._read_n())
        byte = self._read_n_ram(ho_addr, lo_addr)
        self._write_n_ram(shift_left_byte(byte, 1), ho_addr, lo_addr)

        if byte & 0x80 :
            self._set_carry_flag()
        else :
            self._reset_carry_flag()

        # Flag tests.
        self._test_and_set_sign_flag(self._read_n_ram(ho_addr, lo_addr))
        self._test_and_set_zero_flag(self._read_n_ram(ho_addr, lo_addr))
        self._test_and_set_parity_flag(self._read_n_ram(ho_addr, lo_addr))

        # Flag sets & resets.
        self._reset_half_carry_flag()
        self._reset_add_substract_flag()

    def _sla_r(self, r) :
        """
        SLA r. Arithmetic shift left r.
        """
        # Affects : S, Z, P, C.
        # Resets : H, N.
        self._log_instruction_trace("SLA %s" % r)

        if self._read_r(r) & 0x80 :
            self._set_carry_flag()
        else :
            self._reset_carry_flag()

        self._write_r(r, shift_left_byte(self._read_r(r), 1))
        
        # Flag tests.
        self._test_and_set_sign_flag(self._read_r(r))
        self._test_and_set_zero_flag(self._read_r(r))
        self._test_and_set_parity_flag(self._read_r(r))

        # Flag sets & resets.
        self._reset_half_carry_flag()
        self._reset_add_substract_flag()

    def _sll_addr_rr(self, rr) :
        """
        SLL (rr). Shift logical left r.
        """
        # Affects : S, Z, P, C.
        # Resets : H, N.
        self._log_instruction_trace("SLL (%s)" % rr)
        ho_addr, lo_addr = self._read_rr(rr)
        byte = self._read_n_ram(ho_addr, lo_addr)

        if byte & 0x80 :
            self._set_carry_flag()
        else :
            self._reset_carry_flag()
        
        self._write_n_ram(shift_left_byte(byte, 1) | 0x1, ho_addr, lo_addr)

        # Flag tests.
        self._test_and_set_sign_flag(self._read_n_ram(ho_addr, lo_addr))
        self._test_and_set_zero_flag(self._read_n_ram(ho_addr, lo_addr))
        self._test_and_set_parity_flag(self._read_n_ram(ho_addr, lo_addr))

        # Flag sets & resets.
        self._reset_half_carry_flag()
        self._reset_add_substract_flag()

    def _sll_indx_d_r(self, rr, r) :
        """
        SLL (rr + d), r. Shift logical left r &
        store result at address (rr + d).
        """
        # Affects : S, Z, P, C.
        # Resets : H, N.
        self._log_instruction_trace("SLL (%s + 0x%0.2X), %s" % (rr, \
            self._read_n(), r))
        ho_base_addr, lo_base_addr = self._read_rr(rr)
        ho_addr, lo_addr = compute_indexed_address(ho_base_addr, \
            lo_base_addr, self._read_n())

        if self._read_r(r) & 0x80 :
            self._set_carry_flag()
        else :
            self._reset_carry_flag()

        self._write_r(r, shift_left_byte(self._read_r(r), 1) | 0x1)
        self._write_n_ram(self._read_r(r), ho_addr, lo_addr)

        # Flag tests.
        self._test_and_set_sign_flag(self._read_r(r))
        self._test_and_set_zero_flag(self._read_r(r))
        self._test_and_set_parity_flag(self._read_r(r))

        # Flag sets & resets.
        self._reset_half_carry_flag()
        self._reset_add_substract_flag()

    def _sll_indx_d(self, rr) :
        """
        SLL (rr + d). Shift logical left r &
        store result at address (rr + d).
        """
        # Affects : S, Z, P, C.
        # Resets : H, N.
        self._log_instruction_trace("SLL (%s + 0x%0.2X)" % (rr, self._read_n()))
        ho_base_addr, lo_base_addr = self._read_rr(rr)
        ho_addr, lo_addr = compute_indexed_address(ho_base_addr, \
            lo_base_addr, self._read_n())
        byte = self._read_n_ram(ho_addr, lo_addr)
        self._write_n_ram(shift_left_byte(byte, 1) | 0x1, ho_addr, lo_addr)

        if byte & 0x80 :
            self._set_carry_flag()
        else :
            self._reset_carry_flag()

        # Flag tests.
        self._test_and_set_sign_flag(self._read_n_ram(ho_addr, lo_addr))
        self._test_and_set_zero_flag(self._read_n_ram(ho_addr, lo_addr))
        self._test_and_set_parity_flag(self._read_n_ram(ho_addr, lo_addr))

        # Flag sets & resets.
        self._reset_half_carry_flag()
        self._reset_add_substract_flag()
    
    def _sll_r(self, r) :
        """
        SLL r. Shift logical left r.
        """
        # Affects : S, Z, P, C.
        # Resets : H, N.
        self._log_instruction_trace("SLL %s" % r)

        if self._read_r(r) & 0x80 :
            self._set_carry_flag()
        else :
            self._reset_carry_flag()

        self._write_r(r, shift_left_byte(self._read_r(r), 1) | 0x1)
        
        # Flag tests.
        self._test_and_set_sign_flag(self._read_r(r))
        self._test_and_set_zero_flag(self._read_r(r))
        self._test_and_set_parity_flag(self._read_r(r))

        # Flag sets & resets.
        self._reset_half_carry_flag()
        self._reset_add_substract_flag()

    def _sra_addr_rr(self, rr) :
        """
        SRA rr. Shift right arithmetic r.
        """
        # Affects : S, Z, P, C.
        # Resets : H, N.
        self._log_instruction_trace("SRA (%s)" % rr)
        byte = self._read_n_ram(*self._read_rr(rr))

        if self._read_n_ram(*self._read_rr(rr)) & 0x1 :
            self._set_carry_flag()
        else :
            self._reset_carry_flag()

        byte = shift_right_byte(byte, 1)

        if self._read_n_ram(*self._read_rr(rr)) & 0x80 :
            byte |= 0x80

        self._write_n_ram(byte, *self._read_rr(rr))

        # Flag tests.
        self._test_and_set_sign_flag(self._read_n_ram(*self._read_rr(rr)))
        self._test_and_set_zero_flag(self._read_n_ram(*self._read_rr(rr)))
        self._test_and_set_parity_flag(self._read_n_ram(*self._read_rr(rr)))

        # Flag sets & resets.
        self._reset_half_carry_flag()
        self._reset_add_substract_flag()

    def _sra_indx_d(self, rr) :
        """
        SRA (rr + d). Shift right arithmetic r &
        store result at address (rr + d).
        """
        # Affects : S, Z, P, C.
        # Resets : H, N.
        self._log_instruction_trace("SRA (%s + 0x%0.2X)" % \
            (rr, self._read_n()))
        ho_base_addr, lo_base_addr = self._read_rr(rr)
        ho_addr, lo_addr = compute_indexed_address(ho_base_addr, \
            lo_base_addr, self._read_n())
        byte = self._read_n_ram(ho_addr, lo_addr)

        if byte & 0x1 :
            self._set_carry_flag()
        else :
            self._reset_carry_flag()

        if byte & 0x80 :
            self._write_n_ram(shift_right_byte(byte, 1) | 0x80, ho_addr, lo_addr)
        else :
            self._write_n_ram(shift_right_byte(byte, 1), ho_addr, lo_addr)

        # Flag tests.
        self._test_and_set_sign_flag(self._read_n_ram(ho_addr, lo_addr))
        self._test_and_set_zero_flag(self._read_n_ram(ho_addr, lo_addr))
        self._test_and_set_parity_flag(self._read_n_ram(ho_addr, lo_addr))

        # Flag sets & resets.
        self._reset_half_carry_flag()
        self._reset_add_substract_flag()

    def _sra_indx_d_r(self, rr, r) :
        """
        SRA (rr + d), r. Shift right arithmetic r &
        store result at address (rr + d).
        """
        # Affects : S, Z, P, C.
        # Resets : H, N.
        self._log_instruction_trace("SRA (%s + 0x%0.2X), %s" % (rr, \
            self._read_n(), r))
        ho_base_addr, lo_base_addr = self._read_rr(rr)
        ho_addr, lo_addr = compute_indexed_address(ho_base_addr, \
            lo_base_addr, self._read_n())

        if self._read_r(r) & 0x1 :
            self._set_carry_flag()
        else :
            self._reset_carry_flag()

        if self._read_r(r) & 0x80 :
            self._write_r(r, shift_right_byte(self._read_r(r), 1) | 0x80)
        else :
            self._write_r(r, shift_right_byte(self._read_r(r), 1))

        self._write_n_ram(self._read_r(r), ho_addr, lo_addr)

        # Flag tests.
        self._test_and_set_sign_flag(self._read_r(r))
        self._test_and_set_zero_flag(self._read_r(r))
        self._test_and_set_parity_flag(self._read_r(r))

        # Flag sets & resets.
        self._reset_half_carry_flag()
        self._reset_add_substract_flag()

    def _sra_r(self, r) :
        """
        SRA r. Shift right arithmetic r.
        """
        # Affects : S, Z, P, C.
        # Resets : H, N.
        self._log_instruction_trace("SRA %s" % r)

        if self._read_r(r) & 0x1 :
            self._set_carry_flag()
        else :
            self._reset_carry_flag()

        if self._read_r(r) & 0x80 :
            self._write_r(r, shift_right_byte(self._read_r(r), 1) | 0x80)
        else :
            self._write_r(r, shift_right_byte(self._read_r(r), 1))

        # Flag tests.
        self._test_and_set_sign_flag(self._read_r(r))
        self._test_and_set_zero_flag(self._read_r(r))
        self._test_and_set_parity_flag(self._read_r(r))

        # Flag sets & resets.
        self._reset_half_carry_flag()
        self._reset_add_substract_flag()

    def _srl_addr_rr(self, rr) :
        """
        SRL (rr). Shift right arithmetic r.
        """
        # Affects : S, Z, P, C.
        # Resets : H, N.
        self._log_instruction_trace("SRA (%s)" % rr)
        byte = self._read_n_ram(*self._read_rr(rr))

        if byte & 0x1 :
            self._set_carry_flag()
        else :
            self._reset_carry_flag()

        byte = shift_right_byte(byte, 1)

        if byte & 0x80 :
            byte |= 0x80

        self._write_n_ram(byte, *self._read_rr(rr))

        # Flag tests.
        self._test_and_set_sign_flag(byte)
        self._test_and_set_zero_flag(byte)
        self._test_and_set_parity_flag(byte)

        # Flag sets & resets.
        self._reset_half_carry_flag()
        self._reset_add_substract_flag()
    
    def _srl_indx_d(self, rr) :
        """
        SRL (rr + d), r. Shift right arithmetic r &
        store result at address (rr + d).
        """
        # Affects : S, Z, P, C.
        # Resets : H, N.
        self._log_instruction_trace("SRL (%s + 0x%0.2X)" % \
            (rr, self._read_n()))
        ho_base_addr, lo_base_addr = self._read_rr(rr)
        ho_addr, lo_addr = compute_indexed_address(ho_base_addr, \
            lo_base_addr, self._read_n())
        byte = self._read_n_ram(ho_addr, lo_addr)

        if byte & 0x1 :
            self._set_carry_flag()
        else :
            self._reset_carry_flag()
      
        self._write_n_ram(shift_right_byte(byte, 1), ho_addr, lo_addr)

        # Flag tests.
        self._test_and_set_sign_flag(self._read_n_ram(ho_addr, lo_addr))
        self._test_and_set_zero_flag(self._read_n_ram(ho_addr, lo_addr))
        self._test_and_set_parity_flag(self._read_n_ram(ho_addr, lo_addr))

        # Flag sets & resets.
        self._reset_half_carry_flag()
        self._reset_add_substract_flag()

    def _srl_indx_d_r(self, rr, r) :
        """
        SRL (rr + d), r. Shift right arithmetic r &
        store result at address (rr + d).
        """
        # Affects : S, Z, P, C.
        # Resets : H, N.
        self._log_instruction_trace("SRL (%s + 0x%0.2X), %s" % \
            (rr, self._read_n(), r))
        ho_base_addr, lo_base_addr = self._read_rr(rr)
        ho_addr, lo_addr = compute_indexed_address(ho_base_addr, \
            lo_base_addr, self._read_n())

        if self._read_r(r) & 0x1 :
            self._set_carry_flag()
        else :
            self._reset_carry_flag()
      
        self._write_r(r, shift_right_byte(self._read_r(r), 1))
        self._write_n_ram(self._read_r(r), ho_addr, lo_addr)

        # Flag tests.
        self._test_and_set_sign_flag(self._read_r(r))
        self._test_and_set_zero_flag(self._read_r(r))
        self._test_and_set_parity_flag(self._read_r(r))

        # Flag sets & resets.
        self._reset_half_carry_flag()
        self._reset_add_substract_flag()

    def _srl_r(self, r) :
        """
        SRL r. Logical shift r.
        """
        # Affects : S, Z, P, C.
        # Resets : H, N.
        self._log_instruction_trace("SRL %s" % r)

        if self._read_r(r) & 0x1 :
            self._set_carry_flag()
        else :
            self._reset_carry_flag()

        self._write_r(r, shift_right_byte(self._read_r(r), 1))

        # Flag tests.
        self._test_and_set_sign_flag(self._read_r(r))
        self._test_and_set_zero_flag(self._read_r(r))
        self._test_and_set_parity_flag(self._read_r(r))

        # Flag sets & resets.
        self._reset_half_carry_flag()
        self._reset_add_substract_flag()

    def _sub_flag_tests(self, n, m) :
        sub = n - m
        self._test_and_set_sign_flag(sub)
        self._test_and_set_zero_flag(sub)
        self._test_and_set_half_carry_on_substract(n, m)
        self._test_and_set_overflow_flag(n, m, "SUB")
        self._test_and_set_carry_flag(sub)
        self._set_add_substract_flag()

    def _sub_addr_indx_d(self, rr) :
        self._log_instruction_trace("SUB (%s + %d)" % (rr, self._read_n()))
        ho_base_addr, lo_base_addr = self._read_rr(rr)
        ho_addr, lo_addr = compute_indexed_address(ho_base_addr, \
            lo_base_addr, self._read_n())
        self._sub_flag_tests(self._read_r("a"), self._read_n_ram(ho_addr, lo_addr))
        self._write_r("a", sub_bytes(self._read_r("a"), \
            self._read_n_ram(ho_addr, lo_addr)))

    def _sub_addr_rr(self, rr) :
        self._log_instruction_trace("SUB (%s)" % rr)
        self._sub_flag_tests(self._read_r("a"), self._read_n_ram(*self._read_rr(rr)))
        self._write_r("a", sub_bytes(self._read_r("a"), \
            self._read_n_ram(*self._read_rr(rr))))

    def _sub_n(self) :
        self._log_instruction_trace("SUB 0x%0.2X" % self._read_n())
        self._sub_flag_tests(self._read_r("a"), self._read_n())
        self._write_r("a", sub_bytes(self._read_r("a"), self._read_n()))

    def _sub_r(self, r) :
        self._log_instruction_trace("SUB %s" % r)
        self._sub_flag_tests(self._read_r("a"), self._read_r(r))
        self._write_r("a", sub_bytes(self._read_r("a"), self._read_r(r)))

    def _xor_flag_tests(self, n) :
        self._test_and_set_sign_flag(n)
        self._test_and_set_zero_flag(n)
        self._test_and_set_parity_flag(n)
        self._reset_half_carry_flag()
        self._reset_add_substract_flag()
        self._reset_carry_flag()

    def _xor_addr_indx_d(self, rr) :
        self._log_instruction_trace("XOR (%s + 0x%0.2X)" % \
            (rr, self._read_n()))
        ho_base_addr, lo_base_addr = self._read_rr(rr)
        ho_addr, lo_addr = compute_indexed_address(ho_base_addr, \
            lo_base_addr, self._read_n())
        byte = self._read_r("a") ^ self._read_n_ram(ho_addr, lo_addr)
        self._write_r("a", byte)
        self._xor_flag_tests(byte)

    def _xor_addr_rr(self, rr) :
        self._log_instruction_trace("XOR (%s)" % rr)
        byte = self._read_r("a") ^ self._read_n_ram(*self._read_rr(rr))
        self._write_r("a", byte)
        self._xor_flag_tests(byte)
        
    def _xor_n(self) :
        self._log_instruction_trace("XOR %s" % self._read_n())
        byte = self._read_r("a") ^ self._read_n()
        self._write_r("a", byte)
        self._xor_flag_tests(byte)

    def _xor_r(self, r) :
        self._log_instruction_trace("XOR %s" % r)
        byte = self._read_r("a") ^ self._read_r(r)        
        self._write_r("a", byte)
        self._xor_flag_tests(byte)

    def _test_and_set_sign_flag(self, n) :
        """
        Tests n and sets S according to result.
        """
        if test_byte_sign(n) :
            self._set_sign_flag()
            return
        
        self._reset_sign_flag()
    
    def _test_and_set_zero_flag(self, n) :
        """
        Tests n and sets Z according to result.
        """
        if test_byte_zero(n) :
            self._set_zero_flag()
            return

        self._reset_zero_flag()

    def _test_and_set_half_carry_on_add(self, n, m) :
        """
        Tests if there is a half carry when adding n
        and m. Sets H according to result.
        """
        if test_half_carry_on_add(n, m) :
            self._set_half_carry_flag()
            return

        self._reset_half_carry_flag()
    
    def _test_and_set_half_carry_on_substract(self, n, m) :
        """
        Tests if there is a borrow when substracting n from
        m. Sets H according to result.
        """
        if test_half_carry_on_substract(n, m) :
            self._set_half_carry_flag()
            return

        self._reset_half_carry_flag()

    def _test_and_set_parity_flag(self, n) :
        """
        Tests n and sets P according to result.
        """
        # If parity is even set the parity/overflow flag, 
        # otherwise reset it.
        if byte_parity(n) :
            self._set_parity_overflow_flag()
            return

        self._reset_parity_overflow_flag()

    #def _test_and_set_overflow_flag(self, n, m) :
    def _test_and_set_overflow_flag(self, n, m, op="ADD") :
        """
        Tests byte and sets V according to result.
        """
        if test_signed_byte_overflow(n, m, op) :
            self._set_parity_overflow_flag()
            return

        self._reset_parity_overflow_flag()

    def _test_and_set_carry_flag(self, n) :
        """
        Tests n and sets C according to result.
        """
        if test_byte_overflow(n) :
            self._set_carry_flag()
            return

        self._reset_carry_flag()

    def _test_and_set_sign_flag_word(self, n) :
        if test_word_sign(n) :
            self._set_sign_flag()
            return

        self._reset_sign_flag()

    def _test_and_set_zero_flag_word(self, n) :
        if test_word_zero(n) :
            self._set_zero_flag()
            return
        
        self._reset_zero_flag()

    def _test_and_set_half_carry_on_add_word(self, n, m) :
        if test_half_carry_on_add_word(n, m) :
            self._set_half_carry_flag()
            return
        
        self._reset_half_carry_flag()
    
    def _test_and_set_half_carry_on_substract_word(self, n, m) :
        if test_half_carry_on_substract_word(n, m) :
            self._set_half_carry_flag()
            return
        
        self._reset_half_carry_flag()

    def _test_and_set_parity_flag_word(self, n) :
        # If parity is even set the parity/overflow flag, 
        # otherwise reset it.
        if word_parity(n) :
            self._set_parity_overflow_flag()
            return
        
        self._reset_parity_overflow_flag()

    def _test_and_set_overflow_flag_word(self, n, m, op="ADD") :
        if test_signed_word_overflow(n, m, op) :
            self._set_parity_overflow_flag()
            return

        self._reset_parity_overflow_flag()

    def _test_and_set_carry_flag_word(self, n) :
        """
        Tests n and sets C according to result.
        """
        if test_word_overflow(n) :
            self._set_carry_flag()
            return

        self._reset_carry_flag()
