#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 17:20:41 2019

@author: mzimmerman
"""

import sys

if '..' not in sys.path:
    sys.path.append('..')

from intcode import Intcode
#from point import Point

class Grid:
    def __init__(self, data):
        self.data = data
        
    @classmethod
    def from_intcode(cls, intcode):
        process = intcode.create_process()
        data = []
        line = ""
        while not process.is_terminated():
            out = process.run_to_next_output()
            if out is not None:
                c = chr(out)
                if c == "\n":
                    data.append(line)
                    line = ""
                else:
                    line += c
        data.append(line)
        return cls(data)
    
    @classmethod
    def from_file(cls, filename):
        pass


if __name__ == '__main__':
    inp = Grid.from_intcode(Intcode.from_file("input.txt"))
    for d in inp.data:
        print("[%s]" % (d,))