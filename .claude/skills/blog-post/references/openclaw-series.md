# The numbered OpenClaw series — read before touching any of these 7 files

Open this only when adding to, or editing, one of:

```
blog/openclaw-101.html          blog/openclaw-security.html      blog/openclaw-skills.html
blog/openclaw-agent-teams.html  blog/openclaw-integrations.html  blog/openclaw-production.html
blog/openclaw-memory.html
```

These 7 are the un-templated corner of the site. They were hand-written before the
DevOps template settled, and they account for nearly every drift metric in the repo.
Steering a new post here costs 10 file edits instead of 4 — prefer the DevOps template
unless the post genuinely belongs to this narrative arc.

## What makes them different from every other post

| | Other posts (30 non-numbered; 25 with `.post-nav`) | Numbered OpenClaw posts (7) |
|---|---|---|
| Header | `<nav class="blog-nav">` with `href="./"` in 26 of 30 | hand-rolled; **no `<nav class="blog-nav">` / `.blog-nav__back`** — 5 of 7 link back with a bare site-absolute `href="/blog"`; openclaw-memory.html and openclaw-skills.html have no back link at all |
| Nav | `.post-nav` prev/next pair, relative `foo.html` | `.series-nav` chip strip, site-absolute `/blog/<slug>` (no `.html`) |
| CSS vars | own `:root` in 27 of 30 | **no `:root` at all** — plain hex literals |
| `<meta name="description">` | present | missing in 5 of 7 (101, agent-teams, memory, security, skills) |
| Footer | `<footer class="blog-footer">` | `<footer class="footer">` ×5, bare `<footer>` ×2 (security, skills); copyright not standardised — 101 / agent-teams `© 2026 anirach.com • Built with ❤️ for the AI community`; memory `&copy; 2026 Anirach Mingkhwan. สงวนลิขสิทธิ์ทุกประการ.`; security / production `&copy; 2026 Anirach Mingkhwan. All rights reserved.`; integrations `&copy; 2024 …`; skills `&copy; 2026 anirach.com \| OpenClaw for Organizations Series` |

Verify any of the above with e.g.
`grep -c ':root' blog/openclaw-*.html` and `grep -l 'blog-nav' blog/openclaw-*.html`.

## The 7-chip strip is a fixed literal — copy it verbatim

Every one of the 7 files carries this block, identical except for which entry is the
`<span class="current">`. Commit 4c180c9 ("Standardize series navigation across all 7
OpenClaw posts") rewrote all seven at once; commit 7a0db83 then fixed two entries that
still pointed at retired slugs (`vision-2026`, `setup`). Hand-editing one file at a time
is what produced that two-commit sequence.

```html
            <div class="series-nav">
            <h3>📚 OpenClaw for Organizations 2026</h3>
            <div class="series-links">
                <a href="/blog/openclaw-101">#1 OpenClaw 101</a>
                <a href="/blog/openclaw-agent-teams">#2 Agent Teams</a>
                <a href="/blog/openclaw-memory">#3 Memory &amp; Knowledge</a>
                <a href="/blog/openclaw-security">#4 Security &amp; Access</a>
                <a href="/blog/openclaw-integrations">#5 Integrations</a>
                <a href="/blog/openclaw-skills">#6 Skills &amp; Automation</a>
                <a href="/blog/openclaw-production">#7 Production &amp; Scale</a>
            </div>
        </div>
```

In each host file, replace that file's own line with the `<span>` form, keeping the
label byte-identical:

```html
                <span class="current">#6 Skills &amp; Automation</span>
```

The files on disk write `&` literally (`#3 Memory & Knowledge`), not `&amp;`. Match
whatever the neighbouring lines in the file you are editing already use — do not
"normalise" one file in isolation, that is drift.

The extensionless `/blog/<slug>` form works because GitHub Pages resolves it to
`<slug>.html`. All 42 such hrefs currently resolve. Do not "fix" them to `.html`.

## Adding an 8th numbered post

1. Pick the ordinal and slug. The strip is order-sensitive; inserting in the middle
   renumbers every label after it, so append as `#8` unless the user insists.
2. Edit **all 7 existing files** plus the new one: extend `.series-links` with
   `<a href="/blog/openclaw-<new>">#8 <Label></a>` at the end of the list.
3. In the new file the `#8` entry is the `<span class="current">`.
4. Add the ordinal badge in the body. There is no single convention — the 7 files use
   four different markups (`.series-badge` ×4, `.series-info` ×1, bare `<p>` ×1,
   `<strong>` ×1) and `openclaw-memory.html` writes `บทที่ 3` rather than `Post #3`.
   Use `<div class="series-badge">Post #8</div>`, the plurality form.
5. Card goes at the **top** of `#series-openclaw` in `blog/index.html`, and both
   counters get recomputed (see SKILL.md).

## The 14 broken links these files carry

All 7 hand-rolled headers/footers link to pages that have never existed. The site is a
single-page portfolio; `blog/index.html:200-204` already uses the working form.

| Broken href | Correct target | Occurrences |
|---|---|---|
| `/about` | `../index.html#about` | openclaw-101:376, agent-teams:438, integrations:264, security:362, production:386, production:1329 |
| `/projects` | `../index.html#projects` | openclaw-101:375, agent-teams:437 |
| `/research` | `../index.html#research` | integrations:263, security:360 |
| `/teaching` | `../index.html#research` (no teaching section exists) | security:361 |
| `/contact` | `../index.html#contact` | production:387, production:1330 |
| `../about/` | `../index.html#about` | openclaw-memory:318 |

Reproduce the list with:

```bash
grep -n 'href="/about\|href="/projects\|href="/research\|href="/teaching\|href="/contact\|href="\.\./about/' blog/*.html
```

`verify-wiring.py` reports these at **warn** level, not fail, so they do not block your
edit — but if you are already editing one of these files, fix the ones in it.

## Two `#series-openclaw` cards that are NOT part of this strip

`claude-code-architecture.html` and `openclaw-memory-architecture.html` sit in the
OpenClaw section of `blog/index.html` but carry DevOps `.post-nav` chrome. They are not
numbered, they are not in the strip, and they are unreachable from the DevOps chain walk.
That is intentional. See `references/known-exceptions.md`.
