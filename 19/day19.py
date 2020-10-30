# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 21:13:31 2020

@author: matt
"""

import sys

if '..' not in sys.path:
    sys.path.append('..')
    
from intcode import Intcode

ic = Intcode.from_file("input.txt")

p = ic.create_process()
#print(p.run_to_next_output(), p.state)

count = 0
for y in range(60):
    for x in range(100):
        o = ic.run(inp=[x, y])
        if o[0] == 1:
            print("#", end="")
            count += 1
        elif o[0] == 0:
            print(".", end="")
    print()
print(count)