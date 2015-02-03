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

from simplefsm import State, Transition, SimpleFSM
from simplefsm.exceptions import FSMEndOfInput


class Z80FSM(SimpleFSM):
    def __init__(self, z80):
        super(Z80FSM, self).__init__()
        self._z80 = z80

    def read_symbol(self):
        if self.current_state.final_state == True:
            raise FSMEndOfInput

        return self._z80.ram.read(self._z80.pc.bits)

    def post_transit(self):
        self._z80.inc_pc()


class Z80FSMBuilder(object):
    def __init__(self, z80):
        self._z80 = z80
        self._ignore_byte = lambda _: True

    def build(self):
        fsms = [
            self._build_non_prefix_fsm(),
            self._build_cb_fsm(),
            self._build_ed_fsm(),
            self._build_dd_fsm(),
            self._build_fd_fsm(),
            self._build_ddcb_fsm(),
            self._build_fdcb_fsm(),
        ]

        return fsms

    def _build_fsm(self, states, transitions):
        fsm = Z80FSM(self._z80)
        fsm.add_states(states)
        fsm.add_transitions(transitions)

        return fsm

    def _non_prefix_fsm_bytes(self):
        non_prefix_three_bytes = set(
            [0x01, 0x11, 0x21, 0x22, 0x2A, 0x31, 0x32, 0x3A, 0xC2,
            0xC3, 0xC4, 0xCA, 0xCC, 0xCD, 0xD2, 0xD4, 0xDA, 0xDC, 0xE2,
            0xE4, 0xE6, 0xEA, 0xEC, 0xF2, 0xF4, 0xFA, 0xFC]
        )

        non_prefix_two_bytes = set(
            [0x06, 0x0E, 0x10, 0x16, 0x18, 0x1E, 0x20, 0x26, 0x28,
            0x2E, 0x30, 0x36, 0x38, 0x3E, 0xC6, 0xCE, 0xD3, 0xD6, 0xDB,
            0xDE, 0xE6, 0xEE, 0xF6, 0xFE]
        )

        non_prefix_one_byte = set(range(0x00, 0xFF + 1)) - \
            non_prefix_three_bytes - non_prefix_two_bytes

        return non_prefix_one_byte, non_prefix_two_bytes, non_prefix_three_bytes

    def _build_non_prefix_fsm(self):
        non_prefix_one_byte, non_prefix_two_bytes, \
            non_prefix_three_bytes = self._non_prefix_fsm_bytes()

        i_state = State('I', start_state=True)
        f_state = State('F', final_state=True)
        b_state = State('B')
        c_state = State('C')
        d_state = State('D')

        states = [i_state, f_state, b_state, c_state, d_state]
        transitions = [
            Transition(i_state, f_state, lambda b: b in non_prefix_one_byte),
            Transition(i_state, b_state, lambda b: b in non_prefix_two_bytes),
            Transition(b_state, f_state, self._ignore_byte),
            Transition(i_state, c_state, lambda b: b in non_prefix_three_bytes),
            Transition(c_state, d_state, self._ignore_byte),
            Transition(d_state, f_state, self._ignore_byte),
        ]

        return self._build_fsm(states, transitions)

    def _cb_fsm_bytes(self):
        return set(range(0x00, 0xFF + 1))

    def _build_cb_fsm(self):
        cb = self._cb_fsm_bytes()

        i_state = State('I', start_state=True)
        f_state = State('F', final_state=True)
        b_state = State('B')

        states = [i_state, f_state, b_state]
        transitions = [
            Transition(i_state, b_state, lambda b: b == 0xCB),
            Transition(b_state, f_state, lambda b: b in cb)
        ]

        return self._build_fsm(states, transitions)

    def _ed_fsm_bytes(self):
        ed_four_bytes = set(range(0x43, 0x7B + 8, 8))
        ed_two_bytes = set(range(0x00, 0xBB)) - ed_four_bytes

        return ed_two_bytes, ed_four_bytes

    def _build_ed_fsm(self):
        ed_two_bytes, ed_four_bytes = self._ed_fsm_bytes()

        i_state = State('I', start_state=True)
        f_state = State('F', final_state=True)
        b_state = State('B')
        c_state = State('C')
        d_state = State('D')

        states = [i_state, f_state, b_state, c_state, d_state]
        transitions = [
            Transition(i_state, b_state, lambda b: b == 0xED),
            Transition(b_state, f_state, lambda b: b in ed_two_bytes),
            Transition(b_state, c_state, lambda b: b in ed_four_bytes),
            Transition(c_state, d_state, self._ignore_byte),
            Transition(d_state, f_state, self._ignore_byte)
        ]

        return self._build_fsm(states, transitions)

    def _dd_fsm_bytes(self):
        dd_four_bytes = set([0x21, 0x22, 0x2A, 0x36])
        
        dd_three_bytes = set([0x26, 0x2E, 0x34, 0x35, 0x46, 0x4E, 0x56, 0x5E, 0x66, 0x6E])
        dd_three_bytes = dd_three_bytes.union(range(0x70, 0x75 + 1)).union([0x77])
        dd_three_bytes.union(range(0x7E, 0xBE + 8, 8)) 

        dd_two_bytes = set(range(0x09, 0xBE + 1)) 
        dd_two_bytes = dd_two_bytes.union([0xE1, 0xE3, 0xE5, 0xE9, 0xF9])
        dd_two_bytes -= dd_three_bytes - dd_four_bytes

        return dd_two_bytes, dd_three_bytes, dd_four_bytes

    def _build_dd_fsm(self):
        dd_two_bytes, dd_three_bytes, dd_four_bytes = self._dd_fsm_bytes()

        i_state = State('I', start_state=True)
        f_state = State('F', final_state=True)
        b_state = State('B')
        c_state = State('C')
        d_state = State('D')
        e_state = State('E')

        states = [i_state, f_state, b_state, c_state, d_state, e_state]
        transitions = [
            Transition(i_state, b_state, lambda b: b == 0xDD),
            Transition(b_state, f_state, lambda b: b in dd_two_bytes),
            Transition(b_state, c_state, lambda b: b in dd_three_bytes),
            Transition(c_state, f_state, self._ignore_byte),
            Transition(b_state, d_state, lambda b: b in dd_four_bytes),
            Transition(d_state, e_state, self._ignore_byte),
            Transition(e_state, f_state, self._ignore_byte)
        ]

        return self._build_fsm(states, transitions)

    def _fd_fsm_bytes(self):
        fd_four_bytes = set([0x21, 0x22, 0x2A, 0x36])

        fd_three_bytes = set([0x26, 0x2E, 0x34, 0x35, 0x46, 0x4E, 0x56, 0x5E, 0x66, 0x6E])
        fd_three_bytes = fd_three_bytes.union(range(0x70, 0x75 + 1)).union([0x77])
        fd_three_bytes.union(range(0x7E, 0xBE + 8, 8)) 

        fd_two_bytes = set(range(0x09, 0xBE + 1)) 
        fd_two_bytes = fd_two_bytes.union([0xE1, 0xE3, 0xE5, 0xE9, 0xF9])
        fd_two_bytes -= fd_three_bytes - fd_four_bytes

        return fd_two_bytes, fd_three_bytes, fd_four_bytes

    def _build_fd_fsm(self):
        fd_two_bytes, fd_three_bytes, fd_four_bytes = self._fd_fsm_bytes()

        i_state = State('I', start_state=True)
        f_state = State('F', final_state=True)
        b_state = State('B')
        c_state = State('C')
        d_state = State('D')
        e_state = State('E')

        states = [i_state, f_state, b_state, c_state, d_state, e_state]
        transitions = [
            Transition(i_state, b_state, lambda b: b == 0xFD),
            Transition(b_state, f_state, lambda b: b in fd_two_bytes),
            Transition(b_state, c_state, lambda b: b in fd_three_bytes),
            Transition(c_state, f_state, self._ignore_byte),
            Transition(b_state, d_state, lambda b: b in fd_four_bytes),
            Transition(d_state, e_state, self._ignore_byte),
            Transition(e_state, f_state, self._ignore_byte)
        ]

        return self._build_fsm(states, transitions)

    def _ddcb_fsm_bytes(self):
        return set(range(0x00, 0xFF + 1))

    def _build_ddcb_fsm(self):
        ddcb = self._ddcb_fsm_bytes()

        i_state = State('I', start_state=True)
        f_state = State('F', final_state=True)
        b_state = State('B')
        c_state = State('C')
        d_state = State('D')
        e_state = State('E')

        states = [i_state, f_state, b_state, c_state, d_state, e_state]
        transitions = [
            Transition(i_state, b_state, lambda b: b == 0xDD),
            Transition(b_state, c_state, lambda b: b == 0xCB),
            Transition(c_state, d_state, self._ignore_byte),
            Transition(d_state, f_state, lambda b: b in ddcb)
        ]

        return self._build_fsm(states, transitions)

    def _fdcb_fsm_bytes(self):
        return set(range(0x00, 0xFF + 1))

    def _build_fdcb_fsm(self):
        fdcb = self._fdcb_fsm_bytes()

        i_state = State('I', start_state=True)
        f_state = State('F', final_state=True)
        b_state = State('B')
        c_state = State('C')
        d_state = State('D')
        e_state = State('E')

        states = [i_state, f_state, b_state, c_state, d_state, e_state]
        transitions = [
            Transition(i_state, b_state, lambda b: b == 0xFD),
            Transition(b_state, c_state, lambda b: b == 0xCB),
            Transition(c_state, d_state, self._ignore_byte),
            Transition(d_state, f_state, lambda b: b in fdcb)
        ]

        return self._build_fsm(states, transitions)
