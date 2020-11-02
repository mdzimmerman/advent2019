from collections import defaultdict, deque, namedtuple
import string

import numpy as np

def build_chararray(filename, fill_value=' '):
    fh = open(filename, "r")
    lines = []
    width = 0
    for l in fh:
        l = l.rstrip()
        lines.append(l)
        if width < len(l):
            width = len(l)
    height = len(lines)

    grid = np.full(shape=(height, width), fill_value=fill_value, dtype=str)
    for j, l in enumerate(lines):
        grid[j,:len(l)] = [c for c in l]
    return grid

Point = namedtuple("Point", "x y")

class Donut:
    UPPERCASE = string.ascii_uppercase
    DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    def __init__(self, filename):
        self.filename = filename
        self.grid = build_chararray(filename)
        self.height, self.width = self.grid.shape
        self.points = self._build_points()
        self.gates = self._build_gates()

    def _build_points(self):
        points = dict()
        it = np.nditer(self.grid, flags=['multi_index'])
        for c in it:
            j, i = it.multi_index
            pt = Point(i, j)
            if c == '.':
                points[pt] = self._get_label(i, j)
                #print(pt, points[pt])
        return points

    def _build_gates(self):
        gates = defaultdict(set)
        for pt, label in self.points.items():
            if label is not None:
                print(label)
                gates[label].add(pt)
        return gates

    def _get_grid(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return None
        return self.grid[y, x]

    def _get_label(self, x, y):
        if self._get_grid(x, y-1) in Donut.UPPERCASE:
            return self._get_grid(x, y-2) + self._get_grid(x, y-1)
        if self._get_grid(x+1, y) in Donut.UPPERCASE:
            return self._get_grid(x+1, y) + self._get_grid(x+2, y)
        if self._get_grid(x, y+1) in Donut.UPPERCASE:
            return self._get_grid(x, y+1) + self._get_grid(x, y+2)
        if self._get_grid(x-1, y) in Donut.UPPERCASE:
            return self._get_grid(x-2, y) + self._get_grid(x-1, y)
        return None

    def _neighbors(self, pt):
        out = []
        # is this a gate point?
        label = self.points[pt]
        if label is not None:
            out.append(list(self.gates[label] - set(pt))[0])

        # now check the standard dirs
        for dx, dy in Donut.DIRS:
            npt = Point(pt.x+dx, pt.y+dy)
            if npt in self.points:
                out.append(npt)
        return out

    def traverse(self):
        start = next(iter(self.gates['AA']))
        end = next(iter(self.gates['ZZ']))

        queue = deque()
        dist = {start: 0}
        queue.append(start)

        while queue:
            p = queue.pop()
            pdist = dist[p]
            if p == end:
                return dist[p]
            for n in self._neighbors(p):
                if n not in dist:
                    dist[n] = pdist + 1
                    queue.append(n)

        return None

    def print_grid(self):
        height, width = self.grid.shape
        for j in range(height):
            for i in range(width):
                print(self.grid[j,i], end="")
            print()


if __name__ == '__main__':
    d1 = Donut("test1.txt")
    d1.print_grid()
    for k, v in d1.gates.items():
        print(k, v)
    print(d1.traverse())