Introduction
============

PyZ80 is a Z80 cpu emulator written entirely in Python.
Currently the code is being heavily refactored to use
proper object oriented abstractions.

This project relies on the SimpleFSM module which is not
available on PyPI and can be found `here <https://github.com/lliendo/SimpleFSM>`_

Currently only a few tests are green and the code
itself is not able to execute any full program.
Work is now focused on instruction refactoring.
