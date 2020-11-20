import readline
import sys

if '..' not in sys.path:
    sys.path.append('..')

from intcode import Intcode

class Interpreter:
    def __init__(self, filename):
        self.intcode = Intcode.from_file(filename)
        self.process = self.intcode.create_process()

    def run(self):
        while not self.process.is_terminated():
            out = self.process.run_step()
            if self.process.is_blocking_for_output():
                print(chr(out), end="")
            elif self.process.is_blocking_for_input():
                line = input('> ')
                self.process.set_ascii_input([line])


if __name__ == '__main__':
    interp = Interpreter('input.txt')
    interp.run()