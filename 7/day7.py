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

class Day7:
    def __init__(self, program, namps=5, debug=0):
        #self.amps = []
        self.namps = namps
        self.debug = debug
        self.amp = Intcode(program, debug)
        #for _ in range(namps):
        #    self.amps.append(Intcode(program, debug=debug))
    
    @classmethod
    def from_file(cls, filename, namps=5, debug=0):
        program = ""
        with open(filename, "r") as fh:
            for l in fh:
                program += l.rstrip()
        return cls(program, namps, debug)
    
    def run_amps(self, phase_setting):
        inp = 0
        for i in range(self.namps):
            out = self.amp.run(inp=[phase_setting[i],inp])
            #print(out)
            inp = out[0]
        return(inp)
    
    def run_amps_feedback(self, phase_setting):
        # create an IntcodeProcess for each amp and set first input 
        # of each to phase_setting[i]
        amp_process = []
        for i in range(self.namps):
            amp_process.append(self.amp.create_process(inp=[phase_setting[i]]))
    
        inp = 0
        outall = []
        while True:
            for i in range(self.namps):
                amp_process[i].set_input(inp)
                out = amp_process[i].run_to_next_output()
                #print(out)
                if out != None:
                    outall.append(out)
                if amp_process[i].is_terminated():
                    print(outall)
                    return outall[-1]
                inp = out
    
    def run_all(self, permute=[0, 1, 2, 3, 4], method=None):
        if method == None:
            method = self.run_amps
        best_settings, best_output = "", 0
        for s in itertools.permutations(permute):
            output = method(s)
            settings = "".join([str(si) for si in s])
            if output > best_output:
                best_settings, best_output = settings, output
        return best_settings, best_output

test1 = Day7("3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0", debug=0)
print("test1")
print(test1.run_amps([4,3,2,1,0]))
print(test1.run_all())

test2 = Day7("3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0")
print("test2")
print(test2.run_all())

test3 = Day7("3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0")
print("test3")
print(test3.run_all())

inp = Day7.from_file("input.txt")
print("input #1")
print(inp.run_all())

test4 = Day7("3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5")
print("test4")
print(test4.run_amps_feedback([9,8,7,6,5]))

test5 = Day7("3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10")
print("test5")
print(test5.run_amps_feedback([9,7,8,5,6]))

print("input #2")
print(inp.run_all(permute=[5,6,7,8,9], method=inp.run_amps_feedback))
