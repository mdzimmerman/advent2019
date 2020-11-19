#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 17:20:41 2019

@author: mzimmerman
"""

import sys

if '..' not in sys.path:
    sys.path.append('..')

from intcode import Intcode

class SpringScript:
    def __init__(self, filename):
        self.intcode = Intcode.from_file(filename)

    def run(self, code=[]):
        for l in code:
            print(l)
        p = self.intcode.create_process()
        p.set_ascii_input(code)
        for c in p.run():
            if c is None:
                pass
            elif c >= 256:
                print(c)
            else:
                print(chr(c), end="")

if __name__ == '__main__':
    sscript = SpringScript("input.txt")

    #sscript.run(["AND D J", "WALK"])

    #sscript.run([
    #    "NOT A J",
    #    "NOT B T",
    #    "AND T J",
    #    "NOT C T",
    #    "AND T J",
    #    "AND D J",
    #    "WALK",
    #])

    sscript.run([
        "NOT A T",
        "NOT B J",
        "OR T J",
        "NOT C T",
        "OR T J",
        "AND D J",
        "WALK"
    ])

    sscript.run([
        "NOT C J",
        "AND D J",
        "AND H J",
        "NOT B T",
        "AND D T",
        "OR T J",
        "NOT A T",
        "OR T J",
        "RUN"
    ])


