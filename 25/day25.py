import itertools
import readline
import sys

if '..' not in sys.path:
    sys.path.append('..')

from intcode import Intcode

class Interpreter:
    def __init__(self, filename, commands):
        self.intcode = Intcode.from_file(filename)
        self.process = self.intcode.create_process()
        self.process.set_ascii_input(commands)

    def run(self):
        while not self.process.is_terminated():
            out = self.process.run_step()
            if self.process.is_blocking_for_output():
                print(chr(out), end="")
            elif self.process.is_blocking_for_input():
                line = input('> ')
                self.process.set_ascii_input([line])


if __name__ == '__main__':
    commands = [l for l in """
west
west
north
take space heater
south
east
south
take festive hat
south
take sand
north
east
take whirled peas
west
north
east
south
take weather machine
north
east
take mug
east
south
east
south
take easter egg
north
west
west
south
west
take shell
south
""".split("\n") if l != '']

    items = [
        'space heater',
        'festive hat',
        'sand',
        'whirled peas',
        'weather machine',
        'mug',
        'easter egg',
        'shell'
    ]

    for r in range(1, len(items)+1):
        for c in itertools.combinations(items, r):
            for i in items:
                commands.append("drop {}".format(i))
            for i in c:
                commands.append("take {}".format(i))
            commands.append("south")

    interp = Interpreter('input.txt', commands)
    interp.run()