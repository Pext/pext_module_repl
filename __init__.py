#!/usr/bin/env python3

# Copyright (c) 2016 - 2017 Sylvia van Os <sylvia@hackerchick.me>
#
# Pext REPL module is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys

from pext_base import ModuleBase
from pext_helpers import Action, SelectionType


class Module(ModuleBase):
    def init(self, settings, q):
        self.output = None

        self.q = q

        self.q.put([Action.add_command, "eval"])

    def stop(self):
        pass

    def selection_made(self, selection):
        if len(selection) == 0:
            self.q.put([Action.add_command, "eval"])
            if self.output:
                self.q.put([Action.add_entry, self.output])
                self.output = None
        elif len(selection) == 1:
            if selection[0]["type"] == SelectionType.command:
                # Remove command from input string
                input_string = selection[0]["value"].split(" ", 1)

                # Don't do anything if there is nothing to do
                if len(input_string) < 2:
                    self.q.put([Action.set_selection, []])
                    return

                input_string = input_string[1:]

                self.q.put([Action.replace_entry_list, []])
                try:
                    self.output = eval(input_string, {})
                except Exception as e:
                    self.q.put([Action.add_error, str(e)])
            
                self.q.put([Action.set_selection, []])
            else:
                self.q.put([Action.copy_to_clipboard, selection[0]["value"]])
                self.q.put([Action.close])

    def process_response(self, response):
        pass
