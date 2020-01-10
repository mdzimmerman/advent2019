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
    
    NORTH, EAST, SOUTH, WEST = 0, 1, 2, 3
    
    def right(self, d):
        return (d+1) % 4
    
    def left(self, d):
        return (d-1) % 4
        
    def move(self, x, y, d):
        nx, ny = x, y
        if d == self.NORTH:
            ny -= 1
        elif d == self.EAST:
            nx += 1
        elif d == self.SOUTH:
            ny += 1
        elif d == self.WEST:
            nx -= 1
        return nx, ny, d
    
    def check_xy(self, x, y):
        if x < 0 or x >= self.width:
            return '.'
        if y < 0 or y >= self.height:
            return '.'
        return self.grid[y,x]
    
    def can_move(self, x, y, d):
        nx, ny, d = self.move(x, y, d)
        return self.check_xy(nx, ny) == '#'
    
    def walk_path(self):
        path = []
        orig = np.where(self.grid == '^')
        y, x = orig[0][0], orig[1][0]
        print(x, y)
        s = 0
        d = self.NORTH
        has_moves = True
        while has_moves:
            if self.can_move(x, y, d):
                s += 1
                x, y, d = self.move(x, y, d)
            elif self.can_move(x, y, self.right(d)):
                if s > 0:
                    path.append(str(s))
                s = 1  # start at 1 since we've already moved a step right
                path.append('R')
                x, y, d = self.move(x, y, self.right(d))
            elif self.can_move(x, y, self.left(d)):
                if s > 0:
                    path.append(str(s))
                s = 1  # start at 1 since we've already moved a step left
                path.append('L')
                x, y, d = self.move(x, y, self.left(d))
            else:
                if s > 0:
                    path.append(str(s))
                has_moves = False
        return path
    
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
    print(",".join(test.walk_path()))
    
    
    ascii_intcode = Intcode.from_file("input.txt")
    inp = Grid.from_intcode(ascii_intcode)
    inp.print_data()
    print(inp.find_intersections())
    inp_path = ",".join(inp.walk_path())
    print(inp_path)
    
    # figured this out by hand
    sub = {"A": "L,12,L,8,L,8",
           "B": "R,4,L,12,L,12,R,6",
           "C": "L,12,R,4,L,12,R,6"}
    s = inp_path
    for rep, patt in sub.items():
        s = s.replace(patt, rep)
    inp_text = [s, sub['A'], sub['B'], sub['C'], 'n'];
    print(inp_text)
    inp_raw = []
    for l in inp_text:
        for x in [ord(c) for c in l]:
            inp_raw.append(x)
        inp_raw.append(10)
    
    p = ascii_intcode.create_process(inp=inp_raw)
    p.set_value(0, 0, 2)
    for c in p.run():
        if c is None:
            pass
        elif c >= 256:
            print(c)
        else:
            print(chr(c), end="")
    
    print(p.state)
    #print(p)
    #print(inp_raw)
    