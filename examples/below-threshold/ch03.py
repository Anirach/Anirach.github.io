"""Classical repetition code: exact tails, parity decoding and aliasing."""
from math import comb, isclose


def syndrome(bits):
    a, b, c = bits
    return (a ^ b, b ^ c)


def correct(bits):
    result = list(bits)
    location = {(1, 0): 0, (1, 1): 1, (0, 1): 2}.get(syndrome(bits))
    if location is not None:
        result[location] ^= 1
    return tuple(result)


def majority_failure(p, distance):
    if distance < 1 or distance % 2 != 1 or not 0 <= p <= 1:
        raise ValueError("Use odd positive distance and 0 <= p <= 1")
    return sum(comb(distance, k) * p ** k * (1 - p) ** (distance - k)
               for k in range(distance // 2 + 1, distance + 1))


for bit in (0, 1):
    encoded = (bit,) * 3
    for position in range(3):
        noisy = list(encoded)
        noisy[position] ^= 1
        assert correct(noisy) == encoded
print("Single-flip syndrome map: 10 -> first; 11 -> middle; 01 -> last")
for p in (0.1, 0.5, 0.6):
    row = [majority_failure(p, d) for d in (1, 3, 5, 7)]
    print(f"p={p:.1f}: " + " ".join(f"d={d}: {v:.6f}" for d, v in zip((1, 3, 5, 7), row)))

assert isclose(majority_failure(0.1, 3), 0.028)
assert all(isclose(majority_failure(0.5, d), 0.5) for d in (1, 3, 5, 7))
assert syndrome((1, 0, 0)) == syndrome((0, 1, 1))
assert correct((0, 1, 1)) == (1, 1, 1)
print("Alias: errors 100 and 011 share syndrome 10; the assumed single-flip decoder fails on 011")
