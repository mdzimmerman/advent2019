# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 22:07:51 2019

@author: matt
"""

import sys

if '..' not in sys.path:
    sys.path.append('..')

from point import Vec3

class Planet:
    def __init__(self, x, y, z):
        self.pos = Vec3(x, y, z)
        self.vel = Vec3(0, 0, 0)

    def __repr__(self):
        return "Planet(pos=%s vel=%s)" % (self.pos, self.vel)


class Day12:
    def __init__(self, planets):
        self.planets = planets

    def step(self):
        pass

    def apply_gravity(self, a, b):
        pass
        
        
if __name__ == '__main__':
    test1 = Day12([
                Planet(-1, 0, 2),
                Planet(2, -10, -7),
                Planet(4, -8, 8),
                Planet(3, 5, -1)
            ])
    