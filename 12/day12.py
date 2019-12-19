# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 22:07:51 2019

@author: matt
"""

from copy import deepcopy
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

    def pe(self):
        return abs(self.pos.x) + abs(self.pos.y) + abs(self.pos.z)
    
    def ke(self):
        return abs(self.vel.x) + abs(self.vel.y) + abs(self.vel.z)
    
    def te(self):
        return self.pe() * self.ke()

class Day12:
    def __init__(self, planets):
        self.initplanets = planets

    def run(self, n):
        self.t = 0
        self.planets = deepcopy(self.initplanets)
        for _ in range(n):
            for i, a in enumerate(self.planets):
                for b in self.planets[i+1:]:
                    self.apply_gravity(a, b)
            for p in self.planets:
                p.pos = p.pos.add(p.vel)
            self.t += 1

    def apply_gravity(self, a, b):
        for dim in ['x', 'y', 'z']:
            if getattr(a.pos, dim) > getattr(b.pos, dim):
                setattr(a.vel, dim, getattr(a.vel, dim)-1)
                setattr(b.vel, dim, getattr(b.vel, dim)+1)
            elif getattr(a.pos, dim) < getattr(b.pos, dim):
                setattr(a.vel, dim, getattr(a.vel, dim)+1)
                setattr(b.vel, dim, getattr(b.vel, dim)-1)
            else:
                pass
        
    def system_energy(self):
        te = 0
        for p in self.planets:
            te += p.te()
        return te

    def print_state(self):
        print("Day12(")
        for p in self.planets:
            print("  %s" % (p,))
        print(")")

if __name__ == '__main__':
    test1 = Day12([
                Planet(-1, 0, 2),
                Planet(2, -10, -7),
                Planet(4, -8, 8),
                Planet(3, 5, -1)
            ])
    test1.print_state()
    test1b = deepcopy(test1)
    for _ in range(10):
        test1.step()
    test1.print_state()
    test1b.print_state()
    #for p in test1.planets:
    #    print(p)
    print(test1.system_energy())
    
    #test2 = Day12([
    #            Planet(-8, -10, 0),
    #            Planet(5, 5, 10),
    #            Planet(2, -7, 3),
    #            Planet(9, -8, -3)
    #        ])
    #for _ in range(100):
    #    test2.step()
    #for p in test2.planets:
    #    print(p)
    #print(test2.system_energy())
    
    #inp = Day12([
    #            Planet(-13, 14, -7),
    #            Planet(-18, 9, 0),
    #            Planet(0, -3, -3),
    #            Planet(-15, 3, -13)
    #        ])
    #for _ in range(1000):
    #    inp.step()
    #for p in inp.planets:
    #    print(p)
    #print(inp.system_energy())
    