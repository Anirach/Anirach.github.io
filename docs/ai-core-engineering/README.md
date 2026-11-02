# Software Engineering with AI-Core — course maintenance

15 bilingual chapters published 2026-11-02. The course follows the site's house
post design and zero-JavaScript language switch. It adds 15 original chapter
diagrams, one overview diagram, 15 covers, share cards and catalog thumbnails.

The running example is a draft-only issue-to-patch workbench. The companion is
https://github.com/Anirach/ai-core-engineering-workbench, pinned to
`3496e4c5eed84bd78ddbd1ac65a814c105ded719` / tag `v1.0.0`.

## Editorial architecture

- Parts 1–5: mental model, functional boundaries, state contracts, exact inputs,
  Jev response contracts.
- Parts 6–10: skill contracts, semantic inputs, hard permissions, context
  provenance, structural output validation.
- Parts 11–15: independent behavior oracle, separate quality gate, bounded
  recovery, evaluation, release and operation.

Every chapter has a learning outcome, a concrete failure, a diagram, an
implementation excerpt, observed fixture output, a before/after comparison,
a runnable command, a matching test, an exercise and primary references.
Sources were checked 2026-11-02. Fixture agreement is never reported as model
accuracy. No paid live API call was made. Production extensions and the
restricted interpreter's limits are stated in both languages.

## Rebuild

`course.py` retains the editorial source; `build.py` prepares the sheets and
drawings. It currently points at the author's local companion checkout at
`/Users/anirach/Projects/ai-core-engineering-workbench`; adjust that path on a
different machine. It also regenerates learning materials in that checkout,
so inspect the companion diff before committing any regenerated materials.

```sh
python3 docs/ai-core-engineering/build.py
python3 scripts/build_series.py --series ai-engineering --sync-read-min
python3 scripts/build_series.py --series ai-engineering --all
python3 scripts/reindex_blog.py --repo . --out blog/index.html
python3 scripts/gen_feed.py
python3 scripts/gen_sitemap.py
```

The generated posts are the published truth. A prose-only edit does not require
redrawing every cover. Cover specs are in `scripts/covers.tsv`; original motifs
are in `scripts/engineering_motifs.py`. For a changed cover, use
`python3 scripts/make_cover.py <slug>` and regenerate its 144px thumbnail.

## Verified

- All 62 site integrity checks: zero failures, warnings or baseline debt.
- Wiring verifier: 160 posts/cards, 130 series-nav, 24 post-nav, six no-nav.
- Visibility scanner: zero fail-severity findings; standing advisory title and
  heading findings remain in unrelated and existing post metadata.
- Companion: 26 tests and all 15 lessons run from a clean local clone.
- Public GitHub CI: Python 3.11, 3.12 and 3.13 passed for the pinned revision.
- 124 pinned code/test/exercise links resolve in the published companion tree.
- All new chapters switched correctly between TH/EN at 375px with no horizontal
  page overflow. Parts 1, 5, 10 and 15 also checked at 320, 768 and 1440px.
- Browser inspection: first-chapter hero, mobile English hero, catalog spotlight,
  15 numbered cards and Design / Control / Prove groups.
- Diagrams reviewed at source resolution; captions link to full-size PNGs.

`site-check.txt` and `visibility-check.txt` retain the local reports. The feed
generator now preserves the declared publication day when imported draft Git
history has a later first-commit day; three regressions cover that behavior.
The original untracked `docs/screenshots/` folder was left untouched.
