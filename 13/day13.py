from collections import defaultdict
import sys

if '..' not in sys.path:
    sys.path.append('..')

from intcode import Intcode
from point import Point


class Blocks:
    EMPTY, WALL, BLOCK, PADDLE, BALL = 0, 1, 2, 3, 4
    PIXEL = {
        EMPTY:  ' ',
        WALL:   '*',
        BLOCK:  '#',
        PADDLE: '=',
        BALL:   '@'
    }

    def __init__(self, filename):
        self.intcode = Intcode.from_file(filename)
        self.process = None
        self.data = defaultdict(int)
        self.xmax = 0
        self.ymax = 0

    def run(self):
        self.process = self.intcode.create_process()
        self.process.set_value(0, 0, 2)

        score = 0
        ball = None
        paddle = None
        while not self.process.is_terminated():
            x = self.process.run_to_next_output()
            y = self.process.run_to_next_output()
            t = self.process.run_to_next_output()

            if x is None and self.process.is_blocking_for_input():
                # we've reached an Input instruction and the queue is empty
                # so move the joystick
                print("score: %d, blocks remaining: %d" % (score, self.count_blocks()))
                self.print_data()
                if paddle.x > ball.x:
                    self.process.set_input(-1)
                elif paddle.x < ball.x:
                    self.process.set_input(1)
                else:
                    self.process.set_input(0)
                continue
            elif x == -1 and y == 0:
                # score update
                score = t
            elif x is not None and y is not None:
                # update pixel
                p = Point(x, y)
                if p.x > self.xmax:
                    self.xmax = p.x
                if p.y > self.ymax:
                    self.ymax = p.y

                if t == self.BALL:
                    ball = p
                elif t == self.PADDLE:
                    paddle = p
                self.data[Point(x, y)] = t

        print("score: %d, blocks remaining: %d" % (score, self.count_blocks()))
        self.print_data()

    def count_blocks(self):
        n = 0
        for p in self.data.keys():
            if self.data[p] == self.BLOCK:
                n += 1
        return n

    def print_data(self):
        for j in range(self.ymax+1):
            for i in range(self.xmax+1):
                d = self.data[Point(i, j)]
                print(self.PIXEL[d], end='')
            print()


inp = Blocks("input.txt")
inp.run()

#print(count_blocks(data))
#print_data(data)