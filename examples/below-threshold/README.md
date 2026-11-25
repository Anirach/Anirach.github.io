# Below Threshold: ten tutorial examples

Small, dependency-free Python teaching examples for the ten chapter tutorials at
https://anirach.com/blog/#series-below-threshold.

Download the full English book (104 pages):
https://drive.google.com/uc?export=download&id=1iG7oSWLC9UI91VsPOzqcxk3_evH8Sn3b

Use Python 3.10 or later. Each file is complete and includes assertions:

```bash
python3 ch01.py
```

| File | Concept checked |
| --- | --- |
| `ch01.py` | Independent-opportunity failure budget |
| `ch02.py` | Phase, measurement basis and normalization |
| `ch03.py` | Repetition-code parity, exact tails and ambiguity |
| `ch04.py` | Learned lookup decoding and an information-limited floor |
| `ch05.py` | Held-out affine mitigation and a shot-cost ledger |
| `ch06.py` | Exact three-bit CNOT synthesis and equivalence |
| `ch07.py` | Separate semantic and compilation-budget checks |
| `ch08.py` | A local MaxCut optimum compared with exhaustive search |
| `ch09.py` | Visible checks, erasures and selection before held-out scoring |
| `ch10.py` | Separate quality, cost and evidence gates |

`expected-output.txt` records the deterministic outputs captured on 25 November
2026. Run every example and compare the output with that file. The scripts make
no network requests and do not execute generated source.

These examples explain mechanisms. They do not reproduce the book’s full Stim,
PyMatching, neural-network, mitigation, tensor-train or HumanEval experiments.
The blog articles label those original results as reported in the book and keep
their noise models, data splits, hardware and statistical limits explicit.

Author: Anirach Mingkhwan. Editorial sources and figure provenance are maintained
in `docs/below-threshold/` in the website repository.
