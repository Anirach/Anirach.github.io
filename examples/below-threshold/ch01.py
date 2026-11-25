"""Illustrative independent-opportunity error budget; not a device model."""
from math import expm1, isclose, log1p


def any_failure(per_operation, operations):
    if not 0 <= per_operation < 1 or operations < 0:
        raise ValueError("Use 0 <= p < 1 and a nonnegative operation count")
    return -expm1(operations * log1p(-per_operation))


scenarios = [
    ("baseline", 0.001, 1000),
    ("halve physical error", 0.0005, 1000),
    ("halve operation count", 0.001, 500),
    ("hypothetical logical layer", 0.00001, 1000),
]
for label, p, count in scenarios:
    print(f"{label:26s} p={p:.5f} N={count:4d} P(any)={any_failure(p, count):.6f}")

assert any_failure(0, 1000) == 0
assert any_failure(0.001, 0) == 0
assert isclose(any_failure(0.1, 2), 0.19)
assert any_failure(0.001, 500) < any_failure(0.001, 1000)
assert any_failure(0.0005, 1000) < any_failure(0.001, 1000)
print("Checks passed: zero-risk cases and monotonic improvements")
