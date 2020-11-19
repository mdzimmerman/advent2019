import numpy as np
import re

class Deck:
    PAT_REVERSE = re.compile(r'deal into new stack')
    PAT_ROTATE  = re.compile(r'cut (-?\d+)')
    PAT_DEAL    = re.compile(r'deal with increment (\d+)')

    def __init__(self, size, deck=None):
        self.size = size
        if deck is None:
            self.deck = np.arange(self.size)
        else:
            self.deck = deck

    def __str__(self):
        return "Deck({})".format(self.deck)

    def reverse(self):
        return Deck(size=self.size, deck=np.flipud(self.deck).copy())

    def rotate(self, n):
        return Deck(size=self.size, deck=np.concatenate([self.deck[n:], self.deck[0:n]]))

    def deal(self, n):
        dn = np.zeros(shape=self.deck.shape, dtype=self.deck.dtype)
        offset = 0
        for i in range(self.size):
            dn[offset] = self.deck[i]
            offset += n
            if offset >= self.size:
                offset = offset % self.size
        return Deck(size=self.size, deck=dn)

    @classmethod
    def shuffle(cls, operations, deck):
        for op in str.splitlines(operations):
            #print("[{}]".format(op))
            m = cls.PAT_REVERSE.match(op)
            if m:
                deck = deck.reverse()
                #print("  {}".format(deck))
                continue
            m = cls.PAT_ROTATE.match(op)
            if m:
                n = int(m.group(1))
                deck = deck.rotate(n)
                #print("  {}".format(deck))
                continue
            m = cls.PAT_DEAL.match(op)
            if m:
                n = int(m.group(1))
                deck = deck.deal(n)
                #print("  {}".format(deck))
                continue
        return deck

t = Deck(10)

def test(deck, expected):
    value = " ".join(str(n) for n in deck.deck)
    assert value == expected, "'{}' != '{}'".format(value, expected)

print(t)
test(t.reverse(),  "9 8 7 6 5 4 3 2 1 0")
test(t.rotate(3),  "3 4 5 6 7 8 9 0 1 2")
test(t.rotate(-4), "6 7 8 9 0 1 2 3 4 5")
test(t.deal(3),    "0 7 4 1 8 5 2 9 6 3")

test(Deck.shuffle("""
deal with increment 7
deal into new stack
deal into new stack
""", Deck(10)), "0 3 6 9 2 5 8 1 4 7")

test(Deck.shuffle("""
cut 6
deal with increment 7
deal into new stack
""", Deck(10)), "3 0 7 4 1 8 5 2 9 6")

test(Deck.shuffle("""
deal with increment 7
deal with increment 9
cut -2
""", Deck(10)), "6 3 0 7 4 1 8 5 2 9")

test(Deck.shuffle("""
deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1
""", Deck(10)), "9 2 5 8 1 4 7 0 3 6")

inptext = None
with open("input.txt", "r") as fh:
    inptext = fh.read()

out = Deck.shuffle(inptext, Deck(10007))
print(out)
print(np.where(out.deck == 2019))