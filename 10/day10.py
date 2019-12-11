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

    @staticmethod
    def is_between(a, b, c):
        """Is point c on the line segment between points a and b?"""
        crossprod = (c.y - a.y) * (b.x - a.x) - (c.x - a.x) * (b.y - a.y)
        if abs(crossprod) != 0:
            return False
        if c.x < min(a.x, b.x) or c.x > max(a.x, b.x) or c.y < min(a.x, b.x) or c.y > max(a.x, b.x):
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
    
if __name__ == '__main__':
    a = Point(0, 0)
    ptest = [
            (Point(6,4), Point(1,0)),
            (Point(6,4), Point(1,1)),
            (Point(6,4), Point(3,2)),
            (Point(6,2), Point(3,1))]
    for b, c in ptest:
        print(a,b,c,Point.is_between(a,b,c))
    
    test1 = Day10("test1.txt")
    #print(test1.data)
    for a in test1.data:
        bs = sorted(test1.data - set([a]), key=lambda x: x.dist(a), reverse=True)
        for i, b in enumerate(bs):
            for c in bs[i+1:]:
                print("check %s-%s %s" % (a, b, c))

        #print(a, bs)
        
        #for b in sorted(test1.data), key=lambda x: x.dist(a), reverse=True):
        #    next if b == a:
        #    print("    ",b, b.dist(a))
        #    for c in 

