from collections import deque, namedtuple
import sys

if '..' not in sys.path:
    sys.path.append('..')

from intcode import Intcode

Packet = namedtuple("Packet", ['addr', 'x', 'y'])

class Node:
    def __init__(self, nic_code: Intcode, addr: int):
        self.addr = addr
        self.nic = nic_code.create_process()
        self.nic.set_input(addr)
        self.queue = deque()

class Network:
    NODES = 50

    def __init__(self, nic_code_file):
        self.nic_code = Intcode.from_file(nic_code_file)
        self.nodes = self._create_nodes()

    def _create_nodes(self):
        nodes = []
        for i in range(self.NODES):
            nodes.append(Node(self.nic_code, i))
        return nodes

    def run(self):
        running = True

        i = 0
        while running:
            i += 1
            print(i)
            for node in self.nodes:
                out = node.nic.run_step()
                if node.nic.is_running():
                    pass
                elif node.nic.is_terminated():
                    print("  node {}: node dead".format(node.addr))
                elif node.nic.is_blocking_for_input():
                    if len(node.queue) == 0:
                        node.nic.set_input(-1)
                        #print("  node {}: reading empty input, adding -1".format(node.addr))
                    else:
                        p = node.queue.popleft()
                        node.nic.set_input(p.x)
                        node.nic.set_input(p.y)
                        print("  node {}: reading packet {}".format(node.addr, p))
                elif node.nic.is_blocking_for_output():
                    paddr = out
                    px = node.nic.run_to_next_output()
                    py = node.nic.run_to_next_output()
                    p = Packet(paddr, px, py)
                    if paddr >= self.NODES:
                        print("Final packet: {}".format(p))
                        return p
                    else:
                        print("  node {}: sending packet {}".format(node.addr, p))
                        self.nodes[paddr].queue.append(p)


if __name__ == '__main__':
    n = Network("input.txt")
    n.run()


