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

    def is_between(self, a, b):
        """Is self on the line segment between points a and b?"""
        crossprod = (self.y - a.y) * (b.x - a.x) - (self.x - a.x) * (b.y - a.y)
        if abs(crossprod) != 0:
            return False
        if self.x < min(a.x, b.x) or self.x > max(a.x, b.x):
            return False
        if self.y < min(a.y, b.y) or self.y > max(a.y, b.y):
            return False
        return True

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
    
    def find_best_location(self):
        vis_count = {}
        for a in self.data:
            vis_count[a] = 0
            bs = sorted(self.data - set([a]), key=lambda x: x.dist(a), reverse=True)
            for i, b in enumerate(bs):
                visible = True
                for c in bs[i+1:]:
                    if c.is_between(a, b):
                        visible = False
                        break
                if visible:
                    vis_count[a] += 1
        vis_max, a_max = 0, None
        for a in sorted(self.data, key=lambda x: (x.y, x.x)):
            print(a, vis_count[a])
            if vis_count[a] > vis_max:
                vis_max, a_max = vis_count[a], a
        return vis_max, a_max
    
if __name__ == '__main__':
    a = Point(0, 0)
    ptest = [
            (Point(6,4), Point(1,0)),
            (Point(6,4), Point(1,1)),
            (Point(6,4), Point(3,2)),
            (Point(6,2), Point(3,1))]
    for b, c in ptest:
        print(a, b, c, c.is_between(a, b))
    
    test1 = Day10("test1.txt")
    print(test1.find_best_location())
    
    inp = Day10("input.txt")
    print(inp.find_best_location())
