#!/usr/bin/env python2

# makedict.py
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


import urllib2

def make_dict(url):
    symbol_dict = {}
    response = urllib2.urlopen(url)
    for line in response:
        words = line.split()
        if len(words) >= 3 and words[1] == "=>":
            symbol_dict[words[0].strip("\"")[1:]] = words[2].strip(",").strip("\"")
    return symbol_dict

if __name__ == "__main__":
    url = "http://raw.githubusercontent.com\
/JuliaLang/julia/master/base/latex_symbols.jl"
    outfile = open("./symbols.txt", 'w')
    symbol_dict = make_dict(url)
    for key in symbol_dict:
        outfile.write(key+" "+symbol_dict[key]+"\n")
    outfile.close()
