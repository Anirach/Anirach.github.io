"""Toy MaxCut: compare a local optimum with an exact small-instance answer."""
from itertools import product

EDGES = [(0, 1), (0, 5), (1, 2), (2, 4), (3, 4), (3, 5), (4, 5)]


def cut(bits):
    return sum(bits[a] != bits[b] for a, b in EDGES)


def greedy(bits):
    while True:
        neighbours = [bits[:i] + (1 - bits[i],) + bits[i + 1:]
                      for i in range(len(bits))]
        candidate = max(neighbours, key=cut)
        if cut(candidate) <= cut(bits):
            return bits
        bits = candidate


local = greedy((0,) * 6)
exact = max(product((0, 1), repeat=6), key=cut)
print(f"greedy: cut={cut(local)}/{len(EDGES)}, partition={local}")
print(f"exact:  cut={cut(exact)}/{len(EDGES)}, partition={exact}")
print(f"greedy relative gap={(cut(exact) - cut(local)) / cut(exact):.2%}")
assert 0 <= cut(local) <= cut(exact) <= len(EDGES)
assert cut(local) == cut(tuple(1 - x for x in local))
assert all(cut(local[:i] + (1-local[i],) + local[i+1:]) <= cut(local)
           for i in range(6))
