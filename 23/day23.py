from collections import deque, namedtuple
import sys

if '..' not in sys.path:
    sys.path.append('..')

from intcode import Intcode

Packet = namedtuple("Packet", ['addr', 'x', 'y'])

class Node:
    def __init__(self, nic_code: Intcode, addr: int):
        self.addr = addr
        self.nic = nic_code.create_process(inp=addr)
        self.nic.run_to_next_output()
        self.queue = deque()

    def run_to_next_packet(self):
        paddr = self.nic.run_to_next_output()
        if paddr is None and not self.nic.is_terminated():
            if len(self.queue) > 0:
                p = self.queue.popleft()
                self.nic.set_input(p.x)
                self.nic.set_input(p.y)
                return None
            else:
                self.nic.set_input(-1)
                return None
        elif paddr is not None:
            px = self.nic.run_to_next_output()
            py = self.nic.run_to_next_output()
            return Packet(paddr, px, py)

class Network:
    NODES = 50

    def __init__(self, nic_code_file):
        self.nic_code = Intcode.from_file(nic_code_file)
        self.nodes = self._create_nodes()

    def _create_nodes(self):
        nodes = []
        for i in range(self.NODES):
            nodes = Node(self.nic_code, i)
        return nodes

    def run_to 