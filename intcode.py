import numpy as np

class Op:
    def __init__(self, name, opcode, params):
        self.name = name
        self.opcode = opcode
        self.params = params
        
    def __repr__(self):
        return ("Op(name=%s opcode=%d params=%d)" % (self.name, self.opcode, self.params))

class Intcode:
    OPS = [
        Op("Add", 1, 3),
        Op("Mult", 2, 3),
        Op("Input", 3, 1),
        Op("Output", 4, 1),
        Op("Stop", 99, 0)]
    OPS_LOOKUP = {}
    for op in OPS:
        OPS_LOOKUP[op.opcode] = op
    
    def __init__(self, csvdata, debug=False):
        self.initdata = np.array(csvdata.split(','), dtype=np.int64)
        self.debug = debug

    def get_op(self, data, p):
        opcode = data[p]
        if opcode in self.OPS_LOOKUP:
            return self.OPS_LOOKUP[opcode]
        else:
            raise Exception("bad opcode %d at p=%d" % (opcode, p))

    def get_params(self, op, data, p):
        params = []
        for _ in range(op.params):
            p += 1
            params.append(data[p])
        p += 1
        return params, p

    def run(self, noun=None, verb=None):
        p = 0
        data = np.copy(self.initdata)
        if noun != None:
            data[1] = noun
        if verb != None:
            data[2] = verb
        if self.debug: self.print_data(data)
        while True:
            op = self.get_op(data, p)
            params, p = self.get_params(op, data, p)
            if op.name == 'Add':
                data[params[2]] = data[params[0]] + data[params[1]]
            elif op.name == 'Mult':
                data[params[2]] = data[params[0]] * data[params[1]]
            elif op.name == 'Stop':
                return data[0]
            if self.debug: self.print_data(data)

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
