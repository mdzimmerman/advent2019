import re
from collections import namedtuple

PointTuple = namedtuple("PointTuple", "x y")
class Point(PointTuple):
    def add(self, other):
        return Point(self.x + other.x, self.y + other.y)

class Wire():
    PATSTEP = re.compile(r'([UDLR])(\d+)')
    
    def __init__(self, text):
        self.text = text
        self.elements = self._parse_text(self.text)
        #print("Created object 3 %s" % (text,))
        
    def _parse_text(self, text):
        elements = set()
        curr = Point(0, 0)
        elements.add(curr)
        for step in text.split(','):
            m = Wire.PATSTEP.match(step)
            if m:
                d = m.group(1)
                n = m.group(2)
                print(d, n)
            curr = self._add_step(curr, step)
        return set()
            
    def _add_step(self, start, step):
        print(start, step)
        return start
        
if __name__ == '__main__':
    w1 = Wire("R8,U5,L5,D3")
    print(w1)
    