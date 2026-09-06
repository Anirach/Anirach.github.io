---
name: page-design
description: The house visual system for anirach.com (this repo) — canonical :root tokens, type scale, layout constants, component vocabulary, breakpoints, modern-CSS verdicts, and the anti-patterns this repo has already been burned by. Use this whenever you create, restyle, or even lightly touch any HTML/CSS in this repository — a new blog post in blog/, a new section on index.html, a tweak to style.css, a nav or hero or callout or card, a diagram, a cover image, or a sweep across many files. Use it even if the user does not say "design", "style", or "CSS" — requests like "add a post about X", "make this look better", "fix the spacing", "add a diagram", "clean this up", "make it modern" all land here. Read it BEFORE writing markup, because the first question is always "is this file HOUSE, LISTING or DETAIL?" and getting that wrong produces an 87-file inconsistency that is expensive to undo.
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

This looks like 76 hand-written blog posts that must be uniformly messy. It is not. It is **three
self-consistent families**, and every design decision starts by classifying the file you are about
to touch.

```
87 HTML files
  = index.html            (landing — the only page with no embedded <style>;
                           its CSS is all style.css. It is NOT the "only page with
                           a <script>": there is no executable script anywhere —
                           see "Zero JavaScript" in CLAUDE.md and INV-38.)
  + 5 LISTING pages       blog/index.html, books/index.html, news/index.html,
                           projects/index.html, publications/index.html
                                                — .nav chrome, 16px/1.7, 1200px
  + 404.html              (root; LISTING chrome and type, but NOT a section index —
                           it is noindex, carries no social block, and is excluded
                           from sitemap.xml. check_site.py does not enumerate it,
                           which is why the enumerated total is 86 against a tree of
                           87.)
  + 4 DETAIL pages        books/three-old-men.html, books/a-pocketful-of-questions.html,
                           books/the-thirteenth-seal.html, books/one-day-of-light.html
                           — same .nav chrome and type
                           as LISTING, one subject per page, carded from books/index.html
                           (check_site.py INV-26 enforces that link)
  + 76 posts in blog/     = 76 HOUSE. All of them. The ISLAND family is retired
                           (662e966, "Phase 3: convert the 11 island posts to house
                           chrome, content preserved"); obsidian-ai-jarvis is no
                           longer a hybrid either.
```

```bash
find . -name '*.html' -not -path './.git/*' -not -path './.claude/*' \
     -not -path './.bilingual/*' | wc -l                                  # → 87
ls blog/*.html | wc -l                                                    # → 77 (76 posts + index)
for f in blog/*.html; do grep -q 'class="blog-nav"' "$f" || basename "$f"; done # → index.html only
```

That last command used to print 12 names. It now prints exactly one, `blog/index.html`, which is a
LISTING page and correctly wears `.nav` — so **there are 0 island posts**. Every claim below that
reads "convert the island files" is finished history, not a plan.

**The LISTING family is new** (Task 8, commits `fd63657` / `3f3d049` / `5447407`; `publications/`
split out of `books/` on 2026-08-23, `a648a85`) and it is
internally consistent: all five pages use `.nav` / `.nav__inner` / `.nav__links` / `.nav__logo` /
`.nav__right`, `16px`/`1.7` body type, a `max-width: 1200px` container, one `clamp()` hero title,
and the pure-CSS `.nav__toggle` checkbox + `.nav__burger` label mobile menu (takeover at **800px**
since `5178252`, byte-identical across all 9 section-chrome pages — the 5 listing + 4 detail;
`404.html` carries the same block, which is why the 800px count is 10).
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

| Axis | HOUSE (76 posts) | LISTING (5) + DETAIL (4) + 404 |
|---|---|---|
| `:root` tokens | yes 76/76 | yes 10/10 |
| `:focus-visible` + reduced-motion + `color-scheme` + `text-wrap` | yes 76/76 | yes 10/10 |
| Google Fonts + preconnect | yes 76/76 | yes |
| `clamp()` | yes 76/76 | yes (one hero title each) |
| `.post-hero` / `.post-body` | yes 76/76 | no — `.container` 1200px |
| nav | `<nav class="blog-nav">` 76/76 | `.nav` + the `.nav__toggle` checkbox menu |
| code | `<pre>` — `class="code-block"` is at **0** occurrences sitewide | — |
| body type | `17px` / `1.8` (74/76) | `16px` / `1.7` |
| measure | `.post-body` 720px (74/76) — 760px in openclaw-memory-architecture + vibe-coding-devops-process | 1200px |

**The island/house gap is closed.** Three sweeps did it: the canonical `:root` (`6670480`), the
a11y block (`e8da9da`), and finally `662e966` "Phase 3: convert the 11 island posts to house
chrome, content preserved", which took the last 11 files' chrome and typography. The measurements
that used to distinguish the families now all read the same:

```bash
grep -l 'class="code-block"' blog/*.html | wc -l   # → 0
grep -L 'fonts.googleapis.com' blog/*.html          # → empty
grep -L 'Sarabun' blog/*.html                       # → empty
```

The three retired font stacks (`'SF Pro Display'`, `'Segoe UI'`, `'Noto Sans Thai'`) are at **0
files each**. Anti-pattern 9 — "never name a font the page does not load" — is satisfied
everywhere; it stays on the list as a rule, not as a backlog item.

**HOUSE deviations: two, and only two.** `openclaw-memory-architecture.html` and
`vibe-coding-devops-process.html` (both minified) use `.post-body{max-width:760px}`, declare no
`.post-body h2/h3/h4` rules, and are the 2 files with no `font-size: 17px`. All 74 others match
exactly. One further single-file drift: `obsidian-ai-jarvis.html` sets `.post-body h2` to `1.7rem`
and `h3` to `1.3rem` where the house says 1.6/1.25 — snap it on contact.

### The rule this implies

- **Touching a post?** Copy the pattern from its neighbour *in the same series*.
  `blog/api-request-lifecycle.html` is the cleanest DevOps reference; `blog/hermes-101.html` is the
  reference `build_series.py` itself reads at run time for the Deep Blue `<style>` block, and
  `blog/morning-waking.html` is the Sunrise one. Do not invent. Do not "improve" the shared parts;
  you will fork them (see §7 nav drift).
- **Creating a new post?** It is HOUSE, always — there is no other option left. Copy
  `assets/post-template.html`, the **only** post template in this repo
  (`blog-post/assets/post-template.html` was a second copy; it rotted three sweeps behind and was
  deleted — see `blog-post/assets/TEMPLATE-MOVED.md`). It was itself several sweeps behind until
  2026-09-06 and now carries the current skeleton: the skip link, `<main id="main">`,
  `.blog-nav__home`, `.blog-footer__nav`, the paired `.post-toc` `<details>`, the TH ⇄ EN
  apparatus (`lang-switch-box`, `.l-th`/`.l-en`) and a re-keyed 29-token `:root`.

  **Verify before you trust it**, because the template is hand-maintained and this is exactly the
  failure it has already had once:

  ```bash
  T=.claude/skills/page-design/assets/post-template.html
  for k in skip-link 'id="main"' lang-switch-box l-en post-toc blog-nav__home blog-footer__nav; do
    printf '%-18s %s\n' "$k" "$(grep -c "$k" $T)"; done      # every row must be non-zero
  diff <(awk '/^    :root \{/,/^    \}/' $T | sed 's/^ *//' | sed 's|/\*.*\*/||' \
           | grep -o -- '--[a-z-]*: *[^;]*;' | sort) \
       <(awk '/^:root \{/,/^\}/' style.css | sed 's/^ *//' | sed 's|/\*.*\*/||' \
           | grep -o -- '--[a-z-]*: *[^;]*;' | sort)          # → no output
  ```

  A post missing those pieces fails INV-29 (home link + footer nav), INV-30 (skip link + `#main`)
  and `check_visibility.py` S1 (bilingual). If any row above is 0, copy a sibling post in the
  target series instead and fix the template in the same commit.
- **Adding a 21st AI Transformation post?** That series is **generated**. Do not hand-write the
  file and do not hand-edit twenty grouped chip strips — see §4 and the recipe at the end of §7
  item 6.

Because every file embeds its own `<style>`, a "global" change means editing N files by hand.
That is the architecture, not a bug — see anti-pattern 2 before you reach for a shared stylesheet.

---

## 1. The canonical `:root` — already landed, keep it byte-identical

**This sweep is finished, and it has held through four content waves since.** `6670480` put the
block below into every file, `36d9814` fixed its one bad target, `1fca25e` re-keyed the values to
the book covers, and the 37-post bilingual conversion and the 20-post AI Transformation launch
both shipped clean. Re-measured today: **87 `:root` blocks across 88 files** (`index.html`,
`style.css`, `404.html`, the 77 `blog/`, the 5 `books/`, and news/projects/publications), every one
declaring the same **29** tokens with **zero value deviations** — every token reads `×87`.
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
  /* brand — sampled from the book covers (2026-08-26 re-key). --gold is decorative
     on light grounds (2.2:1); --gold-dark is its text form. */
  --gold: #c4a46c; --gold-dark: #7a5f22; --cloud: #dee7e6; --parchment: #e9e1c4;
  --focus: #226299;   /* footers and <pre> re-point this to --gold; see the a11y block */
  /* status — use only these six, never invent a seventh.
     --purple/--purple-dark were re-pointed to the blues by the 2026-08-26 re-key
     ("the end of violet", d44adb9) — the NAMES survive so the 7 OpenClaw posts'
     .series-nav rules still resolve, but nothing renders violet any more. */
  --green: #22c55e; --red: #ef4444; --amber: #f59e0b;
  --cyan: #06b6d4; --purple: #226299; --purple-dark: #1a4d7a;
  /* type */
  --font: 'Inter', 'Sarabun', -apple-system, BlinkMacSystemFont, sans-serif;
  --mono: 'JetBrains Mono', 'Fira Code', 'Sarabun', monospace;
  /* form */
  --radius: 12px; --radius-sm: 8px; --radius-lg: 16px;
  --measure: 720px; --wide: 860px;
  --transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
```

Verify it is still uniform before and after any edit. **`style.css` is the source of truth**; the
template agrees with it on all 29 values as of 2026-09-06, but the two carry different explanatory
comments, so **compare declarations, not lines**:

```bash
T=.claude/skills/page-design/assets/post-template.html
diff <(awk '/^    :root \{/,/^    \}/' $T | sed 's/^ *//' | sed 's|/\*.*\*/||' \
         | grep -o -- '--[a-z-]*: *[^;]*;' | sort) \
     <(awk '/^:root \{/,/^\}/' style.css | sed 's/^ *//' | sed 's|/\*.*\*/||' \
         | grep -o -- '--[a-z-]*: *[^;]*;' | sort)      # → no output
```

The naive line-diff this section used to print reported a false positive for exactly this reason
once the template grew a comment. The whole-site audit that proves the 87 blocks agree is in
`references/tokens.md` §0.

**`--coral: #c2410c` is a 30th token, and it is series-scoped.** The 20 AI Transformation posts
declare it **inside** the brand group of their own `:root`, between `--gold-dark` and `--cloud`:

```css
/* brand — sampled from the book covers. … */
--gold: #c4a46c; --gold-dark: #7a5f22; --coral: #c2410c; --cloud: #dee7e6; --parchment: #e9e1c4; --focus: #226299;
```

That placement is worth knowing before you diff anything: it means the brand **line** is not
byte-identical across all 87 blocks even though every canonical *value* is. Diff token-by-token
(the audit in `references/tokens.md` §0), not line-by-line, or those 20 files read as drift.

It is what their covers and figures are drawn in (`scripts/make_cover.py:132` and
`scripts/make_figure.py:99`, both hard-coding `(194, 65, 12)`). It is a brand token like `--gold`,
**not** a seventh status colour.

**It is declared 20 times and consumed zero times in CSS** (`grep -o 'var(--coral)' blog/*.html |
wc -l` → 0). That is deliberate, not an oversight: the colour lives in the PNG pipeline, and the
token exists so the page and the drawing agree on one name and one hex. If you ever do reach for
it in CSS, the measured numbers gate it — **5.18:1 on white** (rounds to 5.2:1, passes as body
copy) but only **4.11–4.35:1 on the light tints** those pages lay it over (`--cloud` 4.11,
`--parchment` 3.95, the figure engine's own 14% coral wash 4.21, a 12% blue wash 4.34). On any
tint it is **large-text-or-graphics only** (WCAG 1.4.3 large text, 1.4.11 non-text contrast);
never body copy. Full derivation and the ratio script are in `references/tokens.md` §4.

The three pure aliases this section used to list for deletion — `--indigo`, `--muted`, `--violet` —
are **gone** (0 occurrences). What is left off-canon is 6 genuine extras (`--emerald` ×3,
`--emerald-dark` ×3, `--orange` ×3, `--sky` ×2, `--teal` ×2, `--teal2` ×1) plus `--purple-light`
(×1, now `#4992b9` — the re-key caught it too) and 5 legitimate namespaced brand tokens;
`references/tokens.md` §3–§4 has the fold-in table. `--teal2` is **not** an alias — it is a second
teal value.

**`--radius` is `12px`, not `14px`.**
`grep -ho 'border-radius: *[0-9]*px' index.html style.css 404.html blog/*.html books/*.html news/index.html projects/index.html publications/index.html | tr -d ' ' | sort | uniq -c | sort -rn`
→ `249 12px`, `165 10px`, `156 8px`, `152 50px`, `99 2px`, `86 20px`, `67 6px`, `65 5px`, …
`5 14px`, `3 16px`. Use 12 / 8 / 16; keep `20px`–`50px` pills for tags and chips only. The `2px`
hits are almost all the `:focus-visible` ring — do not consolidate them.

Two things moved here. **`border-radius:16px` collapsed from 30 literals to 3** because
`.post-hero__cover` now writes `border-radius: var(--radius-lg, 16px)` in all 75 posts that have a
cover. **Count `var()` with the fallback form or you will undercount by 25×** —
`grep -c 'var(--radius-lg)'` reports 3; `grep -cE 'var\(--radius-lg[,)]'` reports 78. Same trap on
`--gold-dark` (86 → 162) and `--focus` (165 → 241).

And every in-body count roughly **doubled** (`10px` 83→165) because the 2026-09-03 bilingual
conversion duplicates the whole article body, so any rule serving in-body content is matched twice
as often in a whole-file grep. When a count in this file looks like it grew ~2×, that is why — it
is not new sprawl.

**`--radius` is correct in all 87 blocks, and CLAUDE.md was corrected in `5a522ed`** —
the `--radius: 14px` line this paragraph used to flag is gone. Anti-pattern 11 keeps the story.

**The remaining token gap is consumption, not declaration — and it narrowed.** `--radius-sm` is now
the best-consumed form token (**109** uses), `--radius-lg` **78**, `--radius` **56**, `--measure`
**34** (up from 14). `--wide` is still **6** uses against 151 `max-width:860px` literals, and two
brand tokens — `--cloud` and `--parchment` — are declared 87 times and consumed **0** times outside
the gradient stops that spell their hexes out. Nothing renders wrong; it just means "change the
measure" is still an N-file edit. Write `var()` in new code; convert existing files
opportunistically, not as a scheduled sweep. `references/tokens.md` §2.

---

## 2. The type scale is finished — extend it, do not redesign it

This is the most consistent part of the codebase. Resist the urge to "modernise typography"; there
is nothing to fix.

| Role | Value | Evidence |
|---|---|---|
| body | `17px` / `1.8` | 74/76 posts; the 2 exceptions are the minified pair (§0) |
| post title | `clamp(1.8rem, 5vw, 3rem)` | 76/76 posts, one value (74 spaced + 2 unspaced) |
| `.post-body h2` | `1.6rem` / 800 | 74 files declare it, **73 identical**; `obsidian-ai-jarvis` is `1.7rem` |
| `.post-body h3` | `1.25rem` / 700 | 74 files declare it, **73 identical**; `obsidian-ai-jarvis` is `1.3rem` |
| `.post-body h4` | `1.05rem` / 700 | 32 files declare it, **32/32 identical** — the other 42 simply never use `h4` |
| `.post-body p` | `margin-bottom: 1.25rem` | house |
| landing section heading | `clamp(2rem, 4vw, 3.5rem)` | `style.css` lines 310, 364, 437 — identical; line 485 is a near-miss at `clamp(2rem, 4vw, 3.2rem)` — snap it to 3.5rem |

Verify with a block-aware parse, not a line-based grep — and **strip `@media` blocks first**, or
you will read the mobile override as a second house value. A naive count returns 153 `.post-body
h2` rules split 78 × `1.4rem` / 73 × `1.6rem`, and the `1.4rem` majority is not a competing house
size: it is the `@media (max-width: 768px)` step-down, present in nearly every file.

```bash
python3 - <<'PY'
import re, glob, collections
def strip_media(s):
    out=[]; i=0
    while (m := re.search(r'@media[^{]*\{', s[i:])):
        out.append(s[i:i+m.start()]); j=i+m.end(); d=1
        while d and j < len(s):
            d += (s[j]=='{') - (s[j]=='}'); j += 1
        i=j
    out.append(s[i:]); return ''.join(out)
c=collections.Counter()
for f in glob.glob('blog/*.html'):
    if f.endswith('/index.html'): continue
    for m in re.finditer(r'\.post-body h2\s*\{([^}]*)\}', strip_media(open(f).read())):
        c[(re.search(r'font-size:\s*([^;]+)', m.group(1)) or [0,'none'])[1].strip()] += 1
print(c)      # → Counter({'1.6rem': 73, '1.7rem': 1})
PY
```

The 2 files with no `.post-body h2/h3/h4` rules at all are `openclaw-memory-architecture.html` and
`vibe-coding-devops-process.html` (§0).

**The extension work this section used to schedule is DONE.** The 11 island files were converted in
`662e966`; all 76 posts now carry the house body type, the canonical `clamp()` title, and the
Inter + Sarabun webfont pair. The 5 LISTING pages and the 4 DETAIL pages are `16px` / `1.7` and
that is deliberate and uniform across all nine — leave it. The five font stacks this section listed
for retirement (`'SF Pro Display'`, `'Segoe UI', Tahoma, …`, bare `-apple-system`,
`'Inter', 'Noto Sans Thai', system-ui`, and `openclaw-production`'s Inter-without-a-link) are at
**0 occurrences**; that list is now history, kept only so the anti-pattern behind it stays legible.

---

## 3. Layout constants — always pick the incumbent

| Constant | Value | Uses today |
|---|---|---|
| reading measure (`.post-body`) | **720px** | 279 literals (the two minified posts use 760px) |
| wide container (`.blog-nav__inner`) | **860px** | 151 |
| listing/detail container (5 LISTING + 4 DETAIL + 404) | **1200px** | 27 |
| hero cover box | **380px** max-width (75/75) and `border-radius: var(--radius-lg, 16px)` (75/75) — the 420/480/520/560 forks are gone | one value, hold it |
| listing card image | `.card__image`: width 100%; aspect-ratio 16/10 (96px square in the phone row-card override) | `grep -n 'card__image' blog/index.html` |
| tablet breakpoint | **768px** | 63 (61 spaced + 2 unspaced) |
| phone breakpoint | **600px** | 256 |
| section-chrome nav takeover | **800px** | 10 — the 5 LISTING + 4 DETAIL pages + `404.html`, nav rules only (`5178252`) |
| landing nav takeover | **1080px** | 1 — `style.css` only (`5178252`) |
| wide breakpoint | **1024px** | 1 — `style.css`, landing grids only |
| retire | `480px` (2), `900px` (5) | fold into 600px / 768px |

```bash
grep -ho '@media[^{]*' index.html style.css 404.html blog/*.html books/*.html news/index.html projects/index.html publications/index.html \
  | sed 's/[[:space:]]*$//' | sort | uniq -c | sort -rn
```
→ `256 (max-width: 600px)`, `174 (prefers-reduced-motion: reduce)`, `61 (max-width: 768px)`,
`10 (max-width: 800px)`, `5 (max-width: 900px)`, `2 (max-width:768px)`, `2 480px`,
`1 (prefers-reduced-motion: no-preference)`, `1 1080px`, `1 1024px`. The `500px` block is gone.

Two of the 768px hits are still unspaced (`max-width:768px`) — match the spaced form in new code so
grep-based sweeps find them. The reduced-motion blocks are the `e8da9da` a11y sweep, now at 174
occurrences across 87 files because several files declare it more than once; they are not layout
breakpoints. The 10 `800px` blocks are the section-chrome mobile-nav takeover (9 section pages +
`404.html`) and the 1 `1080px` block is `style.css`'s — the desktop bar with the 6-link nav last
fits at 772px on the section-chrome pages, so 768px left a broken 769–771px band (`5178252`); keep
the takeover block byte-identical across all 9 pages.

**The island measures are gone.** The 1200/1000/900/800px `.container` widths this section used to
list for conversion (`openclaw-101`, `openclaw-security`, `openclaw-memory`, `beyond-plugins` and
the rest) all became `.post-body` 720px in `662e966`. The `max-width:1200px` hits that remain are
the LISTING/DETAIL containers, which are correct.

---

## 4. Component vocabulary

The house already has the right chrome, header, body and listing primitives. The Content group was
proposed to replace the box sprawl below, and it is now half-real: `.figure` is live (47 uses) and
`.references` shipped with the AI Transformation series (40), while `.callout` and `.compare` are
still defined-and-unused at **0** occurrences each — the sprawl they were meant to absorb is still
there. **Freeze this list. Anything new must be a modifier or element of an existing noun, never a
new noun.** Full markup for each, copy-paste ready, is in `references/components.md` — open it
whenever you add a callout, card, figure, chip strip, references block, or nav.

```
Chrome     .skip-link                       (first child of <body>, targets #main —
                                          on all 87 pages; INV-30 pairs the two)
           .blog-nav  .blog-nav__inner  .blog-nav__home  .blog-nav__back
           .blog-nav__title                 (posts. __home is the "Anirach" link added
                                          by d44adb9 so no post is a dead end — INV-29
                                          fails without it. 76/76.)
           .nav  .nav__inner  .nav__logo  .nav__links  .nav__right  .nav__cta
           .nav__divider  .nav__toggle  .nav__burger                (LISTING/DETAIL
                                          pages + index.html; .nav__toggle/.nav__burger
                                          are the pure-CSS mobile menu — never JS)
Header     .post-hero  .post-hero__tags  .post-hero__tag  .post-hero__title
           .post-hero__meta  .post-hero__sub  .post-hero__series  .post-hero__cover
Body       .post-body                       (max-width: var(--measure))
           .post-toc                        (the collapsible <details> map, d44adb9;
                                          one per language track, so 152 across 76 posts)
           .table-wrapper                   (overflow-x scroll shell for a wide <table>
                                          or <pre>, d44adb9 — the widest single class
                                          in the corpus at 346 uses)
Footers    .post-series-footer  .post-nav  .series-nav  .series-links
           .series-links--grouped  .series-links__group  .series-links__label
                                          (the 20 AI Transformation posts split their
                                          20 chips into four labelled fives — a modifier
                                          plus two elements of the existing .series-links
                                          noun, never a new noun. INV-03d is the linter's
                                          own guard that its parser survives the nesting.)
           .blog-footer  .blog-footer__nav  (the 7-destination row, d44adb9 — the other
                                          half of INV-29)
Listing    .card  .card__image|__body|__tags|__tag|__title|__excerpt|__footer|__author|__read
           .card__image--pair               (dual-jacket plate — every card on books/index.html
                                          since the 2026-08-24 dual-cover sweep; 7daf3a4 introduced it)
           .feature  .feature__media|__body|__eyebrow|__title|__excerpt
                                          (479f112 — the ONE spotlit post at the top of
                                          blog/index.html. It is deliberately NOT .card:
                                          three separate regexes count class="card",
                                          so a .feature wearing that class would inflate
                                          every counter and duplicate a feed item.)
           .blog-grid  .blog-jump           (the hero chip strip, one chip per series —
                                          INV-02f keeps it honest)
           .series-section  .series-header  .series-header__left
           .series-title  .series-icon  .series-description  .series-count
           .latest  .latest__inner  .latest__heading  .latest__list  .latest__date
                                                        (Task 10, d4b94b5)
Content    .callout  .callout--info|--warn|--good|--bad    [defined in the template — 0 uses]
           .compare  .compare__col  .compare__col--old|--new  [defined — 0 uses]
           .figure  .figure__img  .figure__caption          [live since ea3c8e8 — the 4
                                          books/ DETAIL pages use it for their cover
                                          figure, and the AI Transformation series for
                                          its 19 drawn PNGs]
           .figure--qr                 (reservation QR, books/one-day-of-light.html #event)
           .references  .references__note  .references__list  .ref-supports
           .ref-tag  .ref-tag--law|--standard|--study|--synthesis
                                          (the sourced references block closing every AI
                                          Transformation post; the tag says what KIND of
                                          evidence a source is, .ref-supports says which
                                          claim it carries)
Language   .lang-switch-box  .lang-switch  .lang-th  .lang-sep  .lang-en
           .l-th  .l-en                    (the TH ⇄ EN switch — all 76 posts. Pure CSS:
                                          a hidden checkbox before <main>, two content
                                          tracks. The short .l-* names are the TRACKS;
                                          .lang-* are the pill. Never rename to anything
                                          matching INV-12's menu-token regex.)
Code       <pre><code>                      (never .code-block — 0 occurrences sitewide)
```

The Chrome/Body/Footers additions above are not new invention: `.skip-link`, `.blog-nav__home`,
`.post-toc`, `.table-wrapper` and `.blog-footer__nav` all shipped in `d44adb9`/`bceaecd` and are in
every one of the 76 posts. The list simply had not recorded them. **The freeze still holds: do not
coin a noun this list does not contain.**

**`.category*` is gone.** Task 11 (`635eb94`) had re-cut `blog/index.html` into 3 `.category`
bands holding 2 `.series-section`s; the last band, "Technology", held 100% of the posts and so
partitioned nothing, and it was deleted on 2026-08-26 along with the two empty placeholders.
`grep -c 'class="category' blog/index.html` → **0**. The page is now: hero → one `.feature` → five
`.series-section` blocks. Its heading ladder lost a level with the bands:
`h1` page title → `h2` (the `.feature__title` + the 5 `.series-title`) → `h3` ×76 `.card__title`.

```bash
python3 -c "import re,collections; s=open('blog/index.html').read(); print(collections.Counter(int(m.group(1)) for m in re.finditer(r'<h([1-6])\b[^>]*>', s)))"
# → Counter({3: 76, 2: 6, 1: 1})
```

**Card titles are `h3`.** They were `h2` before Task 11, `h4` between Task 11 and the band
deletion, and are `h3` today. Anything that greps for a fixed level is matching 0 of 76 — write
`<h[1-6] class="card__title">` and let the backreference close it. `verify-wiring.py` was blind for
exactly this reason until 2026-08-10, and `gen_feed.py` had `<h4>` hard-coded and silently emitted
an empty feed until it was made level-agnostic.

**INV-02d survives the bands' deletion** and fails on any empty `.category` band a future commit
adds; INV-02e still verifies a "N Categories" hero stat **if** one is ever present. A new category
would have to ship its band, grid, card and count in one commit. Do not reinstate one just to have
somewhere to put a post.

The sprawl this replaces is real, re-measured today across `blog/` and `books/` (counts are
`class="…X…"` attribute occurrences, and remember every in-body one is **doubled** by the two
language tracks — halve them to get the authored count): **18 bespoke `*-card` classes**
(`info-card` ×54, `tool-card` ×20, `pillar-card` ×18, `skill-card` ×18, `stat-card` ×16,
`component-card` ×16, `mini-card` ×12, `solid-card` ×10, `team-card` ×10, `pattern-card` ×10,
`strategy-card` ×8, `feature-card` ×8, `compare-card` ×8, `provider-card` ×6, `metric-card` ×6,
`level-card` ×6, `slo-card` ×6, `api-card` ×6) and **13 bespoke box/callout classes**
(`alert` ×346 across 30 files, `diagram-box` ×78, `arch-box` ×54, `highlight-box` ×30,
`info-note` ×20, `compare-box` ×8, `warning-box` ×6, `tip` ×4, `insight-box` ×4, `analogy-box` ×4,
`case-study-box` ×2, `danger-box` ×2, `success-box` ×2). `series-info` is at **0** and is retired.

**The ranking flipped: `.alert` is now the sprawl, not `.diagram-box`.** It went from 3 uses to
346 because the AI Transformation series adopted it as its house caution box. That is the single
highest-value rename in the repo — one class, 30 files, and it maps cleanly onto
`.callout--warn`. Do not rename these en masse today; that is Phase 4 (§8). But **never add a 19th
card name or a 14th box name.** When you need a new visual treatment, it is `.card--<modifier>` or
`.callout--<modifier>`.

`blog/index.html` uses perfect BEM (`class="card"` ×76 with `card__image`, `card__body`,
`card__tags`, `card__title`, `card__excerpt`, `card__footer`, `card__author`, `card__read`).
**A raw `grep -c 'class="card"' blog/index.html` returns 77, and 77 is wrong** — the extra hit is
inside the HTML comment above the `.feature` block that warns about exactly this. `check_site.py`'s
`RE_CARD` requires the full `<a href="…" class="card">` anchor and is not fooled; anything you
write that counts cards must match the anchor, not the class token.

Sitewide the bare `class="card"` token resolves to 90 (77 in `blog/index.html` incl. that comment,
7 in `projects/index.html`, 2 in `books/index.html`, 1 on each of the 4 `books/` detail pages);
`card__tag` ×257, `card__title` ×96. `news/index.html` and `publications/index.html` do exactly
what §4 asks for and reach the vocabulary through modifiers — `card card--row` ×7 and ×8,
`card card--quiet`, `card card--feature` — which is why they contribute 0 to the bare-name count.
`style.css` follows the same convention (`.btn--pill`, `.hero__label--bold`). Follow that.

---

## 5. Hero gradients — the post families are down to TWO, and a linter holds them there

This used to be the noisiest thing on the site: 77 distinct `linear-gradient(135deg, …)` values and
17 distinct `.post-hero` gradients across 26 posts. Re-measured today it is **38 distinct values
across 191 occurrences**, and every one of the 76 `.post-hero` rules resolves to one of **two**:

```bash
python3 - <<'PY'
import re, glob, collections
c=collections.Counter()
for f in glob.glob('blog/*.html'):
    if f.endswith('/index.html'): continue
    for m in re.finditer(r'\.post-hero\s*\{([^}]*)\}', open(f).read()):
        g=re.search(r'background:\s*([^;]+)', m.group(1))
        if g: c[' '.join(g.group(1).split())]+=1
print(c)   # → Deep Blue 43, Sunrise 33.  Any third row is a violation of INV-28.
PY
```

| Family | Gradient | Use for |
|---|---|---|
| **Sunrise** (the default / light) | `linear-gradient(135deg, #eef3f3 0%, #dee7e6 50%, #e9e1c4 100%)` | DevOps fundamentals, the Life essays; also `blog/index.html`, `news/`, `404.html` |
| **Deep Blue** | `linear-gradient(135deg, #11304b 0%, #1a4d7a 45%, #226299 100%)` | OpenClaw, Hermes, AI Transformation; also `projects/` and `publications/` |
| Emerald — **section identity only, never a post** | `linear-gradient(135deg, #052e16 0%, #064e3b 40%, #065f46 100%)` | the Books section: all 5 `books/` pages (index + 4 detail) |

**Violet and Teal are retired**, and not merely deprecated — both are at **0 occurrences**
(`grep -c 'linear-gradient(135deg, *#8b5cf6'` and `… *#134e4a'` → 0 and 0). Violet went with
`d44adb9`, "Post chrome: a map, a scroll cue, and **the end of violet**"; the `--purple` token
survives it pointing at blue (§1).

`check_site.py` **INV-28** now fails the build on any `.post-hero` background that is neither
Sunrise nor Deep Blue, so "pick by series" is no longer advice — a third family cannot ship. The
AI Transformation series is the proof the rule works at scale: 20 new posts, and not one new
gradient. Its visual identity comes from `--coral` in the covers and figures instead (§1).

Verify the Sunrise fork has not come back:
`grep -ho 'linear-gradient(135deg, *#eef3f3[^)]*)' index.html 404.html blog/*.html books/*.html news/index.html projects/index.html publications/index.html | sort | uniq -c`
→ **one row, 36 hits**, all `50%`. Two rows means someone forked it again. (The 2026-08-26 re-key
mapped every retired hue through `scripts/retoken.py`; two gradients whose stops would have
collapsed into a dead flat band were replaced whole and are listed in that script's
`WHOLE_STRINGS`.)

**Never hand-pick a third.** Of the eight one-offs this section used to list for retirement, seven
are gone — `#0c1929…` (docker-compose), `#0d1117…` (github-actions), `#1a0533…` (gitops),
`#0369a1…` (cloud), `#0891b2…` (deployment), `#2563eb…` (migration), `#4f46e5…#06b6d4`
(vibe-coding) all report 0. Only `#059669…` (idle) survives, at 3 occurrences, and none of them is
a hero — retire it when you touch that file.

---

## 6. Modern CSS — ranked by ROI, with verdicts

The honest ranking here is lopsided. **Images dominated every CSS technique combined — and that
work is now done.** Items 1 and 3–6 below shipped in `ec2827b`/`21c8a55` and `e8da9da`. They are
kept here as *the standard to hold*, not as a plan. Re-verify before you act on any of it.

### DONE — hold the line, do not re-plan

**1. Image loading — LANDED, and it has held through 40 new posts.** `blog/index.html` now
references **3.29 MB across 78 unique images** over 153 `<img>` tags, of which **152 are
`loading="lazy"`** — the single eager one is the `.feature` share card, which is the LCP element
and must stay eager. The HTML-only first byte cost is 146 KB.
Sitewide, **299 of 299 `<img>` tags have all four of `loading`, `decoding`, `width`, `height`**,
and all 299 have `alt` (83 carry `fetchpriority`; 216 are lazy, 83 eager).

```bash
python3 - <<'PY'
import re, pathlib
n=ok=0
for p in pathlib.Path('.').rglob('*.html'):
    if any(x in p.parts for x in ('.claude','.git','.bilingual')): continue
    for m in re.finditer(r'<img\b[^>]*\bsrc=[^>]*>', p.read_text(encoding='utf-8'), re.S):
        n+=1; ok+= all(a+'=' in m.group(0) for a in ('loading','decoding','width','height'))
print(ok, "/", n)     # → 299 / 299
PY
```

**Two counting traps, both live today, both worth 20–37 tags:**

- **Require `src=`.** Without it the pattern `<img\b[^>]*>` also matches the literal string
  `<img>` inside a CSS comment — the one `50a0d4a` ("Fix squeezed diagrams: height:auto at every
  width") left in 37 posts explaining why `height:auto` belongs at every width. That is **37
  phantom images**, and they read as "37 images with no alt text" if you do not filter them out.
  There is no such defect; the comment is correct and should stay. INV-33 is the real check on that
  rule.
- **Parse multiline.** A line-based `grep -oh '<img[^>]*src=[^>]*>'` reports **279** — it drops the
  20 `<img>` written across several lines (8 in `books/index.html`, 2 on each of the 4 `books/`
  detail pages, 2 in `index.html`, 1 each in `blog/index.html` and `publications/index.html`).

```html
<img src="../images/api-lifecycle-cover.jpg" alt="API Lifecycle — เมื่อกด Send เกิดอะไรขึ้นบ้าง"
     width="800" height="800" loading="eager" fetchpriority="high" decoding="async">
```

Post covers are **800×800** since the drawn-cover system (`1103b7a` / `ee6b708`) — the old
`1600 × 900` in this snippet was the AI-clip-art era and is gone. `width`/`height` are the SOURCE
pixel size, not the display size. Above-the-fold hero covers get
`loading="eager" fetchpriority="high"`; everything else is lazy.

**3–6. `:focus-visible`, `prefers-reduced-motion`, `color-scheme: light`, `text-wrap: balance` —
ALL LANDED** in `e8da9da`, as one 4-line block, now in **86 embedded `<style>` blocks +
`style.css`** = complete 87/87 page coverage; every page added since (the 37 bilingual conversions,
the 10 Hermes, 9 Life and 20 AI Transformation posts) shipped with it.
`index.html` is the one HTML file without the block in its own
source, correctly, because it has no `<style>` block at all.

```bash
grep -L ':focus-visible' style.css 404.html blog/*.html books/*.html news/index.html projects/index.html publications/index.html  # → empty
grep -c ':focus-visible' style.css                                                                   # → 3
```

**There is no `script.js` and no JS guard.** The line this section used to cite — `script.js:12`'s
`matchMedia('(prefers-reduced-motion: reduce)')` — no longer exists: the file was deleted on
2026-08-26 in `bb9c7dc` ("Delete script.js — the site is zero-JavaScript — Phase 7"), and
`check_site.py` **INV-38** now fails the build on any `<script>` that is not
`application/ld+json`. The four jobs the script did all have CSS replacements in `style.css`
(reveal → `animation-timeline: view()`, `.scrolled` → `animation-timeline: scroll(root)`,
hamburger → `.nav__links:target` / the `.nav__toggle` checkbox, smooth scroll → `scroll-behavior`).
**The reveal keyframe has a `from` and deliberately no `to`** — that is what makes the effect safe
without JS; never "complete" it. See CLAUDE.md "Zero JavaScript" for the full story, including why
a `<noscript><style>` override was considered and rejected.

The 79 pages that *do* carry a `<script>` tag carry only `<script type="application/ld+json">`,
which the browser parses as data and never executes. **Keep the double quotes** — INV-38's
whitelist regex requires them.

**Corollary the old text got wrong:** `outline: none` **is** declared, 87 times, as
`:focus:not(:focus-visible) { outline: none; }`. That is correct and deliberate — it suppresses the
UA ring only for mouse/programmatic focus, never for keyboard. Do not "fix" it, and do not cite it
as evidence of a focus failure.

### DONE since this section was last written — do not re-plan these either

**2. `aspect-ratio` on `.post-hero__cover` — LANDED.** All **75** posts that carry a cover declare
it on `.post-hero__cover`, `.card__image` has it (`16/10`, plus a `1/1` override in the phone
row-card), and 76 blog files declare `aspect-ratio` somewhere. Nothing here is open.

**7. `clamp()` fluid type — LANDED everywhere.** The post-title value is canonical
(`clamp(1.8rem, 5vw, 3rem)`) in **76/76** posts, and the 5 listing + 4 detail pages each carry
their one hero `clamp()`. The "extend it to the 11 island files" instruction is finished
(`662e966`). Do not redesign either scale (§2).

### ADOPT NOW

Nothing from the original items 1–7 remains open. The live work is Phase 4 (§8): the vocabulary
collapse — starting with `.alert` → `.callout--warn` across 30 files — and then dark mode.

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

There is nothing to guard in JS. The paragraph that used to sit here told you to add
`window.matchMedia('(prefers-reduced-motion: reduce)')` to `script.js`; that file does not exist,
and adding it back fails INV-38. The scroll-driven animations are pure CSS
(`animation-timeline: scroll(root)` / `view()`) and the media block above does reach them.

**Proving the sweep landed — `index.html` is not like the other 86 files.** Every `blog/*.html`
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
grep -c ':focus-visible' style.css # → 3
grep -c 'color-scheme' style.css   # → 1
grep -c 'text-wrap' style.css      # → 6
```
Then in a real browser on `index.html`: tab once and confirm a visible focus ring, and confirm
`getComputedStyle(document.documentElement).getPropertyValue('--blue')` resolves — both prove the
`style.css` link is doing its job, which a text grep on `index.html` itself cannot show.

### LATER — blocked, not declined

- **`prefers-color-scheme` dark mode.** Genuinely worth having, but with per-file CSS it means 86
  hand-maintained dark palettes plus dark variants of 38 gradients. **The §1 blocker is cleared**
  — the tokens landed in all files in `6670480`, and `color-scheme: light` is declared in all 87,
  so a dark block now has a single well-defined place to go and a single set of names to redefine.
  Two things got easier since this was written: the gradient set halved (77 → 38 distinct, and only
  2 post families), and the light-lavender hero that had "no dark analogue" is gone. This is the
  largest remaining design project and it is genuinely unblocked, not merely deferred. Scope it as
  one `@media` block per file, written once and pasted, exactly like `e8da9da` did.
- **`color-mix()`.** Would collapse ~30 one-off tint gradients (`#eff6ff`, `#ecfdf5`, `#fefce8` …)
  into derivations of `--blue` / `--green` / `--amber`. Excellent second pass, after tokens.

### NOT NOW

- **`content-visibility: auto`.** Long posts exist and got longer — the four biggest are now all AI
  Transformation (`ai-transformation-obligations.html` 271 KB, `-eight-questions` 241 KB,
  `-ai-core` 233 KB, `-workforce` 230 KB), where `web-architecture.html` at 91 KB used to top the
  list. But `.post-body` still has no section children to apply it to — the two language
  tracks are one `<div class="l-th">` and one `<div class="l-en">`, and the hidden one already
  costs nothing to lay out because `.l-en { display: none }`. Revisit only if posts get sectioned.

### NEVER — with reasons

- **CSS nesting.** This repo is maintained by grepping and find-replacing *flat* selectors across 86
  embedded stylesheets. There is no build step to flatten nesting. §7 shows how easily cross-file
  edits already drift; nesting would make every sweep measurably harder. Actively harmful here.
- **Logical properties** (`margin-inline`, `padding-block`). Zero adoption today; both site languages
  (English, Thai) are LTR. Buys nothing, costs a rewrite of every margin and padding in 86 files.
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
   **Exception:** box-drawing characters *inside* `<pre>` that reproduce real CLI output are
   correct — e.g. the `subagents list` table in `blog/openclaw-agent-teams.html`. Do not strip
   those while cleaning up ASCII art. The `/* ── SECTION ── */` CSS comment convention is also
   deliberate and worth keeping.

   The AI Transformation series is the current proof that the PNG rule scales: **19 figures**, all
   drawn by `scripts/make_figure.py`, all `<img>` inside a `.figure` — not one div-diagram. See
   `references/components.md` §8.

2. **Never add a shared stylesheet before resolving the name collisions.** `index.html` is the only
   file linking `style.css`. Dropping a `<link>` into a post today collides immediately: `.nav`
   still means two different components (`index.html` and the 9 section pages use one; posts wear
   `.blog-nav` and would inherit the other) — the third meaning, the island posts', went with
   `662e966`; `.card` means "blog listing card" in `blog/index.html` but is a generic name inside
   posts; and each post's own `:root` would fight the shared one. Rename to the §4 vocabulary
   *first*, then share. Until then, propagating a change means editing N files — that is the deal.

3. **Never let a duplicated block drift silently.** Re-measured today, `.blog-nav` CSS exists in
   **4 variants across the 76 posts**: 65 files on `rgba(248,250,252,0.85)`, 9 on
   `rgba(250,247,240,0.85)` (the `--bg` tint), and the two minified singletons
   (`openclaw-memory-architecture.html` `blur(14px)`/`z-index:50`;
   `vibe-coding-devops-process.html` `blur(16px)`). The `display: flex; align-items: center;
   gap: 0.4rem;` fix on `.blog-nav__back` is in **21 files; 55 never received it** — the ratio got
   worse, not better, because the island conversion and the new series each copied whichever
   neighbour was nearest. When you edit a duplicated block, edit all N or none, and say which N in
   the commit.

   The hard-coded-hex half of this entry has half-resolved itself: `.blog-nav__back:hover` writes
   the literal `#1a4d7a` in 64 files and `var(--blue-dark)` in 10. The *value* is right now (the
   re-key fixed the old `#4f46e5`); it is the tokenisation that is still outstanding.

4. **Never reuse a cover image.** Fixed 2026-08-26 by the drawn-cover system (`1103b7a`): every
   card on the listing resolves to its own cover, and 40 posts have shipped since without a
   collision. Until then 37 cards shared only 35 —
   `../images/github-actions-cover.jpg` was double-booked by `vibe-coding-devops-process.html` and
   `github-actions.html`, `../images/monitoring-cover.jpg` by `openclaw-memory-architecture.html`
   and `monitoring-observability.html`, and the pairs were indistinguishable on the listing.
   `check_site.py` INV-07a carries no baseline entry and fails the build on any new sharing. The fix
   for a future collision is a new image, not a re-point.

5. **Never commit a cover over ~200 KB, and never as PNG. This is now clean — keep it clean.**
   `ec2827b` + `21c8a55` re-encoded every PNG cover to JPG, and `1103b7a`/`ee6b708` replaced the
   whole set with drawn art. Re-measured today: **85 JPG covers (77 `*-cover.jpg` + 8 suffixed),
   0 PNG covers, average 46 KB, largest 174 KB, zero over 200 KB.** The largest is
   `three-old-men-cover-front.jpg`; the eight suffixed faces are the four books' EN/TH jackets,
   all portrait (625–775 × 1000–1100). The `*-cover.jpg` glob alone misses the suffixed eight, so
   add `images/*-cover-*.jpg` to any cover census.

   ```bash
   ls images/*-cover.png 2>/dev/null | wc -l                                   # → 0
   find images -name '*-cover*' -size +200k                                    # → nothing
   ls -l images/*-cover.jpg images/*-cover-*.jpg \
     | awk '{s+=$5;n++} END {print n" jpg, avg "int(s/n/1024)" KB"}'           # → 85 jpg, avg 46 KB
   ```

   **Post covers are 800×800 and drawn, not photographic.** 76 of the 77 `*-cover.jpg` files are
   exactly 800×800 (the odd one out, `libraries-in-transformation-cover.jpg` at 306×461, is not a
   post cover). That squareness is load-bearing downstream: a square cover in a
   `summary_large_image` card loses ~48% of its height, which is why every post also ships a
   separate 1200×630 share card — see §9.

   PNG survives for **flat art only**: the 5 diagram images (`*-arch.png`, `*-flow.png`,
   `*-levels.png`, 123–235 KB), the 19 AI Transformation series figures
   (`ai-transformation-fig-NN-*.png`, all 1400px wide, avg 44 KB, max 58 KB) and the 884-byte
   registration QR (`one-day-of-light-qr.png`) — 25 PNGs in all. Those are correctly PNG and must
   not be converted; a q70 JPEG smears their lines (and would break the QR's modules).

6. **Never add a post without recomputing every counter in `blog/index.html`.** They were all
   stale; `b9fb125` fixed them, the bands took two of them away again, and the five-series launch
   re-cut the rest. **All seven are correct today** and `check_site.py` INV-02a–INV-02f all PASS —
   so any drift you see is drift you introduced.

   | Counter | Value today |
   |---|---|
   | `.blog-hero__stat` "N Series" | 5 |
   | `.blog-hero__stat` "N Articles" | 76 |
   | `.series-count` `#series-ai-transformation` | 20 articles |
   | `.series-count` `#series-hermes` | 10 articles |
   | `.series-count` `#series-openclaw` | 13 articles |
   | `.series-count` `#series-devops` | 24 articles |
   | `.series-count` `#series-life` | 9 articles |

   There is no "N Categories" stat any more — it went with the bands (§4). The `.blog-jump` chip
   strip in the hero is an eighth counter site in all but name: each chip's trailing `· N` must
   equal its section's card count, and INV-02f fails otherwise. It was forgotten twice at the Life
   launch, which is why the check exists.

   Recompute, never increment — incrementing by hand is how all of them went stale. Never cite line
   numbers for these; they have moved several times. Grep for the class.

   **A 21st AI Transformation post is not a hand edit.** That series is emitted by
   `scripts/build_series.py` from `scripts/series/ai-transformation.json` plus per-post content
   sheets, and it reads `blog/hermes-101.html` at run time for the `<style>` skeleton, so the
   template cannot rot. Adding one is: a manifest row → `python3 scripts/build_series.py --post
   <slug>` → `python3 scripts/build_series.py --restrip` to rewrite the grouped chip strip in the
   other twenty. Hand-editing 20 grouped strips is the failure mode `--restrip` exists to prevent;
   `--check` diffs what the builder lifted from the skeleton, and `--index-fragment` /
   `--llms-fragment` / `--covers-rows` emit the wiring the other files need. The other four series
   are still hand-wired — see `references/components.md` §5 for all four nav patterns.

7. **Never invent a token name for a value that already has one.** `--indigo` == `--blue`,
   `--muted` == `--slate-light`, `--violet` == `--purple-dark`. (`--teal2` is *not* an alias — it
   is a second teal value; see `references/tokens.md` §3.) Check `references/tokens.md` before
   adding anything.

8. **Never hand-pick a new hero gradient.** 38 distinct `135deg` values already exist. A post's
   hero is Sunrise or Deep Blue and nothing else — INV-28 enforces it (§5).

9. **Never name a font the page does not load. Now clean — keep it clean.**
   `blog/openclaw-production.html` and `blog/openclaw-security.html` used to declare `'Inter'` with
   no Google Fonts `<link>` and no `preconnect`, silently rendering in a system font while claiming
   the house typeface; all 10 pure island files lacked both tags. `662e966` fixed all of them.
   Today `grep -L 'fonts.googleapis.com' blog/*.html` and `grep -L 'preconnect' blog/*.html` are
   both **empty**, and so is `grep -L 'Sarabun' blog/*.html` — every post loads Inter and the Thai
   Sarabun face it actually renders in.

10. **Never link an absolute route that does not exist. Now clean — keep it clean.** `b9fb125`
    removed the 14 dead absolute links (`/about`, `/research`, `/contact`, `/teaching`,
    `../about/`), and Task 8 gave `/projects` a real page. Every one of those five routes is now
    linked from **0** files, and `check_site.py` INV-05 ("every relative/site-absolute href resolves
    on disk") PASSes with 0 violations. Extensionless `/blog/<slug>` links **are** fine — GitHub
    Pages resolves them to `.html`, and INV-09 checks every one. All four `.series-nav` chip strips
    use that form deliberately (46 strips: 7 OpenClaw + 10 Hermes + 9 Life + 20 AI Transformation);
    the `<link rel="canonical">` with the `.html` extension is what resolves the duplicate.

    ```bash
    python3 .claude/skills/site-check/scripts/check_site.py | grep 'INV-05 \|INV-09'
    ```

11. **Never let CLAUDE.md — or a skill file — drift.** The three claims this entry used to track
    are all fixed (`5a522ed` rewrote CLAUDE.md against the shipped implementation): the
    `--radius: 14px` line is gone (real value `12px`, 249 uses vs 5, declared in 87 of 87 `:root`
    blocks), the CSS-variables advice points at the canonical set, and the category-band prose was
    later removed with the bands themselves. `79fe517` and `0e0a78c` are two more of the same
    repair.

    **The lesson generalises to this file, and it has bitten here too.** `bb9c7dc` and `662e966`
    both landed on 2026-08-26; for the eleven days to 2026-09-06 this skill still called
    `index.html` "the only page with a `<script>`" (there is no script anywhere) and still listed
    11 island posts in §0 (there are none) — because those sweeps landed without touching a skill
    file. CLAUDE.md is hand-maintained prose about a hand-maintained site; so is this. Both go
    stale the moment a sweep lands without touching them.

    This entry is also the reason for the standing rule at the top of this file.

12. **Never add JavaScript — to `blog/index.html` or to anything else.** This is no longer a
    per-page convention, it is a sitewide invariant with a linter behind it: `script.js` was
    deleted in `bb9c7dc` and `check_site.py` **INV-38** fails the build on any `<script>` that is
    not `application/ld+json`. `grep -c '<script' blog/index.html` → `0`, and the 79 pages that do
    have a `<script>` tag have only the JSON-LD data block. Any filtering, any toggle, any reveal
    must work in CSS or not ship. See §6 and CLAUDE.md "Zero JavaScript".

13. **Cap emoji in headings at roughly one per section, and never in `<h2>`.** Re-measured today,
    the spread is worse, not better: `openclaw-memory.html` is at **107 of 107** `h2`–`h4`
    headings, `openclaw-skills.html` 115 of 127, `openclaw-agent-teams.html` 60 of 100 — while
    **9 files are at zero** (claude-code-architecture, docker-vs-vms, git-branching,
    kubernetes-orchestration, linux-command-line, monitoring-observability,
    networking-fundamentals, openclaw-memory-architecture, vibe-coding-devops-process). Sitewide
    **376 of 1390 `<h2>` carry an emoji**, against a rule that says none should. Posts sitting side
    by side in the same series read as different websites. (The heading count is inflated ~2× by
    the two language tracks; the ratios are not.)

14. **Never regress alt text or image attributes.** **299 of 299** `<img src=…>` have `alt`,
    `loading`, `decoding`, `width` and `height`. Two complete sitewide practices — the only two.
    Protect both, and count them with the `src=`-anchored multiline parse in §6 or you will invent
    37 defects that do not exist. (Alt *quality* is still uneven; see a11y-perf R6.)

---

## 8. Adoption order — where the plan actually stands

Phases 1–3 **shipped** between `6670480` and `e8da9da`, and the first half of Phase 4 — the whole
island → HOUSE conversion — shipped in `662e966`. They are recorded here as history so nobody
re-plans them; the only live work is the rest of Phase 4.

| Phase | What it was | Status |
|---|---|---|
| 1 — tokens | canonical `:root` in every file, aliases deleted, `--radius: 12px` | **DONE** `6670480`, `36d9814`, re-keyed `1fca25e`. 87/87 blocks today, 29 tokens, 0 deviations. CLAUDE.md's `14px` line is fixed too (`5a522ed`). |
| 2 — images + counters + routes | JPG covers, `loading`/`decoding`/`width`/`height`, counters, dead routes, hero-gradient fork | **DONE** `ec2827b`, `21c8a55`, `b9fb125`, drawn covers `1103b7a`/`ee6b708`. 299/299 images attributed; 0 PNG covers; all 7 counters correct; 0 dead absolute links. |
| 3 — modern polish | `:focus-visible`, `prefers-reduced-motion`, `color-scheme`, `text-wrap`, `aspect-ratio`, `clamp()` | **DONE** `e8da9da`. 86 embedded blocks + `style.css` = 87/87 pages. `aspect-ratio` on 75/75 hero covers. |
| 4a — island → HOUSE | 11 posts get `.blog-nav`, `.post-hero`/`.post-body`, `<pre>`, the webfonts, 720px | **DONE** `662e966`. 0 island posts remain. |
| 4b — structural | vocabulary collapse, shared stylesheet, dark mode | **OPEN — the only live phase.** |

**Still open from Phases 1–3, small and specific:**

- `var(--wide)` is declared 87 times and consumed 6 (§1); `--cloud` and `--parchment` are consumed
  0 times. `var(--measure)` improved to 34 and `var(--radius-lg)` to 78.
- The `.blog-nav` / `.blog-nav__back` drift of anti-pattern 3 (4 variants; the flex fix in 21 of 76).
- Emoji in `<h2>`: 376 of 1390 (anti-pattern 13).
- Contrast: check the a11y-perf skill for the current R3/R4 status rather than trusting a number
  here — that skill owns the measured palette work and is re-measured on its own schedule.

**Phase 4b — structural, genuinely optional.** The cheapest first move is now the `.alert` rename:
one class, 346 occurrences, 30 files, and it lands on the existing `.callout--warn` (§4). Then the
rest of the callout and card vocabularies. **Only then** consider a shared stylesheet — and note
that the blocker in anti-pattern 2 shrank when the island posts went, since `.nav` now means two
components rather than three. After that, dark mode, which §6 lists as unblocked rather than
deferred.

A partial migration is not a failure. Phases 2, 3 and 4a are where the site visibly became nice,
modern and tidy; 4b is housekeeping.

---

## 9. What is already right — do not "improve" it

Leave these alone unless the user explicitly asks:

- the heading scale (`h2` 1.6rem 73/74, `h3` 1.25rem 73/74, hero `clamp(1.8rem, 5vw, 3rem)` ×76)
- the 720px measure and the 860px wide container
- the BEM naming in `style.css`, in `blog/index.html`'s `.card`, and in the `card--row` /
  `card--quiet` / `card--feature` modifiers on `news/` and `publications/`
- the glassy nav: `background: rgba(248,250,252,0.85); backdrop-filter: blur(20px)` — 87 files use
  `backdrop-filter` somewhere
- the `/* ── SECTION ── */` CSS comment convention (87 files, 726 uses)
- the canonical 29-token `:root`, byte-identical in 87/87 blocks (`references/tokens.md`)
- the 4-line a11y block (`:focus-visible`, reduced-motion, `color-scheme`, `text-wrap`) in 86
  embedded `<style>` blocks + `style.css` — including its `outline: none`, which is scoped to
  `:focus:not(:focus-visible)` and is correct
- **view transitions**: `@view-transition { navigation: auto; }` plus
  `view-transition-name: site-nav` / `site-footer` on all 87 pages, landed in `bb9c7dc` as part of
  the zero-JS work. It is pure CSS, degrades to nothing, and is the one modern-CSS feature this
  skill's §6 ranking never anticipated. Do not strip it, and do not add a JS fallback.
- image attributes: 299/299 `<img src=…>` carry `alt`, `loading`, `decoding`, `width` and `height`
- cover budget: 85 JPG covers (77 + 8 suffixed), 0 PNG, avg 46 KB, max 174 KB, none over 200 KB
- `<meta name="viewport">` on 87/87 files
- zero executable JavaScript sitewide, enforced by INV-38 — a feature, not an omission
  (anti-pattern 12)

**Social metadata landed 2026-08-26 — hold this line too.** All **86** enumerated pages carry a
`<!-- social -->` … `<!-- /social -->` block (canonical, `og:*`, `twitter:card`, icons,
`theme-color`, `robots`), and all 86 carry a `<meta name="description">`. `check_site.py`
**INV-27** (FAIL severity) recomputes the canonical path from each file's location and reads real
pixel dimensions out of the JPEG/PNG header, so a wrong `og:url` or a stale `og:image:width` fails
the build. **79 of the 86 also carry a JSON-LD block** right after `<!-- /social -->` — outside the
delimiters, so a social sweep cannot wipe it. `404.html` is deliberately outside all of this:
noindex, no social block, not in `sitemap.xml`, not enumerated.

Do not hand-edit a social block — regenerate it, and never point `og:image` at a diagram PNG or a
square cover with `summary_large_image` (half the image is cropped — and since `1103b7a` **every**
post cover is square). That is why the share-card set grew from 9 files to **82**: `og-site-card.jpg`,
`og-publications.jpg`, and 80 `<slug>-og.jpg` — one for each of the 76 posts and each of the 4
books. All 82 measure exactly 1200×630, verified by reading the JPEG headers. They are matched by
neither the `*-cover.jpg` nor the `*-cover-*.jpg` census glob — add
`images/*-og.jpg images/og-*.jpg` when counting them, and remember 82 ≠ 80: the two `og-*` files
are site furniture, not per-item share cards.

Genuinely missing sitewide, if the user wants more: dark mode (§6). The two double-booked hero
covers of anti-pattern 4 were fixed 2026-08-26 by the drawn-cover system, so the listing page no
longer shows any identical pair.

---

## Files in this skill

| File | Open it when |
|---|---|
| `references/tokens.md` | adding/changing any colour, radius, or token; doing a Phase 1 sweep |
| `references/components.md` | writing markup for a nav, hero, callout, card, figure, chip strip, references block, or code block |
| `assets/post-template.html` | creating a new blog post — copy this. **It is the only post template in the repo** (`blog-post/assets/post-template.html` was a duplicate that rotted three sweeps behind and was deleted — see `blog-post/assets/TEMPLATE-MOVED.md`). Brought current on 2026-09-06 after lagging `d44adb9` and the bilingual conversion; run the two verification commands in §0 before trusting it, since it has rotted once. |

Numbers in this skill were last re-measured against `905d3a4` on **2026-09-06** — the state after
the 2026-09-03 bilingual conversion (`50f56ab`…`9124920`) and the 2026-09-05 AI Transformation
launch (`5348a2c`…`905d3a4`): 87 HTML files, 86 enumerated, 76 posts in 5 series, 76/76 HOUSE,
2 post hero families, 29 `:root` tokens in 87 blocks, 61 checks in `check_site.py`.

Four numbers in this file are the ones most likely to be stale first, because a single new post
moves all of them: the post count (76), the series counts (20/10/13/24/9), the image census
(299 `<img>`, 85 covers, 82 share cards) and the `.card__title` heading level (`h3`). Re-run their
commands before trusting them — and then update them here, per the standing rule at the top.
