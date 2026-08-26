---
name: site-check
description: Runs the cross-file integrity linter for the anirach.com static site (37 self-contained posts in blog/, no build step, no tests, no CI) and explains how to repair every failure it reports. This repo has zero tooling — this skill IS the test suite. Use it before any push, and immediately after ANY edit under blog/, images/, index.html, style.css, or script.js — every page carries its own copy of the nav, the CSS and the counters, so even a one-line edit silently desynchronises blog/index.html card counts, the post-nav prev/next chain, the 7-entry OpenClaw series strip, or a cover image. Also use it when adding or renaming a blog post, when the user says "check the site", "did I break anything", "is the blog consistent", "verify before deploy", "run the tests", or when reviewing a diff that touches blog/index.html. Run it BEFORE the edit too, to capture the known-red baseline, so you can tell your own breakage apart from the failures that were already there.
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

Exit 0 = no fail-severity violation outside the hard-coded BASELINE in check_site.py:263-377.
Exit 1 = at least one fail-severity violation whose key is not in that baseline. Exit 2 = usage or
environment error (bad `--root`, unknown `--check` id, bad flag). Warn- and info-level checks print
but never change the exit code, and neither do fail-level violations that match a baseline key —
today 6 fail-severity violations (INV-04a 2, INV-04f 1, INV-07a 2, INV-11 1) are reported as
[known] and the script exits 0.

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

**Run it twice around every edit.** Capture the baseline before you touch anything, then compare.
The tree exits 0 today but is not violation-free (see below), so "the script passed" means nothing
on its own; "the script reports a violation that was not in the baseline" means you broke
something. One blind spot remains: cohort-keyed checks (INV-15's copyright year, INV-16's footer
class) report one violation per cohort, so a post moving between two already-known cohorts (e.g.
© 2026 → © 2025) stays [known] and will NOT flip the exit code — read the per-check counts and
details, not just the exit status.

## Expected `[known]` on today's tree — do not panic, do not mass-fix

A clean checkout **exits 0** with **55 violations across 17 checks**, every one of them baselined.
Verified against the One Day of Light tree of 2026-08-24, `7daf3a4` — 47 HTML files, `books/`
now holding four detail pages (50 checks:
31 fail / 15 warn / 4 info — INV-26 and INV-27 both joined at fail level):

| id | sev | count | what |
|----|-----|-------|------|
| INV-03b | warn | 1 | `openclaw-integrations.html` heads its chip strip differently from the other six |
| INV-04a | fail | 2 | one allowlisted chain-head edge (`cicd-pipeline.prev → git-branching`, by design) + one real defect (`openclaw-memory-architecture` grafted onto `deployment-hosting`) |
| INV-04c | warn | 4 | `<nav class="post-nav">` instead of `<div>` in 4 posts |
| INV-04d | warn | 2 | `claude-code-architecture`'s `Related` / `See also` block (allowlisted) |
| INV-04f | fail | 1 | `deployment-hosting` is claimed as `prev` by 2 posts |
| INV-04h | info | 2 | the same 2 posts are unreachable from the chain walk |
| INV-05b | info | 4 | illustrative paths inside `<pre>`/`<code>` in `frontend-performance.html` |
| INV-06a | warn | 9 | orphan images from a prior template |
| INV-07a | fail | 2 | two covers each shared by two posts |
| INV-10 | warn | 8 | stale `.post-nav__title` labels |
| INV-11 | fail | 1 | `blog/deployment-hosting.html` has two `<h1>` (lines **184** and **196**) |
| INV-14 | warn | 6 | posts with no `<meta name="description">` |
| INV-15 | warn | 2 | 25 posts `© 2025`, 8 with no `©` line |
| INV-16 | warn | 4 | four different footer container classes |
| INV-17 | warn | 2 | 2 cards whose section contradicts their nav family |
| INV-20b | warn | 4 | four ordinal-badge markup variants |
| INV-20c | warn | 1 | `openclaw-memory.html` writes `บทที่ 3` |

**Four checks that used to be red are now green — do not re-report them as debt:** INV-02a and
INV-02c (counters, fixed in `b9fb125`), INV-05 (the 14 dead site-absolute links, fixed in the same
commit), INV-12 (`blog/index.html`'s dead hamburger, replaced with the CSS checkbox toggle in Task
9). INV-22/INV-22b likewise: every post now carries the canonical `:root` block (`6670480`). Their
baseline entries have been deleted, so a recurrence of any of them fails the build.

Fixing the baseline is welcome but is a separate, deliberate task — never bundle it into an
unrelated edit, because it makes the diff unreviewable. Whatever you fix, delete its BASELINE key in
the same commit or INV-25 will fail.

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

The DevOps posts form one 24-node path. Two edges are broken today and both are genuine:

1. `blog/cicd-pipeline.html:607` sets `prev → git-branching.html`, but `git-branching.html` has no
   nav at all and cannot reciprocate. `git-branching` is the chain **head**; this is arguably
   working-as-intended and is on the allowlist below.
2. `blog/openclaw-memory-architecture.html:224` sets `prev → deployment-hosting.html`, but
   `deployment-hosting.next = vibe-coding-devops-process.html`. `openclaw-memory-architecture` is an
   OpenClaw-section post grafted onto the DevOps chain. It is the only real defect here.

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
`newpost.next = "./"` (moving the `"./"` terminal off the previous tail).

### INV-04f — no post is `prev` for more than one other post

**Failure means** a fork in a structure that must be a path. Today
`deployment-hosting.html` is claimed by both `vibe-coding-devops-process.html` and
`openclaw-memory-architecture.html`.

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

**INV-05b (never fails the build):** 4 refs inside `<pre>`/`<code>` in
`blog/frontend-performance.html` are illustrative code samples. Leave them alone.

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
- **07a** no cover is shared by two posts — **2 known failures**:
  `github-actions-cover.jpg` (`github-actions.html` + `vibe-coding-devops-process.html`) and
  `monitoring-cover.jpg` (`monitoring-observability.html` + `openclaw-memory-architecture.html`).

**Repair for 07a:** these two posts have no dedicated asset. Generate the missing PNG and point both
the post body and the index card at it. Do **not** silently re-point one card to a different
existing image — that produces a card whose picture contradicts the article.

**Do not enforce `<slug>-cover.*`.** Only 23 of 37 posts follow that pattern; 14 deliberately use
short names (`iac-cover.jpg`, `auth-cover.jpg`, `sre-cover.jpg`, `cicd-cover.png`, `linux-cli-cover.jpg`
…). A literal slug rule produces 14 false positives. The enforceable form is INV-07d below.

### INV-07d — if `images/<slug>-cover.*` exists, the post must use it

0 violations today; a violation means a post ignores its own correctly-named asset. **Repair:**
repoint the post.

### INV-08 — nav-pattern exclusivity

The partition is exact: **7** `.series-nav` + **25** `.post-nav` + **5** no-nav = 37. No file may
carry two patterns.

**Failure means** you pasted a chip strip into a DevOps post or a prev/next pair into a series post.
**Repair:** delete the wrong one. Which pattern a post gets is decided by which section its card
lives in, not by taste.

### INV-09 — extensionless `/blog/<slug>` links resolve

42 such hrefs across the 7 series posts; each must exist once `.html` is appended. GitHub Pages
serves them, but only if the file is really there.

**Repair:** if a slug 404s, the file was renamed — update all 7 copies of the strip, not one.

### INV-11 — exactly one `<h1>` per post

`blog/deployment-hosting.html` has two: `:184` the hero title, `:196` a near-duplicate inside the
article body. **Repair:** delete the body one (`:196`), keep `.post-hero__title`.

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

0 today. 7 selectors harvested: `#nav`, `#hamburger`, `#navLinks`, `a`, `[data-reveal]` ×2,
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
already does this for INV-05, INV-12, INV-22 and INV-22b). Never re-add a key to silence it.

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
cosmetics gets switched off. The real split is 31 fail / 15 warn / 4 info across 50 checks —
`--list` prints each check's severity.

| id | rule | today | repair |
|----|------|-------|--------|
| INV-03b | series-nav `<h3>` identical across the 7 | 1 | `blog/openclaw-integrations.html` says `OpenClaw for Organizations 2026 — Series Navigation`; the other six say `📚 OpenClaw for Organizations 2026`. Make it match the six. |
| INV-04c | `.post-nav` container is `<div>` | 4 | `<nav class="post-nav">` in `claude-code-architecture`, `deployment-hosting`, `openclaw-memory-architecture`, `vibe-coding-devops-process`. Harmless; normalise to `<div>` only in a dedicated cleanup. |
| INV-04d | `.post-nav__dir` ∈ {`← Previous`, `Next →`} | 2 | `blog/claude-code-architecture.html:602-609` uses `Related` / `See also` — a post-nav-shaped block that is not part of any chain. Intentional; see allowlist. |
| INV-06a | every file in `images/` is referenced | 9 | Orphans from a prior template: `Opic02.jpg bg.jpg overlay.png pic01.jpg pic02.jpg pic03.jpg pictop.png xpic01.jpg xpic03.jpg`. Safe to delete in one commit; confirm with `grep -r` first. |
| INV-10 | `.post-nav__title` matches the target's card title | 8 | Stale labels. Worst: `devops-security.html` calls its Next target "Linux & Shell Essentials" but the post is "Linux Command Line". Copy the card title from `blog/index.html`. |
| INV-13 | `lang` attrs | 0 | Green: the 6 nav-bearing index pages and the 4 `books/` detail pages are `lang="en"`, all 37 posts `lang="th"`. |
| INV-14 | every post has `<meta name="description">` | 6 | Missing in `idle-self-improvement`, `openclaw-101`, `openclaw-agent-teams`, `openclaw-memory`, `openclaw-security`, `openclaw-skills`. |
| INV-15 | footer copyright year uniform **in posts** | 2 | 25 × `© 2025`, 8 × none, against the expected 4 × `© 2026` (beyond-plugins, obsidian-ai-jarvis, openclaw-101, openclaw-agent-teams). The script reports one violation per non-2026 cohort. |
| INV-16 | footer container class uniform | 4 variants | `blog-footer` 23, `footer` 7, `post-footer` 3, bare `<footer>` 4. |
| INV-17 | a card's section matches its nav family | 2 | `claude-code-architecture` and `openclaw-memory-architecture` sit in `#series-openclaw` but carry DevOps `post-nav`. See allowlist. |
| INV-18 | no `#series-devops` card uses the chip strip | 0 | Green. (The mirror rule, INV-19, is fail-level — see above.) |
| INV-20b | ordinal badge uses one consistent markup form | 4 | `.series-badge` ×4 (101, agent-teams, memory, production), `.series-info` ×1 (security), bare `<p>` ×1 (integrations), `<strong>` ×1 (skills). |
| INV-20c | badge is worded "Post #N" | 1 | `blog/openclaw-memory.html:328` writes `บทที่ 3`. |
| INV-22 | every post defines its own `:root` | 0 | Green since `6670480` landed the canonical block (28 tokens since the 2026-08-26 re-key) in all 42 files with embedded CSS, `style.css` included (INV-22b, info-level, is green for the same reason). Baseline entries deleted — a post that loses its `:root` is now reported as new. |
| INV-24 | the 6 nav-bearing pages agree on the footer `©` year and all carry a meta description | 0 | INV-14/15/16 iterate `site.posts` only, so `blog/index.html` and the landing pages sat outside every footer/meta check — which is how a `© 2025` footer survived on `blog/index.html` while the others read 2026. The year is checked for **consistency** (modal year wins), never against a hardcoded literal, so 1 January is not a linter event. |

Full drift inventory with counts and the reason each cohort exists: `references/drift-budget.md`.

## Allowlist — three things that look broken and must stay

Hard-coded in the script with comments. A future agent that "fixes" these will corrupt the one chain
that currently verifies perfectly.

1. **`git-branching.html`** — chain head. It has no nav at all, so it legitimately cannot reciprocate
   `cicd-pipeline.prev`. Do not invent a nav for it just to satisfy INV-04a.
2. **`claude-code-architecture.html`** — sits in `#series-openclaw` with a `Related` / `See also`
   block that belongs to no chain. Off-chain by design.
3. **The 5 no-nav posts** — `beyond-plugins.html`, `git-branching.html`,
   `idle-self-improvement.html`, `obsidian-ai-jarvis.html`, `openclaw-migration.html`. Standalone
   articles, not series members.

`openclaw-memory-architecture.html` is **not** allowlisted — its graft onto `deployment-hosting` is a
real INV-04a/04f defect.

## Adding or renaming a post

Read `references/adding-a-post.md` before touching `blog/`. It has the exact card block, the
three-edit chain rewiring recipe, and the copy-paste series strip. The one-line summary: copy a
DevOps post that already has `<nav class="blog-nav">` + `.post-nav` as your template — the 7
OpenClaw series posts are the un-templated corner of the site and account for nearly every warn-level
violation in the table above.

## If you edit the script

Five regex traps, each of which produced a *wrong pass or a false alarm* in a real audit. A wrong
regex makes the linter lie in the dangerous direction: it reports working chains as broken and
invites "fixes" that destroy real links — or, worse, it silently narrows a check's domain to
nothing and reports PASS forever.

```python
CARD  = r'<a\s+href="([^"]+)"\s+class="card">'
PNAV  = r'<(div|nav)\s+class="post-nav">'                 # BOTH tags: div ×21, nav ×4
PLINK = (r'<a\s+href="([^"]+)"\s+class="post-nav__link"[^>]*>\s*'   # [^>]*> is load-bearing
         r'<div class="post-nav__dir">([^<]*)</div>\s*'
         r'<div class="post-nav__title">(.*?)</div>')
ATTR  = r'\b(href|src|srcset|poster)\s*=\s*"([^"]+)"'     # NEVER include content=
CODE  = r'<(pre|code)\b[^>]*>.*?</\1>'                    # exclusion spans for the link checker
INERT = r'<(style|script|pre|code)\b[^>]*>.*?</\1>'       # blank_inert(): markup-shape checks
```

1. `class="post-nav__link">` (no `[^>]*`) drops the 3 Next anchors that carry
   `style="text-align:right;"` and fabricates 3 phantom dead-ends.
2. The container is `<nav class="post-nav">` in 4 files; a `div`-only pattern finds 0 links in them.
3. Non-greedy `<div …>(.*?)</div>` mis-nests, because post-nav blocks contain nested divs — anchor on
   the link pattern, never on the container's closing tag.
4. Scanning `content=` turns every `<meta name="description">` and the viewport tag into a "broken
   path" (90 hits instead of 14). Skipping `<pre>`/`<code>` removes 4 more false positives.
5. Any check that reasons about **markup shape** must run its text through `blank_inert()` first, or
   a CSS rule that merely names a class, or example markup inside a code sample, is counted as a
   real element. `blank_inert` blanks `<style>`/`<script>`/`<pre>`/`<code>` bodies while preserving
   byte offsets, so reported line numbers stay correct.

Title comparison for INV-10 must be `html.unescape(re.sub(r'\s+',' ',t)).strip()`, then emoji-stripped
(`[\U0001F000-\U0001FAFF☀-➿️]`), then `.strip().strip('—-').strip()` — see `norm_title` at
check_site.py:446-451. `&amp;` vs `&` alone yields ~14 false positives.

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
2. **No two cards adjacent on `blog/index.html` may share both ground and motif.** "37 covers that
   all look like one cover" is the real failure mode of a system this regular, and it shows up
   worst between neighbours. Checked in reading order, not table order.

`cream` (#faf7f0) was designed in and then **retired**: cards are `var(--white)`, so a cream cover
had no visible edge and read as a missing image.

Contact sheet for review — writes to `.covers/`, a dot-dir, because the first version wrote to the
repo root and INV-06a correctly reported it as an unreferenced published image:

```bash
python3 scripts/make_cover.py --check      # validate the table, draw nothing
python3 scripts/make_cover.py --all        # 37 covers + 37 share cards, ~2s
python3 scripts/make_cover.py --contact    # .covers/contact-sheet.jpg
```
