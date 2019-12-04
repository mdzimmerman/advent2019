from collections import namedtuple
import re

PointTuple = namedtuple("PointTuple", "x y")
class Point(PointTuple):
    def add(self, other):
        return Point(self.x + other.x, self.y + other.y)

class Wire():
    PATSTEP = re.compile(r'([UDLR])(\d+)')
    DIR = {'U': Point(0,1), 'D': Point(0,-1), 'L': Point(-1,0), 'R': Point(1,0)}
    ORIGIN = Point(0,0)
    
    def __init__(self, text, debug=0):
        self.text = text
        self.debug = debug
        self.elements = self._parse_text(self.text)
        #print("Created object 3 %s" % (text,))

    def __str__(self):
        return("Wire(%s)" % (self.text,))
        
    def _parse_text(self, text):
        if self.debug >= 2:
            print(text)
        elements = dict()
        curr = Point(0, 0)
        i = 0
        elements[curr] = i
        for step in text.split(','):
            m = Wire.PATSTEP.match(step)
            if m:
                d = m.group(1)
                n = int(m.group(2))
                for j in range(n):
                    curr = curr.add(Wire.DIR[d])
                    i += 1
                    elements[curr] = i
                    if self.debug >= 2:
                        print(curr)
        return elements
    
    @classmethod
    def find_intersections(cls, wires, criteria="manhattan", debug=0):
        dist_min = 1_000_000
        set1 = set(wires[0].elements.keys())
        set2 = set(wires[1].elements.keys())
        for inter in set1.intersection(set2):
            if inter == Wire.ORIGIN:
                next
            else:
                if criteria == "manhattan":
                    dist = abs(inter.x) + abs(inter.y)
                elif criteria == "wire":
                    dist = wires[0].elements[inter] + wires[1].elements[inter]
                if debug >= 1:
                    print(inter, dist)
                if dist < dist_min:
                    dist_min = dist
        return dist_min
        
    @classmethod
    def read_wires(cls, filename, debug=0):
        wires = []
        with open(filename, "r") as fh:
            for l in fh:
                wires.append(cls(l.rstrip(), debug=debug))
                if debug >= 1: print(wires[-1])
        return(wires)
        
if __name__ == '__main__':
    print("## test 1 ##")
    w1 = Wire("R8,U5,L5,D3", debug=1)
    w2 = Wire("U7,R6,D4,L4", debug=1)
    print(w1)
    print(w2)
    print(Wire.find_intersections([w1,w2]))
    print(Wire.find_intersections([w1,w2], criteria="wire", debug=1))
    
    print("## test 2 ##")
    test2 = Wire.read_wires("test2.txt", debug=1)
    print(Wire.find_intersections(test2))
    print(Wire.find_intersections(test2, criteria="wire"))
    
    print("## test 3 ##")
    test3 = Wire.read_wires("test3.txt", debug=1)
    print(Wire.find_intersections(test3))
    print(Wire.find_intersections(test3, criteria="wire"))
    
    print("## input ##")
    inp = Wire.read_wires("input.txt", debug=0)
    print(Wire.find_intersections(inp))
    print(Wire.find_intersections(inp, criteria="wire"))
    