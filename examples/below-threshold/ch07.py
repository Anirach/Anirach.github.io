"""Toy workflow: verify source/compiled behaviour independently of gate count."""
from itertools import product
import hashlib
import json


def run(bits, gates):
    state = list(bits)
    for control, target in gates:
        state[target] ^= state[control]
    return tuple(state)


def check(source, compiled, max_gates):
    equivalent = all(run(x, source) == run(x, compiled)
                     for x in product((0, 1), repeat=3))
    within_budget = len(compiled) <= max_gates
    return equivalent, within_budget, equivalent and within_budget


source = [(0, 1), (0, 1), (1, 2)]
candidates = {"cancel pair": [(1, 2)], "delete all": []}
for label, compiled in candidates.items():
    same, fits, accept = check(source, compiled, max_gates=1)
    print(f"{label}: equivalent={same}, budget={fits}, accept={accept}")
assert check(source, candidates["cancel pair"], 1) == (True, True, True)
assert check(source, candidates["delete all"], 1) == (False, True, False)
record = {"source": source, "candidates": candidates, "inputs": 8}
digest = hashlib.sha256(json.dumps(record, sort_keys=True).encode()).hexdigest()
print(f"record SHA-256: {digest}")
