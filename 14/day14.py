# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 18:13:32 2019

@author: matt
"""

from collections import defaultdict
import math

class Ingr:
    def __init__(self, n, name):
        self.n = n
        self.name = name
        
    def __repr__(self):
        return "Ingr(%d %s)" % (self.n, self.name)

    @classmethod
    def parse(cls, text):
        n, name = text.split(" ")
        return cls(int(n), name)

class Rule:
    def __init__(self, ingr, result):
        self.ingr = ingr
        self.result = result

    def __repr__(self):
        return "Rule(ingr=%s result=%s)" % (self.ingr, self.result)
        
    @classmethod
    def parse(cls, text):
        text_ingr, text_result = text.split(" => ")
        ingr = []
        for i in text_ingr.split(", "):
            ingr.append(Ingr.parse(i))
        result = Ingr.parse(text_result)
        return cls(ingr, result)

class Nanofactory:
    ORE_RULE = Rule([], Ingr(1, "ORE"))
    
    def __init__(self, filename):
        self.rules = []
        with open(filename, "r") as fh:
            for l in fh:
                self.rules.append(Rule.parse(l.rstrip()))
        self.ruleindex = dict()
        for r in self.rules:
            self.ruleindex[r.result.name] = r
        self.surplus = defaultdict(int)

    def print_rules(self):
        for r in self.rules:
            print(r)

    def make_fuel(self, n):
        self.surplus = defaultdict(int)
        return self.make("FUEL", n)

    def make(self, elem, n):
        #print("#%s %d %s" % (elem, n, self.surplus))
        rule = self.ORE_RULE
        if elem in self.ruleindex:
            rule = self.ruleindex[elem]
        existing = self.surplus[elem]
        m = math.ceil(max(n-existing,0) / rule.result.n)
        extra = (rule.result.n * m) - (n - existing)
        if elem != "ORE":
            self.surplus[elem] = extra
        ore = 0
        for ingr in rule.ingr:
            if ingr.name == "ORE":
                ore += m * ingr.n
            else:
                ore += self.make(ingr.name, m * ingr.n)
        return ore
        
if __name__ == '__main__':
    print("test1")
    test1 = Nanofactory("test1.txt")
    print(test1.make_fuel(1))

    print("test2")
    test2 = Nanofactory("test2.txt")
    print(test2.make_fuel(1))
    
    print("input")
    inp = Nanofactory("input.txt")
    print(inp.make_fuel(1))
    
    
    for f in range(11):
        print("%2d %8d" % (f, inp.make_fuel(f)))
    
    def binary_search(a, b, x, f, depth=0):
        #if depth > 10:
        #    return
        #print("#binary_search(%d, %d)" % (a, b))
        if a == b:
            return a
        elif (b-a) == 1:
            #xa = f(a)
            #xb = f(b)
            #print(xa, xb)
            return a
        else:
            mid = (a + b+1)//2
            xmid = f(mid)
            #print("   %d %d" % (mid, xmid))
            if xmid == x:
                return mid
            elif xmid < x:
                return binary_search(mid, b, x, f, depth+1)
            else:
                return binary_search(a, mid, x, f, depth+1)
    
    print(binary_search(1, 1_000_000_000, 1_000_000_000_000, inp.make_fuel))    
    #print(inp.make_fuel(1_000_000_000))    