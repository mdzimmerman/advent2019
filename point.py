# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 23:42:31 2019

@author: matt
"""

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __key(self):
        return self.x, self.y

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.__key() == other.__key()
        return NotImplemented

    def __repr__(self):
        return "Point(%d %d)" % (self.x, self.y)

    def add(self, other):
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        return NotImplemented

    def dist(self, other):
        if isinstance(other, Point):
            return abs(self.x - other.x) + abs(self.y - other.y)
        return NotImplemented

    def move(self, d):
        nx, ny = self.x, self.y
        if d == 1:
            ny += 1
        elif d == 2:
            ny -= 1
        elif d == 3:
            nx -= 1
        elif d == 4:
            nx += 1
        else:
            raise Exception("bad direction")
        return Point(nx, ny)


class Vec3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __key(self):
        return self.x, self.y, self.z

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Vec3):
            return self.__key() == other.__key()
        return NotImplemented

    def __repr__(self):
        return "Vec3(%d %d %d)" % (self.x, self.y, self.z)

    def add(self, other):
        if isinstance(other, Vec3):
            return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)
        return NotImplemented

    def dist(self, other):
        if isinstance(other, Vec3):
            return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)
        return NotImplemented