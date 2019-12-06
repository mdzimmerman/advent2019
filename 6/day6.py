#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 11:15:42 2019

@author: mzimmerman
"""

import networkx as nx

class Orbits:
    def __init__(self, filename):
        self.graph = self._parse_file(filename)
        self.filename = filename
    
    def _parse_file(self, filename):
        graph = nx.DiGraph()
        with open(filename, 'r') as fh:
            for l in fh:
                src, dst = l.rstrip().split(')')
                graph.add_edge(src, dst)
        return graph
    
    def get_ancestors(self, n, ancestors):
        for p in self.graph.predecessors(n):
            ancestors.append(p)
            self.get_ancestors(p, ancestors)
            #print(p, ancestors)
        return ancestors
    
    def checksum(self):
        total = 0
        for n in self.graph:
            a = len(self.get_ancestors(n, []))
            total += a
            #print(n, na)
        return total
    
    def orbital_transfers(self, n1, n2):
        n1path = self.get_ancestors(n1, [])
        n2path = self.get_ancestors(n2, [])
        print(n1path)
        print(n2path)
        for i, n1p in enumerate(n1path):
            for j, n2p in enumerate(n2path):
                if n1p == n2p:
                    print(n1p, i, j, i+j)
                    return i+j
                
if __name__ == '__main__':
    test = Orbits("test.txt")
    print(test.checksum())
    
    test2 = Orbits("test2.txt")
    print(test2.orbital_transfers("YOU", "SAN"))
    
    inp = Orbits("input.txt")
    print(inp.checksum())
    print(inp.orbital_transfers("YOU", "SAN"))