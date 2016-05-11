#!/usr/bin/env python3

# Junitex.py
#
# Copyright (C) 2016 Nathan Smith <nathan.smith5@mail.mcgill.ca>
#
# This program is free software: you can redistribute it and/or modify
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
#

import gi
import os

gi.require_version('GtkSource', '3.0')
gi.require_version('Ide', '1.0')

from gi.repository import GObject
from gi.repository import GtkSource
from gi.repository import Ide

class CompletionProvider(Ide.Object, GtkSource.CompletionProvider,
                         Ide.CompletionProvider):
    _dictionary = None
    _dictionary_filled = False

    def do_populate(self, context):
        iter1 = context.props.iter          
        textbuffer = iter1.get_buffer()         
        iter2 = iter1.copy()                    
        iter1.backward_word_starts(1)            
        iter1.backward_char()                  
        text1 = textbuffer.get_text(iter1, iter2, True)  
        iter1.backward_char()
        text2 = textbuffer.get_text(iter1, iter2, True)

        if not (text1.startswith('\\') or text2.startswith('\\')):         
            context.add_proposals(self, [], True)
            return

        if self._dictionary_filled == False:
            self.init_dict()

        if text1 in self._dictionary.keys():
            item = GtkSource.CompletionItem(label=self._dictionary[text1], 
                                            text=self._dictionary[text1])
            context.add_proposals(self, [item], True)
        
        if text2 in self._dictionary.keys():
            item = GtkSource.CompletionItem(label=self._dictionary[text2], 
                                            text=self._dictionary[text2])
            context.add_proposals(self, [item], True)

    def do_get_start_iter(self, context, proposal):
        iter = context.props.iter
        iter.backward_word_starts(1)
        iter.backward_char()
        g = iter.get_char()
        if g == "\\":
            return True, iter
        else:
            iter.backward_char()
            return True, iter

    def init_dict(self):
        self._dictionary = {}
        symboldir = os.path.dirname(os.path.abspath(__file__))
        symbolfilename = os.path.join(symboldir, "symbols.txt")
        symbolfile = open(symbolfilename, 'r')
        for line in symbolfile:
            words = line.split(" ")
            self._dictionary[words[0]] = words[1].strip('\n')
        self._dictionary_filled=True

        return
