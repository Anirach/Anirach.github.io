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

Last verified **2026-08-24** against `7daf3a4` (One Day of Light joined `books/`: the site is
47 HTML files — `index.html`, the 5 section indexes, four `books/*.html` detail pages and 37
posts, all carrying the canonical block).

---

## 0. The audit command

```bash
python3 - <<'PY'
import re,glob,collections
files=['index.html','style.css']+sorted(glob.glob('blog/*.html'))+ \
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
    print(f"{k:16s} {sum(c.values()):3d}  " + " | ".join(f"{v}x{n}" for v,n in c.most_common()))
PY
```

Current output: **48 files scanned, 47 `:root` blocks**, and every one of the 24
canonical tokens reads `…x47` — one value, no variants, zero deviations.

`48 − 47 = 1`: `index.html` is the only file with no `:root` of its own, **by
design**. It is the one page whose CSS lives entirely in `style.css`
(`grep -c '<style' index.html` → the only hit is a comment saying so, added in
`7867c00`), and `style.css:5` carries the canonical block for it.

**Edge case that still bites audit regexes.** The two minified house files
(`blog/openclaw-memory-architecture.html`, `blog/vibe-coding-devops-process.html`)
write `:root{...}` on one line with no trailing `;` before the closing `}`, so a
regex requiring `[^;]+;` silently drops each file's *last* declaration. The
pattern above matches up to the next `;` **or** end-of-block. Exercise any
hand-rolled token audit against those two files before trusting its output.

---

## 1. The canonical block — 24 tokens, 47/47 files, zero deviations

| Group | Tokens | Files holding the canonical value | Deviating |
|---|---|---|---|
| ink | `--navy` `#0f172a`, `--slate` `#334155`, `--slate-light` `#64748b`, `--gray` `#94a3b8` | 47 | **0** |
| ground | `--bg` `#f8fafc`, `--white` `#ffffff`, `--code-bg` `#1e293b` | 47 | **0** |
| accent | `--blue` `#6366f1`, `--blue-dark` `#4f46e5`, `--blue-light` `#818cf8` | 47 | **0** |
| status | `--green` `#22c55e`, `--red` `#ef4444`, `--amber` `#f59e0b`, `--cyan` `#06b6d4`, `--purple` `#8b5cf6`, `--purple-dark` `#7c3aed` | 47 | **0** |
| type | `--font`, `--mono` | 47 | **0** |
| form | `--radius` `12px`, `--radius-sm` `8px`, `--radius-lg` `16px`, `--measure` `720px`, `--wide` `860px`, `--transition` `0.3s cubic-bezier(0.4, 0, 0.2, 1)` | 47 | **0** |

Plus `color-scheme: light` on the same `:root` in all 47.

The three pure aliases this file used to list for deletion — `--indigo`,
`--muted`, `--violet` — are **gone**; the audit reports 0 occurrences of each.

Paste the block from `assets/post-template.html`, which is byte-identical to
`style.css:5-23`. Verify after any edit:

```bash
diff <(awk '/^    :root \{/,/^    \}/' .claude/skills/page-design/assets/post-template.html | sed 's/^ *//') \
     <(awk '/^:root \{/,/^\}/' style.css | sed 's/^ *//')   # → no output
```

---

## 2. The real remaining gap: tokens are DECLARED but not CONSUMED

This is the honest outstanding work, and it is the opposite of what this file
used to describe. The colour tokens are used heavily; the **form** tokens are
declared 47 times and used almost never — though the 2026-08 section pages
(books/, publications/) finally consume `var(--measure)` and pushed several
counts up.

```bash
python3 - <<'PY'
import pathlib
files=[p for p in pathlib.Path('.').rglob('*.html')
       if '.claude' not in p.parts and '.git' not in p.parts]+[pathlib.Path('style.css')]
txt=[p.read_text(encoding='utf-8') for p in files]
for v in ['navy','blue','slate-light','gray','slate','blue-dark',
          'transition','radius','radius-sm','wide','radius-lg','measure']:
    print(f"var(--{v:11s}) {sum(t.count(f'var(--{v})') for t in txt):5d}")
PY
```

| Token | `var()` uses | Literal still in the CSS |
|---|---|---|
| `--navy` | 387 | — |
| `--blue` | 279 | — |
| `--gray` | 98 | — |
| `--slate` | 82 | — |
| `--slate-light` | 78 | — |
| `--blue-dark` | 60 | — |
| `--transition` | 32 | — |
| `--radius` | 28 | `border-radius:12px` ×169 |
| `--radius-sm` | 19 | `border-radius:8px` ×96 |
| `--measure` | 14 | `max-width:720px` ×76 |
| `--wide` | 1 | `max-width:860px` ×26 |
| `--radius-lg` | 1 | `border-radius:16px` ×30 |

Nothing is broken by this — the literals and the token values agree — but it
means a future "change the measure" or "change the radius ladder" is still an
N-file find-and-replace rather than a one-line token edit. **New code uses
`var()`**; `assets/post-template.html` does. Converting existing files is an
optional, purely mechanical follow-up, best done per-file when you are in the
file anyway. It is not a sweep worth scheduling on its own.

---

## 3. Non-canonical tokens still on disk

Not aliases, so not deletable by find-and-replace. Fold them into the six status
colours when you touch the file — the point of a six-colour status palette is
that a reader can learn it.

| Token | Value | Files | Fold into |
|---|---|---|---|
| `--emerald` | `#10b981` | 3 | `--green` |
| `--emerald-dark` | `#065f46` | 3 | keep only inside the Emerald hero gradient |
| `--orange` | `#f97316` | 3 | `--amber` |
| `--sky` | `#0ea5e9` | 2 | `--cyan` |
| `--teal` | `#0d9488` ×1, `#14b8a6` ×1 | 2 | pick `#0d9488`; the other is the Teal hero stop |
| `--teal2` | `#14b8a6` | 1 | fold into the Teal hero gradient stops |
| `--purple-light` | `#a78bfa` | 1 | `--purple` |

`--teal2` is a **second teal, not an alias**:
`blog/openclaw-memory-architecture.html` declares `--teal:#0d9488` and
`--teal2:#14b8a6` side by side, while `blog/sre-fundamentals.html` declares
`--teal: #14b8a6`. That disagreement is the whole reason `--teal` is not in the
canonical set.

---

## 4. Per-post brand tokens — the only allowed exception

Legitimate **only** for an external product's brand colour, and it must carry the
product prefix so a grep can find and scope it.

| Token | Value | File |
|---|---|---|
| `--gh-dark` | `#0d1117` | `blog/github-actions.html` |
| `--gh-blue` | `#58a6ff` | `blog/github-actions.html` |
| `--gh-green` | `#3fb950` | `blog/github-actions.html` |
| `--gh-orange` | `#d29922` | `blog/github-actions.html` |
| `--docker-blue` | `#2496ed` | `blog/docker-compose.html` |

Declare them **after** the canonical block, never interleaved, so the canonical
block stays a byte-identical paste across all 47 files.

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

Remaining off-palette literal in `style.css`: `#475569` (1 use). It is *not*
junk — it is the a11y-perf R4 replacement colour for text on the light hero
(`5.08:1` on `#c7d2fe`, where `--slate-light` is only `3.19:1`). Leave it, or
promote it to a token if a second use appears.

---

## 6. Radius

```bash
grep -ho 'border-radius: *[0-9]*px' index.html style.css blog/*.html \
     books/*.html news/index.html projects/index.html publications/index.html \
  | tr -d ' ' | sort | uniq -c | sort -rn
```

```
169 border-radius:12px      <- --radius
 96 border-radius:8px       <- --radius-sm
 83 border-radius:10px      <- migrate to 12px
 58 border-radius:2px       <- 56 of these are the :focus-visible ring (37 posts
                               x1, style.css x1, and the 9 island-chrome pages
                               x2 — base ring + the .nav__burger label ring).
                               The other 2 are the indicator bars at style.css:116
                               and :134. Do not "consolidate" them.
 54 border-radius:6px       <- migrate to 8px
 40 border-radius:20px      <- pills only (tags, chips)
 30 border-radius:16px      <- --radius-lg
 24 border-radius:5px       <- migrate to 6px/8px
 20 border-radius:50px      <- pills
 11 border-radius:4px
  7 border-radius:100px     <- pills
  5 border-radius:14px      <- BAN. (CLAUDE.md's stray 14px doc line was fixed in 5a522ed.)
  2 border-radius:25px      <- pills
  1 border-radius:999px / 30px / 24px
```

Ladder: `--radius-sm: 8px` (tags, inline code, small chips) → `--radius: 12px`
(cards, callouts, `<pre>`) → `--radius-lg: 16px` (hero cover, large media).
Pills (`20px`/`50px`/`100px`) are for tag chips and buttons only.

---

## 7. Breakpoints

```bash
grep -ho '@media[^{]*' index.html style.css blog/*.html \
     books/*.html news/index.html projects/index.html publications/index.html \
  | sed 's/[[:space:]]*$//' | sort | uniq -c | sort -rn
```

```
47 @media (prefers-reduced-motion: reduce)   <- the e8da9da sweep: 46 embedded
                                                <style> blocks + style.css
29 @media (max-width: 600px)      <- phone
23 @media (max-width: 768px)      <- tablet
 9 @media (max-width: 800px)      <- island-chrome mobile-nav takeover, nav rules
                                     only: the 5 listing + 4 detail pages (5178252;
                                     the 6-link desktop bar breaks at 769-771px)
 2 @media (max-width:768px)       <- same, unspaced; normalise on contact
 2 @media (max-width: 480px)      <- retire, fold into 600px
 1 @media (max-width: 500px)      <- retire, fold into 600px
 1 @media (max-width: 1080px)     <- style.css only, landing mobile-nav takeover (5178252)
 1 @media (max-width: 1024px)     <- style.css only, landing grids
```

Always write the spaced form `(max-width: 600px)` so grep sweeps catch it.

---

## 8. Measures

```bash
grep -ho 'max-width:[[:space:]]*[0-9]*px' index.html style.css blog/*.html \
     books/*.html news/index.html projects/index.html publications/index.html \
  | tr -d ' ' | sort | uniq -c | sort -rn | head -15
```

```
76 max-width:720px    <- --measure, .post-body  (still a literal in the posts; §2)
34 max-width:600px    <- breakpoint value, not a measure
33 max-width:1200px   <- islands + blog/index.html + the 5 listing + 4 detail pages
30 max-width:800px    <- island containers + the 9 island-chrome nav-takeover
                         breakpoints + section-page boxes
26 max-width:860px    <- --wide, .blog-nav__inner
25 max-width:768px    <- breakpoint value
16 max-width:380px    <- .post-hero__cover incumbent
10 max-width:560px    <- hero sub-copy on the section pages
 9 max-width:700px    <- cover boxes, not a text measure
 7 max-width:520px    <- 4 house .post-hero__cover + 3 diagram boxes
 6 max-width:900px    <- 2 island measures + a box on each books/ detail page
 6 max-width:760px    <- the two HOUSE .post-body deviants, SKILL.md §0
 6 max-width:480px    <- 4 house .post-hero__cover + 2 breakpoint values
 4 max-width:420px
 4 max-width:240px    <- the cover .figure cap on each books/ detail page
```

Island measures to convert: `1200px`, `1000px`, `900px`, `800px` — SKILL.md §3.

---

## 9. Gradients

**77 distinct `linear-gradient(135deg, …)` values across 138 occurrences.**

```bash
grep -ho 'linear-gradient(135deg[^)]*)' index.html style.css blog/*.html \
     books/*.html news/index.html projects/index.html publications/index.html \
  | sed 's/[[:space:]]\+/ /g;s/, /,/g' | sort | uniq -c | sort -rn | head
```

```
11 linear-gradient(135deg,rgba(99,102,241,0.03)              <- tint wash, fine
11 linear-gradient(135deg,#e8f0fe 0%,#ddd6fe 50%,#c7d2fe 100%)  <- canonical light hero
 7 linear-gradient(135deg,#8b5cf6,#7c3aed,#a78bfa)           <- violet, 3-stop variant
 7 linear-gradient(135deg,#052e16 0%,#064e3b 40%,#065f46 100%)  <- canonical emerald:
                                              2 posts + all 5 books/ (Books) pages
 5 linear-gradient(135deg,#8b5cf6 0%,#7c3aed 100%)           <- canonical violet
 4 linear-gradient(135deg,#f59e0b,#d97706)
 4 linear-gradient(135deg,#3b82f6,#2563eb)
```

The canonical light hero is now at **11 uses and there is no `40%`-stop fork
left** — `b9fb125` fixed `blog/index.html`'s. Verify the fork has not returned:

```bash
grep -ho 'linear-gradient(135deg, *#e8f0fe[^)]*)' index.html blog/*.html \
     books/*.html news/index.html projects/index.html publications/index.html \
  | sort | uniq -c        # → one row, all 50%
```

The five approved hero families are in SKILL.md §5. Everything else is either a
small tint wash (acceptable) or a one-off to retire on contact.
