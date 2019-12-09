#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 10:17:19 2019

@author: mzimmerman
"""

import numpy as np

class SIF:
    def __init__(self, data, width, height):
        self.data   = data
        self.width  = width
        self.height = height
        self.layers = self._parse_data()
        self.nlayers = self.layers.shape[0]
        
    @classmethod
    def from_file(cls, filename, width, height):
        data = ""
        with open(filename, "r") as fh:
            for d in fh:
                data += d.rstrip()
        return cls(data, width, height)
        
    def _parse_data(self):
        nlayers = len(self.data) // (self.width * self.height)
        layers = np.array([int(c) for c in self.data]).reshape((nlayers, self.height, self.width))
        return layers
    
    def flatten(a, b): 
        if a == 2: 
            return b 
        else: 
            return a

    vflatten = np.vectorize(SIF.flatten)
    
    def decode(self):
        out = self.layers[0].copy()
        for i in range(1,self.nlayers):
            out = self.vflatten(out, self.layers[i])
        for j in range(self.height):
            for i in range(self.width):
                if out[j,i] == 1:
                    print('##', end="")
                else:
                    print('--', end="")
            print()
    
if __name__ == '__main__':
    test = SIF("123456789012", width=3, height=2)
    print(test.layers)
    print(test.layers[1])
    
    inp = SIF.from_file("input.txt", width=25, height=6)
    #print(inp.layers.shape)
    #print(np.sum(inp.layers[0] == 1))
    nmin = (150, 0, 0)
    for i in range(inp.nlayers):
        l = inp.layers[i]
        ncurr = (np.sum(l == 0), np.sum(l == 1), np.sum(l == 2))
        if ncurr[0] < nmin[0]:
            nmin = ncurr
    print(nmin)
    print(nmin[1] * nmin[2])
    #for i in inp.layers:
    #    c = np.count_nonzero(inp.layers[i,:,:] == 1)
    #    print(i,c)

    inp.decode()        