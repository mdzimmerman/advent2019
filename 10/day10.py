#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 13:34:49 2019

@author: mzimmerman
"""

import math


class Slope:
    def __init__(self, dx, dy):
        gcd = math.gcd(dx, dy)
        self.dx = dx // gcd
        self.dy = dy // gcd
        self.heading = self._calc_heading()

    def __key(self):
        return self.dx, self.dy

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Slope):
            return self.__key() == other.__key()
        return NotImplemented

    def __repr__(self):
        return "Slope(%d %d)" % (self.dx, self.dy)

    def _calc_heading(self):
        rad = math.atan2(-self.dy, self.dx)  # -y because y-axis is inverted
        if rad < 0:
            rad += 2 * math.pi
        deg = rad * 360 / (2 * math.pi)
        return (90.0 - deg) % 360.0


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

    def slope(self, other):
        if isinstance(other, Point):
            return Slope(other.x - self.x, other.y - self.y)
        return NotImplemented

    def point_along_slope(self, slope, n=1):
        if isinstance(slope, Slope):
            return Point(self.x + n * slope.dx, self.y + n * slope.dy)
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

    def find_best_location(self):
        vis_count = {}
        for a in self.data:
            vis_count[a] = 0
            bs = sorted(self.data - set([a]), key=lambda x: x.dist(a), reverse=True)
            for i, b in enumerate(bs):
                visible = True
                for c in bs[i + 1:]:
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

    def kill_asteroid(self, p0):
        others = self.data - {p0}
        slopes = set()
        for s in [p0.slope(x) for x in others]:
            slopes.add(s)

        killed = []
        while len(others) > 0:
            for s in sorted(slopes, key=lambda x: x.heading):
                #print(s, s.heading)
                i = 1
                p = p0.point_along_slope(s, i)
                while 0 <= p.x < self.width and 0 <= p.y < self.height:
                    if p in others:
                        others.remove(p)
                        killed.append(p)
                        if len(killed) % 10 == 0:
                            print()
                            self.print_grid(others)
                        break

                    i += 1
                    p = p0.point_along_slope(s, i)
            #print()
            #self.print_grid(others)
        for p in killed:
            print(p)

    def print_grid(self, data=None):
        if data is None:
            data = self.data
        for j in range(self.height):
            for i in range(self.width):
                if Point(i, j) in data:
                    print("#", end="")
                else:
                    print(".", end="")
            print()


if __name__ == '__main__':
    def test_is_between():
        print("test is_between()")
        a = Point(0, 0)
        tests = [
            (Point(6, 4), Point(1, 0), False),
            (Point(6, 4), Point(1, 1), False),
            (Point(6, 4), Point(3, 2), True),
            (Point(6, 2), Point(3, 1), True)
        ]
        for b, c, expect in tests:
            # print(a, b, c, c.is_between(a, b))
            assert c.is_between(a, b) == expect


    def test_slope():
        print("test Slope.heading")
        expected_headings = {
            Point(0, -2): 0.0,
            Point(2, 0): 90.0,
            Point(0, 2): 180.0,
            Point(-2, 0): 270.0
        }
        p0 = Point(0, 0)
        for j in range(-2, 3):
            for i in range(-2, 3):
                p1 = Point(i, j)
                if p0 != p1:
                    s = p0.slope(p1)
                    # print(p1, s, s.heading)
                    if p1 in expected_headings:
                        assert s.heading == expected_headings[p1]


    test_is_between()
    test_slope()

    test5 = Day10("test6.txt")
    test5.kill_asteroid(Point(8, 3))
