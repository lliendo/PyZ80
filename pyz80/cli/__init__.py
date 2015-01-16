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

from argparse import ArgumentParser


class CLIError(Exception) :
    pass


class CLI(object) :
    def __init__(self) :
        self._options = self._build_parser().parse_args()

    def __getattr__(self, option_name) :
        try :
            return getattr(self._options, option_name)
        except AttributeError :
            raise CLIError(
                'Error - Option : {0} does not exist.'.format(option_name)
            )

    def _build_parser(self) :
        parser = ArgumentParser(prog='PyZ80')
        parser.add_argument(
            '-a', '--address', dest='address', action='store', required=False
        )
        parser.add_argument(
            '-p', '--program', dest='program_path', action='store', required=True
        )
        parser.add_argument(
            '-d', '--devices_dir', dest='devices_module_path', action='store',
            default=None, required=False
        )

        return parser
