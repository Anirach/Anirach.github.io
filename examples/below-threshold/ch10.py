"""Toy release gate: quality, cost, and complete evidence are separate checks."""
baseline = {"failures": 50, "trials": 1000, "seconds": 1.0}
experiments = {
    "accurate but slow": {"failures": 20, "trials": 1000, "seconds": 1.6,
                          "held_out": True, "equivalent": True},
    "candidate": {"failures": 30, "trials": 1000, "seconds": 1.1,
                  "held_out": True, "equivalent": True},
    "training-only": {"failures": 1, "trials": 1000, "seconds": 1.0,
                      "held_out": False, "equivalent": True},
}


def evaluate(run):
    if not run["held_out"] or not run["equivalent"]:
        return "INCOMPLETE EVIDENCE"
    error = run["failures"] / run["trials"]
    reference = baseline["failures"] / baseline["trials"]
    quality_ok = error <= reference * 0.8
    cost_ok = run["seconds"] <= baseline["seconds"] * 1.2
    return "PILOT" if quality_ok and cost_ok else "REVISE"


print("Toy gate: >=20% relative error reduction; <=20% runtime increase")
for name, run in experiments.items():
    print(f"{name}: error={run['failures']/run['trials']:.1%}, "
          f"time={run['seconds']:.1f}s -> {evaluate(run)}")
assert evaluate({**experiments["candidate"], "held_out": False}) == "INCOMPLETE EVIDENCE"
assert evaluate({**experiments["candidate"], "equivalent": False}) == "INCOMPLETE EVIDENCE"
