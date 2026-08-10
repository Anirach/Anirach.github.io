---
name: page-design
description: The house visual system for anirach.com (this repo) — canonical :root tokens, type scale, layout constants, component vocabulary, breakpoints, modern-CSS verdicts, and the anti-patterns this repo has already been burned by. Use this whenever you create, restyle, or even lightly touch any HTML/CSS in this repository — a new blog post in blog/, a new section on index.html, a tweak to style.css, a nav or hero or callout or card, a diagram, a cover image, or a sweep across many files. Use it even if the user does not say "design", "style", or "CSS" — requests like "add a post about X", "make this look better", "fix the spacing", "add a diagram", "clean this up", "make it modern" all land here. Read it BEFORE writing markup, because the first question is always "is this file HOUSE or ISLAND?" and getting that wrong produces a 39-file inconsistency that is expensive to undo.
---

# The house visual system for anirach.com

## 0. Correct your mental model first

This looks like 37 hand-written blog posts that must be uniformly messy. It is not. It is **two
self-consistent families plus one hybrid**, and every design decision starts by classifying the
file you are about to touch.

```
blog/*.html  = 38 files = blog/index.html (listing) + 37 posts
37 posts     = 26 HOUSE + 11 ISLAND (one of which, obsidian-ai-jarvis, is a HYBRID)
```

Verified: `for f in blog/*.html; do grep -q 'class="blog-nav"' "$f" || basename "$f"; done`
→ 12 files, of which one is `index.html`, leaving 11 island posts.

| Axis | HOUSE (26) | ISLAND (10 pure) | HYBRID (obsidian-ai-jarvis) |
|---|---|---|---|
| `:root` + `var()` | yes 26/26 | no 0/10 | yes |
| Google Fonts + preconnect | yes 26/26 | no 0/10 | yes |
| `clamp()` | yes 26/26 | no 0/10 | yes |
| `.post-hero` / `.post-body` | yes 26/26 | no 0/10 | **no** (`.container` 800px) |
| nav | `<nav class="blog-nav">` | `.nav` ×7, none ×4 | `.nav` |
| code | `<pre>` 26/26 | `.code-block` 10/10 | `.code-block` |
| body type | `17px` / `1.8` | no `font-size` (UA 16px); 5×`1.6`, 5×`1.7` | `17px` / `1.8` |
| measure | `.post-body` 720px (24/26) — 760px in openclaw-memory-architecture + vibe-coding-devops-process | 1200 / 1000 / 900 / 800px | 800px |

**HOUSE deviations on those axes: two.** `openclaw-memory-architecture.html` and
`vibe-coding-devops-process.html` (both minified) use `.post-body{max-width:760px}` and declare no
`.post-body h2/h3/h4` rules. All 24 others match exactly.

**ISLAND (10):** `beyond-plugins`, `idle-self-improvement`, `openclaw-101`, `openclaw-agent-teams`,
`openclaw-integrations`, `openclaw-memory`, `openclaw-migration`, `openclaw-production`,
`openclaw-security`, `openclaw-skills`.
(Note the overlap: the 7 `.series-nav` OpenClaw posts are all island.)

### The rule this implies

- **Touching a HOUSE file?** Copy the pattern from its neighbour. `blog/api-request-lifecycle.html`
  is the cleanest reference — read lines 1–80 for the head + CSS and 180–201 for the markup.
  Do not invent. Do not "improve" the shared parts; you will fork them (see §7 nav drift).
- **Touching an ISLAND file?** Either leave its chrome alone or convert it fully to HOUSE. Never
  half-convert — a partial conversion creates a third family and destroys the property that makes
  this codebase tractable.
- **Creating a new post?** It is HOUSE, always. Copy `assets/post-template.html`.

Because every file embeds its own `<style>`, a "global" change means editing N files by hand.
That is the architecture, not a bug — see anti-pattern 2 before you reach for a shared stylesheet.

---

## 1. The canonical `:root`

Paste this verbatim. Read `references/tokens.md` for the per-token deviation table, the delete
list, and the rules for per-post brand tokens.

```css
:root {
  /* ink */
  --navy: #0f172a; --slate: #334155; --slate-light: #64748b; --gray: #94a3b8;
  /* ground */
  --bg: #f8fafc; --white: #ffffff; --code-bg: #1e293b;
  /* accent */
  --blue: #6366f1; --blue-dark: #4f46e5; --blue-light: #818cf8;
  /* status — use only these six, never invent a seventh */
  --green: #22c55e; --red: #ef4444; --amber: #f59e0b;
  --cyan: #06b6d4; --purple: #8b5cf6; --purple-dark: #7c3aed;
  /* type */
  --font: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  --mono: 'JetBrains Mono', 'Fira Code', monospace;
  /* form */
  --radius: 12px; --radius-sm: 8px; --radius-lg: 16px;
  --measure: 720px; --wide: 860px;
  --transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
```

**Why you can paste this into 39 files without fear:** the core twelve tokens have *zero value
conflicts* across all 28 `:root` blocks that exist today. `--navy #0f172a`, `--slate #334155` and
`--bg #f8fafc` are 28/28 identical; `--slate-light` and `--gray` are 26/26; `--blue` and
`--blue-light` 25/25; `--code-bg` 24/24; `--blue-dark` 20/20. And `style.css` — which declares
**zero** custom properties (`grep -cE '^\s*--[a-z-]+\s*:' style.css` → `0`) — already uses nine of
the ten palette hexes as literals (all but `--blue-light` `#818cf8`). Standardising the palette is
a visual no-op. The entire diff is 9 value normalisations and 3 deletions, not a redesign. Say so
in the commit message; that is what makes a 39-file sweep reviewable.

Only five tokens genuinely conflict, and three names are pure aliases of tokens that already exist
(`--indigo` == `--blue`, `--muted` == `--slate-light`, `--violet` == `--purple-dark`). `--teal2` is
**not** an alias — it is a second teal value; see `references/tokens.md` §2. Full list there.

**`--radius` is `12px`, not `14px`.** `grep -ho 'border-radius: *[0-9]*px' index.html style.css blog/*.html | tr -d ' ' | sort | uniq -c | sort -rn`
→ `168 12px`, `96 8px`, `75 10px`, `54 6px`, `33 20px`, `31 16px`, … `5 14px`. CLAUDE.md documents
`--radius: 14px`, and `--radius` is declared in exactly one file (`blog/index.html`) at that wrong
value. Use 12 / 8 / 16. Keep `20px`–`50px` pills for tags and chips only. See anti-pattern 10.

---

## 2. The type scale is finished — extend it, do not redesign it

This is the most consistent part of the codebase. Resist the urge to "modernise typography"; there
is nothing to fix.

| Role | Value | Evidence |
|---|---|---|
| body | `17px` / `1.8` | 26/26 house posts, zero variance |
| post title | `clamp(1.8rem, 5vw, 3rem)` | 26 files, one value |
| `.post-body h2` | `1.6rem` / 800 | 24 files declare it, **24/24 identical** |
| `.post-body h3` | `1.25rem` / 700 | 24 files declare it, **24/24 identical** |
| `.post-body h4` | `1.05rem` / 700 | 24 files, **24/24 identical** |
| `.post-body p` | `margin-bottom: 1.25rem` | house |
| landing section heading | `clamp(2rem, 4vw, 3.5rem)` | `style.css` lines 310, 364, 437 — identical; line 485 is a near-miss at `clamp(2rem, 4vw, 3.2rem)` — snap it to 3.5rem |

Verify with a block-aware parse, not a line-based grep (most rules span lines, so
`grep -ho '\.post-body h2[^}]*}'` undercounts):
`python3 -c "import re,glob; print(sum(1 for f in glob.glob('blog/*.html') for m in re.finditer(r'([^{}]*)\{[^{}]*\}', open(f).read()) if re.search(r'\.post-body\s+h2\b', m.group(1))))"`
→ `24`, every one `font-size: 1.6rem`. The 2 house files with no `.post-body h2/h3/h4` rules at all
are `openclaw-memory-architecture.html` and `vibe-coding-devops-process.html` (§0).

The work is not redesign, it is **extension to the 11 island files** (and `blog/index.html`, which
is `16px` / `1.7`). Font stacks to retire when you convert an island file: `'SF Pro Display', …`
(×3), `'Segoe UI', Tahoma, Geneva, Verdana` (×1), bare `-apple-system, …` (×4),
`'Inter', 'Noto Sans Thai', system-ui` (×1), and
`'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif` (×1,
`openclaw-production` — names Inter but never loads it, see anti-pattern 9).

---

## 3. Layout constants — always pick the incumbent

| Constant | Value | Uses today |
|---|---|---|
| reading measure (`.post-body`) | **720px** | 74 |
| wide container (`.blog-nav__inner`, listing) | **860px** | 26 |
| hero cover box | **380px** max-width (13 of 25), border-radius 16px = `--radius-lg` (25/25) | retire 420/480/520/560 |
| listing card image | `.card__image`: width 100%; aspect-ratio 16/10 | `blog/index.html:101-103` |
| tablet breakpoint | **768px** | 17 |
| phone breakpoint | **600px** | 21 |
| wide breakpoint | **1024px** | 1 — `style.css:586`, landing grids only |
| retire | `480px` (2), `500px` (1) | fold into 600px |

`grep -ho '@media[^{]*' index.html style.css blog/*.html | sort | uniq -c | sort -rn`
→ `21 (max-width: 600px)`, `15 + 2 (max-width: 768px)`, `2 480px`, `1 500px`, `1 1024px`.
Two of the 768px hits are unspaced (`max-width:768px`) — match the spaced form in new code so
grep-based sweeps find them.

Island measures to convert away from: 1200px (`openclaw-101`, `openclaw-agent-teams`,
`openclaw-production`), 1000px (`openclaw-security`), 900px (`openclaw-memory`), 800px
(`beyond-plugins`, `idle-self-improvement`, `obsidian-ai-jarvis`, `openclaw-migration`,
`openclaw-integrations`, `openclaw-skills`).

---

## 4. Component vocabulary

The house already has the right chrome, header, body and listing primitives; the Content group is
**new** and replaces the box sprawl below. **Freeze this list. Anything new must be a modifier of
an existing noun, never a new noun.** Full markup for each, copy-paste ready, is in
`references/components.md` — open it whenever you add a callout, card, figure, or nav.

```
Chrome     .blog-nav  .blog-nav__inner  .blog-nav__back  .blog-nav__title
Header     .post-hero  .post-hero__tags  .post-hero__tag  .post-hero__title
           .post-hero__meta  .post-hero__series  .post-hero__cover
Body       .post-body                       (max-width: var(--measure))
Footers    .post-series-footer  .post-nav  .series-nav
Listing    .card  .card__image|__body|__tags|__tag|__title|__excerpt|__footer|__author|__read
           .blog-grid  .series-section  .series-header  .series-count
Content    .callout  .callout--info|--warn|--good|--bad    [NEW — 0 uses today]
           .compare  .compare__col  .compare__col--old|--new  [NEW — 0 uses today]
           .figure  .figure__img  .figure__caption          [NEW — 0 uses today]
Code       <pre><code>                      (never .code-block)
```

The sprawl this replaces is real (counts are exact `class="X"` token occurrences): **18 bespoke
`*-card` classes** (`info-card` ×27, `tool-card` ×10, `pillar-card` ×9, `skill-card` ×9,
`stat-card` ×8, `component-card` ×8, `mini-card` ×6, `solid-card` ×5, `team-card` ×5,
`pattern-card` ×5, `strategy-card` ×4, `feature-card` ×4, `compare-card` ×4, `provider-card` ×3,
`metric-card` ×3, `level-card` ×3, `slo-card` ×3, `api-card` ×3) and **14 bespoke box/callout
classes** (`diagram-box` ×39, `arch-box` ×27, `highlight-box` ×15, `info-note` ×10,
`compare-box` ×4, `series-info` ×4, `warning-box` ×3, `alert` ×3, `tip` ×2, `insight-box` ×2,
`analogy-box` ×2, `case-study-box` ×1, `danger-box` ×1, `success-box` ×1).

Do not rename these en masse today — that is Phase 4 (§8). But **never add a 19th card name or a
15th box name.** When you need a new visual treatment, it is `.card--<modifier>` or
`.callout--<modifier>`.

`blog/index.html` already uses perfect BEM (`class="card"` ×37 with `card__image`, `card__body`,
`card__tags`, `card__title`, `card__excerpt`, `card__footer`, `card__author`, `card__read`, and
`card__tag` ×111). So does `style.css` (`.btn--pill`, `.hero__label--bold`). Follow that.

---

## 5. Hero gradients — five approved, pick by series

Today there are **78 distinct `linear-gradient(135deg, …)` values across 130 occurrences**, and 17
distinct `.post-hero` gradients across 26 house posts. This is the noisiest thing on the site.

| Family | Gradient | Use for |
|---|---|---|
| Default / light | `linear-gradient(135deg, #e8f0fe 0%, #ddd6fe 50%, #c7d2fe 100%)` | DevOps fundamentals |
| Indigo deep | `linear-gradient(135deg, #1e1b4b 0%, #312e81 40%, #3730a3 100%)` | security / auth |
| Violet | `linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%)` | OpenClaw series |
| Emerald | `linear-gradient(135deg, #052e16 0%, #064e3b 40%, #065f46 100%)` | testing / quality |
| Teal | `linear-gradient(135deg, #134e4a 0%, #115e59 40%, #0f766e 100%)` | SRE / observability |

The default is already the plurality (9 posts). `blog/index.html` carries an accidental fork of it
at line 64 — identical except the middle stop is `40%` instead of `50%`. Verified:
`grep -ho 'linear-gradient(135deg, *#e8f0fe[^)]*)' index.html blog/*.html | sort | uniq -c`
→ `9` at 50% and `1` at 40%. Align it to 50%.

**Never hand-pick a sixth.** Retire the one-offs when you touch their file: `#0c1929…`
(docker-compose), `#0d1117…` (github-actions), `#1a0533…` (gitops), `#0369a1…` (cloud), `#0891b2…`
(deployment), `#059669…` (idle), `#2563eb…` (migration), `#4f46e5…#06b6d4` (vibe-coding).

---

## 6. Modern CSS — ranked by ROI, with verdicts

The honest ranking here is lopsided. **Images dominate every CSS technique combined.**

### ADOPT NOW, in this order

**1. Image loading — the single highest-ROI change in the repo.**
`blog/index.html` ships **18.4 MB across 36 unique images** (`19,247,246` bytes, computed by
summing unique `src="../images/…"` targets), over **74 `<img>` tags**, with `loading=` on **0**
files and `decoding=` on **0** files and zero `width`/`height` attributes anywhere. Guaranteed
layout shift on every visit.

```html
<img src="../images/api-lifecycle-cover.jpg" alt="API Request Lifecycle — cute dog illustration"
     width="1600" height="900" loading="lazy" decoding="async">
```

Above-the-fold hero covers get `loading="eager" fetchpriority="high"` instead. Pair with
`aspect-ratio` (below) so the box is reserved before the bytes arrive.

**2. `aspect-ratio`** — already correct on `.card__image` (`blog/index.html:102`, `16/10`) and
`style.css:516`. Do not change it. The gap is `.post-hero__cover`, which reserves no box in any of
the 25 files that declare it; add `aspect-ratio` there matching the actual cover art ratio.

**3. `:focus-visible`** — there is **zero** focus styling in the entire repo. `grep -l ':focus-visible'`
matches 0 files, and there is no `outline` declaration anywhere. The site is currently unusable by
keyboard. Non-negotiable; three lines per file.

**4. `prefers-reduced-motion`** — also **0 files**, against 63 `transition:` declarations (70 raw
hits including one `--transition:` and six `var(--transition)`), **36 `translateY`** hover lifts,
an IntersectionObserver reveal at `script.js:40–59`, a nav scroll toggle at `script.js:13–17`, and
a scroll parallax at `script.js:75+`. The parallax alone justifies it.

**5. `color-scheme: light`** — 0 files. The site is 100% light but declares nothing, so UA-painted
scrollbars and form controls render dark for dark-OS visitors against a `#f8fafc` page. One line.

**6. `text-wrap: balance`** — 0 files. Stops orphaned words in the `clamp()` hero titles and the 37
card titles. Degrades to nothing where unsupported. Free.

**7. `clamp()` fluid type** — already the mechanism in 28 HTML files plus `style.css`. The
post-title value is canonical (`clamp(1.8rem, 5vw, 3rem)`, 26/26 house files); the landing page has
its own scale in `style.css`. Extend to the 11 island files; do not redesign either scale (§2).

The three snippets to paste, verbatim:

```css
/* focus — currently zero coverage repo-wide */
:focus-visible { outline: 2px solid var(--blue); outline-offset: 3px; border-radius: 2px; }
:focus:not(:focus-visible) { outline: none; }

/* motion */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: .01ms !important; animation-iteration-count: 1 !important;
    transition-duration: .01ms !important; scroll-behavior: auto !important;
  }
}

/* colour scheme + heading wrap */
:root { color-scheme: light; }
h1, h2, h3, .post-hero__title, .card__title { text-wrap: balance; }
```

And guard the JS in `script.js` (the CSS media block cannot stop a `scrollY`-driven transform):

```js
const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
```

### LATER — blocked, not declined

- **`prefers-color-scheme` dark mode.** Genuinely worth having, but with per-file CSS it means 39
  hand-maintained dark palettes plus dark variants of 78 gradients, and the light-lavender hero has
  no dark analogue. **Blocked on the §1 tokens landing in all 39 files.** Once they have, it is one
  `@media` block per file. Do not attempt before then.
- **`color-mix()`.** Would collapse ~30 one-off tint gradients (`#eff6ff`, `#ecfdf5`, `#fefce8` …)
  into derivations of `--blue` / `--green` / `--amber`. Excellent second pass, after tokens.

### NOT NOW

- **`content-visibility: auto`.** Long posts exist (`web-architecture.html` 91 KB,
  `frontend-performance.html` 69 KB) but `.post-body` has no section children to apply it to, and
  the real bottleneck is 18.4 MB of images. Revisit only if posts get sectioned.

### NEVER — with reasons

- **CSS nesting.** This repo is maintained by grepping and find-replacing *flat* selectors across 39
  files. There is no build step to flatten nesting. §7 shows how easily cross-file edits already
  drift; nesting would make every sweep measurably harder. Actively harmful here.
- **Logical properties** (`margin-inline`, `padding-block`). Zero adoption today; both site languages
  (English, Thai) are LTR. Buys nothing, costs a rewrite of every margin and padding in 39 files.
- **Container queries.** `.post-body` is a single 720px column with nothing to adapt, and the card
  grid already works via `auto-fit`/`minmax`. No problem to solve.
- **`:has()`.** No identified use case.

---

## 7. Anti-patterns — every one of these already happened here

1. **Never build an architecture diagram from inline HTML/CSS or ASCII art.** This repo tried and
   reverted twice: `f4f7e1b` "Replace ASCII art diagrams with proper HTML/CSS…" and `4fc85af`
   "Replace ASCII diagram with responsive HTML/CSS component" built them; `c270892` "Replace broken
   inline HTML diagrams with proper PNG diagrams" (+14/−84) ripped them out and `4ae2660` swept the
   leftovers (−40). Also `2f7ea33` had to restore content a nav edit ate. **Diagrams are PNGs in
   `images/`**, referenced with `width`/`height`/`loading="lazy"`. 19 files still carry
   `.diagram-box`/`.arch-box` remnants — delete them when you touch those files.
   **Exception:** box-drawing characters *inside* `<pre>` or `.code-block` that reproduce real CLI
   output are correct — e.g. `blog/openclaw-agent-teams.html:874`, a `subagents list` table. Do not
   strip those while cleaning up ASCII art. The `/* ── SECTION ── */` CSS comment convention
   (10 files, 39 uses) is also deliberate and worth keeping.

2. **Never add a shared stylesheet before resolving the name collisions.** `index.html` is the only
   file linking `style.css`. Dropping a `<link>` into a post today collides immediately: `.nav`
   means three different components (`index.html`, `blog/index.html`, island posts); `.card` means
   "blog listing card" in `blog/index.html` but is a generic name in 20 posts; and each post's own
   `:root` would fight the shared one. Rename to the §4 vocabulary *first*, then share. Until then,
   propagating a change means editing N files — that is the deal.

3. **Never let a duplicated block drift silently.** `.blog-nav` CSS already exists in 4 variants
   across the 26 house posts: 14 files, 10 files, and two singletons
   (`openclaw-memory-architecture.html`, minified; `vibe-coding-devops-process.html`). The 10-file
   variant adds `display: flex; align-items: center; gap: 0.4rem;` to `.blog-nav__back` — so **14
   files never received that fix.** When you edit a duplicated block, edit all N or none, and say
   which N in the commit. (That same rule also has `color: #4f46e5` hard-coded where
   `var(--blue-dark)` belongs.)

4. **Never reuse a cover image.** 37 cards resolve to only 35 unique covers:
   `../images/github-actions-cover.jpg` is shared by `vibe-coding-devops-process.html` and
   `github-actions.html`; `../images/monitoring-cover.jpg` by `openclaw-memory-architecture.html`
   and `monitoring-observability.html`. Those pairs are indistinguishable on the listing.

5. **Never commit a cover over ~200 KB, and never as PNG.** PNGs average **821 KB** (22 files,
   17.6 MB); JPGs average **82 KB** (28 files, 2.3 MB) for the identical editorial job — a 10×
   difference. 15 files exceed 500 KB, all PNG, led by `obsidian-ai-jarvis-cover.png` (1.57 MB),
   `idle-self-improvement-cover.png` (1.54 MB), `claude-code-architecture-cover.png` (1.50 MB).
   Photographic / AI-generated covers are JPG or WebP at ≤1600px wide. PNG is only for diagrams
   with flat colour and text.

6. **Never add a post without updating all three counters in `blog/index.html`.** Line 221
   `<strong>33</strong> Articles` — actual is **37**. Line 235 `<span class="series-count">12
   articles</span>` for `#series-openclaw` — actual is **13**. Line 573 `24 articles` for
   `#series-devops` — correct. Three numbers, three line numbers, every single time. (Link integrity
   itself is fine: 37 unique post links, 37 post files, no orphans, no dead post links.)

7. **Never invent a token name for a value that already has one.** `--indigo` == `--blue`,
   `--muted` == `--slate-light`, `--violet` == `--purple-dark`. (`--teal2` is *not* an alias — it
   is a second teal value; see `references/tokens.md` §2.) Check `references/tokens.md` before
   adding anything.

8. **Never hand-pick a new hero gradient.** 78 already exist. Choose from the five in §5.

9. **Never name a font the page does not load.** `blog/openclaw-production.html` and
   `blog/openclaw-security.html` both declare `'Inter'` in `font-family` with no Google Fonts
   `<link>` and no `preconnect` — they silently render in a system font while claiming the house
   typeface. All 10 pure island files lack both tags.

10. **Never link an absolute route that does not exist.** None of `/about`, `/projects`, `/research`,
    `/contact`, `/teaching` exist on disk, yet `/about` is linked from 5 files, `/projects` from 2,
    `/research` from 2, `/contact` from 1, `/teaching` from 1, plus `href="../about/"` at
    `blog/openclaw-memory.html:318`. Extensionless `/blog/openclaw-*` links **are** fine — GitHub
    Pages resolves them to `.html`, and all 7 targets exist.

11. **Never let CLAUDE.md drift.** It currently states three false things: `--radius: 14px` (real
    value 12px, 168 uses vs 5, and `--radius` is declared in 1 of 39 files); "see `blog/index.html`
    or `style.css`" for CSS variables (`style.css` has **zero**); and "Blog listing with category
    filters" (`blog/index.html` has **zero** `<script>` tags; the only `filter` occurrences are
    `backdrop-filter: blur(...)` at lines 32 and 168). **Fix these three when the house system
    lands**, or the next session inherits the same three false beliefs.

12. **Never add JavaScript to `blog/index.html`.** `grep -c '<script' blog/index.html` → `0`. That
    is a feature worth defending. Any filtering must work without JS or not ship.

13. **Cap emoji in headings at roughly one per section, and never in `<h2>`.** Today it ranges from
    57-of-65 headings (`openclaw-skills.html`) and 53-of-55 (`openclaw-memory.html`) down to zero in
    7 files (claude-code-architecture, docker-vs-vms, git-branching, kubernetes-orchestration,
    linux-command-line, monitoring-observability, networking-fundamentals). Posts sitting side by
    side in the same series read as different websites.

14. **Never regress alt text.** 118 of 118 `<img>` have `alt` — the one complete accessibility
    practice in the repo. Protect it.

---

## 8. Adoption order — smallest diff first

**Phase 1 — invisible, mechanical, zero visual change.** Paste the §1 `:root` into all 39 files. In
the 28 that already have one this only *adds* missing tokens and normalises 9 values. In
`style.css`, 9 of 10 hexes already match, so it is a pure find-and-replace (only `#475569`, 1 use,
is off-palette). In the 11 island files, replace their hex literals with `var()`. Delete the 3
alias tokens and fold `--teal2` into the Teal hero gradient. Set `--radius: 12px` and correct
CLAUDE.md (anti-pattern 11).

**Phase 2 — visible tidy, high ROI.** `loading="lazy"` + `decoding="async"` + `width`/`height` on
all 118 `<img>`; re-encode the 15 oversized PNG covers to JPG (drops `blog/index.html` from 18.4 MB
to roughly 3 MB); commission art for the 2 shared covers; fix the 3 counters; fix the 6 dead
routes; move `blog/index.html:64`'s hero gradient stop from 40% to 50%.

**Phase 3 — modern polish, 3 snippets × 39 files.** `:focus-visible`, `prefers-reduced-motion`
(+ the `matchMedia` guard in `script.js`), `color-scheme: light`, `text-wrap: balance`,
`aspect-ratio` on covers.

**Phase 4 — structural, genuinely optional.** Convert `obsidian-ai-jarvis.html` first: it already
has house tokens, Inter, `clamp()` and `17px`/`1.8`, and only needs `.nav`→`.blog-nav`,
`.container` 800px → `.post-hero`/`.post-body` 720px, and `.code-block`→`<pre>`. It is ~80% done and
is the cheapest possible proof that the recipe works. Then the 10 island posts. Then collapse the
callout and card vocabularies. **Only then** consider a shared stylesheet, and after that, dark mode.

A partial migration is not a failure. Phases 2 and 3 are where the site visibly becomes nice,
modern and tidy; Phase 4 is housekeeping.

---

## 9. What is already right — do not "improve" it

Leave these alone unless the user explicitly asks:

- the heading scale (`h2` 1.6rem 24/24, `h3` 1.25rem 24/24, hero `clamp(1.8rem, 5vw, 3rem)` ×26)
- the 720px measure (74 uses) and the 860px wide container (26 uses)
- the BEM naming in `style.css` and in `blog/index.html`'s `.card`
- the glassy nav: `background: rgba(248,250,252,0.85); backdrop-filter: blur(20px)`
- the `/* ── SECTION ── */` CSS comment convention (10 files, 39 uses)
- 100% alt-text coverage (118/118)
- `<meta name="viewport">` on 39/39 files

Genuinely missing sitewide, if the user wants more: `og:image`, `og:title` and `rel="canonical"` are
on **0** of 39 files, so every shared link renders as a bare URL; and 6 of 39 files still lack even
a `<meta name="description">`.

---

## Files in this skill

| File | Open it when |
|---|---|
| `references/tokens.md` | adding/changing any colour, radius, or token; doing a Phase 1 sweep |
| `references/components.md` | writing markup for a nav, hero, callout, card, figure, or code block |
| `assets/post-template.html` | creating a new blog post — copy this, do not hand-roll |
