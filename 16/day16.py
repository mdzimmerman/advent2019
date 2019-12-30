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

def fft(inp, nphases):
    x = np.array([int(d) for d in inp], dtype=np.int64)
    mat = build_matrix(x.shape[0])
    for _ in range(nphases):
        x = abs(mat.dot(x)) % 10
    return "".join([str(d) for d in x])

def fastfft(inp, nphases):
    offset = int(inp[:7])
    #print("offset = %d" % (offset,))
    inpfull = (inp * 10_000)[offset:]
    #print("len(inpfull) = %d" % (len(inpfull),))
    xlen = len(inpfull)
    x = np.array([int(d) for d in inpfull], dtype=np.int64)
    for n in range(nphases):
        #print("# n=%d" % (n,))
        xnew = np.zeros(shape=(xlen,), dtype=np.int64)
        xsum = 0
        for i in range(xlen-1, -1, -1):
            xsum += x[i]
            xnew[i] = xsum
        x = abs(xnew) % 10
    return "".join([str(d) for d in x[:8]])

if __name__ == '__main__':
    inp = ""
    with open("input.txt", "r") as fh:
        for l in fh:
            inp += l.rstrip()
    print("len(inp) = %d" % (len(inp),))

    print()
    print("-- part1 --")
    print("tests")
    print(fft("12345678", 4))
    print(fft("80871224585914546619083218645595", 100)[:8])
    print("input")
    print(fft(inp, 100)[:8])
    
    print()
    print("-- part2 --")
    print("tests")
    print(fastfft("03036732577212944063491565474664", 100))
    print(fastfft("02935109699940807407585447034323", 100))
    print(fastfft("03081770884921959731165446850517", 100))
    print("input")
    print(fastfft(inp, 100))
