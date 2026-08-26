# Drift budget — the warn-level backlog

Open this when the user wants to pay down cosmetic inconsistency, or when you need to know whether a
warn-level violation is pre-existing. **None is, today.** Every count below was computed from the
tree; re-verify with the quoted command before repeating a number.

Baseline shape (2026-08-26, `21d5cfc`): 37 posts in `blog/`, 38 HTML files in `blog/`, 47
repo-wide — `index.html` plus five section directories (`books/` split into `publications/`
(academic) + `books/` (fiction) on 2026-08-23, and `books/` now carries four per-book detail
pages beside its index, plus two downloadable PDFs). Nav partition: 7 `.series-nav` + 24 `.post-nav`
+ 6 no-nav. The linter runs 58 checks (39 fail / 17 warn / 2 info) and reports
`checks run 58 / clean 58 / known baseline 0 / violations 0 new, 0 known`. `BASELINE` in
`check_site.py` is an empty table holding only retirement comments — **the tree is clean, and any
violation of any severity is new.**

**If you ever add a baseline key, delete it from `BASELINE` in `check_site.py` in the same commit
you pay it down.** INV-25 fails the build on any baseline key that no longer matches a live
violation, because a dead key silently absorbs the next occurrence of the same defect. This file is
the human-readable half of that table; keep the two in step. (INV-25 passes on the empty table.)

## The pattern behind almost all of it

The 7 OpenClaw series posts (`openclaw-101`, `-agent-teams`, `-memory`, `-security`, `-integrations`,
`-skills`, `-production`) were the un-templated corner of the site. They hand-rolled their own header,
their own footer, their own ordinal badge, and their own site nav — and they supplied 5 of the 6
missing meta descriptions (INV-14), all 4 ordinal-badge markup variants (INV-20b), the one drifted
series heading (INV-03b), all 14 broken internal links (INV-05) and 7 of the 10 posts with no
`:root` (INV-22). All of that is paid; see "Already paid" below.

The second pattern was two OpenClaw-section posts wearing DevOps-chain chrome
(`claude-code-architecture`, `openclaw-memory-architecture`): one graft accounted for 13 of the last
29 known violations across seven checks (INV-04a/04c/04d/04f/04h/10/17). Also paid.

## Inventory

Empty. There is no standing drift: every check in the linter returns clean on its own, with no
baseline entry, so the next violation of any kind fails the build as new. Do not re-create this
inventory from memory — run `check_site.py` and read what it prints.

Header variants (informational, no INV id) are gone too: all 37 posts carry `<nav class="blog-nav">`
with the `href="./"` back link.

## Suggested order to pay it down

Nothing to pay down. If a future commit re-introduces a warn-level cohort, fix it in a dedicated
commit rather than baselining it — see site-check SKILL.md, "Never baseline your way to green".

Already paid — each one's BASELINE key is gone, do not resurrect them:

- **INV-05** (14 broken links, `b9fb125`), **INV-02a/02c** (counters, same commit),
  **INV-12** (dead hamburger on `blog/index.html`, Task 9), **INV-22 / INV-22b** (`:root`, `6670480`, 2026-08-10).
- **INV-06a** (9 orphan images deleted, 2026-08-26), **INV-07a** (two borrowed covers replaced by
  dedicated drawn art, 2026-08-26), **INV-11** (`deployment-hosting.html`'s second `<h1>`, 2026-08-26
  metadata sweep), **INV-14** (6 meta descriptions, same sweep), **INV-15** (copyright unified on one
  string and one encoding, 2026-08-26), **INV-20b** (ordinal badge converged on `.post-hero__tag`,
  Phase 3, 2026-08-26), **INV-21 / INV-21b** (retired with `script.js`, 2026-08-26).
- **INV-03b** and **INV-20c** (one string each in the series posts, `01332eb`, 2026-08-26).
- **INV-04d / INV-04f / INV-04h / INV-17** and part of INV-04a/04c/10 (the two grafted OpenClaw posts
  lost their DevOps-style `.post-nav` blocks and joined `NO_NAV_POSTS`, `f5e53fb`, 2026-08-26).
- **INV-04a** (`24564b0`, 2026-08-26). The last key was `cicd-pipeline.prev → git-branching`, which
  the docs called "chain head has no nav by design". That claim was wrong: the file carried a
  hand-rolled, inline-styled Next link no linter could see. It now has the house `.post-nav`
  (prev `"./"`, next `cicd-pipeline`); `CHAIN_HEAD` is deleted and `CHAIN_TERMINAL_PREV = "./"` sits
  beside `CHAIN_TERMINAL_NEXT`.
- **INV-04c** (last two `<nav class="post-nav">` became `<div>` — 24 files use `div`, 0 use `nav`;
  the linter still matches `<(div|nav)\s+class="post-nav">` on purpose) and **INV-16** (last three
  `post-footer` became `blog-footer`, 37/37), `08cfd95`, 2026-08-26.
- **INV-10** (8 stale `.post-nav__title` labels → 0; `verify-wiring.py` agrees at 0 warn), `73032cb`, 2026-08-26.
- **INV-05b** retired outright (`21d5cfc`, 2026-08-26): its whole domain was illustrative paths inside
  `<pre>`/`<code>`, so it was deleted rather than narrowed. Checks 59 → 58.
