---
name: page-design
description: The house visual system for anirach.com (this repo) — canonical :root tokens, type scale, layout constants, component vocabulary, breakpoints, modern-CSS verdicts, and the anti-patterns this repo has already been burned by. Use this whenever you create, restyle, or even lightly touch any HTML/CSS in this repository — a new blog post in blog/, a new section on index.html, a tweak to style.css, a nav or hero or callout or card, a diagram, a cover image, or a sweep across many files. Use it even if the user does not say "design", "style", or "CSS" — requests like "add a post about X", "make this look better", "fix the spacing", "add a diagram", "clean this up", "make it modern" all land here. Read it BEFORE writing markup, because the first question is always "is this file HOUSE, LISTING, DETAIL or ISLAND?" and getting that wrong produces a 47-file inconsistency that is expensive to undo.
---

# The house visual system for anirach.com

> ## Standing rule — numbers in this skill are load-bearing
>
> **Any change that invalidates a number in a skill file must update that number
> in the same commit.** Every count in this file, in `references/tokens.md` and in
> `references/components.md` is printed next to the command that produces it. If
> you run a sweep and do not re-run those commands, the next session inherits a
> confident, precise, wrong number and plans work that is already done.
>
> This is not hypothetical. Three sitewide sweeps (`6670480` tokens, `ec2827b`
> covers, `e8da9da` a11y) landed without touching a single skill file, which is
> how this skill spent a whole session telling readers there were "0
> `:focus-visible` rules" in a repo that had 42 of them.

## 0. Correct your mental model first

This looks like 37 hand-written blog posts that must be uniformly messy. It is not. It is **four
self-consistent families plus one hybrid**, and every design decision starts by classifying the
file you are about to touch.

```
67 HTML files
  = index.html            (landing — the only page with <script> and the only one
                           with no embedded <style>; its CSS is all style.css)
  + 5 LISTING pages       blog/index.html, books/index.html, news/index.html,
                           projects/index.html, publications/index.html
                                                — .nav chrome, 16px/1.7, 1200px
  + 404.html              (root; LISTING chrome and type, but NOT a section index —
                           it is noindex, carries no social block, and is excluded
                           from sitemap.xml. check_site.py does not enumerate it,
                           which is why every count below still reads 47.)
  + 4 DETAIL pages        books/three-old-men.html, books/a-pocketful-of-questions.html,
                           books/the-thirteenth-seal.html, books/one-day-of-light.html
                           — same .nav chrome and type
                           as LISTING, one subject per page, carded from books/index.html
                           (check_site.py INV-26 enforces that link)
  + 56 posts in blog/     = 45 HOUSE + 11 ISLAND (the 9 Life + 10 Hermes bilingual posts are HOUSE)
                           (one of the 11, obsidian-ai-jarvis, is a HYBRID)
```

```bash
find . -name '*.html' -not -path './.git/*' -not -path './.claude/*' | wc -l   # → 67
for f in blog/*.html; do grep -q 'class="blog-nav"' "$f" || basename "$f"; done # → 12
```

That second command returns 12, of which one is `blog/index.html`, leaving **11 island posts**.

**The LISTING family is new** (Task 8, commits `fd63657` / `3f3d049` / `5447407`; `publications/`
split out of `books/` on 2026-08-23, `a648a85`) and it is
internally consistent: all five pages use `.nav` / `.nav__inner` / `.nav__links` / `.nav__logo` /
`.nav__right`, `16px`/`1.7` body type, a `max-width: 1200px` container, one `clamp()` hero title,
and the pure-CSS `.nav__toggle` checkbox + `.nav__burger` label mobile menu (takeover at **800px**
since `5178252`, byte-identical across all 9 island-chrome pages — the 5 listing + 4 detail).
Copy a sibling listing
page when you add another; do not give a listing page `.blog-nav` chrome and do not give a post
`.nav` chrome.

**The DETAIL family is newer still** (`ea3c8e8`, 2026-08-23): a per-subject page inside a section
directory — today the four books under `books/` (`one-day-of-light.html` joined in `7daf3a4`). A DETAIL page shares the LISTING chrome and type
wholesale (same `.nav`, same 800px takeover block, `16px`/`1.7`, 1200px container, `clamp()` hero
title), wraps its content in `<main id="main">`, and is reached from its own section index via a
whole-card anchor (`<a class="card card--feature" href="<slug>.html"
aria-labelledby="card-title-<slug>">` — the `aria-labelledby` scopes the card's accessible name to
its title instead of the whole card text). `check_site.py` INV-26 fails the build if a detail page
exists that its index never links, or if the index links a same-dir `.html` that does not exist.
Adding a book = one new `books/<slug>.html` copied from a sibling detail page + its card in
`books/index.html` + the counter labels `check-news-sync.py` recomputes.

| Axis | HOUSE (26) | ISLAND (10 pure) | HYBRID (obsidian-ai-jarvis) |
|---|---|---|---|
| `:root` tokens | yes 26/26 | **yes 10/10 since `6670480`** | yes |
| `:focus-visible` + reduced-motion + `color-scheme` + `text-wrap` | yes 26/26 | **yes 10/10 since `e8da9da`** | yes |
| Google Fonts + preconnect | yes 26/26 | no 0/10 | yes |
| `clamp()` | yes 26/26 | no 0/10 | yes |
| `.post-hero` / `.post-body` | yes 26/26 | no 0/10 | **no** (`.container` 800px) |
| nav | `<nav class="blog-nav">` | `.nav` ×7, none ×4 | `.nav` |
| code | `<pre>` 26/26 | `.code-block` 10/10 | `.code-block` |
| body type | `17px` / `1.8` | no `font-size` (UA 16px); 5×`1.6`, 5×`1.7` | `17px` / `1.8` |
| measure | `.post-body` 720px (24/26) — 760px in openclaw-memory-architecture + vibe-coding-devops-process | 1200 / 1000 / 900 / 800px | 800px |

**The island/house gap is now narrower than it looks.** Two of the sweeps reached every file
regardless of family: the canonical 28-token `:root` (all 49 blocks) and the a11y block (46
embedded `<style>` blocks + `style.css`). What still separates island from house is **chrome and
typography**, not tokens or accessibility. Do not re-plan the token or a11y work for island files;
it is done. See `references/tokens.md` §1.

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
- **Creating a new post?** It is HOUSE, always. Copy `assets/post-template.html` — the **only**
  post template in this repo. (`blog-post/assets/post-template.html` was a second copy; it rotted
  three sweeps behind and was deleted. See `blog-post/assets/TEMPLATE-MOVED.md`.)

Because every file embeds its own `<style>`, a "global" change means editing N files by hand.
That is the architecture, not a bug — see anti-pattern 2 before you reach for a shared stylesheet.

---

## 1. The canonical `:root` — already landed, keep it byte-identical

**This sweep is finished.** `6670480` put the block below into every file; `36d9814` fixed its one
bad target, and the 2026-08-23 books/publications split and the 2026-08-24 One Day of Light page kept it clean. All **47** `:root` blocks
across the 46 HTML files that have one plus `style.css`
declare all 28 tokens with **zero value deviations** — every token reads `×49` in the audit
(47 site pages + `404.html` + `assets/post-template.html`).
`index.html` is the one file with no `:root` of its own, by design: its CSS is `style.css`, which
carries the block at line 5.

Paste this verbatim into anything new. Read `references/tokens.md` for the audit command, the
remaining non-canonical tokens, and the rules for per-post brand tokens.

```css
:root {
  color-scheme: light;
  /* ink */
  --navy: #11304b; --slate: #334155; --slate-light: #526174; --gray: #94a3b8;
  /* ground */
  --bg: #faf7f0; --white: #ffffff; --code-bg: #1e293b;
  /* accent */
  --blue: #226299; --blue-dark: #1a4d7a; --blue-light: #4992b9;   /* --blue-light is BORDERS ONLY */
  /* brand — sampled from the book covers (2026-08-26 re-key) */
  --gold: #c4a46c; --gold-dark: #7a5f22; --cloud: #dee7e6; --parchment: #e9e1c4;
  --focus: #226299;   /* footers and <pre> re-point this to --gold; see the a11y block */
  /* status — use only these six, never invent a seventh */
  --green: #22c55e; --red: #ef4444; --amber: #f59e0b;
  --cyan: #06b6d4; --purple: #8b5cf6; --purple-dark: #7c3aed;
  /* type */
  --font: 'Inter', 'Sarabun', -apple-system, BlinkMacSystemFont, sans-serif;
  --mono: 'JetBrains Mono', 'Fira Code', 'Sarabun', monospace;
  /* form */
  --radius: 12px; --radius-sm: 8px; --radius-lg: 16px;
  --measure: 720px; --wide: 860px;
  --transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
```

Verify it is still uniform before and after any edit:

```bash
diff <(awk '/^    :root \{/,/^    \}/' .claude/skills/page-design/assets/post-template.html | sed 's/^ *//') \
     <(awk '/^:root \{/,/^\}/' style.css | sed 's/^ *//')      # → no output
```

The three pure aliases this section used to list for deletion — `--indigo`, `--muted`, `--violet` —
are **gone** (0 occurrences). What is left off-canon is 7 genuine extras (`--emerald`,
`--emerald-dark`, `--orange`, `--sky`, `--teal`, `--teal2`, `--purple-light`) plus 5 legitimate
namespaced brand tokens; `references/tokens.md` §3–§4 has the fold-in table. `--teal2` is **not**
an alias — it is a second teal value.

**`--radius` is `12px`, not `14px`.**
`grep -ho 'border-radius: *[0-9]*px' index.html style.css blog/*.html books/*.html news/index.html projects/index.html publications/index.html | tr -d ' ' | sort | uniq -c | sort -rn`
→ `169 12px`, `96 8px`, `83 10px`, `58 2px`, `54 6px`, `40 20px`, `30 16px`, … `5 14px`. Use
12 / 8 / 16; keep `20px`–`50px` pills for tags and chips only. The 58 `2px` hits are almost all the
`:focus-visible` ring — do not consolidate them.

**`--radius` is now correct in all 47 blocks, and CLAUDE.md was finally corrected in `5a522ed`** —
the `--radius: 14px` line this paragraph used to flag is gone. Anti-pattern 11 keeps the story.

**The remaining token gap is consumption, not declaration.** `--measure` is declared 47 times and
used `var(--measure)` only **14** times (all on the 2026-08 section pages) — `max-width:720px` is
still written as a literal 76 times.
Same story for `--wide` (1 use vs 26 literals) and `--radius-lg` (1 vs 30). Nothing renders wrong;
it just means "change the measure" is still an N-file edit. Write `var()` in new code (the template
does); convert existing files opportunistically, not as a scheduled sweep. `references/tokens.md` §2.

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

The work is not redesign, it is **extension to the 11 island files**. The 5 LISTING pages and the
3 DETAIL pages are
`16px` / `1.7` and that is deliberate and uniform across all eight — leave it. Font stacks to retire
when you convert an island file: `'SF Pro Display', …`
(×3), `'Segoe UI', Tahoma, Geneva, Verdana` (×1), bare `-apple-system, …` (×4),
`'Inter', 'Noto Sans Thai', system-ui` (×1), and
`'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif` (×1,
`openclaw-production` — names Inter but never loads it, see anti-pattern 9).

---

## 3. Layout constants — always pick the incumbent

| Constant | Value | Uses today |
|---|---|---|
| reading measure (`.post-body`) | **720px** | 76 |
| wide container (`.blog-nav__inner`) | **860px** | 26 |
| listing/detail container (5 LISTING + 3 DETAIL) | **1200px** | 31 |
| hero cover box | **380px** max-width (13 of 25), border-radius 16px = `--radius-lg` (25/25) | retire 420/480/520/560 |
| listing card image | `.card__image`: width 100%; aspect-ratio 16/10 | `grep -n 'card__image' blog/index.html` |
| tablet breakpoint | **768px** | 26 (24 spaced + 2 unspaced) |
| phone breakpoint | **600px** | 30 |
| island-chrome nav takeover | **800px** | 10 — the 5 LISTING + 4 DETAIL pages + `404.html`, nav rules only (`5178252`) |
| landing nav takeover | **1080px** | 1 — `style.css` only (`5178252`) |
| wide breakpoint | **1024px** | 1 — `style.css`, landing grids only |
| retire | `480px` (2), `500px` (1) | fold into 600px |

```bash
grep -ho '@media[^{]*' index.html style.css 404.html blog/*.html books/*.html news/index.html projects/index.html publications/index.html \
  | sed 's/[[:space:]]*$//' | sort | uniq -c | sort -rn
```
→ `48 (prefers-reduced-motion: reduce)`, `30 (max-width: 600px)`, `24 (max-width: 768px)`,
`10 (max-width: 800px)`, `2 (max-width:768px)`, `2 480px`, `1 500px`, `1 1080px`, `1 1024px`.
Two of the 768px hits are unspaced (`max-width:768px`) — match the spaced form in new code so
grep-based sweeps find them. The 48 reduced-motion blocks are the `e8da9da` a11y sweep (47
embedded `<style>` blocks + `style.css`, `404.html` included); they are not layout breakpoints. The 9 `800px` blocks
are the island-chrome mobile-nav takeover (9 section pages + `404.html`) and the 1 `1080px` block is `style.css`'s — the desktop
bar with the 6-link nav last fits at 772px on the island-chrome pages, so 768px left a broken
769–771px band (`5178252`); keep the takeover block byte-identical across all 9 pages.

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
Chrome     .blog-nav  .blog-nav__inner  .blog-nav__back  .blog-nav__title      (posts)
           .nav  .nav__inner  .nav__logo  .nav__links  .nav__right  .nav__cta
           .nav__divider  .nav__toggle  .nav__burger                (LISTING pages
                                          + index.html; .nav__toggle/.nav__burger
                                          are the pure-CSS mobile menu — never JS)
Header     .post-hero  .post-hero__tags  .post-hero__tag  .post-hero__title
           .post-hero__meta  .post-hero__series  .post-hero__cover
Body       .post-body                       (max-width: var(--measure))
Footers    .post-series-footer  .post-nav  .series-nav
Listing    .card  .card__image|__body|__tags|__tag|__title|__excerpt|__footer|__author|__read
           .card__image--pair               (dual-jacket plate — every card on books/index.html
                                          since the 2026-08-24 dual-cover sweep; 7daf3a4 introduced it)
           .blog-grid  .series-section  .series-header  .series-header__left
           .series-title  .series-icon  .series-description  .series-count
           .category  .category__header  .category__icon  .category__title
           .category__count  .category__note              (Task 11, 635eb94)
           .latest  .latest__inner  .latest__heading  .latest__list  .latest__date
                                                        (Task 10, d4b94b5)
Content    .callout  .callout--info|--warn|--good|--bad    [defined in the template — 0 uses]
           .compare  .compare__col  .compare__col--old|--new  [defined — 0 uses]
           .figure  .figure__img  .figure__caption          [live since ea3c8e8 — the 4
                                          books/ DETAIL pages use it for their cover figure]
           .figure--qr                 (reservation QR, books/one-day-of-light.html #event)
Code       <pre><code>                      (never .code-block)
```

**`.category*` is the outer band, `.series*` is the inner group.** Task 11 (`635eb94`) re-cut
`blog/index.html` into 3 `.category` bands (`#cat-technology`, `#cat-academic`, `#cat-lifestyle`)
holding 2 `.series-section`s, and gave the page a real heading ladder:
`h1` page title → `h2` ×3 `.category__title` → `h3` ×2 `.series-title` → `h4` ×37 `.card__title`.

```bash
python3 -c "import re,collections; s=open('blog/index.html').read(); print(collections.Counter(int(m.group(1)) for m in re.finditer(r'<h([1-6])\b[^>]*>', s)))"
# → Counter({4: 37, 2: 3, 3: 2, 1: 1})
```

**Card titles are `h4`.** They were `h2` before Task 11. Anything that greps for
`<h2 class="card__title">` is matching 0 of 37 — write `<h[1-6] class="card__title">` and let the
backreference close it. `verify-wiring.py` was blind for exactly this reason until 2026-08-10.

**Empty `.category` bands are forbidden** since 2026-08-26: `check_site.py` INV-02d fails on any
band with 0 cards. The two placeholders (`#cat-academic`, `#cat-lifestyle`) and the hero's
"N Categories" stat were deleted together — they had advertised categories the blog did not have
for 16 days, with nothing able to expire them. A new category ships its band, grid, card and count
in one commit. INV-02e still verifies the Categories stat **if** one is present.

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
`card__tags`, `card__title`, `card__excerpt`, `card__footer`, `card__author`, `card__read`).
Sitewide the `.card` vocabulary is now `card` ×70 (37 in `blog/index.html`, 9 in
`publications/index.html`, 8 in `news/index.html`, 7 in `projects/index.html`, 5 in
`books/index.html` — 4 cards plus the counters-gate comment that quotes the pattern — and
1 on each of the 4 books/ detail pages), `card__tag` ×163, `card__title` ×57.
`style.css` follows the same convention (`.btn--pill`, `.hero__label--bold`). Follow that.

---

## 5. Hero gradients — five approved, pick by series

Today there are **77 distinct `linear-gradient(135deg, …)` values across 138 occurrences**, and 17
distinct `.post-hero` gradients across 26 house posts. This is the noisiest thing on the site.

| Family | Gradient | Use for |
|---|---|---|
| Default / light | `linear-gradient(135deg, #eef3f3 0%, #dee7e6 50%, #e9e1c4 100%)` — the sunrise | DevOps fundamentals |
| Indigo deep → **Deep blue** | `linear-gradient(135deg, #11304b 0%, #1a4d7a 45%, #226299 100%)` | security / auth; the `publications/` hero |
| Violet | `linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%)` | OpenClaw series |
| Emerald | `linear-gradient(135deg, #052e16 0%, #064e3b 40%, #065f46 100%)` | testing / quality; the Books section identity — all 5 `books/` pages (index + 4 detail) |
| Teal | `linear-gradient(135deg, #134e4a 0%, #115e59 40%, #0f766e 100%)` | SRE / observability |

The default is the plurality at **11 uses** (Emerald is next at 7 — 2 posts + the 5 `books/`
pages), and the `40%`-stop fork `blog/index.html` used to
carry was fixed by `b9fb125`. Verify it has not come back:
`grep -ho 'linear-gradient(135deg, *#eef3f3[^)]*)' index.html blog/*.html books/*.html news/index.html projects/index.html publications/index.html | sort | uniq -c`
→ **one row**, all `50%`. Two rows means someone forked it again. (The 2026-08-26 re-key mapped
every retired hue through `scripts/retoken.py`; two gradients whose stops would have collapsed into
a dead flat band were replaced whole and are listed in that script's `WHOLE_STRINGS`.)

**Never hand-pick a sixth.** Retire the one-offs when you touch their file: `#0c1929…`
(docker-compose), `#0d1117…` (github-actions), `#1a0533…` (gitops), `#0369a1…` (cloud), `#0891b2…`
(deployment), `#059669…` (idle), `#2563eb…` (migration), `#4f46e5…#06b6d4` (vibe-coding).

---

## 6. Modern CSS — ranked by ROI, with verdicts

The honest ranking here is lopsided. **Images dominated every CSS technique combined — and that
work is now done.** Items 1 and 3–6 below shipped in `ec2827b`/`21c8a55` and `e8da9da`. They are
kept here as *the standard to hold*, not as a plan. Re-verify before you act on any of it.

### DONE — hold the line, do not re-plan

**1. Image loading — LANDED.** `blog/index.html` now references **2.23 MB across 48 unique
images** over 74 `<img>` tags, and **all 74 carry `loading="lazy"`**, so the HTML-only first byte
cost is 67 KB and a first desktop viewport (first ~10 cards) fetches ≈1.7 MB, not 18.4 MB.
Sitewide, **137 of 137 `<img>` tags have all four of `loading`, `decoding`, `width`, `height`**
(42 also carry `fetchpriority`; 95 are lazy, 42 eager).

```bash
python3 - <<'PY'
import re, pathlib
n=ok=0
for p in pathlib.Path('.').rglob('*.html'):
    if '.claude' in p.parts or '.git' in p.parts: continue
    for m in re.finditer(r'<img\b[^>]*>', p.read_text(encoding='utf-8'), re.S):
        n+=1; ok+= all(a+'=' in m.group(0) for a in ('loading','decoding','width','height'))
print(ok, "/", n)     # → 137 / 137
PY
```

A line-based `grep -oh "<img[^>]*>"` reports **120** here — it drops the seventeen `<img>` written
across multiple lines (all on the books/publications pages: 8 in `books/index.html`,
2 on each of the 4 `books/` detail pages, 1 in `publications/index.html`). Use the
multiline parse above;
a seventeen-tag discrepancy is exactly the kind of thing that
makes a reader distrust the whole file.

```html
<img src="../images/api-lifecycle-cover.jpg" alt="API Request Lifecycle — cute dog illustration"
     width="1600" height="900" loading="lazy" decoding="async">
```

Above-the-fold hero covers get `loading="eager" fetchpriority="high"` instead.

**3–6. `:focus-visible`, `prefers-reduced-motion`, `color-scheme: light`, `text-wrap: balance` —
ALL LANDED** in `e8da9da`, as one 4-line block, now in **47 embedded `<style>` blocks +
`style.css`**
= complete 48/48 page coverage (the 2026-08 books/publications pages, `books/one-day-of-light.html`
and `404.html` all shipped with it).
`index.html` is the one HTML file without the block in its own
source, correctly, because it has no `<style>` block at all.

```bash
grep -L ':focus-visible' style.css 404.html blog/*.html books/*.html news/index.html projects/index.html publications/index.html  # → empty
grep -c ':focus-visible' style.css                                                                   # → 2
```

`script.js:12` carries the `matchMedia('(prefers-reduced-motion: reduce)')` guard for the
scroll-driven work the CSS block cannot reach.

**Corollary the old text got wrong:** `outline: none` **is** now declared, 47 times, as
`:focus:not(:focus-visible) { outline: none; }`. That is correct and deliberate — it suppresses the
UA ring only for mouse/programmatic focus, never for keyboard. Do not "fix" it, and do not cite it
as evidence of a focus failure.

### ADOPT NOW

**2. `aspect-ratio` on `.post-hero__cover`** — the one image item still partly open. `.card__image`
has it (`16/10`), and 26 blog files now declare `aspect-ratio` somewhere, but not every one of the
25 `.post-hero__cover` rules reserves a box. Add `aspect-ratio: 16 / 9` plus
`object-fit: cover` on the child `img` when you are in the file; the template already does.

**7. `clamp()` fluid type** — the mechanism in the 26 house posts, the 5 listing pages, the 4
detail pages and
`style.css`. The post-title value is canonical (`clamp(1.8rem, 5vw, 3rem)`, 26/26 house files).
Extend to the 11 island files; do not redesign either scale (§2).

The block that shipped, verbatim — **keep it byte-identical** so a grep sweep still finds it:

```css
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

**Proving the sweep landed — `index.html` is not like the other 46 files.** Every `blog/*.html`
post, `blog/index.html`, the five `books/*.html` pages, `projects/index.html`, `news/index.html`,
`publications/index.html` and
`style.css` itself embed or *are* their own CSS, so a per-file `<style>`-block grep proves coverage
for each of them directly:

```bash
grep -L ':focus-visible' style.css blog/*.html books/*.html projects/index.html news/index.html publications/index.html   # → empty
```

`index.html` is the one page whose CSS lives entirely in `style.css` via
`<link rel="stylesheet" href="style.css">` — it has **zero** embedded `<style>` blocks by design,
an explicit requirement since Task 10. **Use `grep -c '</style>' index.html` → `0`, not
`grep -c '<style'`**: since `7867c00` the file carries a comment reading "index.html deliberately
has no `<style>` block of its own", so the opening-tag grep returns `1` and looks like a violation
of the very rule the comment states. Closing tags cannot appear in that prose. Running
the same per-file grep against `index.html` and expecting a hit is checking the wrong file: it will
always report `index.html` as "missing" the snippet even when coverage is real, and the tempting
fix — pasting a duplicate `<style>` block into `index.html` just to make the grep pass — is wrong.
It was tried once (Task 12, first pass) and reverted: the block was byte-for-byte identical to text
already in `style.css`, added zero coverage, was pure drift risk, and violated the "index.html has
no embedded style" invariant for no benefit. When a proof and the goal disagree, fix the proof, not
the file.

The correct check for `index.html`'s coverage is against `style.css`, plus a browser check that the
cascade actually reaches the page (custom properties and `:focus-visible` both apply document-wide
regardless of which linked/embedded sheet declared them):

```bash
grep -c '</style>' index.html      # → 0  (must stay 0 — Task 10, and anti-pattern 2)
grep -c ':focus-visible' style.css # → 2
grep -c 'color-scheme' style.css   # → 1
grep -c 'text-wrap' style.css      # → 1
```
Then in a real browser on `index.html`: tab once and confirm a visible focus ring, and confirm
`getComputedStyle(document.documentElement).getPropertyValue('--blue')` resolves — both prove the
`style.css` link is doing its job, which a text grep on `index.html` itself cannot show.

### LATER — blocked, not declined

- **`prefers-color-scheme` dark mode.** Genuinely worth having, but with per-file CSS it means 47
  hand-maintained dark palettes plus dark variants of 77 gradients, and the light-lavender hero has
  no dark analogue. **The §1 blocker is cleared** — the tokens landed in all files in `6670480`,
  and `color-scheme: light` is declared in all 47, so a dark block now has a single well-defined
  place to go and a single set of names to redefine. This is the largest remaining design project
  and it is now genuinely unblocked, not merely deferred. Scope it as one `@media` block per file,
  written once and pasted, exactly like `e8da9da` did.
- **`color-mix()`.** Would collapse ~30 one-off tint gradients (`#eff6ff`, `#ecfdf5`, `#fefce8` …)
  into derivations of `--blue` / `--green` / `--amber`. Excellent second pass, after tokens.

### NOT NOW

- **`content-visibility: auto`.** Long posts exist (`web-architecture.html` 91 KB,
  `frontend-performance.html` 69 KB) but `.post-body` has no section children to apply it to. The
  image bottleneck that used to dwarf it is gone (18.4 MB → 4.07 MB → 2.23 MB referenced, all lazy), so this
  is now merely small rather than irrelevant. Revisit only if posts get sectioned.

### NEVER — with reasons

- **CSS nesting.** This repo is maintained by grepping and find-replacing *flat* selectors across 47
  files. There is no build step to flatten nesting. §7 shows how easily cross-file edits already
  drift; nesting would make every sweep measurably harder. Actively harmful here.
- **Logical properties** (`margin-inline`, `padding-block`). Zero adoption today; both site languages
  (English, Thai) are LTR. Buys nothing, costs a rewrite of every margin and padding in 47 files.
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
   (13 files, 66 uses) is also deliberate and worth keeping.

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

4. **Never reuse a cover image.** Fixed 2026-08-26 by the drawn-cover system (`1103b7a`): every
   card on the listing now resolves to its own cover. Until then 37 cards shared only 35 —
   `../images/github-actions-cover.jpg` was double-booked by `vibe-coding-devops-process.html` and
   `github-actions.html`, `../images/monitoring-cover.jpg` by `openclaw-memory-architecture.html`
   and `monitoring-observability.html`, and the pairs were indistinguishable on the listing.
   `check_site.py` INV-07a carries no baseline entry and fails the build on any new sharing. The fix
   for a future collision is a new image, not a re-point.

5. **Never commit a cover over ~200 KB, and never as PNG. This is now clean — keep it clean.**
   `ec2827b` + `21c8a55` re-encoded every PNG cover to JPG at `formatOptions 70`. Today:
   **46 JPG covers (38 `*-cover.jpg` + 8 suffixed), 0 PNG covers, average 51 KB, largest 174 KB,
   zero over 200 KB** (the eight paired book faces — `three-old-men-cover-front/-back` 175 / 120 KB,
   `a-pocketful-of-questions-cover-en/-th` 73 / 77 KB, `the-thirteenth-seal-cover-en/-th` 54 / 62 KB,
   `one-day-of-light-cover-en/-th` 67 KB each — all comply; the `*-cover.jpg` glob alone reports
   36 jpg, avg 112 KB, so add `images/*-cover-*.jpg` to any cover census).

   ```bash
   ls images/*-cover.png 2>/dev/null | wc -l                                   # → 0
   find images -name '*-cover.*' -size +200k                                   # → nothing
   ls -l images/*-cover.jpg | awk '{s+=$5;n++} END {print n" jpg, avg "int(s/n/1024)" KB"}'
   ```

   Photographic / AI-generated covers are JPG at ≤1600px wide. PNG survives for **flat art
   only**: the 5 diagram images (`*-arch.png`, `*-flow.png`, `*-levels.png`, 123–235 KB) and the
   884-byte registration QR (`one-day-of-light-qr.png`) — those are correctly PNG and must not be
   converted; a q70 JPEG smears their lines (and would break the QR's modules).

6. **Never add a post without recomputing every counter in `blog/index.html`.** They were all
   stale; `b9fb125` fixed them and Task 11 added two more sites. **All five are correct today** and
   `check_site.py` INV-02a–INV-02e all PASS — so any drift you see is drift you introduced.

   | Counter | Value today |
   |---|---|
   | `.blog-hero__stat` "N Categories" | 3 |
   | `.blog-hero__stat` "N Series" | 2 |
   | `.blog-hero__stat` "N Articles" | 37 |
   | `.category__count` `#cat-technology` | 37 articles |
   | `.series-count` `#series-openclaw` / `#series-devops` | 13 / 24 |

   Recompute, never increment — incrementing by hand is how all of them went stale. Never cite line
   numbers for these; they have moved twice. Grep for the class.

7. **Never invent a token name for a value that already has one.** `--indigo` == `--blue`,
   `--muted` == `--slate-light`, `--violet` == `--purple-dark`. (`--teal2` is *not* an alias — it
   is a second teal value; see `references/tokens.md` §2.) Check `references/tokens.md` before
   adding anything.

8. **Never hand-pick a new hero gradient.** 78 already exist. Choose from the five in §5.

9. **Never name a font the page does not load.** `blog/openclaw-production.html` and
   `blog/openclaw-security.html` both declare `'Inter'` in `font-family` with no Google Fonts
   `<link>` and no `preconnect` — they silently render in a system font while claiming the house
   typeface. All 10 pure island files lack both tags.

10. **Never link an absolute route that does not exist. Now clean — keep it clean.** `b9fb125`
    removed the 14 dead absolute links (`/about`, `/research`, `/contact`, `/teaching`,
    `../about/`), and Task 8 gave `/projects` a real page. Every one of those five routes is now
    linked from **0** files, and `check_site.py` INV-05 ("every relative/site-absolute href resolves
    on disk") PASSes with 0 violations. Extensionless `/blog/openclaw-*` links **are** fine — GitHub
    Pages resolves them to `.html`, all 7 targets exist, and INV-09 checks it.

    ```bash
    python3 .claude/skills/site-check/scripts/check_site.py | grep 'INV-05 \|INV-09'
    ```

11. **Never let CLAUDE.md drift.** Re-checked 2026-08-23 — the three claims this entry used to
    track are all fixed now (`5a522ed` rewrote CLAUDE.md against the shipped implementation):
    the `--radius: 14px` line is gone (real value `12px`, 169 uses vs 5, declared in 47 of 47
    `:root` blocks), the CSS-variables advice correctly points at the canonical set, and "category
    filters" now reads "3 category bands … no client-side JS". The lesson stands: CLAUDE.md is
    hand-maintained prose about a hand-maintained site, and it goes stale the moment a sweep lands
    without touching it.

    This entry is also the reason for the standing rule at the top of this file.

12. **Never add JavaScript to `blog/index.html`.** `grep -c '<script' blog/index.html` → `0`. That
    is a feature worth defending. Any filtering must work without JS or not ship.

13. **Cap emoji in headings at roughly one per section, and never in `<h2>`.** Today it ranges from
    57-of-65 headings (`openclaw-skills.html`) and 53-of-55 (`openclaw-memory.html`) down to zero in
    7 files (claude-code-architecture, docker-vs-vms, git-branching, kubernetes-orchestration,
    linux-command-line, monitoring-observability, networking-fundamentals). Posts sitting side by
    side in the same series read as different websites.

14. **Never regress alt text or image attributes.** **137 of 137** `<img>` have `alt`, and since
    `e8da9da` all carry `loading`, `decoding`, `width` and `height` too. Two complete
    sitewide practices — the only two. Protect both. (Alt *quality* is still uneven: 4 alts end in
    the word "Cover" and 37 avatars repeat `alt="Anirach"`; see a11y-perf R6.)

---

## 8. Adoption order — where the plan actually stands

Phases 1–3 **shipped** between `6670480` and `e8da9da`. They are recorded here as history so nobody
re-plans them; the only live work is Phase 4 and the short "still open" list below.

| Phase | What it was | Status |
|---|---|---|
| 1 — tokens | canonical `:root` in every file, aliases deleted, `--radius: 12px` | **DONE** `6670480`, `36d9814`. 47/47 blocks today, 0 deviations. CLAUDE.md's `14px` line is fixed too (`5a522ed`). |
| 2 — images + counters + routes | JPG covers, `loading`/`decoding`/`width`/`height`, counters, dead routes, hero-gradient fork | **DONE** `ec2827b`, `21c8a55`, `b9fb125`. 137/137 images attributed today; 0 PNG covers; all 5 counters correct; 0 dead absolute links. |
| 3 — modern polish | `:focus-visible`, `prefers-reduced-motion` (+ `script.js` guard), `color-scheme`, `text-wrap`, `aspect-ratio` | **DONE** `e8da9da`. 41 embedded blocks + `style.css`. |
| 4 — structural | island → HOUSE conversion, vocabulary collapse, shared stylesheet, dark mode | **OPEN — the only live phase.** |

**Still open from Phases 1–3, small and specific:**

- `var(--measure)` / `var(--wide)` / `var(--radius-lg)` are declared but barely consumed (§1) —
  though the 2026-08 section pages started consuming `var(--measure)` (10 uses now).
- `aspect-ratio` is not on every `.post-hero__cover` (§6 item 2).
- Contrast: `.post-hero__meta` is still `rgba(255,255,255,0.6)` in 15 files and
  `.post-series-footer` is still `var(--gray)` in 22 — see the a11y-perf skill, R3/R4. The a11y
  *infrastructure* landed; the *palette* corrections did not.

**Phase 4 — structural, genuinely optional.** Convert `obsidian-ai-jarvis.html` first: it already
has house tokens, Inter, `clamp()` and `17px`/`1.8`, and only needs `.nav`→`.blog-nav`,
`.container` 800px → `.post-hero`/`.post-body` 720px, and `.code-block`→`<pre>`. It is ~80% done and
is the cheapest possible proof that the recipe works. Then the 10 island posts. Then collapse the
callout and card vocabularies. **Only then** consider a shared stylesheet, and after that, dark mode
— which §6 now lists as unblocked rather than deferred.

A partial migration is not a failure. Phases 2 and 3 are where the site visibly became nice, modern
and tidy; Phase 4 is housekeeping.

---

## 9. What is already right — do not "improve" it

Leave these alone unless the user explicitly asks:

- the heading scale (`h2` 1.6rem 24/24, `h3` 1.25rem 24/24, hero `clamp(1.8rem, 5vw, 3rem)` ×26)
- the 720px measure (76 uses) and the 860px wide container (26 uses)
- the BEM naming in `style.css` and in `blog/index.html`'s `.card`
- the glassy nav: `background: rgba(248,250,252,0.85); backdrop-filter: blur(20px)`
- the `/* ── SECTION ── */` CSS comment convention (13 files, 66 uses)
- the canonical 24-token `:root`, byte-identical in 47/47 blocks (`references/tokens.md`)
- the 4-line a11y block (`:focus-visible`, reduced-motion, `color-scheme`, `text-wrap`) in 46
  embedded `<style>` blocks + `style.css` — including its `outline: none`, which is scoped to
  `:focus:not(:focus-visible)` and is correct
- image attributes: 137/137 `<img>` carry `alt`, `loading`, `decoding`, `width` and `height`
- cover budget: 44 JPG covers (36 + 8 suffixed), 0 PNG, avg 107 KB, max 194 KB, none over 200 KB
- `<meta name="viewport">` on 47/47 files
- `blog/index.html` has 0 `<script>` tags — a feature, not an omission (anti-pattern 12)

**Social metadata landed 2026-08-26 — hold this line too.** All **47** enumerated pages carry a
`<!-- social -->` … `<!-- /social -->` block (canonical, `og:*`, `twitter:card`, icons,
`theme-color`, `robots`), and all 47 now carry a `<meta name="description">` — the 6 that lacked
one are fixed and their INV-14 baseline entries are deleted. `check_site.py` **INV-27** (FAIL
severity) recomputes the canonical path from each file's location and reads real pixel dimensions
out of the JPEG/PNG header, so a wrong `og:url` or a stale `og:image:width` fails the build.
`404.html` is deliberately outside all of this: noindex, no social block, not in `sitemap.xml`.

Do not hand-edit a social block — regenerate it, and never point `og:image` at a diagram PNG or a
square cover with `summary_large_image` (half the image is cropped). The 9 share cards in
`images/` (`og-site-card.jpg`, `og-publications.jpg`, four `<book>-og.jpg` diptychs, three
`<post>-og.jpg`) are all 1200×630 and are matched by neither the `*-cover.jpg` nor the
`*-cover-*.jpg` census glob — add `images/*-og.jpg images/og-*.jpg` when counting them.

Genuinely missing sitewide, if the user wants more: dark mode (§6). The two double-booked hero
covers of anti-pattern 4 were fixed 2026-08-26 by the drawn-cover system, so the listing page no
longer shows any identical pair.

---

## Files in this skill

| File | Open it when |
|---|---|
| `references/tokens.md` | adding/changing any colour, radius, or token; doing a Phase 1 sweep |
| `references/components.md` | writing markup for a nav, hero, callout, card, figure, or code block |
| `assets/post-template.html` | creating a new blog post — copy this, do not hand-roll. **It is the only post template in the repo**; `blog-post/assets/post-template.html` was a duplicate that rotted three sweeps behind and was deleted (see `blog-post/assets/TEMPLATE-MOVED.md`). |

Numbers in this skill were last re-measured against `7daf3a4` on **2026-08-24** (One Day of
Light joined `books/`: 47 files, 5 LISTING + 4 DETAIL, 800px/1080px nav takeovers). If you are
reading
this after a sitewide sweep whose commit is not named above, re-run the commands before trusting
any count — and then update them here, per the standing rule at the top.
