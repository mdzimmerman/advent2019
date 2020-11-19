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
        print(self.nic.run_to_next_output())
        print(self.nic.state)
        self.queue = deque()

    def run_to_next_packet(self):
        print("Running node {}".format(self.addr))
        paddr = self.nic.run_to_next_output()
        if paddr is None and self.nic.is_blocking_for_input():
            if len(self.queue) > 0:
                p = self.queue.popleft()
                print("  Input: {}".format(p))
                self.nic.set_input(p.x)
                self.nic.set_input(p.y)
                return None
            else:
                print("  Input: {}".format(-1))
                self.nic.set_input(-1)
                return None
        elif paddr is not None:
            px = self.nic.run_to_next_output()
            py = self.nic.run_to_next_output()
            p = Packet(paddr, px, py)
            print("  Output: {}".format(p))
            return p

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

    def run_step(self):
        for node in self.nodes:
            node.run_to_next_packet()


if __name__ == '__main__':
    n = Network("input.txt")
    n.run_step()


