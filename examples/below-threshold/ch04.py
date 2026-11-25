"""Enumerated toy decoder: the same syndrome can hide opposite logical effects."""
from collections import defaultdict
from math import isclose

# Synthetic training histogram, not samples from a quantum processor.
training = {"000": 1800, "100": 40, "010": 40, "001": 40,
            "110": 50, "101": 10, "011": 10, "111": 10}
# A separately specified deployment distribution, with the same ordering.
deployment = {"000": .895, "100": .020, "010": .020, "001": .020,
              "110": .030, "101": .005, "011": .005, "111": .005}

def syndrome(error):
    a, b, c = map(int, error)
    return (a ^ b, b ^ c)

counts = defaultdict(lambda: [0, 0])
for error, count in training.items():
    counts[syndrome(error)][int(error[0])] += count
learned = {s: int(n[1] > n[0]) for s, n in counts.items()}
# Minimum-weight correction: first-bit effect of the lightest error.
lightest = {}
for error in sorted(training, key=lambda e: (e.count("1"), e)):
    lightest.setdefault(syndrome(error), int(error[0]))

def risk(decoder):
    return sum(p for e, p in deployment.items()
               if decoder[syndrome(e)] != int(e[0]))

assert isclose(sum(deployment.values()), 1)
assert syndrome("001") == syndrome("110") == (0, 1)
assert learned[(0, 1)] == 1 and lightest[(0, 1)] == 0
floor = sum(min(sum(p for e, p in deployment.items()
                    if syndrome(e) == s and int(e[0]) == y)
                for y in (0, 1)) for s in counts)
# Drift may make the training-derived lookup worse than the deployment optimum.
assert risk(learned) >= floor - 1e-12
print("Ambiguous syndrome:", syndrome("001"))
print(f"Minimum-weight failure: {risk(lightest):.3%}")
print(f"Learned lookup failure: {risk(learned):.3%}")
print(f"Information-limited floor: {floor:.3%}")
