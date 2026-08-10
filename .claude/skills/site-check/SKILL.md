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

Exit 0 = no fail-severity violation outside the hard-coded BASELINE in check_site.py:153-260.
Exit 1 = at least one fail-severity violation whose key is not in that baseline. Exit 2 = usage or
environment error (bad `--root`, unknown `--check` id, bad flag). Warn- and info-level checks print
but never change the exit code, and neither do fail-level violations that match a baseline key —
today 20 fail-severity violations across INV-04a/05/07a/11/12 are reported as [known] and the
script still exits 0 once INV-02a/02c are fixed.

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
(`:220` Series, `:221` Articles) and every `.series-count` (`:235`, `:573`) — from the actual
`class="card"` counts, and rewrites only the ones that are wrong (2 of 4 today). It reports the
already-correct ones as `ok … (already correct)`. It is idempotent and touches no other file.
Nothing else is auto-fixable — every other failure needs a judgement call about which of two files
is wrong.

**Run it twice around every edit.** Capture the baseline before you touch anything, then compare.
The repo is red today (see below), so "the script failed" means nothing on its own; "the script
reports a violation that was not in the baseline" means you broke something. One blind spot
remains: cohort-keyed checks (INV-15's copyright year, INV-16's footer class) report one violation
per cohort, so a post moving between two already-known cohorts (e.g. © 2026 → © 2025) stays
[known] and will NOT flip the exit code — read the per-check counts and details, not just the
exit status.

## Expected red on today's tree — do not panic, do not mass-fix

A clean checkout fails. These are pre-existing, verified as of the last audit:

| id | count | what |
|----|-------|------|
| INV-02a | 1 | `blog/index.html:221` says `<strong>33</strong> Articles`, actual `class="card"` count is **37** |
| INV-02c | 1 | `blog/index.html:235` says `12 articles` for `#series-openclaw`, actual is **13** |
| INV-04a | 2 | one allowlisted chain-head edge (`cicd-pipeline.prev → git-branching`, by design) + one real defect (`openclaw-memory-architecture` grafted onto `deployment-hosting`) — see INV-04a below |
| INV-05 | 14 | broken site-absolute links in the per-post header/footer site nav of 6 of the 7 OpenClaw posts |
| INV-07a | 2 | two covers each shared by two posts |
| INV-11 | 1 | `blog/deployment-hosting.html` has two `<h1>` (lines 164 and 176) |
| INV-12 | 1 | `blog/index.html` renders a hamburger button but loads no JS |
| warn-level | — | INV-03b 1, INV-04c 4, INV-04d 2, INV-06a 9, INV-10 8, INV-14 6, INV-15/16/17/20b/20c/22 |

The parent brief describes "three stale counters". Verify before repeating that: the third counter,
`blog/index.html:573` `24 articles` for `#series-devops`, is **correct** today, as is
`:220 <strong>2</strong> Series`. Only two counters are stale. Say what the script prints, not what
you remember.

Fixing the baseline is welcome but is a separate, deliberate task — never bundle it into an
unrelated edit, because it makes the diff unreviewable.

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

14 failures today, all in the hand-rolled per-post site nav (`<ul class="nav-links">` /
`<div class="nav-links">` inside each post's own `<nav>`, plus openclaw-production's footer link
row at `:1327-1332`) — NOT in the `.series-nav` chip strip, which is clean. `openclaw-skills.html`
has none, so 6 of the 7 OpenClaw posts are affected. All point at pages that were never built.
**anirach.com is a single-page portfolio**; the working form is the one
`blog/index.html:200-204` already uses. Apply this mapping verbatim:

| broken | correct |
|--------|---------|
| `/about`, `../about/` | `../index.html#about` |
| `/projects` | `../index.html#projects` |
| `/research` | `../index.html#research` |
| `/contact` | `../index.html#contact` |
| `/teaching` | `../index.html#research` (no `#teaching` section exists — verify with `grep -n 'id="' index.html` before writing it) |

Exact sites: `openclaw-101.html:375,376`; `openclaw-agent-teams.html:437,438`;
`openclaw-integrations.html:263,264`; `openclaw-memory.html:318`;
`openclaw-production.html:386,387,1329,1330`; `openclaw-security.html:360,361,362`.

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

`blog/deployment-hosting.html` has two: `:164` the hero title, `:176` a near-duplicate inside the
article body. **Repair:** delete the body one (`:176`), keep `.post-hero__title`.

### INV-12 — a page rendering `.nav__hamburger` must load JS

`blog/index.html` has 4 hamburger references and **zero** `<script>` tags — the mobile menu is dead,
and it is the only page in the repo with this defect (`index.html` has both). At `max-width: 768px`,
`blog/index.html:173` sets `.nav__links { display: none; }`, so on a phone the blog index has no
navigation at all.

**Repair, pick one:** (a) add a small inline `<script>` mirroring `script.js`'s toggle — note
`script.js` is loaded *only* by root `index.html` and hooks `#hamburger`, `#nav`, `#navLinks`, so
the IDs must match; or (b) delete the hamburger button and the `@media` rule that hides
`.nav__links`. Do not leave it as-is and call the page done.

### INV-19 — the 7 numbered OpenClaw posts all live in `#series-openclaw`

0 today. A violation means a numbered series post was carded into the wrong section.

### INV-20a — the OpenClaw ordinal badge number == series-nav position

0 today; values 1–7 all correct. Only the badge *markup and wording* drift is warn-level
(INV-20b/20c below); a wrong number blocks the push.

### INV-21 — every DOM hook `script.js` uses exists in `index.html`

0 today. 8 selectors harvested: `#nav`, `#hamburger`, `#navLinks`, `a`, `[data-reveal]` ×2,
`a[href^="#"]`, `.hero__bg-text`. `index.html` carries 9 `data-reveal` attributes. Note
`data-reveal` inside `blog/` is inert (0 uses, 0 JS) — CLAUDE.md's advice to add it for scroll
fade-in is a **no-op in blog/** (INV-21b, info-level).

---

## Warn-level checks (real drift, never blocks a push)

Surface these; fix them deliberately, not opportunistically. A linter that fails the build on
cosmetics gets switched off. The real split is 25 fail / 14 warn / 4 info across 43 checks —
`--list` prints each check's severity.

| id | rule | today | repair |
|----|------|-------|--------|
| INV-03b | series-nav `<h3>` identical across the 7 | 1 | `blog/openclaw-integrations.html` says `OpenClaw for Organizations 2026 — Series Navigation`; the other six say `📚 OpenClaw for Organizations 2026`. Make it match the six. |
| INV-04c | `.post-nav` container is `<div>` | 4 | `<nav class="post-nav">` in `claude-code-architecture`, `deployment-hosting`, `openclaw-memory-architecture`, `vibe-coding-devops-process`. Harmless; normalise to `<div>` only in a dedicated cleanup. |
| INV-04d | `.post-nav__dir` ∈ {`← Previous`, `Next →`} | 2 | `blog/claude-code-architecture.html:602-609` uses `Related` / `See also` — a post-nav-shaped block that is not part of any chain. Intentional; see allowlist. |
| INV-06a | every file in `images/` is referenced | 9 | Orphans from a prior template: `Opic02.jpg bg.jpg overlay.png pic01.jpg pic02.jpg pic03.jpg pictop.png xpic01.jpg xpic03.jpg`. Safe to delete in one commit; confirm with `grep -r` first. |
| INV-10 | `.post-nav__title` matches the target's card title | 8 | Stale labels. Worst: `devops-security.html` calls its Next target "Linux & Shell Essentials" but the post is "Linux Command Line". Copy the card title from `blog/index.html`. |
| INV-13 | `lang` attrs | 0 | Green: `index.html` and `blog/index.html` are `lang="en"`, all 37 posts `lang="th"`. |
| INV-14 | every post has `<meta name="description">` | 6 | Missing in `idle-self-improvement`, `openclaw-101`, `openclaw-agent-teams`, `openclaw-memory`, `openclaw-security`, `openclaw-skills`. |
| INV-15 | footer copyright year uniform | 2 | 25 × `© 2025`, 8 × none, against the expected 4 × `© 2026` (beyond-plugins, obsidian-ai-jarvis, openclaw-101, openclaw-agent-teams). The script reports one violation per non-2026 cohort. |
| INV-16 | footer container class uniform | 4 variants | `blog-footer` 23, `footer` 7, `post-footer` 3, bare `<footer>` 4. |
| INV-17 | a card's section matches its nav family | 2 | `claude-code-architecture` and `openclaw-memory-architecture` sit in `#series-openclaw` but carry DevOps `post-nav`. See allowlist. |
| INV-18 | no `#series-devops` card uses the chip strip | 0 | Green. (The mirror rule, INV-19, is fail-level — see above.) |
| INV-20b | ordinal badge uses one consistent markup form | 4 | `.series-badge` ×4 (101, agent-teams, memory, production), `.series-info` ×1 (security), bare `<p>` ×1 (integrations), `<strong>` ×1 (skills). |
| INV-20c | badge is worded "Post #N" | 1 | `blog/openclaw-memory.html:328` writes `บทที่ 3`. |
| INV-22 | every post defines its own `:root` | 10 | The 7 series posts + `beyond-plugins`, `idle-self-improvement`, `openclaw-migration` have none. Also: `style.css` has **0** `:root` and **0** `var(` — it is hex-literal only, so CLAUDE.md's "use `--navy`/`--blue` from `:root`" applies to `blog/` pages, not to `style.css`. |

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

Four regex traps, each of which produced a *wrong pass or a false alarm* during the original audit.
A wrong regex makes the linter lie in the dangerous direction: it reports working chains as broken
and invites "fixes" that destroy real links.

```python
CARD  = r'<a\s+href="([^"]+)"\s+class="card">'
PNAV  = r'<(div|nav)\s+class="post-nav">'                 # BOTH tags: div ×21, nav ×4
PLINK = (r'<a\s+href="([^"]+)"\s+class="post-nav__link"[^>]*>\s*'   # [^>]*> is load-bearing
         r'<div class="post-nav__dir">([^<]*)</div>\s*'
         r'<div class="post-nav__title">(.*?)</div>')
ATTR  = r'\b(href|src|srcset|poster)\s*=\s*"([^"]+)"'     # NEVER include content=
CODE  = r'<(pre|code)\b[^>]*>.*?</\1>'                    # exclusion spans for the link checker
```

1. `class="post-nav__link">` (no `[^>]*`) drops the 3 Next anchors that carry
   `style="text-align:right;"` and fabricates 3 phantom dead-ends.
2. The container is `<nav class="post-nav">` in 4 files; a `div`-only pattern finds 0 links in them.
3. Non-greedy `<div …>(.*?)</div>` mis-nests, because post-nav blocks contain nested divs — anchor on
   the link pattern, never on the container's closing tag.
4. Scanning `content=` turns every `<meta name="description">` and the viewport tag into a "broken
   path" (90 hits instead of 14). Skipping `<pre>`/`<code>` removes 4 more false positives.

Title comparison for INV-10 must be `html.unescape(re.sub(r'\s+',' ',t)).strip()`, then emoji-stripped
(`[\U0001F000-\U0001FAFF☀-➿️]`), then `.strip().strip('—-').strip()` — see `norm_title` at
check_site.py:337-342. `&amp;` vs `&` alone yields ~14 false positives.
