# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 23:41:21 2019

@author: matt
"""

from collections import defaultdict
import sys

if '..' not in sys.path:
    sys.path.append('..')

from intcode import Intcode
from point import Point

class Day11:
    MOVE = {
        0: Point(0, 1),
        1: Point(1, 0),
        2: Point(0, -1),
        3: Point(-1, 0)
    }

    def __init__(self, filename, debug=0):
        self.intcode = Intcode.from_file(filename, debug=debug)
        self.process = self.intcode.create_process()
        self.data = defaultdict(int)
        self.current = Point(0, 0)
        self.dir = 0
    
    def run(self):
        self.data[Point(0, 0)] = 1
        while not self.process.is_terminated():
            self.process.set_input(self.data[self.current])
            col = self.process.run_to_next_output()
            lr  = self.process.run_to_next_output()
            self.data[self.current] = col
            if lr == 0:
                self.dir = (self.dir-1) % 4
            elif lr == 1:
                self.dir = (self.dir+1) % 4
            else:
                print("bad output")
            self.current = self.current.add(self.MOVE[self.dir])

    def print_data(self):
        xmin, xmax, ymin, ymax = 0, 0, 0, 0
        for p in self.data.keys():
            if p.x < xmin:
                xmin = p.x
            if p.x > xmax:
                xmax = p.x
            if p.y < ymin:
                ymin = p.y
            if p.y > ymax:
                ymax = p.y
        for y in range(ymax, ymin-1, -1):
            for x in range(xmin, xmax+1):
                p = Point(x, y)
                if self.data[p] == 1:
                    print('#', end='')
                else:
                    print('.', end='')
            print()

if __name__ == '__main__':
    inp = Day11('input.txt')
    inp.run()
    print(len(inp.data.keys()))
    inp.print_data()
    
    #print(inp.data)
    