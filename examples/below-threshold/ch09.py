"""Toy SDD with handwritten functions; no generated source is executed."""
from collections import Counter
from statistics import median


def upper(xs):
    return sorted(xs)[len(xs) // 2]


def correct(xs):
    ys = sorted(xs)
    m = len(ys) // 2
    return ys[m] if len(ys) % 2 else (ys[m - 1] + ys[m]) / 2


candidates = {"A": upper, "B": upper, "C": upper,
              "D": correct, "E": correct, "F": None}
visible = [([3, 1, 2], 2), ([4, 1, 3, 2], 2.5)]
probes = [[9], [1, 2], [2, 8, 4], [7, 1, 9, 3]]
live = [n for n, f in candidates.items() if f is not None]
syndrome = {n: tuple(int(candidates[n](x) != y) for x, y in visible)
            for n in live}
signature = {n: tuple(candidates[n](x) for x in probes) for n in live}


def vote(names):
    if not names:
        return None
    counts = Counter(signature[n] for n in names)
    return max(names, key=lambda n: counts[signature[n]])


def checked_vote(names):
    survivors = [n for n in names if not any(syndrome[n])]
    return vote(survivors) if survivors else None


plain = vote(live)
decoded = checked_vote(live)
for n in candidates:
    print(n, "erasure" if candidates[n] is None else "syndrome=" + str(syndrome[n]))
print(f"plain vote={plain or 'ESCALATE'}; checked vote={decoded or 'ESCALATE'}")
# This held-out oracle scores choices only after selection.
held_out = [[-10, 4, 6, 1000, 10, 20], [-2, 4], [1, 1, 7]]
for name in (plain, decoded):
    if name is None:
        print("ESCALATE: no candidate to score")
        continue
    score = sum(candidates[name](x) == median(x) for x in held_out)
    print(f"{name}: held-out {score}/{len(held_out)}")
assert decoded is None or not any(syndrome[decoded])
assert checked_vote([n for n in live if any(syndrome[n])]) is None
assert vote([]) is None and checked_vote([]) is None
assert correct(held_out[0]) == 8 and upper(held_out[0]) == 10
