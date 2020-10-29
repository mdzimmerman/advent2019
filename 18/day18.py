from collections import namedtuple
import heapq
import itertools
import string
import time

import numpy as np

Point = namedtuple("Point", 'x y char')

class Path:
    def __init__(self, endpt: Point, keys: frozenset):
        self.endpt = endpt
        self.keys = keys

    def __repr__(self):
        return "Path(endpt={}, keys={}".format(self.endpt, self.keys)

    def __key(self):
        return (self.endpt, self.keys)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Path):
            return self.__key() == other.__key()
        return NotImplemented

class PriorityQueue:
    def __init__(self):
        self.pq = []
        self.entry_finder = {}
        self.REMOVED = '<REMOVED>'
        self.counter = itertools.count()

    def add(self, item, priority=0):
        if item in self.entry_finder:
            if priority > self.entry_finder[item][0]:
                return
            self.remove(item)
        count = next(self.counter)
        entry = [priority, count, item]
        self.entry_finder[item] = entry
        heapq.heappush(self.pq, entry)

    def remove(self, item):
        entry = self.entry_finder.pop(item)
        entry[-1] = self.REMOVED

    def pop(self):
        while self.pq:
            priority, count, item = heapq.heappop(self.pq)
            if item is not self.REMOVED:
                del self.entry_finder[item]
                return priority, item
        raise KeyError('pop from an empty PriorityQueue')


class Maze:
    DOORS = set(string.ascii_uppercase)
    KEYS = set(string.ascii_lowercase)
    DIRS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    def __init__(self, lines):
        self.lines = lines
        self._build_grid(lines)
        self.all_keys = self._get_all_keys()

    def _build_grid(self, lines):
        self.grid = np.array([list(l) for l in lines])

    def _get_all_keys(self):
        return frozenset(c for c in self.grid.flatten() if c in Maze.KEYS)

    def print_grid(self):
        c, r = self.grid.shape
        for j in range(c):
            print("".join(self.grid[j, :]))

    def point_for_char(self, char):
        loc = np.where(self.grid == char)
        x = loc[1][0]
        y = loc[0][0]
        return Point(x, y, char)

    def neighbors(self, p, keys=set()):
        for dx, dy in Maze.DIRS:
            x = p.x + dx
            y = p.y + dy
            c = self.grid[y, x]
            if c == '.'  or c == '@' or c in self.all_keys or (c in Maze.DOORS and c.lower() in keys):
                yield Point(x, y, c)

    def get_available_keys(self, p, keys=set()):
        distance = {p: 0}
        queue = [p]

        # use BFS to find keys currently available
        newkeys = dict()
        while queue:
            s = queue.pop(0)
            if s.char in self.all_keys and s.char not in keys:
                newkeys[s] = distance[s]
            else:
                for n in self.neighbors(s, keys):
                    if n not in distance:
                        distance[n] = distance[s]+1
                        queue.append(n)
        return newkeys

    def get_available_paths(self):
        #full_paths = []
        start_time = time.time()
        origin = Path(self.point_for_char("@"), keys=frozenset())
        pq = PriorityQueue()
        pq.add(origin, 0)

        node = origin
        while node != pq.REMOVED:
            try:
                dist, node = pq.pop()
            except:
                break
            print(dist, node)
            if node.keys == self.all_keys:
                print("Exec time: {:.4f} seconds".format(time.time() - start_time))
                #full_paths.append({"dist": dist, "node": node})
                return dist
            for n_point, n_dist in self.get_available_keys(node.endpt, node.keys).items():
                n_node = Path(n_point, keys=frozenset(node.keys | {n_point.char}))
                pq.add(n_node, dist + n_dist)

        #for p in full_paths:
        #    print(p)


    @classmethod
    def from_file(cls, filename):
        with open(filename, "r") as fh:
            lines = []
            for l in fh:
                l = l.rstrip()
                lines.append(l)
            return cls(lines)


if __name__ == '__main__':
    for i in range(1, 6):
        f = "test{}.txt".format(i)
        print("--- {} ---".format(f))
        t = Maze.from_file(f)
        t.print_grid()
        print("result = {}".format(t.get_available_paths()))
        print()

    inp = Maze.from_file("input.txt")
    print("result = {}".format(inp.get_available_paths()))
