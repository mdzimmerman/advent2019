#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 12:57:22 2019

@author: mzimmerman
"""

def get(s, i):
    if i < 0 or i >= len(s):
        return None
    else:
        return s[i]

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

def repeats2(s):
    for i in range(0,len(s)-1):
        b, s1, s2, a = get(s,i-1), get(s,i), get(s,i+1), get(s,i+2)
        if b != s1 and s1 == s2 and s2 != a:
            return True
    return False

def string_range(srange):
    imin, imax = srange.split('-')
    for i in range(int(imin), int(imax)+1):
        yield str(i)

if __name__ == '__main__':
    tests = ['111111', '223450', '123789', '112233', '123444', '111122']
    for t in tests:
        print(t, increasing(t), repeats(t), repeats2(t))
        
    count = 0
    srange = '240920-789857'
    #print(inp_min, inp_max)
    for n in string_range(srange):
        if increasing(n) and repeats(n):
            count += 1
    print(count)
    
    count = 0
    for n in string_range(srange):
        if increasing(n) and repeats2(n):
            count += 1
    print(count)
    
