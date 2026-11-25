"""Toy affine mitigation: held-out scoring and a transparent shot ledger."""
from math import isclose, sqrt

# Known synthetic noise channel; exact targets are available in this toy only.
noisy = lambda ideal: .8 * ideal + .05
training_ideal = [-1, -.5, 0, .5, 1]
training = [(noisy(x), x) for x in training_ideal]
xbar = sum(x for x, _ in training) / len(training)
ybar = sum(y for _, y in training) / len(training)
slope = sum((x-xbar)*(y-ybar) for x, y in training) / sum(
    (x-xbar)**2 for x, _ in training)
intercept = ybar - slope*xbar
held_out = [-.8, -.2, .4, .9]
raw_mae = sum(abs(noisy(x)-x) for x in held_out) / len(held_out)
fixed_mae = sum(abs(slope*noisy(x)+intercept-x)
                for x in held_out) / len(held_out)
assert set(held_out).isdisjoint(training_ideal)
assert isclose(slope, 1.25) and isclose(intercept, -.0625)
assert fixed_mae < 1e-12
# Two-point linear ZNE: estimate = 1.5*E(scale=1) - .5*E(scale=3).
# Independent +/-1 outcomes with worst-case variance 1, equal total shots.
shots = 12000
zne_sd_bound = sqrt((1.5**2 + .5**2) / (shots/2))
raw_sd_bound = sqrt(1/shots)
print(f"Learned map: ideal = {slope:.4f}*noisy {intercept:+.4f}")
print(f"Held-out MAE: raw={raw_mae:.4f}, corrected={fixed_mae:.4f}")
print(f"Worst-case SD bounds: raw={raw_sd_bound:.4f}, ZNE={zne_sd_bound:.4f}")
for runs in (10, 1000):
    training_shots = 300 * shots
    print(f"{runs} later circuits: ML ledger={training_shots+runs*shots:,} shots; "
          f"no-training ledger={runs*shots:,} shots")
