import re
from collections import namedtuple

PointTuple = namedtuple("PointTuple", "x y")
class Point(PointTuple):
    def add(self, other):
        return Point(self.x + other.x, self.y + other.y)

class Wire():
    PATSTEP = re.compile(r'([UDLR])(\d+)')
    DIR = {'U': Point(0,1), 'D': Point(0,-1), 'L': Point(-1,0), 'R': Point(1,0)}
    
    def __init__(self, text, debug=False):
        self.text = text
        self.debug = debug
        self.elements = self._parse_text(self.text)
        #print("Created object 3 %s" % (text,))
        
    def _parse_text(self, text):
        if self.debug:
            print(text)
        elements = set()
        curr = Point(0, 0)
        elements.add(curr)
        for step in text.split(','):
            m = Wire.PATSTEP.match(step)
            if m:
                d = m.group(1)
                n = int(m.group(2))
                for i in range(n):
                    curr = curr.add(Wire.DIR[d])
                    elements.add(curr)
                    if self.debug:
                        print(curr)
        return elements
            
    def _add_step(self, start, step):
        print(start, step)
        return start
        
if __name__ == '__main__':
    w1 = Wire("R8,U5,L5,D3", debug=True)
    w2 = Wire("U7,R6,D4,L4", debug=True)
    