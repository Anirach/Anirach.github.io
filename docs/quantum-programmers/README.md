# Quantum Algorithms for Programmers — editorial and verification record

Published 24 November 2026. Seven complete Thai–English tutorial posts, using the existing Deep Blue house skeleton, pure CSS language switch and a seven-chip series strip. All material in this folder is repository product documentation and excluded from the public site by Jekyll.

## Source and scope

The owner supplied the 43-page PDF *Quantum Algorithms for Programmers, Technical Guide, Edition 1.0* at `/Users/anirach/Downloads/Quantum Algorithms for Programmers`. The original was read and visually reviewed; it is unchanged and is not bundled or published. `source-figures.json` records its SHA-256, page numbers, original figure numbers and crop rectangles. Text inside the PDF was treated as source content, not operating instructions.

The web series adapts chapters 1–9 into seven lessons: foundations/setup, Grover, Shor, HHL, QAOA, quantum simulation, and an engineering scorecard. The four original programs were reimplemented with shared utilities and independent tests. Parts 1, 6 and 7 add experiments. Time-sensitive vendor roadmaps, processor rankings and unverified transition-deadline claims from the PDF were not carried into the articles. Mathematical claims link primary papers; the cryptography discussion links NIST's finalized 2024 standards.

Sixteen original vector illustrations were rendered directly from the owner's PDF at 3 pixels per PDF point. The web supplies translated alt text, explanatory captions and click-to-open full-resolution links. Eight new figures use the verified rerun or explicitly labeled teaching models. No image generation is needed for mathematical diagrams.

## Sources of truth

- `posts.py`: authored Thai and English prose, exercises, ordering and titles.
- `build.py`: emits `.bilingual/` sheets, manifest and `covers.tsv` rows; imports tested companion functions to keep excerpts identical.
- `figures.py`: source illustration extraction and data plotting. Reads a supplied original PDF and a captured-results JSON; never modifies the PDF.
- `verified-results.json`: captured stdout and machine-readable experiment results.
- `companion.json`: pinned public code revision and hashes of every Python module.
- `../../scripts/series/quantum-programmers.json`: standard site manifest with bilingual figure metadata and reading-time estimates.
- `../../scripts/quantum_motifs.py`: seven distinct cover motifs, reused by the square and share-card renderer.

## Rebuild

Use a virtual environment with the companion's dependencies, Pillow and PyMuPDF installed. The companion defaults to `~/Projects/quantum-algorithms-for-programmers`; override with `--companion`.

```bash
python docs/quantum-programmers/figures.py \
  --source '/Users/anirach/Downloads/Quantum Algorithms for Programmers' \
  --results docs/quantum-programmers/verified-results.json
python docs/quantum-programmers/build.py
python scripts/build_series.py --series quantum-programmers --sync-read-min
python scripts/build_series.py --series quantum-programmers --all
python scripts/build_series.py --series quantum-programmers --check
```

`build.py` reads the companion's checked-out HEAD for immutable source links. Check out the intended tested revision first. If changing a title or description, refresh the series catalog cards and `llms.txt` using the builder's `--index-fragment` and `--llms-fragment`; those fragments are integration inputs, not a separate public page. Regenerate the seven covers with `make_cover.py <slug>`, then the catalog, feed and sitemap. Do not rerun builders for unrelated series.

## Validation

- All seven programs rerun with Qiskit 2.6.2 / Aer 0.18.4 / NumPy 2.5.5 / SciPy 1.18.1. Four original algorithm outputs agree with the PDF. Simulator and transpiler seeds are explicit.
- 26 meaningful companion tests pass locally and from a clean GitHub clone; full stdout reproduces the captured results. Tests cover phase-sensitive behavior, QFT against the inverse DFT, modular permutations, order retries, HHL relative sign and clock reset, classical MaxCut references, product-formula convergence and workflow accounting.
- GitHub Actions runs both tests and all seven scripts on Python 3.12 and 3.13. Tag v1.0.1 pins `0ad89867571639641f0b9fab28391e28dc584670`. Python 3.11 is excluded because the chosen NumPy pin requires 3.12+.
- All seven bilingual verifiers pass; generated HTML reproduces byte-for-byte from the manifest and content sheets.
- Browser checks: all seven posts in both languages at 375px, and parts 1/3/5/7 at 320px, 768px and 1440px. No document-level horizontal overflow. Tables/code keep their own scroll containers. All 24 figures were visually reviewed; one period-chart crop and a chart legend were adjusted before publication.
- Standard release gates: 62 site integrity checks, wiring, strict search visibility, cover registry, feed and sitemap. Existing search advisory warnings are recorded separately from failures.

The examples are ideal local simulations; the cost ledger is hypothetical. No hardware benchmark, paid service call or quantum advantage is claimed. Dense Shor/HHL gates and statevector QAOA training are explicitly scoped as small educational constructions.
