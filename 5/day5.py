#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 13:06:55 2019

@author: mzimmerman
"""

import sys

if '..' not in sys.path:
    sys.path.append('..')

from intcode import Intcode

test = Intcode("1002,4,3,4,33", debug=2)
test.run()

inp = Intcode.from_file("input.txt", debug=1)
#print(inp.initdata)
inp.run(inp=1)

inp.run(inp=5)