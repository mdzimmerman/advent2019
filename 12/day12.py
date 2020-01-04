# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 22:07:51 2019

@author: matt
"""

from copy import deepcopy
from functools import reduce
import sys

if '..' not in sys.path:
    sys.path.append('..')

from point import Vec3

def gcd(a, b):
    """Return greatest common divisor using Euclid's Algorithm."""
    while b:      
        a, b = b, a % b
    return a

def lcm(a, b):
    """Return lowest common multiple."""
    return a * b // gcd(a, b)

def lcmm(*args):
    """Return lcm of args."""   
    return reduce(lcm, args)

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

class System:
    def __init__(self, planets):
        self.initpos=[[], [], []]
        self.initvel=[[], [], []]
        self.nplanets = 0
        for p in planets:
            self.nplanets += 1
            for i, d in enumerate(p):
                self.initpos[i].append(d)
                self.initvel[i].append(0)
    
    def step_dim(self, pos, vel):
        for i in range(self.nplanets):
            for j in range(i+1, self.nplanets):
                if pos[i] > pos[j]:
                    vel[i] -= 1
                    vel[j] += 1
                elif pos[i] < pos[j]:
                    vel[i] += 1
                    vel[j] -= 1
        for i in range(self.nplanets):
            pos[i] += vel[i]
    
    def find_dim_repeat(self, d):
        pos = deepcopy(self.initpos[d])
        vel = deepcopy(self.initvel[d])
        i = 1
        self.step_dim(pos, vel)
        while pos != self.initpos[d] or vel != self.initvel[d]:
            i += 1
            self.step_dim(pos, vel)
        return i
    
    def find_repeat(self):
        repeats = []
        for d in range(3):
            r = self.find_dim_repeat(d)
            print("d=%d repeat=%d" % (d, r))
            repeats.append(r)
        return(lcmm(repeats[0], repeats[1], repeats[2]))
    
    
if __name__ == '__main__':
    test1 = Day12([
                Planet(-1, 0, 2),
                Planet(2, -10, -7),
                Planet(4, -8, 8),
                Planet(3, 5, -1)
            ])
    
    t1b = System([
                [-1, 0, 2],
                [2, -10, -7],
                [4, -8, 8],
                [3, 5, -1]
            ])
    print(t1b.find_repeat())
    
    t2b = System([
            [-8, -10,  0],
            [ 5,   5, 10],
            [ 2,  -7,  3],
            [ 9,  -8, -3]
        ])
    print(t2b.find_repeat())
    
    inp = System([
                (-13, 14,  -7),
                (-18,  9,   0),
                (  0, -3,  -3),
                (-15,  3, -13)
            ])
    print(inp.find_repeat())
    