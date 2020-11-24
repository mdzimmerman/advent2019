from collections import namedtuple
from enum import Enum
import queue

import numpy as np

OpType = namedtuple('OpType', ['name', 'opcode', 'nparams'])


class Op:
    OPTYPES = [
        OpType("Add", 1, 3),
        OpType("Mult", 2, 3),
        OpType("Input", 3, 1),
        OpType("Output", 4, 1),
        OpType("JumpIfTrue", 5, 2),
        OpType("JumpIfFalse", 6, 2),
        OpType("LessThan", 7, 3),
        OpType("Equals", 8, 3),
        OpType("AdjustRel", 9, 1),
        OpType("Stop", 99, 0)]
    OPTYPE_LOOKUP = {}
    for t in OPTYPES:
        OPTYPE_LOOKUP[t.opcode] = t

    def __init__(self, optype, params, pmodes, pointer):
        self.optype = optype
        self.params = params
        self.pmodes = pmodes
        self.pointer = pointer
        
    def __repr__(self):
        return "Op(optype=%s params=%d pmodes=%d, pointer=%d)" \
               % (self.optype, self.params, self.pmodes, self.pointer)

    @classmethod
    def get_op(cls, data, p):
        opcode_raw = data[p]
        opcode = (data[p]) % 100
        p += 1
        if opcode in cls.OPTYPE_LOOKUP:
            optype = cls.OPTYPE_LOOKUP[opcode]
            params = []
            pmodes = []
            for i in range(optype.nparams):
                params.append(data[p])
                pmode = (opcode_raw // (10 ** (i+2))) % 10
                pmodes.append(pmode)
                p += 1
            return cls(optype, params, pmodes, p)
        else:
            raise Exception("bad opcode %d at p=%d" % (opcode, p))


class State(Enum):
    RUNNING         = 0
    BLOCKING_OUTPUT = 1
    TERMINATED      = 2
    BLOCKING_INPUT  = 3



class IntcodeProcess:
    #RUNNING, BLOCKING_OUTPUT, TERMINATED, BLOCKING_INPUT = 0, 1, 2, 3

    def __init__(self, intcode, input_on_empty=None):
        self.intcode = intcode
        self.input_on_empty = input_on_empty
        self.debug = intcode.debug
        self.inp = queue.Queue()
        self.output = []
        self.state = State.RUNNING
        self.data = np.copy(self.intcode.initdata)
        self.relbase = 0
        self.pointer = 0

    def is_running(self):
        return self.state == State.RUNNING

    def is_blocking_for_input(self):
        return self.state == State.BLOCKING_INPUT

    def is_blocking_for_output(self):
        return self.state == State.BLOCKING_OUTPUT

    def is_terminated(self):
        return self.state == State.TERMINATED

    def set_input(self, value):
        self.inp.put(value, block=False)

    def set_ascii_input(self, lines):
        for l in lines:
            for x in [ord(c) for c in l]:
                self.inp.put(x, block=False)
            self.inp.put(10, block=False)

    def get(self, param, mode):
        if mode == 2:
            i = self.relbase + param
            self._resize_data(i)
            return self.data[i]
        if mode == 1:
            return param
        else:
            i = param
            self._resize_data(i)
            return self.data[i]

    def set_value(self, param, pmode, value):
        i = param
        if pmode == 2:
            i = self.relbase + param
        self._resize_data(i)
        self.data[i] = value

    def run_step(self):
        if self.state == State.TERMINATED:
            return None
        self.state = State.RUNNING
        op = Op.get_op(self.data, self.pointer)
        params = op.params
        pmodes = op.pmodes
        pn = op.pointer
        if self.debug >= 1:
            print("#%-11s %-16s %-10s %3d" % (op.optype.name, params, pmodes, pn))
        if op.optype.name == 'Add':
            self.set_value(params[2], pmodes[2], self.get(params[0], pmodes[0]) + self.get(params[1], pmodes[1]))
        elif op.optype.name == 'Mult':
            self.set_value(params[2], pmodes[2], self.get(params[0], pmodes[0]) * self.get(params[1], pmodes[1]))
        elif op.optype.name == 'Input':
            if self.inp.empty():
                if self.input_on_empty is None:
                    self.state = State.BLOCKING_INPUT
                    # don't update pointer so we come back to this point
                    return None
                else:
                    self.set_value(params[0], pmodes[0], self.input_on_empty)
            else:
                inputval = self.inp.get(block=False)
                #print("  reading input value {}".format(inputval))
                self.set_value(params[0], pmodes[0], inputval)
        elif op.optype.name == 'Output':
            output = self.get(params[0], pmodes[0])
            if self.debug >= 1:
                print(output)
            self.output.append(output)
            self.state = State.BLOCKING_OUTPUT
            self.pointer = pn
            return output
        elif op.optype.name == 'JumpIfTrue':
            if self.get(params[0], pmodes[0]) != 0:
                pn = self.get(params[1], pmodes[1])
        elif op.optype.name == 'JumpIfFalse':
            if self.get(params[0], pmodes[0]) == 0:
                pn = self.get(params[1], pmodes[1])
        elif op.optype.name == 'LessThan':
            res = 0
            if self.get(params[0], pmodes[0]) < self.get(params[1], pmodes[1]):
                res = 1
            self.set_value(params[2], pmodes[2], res)
        elif op.optype.name == 'Equals':
            res = 0
            if self.get(params[0], pmodes[0]) == self.get(params[1], pmodes[1]):
                res = 1
            self.set_value(params[2], pmodes[2], res)
        elif op.optype.name == 'AdjustRel':
            self.relbase += self.get(params[0], pmodes[0])
        elif op.optype.name == 'Stop':
            self.state = State.TERMINATED
            return None
        self.pointer = pn
        if self.debug >= 2:
            print(self.data)
        return None

    def run_to_next_output(self):
        out = None
        self.state = State.RUNNING
        while self.state != State.BLOCKING_OUTPUT and self.state != State.TERMINATED:
            #print(self.state)
            out = self.run_step()
        #print(self.state, out)
        return out

    def run(self):
        output = []
        while self.state != State.TERMINATED:
            output.append(self.run_to_next_output())
        return(output)

    def _resize_data(self, i):
        """Resize data if i refers to an index beyond the current size of the ndarray"""

        # TODO: probably should resize to the next largest power of 2 rather than i+1
        if i >= self.data.shape[0]:
            self.data.resize(i+1)


class Intcode:
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
    
    def create_process(self, noun=None, verb=None, inp=[], ascii_inp=None):
        process = IntcodeProcess(self)
        if noun is not None:
            process.set_value(1, noun)
        if verb is not None:
            process.set_value(2, verb)

        if ascii_inp is not None:
            process.set_ascii_input(ascii_inp)
        else:
            for i in inp:
                process.set_input(i)
        return process
    
    def run(self, noun=None, verb=None, inp=[], ascii_inp=None):
        process = self.create_process(noun, verb, inp, ascii_inp)
        return process.run()

    def run_all(self, stop=None):
        for n in range(100):
            for v in range(100):
                out = self.run(n, v)
                if self.debug:
                    print("noun=%2d verb=%2d out=%s" % (n, v, out))
                if out == stop:
                    return (n, v)

    def print_data(self):
        print(",".join(self.initdata.astype(str)))


if __name__ == '__main__':
    test = Intcode('1,9,10,3,2,3,11,0,99,30,40,50', debug=True)
    test.run()
