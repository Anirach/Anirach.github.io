# Token reference — current state and the rules for staying there

**Status: the token sweep is DONE.** Commit `6670480` ("phase1: land canonical
:root tokens in all pages") landed the canonical block, and `36d9814` fixed the
one bad `--slate-light` → `--slate` target it left behind. There is no migration
left to run. This file used to be a migration plan; it is now a description of
what is on disk plus the rules for not undoing it.

> **Standing rule.** Any change that invalidates a number in this file must
> update that number in the same commit. Every count below is reproducible from
> the command printed next to it — if you change the repo and do not re-run it,
> you have created the exact drift this file exists to prevent.

Last verified **2026-09-06** against `905d3a4` (the state after the 2026-09-03 bilingual conversion
and the 2026-09-05 AI Transformation launch): the site is **87 HTML files** — `index.html`,
`404.html`, the 5 section indexes, four `books/*.html` detail pages and 76 posts — of which **86
carry a `:root` block**, plus `style.css`, for **87 blocks** in total. `index.html` is the one file
with none, by design.

The block is **29 tokens**, not the 24 this file used to describe, and its *values* changed
wholesale on 2026-08-26 when `1fca25e` / `scripts/retoken.py` re-keyed the palette to the book
covers. Every hex in §1 below is the post-re-key value; if you are holding a note that says
`--navy: #0f172a` or `--blue: #6366f1`, that note is from before the re-key.

---

## 0. The audit command

```bash
python3 - <<'PY'
import re,glob,collections
files=['index.html','style.css','404.html']+sorted(glob.glob('blog/*.html'))+ \
      sorted(glob.glob('books/*.html'))+ \
      ['news/index.html','projects/index.html','publications/index.html']
vals=collections.defaultdict(collections.Counter); n=0
for f in files:
    s=open(f,encoding='utf-8',errors='replace').read()
    for m in re.finditer(r':root\s*\{(.*?)\}', s, re.S):
        n+=1
        # trailing ';' is optional: a minified last declaration before '}' has none
        for d in re.finditer(r'(--[a-zA-Z0-9-]+)\s*:\s*([^;]+?);?(?=;|$)', m.group(1)):
            vals[d.group(1)][' '.join(d.group(2).split())]+=1
print("files", len(files), " :root blocks", n)
for k,c in sorted(vals.items(), key=lambda kv:-sum(kv[1].values())):
    print(f"{k:16s} {sum(c.values()):3d}  " + " | ".join(f"{v}x{cnt}" for v,cnt in c.most_common()))
PY
```

Current output: **88 files scanned, 87 `:root` blocks**, and every one of the 29
canonical tokens reads `…x87` — one value, no variants, zero deviations. Below
the canonical 29 the audit prints `--coral x20` and then the small off-canon tail
(§3–§4).

`88 − 87 = 1`: `index.html` is the only file with no `:root` of its own, **by
design**. It is the one page whose CSS lives entirely in `style.css`
(`grep -c '<style' index.html` → the only hit is a comment saying so, added in
`7867c00`), and `style.css:5` carries the canonical block for it.

**Note the file list grew twice.** `404.html` was missing from the old version of
this command, and `blog/*.html` went from 37 posts to 77 files. A stale file list
is the quietest way to under-report a drift: the old command would have scanned
48 files and declared the site uniform while never opening 40 of them.

**Edge case that still bites audit regexes.** The two minified house files
(`blog/openclaw-memory-architecture.html`, `blog/vibe-coding-devops-process.html`)
write `:root{...}` on one line with no trailing `;` before the closing `}`, so a
regex requiring `[^;]+;` silently drops each file's *last* declaration. The
pattern above matches up to the next `;` **or** end-of-block. Exercise any
hand-rolled token audit against those two files before trusting its output.

---

## 1. The canonical block — 29 tokens, 87/87 blocks, zero deviations

Values are the **2026-08-26 re-key** (`1fca25e`, `scripts/retoken.py`), sampled from the book
covers. The old indigo palette (`--navy #0f172a`, `--blue #6366f1`, `--blue-dark #4f46e5`,
`--blue-light #818cf8`, `--bg #f8fafc`, `--slate-light #64748b`) is gone from every file.

| Group | Tokens | Blocks holding the canonical value | Deviating |
|---|---|---|---|
| ink | `--navy` `#11304b`, `--slate` `#334155`, `--slate-light` `#526174`, `--gray` `#94a3b8` | 87 | **0** |
| ground | `--bg` `#faf7f0`, `--white` `#ffffff`, `--code-bg` `#1e293b` | 87 | **0** |
| accent | `--blue` `#226299`, `--blue-dark` `#1a4d7a`, `--blue-light` `#4992b9` | 87 | **0** |
| brand | `--gold` `#c4a46c`, `--gold-dark` `#7a5f22`, `--cloud` `#dee7e6`, `--parchment` `#e9e1c4`, `--focus` `#226299` | 87 | **0** |
| status | `--green` `#22c55e`, `--red` `#ef4444`, `--amber` `#f59e0b`, `--cyan` `#06b6d4`, `--purple` `#226299`, `--purple-dark` `#1a4d7a` | 87 | **0** |
| type | `--font`, `--mono` (Inter + **Sarabun** + system; JetBrains Mono + Sarabun) | 87 | **0** |
| form | `--radius` `12px`, `--radius-sm` `8px`, `--radius-lg` `16px`, `--measure` `720px`, `--wide` `860px`, `--transition` `0.3s cubic-bezier(0.4, 0, 0.2, 1)` | 87 | **0** |

Plus `color-scheme: light` on the same `:root` in all 87.

Three things about that table are easy to misread:

- **`--purple` and `--purple-dark` are blues now** (`#226299` / `#1a4d7a`), not violet. The names
  survived the re-key because the 7 OpenClaw posts' `.series-nav` rules reference them; the hues
  did not. `d44adb9` is titled "the end of violet". Do not "restore" them.
- **`--blue-light` is BORDERS ONLY.** At `#4992b9` it does not carry text.
- **`--focus` is a separate token from `--blue` even though they share a value.** Footers and
  `<pre>` re-point `--focus` to `--gold`, where a blue ring falls to 2.12:1.

The three pure aliases this file used to list for deletion — `--indigo`,
`--muted`, `--violet` — are **gone**; the audit reports 0 occurrences of each.

**Paste the block from `style.css:5-25`, from `assets/post-template.html`, or
from any shipped post** — all 29 values agree across the three as of 2026-09-06.
The template lagged the re-key on `--purple`/`--purple-dark` until that date, so
verify rather than assume, and **compare declarations, not lines**: the template
and `style.css` carry different explanatory comments, and a naive line-diff
reports those as drift.

```bash
T=.claude/skills/page-design/assets/post-template.html
diff <(awk '/^    :root \{/,/^    \}/' $T | sed 's/^ *//' | sed 's|/\*.*\*/||' \
         | grep -o -- '--[a-z-]*: *[^;]*;' | sort) \
     <(awk '/^:root \{/,/^\}/' style.css | sed 's/^ *//' | sed 's|/\*.*\*/||' \
         | grep -o -- '--[a-z-]*: *[^;]*;' | sort)   # → no output
```

An empty diff there is the check to run after any `:root` edit.

---

## 2. The real remaining gap: tokens are DECLARED but not CONSUMED

This is the honest outstanding work, and it is the opposite of what this file
used to describe. The colour tokens are used heavily; the **form** tokens are
declared 87 times and consumed unevenly. The gap narrowed a lot since 2026-08-24
— `--radius-sm` went 19 → 109, `--measure` 14 → 34, `--radius-lg` 1 → 78 — but
`--wide`, `--cloud` and `--parchment` are still barely or never used.

**Count with the fallback form.** 75 files write `var(--radius-lg, 16px)`, so a
plain `t.count('var(--radius-lg)')` reports 3 instead of 78 — a 25× undercount
that would make you re-plan a sweep that already landed. Same trap on
`--gold-dark` (86 vs 162) and `--focus` (165 vs 241).

```bash
python3 - <<'PY'
import pathlib, re
files=[p for p in pathlib.Path('.').rglob('*.html')
       if not any(x in p.parts for x in ('.claude','.git','.bilingual'))]+[pathlib.Path('style.css')]
txt=[p.read_text(encoding='utf-8') for p in files]
for v in ['navy','blue','slate-light','gray','slate','blue-dark','blue-light','gold','gold-dark',
          'cloud','parchment','focus','coral','mono','font','transition',
          'radius','radius-sm','radius-lg','wide','measure']:
    bare = sum(len(re.findall(r'var\(--%s\)'      % v, t)) for t in txt)
    full = sum(len(re.findall(r'var\(--%s[,)]'    % v, t)) for t in txt)
    print(f"var(--{v:12s}) {bare:5d}  incl-fallback {full:5d}")
PY
```

| Token | `var()` uses (incl. fallback) | Literal still in the CSS |
|---|---|---|
| `--navy` | 1156 | — |
| `--blue` | 636 | — |
| `--slate-light` | 444 | — |
| `--gold` | 397 | — |
| `--focus` | 241 | — |
| `--slate` | 237 | — |
| `--blue-dark` | 306 | `#1a4d7a` ×64 on `.blog-nav__back:hover` alone |
| `--gray` | 210 | — |
| `--gold-dark` | 162 | — |
| `--mono` | 156 | — |
| `--radius-sm` | 109 | `border-radius:8px` ×156 |
| `--font` | 93 | — |
| `--radius-lg` | 78 | `border-radius:16px` ×3 — **effectively done** |
| `--radius` | 56 | `border-radius:12px` ×249 |
| `--transition` | 36 | — |
| `--measure` | 34 | `max-width:720px` ×279 |
| `--blue-light` | 6 | borders only, by design |
| `--wide` | 6 | `max-width:860px` ×151 |
| `--cloud` | **0** | its hex appears only as a gradient stop |
| `--parchment` | **0** | same |
| `--coral` | **0** | declared in 20 files, lives in the PNG pipeline — §4 |

Nothing is broken by this — the literals and the token values agree — but it
means a future "change the measure" or "change the radius ladder" is still an
N-file find-and-replace rather than a one-line token edit. **New code uses
`var()`**. Converting existing files is an optional, purely mechanical follow-up,
best done per-file when you are in the file anyway. It is not a sweep worth
scheduling on its own.

`--cloud` and `--parchment` are the two genuinely dead names. They are the
Sunrise gradient's middle and end stops, which every file spells out as literal
hex inside the `linear-gradient()`. Either consume them there or accept that they
exist to document where those two hexes came from.

---

## 3. Non-canonical tokens still on disk

Not aliases, so not deletable by find-and-replace. Fold them into the six status
colours when you touch the file — the point of a six-colour status palette is
that a reader can learn it.

| Token | Value | Blocks | Fold into |
|---|---|---|---|
| `--emerald` | `#10b981` | 3 | `--green` |
| `--emerald-dark` | `#065f46` | 3 | keep only inside the Emerald hero gradient (the 5 `books/` pages) |
| `--orange` | `#f97316` | 3 | `--amber` |
| `--sky` | `#0ea5e9` | 2 | `--cyan` |
| `--teal` | `#0d9488` ×1, `#14b8a6` ×1 | 2 | pick `#0d9488` |
| `--teal2` | `#14b8a6` | 1 | fold into `--teal` |
| `--purple-light` | `#4992b9` | 1 | `--blue-light` — the re-key caught it, so it is now an exact alias |

`--teal2` is a **second teal, not an alias**:
`blog/openclaw-memory-architecture.html` declares `--teal:#0d9488` and
`--teal2:#14b8a6` side by side, while `blog/sre-fundamentals.html` declares
`--teal: #14b8a6`. That disagreement is the whole reason `--teal` is not in the
canonical set.

`--purple-light` **is** now a pure alias: the re-key mapped it onto `#4992b9`,
which is exactly `--blue-light`. Its one consumer is a `.blog-footer a` rule that
should read `var(--gold)` like the other 70 — fix that and the token can go.

The Teal hero gradient this section used to defend no longer exists (0
occurrences), so nothing is protecting `--teal`/`--teal2` any more.

---

## 4. Series and per-post brand tokens — the only allowed exceptions

### 4a. `--coral: #c2410c` — the 30th token, series-scoped

The 20 AI Transformation posts (`blog/ai-transformation-*.html`) declare one
token beyond the canonical 29. It is **interleaved into the brand group**, not
appended after the block — between `--gold-dark` and `--cloud`:

```css
/* brand — sampled from the book covers. --gold is decorative on light grounds (2.2:1); --gold-dark is its text form. */
--gold: #c4a46c; --gold-dark: #7a5f22; --coral: #c2410c; --cloud: #dee7e6; --parchment: #e9e1c4; --focus: #226299;
```

**This breaks the "byte-identical paste" property for one line in 20 files**, and
it is the one exception to the rule in §4b below. Every canonical *value* still
agrees across all 87 blocks, so the §0 audit — which parses declarations, not
lines — reports zero deviations. A line-based diff of the brand row would report
20 false positives. Parse, do not diff.

It is a **brand** token like `--gold`, not a seventh status colour. It is the
series' visual signature: the covers and the 19 figures are drawn in it, and both
generators hard-code the same RGB rather than reading the CSS —
`scripts/make_cover.py:132` (`"coral": (194, 65, 12)`) and
`scripts/make_figure.py:99` (`CORAL = (194, 65, 12)`). The token exists so the
page and the drawing agree on one name and one hex.

**It is declared 20 times and consumed 0 times in CSS.** `grep -c 'var(--coral)'`
across every HTML file and `style.css` returns 0, and the literal `#c2410c`
appears exactly once per file — the declaration itself. That is deliberate, not
an oversight. Do not "fix" it by inventing a use.

**Measured contrast, and what it permits.** Computed with the WCAG 2.x relative
luminance formula (sRGB linearisation, `(L1+0.05)/(L2+0.05)`):

| Coral on | Ratio | Verdict |
|---|---|---|
| `#ffffff` white | **5.18:1** | passes AA for body text (≥4.5) |
| `--bg` `#faf7f0` | 4.84:1 | passes AA for body text |
| 12% coral wash on white | 4.35:1 | **fails** AA body — large text / graphics only |
| `--cloud` `#dee7e6` | 4.11:1 | **fails** AA body |
| gold tint 30% on white | 4.10:1 | **fails** AA body |
| `--parchment` `#e9e1c4` | 3.95:1 | **fails** AA body |
| `make_figure.py`'s own 14% coral wash | 4.21:1 | **fails** AA body |

So: **coral on white is a text colour; coral on any of this site's light tints is
not.** On a tint it is large-text-or-graphics only — WCAG 1.4.3 (large text,
≥18.66px bold / 24px regular) and 1.4.11 (non-text contrast, ≥3:1 for a border,
rule or icon). The figures stay inside that: coral is used there for 3–6px
outlines, rounded envelopes and heading-size labels, never for small type.

Re-derive rather than trust:

```bash
python3 - <<'PY'
def lin(c):
    c/=255
    return c/12.92 if c<=0.04045 else ((c+0.055)/1.055)**2.4
def L(rgb):
    r,g,b=map(lin,rgb); return 0.2126*r+0.7152*g+0.0722*b
def ratio(a,b):
    la,lb=L(a),L(b); hi,lo=max(la,lb),min(la,lb); return (hi+.05)/(lo+.05)
def over(fg,bg,a): return tuple(round(bg[i]+(fg[i]-bg[i])*a) for i in range(3))
coral,white=(194,65,12),(255,255,255)
print("white       %.2f" % ratio(coral,white))
print("--bg        %.2f" % ratio(coral,(250,247,240)))
print("--cloud     %.2f" % ratio(coral,(222,231,230)))
print("--parchment %.2f" % ratio(coral,(233,225,196)))
print("coral 14%%   %.2f" % ratio(coral,over(coral,white,0.14)))
PY
# → 5.18 / 4.84 / 4.11 / 3.95 / 4.21
```

For comparison, `--blue` `#226299` is **6.41:1** on white — which is why it, and
not coral, is the body link colour.

### 4b. Per-post product brand tokens

Legitimate **only** for an external product's brand colour, and it must carry the
product prefix so a grep can find and scope it.

| Token | Value | File |
|---|---|---|
| `--gh-dark` | `#0d1117` | `blog/github-actions.html` |
| `--gh-blue` | `#58a6ff` | `blog/github-actions.html` |
| `--gh-green` | `#3fb950` | `blog/github-actions.html` |
| `--gh-orange` | `#d29922` | `blog/github-actions.html` |
| `--docker-blue` | `#2496ed` | `blog/docker-compose.html` |

Declare these **after** the canonical block, never interleaved, so the canonical
29 stay a byte-identical paste. `--coral` is the standing exception (§4a) and it
predates this rule being written down — do not add a second one.

---

## 5. `style.css` — it HAS the tokens now

The previous version of this file said "`style.css` declares **zero** custom
properties". That is false as of `6670480`. `style.css:5-23` carries the full
canonical `:root`, and `check_site.py` INV-22b exists specifically to keep it
that way (it currently PASSes).

```bash
grep -n ':root' style.css                    # → 5
grep -c 'var(--' style.css                   # → non-zero
```

The seven `--` hits at the old lines 30, 34, 37, 154, 198, 390, 589 are BEM
modifiers like `.btn--pill` and `.hero__label--bold`, not variables — that part
of the old note was correct and is the reason the wrong conclusion was drawn.
Use `grep -nE '^\s*--[a-z-]+\s*:' style.css`, which counts declarations, not
double-hyphens anywhere in the file.

`style.css:5` still carries the canonical block, now re-keyed and 29 tokens long,
and INV-22b still PASSes. Its `:focus-visible` count is **3** and `text-wrap`
appears **6** times (the a11y block plus per-component uses) — the "2" and "1"
this file's neighbours used to quote are pre-re-key numbers.

The off-palette literal `#475569` this section used to defend is **gone** (0 uses),
and so is the light-lavender hero `#c7d2fe` it was contrast-matched against (0
uses sitewide). Both went with the 2026-08-26 re-key. There is no off-palette
literal left in `style.css` to argue about.

---

## 6. Radius

```bash
grep -ho 'border-radius: *[0-9]*px' index.html style.css 404.html blog/*.html \
     books/*.html news/index.html projects/index.html publications/index.html \
  | tr -d ' ' | sort | uniq -c | sort -rn
```

```
249 border-radius:12px      <- --radius
165 border-radius:10px      <- migrate to 12px
156 border-radius:8px       <- --radius-sm
152 border-radius:50px      <- pills (chips, tags, .ref-tag, .series-links)
 99 border-radius:2px       <- the :focus-visible ring (86 pages x1, style.css x1,
                               and the 9 section-chrome pages carry a second for
                               the .nav__burger label) plus 2 indicator bars in
                               style.css. Do not "consolidate" them.
 86 border-radius:20px      <- pills only (tags, chips)
 67 border-radius:6px       <- migrate to 8px
 65 border-radius:5px       <- migrate to 6px/8px
 16 border-radius:4px
  9 border-radius:100px     <- pills
  5 border-radius:14px      <- BAN. (CLAUDE.md's stray 14px doc line was fixed in 5a522ed.)
  3 border-radius:16px      <- the last literals; 75 files now write
                               var(--radius-lg, 16px) on .post-hero__cover instead
  1 border-radius:999px / 30px / 25px / 24px
```

**Read these against the bilingual doubling.** Anything inside `.post-body` is
matched twice per file since 2026-09-03, so `10px` at 165 is not twice the sprawl
it was at 83 — it is the same sprawl, counted twice. The `12px`/`8px`/`2px`
figures are mostly chrome and scale with the page count, not with the tracks.

Ladder: `--radius-sm: 8px` (tags, inline code, small chips) → `--radius: 12px`
(cards, callouts, `<pre>`) → `--radius-lg: 16px` (hero cover, large media).
Pills (`20px`/`50px`/`100px`) are for tag chips and buttons only.

---

## 7. Breakpoints

```bash
grep -ho '@media[^{]*' index.html style.css 404.html blog/*.html \
     books/*.html news/index.html projects/index.html publications/index.html \
  | sed 's/[[:space:]]*$//' | sort | uniq -c | sort -rn
```

```
256 @media (max-width: 600px)      <- phone
174 @media (prefers-reduced-motion: reduce)   <- the e8da9da sweep, now across 86
                                     embedded <style> blocks + style.css; several
                                     files declare it more than once
 61 @media (max-width: 768px)      <- tablet
 10 @media (max-width: 800px)      <- section-chrome mobile-nav takeover, nav rules
                                      only: the 5 listing + 4 detail pages + 404.html
                                      (5178252; the 6-link desktop bar breaks at 769-771px)
  5 @media (max-width: 900px)      <- retire; leftovers in 5 ex-island posts
                                      (idle-self-improvement, openclaw-integrations,
                                      openclaw-memory-architecture, openclaw-migration,
                                      openclaw-security). Fold into 768px.
  2 @media (max-width:768px)       <- same as 768; unspaced, normalise on contact
  2 @media (max-width: 480px)      <- style.css + blog/index.html; fold into 600px
  1 @media (prefers-reduced-motion: no-preference)
  1 @media (max-width: 1080px)     <- style.css only, landing mobile-nav takeover (5178252)
  1 @media (max-width: 1024px)     <- style.css only, landing grids
```

The `500px` block this table used to list is gone. Always write the spaced form
`(max-width: 600px)` so grep sweeps catch it.

---

## 8. Measures

```bash
grep -ho 'max-width:[[:space:]]*[0-9]*px' index.html style.css 404.html blog/*.html \
     books/*.html news/index.html projects/index.html publications/index.html \
  | tr -d ' ' | sort | uniq -c | sort -rn | head -20
```

```
279 max-width:720px    <- --measure, .post-body  (still a literal in the posts; §2)
258 max-width:600px    <- breakpoint value, not a measure
151 max-width:860px    <- --wide, .blog-nav__inner
 75 max-width:380px    <- .post-hero__cover, now the ONLY hero-cover value
 63 max-width:768px    <- breakpoint value
 41 max-width:640px    <- in-body content boxes
 27 max-width:1200px   <- blog/index.html + the 5 listing + 4 detail pages + 404.html
 21 max-width:800px    <- the 9 section-chrome nav-takeover breakpoints + boxes
 19 max-width:560px    <- hero sub-copy on the section pages
 10 max-width:620px
  9 max-width:900px    <- breakpoint value in 5 ex-island posts + books/ boxes
  6 max-width:520px
  4 max-width:760px    <- the two .post-body deviants, SKILL.md §0
  4 max-width:240px    <- the cover .figure cap on each books/ detail page
  3 max-width:400px
  2 max-width:700px / 480px / 300px / 220px
  1 max-width:500px
```

**The island measures are converted.** `1000px` is at 0, and no `blog/*.html`
post carries `max-width:1200px` any more — `662e966` moved all 11 onto
`.post-body` 720px. The 27 remaining `1200px` hits are all LISTING/DETAIL
containers, which are correct. The `420/480/520/560` hero-cover forks are gone
too: `.post-hero__cover` is `380px` in 75 of 75.

---

## 9. Gradients

**38 distinct `linear-gradient(135deg, …)` values across 191 occurrences** — down
from 77 distinct / 138, because the re-key collapsed the hues and `662e966`
deleted the island one-offs.

```bash
grep -ho 'linear-gradient(135deg[^)]*)' index.html style.css 404.html blog/*.html \
     books/*.html news/index.html projects/index.html publications/index.html \
  | sed 's/[[:space:]]\+/ /g;s/, /,/g' | sort | uniq -c | sort -rn | head
```

```
45 linear-gradient(135deg,#11304b 0%,#1a4d7a 45%,#226299 100%)  <- DEEP BLUE hero
36 linear-gradient(135deg,#eef3f3 0%,#dee7e6 50%,#e9e1c4 100%)  <- SUNRISE hero
31 linear-gradient(135deg,#f3f4f6 0%,#e5e7eb 100%)           <- neutral placeholder wash
11 linear-gradient(135deg,rgba(34,98,153,0.03)               <- blue tint wash, fine
 6 linear-gradient(135deg,#052e16 0%,#064e3b 40%,#065f46 100%)  <- EMERALD: the 5
                                              books/ (Books) pages only, never a post
 5 linear-gradient(135deg,#f59e0b,#d97706)
 5 linear-gradient(135deg,#3b82f6,#2563eb)
 3 linear-gradient(135deg,#226299,#1a4d7a)
```

**Violet and Teal are at 0.** `#8b5cf6` and `#134e4a` return nothing — violet
went in `d44adb9` ("the end of violet"), and the Teal hero with it. The
light-lavender `#e8f0fe → #ddd6fe → #c7d2fe` hero that used to head this list is
also at 0; Sunrise replaced it.

Verify the Sunrise fork has not returned:

```bash
grep -ho 'linear-gradient(135deg, *#eef3f3[^)]*)' index.html 404.html blog/*.html \
     books/*.html news/index.html projects/index.html publications/index.html \
  | sort | uniq -c        # → one row, 36 hits, all 50%
```

**Post heroes are Sunrise or Deep Blue and nothing else** — 33 and 43 across the
76 posts, and `check_site.py` INV-28 fails the build on a third. Emerald is a
section identity, not a post family. See SKILL.md §5. Everything else here is
either a small tint wash (acceptable) or a one-off to retire on contact; of the
eight one-offs this file used to name, only `#059669…` survives, at 3
occurrences, none of them a hero.
