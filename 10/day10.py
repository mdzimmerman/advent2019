#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 13:34:49 2019

@author: mzimmerman
"""

#import numpy as np

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __key(self):
        return (self.x, self.y)
    
    def __hash__(self):
        return hash(self.__key())
    
    def __eq__(self, other):
        if isinstance(other, Point):
            return self.__key() == other.__key()
        return NotImplemented

    def __repr__(self):
        return "Point(%d %d)" % (self.x, self.y)
    
    def dist(self, other):
        if isinstance(other, Point):
            return abs(self.x - other.x) + abs(self.y - other.y)
        return NotImplemented        

class Day10:
    def __init__(self, filename):
        self.data, self.width, self.height = self._read_file(filename)
        self.filename = filename
        
    def _read_file(self, filename):
        d = set()
        w = 0
        h = 0
        with open(filename, "r") as fh:
            for j, l in enumerate(fh):
                l = l.rstrip()
                if j == 0:
                    w = len(l)
                h += 1
                for i, c in enumerate(l):
                    if c == '#':
                        d.add(Point(i, j))
        return d, w, h
    
if __name__ == '__main__':
    test1 = Day10("test1.txt")
    print(test1.data)
    for a in test1.data:
        print(a)
        for b in sorted(test1.data - set([a]), key=lambda x: x.dist(a), reverse=True):
            print("    ",b, b.dist(a))

        
