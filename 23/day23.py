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
        self.n_empty_input = 0

    def is_idle(self, tries=10):
        return len(self.queue) == 0 and self.n_empty_input >= tries


class Network:
    NODES = 50

    def __init__(self, nic_code_file, idle_tries=10):
        self.nic_code = Intcode.from_file(nic_code_file)
        self.nodes = self._create_nodes()
        self.nat_packet = None
        self.nat_y_values = set()
        self.idle_tries = idle_tries

    def _create_nodes(self):
        nodes = []
        for i in range(self.NODES):
            nodes.append(Node(self.nic_code, i))
        return nodes

    def _network_is_idle(self):
        return all(n.is_idle(self.idle_tries) for n in self.nodes)

    def run(self):
        running = True

        y = None
        i = 0
        while running:
            i += 1
            messages = []
            #print(i)
            for node in self.nodes:
                out = node.nic.run_step()
                if node.nic.is_running():
                    pass
                elif node.nic.is_terminated():
                    messages.append("node {}: node dead".format(node.addr))
                elif node.nic.is_blocking_for_input():
                    if len(node.queue) == 0:
                        node.n_empty_input += 1
                        node.nic.set_input(-1)
                        #node.history.append('i')
                        #print("  node {}: reading empty input, adding -1".format(node.addr))
                    else:
                        node.n_empty_input = 0
                        p = node.queue.popleft()
                        node.nic.set_input(p.x)
                        node.nic.set_input(p.y)
                        #messages.append("node {}: reading packet {}".format(node.addr, p))
                elif node.nic.is_blocking_for_output():
                    node.n_empty_input = 0
                    paddr = out
                    px = node.nic.run_to_next_output()
                    py = node.nic.run_to_next_output()
                    p = Packet(paddr, px, py)
                    if paddr >= self.NODES:
                        messages.append("node {}: sending packet to NAT: {}".format(node.addr, p))
                        self.nat_packet = p
                        #for j, n in enumerate(self.nodes):
                        #    print("node {}: {} {}".format(j, n.queue, n.is_idle()))
                        #return p
                    else:
                        #messages.append("node {}: sending packet {}".format(node.addr, p))
                        self.nodes[paddr].queue.append(p)
            if self._network_is_idle() and isinstance(self.nat_packet, Packet):
                messages.append("nat: sending packet {} to node 0".format(self.nat_packet))
                y = self.nat_packet.y
                if y in self.nat_y_values:
                    # found the value sent twice
                    running = False
                else:
                    self.nat_y_values.add(y)
                    self.nodes[0].queue.append(self.nat_packet)
                    self.nat_packet = None
            if len(messages) > 0:
                for m in messages:
                    print("{:4d}: {}".format(i, m))
        print(y)

if __name__ == '__main__':
    n = Network("input.txt")
    n.run()


