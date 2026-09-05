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

## 2026-09-05 — three checks added for the AI Transformation launch

Checks 58 → 61. All three landed green on the tree as it stood, which is the point: they were
written to close surfaces nothing was watching, not to paper over a failure.

**INV-03c — non-SERIES7 strip consistency (FAIL).** The `.series-nav` content checks
(INV-03/03b/20) iterate the hardcoded `SERIES7` list, so the Hermes (10 chips), Life (9) and now
AI Transformation (20) strips had **no content check at all** — and each is duplicated by hand into
every member of its series. The new check needs no table: it groups posts by their strip's `<h3>`,
substitutes each post's own href for its current chip, and requires the members' chip sequences to
be identical. That single comparison proves both "same strip everywhere" and "each marks itself".
A closure pass then requires every chip to target a member of that same strip.

Fault-injected before being trusted, on Hermes:

| Injection | Result |
|---|---|
| one chip label mistyped in one file (`#4 Security` → `#4 Secrity`) | `hermes-memory.html\|shape` names the file, the strip, the chip index and both values |
| a chip re-pointed at `/blog/openclaw-101` in all 10 files | `\|shape` on the self-marked post **and** `\|closure` — INV-09 stays silent because the target file exists, which is exactly the gap |
| clean tree | silent; Hermes 10/10 and Life 9/9 agree |

**INV-03d — parser self-check (FAIL).** `_parse_navs` now finds the strip with a div-depth walk
(`series_nav_body`) instead of `RE_SNAV`'s first `</div></div>`. The self-check's fourth probe is
the one that matters, and the first draft of it asserted something **false**: it claimed the old
regex could not parse a grouped strip. It can. With chips as direct children of each group — the
shape actually shipped — the first `</div></div>` is group-4 plus `.series-links`, i.e. the true
end, and the old regex returns all 20 chips. The probe was rewritten to wrap the chips one level
deeper, which is what a future "let me just wrap the chips" edit would produce:

```
shipped grouped  old RE_SNAV=20   depth walker=20
nested chips     old RE_SNAV= 5   depth walker=20
```

The check now fails if the old regex ever parses the nested probe too, so it cannot go vacuous
without saying so. **Read this before "simplifying" the walker back to a regex:** the depth walk is
defence in depth for the shipped markup, not a hard requirement of it.

**INV-02f — `.blog-jump` chips (FAIL).** The jump strip on `blog/index.html` is not a card, not a
counter and not a nav pattern, so every existing check looked straight past it; the Life launch
forgot its chip twice (`dae4304`). The check now requires each chip to anchor a real
`series-section`, its trailing `· N` to equal that section's card count, and each section to have
exactly one chip. Tests: change a count → fires; delete a chip → fires; clean → silent.
