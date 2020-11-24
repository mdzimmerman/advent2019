# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 21:13:31 2020

@author: matt
"""

import sys

if '..' not in sys.path:
    sys.path.append('..')
    
from intcode import Intcode

ic = Intcode.from_file("input.txt", debug=0)

#p = ic.create_process()
#print(p.run_to_next_output(), p.state)

for y in range(50):
    for x in range(100):
        o = ic.run(inp=[x, y])
        if o[0] == 1:
            print("#", end="")
        else:
            print(".", end="")
    print()


count = 0
for x in range(5, 100):
    y1, y2 = None, None
    o_last = 0
    y = 0
    #print(x)
    while y2 is None:
        o = ic.run(inp=[x, y])[0]
        #print("  ", x, y, o)
        if o == 1 and o_last == 0:
            y1 = y
        elif o == 0 and o_last == 1:
            y2 = y-1
        #print(y, o)
        y += 1
        o_last = o
    print(x, y1, y2)
