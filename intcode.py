import queue

import numpy as np

class Op:
    def __init__(self, name, opcode, params):
        self.name = name
        self.opcode = opcode
        self.params = params
        
    def __repr__(self):
        return ("Op(name=%s opcode=%d params=%d)" % (self.name, self.opcode, self.params))

class IntcodeProcess():
    def __init__(self, intcode):
        self.intcode = intcode
        self.debug = intcode.debug
        self.inp = queue.Queue()
        self.output = []
        self.state = 'RUNNING'
        self.data = np.copy(self.intcode.initdata)
        self.pointer = 0

    def set_input(self, value):
        self.inp.put(value, block=False)

    def get(self, param, mode):
        if mode == 1:
            return param
        else:
            return self.data[param]
        
    def set_value(self, i, value):
        self.data[i] = value
            
    def run_to_next_output(self):
        if self.state == 'TERMINATED':
            return None
        self.state = 'RUNNING'
        output = None
        while self.state == 'RUNNING':
            op, pmodes = self.intcode.get_op(self.data, self.pointer)
            params, pn = self.intcode.get_params(op, self.data, self.pointer)
            if self.debug >= 1:
                print("#%-11s %-16s %-10s %3d" % (op.name, params, pmodes, pn))
            if op.name == 'Add':
                self.set_value(params[2], self.get(params[0], pmodes[0]) + self.get(params[1], pmodes[1]))
            elif op.name == 'Mult':
                self.set_value(params[2], self.get(params[0], pmodes[0]) * self.get(params[1], pmodes[1]))
            elif op.name == 'Input':
                self.set_value(params[0], self.inp.get(block=False))
            elif op.name == 'Output':
                output = self.get(params[0], pmodes[0])
                if self.debug >= 1: 
                    print(output)
                self.output
                self.state = 'BLOCKING_OUTPUT'
            elif op.name == 'JumpIfTrue':
                if self.get(params[0], pmodes[0]) != 0:
                    pn = self.get(params[1], pmodes[1])
            elif op.name == 'JumpIfFalse':
                if self.get(params[0], pmodes[0]) == 0:
                    pn = self.get(params[1], pmodes[1])
            elif op.name == 'LessThan':
                res = 0
                if self.get(params[0], pmodes[0]) < self.get(params[1], pmodes[1]):
                    res = 1
                self.set_value(params[2], res)
            elif op.name == 'Equals':
                res = 0
                if self.get(params[0], pmodes[0]) == self.get(params[1], pmodes[1]):
                    res = 1
                self.set_value(params[2], res)
            elif op.name == 'Stop':
                self.state = 'TERMINATED'
            self.pointer = pn
            if self.debug >=2:
                self.print_data(self.data)
        
        return output
        
class Intcode:
    OPS = [
        Op("Add", 1, 3),
        Op("Mult", 2, 3),
        Op("Input", 3, 1),
        Op("Output", 4, 1),
        Op("JumpIfTrue", 5, 2),
        Op("JumpIfFalse", 6, 2),
        Op("LessThan", 7, 3),
        Op("Equals", 8, 3),
        Op("Stop", 99, 0)]
    OPS_LOOKUP = {}
    for op in OPS:
        OPS_LOOKUP[op.opcode] = op
    
    def __init__(self, csvdata, debug=False):
        self.initdata = np.array(csvdata.split(','), dtype=np.int64)
        self.debug = debug

    @classmethod
    def from_file(cls, filename, debug=False):
        csvdata = ""
        with open(filename, "r") as fh:
            for l in fh:
                csvdata += l.rstrip()
        return cls(csvdata, debug=debug)

    def get_op(self, data, p):
        opcode = (data[p]) % 100
        #print(opcode)
        if opcode in self.OPS_LOOKUP:
            op = self.OPS_LOOKUP[opcode]
            pmodes = []
            for i in range(op.params):
                pmode = (data[p] // (10 ** (i+2))) % 10
                pmodes.append(pmode)
            #print(op, pmodes)
            return op, pmodes
        else:
            raise Exception("bad opcode %d at p=%d" % (opcode, p))

    def get_params(self, op, data, p):
        params = []
        for _ in range(op.params):
            p += 1
            params.append(data[p])
        p += 1
        return params, p
    
    def create_process(self, noun=None, verb=None, inp=[]):
        process = IntcodeProcess(self)
        if noun != None:
            process.set_value(1, noun)
        if verb != None:
            process.set_value(2, verb)
        for i in inp:
            process.set_input(i)
        return process
    
    def run(self, noun=None, verb=None, inp=[]):
        process = self.create_process(noun, verb, inp)
        output = []
        while process.state != 'TERMINATED':
            out = process.run_to_next_output()
            output.append(out)
            if self.debug >= 2:
                print(out)
                print(process.state)

        return output

    def run_all(self, stop=None):
        for n in range(100):
            for v in range(100):
                out = self.run(n, v)
                if self.debug: print("noun=%2d verb=%2d out=%d" % (n, v, out))
                if out == stop:
                    return (n, v)

    def print_data(self, data):
        print(",".join(data.astype(str)))

if __name__ == '__main__':
    test = Intcode('1,9,10,3,2,3,11,0,99,30,40,50', debug=True)
    test.run()
