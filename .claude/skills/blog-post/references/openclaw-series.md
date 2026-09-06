# The numbered OpenClaw series — read before touching any of these 7 files

Open this only when adding to, or editing, one of:

```
blog/openclaw-101.html          blog/openclaw-security.html      blog/openclaw-skills.html
blog/openclaw-agent-teams.html  blog/openclaw-integrations.html  blog/openclaw-production.html
blog/openclaw-memory.html
```

These 7 were the roughest corner of the site. They were hand-written before the DevOps
template settled and for months supplied most of the repo's drift metrics — **that debt is
now fully paid** and the residual cost is structural, not cosmetic: the chip strip is a
fixed literal duplicated seven times, so steering a new post here costs 7 extra file edits.
Prefer the DevOps template unless the post genuinely belongs to this narrative arc.

**Their old problems are ALL fixed. Do not re-report any of them.** Re-verified
**2026-09-06**:

| Old defect | Fixed by | Guard, green today |
|---|---|---|
| no `:root` in 7 of them | `6670480` (canonical block; 24 tokens then, 29 now) | INV-22 |
| no a11y block | `e8da9da` | — |
| 14 broken site-absolute links | `b9fb125` | INV-05 |
| 5 of 7 missing `<meta name="description">` | 2026-08-26 metadata sweep | INV-14 / INV-27 |
| hand-rolled headers, no `.blog-nav__back` | 2026-08-26 island→house conversion | INV-29 |
| `<footer class="footer">` ×5, bare `<footer>` ×2, six different copyright strings | 2026-08-26 (`08cfd95`) | INV-15 / INV-16 |
| four different ordinal-badge markups, `บทที่ 3` in `openclaw-memory` | Phase 3 + `01332eb` | INV-20a/20b/20c |
| `openclaw-integrations`'s drifted `<h3>` | `01332eb` | INV-03b |
| monolingual | 2026-09-03 sweep (`scripts/bilingualize.py --all`) | `check_visibility.py` S1 |

## What still makes them different from every other post

| | Other posts (69 non-numbered) | Numbered OpenClaw posts (7) |
|---|---|---|
| Header | `<nav class="blog-nav">` with `href="./"` — **all 76 posts, these 7 included** | same |
| Footer | `<footer class="blog-footer">` — **all 76** | same |
| Nav | `.post-nav` prev/next pair (24), a different series' chip strip (39), or none (6) | `.series-nav` chip strip, site-absolute `/blog/<slug>` (no `.html`) |
| Badge | most posts have none; Hermes and AI Transformation write `• Post #N` in `.post-hero__series` | `.post-hero__tag` "OpenClaw for Organizations 2026 • Post #N", all 7 |
| CSS vars | canonical `:root`, all of them | canonical `:root`, all 7 — same block. `grep -c ':root' blog/openclaw-*.html` → `1` for every file. |

Verify any of the above with e.g.
`grep -c ':root' blog/openclaw-*.html` and `grep -l 'blog-nav' blog/openclaw-*.html`.

**They are also the only strip INV-03 checks by name.** INV-03/03b/20a iterate a hardcoded
`SERIES7` list; the Hermes, Life and AI Transformation strips are covered by INV-03c
instead, which needs no table. Both are FAIL severity — a strip edited in one file and not
the rest blocks the push either way.

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
`<slug>.html`. These 7 strips contribute **42** such hrefs (6 links × 7 files); the Hermes,
Life and AI Transformation strips add their own, and every one of them resolves
(`check_site.py` INV-09 PASSes). Do not "fix" them to `.html` — the canonical tag in the
head is what resolves the duplicate, and it deliberately uses the `.html` form.

## Adding an 8th numbered post

1. Pick the ordinal and slug. The strip is order-sensitive; inserting in the middle
   renumbers every label after it, so append as `#8` unless the user insists.
2. Edit **all 7 existing files** plus the new one: extend `.series-links` with
   `<a href="/blog/openclaw-<new>">#8 <Label></a>` at the end of the list. The strip is
   flat — do **not** copy the AI Transformation series' `.series-links--grouped` shape.
3. In the new file the `#8` entry is the `<span class="current">`. INV-03 compares the
   full 8-label sequence in order across all 8 files, so a typo in one is a violation.
4. Add the ordinal badge in the hero. There **is** a single convention now, since Phase 3
   (2026-08-26) converged all four old markups onto it and INV-20b/20c guard it:
   `<span class="post-hero__tag">OpenClaw for Organizations 2026 • Post #8</span>`.
   The old forms (`.series-badge` ×4, `.series-info` ×1, bare `<p>` ×1, `<strong>` ×1, and
   `openclaw-memory.html`'s `บทที่ 3`) are gone — do not resurrect one.
5. Give it **both language tracks** like every other post: `python3
   scripts/bilingualize.py --post openclaw-<new>`, then `--fill`, then `--verify` until it
   prints OK. The chip strip and the ordinal badge stay **monolingual** — INV-03 and
   INV-20a read them with regexes that truncate on a nested tag.
6. Card goes at the **top** of `#series-openclaw` in `blog/index.html`, and three counter
   sites get recomputed: the hero `Articles` stat, `#series-openclaw`'s `.series-count`,
   and its `.blog-jump` chip's trailing `· N` (INV-02f — `--fix` repairs the first two, not
   the chip).

## The 14 broken links these files used to carry — **FIXED, do not re-report**

All 7 hand-rolled headers/footers used to link to `/about`, `/projects`, `/research`,
`/teaching`, `/contact` and `../about/`, none of which existed. `b9fb125` ("fix stale
counters, forked hero gradient, and 14 dead absolute links") removed them, and Task 8
gave `/projects` a real page. The grep now returns **nothing**:

```bash
grep -c 'href="/about\|href="/projects\|href="/research\|href="/teaching\|href="/contact\|href="\.\./about/' blog/*.html \
  | grep -v ':0$'          # → no output
python3 .claude/skills/site-check/scripts/check_site.py | grep 'INV-05 '   # → PASS
```

The **back link** was the last piece and it is done too: all 7 now open with the house
`<nav class="blog-nav">` carrying `<a href="./" class="blog-nav__back">‹ Blog</a>`, like
the other 69 posts. The only surviving site-absolute form is one footer link in
`openclaw-production.html` (`href="/blog/"` — with the trailing slash, which is the point:
bare `/blog` cost two redirects, one of them an https→http downgrade). Never write a bare
directory href.

## Six `#series-openclaw` cards that are NOT part of this strip

`#series-openclaw` holds 13 cards: these 7 numbered posts plus 6 standalone ones —
`beyond-plugins`, `claude-code-architecture`, `idle-self-improvement`, `obsidian-ai-jarvis`,
`openclaw-memory-architecture`, `openclaw-migration`. They are not numbered, not in the
strip, and carry **no nav block at all**. Two of them (`claude-code-architecture`,
`openclaw-memory-architecture`) wore DevOps `.post-nav` chrome until `f5e53fb` deleted it
on 2026-08-26; INV-17 fails an OpenClaw card that grows it back, and INV-08 fails a post
outside `NO_NAV_POSTS` that has no nav. See `references/known-exceptions.md`.
