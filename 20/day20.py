from collections import defaultdict, deque, namedtuple
import logging
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

PointBase = namedtuple("PointBase", "x y")
class Point(PointBase):
    DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    def neighbors(self):
        for dx, dy in Point.DIRS:
            yield Point(self.x+dx, self.y+dy)

class Donut:
    UPPERCASE = string.ascii_uppercase

    def __init__(self, filename):
        self.logger = logging.getLogger("Donut")
        self.logger.setLevel(logging.INFO)

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
        return points

    def _build_gates(self):
        gates = defaultdict(set)
        for pt, label in self.points.items():
            if label is not None:
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
        # is this a gate point? the other gate point is also my neighbor
        label = self.points[pt]
        for npt in self.gates[label]:
            if npt != pt:
                yield npt

        # now check the standard directions
        for npt in pt.neighbors():
            if npt in self.points:
                yield npt

    def traverse(self):
        """BFS search for shortest path from start to end"""
        start = next(iter(self.gates['AA']))
        end = next(iter(self.gates['ZZ']))

        queue = deque()
        dist = {start: 0}
        queue.append(start)

        while queue:
            self.logger.debug(queue)
            p = queue.popleft()
            pdist = dist[p]
            self.logger.debug("   d={}, phead={}".format(pdist, p))
            if p == end:
                return pdist
            neighbors = self._neighbors(p)
            self.logger.debug("   neighbors={}".format(neighbors))
            for n in neighbors:
                if n not in dist:
                    dist[n] = pdist + 1
                    queue.append(n)

        return None

    def print_grid(self):
        height, width = self.grid.shape
        for j in range(height):
            for i in range(width):
                print(self.grid[j, i], end=" ")
            print()


if __name__ == '__main__':
    def test1():
        t = Donut("test1.txt")
        t.print_grid()
        out = t.traverse()
        print(out)
        assert out == 23

    def test2():
        t = Donut("test2.txt")
        t.print_grid()
        out = t.traverse()
        print(out)
        assert out == 58

    test1()
    test2()

    inp = Donut("input.txt")
    print(inp.traverse())