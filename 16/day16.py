# -*- coding: utf-8 -*-
"""
Created on Sun Dec 29 20:34:36 2019

@author: matt
"""

import math

import numpy as np

def build_matrix(l, patt=[0, 1, 0, -1]):
    out = []
    for i in range(1, l+1):
        out.extend(build_row(l, i, patt))
    return np.array(out, dtype=np.int64).reshape((l, l)) 
    
def build_row(l, n, patt):
    lneed = l + 1
    repeat = []
    for x in patt:
        repeat.extend([x] * n)
    m = math.ceil(lneed / (len(repeat)))
    #print(lneed, n, repeat)
    return (repeat * m)[1:l+1]

def apply_phases(inp, n):
    x = np.array([int(d) for d in inp], dtype=np.int64)
    mat = build_matrix(x.shape[0])
    for _ in range(n):
        x = abs(mat.dot(x)) % 10
    return "".join([str(d) for d in x])

if __name__ == '__main__':
    print(apply_phases("12345678", 4))
    print(apply_phases("80871224585914546619083218645595", 100)[:8])
    
    inp = ""
    with open("input.txt", "r") as fh:
        for l in fh:
            inp += l.rstrip()
    print(len(inp))
    print(apply_phases(inp, 100)[:8])
    print(len(inp * 10_000))
    print(apply_phases(inp * 10_000, 100)[:100])
    #X = build_matrix(8)
    #a = np.array([1, 2, 3, 4, 5, 6, 7, 8], dtype=np.int64)
    #b = X.dot(a)
    #print(abs(b) % 10)
    #for i in range(1, 9):
    #    print(build_row(8, i, [0, 1, 0, -1]))
    #print(build_row(8, 2, [0, 1, 0, -1]))