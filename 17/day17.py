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
import numpy as np
#from point import Point

class Grid:
    def __init__(self, data):
        self.data = data
        self._init_grid(data)
    
    def _init_grid(self, data):
        self.height = len(data)
        self.width  = max(len(d) for d in data)
        for d in data:
            if len(d) > self.width:
                self.width = len(d)
        self.grid = np.array([list(d.ljust(self.width)) for d in data])
    
    def print_data(self):
        for j in range(self.height):
            for i in range(self.width):
                print(self.grid[j,i], end="")
            print()
    
    def find_intersections(self):
        tot = 0
        # don't bother checking points on the edge
        for j in range(1, self.height-1):
            for i in range(1, self.width-1):
                found = True
                for i2, j2 in [(i,j), (i-1,j), (i+1,j), (i,j-1), (i,j+1)]:
                    if self.grid[j2,i2] != '#':
                        found = False
                        break
                if found:
                    print("# %d,%d" % (i,j))
                    tot += i * j
        return tot
    
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
                    if line != "":
                        data.append(line)
                    line = ""
                else:
                    line += c
        #data.append(line)
        return cls(data)
    
    @classmethod
    def from_file(cls, filename):
        data = []
        with open(filename, "r") as fh:
            for l in fh:
                data.append(l.rstrip())
        return cls(data)

if __name__ == '__main__':
    test = Grid.from_file("test1.txt")
    test.print_data()
    print(test.find_intersections())
    
    inp = Grid.from_intcode(Intcode.from_file("input.txt"))
    inp.print_data()
    print(inp.find_intersections())
    