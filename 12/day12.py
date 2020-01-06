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
        #self.planets = deepcopy(self.initplanets)

    def run(self, n):
        t = 0
        planets = deepcopy(self.initplanets)
        #print(planets)
        for _ in range(n):
            for i, a in enumerate(planets):
                #print(i, a)
                for b in planets[i+1:]:
                    self.apply_gravity(a, b)
            for p in planets:
                p.pos = p.pos.add(p.vel)
            t += 1
        self.print_state(planets)
        print('total energy = %d' % (self.system_energy(planets)))
        return planets

    def apply_gravity(self, a, b):
        for dim in ['x', 'y', 'z']:
            self.apply_gravity_dim(a, b, dim)
            
    def apply_gravity_dim(self, a, b, dim):
        if getattr(a.pos, dim) > getattr(b.pos, dim):
            setattr(a.vel, dim, getattr(a.vel, dim)-1)
            setattr(b.vel, dim, getattr(b.vel, dim)+1)
        elif getattr(a.pos, dim) < getattr(b.pos, dim):
            setattr(a.vel, dim, getattr(a.vel, dim)+1)
            setattr(b.vel, dim, getattr(b.vel, dim)-1)
        else:
            pass

    def step_dim(self, dim, planets):
        for i, a in enumerate(planets):
            for b in planets[i+1]:
                self.apply_gravity_dim(a, b, dim)
        for p in planets:
            dpos = getattr(p.pos, dim)
            dvel = getattr(p.vel, dim)
            setattr(p.pos, dim, dpos + dvel)
   
    def run_dim(self, dim):
        init_pos = tuple([getattr(p.pos, dim) for p in self.initplanets])
        init_vel = tuple([getattr(p.vel, dim) for p in self.initplanets])
        print(init_pos, init_vel)
        pos = tuple([-1] * 4)
        vel = tuple([-1] * 4)
        i = 0
        planets = deepcopy(self.initplanets)
        print(planets)
        while pos != init_pos and vel != init_vel:
            i += 1
            self.step_dim(dim, planets)
            pos = tuple([getattr(p.pos, dim) for p in planets])
            vel = tuple([getattr(p.vel, dim) for p in planets])
        
        print(i, init_pos, init_vel)
        #print(init_pos)
        #print(init_vel)
        
        #init_pos = getattr(self.initplanets.pos, dim)  # should be 0
        #init_vel = getattr()
        #while
        
    def system_energy(self, planets):
        te = 0
        for p in planets:
            te += p.te()
        return te

    def print_state(self, planets):
        for p in planets:
            print("%s" % (p,))

if __name__ == '__main__':
    print("-- part 1 --")
    print("test1")
    test1 = Day12([
                Planet(-1, 0, 2),
                Planet(2, -10, -7),
                Planet(4, -8, 8),
                Planet(3, 5, -1)
            ])
    test1.run(10)
    
    print()
    print("test2")
    test2 = Day12([
                Planet(-8, -10, 0),
                Planet(5, 5, 10),
                Planet(2, -7, 3),
                Planet(9, -8, -3)
            ])
    test2.run(100)
    
    print()
    print("input")
    inp = Day12([
                Planet(-13, 14, -7),
                Planet(-18, 9, 0),
                Planet(0, -3, -3),
                Planet(-15, 3, -13)
            ])
    inp.run(1000)
    
    print()
    print("-- part 2 --")
    