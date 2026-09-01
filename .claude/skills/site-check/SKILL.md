---
name: site-check
description: Runs the cross-file integrity linter for the anirach.com static site (46 self-contained posts in blog/, no build step, no tests, no CI) and explains how to repair every failure it reports. This repo has zero tooling — this skill IS the test suite. Use it before any push, and immediately after ANY edit under blog/, images/, index.html, style.css, or script.js — every page carries its own copy of the nav, the CSS and the counters, so even a one-line edit silently desynchronises blog/index.html card counts, the post-nav prev/next chain, the 7-entry OpenClaw series strip, or a cover image. Also use it when adding or renaming a blog post, when the user says "check the site", "did I break anything", "is the blog consistent", "verify before deploy", "run the tests", or when reviewing a diff that touches blog/index.html. Run it BEFORE the edit too, to confirm the tree is green (0 new, 0 known since 2026-08-26), so any violation the run after your edit reports is yours.
---

# site-check — the site's only test suite

`/Users/anirach/Documents/Anirach.github.io` has no package manager, no build step, no CI, and no
tests. Every file in `blog/` is self-contained: its own `<style>` block, its own copy of the nav
markup, its own footer. There are no shared partials, so a "global" change means editing N files by
hand, and nothing tells you when file 23 of 37 got missed. The bundled script is what tells you.

## Run it

```bash
cd /Users/anirach/Documents/Anirach.github.io
python3 .claude/skills/site-check/scripts/check_site.py
```

Stdlib-only Python 3, no dependencies — matching the repo's no-build-system constraint. Each check
prints one line, `[STATUS ] INV-id  count  title`, where STATUS is PASS (0 violations), KNOWN
(violations, all matching the built-in baseline), or FAIL / WARN / INFO (at least one violation
outside the baseline, at that check's severity). Non-zero checks then print a detail block: new
violations marked ✗, baselined ones marked `· [known]`. A SUMMARY block closes the report.

Exit 0 = no fail-severity violation outside the hard-coded BASELINE in check_site.py (find it with
`grep -n 'BASELINE = {'`). Exit 1 = at least one fail-severity violation whose key is not in that
baseline. Exit 2 = usage or environment error (bad `--root`, unknown `--check` id, bad flag). Warn-
and info-level checks print but never change the exit code, and neither would fail-level violations
that match a baseline key — but **the table is empty today** (2026-08-26, `21d5cfc`): it holds only
retirement comments, so every violation of any severity is new, and every fail-severity one exits 1.

A baseline entry is a promise, not a mute button. When you repair baselined debt, delete its key in
the same commit: **INV-25 audits the whole table and fails if any key has stopped matching a live
violation.** That check exists because INV-22's 10 keys and INV-22b's 1 key outlived their debt by
19 commits and were caught laundering a freshly injected `:root` regression as [known].

Flags: `--root PATH` (default: walk up from cwd, then from the script's own directory),
`--check INV-05` (repeatable, run a subset), `--quiet` (status lines and summary only, no detail),
`--list` (ids + severities, then exit 0), `--color auto|always|never`, `--fix`. For baseline
diffing use `--quiet`. `--fix` always repairs the counters regardless of any `--check` narrowing;
it is the only flag that writes.

```bash
# Only counter checks (INV-02a/b/c) can be auto-repaired:
python3 .claude/skills/site-check/scripts/check_site.py --fix
```

`--fix` recomputes all four counter sites in `blog/index.html` — the two `.blog-hero__stat` values
(Series, Articles) and both `.series-count` spans (`#series-openclaw`, `#series-devops`) — from the
actual `class="card"` counts, and rewrites only the ones that are wrong (**0 of 4 today**: 37 cards,
2 series-sections, 13 + 24). It reports the already-correct ones as `ok … (already correct)`. It is
idempotent and touches no other file. Nothing else is auto-fixable — every other failure needs a
judgement call about which of two files is wrong. Line numbers are deliberately not quoted here;
`blog/index.html` is edited often and `--fix` prints the current ones.

**Run it twice around every edit.** Confirm it is green before you touch anything, then compare.
The tree exits 0 today **and is violation-free** (see below), so the script passing IS the signal;
any violation it reports, at any severity, is new and is yours. The old blind spot — cohort-keyed
checks (INV-15's copyright year, INV-16's footer class) letting a post move between two
already-baselined cohorts without flipping the exit code — is gone with the baseline: with one
cohort on disk, a second cohort is reported as new. Warn- and info-level violations still do not
change the exit code, so read the per-check status lines, not just the exit status.

## Expected `[known]` on today's tree — none

A clean checkout **exits 0 with 0 violations**: `checks run 58 / clean 58 / known baseline 0 /
violations 0 new, 0 known`. Verified 2026-08-26 at `21d5cfc` — 47 HTML files, 37 posts, `books/`
holding four detail pages; 58 checks, 39 fail / 17 warn / 2 info. `BASELINE = {}` holds only
retirement comments. There is no table of expected debt to compare against any more: **any
violation the script prints is new**, and any fail-severity one blocks the push.

The last 29 baselined violations were paid down honestly in seven commits on 2026-08-26
(`01332eb` → `21d5cfc`; read those messages for the per-check story). Retired, in order: INV-03b
and INV-20c (one string each), INV-04d / INV-04f / INV-04h / INV-17 and part of INV-04a / INV-04c /
INV-10 (two OpenClaw posts stopped wearing DevOps-chain chrome), the rest of INV-04a (the chain head
gained a real nav — see INV-04a below), the rest of INV-04c and INV-16 (last `<nav>` containers and
`post-footer` footers normalised), the rest of INV-10 (five labels rewritten), and INV-05b (the
check itself deleted, not narrowed — its whole domain was illustrative text). Before them, the
2026-08-26 redesign phases had already retired INV-06a, INV-07a, INV-11, INV-14, INV-15 and INV-20b,
and earlier commits INV-02a / INV-02c / INV-05 (`b9fb125`), INV-12 (Task 9) and INV-22 / INV-22b
(`6670480`). Every one of those baseline entries has been deleted, so a recurrence of any of them
is reported as new — do not re-report them as debt, and do not re-add a key to absorb one.

If you ever add a baseline entry, it is a separate, deliberate commit with the debt described in a
comment — never bundled into an unrelated edit — and it is deleted the moment the debt is paid, or
INV-25 will fail.

---

## Fail-level checks

### INV-01a/b/c — link closure between `blog/index.html` and `blog/`

- **01a** every `blog/*.html` except `index.html` is linked from `blog/index.html`
- **01b** every card href resolves to a real file
- **01c** no post is carded twice

**Failure means** you created a post and forgot the index card (01a), renamed/deleted a file without
updating its card (01b), or pasted a card block and forgot to change the href (01c). An orphaned
post is unreachable — the site has no search and no tag pages, `blog/index.html` is the only way in.

**Repair:** add or correct the card in the right `<section class="series-section">`. Card anchors
are matched as `<a href="…" class="card">` — whitespace-tolerant, but the attribute order (`href`
before `class`) is load-bearing; keep that shape or the linter (and the counters) will miss it.
Then re-run with `--fix` to resync counts.

### INV-02a/b/c — the counters in `blog/index.html`

- **02a** `<span class="blog-hero__stat"><strong>N</strong> Articles</span>` == total `class="card"`
- **02b** `<strong>N</strong> Series` == number of `<section class="series-section">`
- **02c** each `<span class="series-count">N articles</span>` == cards inside its own section

**Failure means** somebody hand-incremented. That is exactly how 33 drifted from 37.

**Repair:** run `--fix`, or edit `blog/index.html:221` and `:235`. Never bump a counter by hand when
adding a post — recompute:

```bash
grep -c 'class="card"' blog/index.html
```

### INV-03 — the 7-entry OpenClaw series strip

Each of the 7 numbered posts (`openclaw-101`, `-agent-teams`, `-memory`, `-security`,
`-integrations`, `-skills`, `-production`) must carry exactly one `<div class="series-nav">` holding
7 entries in the canonical order, 6 `<a>` + 1 `<span class="current">`, and `current` must be the
host file's own entry.

**Failure means** you edited the strip in one file and not the other six, or you copied a post to
make a new one and left the wrong entry marked `current` (so the page links to itself and orphans a
sibling).

**Repair:** copy `assets/series-nav.html` into the file and swap exactly one `<a href="/blog/X">`
for `<span class="current">`. The strip is a fixed literal duplicated 7×, so adding an 8th post
means editing all 7 existing files plus the new one. See `references/adding-a-post.md`.

### INV-04a — prev/next symmetry (`A.next == B` ⟺ `B.prev == A`)

The DevOps posts form one 24-node path. **0 today, and no baseline entry remains** — the chain
verifies end to end, head included. Two edges were baselined until 2026-08-26:

1. `cicd-pipeline.prev → git-branching.html`, which this file described as the chain head having
   "no nav by design" and therefore unable to reciprocate. **That claim was wrong.** The file
   carried a hand-rolled, inline-styled "Next →" anchor to `cicd-pipeline` with no `.post-nav`
   classes — a link no linter could see and that would have gone stale silently. `24564b0` gave
   `git-branching` the house `.post-nav`: `prev → "./"` ("Back to all posts", newly authored to
   mirror the tail's `next → "./"`) and `next → cicd-pipeline.html`. The script now has
   `CHAIN_TERMINAL_PREV = "./"` beside `CHAIN_TERMINAL_NEXT = "./"`, `CHAIN_HEAD` is deleted, and
   every head exemption is gone from INV-04a, INV-04e and INV-04h.
2. `openclaw-memory-architecture.prev → deployment-hosting.html`, an OpenClaw-section post grafted
   onto the DevOps chain. `f5e53fb` deleted that `.post-nav` block; the post is standalone now.

**Repair:** fix the *pair*, never one side. If you change `A.next`, change `B.prev` in the same
edit. For a new post, do not hand-author order — derive it (INV-04e).

### INV-04b — every `.post-nav` block has exactly 2 `.post-nav__link`

**Failure means** a half-copied nav. A post with one link is a dead end for readers going the other
way.

**Repair:** add the missing side. Note the anchor is **not** always plain —
`class="post-nav__link" style="text-align:right;"` appears in `blog/cicd-pipeline.html`,
`blog/frontend-performance.html`, `blog/web-architecture.html`. That is legal; don't strip it.

### INV-04e — chain order == `reversed(#series-devops card order)`

This is the repo's hidden source of truth: reversing the 24 card hrefs inside
`<section class="series-section" id="series-devops">` reproduces the prev/next chain **byte for
byte**. `blog/index.html` is therefore canonical and the per-post navs are derived data.

**Failure means** the index and the navs disagree about reading order. Trust the index; rewrite the
navs.

**Repair:** see `references/adding-a-post.md` — insert the new card at the **top** of
`#series-devops`, then rewire only three things: `newpost.prev = old_top`, `old_top.next = newpost`,
`newpost.next = "./"` (moving the `"./"` terminal off the previous tail). The chain terminates
with `"./"` at **both** ends — `CHAIN_TERMINAL_PREV` on the head (`git-branching.prev`) and
`CHAIN_TERMINAL_NEXT` on the tail — and both are the blog index.

### INV-04f — no post is `prev` for more than one other post

**Failure means** a fork in a structure that must be a path. 0 today: until 2026-08-26
`deployment-hosting.html` was claimed by both `vibe-coding-devops-process.html` and
`openclaw-memory-architecture.html`; the latter's grafted nav was deleted (`f5e53fb`).

**Repair:** decide which post really follows it and clear the other, or re-parent the interloper to
a post that has a free slot.

### INV-05 — every internal `href`/`src`/`srcset`/`poster` resolves on disk

**0 today, and no baseline entry remains** — the 14 dead site-absolute links in the hand-rolled
per-post site nav of 6 of the 7 OpenClaw posts were repaired in `b9fb125`, so any recurrence fails
the build. The repaired form is the mapping below; keep using it, and never re-introduce a bare
`/about`-style path. The home page is a single scroll with `#`-anchored sections, plus the five
section directories (`blog/`, `books/`, `news/`, `projects/`, `publications/`).

| never write | write |
|--------|---------|
| `/about`, `../about/` | `../index.html#about` |
| `/projects` (as a home anchor) | `../index.html#projects` |
| `/research` | `../index.html#research` |
| `/contact` | `../index.html#contact` |
| `/teaching` | `../index.html#research` (no `#teaching` section exists — verify with `grep -n 'id="' index.html` before writing it) |

**INV-05b is retired** (2026-08-26, `21d5cfc`, 59 → 58 checks). It reported unresolvable paths
inside `<pre>`/`<code>` at info level, and its entire possible output was illustrative text — four
teaching samples in `blog/frontend-performance.html` that must not be edited — yet it had to be
baselined as a count INV-25 audited, so editing that code sample would have failed the build as an
"overcount". A check with no defect domain was deleted, not narrowed; `_scan_links` documents what
is skipped and why. The same commit fixed a blind spot in INV-05 itself: a Phase-5 CSS comment
reading "440 `<pre>` blocks" in every post opened a fake code span that hid 111 real `<head>`
attributes from the link check. `code_spans()` now blanks `<style>`, `<script>` and comments first,
and the comment reads "440 pre blocks".

### INV-06b — every referenced image exists in `images/`

**Failure means** a broken `<img>`. **Repair:** add the asset or repoint the reference. Diagrams in
this repo are **PNGs in `images/`** — inline HTML/CSS and ASCII-art diagrams were tried and
abandoned because they kept breaking layout (commits `f4f7e1b`, `4fc85af`, `c270892`, `4ae2660`).
Do not "fix" a missing diagram by inlining markup; regenerate the PNG.

### INV-07a/b/c — cover images

- **07b** (currently green, the strongest cover rule) a post's own cover == the cover its card uses
  in `blog/index.html`. Covers are read from both `src="../images/…"` and `url('../images/…')` —
  `blog/openclaw-production.html:84` is the only post using a CSS background.
- **07c** (green) every post embeds a cover.
- **07a** (green, no baseline entry remains) no cover is shared by two posts. Two were, until the
  drawn-cover system of 2026-08-26 (`scripts/make_cover.py`, INV-35) gave `vibe-coding-devops-process`
  and `openclaw-memory-architecture` their own art instead of `github-actions`' and `monitoring`'s.

**Repair for 07a:** add a `covers.tsv` row and draw the missing cover. Do **not** silently re-point
one card to a different existing image — that produces a card whose picture contradicts the article.

**Do not enforce `<slug>-cover.*`.** Only 23 of 37 posts follow that pattern; 14 deliberately use
short names (`iac-cover.jpg`, `auth-cover.jpg`, `sre-cover.jpg`, `cicd-cover.png`, `linux-cli-cover.jpg`
…). A literal slug rule produces 14 false positives. The enforceable form is INV-07d below.

### INV-07d — if `images/<slug>-cover.*` exists, the post must use it

0 violations today; a violation means a post ignores its own correctly-named asset. **Repair:**
repoint the post.

### INV-08 — nav-pattern exclusivity

The partition is exact: **7** `.series-nav` + **24** `.post-nav` + **6** no-nav = 37 (since
2026-08-26 — `git-branching` joined the `.post-nav` set, `claude-code-architecture` and
`openclaw-memory-architecture` left it). No file may carry two patterns.

**Failure means** you pasted a chip strip into a DevOps post or a prev/next pair into a series post.
**Repair:** delete the wrong one. Which pattern a post gets is decided by which section its card
lives in, not by taste.

### INV-09 — extensionless `/blog/<slug>` links resolve

42 such hrefs across the 7 series posts; each must exist once `.html` is appended. GitHub Pages
serves them, but only if the file is really there.

**Repair:** if a slug 404s, the file was renamed — update all 7 copies of the strip, not one.

### INV-11 — exactly one `<h1>` per post

0 today, no baseline entry remains. `blog/deployment-hosting.html` had two until the 2026-08-26
metadata sweep deleted the near-duplicate inside the article body. **Repair:** delete the body one,
keep `.post-hero__title`.

### INV-12 — every menu-toggle control is actually wired

0 today. The site ships **two** legitimate mobile-menu patterns and the check knows both:

- **JS-driven** — `index.html:32` `<button class="nav__hamburger" id="hamburger">`, wired by
  `script.js`. A page carrying this shape must contain a `<script>` tag.
- **Pure CSS** — `<input type="checkbox" id="navToggle" class="nav__toggle">` +
  `<label for="navToggle" class="nav__burger">` on `blog/index.html` and the eight sibling
  section pages (the four other section indexes plus the four `books/` detail pages), which load
  no JS at all. Both halves must be present, and the `for=` must name the
  checkbox's `id`, or the tap does nothing.

The check used to grep the literal string `hamburger`. After Task 9 converted four pages to the
checkbox pattern, that string survived in `index.html` alone, so the check policed **1 page out of
42** and could not see the four pages most likely to regress. It now walks the rendered markup
(`<style>`/`<script>`/`<pre>`/`<code>` blanked first, so CSS rules that merely *name* `.nav__burger`
and example markup in code samples are not mistaken for controls) and reports: a JS-driven toggle on
a JS-less page, a menu `<label>` with no `for=`, a `<label for=X>` with no checkbox `X`, and a menu
checkbox no label points at.

**Repair:** finish whichever pattern the page started. Do not "fix" it by deleting the control and
leaving `.nav__links { display: none; }` in the mobile media query — that leaves the page with no
navigation at all on a phone.

### INV-19 — the 7 numbered OpenClaw posts all live in `#series-openclaw`

0 today. A violation means a numbered series post was carded into the wrong section.

### INV-20a — the OpenClaw ordinal badge number == series-nav position

0 today; values 1–7 all correct. Only the badge *markup and wording* drift is warn-level
(INV-20b/20c below); a wrong number blocks the push.

### INV-21 — every DOM hook `script.js` uses exists in `index.html`

**Retired 2026-08-26 with INV-21b** (`bb9c7dc`, Phase 7): `script.js` was deleted and the site is
zero-JavaScript, so both checks policed a contract with a file that no longer exists; **INV-38**
(no page loads executable JavaScript) replaced them. The record below is what they did while alive.

7 selectors were harvested: `#nav`, `#hamburger`, `#navLinks`, `a`, `[data-reveal]` ×2,
`a[href^="#"]`. `index.html` carries 12 `data-reveal` attributes and is the only file in the repo
that carries any. (`.hero__bg-text` was the 8th until 2026-08-26, when the hero watermark was
deleted — INV-21 caught the orphaned parallax listener left behind in `script.js`, which is
precisely the failure it exists to catch.)

**INV-21b (info-level)** asks the paired question: does every page holding a `data-reveal` hook load
the JavaScript that acts on it? `style.css` ships `[data-reveal] { opacity: 0 }` and `script.js`
adds `.revealed`, so a page with the hook and no script does not merely lose an animation — it
renders that content **invisible**. It used to skip `index.html`, which is the only file containing
the hook, so its domain was guaranteed empty; it now covers every page. Adding `data-reveal` to a
`blog/` page is still a no-op (no blog page loads JS) and the check will say so.

### INV-23 — the nav-bearing pages all link to every destination

0 today. `index.html`, `blog/index.html` and every discovered section index — six pages now that
`publications/` exists — each carry their own
hand-copied `<nav>`; every one must link to home, `#contact`, and all five section directories
(the check's title still says "5 destinations" from when home + four directories was the whole
list — the destination set is discovered, so `publications/` joined it automatically), and
every relative href inside that `<nav>` must resolve on disk.

The page list is **discovered, not hardcoded**: any non-hidden top-level directory that ships an
`index.html` is a section of the site (`blog/` is handled separately; `images/` and `docs/` have no
`index.html` and are skipped for free). Create `talks/index.html` and it is immediately in scope for
this check, the link scan, the image-orphan scan and the lang check — and every existing nav goes red
until it links there. That is the intended behaviour: a section nobody can navigate to is not
shipped.

### INV-25 — the linter audits its own BASELINE

0 today. Every key in `BASELINE` must still match at least one live violation, and a key baselined
for *N* occurrences must still fire *N* times. A key that matches nothing is not documentation, it
is a suppression rule aimed at a violation that no longer exists — the next time that defect
reappears it is absorbed as `[known]` and the build stays green.

This is not theoretical. `INV-22`'s 10 keys and `INV-22b`'s 1 key survived the `:root` sweep
(`6670480`) by 19 commits and four linter-editing tasks; stripping `:root` from two posts produced
two identical fresh violations and only the non-baselined one was reported. INV-25 reports all 11 of
those keys.

**Repair:** delete the dead key and leave a one-line retirement comment in its place (the file
already does this for every key it ever held — INV-03b, INV-04a, INV-04c, INV-04d, INV-04f,
INV-04h, INV-05, INV-05b, INV-06a, INV-07a, INV-10, INV-11, INV-12, INV-14, INV-15, INV-16, INV-17,
INV-20b, INV-20c, INV-22 and INV-22b — the table is nothing but those comments today). Never re-add a key to silence it.

### INV-26 — section-dir detail pages are wired to their index

0 today. Added 2026-08-23 with the books/publications split, when `books/` grew three per-book
detail pages (four since `7daf3a4`) — the mirror of INV-01a/b for the sibling directories. For every discovered section
directory, (a) every non-index `*.html` in it must be linked from that directory's own
`index.html` — an orphan detail page is unreachable, since the section index is the only way in —
and (b) every same-directory `.html` href in that index must resolve to a real file, or the card
404s on the page that advertises it.

The two directions deliberately read different texts. The **orphan** direction reads the
comment-**stripped** index: an href quoted inside an HTML comment is not a link a visitor can
follow, so a detail page whose only mention is commented out is still an orphan. The **dead-link**
direction reads the **raw** text, matching INV-05's policy that comments in this repo never quote
an unresolvable href (`books/index.html` spells wrap-pending attributes in prose for exactly this
reason). Same-directory links are matched by a first-character class that excludes `.` and `/`, so
`../index.html` and absolute URLs never count.

**Failure means** you added a `books/<slug>.html` (or any future section's detail page) without
its card, deleted/renamed a detail page without updating the index, or commented out the only card
that reached it. **Repair:** add or fix the card in the section index — never delete the detail
page to silence the orphan report unless removing the book is the actual intent. `Site.pages`
sweeps every `*.html` in the sibling directories, so detail pages are also covered by INV-05/06/12/13
automatically; INV-26 is the one check that ties them to their index.

---

## Warn-level checks (real drift, never blocks a push)

Surface these; fix them deliberately, not opportunistically. A linter that fails the build on
cosmetics gets switched off. The real split is 39 fail / 17 warn / 2 info across 58 checks —
`--list` prints each check's severity. Every row below reads 0 today; the "repair" column is
what to keep it at 0.

| id | rule | today | repair |
|----|------|-------|--------|
| INV-03b | series-nav `<h3>` identical across the 7 | 0 | All seven say `📚 OpenClaw for Organizations 2026` (`openclaw-integrations` was the outlier until `01332eb`). |
| INV-04c | `.post-nav` container is `<div>` | 0 | All 24 use `<div class="post-nav">`; the last `<nav>` containers went in `08cfd95`. `RE_PNAV_OPEN` still matches `(div\|nav)` on purpose so a `<nav>` regression is reported, not hidden. |
| INV-04d | `.post-nav__dir` ∈ {`← Previous`, `Next →`} | 0 | `claude-code-architecture`'s `Related` / `See also` block was deleted in `f5e53fb` (the post is no-nav now, and lost those two links). |
| INV-06a | every file in `images/` (and the repo root) is referenced | 0 | The 9 template leftovers were deleted 2026-08-26. Confirm with `grep -r` before deleting any future orphan. |
| INV-10 | `.post-nav__title` matches the target's card title | 0 | Copy the card title from `blog/index.html` verbatim, Thai subtitle included (`73032cb` rewrote the last five). `verify-wiring.py` agrees one-for-one. |
| INV-13 | `lang` attrs | 0 | Green: the 6 nav-bearing index pages and the 4 `books/` detail pages are `lang="en"`, all 37 posts `lang="th"`. |
| INV-14 | every post has `<meta name="description">` | 0 | All 47 pages carry one since the 2026-08-26 metadata sweep; INV-27 enforces it at fail level. |
| INV-15 | footer copyright year uniform **in posts** | 0 | One string, one encoding (the literal `©`, never `&copy;`) on every page since 2026-08-26. The script reports one violation per non-modal cohort. |
| INV-16 | footer container class uniform | 0 | 37 of 37 posts open with `<footer class="blog-footer">` (the last three `post-footer` posts converged in `08cfd95`). A second cohort is reported as new. |
| INV-17 | a card's section matches its nav family | 0 | `claude-code-architecture` and `openclaw-memory-architecture` sit in `#series-openclaw` and no longer carry a DevOps `post-nav` (`f5e53fb`). |
| INV-18 | no `#series-devops` card uses the chip strip | 0 | Green. (The mirror rule, INV-19, is fail-level — see above.) |
| INV-20b | ordinal badge uses one consistent markup form | 0 | All seven use one `.post-hero__tag` line since Phase 3 (2026-08-26). |
| INV-20c | badge is worded "Post #N" | 0 | `openclaw-memory` wrote `บทที่ 3` until `01332eb`. |
| INV-22 | every post defines its own `:root` | 0 | Green since `6670480` landed the canonical block (28 tokens since the 2026-08-26 re-key) in all 42 files with embedded CSS, `style.css` included (INV-22b, info-level, is green for the same reason). Baseline entries deleted — a post that loses its `:root` is now reported as new. |
| INV-24 | the 6 nav-bearing pages agree on the footer `©` year and all carry a meta description | 0 | INV-14/15/16 iterate `site.posts` only, so `blog/index.html` and the landing pages sat outside every footer/meta check — which is how a `© 2025` footer survived on `blog/index.html` while the others read 2026. The year is checked for **consistency** (modal year wins), never against a hardcoded literal, so 1 January is not a linter event. |

Full drift inventory with counts and the reason each cohort exists: `references/drift-budget.md`.

## Allowlist — the one thing that looks broken and must stay

Hard-coded in the script as `NO_NAV_POSTS`, with comments. Since 2026-08-26 it is the only
exemption the script carries:

1. **The 6 no-nav posts** — `beyond-plugins.html`, `claude-code-architecture.html`,
   `idle-self-improvement.html`, `obsidian-ai-jarvis.html`, `openclaw-memory-architecture.html`,
   `openclaw-migration.html`. Standalone articles, not series members. INV-08 fails if one of them
   grows a nav, or if any post outside the set has none.

Two entries this section used to carry are gone, and the reasons matter:

- **`git-branching.html`** was listed as the chain head that "has no nav at all" and so could not
  reciprocate `cicd-pipeline.prev` — with an instruction not to invent a nav for it. That was wrong:
  it had a nav, a hand-rolled inline-styled "Next →" no regex could see. It now carries the house
  `.post-nav` (`24564b0`), the chain verifies from head to tail, and it is a DevOps chain member
  like the other 23 — not an exception.
- **`claude-code-architecture.html`** was listed as "off-chain by design" for its `Related` /
  `See also` block. The owner chose to delete the block (`f5e53fb`), which cost the post its only
  links to `openclaw-101` and `web-architecture`; it is now simply a no-nav post.

`openclaw-memory-architecture.html`'s graft onto `deployment-hosting` — formerly a real
INV-04a/04f defect — was deleted in the same commit; it is a no-nav post too.

## Adding or renaming a post

Read `references/adding-a-post.md` before touching `blog/`. It has the exact card block, the
three-edit chain rewiring recipe, and the copy-paste series strip. The one-line summary: copy a
DevOps post that already has `<nav class="blog-nav">` + `.post-nav` as your template — the 7
OpenClaw series posts were the un-templated corner of the site and accounted for most of the
warn-level drift the table above used to carry, before Phase 3 and `01332eb` normalised them.

## If you edit the script

Five regex traps, each of which produced a *wrong pass or a false alarm* in a real audit. A wrong
regex makes the linter lie in the dangerous direction: it reports working chains as broken and
invites "fixes" that destroy real links — or, worse, it silently narrows a check's domain to
nothing and reports PASS forever.

```python
CARD  = r'<a\s+href="([^"]+)"\s+class="card">'
PNAV  = r'<(div|nav)\s+class="post-nav">'                 # BOTH tags: div ×24, nav ×0 — keep both
PLINK = (r'<a\s+href="([^"]+)"\s+class="post-nav__link"[^>]*>\s*'   # [^>]*> is load-bearing
         r'<div class="post-nav__dir">([^<]*)</div>\s*'
         r'<div class="post-nav__title">(.*?)</div>')
ATTR  = r'\b(href|src|srcset|poster)\s*=\s*"([^"]+)"'     # NEVER include content=
CODE  = r'<(pre|code)\b[^>]*>.*?</\1>'                    # exclusion spans for the link checker
INERT = r'<(style|script|pre|code)\b[^>]*>.*?</\1>'       # blank_inert(): markup-shape checks
```

1. `class="post-nav__link">` (no `[^>]*`) drops the 3 Next anchors that carry
   `style="text-align:right;"` and fabricates 3 phantom dead-ends.
2. The container was `<nav class="post-nav">` in 4 files until 2026-08-26; a `div`-only pattern found
   0 links in them. All 24 are `<div>` now, and the pattern deliberately still matches both so a
   returning `<nav>` is reported by INV-04c rather than made invisible to INV-04a/b/e.
3. Non-greedy `<div …>(.*?)</div>` mis-nests, because post-nav blocks contain nested divs — anchor on
   the link pattern, never on the container's closing tag.
4. Scanning `content=` turns every `<meta name="description">` and the viewport tag into a "broken
   path" (90 hits instead of 14). Skipping `<pre>`/`<code>` removes 4 more false positives.
5. Any check that reasons about **markup shape** must run its text through `blank_inert()` first, or
   a CSS rule that merely names a class, or example markup inside a code sample, is counted as a
   real element. `blank_inert` blanks `<style>`/`<script>`/`<pre>`/`<code>` bodies while preserving
   byte offsets, so reported line numbers stay correct.

Title comparison for INV-10 must be `html.unescape(re.sub(r'\s+',' ',t)).strip()`, then emoji-stripped
(`[\U0001F000-\U0001FAFF☀-➿️]`), then `.strip().strip('—-').strip()` — see `norm_title` in
check_site.py (`grep -n 'def norm_title'`). `&amp;` vs `&` alone yields ~14 false positives.

**Three rules that outrank "make the run green":**

1. **Never hardcode a set the filesystem can answer.** `NAV_SIBLING_DIRS = ["books","projects",
   "news"]` meant a future `talks/` was invisible to every check that walks the site;
   `discover_nav_sibling_dirs()` replaced it.
2. **Never narrow a check to a literal that only one file happens to contain.** INV-12's `"hamburger"`
   grep and INV-21b's `if rel == "index.html": continue` both reduced their check's domain to
   (almost) nothing while still printing PASS. Ask "which files can this check *see*?" — if the
   answer is one file, or none, the check is decorative.
3. **Never baseline your way to green.** Add the key only for debt you have inspected and can
   describe in a comment, and delete it the moment it is paid. INV-25 enforces the second half.

Every new or modified check must be proven failable by fault injection **on a copy of the repo**
(`--root /tmp/copy`), never on the real tree. Paste the injected output into the commit or the PR;
"it passes" is not evidence that a check works.

### INV-27 — the social / canonical head block

Added 2026-08-26 with the metadata sweep. Nothing in this repo generates a `<head>`; all 47
enumerated pages carry a hand-copied one, and a wrong canonical or a stale `og:url` is invisible
in a browser — it only shows up in a search result or a LINE preview, where nobody on this project
ever looks. So INV-27 **derives** every value it can and compares the file against the derivation,
never one hand-typed tag against another:

| Facet | Derived from |
|---|---|
| `canonical` + `og:url` | the file's own path — `/blog/<slug>.html`, `/books/<slug>.html`, `/<dir>/`, `/`. Never `/index.html`, never extensionless. |
| `og:image:width` / `:height` | the real pixel size, read out of the JPEG SOF / PNG IHDR marker with `struct`. **Pillow is not a dependency and must never become one.** |
| `og:locale` | the same `blog/`-prefix rule INV-13 uses for `lang=` — `th_TH` on posts, `en_US` on the 10 English pages |
| `og:site_name` | the one constant: `Anirach Mingkhwan` |

It also requires `og:title`, `og:description`, `og:type`, `twitter:card` and a `<meta name="description">`
to be present and non-empty, and `og:image` to resolve to a file that exists.

Two deliberate design choices worth keeping:

- **It reads `content="`, and that does not violate trap #4.** Trap #4 forbids `content=` to the
  *link* scanner (`RE_ATTR`) because a viewport string is not a path. A metadata checker has
  nothing else to read. `RE_ATTR` is untouched; INV-27 owns its own regexes, and both run over
  `blank_inert()` text so a `<code>` sample showing an `og:` tag can neither satisfy nor break a
  real page's block.
- **A page with no social block at all reports ONE violation, not eight.** The fix is a single
  block; eight lines per page would bury the pages that have a block with something *wrong* inside it.

`404.html` is deliberately outside all of this — it is noindex, carries no social block, and is
not enumerated by `site.pages`. Do not "fix" it by adding one.

The same sweep taught **INV-06a** to see `og:image`: share images are referenced only from
`content=`, so without `RE_META_IMG_REF` every one of them reported as an unreferenced orphan.

### INV-34 — every `mailto:` is exempt from Cloudflare email obfuscation

**The edge rewrites your HTML, and no repo grep can see it.** anirach.com sits behind Cloudflare
with Scrape Shield's *Email Address Obfuscation* enabled. The repo ships:

```html
<a href="mailto:anirach.m@fitm.kmutnb.ac.th" …>anirach.m@fitm.kmutnb.ac.th</a>
```

and what Cloudflare actually serves is:

```html
<a href="/cdn-cgi/l/email-protection#a8c9c6c1dac9cbc086…">
  <span class="__cf_email__" data-cfemail="3657585f4457555e18…">[email&#160;protected]</span></a>
<script data-cfasync="false" src="/cdn-cgi/scripts/…/email-decode.min.js"></script>
```

Two things break, and both matter to this site specifically:

1. **A visitor without JavaScript reads the literal string `[email protected]`** — not the address.
   This was found the same day Phase 2 published the site's first email, on a site that had just
   spent Phase 1 removing its no-JS blank.
2. **The injected `<script>` comes from the edge**, so the Phase-7 goal of zero `<script>` sitewide
   is unverifiable by `grep -rl "<script" --include="*.html"`. The repo can be clean while the
   served page is not.

**The fix is pure HTML** — Cloudflare's documented opt-out, which Jekyll passes through untouched:

```html
<!--email_off--><a href="mailto:…" class="contact__pill">…</a><!--email_on-->
```

Wrap the **whole anchor**, not just the `href` — the visible text is rewritten too.

The check cannot reach the edge, so it polices what it can reach: no `mailto:` may ship without an
`<!--email_off-->` opened and not yet closed before it. Fault-injected 2026-08-26 by stripping one
pair, which reproduced the live defect and failed the build.

Alternative fixes that need dashboard access this repo does not have: turning the feature off under
Scrape Shield, or a Configuration Rule scoped to the site. The comment pair is preferred precisely
because it lives in version control next to the thing it protects.

### INV-35 — the drawn cover system is intact

Guards `scripts/make_cover.py` + `scripts/covers.tsv`, which on 2026-08-26 replaced 35 AI clip-art
covers (glowing circuit-brains, dogs in hard hats) with one drawn system in the book-jacket
language. `blog/index.html` went from **4.07 MB → 1.59 MB** of referenced bytes as a side effect.

The spec table is the source of truth — one row per post:

```
slug | out | motif | ground | eyebrow | title | thai | opts
```

Five motifs (`planes` `chain` `nest` `tree` `grid`), four grounds (`navy` `deep` `cloud`
`parchment`). Adding a post means adding a row, never editing the renderer.

INV-35 checks the four things that actually rot, each of which broke at least once while the
system was being built:

| Branch | Why it matters |
|---|---|
| every post has a row | a post added later keeps whatever cover it was born with, and the family gains a silent outlier |
| cover is exactly 800×800 | 74 `<img>` tags hard-code those numbers — a different canvas renders squeezed (INV-33's trap, one level up) |
| share card exists at 1200×630 | `og:image` points at `<slug>-og.jpg`; a missing one is a broken share preview no page visibly shows |
| cover ≤ 90 KB | the whole point was the weight; flat drawn art has no business exceeding it, and one that does is usually a photo that slipped in |

All four were fault-injected before the check was trusted.

**Two rules live in `make_cover.py --check`, not here**, because they are authoring rules rather
than repo invariants:

1. **A cover's ground may never be the same tone as its post's hero.** Sunrise (light) heroes take
   `navy`/`deep` covers; Deep Blue (dark) heroes take `cloud`/`parchment`. The site shipped the
   opposite once — a teal cover on a teal hero, which vanished. The checker reads each post's
   ACTUAL `.post-hero` gradient rather than a second table that could drift.
2. **No two posts may share a motif — one drawing per post, 37 of them.** This replaced a weaker
   "no two ADJACENT cards share ground+motif" rule on 2026-09-01. The weaker rule passed happily
   while five generic motifs were spread over 37 posts, which is exactly how the listing ended up
   with six near-identical grey wireframes; the owner reported it with screenshots. Uniqueness is
   now structural: `MOTIFS` has one named function per slug and `--check` rejects a repeat.

`cream` (#faf7f0) was designed in and then **retired**: cards are `var(--white)`, so a cream cover
had no visible edge and read as a missing image.

A third authoring rule arrived with the 2026-09-01 redesign: **`accent` must be a known key.**
DevOps covers are coloured by TOPIC CLUSTER, not per post — cyan containers, green testing, amber
CI/CD, red security, teal reliability — so a reader learns the code across covers. OpenClaw is
always `violet`. All nine accents are `:root` tokens; no seventh status colour was invented.

Contact sheet for review — writes to `.covers/`, a dot-dir, because the first version wrote to the
repo root and INV-06a correctly reported it as an unreferenced published image:

```bash
python3 scripts/make_cover.py --check      # validate the table, draw nothing
python3 scripts/make_cover.py --all        # 37 covers + 37 share cards, ~2s
python3 scripts/make_cover.py --contact    # .covers/contact-sheet.jpg
```

### INV-36 — every visible date agrees with `feed.xml` and with `article:published_time`

Three places stated when a post was published and, until 2026-08-26, only two were true:

| Source | Was |
|---|---|
| `feed.xml` `<pubDate>` | generated from `git log --diff-filter=A` — correct |
| head `article:published_time` | the same git date — correct |
| **the visible text** | the literal string **"March 2026"** on all 37, hand-typed, month-precision |

The corpus actually spans **7–24 March 2026**. A reader saw one date, a feed reader another, and
"newest" could not be computed from the page at all — which the featured card on `blog/index.html`
now depends on. All three derive from the same git date now. INV-36 fails if any `<time datetime>`
in a post disagrees with that post's own `article:published_time`, if a card's date disagrees with
the feed, or if a card has no `<time>` at all.

Fault-injected on all three branches. **18 posts had no visible date whatsoever** — a byline and a
series label but never a *when*, on a blog — and now do.

### INV-37 — no inline colour inside a post hero fights its own gradient

**A regression this repo shipped**, the same day it consolidated the hero families. Moving 15 posts
from a dark gradient to light Sunrise inverted their ink — but 12 carried

```html
<strong style="color:#fff">Anirach Mingkhwan</strong>
```

*inline* in the hero. An inline style beats any stylesheet, so the sweep could not see it and the
author's name went out white-on-cream: invisible, on twelve live pages.

The rule is about the mechanism, not the shade: **an inline colour in a hero is unreachable by every
sweep this repo runs** — `retoken.py`, `reheroize.py`, and the dark-mode block Phase 8 adds — so it
survives every future palette change too. Light ink on Sunrise fails; dark ink on Deep Blue fails
the same way mirrored. Both branches fault-injected with the exact markup that shipped.

Severity here is per-check rather than per-violation, so a merely *latent* inline colour (one not
currently invisible) is deliberately not reported — see the note in the check body.
