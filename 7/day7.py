# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 08:12:26 2019

@author: matt
"""

import itertools
import sys

if '..' not in sys.path:
    sys.path.append('..')

from intcode import Intcode

class Day5:
    def __init__(self, program, namps=5, debug=0):
        self.amps = []
        self.namps = namps
        self.debug = debug
        for _ in range(namps):
            self.amps.append(Intcode(program, debug=debug))
    
    @classmethod
    def from_file(cls, filename, namps=5, debug=0):
        program = ""
        with open(filename, "r") as fh:
            for l in fh:
                program += l.rstrip()
        return cls(program, namps, debug)
    
    def run_amps(self, phase_setting):
        inp = 0
        for i, amp in enumerate(self.amps):
            out = amp.run(inp=[phase_setting[i],inp])
            #print(out)
            inp = out[0]
        return(inp)
        
    def run_all(self):
        best_settings, best_output = "", 0
        for s in itertools.permutations(range(self.namps)):
            output = self.run_amps(s)
            settings = "".join([str(si) for si in s])
            #print(settings, output)
            if output > best_output:
                best_settings, best_output = settings, output
        return best_settings, best_output

test1 = Day5("3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0", debug=0)
print("test1")
print(test1.run_amps([4,3,2,1,0]))
print(test1.run_all())

test2 = Day5("3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0")
print("test2")
print(test2.run_all())

test3 = Day5("3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0")
print("test3")
print(test3.run_all())

inp = Day5.from_file("input.txt")
print("input #1")
print(inp.run_all())