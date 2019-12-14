import sys

if '..' not in sys.path:
    sys.path.append('..')

from intcode import Intcode

print("test1")
test1 = Intcode("109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99", debug=1)
print(test1.run())

print()
print("test2")
test2 = Intcode("1102,34915192,34915192,7,4,7,99,0", debug=1)
print(test2.run())

print()
print("test3")
test3 = Intcode("104,1125899906842624,99", debug=1)
print(test3.run())

print()
print("part #1")
inp = Intcode.from_file("input.txt", debug=1)
print(inp.run(inp=[1]))

print()
print("part #2")
inp.run(inp=[2])