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


from setuptools import setup

setup(
    name="PyZ80",
    description="A Z80 cpu emulator fully implemented in Python",
    version="0.0.1",
    packages=["pyz80"],
    author="Lucas Liendo",
    author_email="mindmaster@gmail.com",
    keywords="emulator z80 pyz80",
    install_requires=[
        "nose>=1.3.2",
    ],
    zip_safe=False,
    test_suite="nose.collector",
)
