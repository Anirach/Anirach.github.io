# Working Philosophies — series design

**Date:** 2026-09-08 · **Status:** built in the working tree, uncommitted, awaiting the author's read
**Brief (owner):** ten Thoughts essays on working philosophies — useful to the worker, help them out
of bad situations, manage thought through tough work, keep morale and a good moral compass.

## 1. Shape

One working week, Monday to Friday, two essays a day, in reading order. The week is the unit a
person can actually do well, and it rhymes with the Thoughts page's other series, which is one day.

| Day | Theme | Essays |
|---|---|---|
| Monday | arriving | #1 Where You Stand — a bad day, a bad season, a bad place; the three-column notebook · #2 Whose Weather — the organisation's weather vs your load; the three rings |
| Tuesday | the heavy work | #3 One Brick — the task loop vs the thought loop; the done list · #4 The Voice in the Corridor — worry vs thinking; the worry appointment; task / weather / dead |
| Wednesday | the middle | #5 Stuck Is a Place — stuck vs slow; the ninety-day experiment; the boring feedback · #6 A Small Fire — three logs; three things that went right; the one person; the protected evening |
| Thursday | the compass | #7 The Line You Do Not Cross — three lines written on a clear day; compounding compromises; saying no without a speech · #8 A Fair Fight — do not become what you fight; the two-column memo; direct, early, short; the fight budget |
| Friday | leaving well | #9 The Door and the Window — signals; the window before the door; three runways and the exit ledger; leaving without burning the bridge · #10 What You Carry Home — what stays on the desk; craft, people, name; what a working life adds up to |

Every essay keeps the Life essays' skeleton: an epigraph (`blockquote.lamps`, a classical source or
the essay's own thesis), four sections, a `.practice` box ("Try this …") and a `.carry` question,
and closes with a link to the Thoughts page. The tools cross-reference each other across the week
(the notebook, the rings, the brick, the appointment, the memo, the ledger) so the series reads as
one method, not ten tips.

## 2. Production

- **Generated** by `scripts/build_series.py --series working` from `scripts/series/working.json`
  and the sheets `.bilingual/work-*.{th,en}.html`. The manifest names `blog/morning-waking.html`
  as its skeleton — the Sunrise reference and the first non-Hermes skeleton the builder has used —
  and supplies the one rule that skeleton lacks (`.post-hero__sub`) through a new manifest key,
  `extra_css`, which `series_css()` appends.
- **Read times** come from `--sync-read-min` (visible Thai characters at the house rate), never
  typed.
- **Covers** are ten new `wp_*` motifs in `scripts/make_cover.py`, on the Life family's navy/deep
  grounds with the gold accent; subjects were chosen not to collide with the Life covers (a tape
  measure rather than a compass, a window beside the door, a ring of stones rather than a candle).
- **Catalog**: `thoughts/index.html` gains a `#series-working` section above the companion band —
  five `.part` blocks with a `.essay-grid--pair` (two cards at the 3-up card width) and weekday
  colours that darken from cloud blue to navy and end on gold. A scratch assembler derives the
  cards from the manifest; re-derive rather than hand-edit.
- **Feed** dates: `gen_feed.py` now dates an uncommitted post today (as `gen_sitemap.py` already
  did), so INV-36 holds before the launch commit as well as after it.

## 3. Wiring touched

`thoughts/index.html` (section, CSS, hero and head copy), `llms.txt` (a Thoughts — Working
Philosophies section), `feed.xml` and `sitemap.xml` (regenerated), `index.html` ("Read the
essays"), `404.html` (Thoughts card copy), `scripts/covers.tsv` (+10 rows), CLAUDE.md, README and
the four project skills' counts (103 posts; 73 series-nav posts).
