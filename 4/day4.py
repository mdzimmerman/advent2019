#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 12:57:22 2019

@author: mzimmerman
"""

def increasing(s):
    for i in range(1,len(s)):
        if s[i-1] > s[i]:
            return False
    return True

def repeats(s):
    for i in range(1,len(s)):
        if s[i-1] == s[i]:
            return True
    return False

if __name__ == '__main__':
    tests = ['111111', '223450', '123789']
    for t in tests:
        print(t, increasing(t), repeats(t))
        
    count = 0
    inp_min, inp_max = '240920-789857'.split('-')
    #print(inp_min, inp_max)
    for n in [str(i) for i in range(int(inp_min), int(inp_max)+1)]:
        if increasing(n) and repeats(n):
            count += 1
    print(count)
    
