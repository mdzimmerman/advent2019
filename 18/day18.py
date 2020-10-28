import numpy as np

class Maze:
    def __init__(self, lines):
        self.lines = lines
        self._build_grid(lines)

    def _build_grid(self, lines):
        self.grid = np.array([list(l) for l in lines])

    def print_grid(self):
        c, r = self.grid.shape
        for j in range(c):
            print("".join(self.grid[j, :]))

    @classmethod
    def from_file(cls, filename):
        with open(filename, "r") as fh:
            lines = []
            for l in fh:
                l = l.rstrip()
                lines.append(l)
            return cls(lines)

if __name__ == '__main__':
    t1 = Maze.from_file("test1.txt")
    t1.print_grid()
    #print(np.where(t1.grid == '.'))
