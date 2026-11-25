"""Exact two-amplitude teaching model: a phase error can hide in Z readout."""
from math import isclose, sqrt


def apply(gate, state):
    return tuple(sum(gate[i][j] * state[j] for j in range(2)) for i in range(2))


def probabilities(state):
    return tuple(round(abs(a) ** 2, 6) for a in state)


r = 1 / sqrt(2)
H = ((r, r), (r, -r))
X = ((0, 1), (1, 0))
Z = ((1, 0), (0, -1))
Y = ((0, -1j), (1j, 0))
zero = (1 + 0j, 0j)
plus = apply(H, zero)
minus = apply(Z, plus)
print("|+>, measured in Z:", probabilities(plus))
print("Z|+>, measured in Z:", probabilities(minus))
print("H|+>, measured in Z:", probabilities(apply(H, plus)))
print("HZ|+>, measured in Z:", probabilities(apply(H, minus)))
print("X|0>, measured in Z:", probabilities(apply(X, zero)))
print("Y|0>, measured in Z:", probabilities(apply(Y, zero)))

assert probabilities(plus) == probabilities(minus)
assert probabilities(apply(H, plus)) == (1.0, 0.0)
assert probabilities(apply(H, minus)) == (0.0, 1.0)
for gate in (H, X, Y, Z):
    assert isclose(sum(abs(a) ** 2 for a in apply(gate, plus)), 1.0)
print("Checks passed: normalization and a hidden phase revealed by H")
