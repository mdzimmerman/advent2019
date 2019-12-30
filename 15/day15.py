# -*- coding: utf-8 -*-
"""
Created on Sat Dec 28 19:35:07 2019

@author: matt
"""

import sys

if '..' not in sys.path:
    sys.path.append('..')

from intcode import Intcode
from point import Point


class Bot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def current_point(self):
        return Point(self.x, self.y)
    
    def next_point(self, d):
        return self.current_point().move(d)


class TestBot(Bot):
    GRID = {Point(0, 0), Point(1, 0), Point(0, -1), Point(-1, -1)}
    DEST = Point(-1, -1)
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def move(self, d):
        np = self.next_point(d)
        if np in self.GRID:
            self.x = np.x
            self.y = np.y
            if np == self.DEST:
                return 2
            else:
                return 1
        else:
            return 0


class InputBot(Bot):
    def __init__(self, x, y, filename):
        self.x = x
        self.y = y
        self.intcode = Intcode.from_file(filename)
        self.process = self.intcode.create_process()
    
    def move(self, d):
        np = self.next_point(d)
        self.process.set_input(d)
        out = self.process.run_to_next_output()
        if out == 1 or out == 2:
            self.x = np.x
            self.y = np.y
        return out


class SearchGrid:
    REV = {1: 2, 2: 1, 3: 4, 4: 3}
    
    def __init__(self, bot):
        self.bot = bot
        self.grid = {Point(0, 0): 0}
        self.dest = 0
        self.oxygen = Point(0, 0)
        self.oxylevels = 0

    def bfs(self, dist=0):
        dnext = []
        for d in range(1, 5):
            np = self.bot.next_point(d)
            out = self.bot.move(d)
            if out == 0:
                self.grid[np] = -1
            else:
                if np not in self.grid:
                    dnext.append(d)
                    self.grid[np] = dist+1
                self.bot.move(self.REV[d])
            if out == 2:
                self.dest = dist+1
                self.oxygen = np
        for d in dnext:
            self.bot.move(d)
            self.bfs(dist+1)
            self.bot.move(self.REV[d])
        return self.dest, self.oxygen

    def bfsoxygen(self, p, dist=0, visited=set()):
        dnext = []
        if dist > self.oxylevels:
            self.oxylevels = dist
        #self.oxylevels = dist+1
        for d in range(1, 5):
            np = p.move(d)
            if np in self.grid and self.grid[np] >= 0:
                if np not in visited:
                    dnext.append(d)
                    visited.add(np)
        for d in dnext:
            self.bfsoxygen(p.move(d), dist+1, visited)
        return self.oxylevels


    def print_grid(self, special={}):
        xmin, xmax = 0, 0
        ymin, ymax = 0, 0
        for p in self.grid:
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
                if p in self.grid:
                    if self.grid[p] == -1:
                        print("#", end="")
                    elif p in special:
                        print(special[p], end="")
                    else:
                        print(".", end="")
                        #print(self.grid[p] % 10, end="")
                else:
                    print(" ", end="")
            print()

if __name__ == '__main__':
    test = SearchGrid(bot=TestBot(0, 0))
    print(test.bfs())
    test.print_grid()
 
    inp = SearchGrid(bot=InputBot(0, 0, "input.txt"))
    print(inp.bfs())
    inp.print_grid({Point(0, 0): '0', Point(-20, 14): 'O'})
    print(inp.bfsoxygen(Point(-20, 14)))
