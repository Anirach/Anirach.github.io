# Below Threshold chapter tutorials

Ten bilingual Thai/English tutorials, one for each numbered chapter of Anirach
Mingkhwan’s *Below Threshold: AI, Quantum Errors and Better Code*, Edition 1.0
(November 2026). The executive summary, glossary and appendices remain supporting
reading in the book, rather than extra chapter posts.

The series uses the same generated Deep Blue layout, language switch, original
cover system, clickable diagrams and reading-order navigation as the Quantum
Algorithms for Programmers series.

## Source and downloads

The owner supplied `/Users/anirach/Documents/Below-Threshold-Book/dist/Below-Threshold.pdf`
(104 pages, 5,420,043 bytes). Its SHA-256 is
`08f3f4e402d968a31a173dbfe61cd53ff768ecbdefeb86ce43c33ccd8a239f86`.
The public Drive download was fetched without authentication and matched the
supplied PDF byte for byte on 25 November 2026.

Every post and both language tracks link to the owner’s public Drive download:
https://drive.google.com/uc?export=download&id=1iG7oSWLC9UI91VsPOzqcxk3_evH8Sn3b

A separate link opens the Drive reader. Labels explicitly identify the book as
English. The original book files are unchanged. No second copy of the book is
published in this repository.

All 17 diagrams are unchanged PNGs from the owner’s book project. Captions name
their source figures and both tracks have descriptive alt text. `source-figures.json`
records each image hash and the supplied PDF hash. The book’s printed page numbers
are used throughout the tutorials.

## Maintained files

- `chapters-01-03.json`, `chapters-04-06.json`, `chapters-07-10.json`: complete
  bilingual article prose, titles, descriptions, chapter pages and references.
- `build.py`: prepares content sheets, manifest, source-figure records, executed
  example outputs and a deterministic ZIP. Does not execute generated code.
- `scripts/series/below-threshold.json`: generated series metadata and figures.
- `examples/below-threshold/`: ten standard-library Python teaching examples,
  assertions, README and expected outputs.
- `downloads/below-threshold-tutorial-examples.zip`: offline example bundle.
- `scripts/threshold_motifs.py`: ten distinct house-style cover motifs.

## Rebuild

From the website root, with Python and the existing Pillow cover dependencies:

```bash
python3 docs/below-threshold/build.py
python3 scripts/build_series.py --series below-threshold --sync-read-min
python3 scripts/make_cover.py --check
# Draw one named cover per manifest post, then emit the pages:
python3 scripts/make_cover.py below-threshold-overview
python3 scripts/build_series.py --series below-threshold --all
python3 scripts/build_series.py --series below-threshold --check
python3 scripts/build_series.py --series below-threshold --index-fragment
python3 scripts/build_series.py --series below-threshold --llms-fragment
```

The builder uses the local book project to refresh diagrams when available;
otherwise it uses the committed images. All short examples are executed and must
exit successfully. When re-emitting the manifest, re-sync read times before
building pages. Integrate the index and llms fragments once; on later edits replace
the existing section. Then regenerate Tutorials before Thoughts, the feed and the
sitemap, and run the repository’s publication gates.

The short examples were executed for the web series. Full original book labs were
not rerun for this publication. Tables and result plots retain the book’s recorded
scope; small synthetic examples are clearly distinguished from those results.
