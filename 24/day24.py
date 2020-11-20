#import numpy as np

def _bitarray_to_int(arr):
    return int("".join(reversed(arr)), 2)

class State:
    GRIDSIZE = 5

    def __init__(self, value: int):
        self.value = value

    def __str__(self):
        return "State({})".format(bin(self.value))

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        if isinstance(other, State):
            return self.value == other.value
        return NotImplemented

    def get_neighbors(self, x, y):
        count = 0
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            count += self.get(x+dx, y+dy)
        return count

    def get(self, x, y):
        if x < 0 or x >= self.GRIDSIZE or y < 0 or y >= self.GRIDSIZE:
            return 0
        else:
            n = y * self.GRIDSIZE + x
            return (self.value & 1 << n) >> n

    def next(self):
        nbits = []
        for j in range(self.GRIDSIZE):
            for i in range(self.GRIDSIZE):
                current = self.get(i, j)
                neighbors = self.get_neighbors(i, j)
                #print("{},{}: current={} neighbors={}".format(i, j, current, neighbors))
                if current == 1:
                    if neighbors == 1:
                        nbits.append('1')
                    else:
                        nbits.append('0')
                else:
                    if neighbors == 1 or neighbors == 2:
                        nbits.append('1')
                    else:
                        nbits.append('0')
        return State(_bitarray_to_int(nbits))

    def print_grid(self):
        for j in range(self.GRIDSIZE):
            for i in range(self.GRIDSIZE):
                if self.get(i, j):
                    print("#", end="")
                else:
                    print(".", end="")
            print()

    def run1(self):
        state = State(self.value)
        seen = set()
        while state not in seen:
            seen.add(state)
            state = state.next()
        return state

    @classmethod
    def read_from_string(cls, s):
        bits=[]
        for l in s.split('\n'):
            if l != "":
                for c in l:
                    if c == '.':
                        bits.append('0')
                    elif c == '#':
                        bits.append('1')
        return cls(_bitarray_to_int(bits))

def test1():
    test = State.read_from_string("""
....#
#..#.
#..##
..#..
#....
    """)

    out = test.run1()
    out.print_grid()
    print(out.value)

test1()

inp = State.read_from_string("""
#.#.#
.#...
...#.
.###.
###.#
""")
out = inp.run1()
out.print_grid()
print(out.value)