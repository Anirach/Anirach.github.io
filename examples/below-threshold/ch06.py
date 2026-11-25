"""Exact synthesis for three-bit linear reversible maps over GF(2)."""
from collections import deque
from itertools import product

N = 3
identity = tuple(1 << i for i in range(N))
gates = [(c, t) for c in range(N) for t in range(N) if c != t]

def apply(matrix, gate):
    control, target = gate
    rows = list(matrix)
    rows[target] ^= rows[control]
    return tuple(rows)

# Breadth-first search has unit-cost edges, so first discovery is shortest.
paths = {identity: []}
queue = deque([identity])
while queue:
    matrix = queue.popleft()
    for gate in gates:
        nxt = apply(matrix, gate)
        if nxt not in paths:
            paths[nxt] = paths[matrix] + [gate]
            queue.append(nxt)
original = [(0, 1), (1, 2), (0, 1), (0, 1), (2, 0)]
target = identity
for gate in original:
    target = apply(target, gate)
optimized = paths[target]

def run(bits, circuit):
    bits = list(bits)
    for control, target_bit in circuit:
        bits[target_bit] ^= bits[control]
    return tuple(bits)

inputs = list(product((0, 1), repeat=N))
assert len(paths) == (8-1)*(8-2)*(8-4) == 168
assert all(run(x, original) == run(x, optimized) for x in inputs)
assert all(run(run(x, optimized), reversed(optimized)) == x for x in inputs)
print(f"Invertible maps checked: {len(paths)}")
print(f"CNOT count: original={len(original)}, exact shortest={len(optimized)}")
print("Shortest circuit:", optimized)
print(f"Equivalence and inverse verified on all {len(inputs)} inputs")
