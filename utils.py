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