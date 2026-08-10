# Token reference

All counts below were computed over the 28 `:root` blocks that exist across
`index.html`, `style.css` and `blog/*.html`. Re-verify with:

```bash
python3 - <<'PY'
import re,glob,collections
files=['index.html','style.css']+sorted(glob.glob('blog/*.html'))
vals=collections.defaultdict(collections.Counter)
for f in files:
    s=open(f,encoding='utf-8',errors='replace').read()
    for m in re.finditer(r':root\s*\{(.*?)\}', s, re.S):
        for d in re.finditer(r'(--[a-zA-Z0-9-]+)\s*:\s*([^;]+);', m.group(1)):
            vals[d.group(1)][' '.join(d.group(2).split())]+=1
for k,c in sorted(vals.items(), key=lambda kv:-sum(kv[1].values())):
    print(f"{k:16s} {sum(c.values()):3d}  " + " | ".join(f"{v}x{n}" for v,n in c.most_common()))
PY
```

---

## 1. Deviation table — the exact size of a Phase 1 sweep

| Token | Canonical | Files holding it | Deviating | Action |
|---|---|---|---|---|
| `--navy` | `#0f172a` | 28 | **0** | none |
| `--slate` | `#334155` | 28 | **0** | none |
| `--bg` | `#f8fafc` | 28 | **0** | none |
| `--white` | `#ffffff` | 27 | 1 (`#fff`) | normalise 1 |
| `--font` | `'Inter', -apple-system, BlinkMacSystemFont, sans-serif` | 27 | 1 (`'Inter',sans-serif`) | normalise 1 |
| `--slate-light` | `#64748b` | 26 | **0** | none |
| `--gray` | `#94a3b8` | 26 | **0** | none |
| `--mono` | `'JetBrains Mono', 'Fira Code', monospace` | 26 | 2 (`'…','SF Mono',Monaco,Consolas,…'`, `'JetBrains Mono',monospace`) | normalise 2 |
| `--blue` | `#6366f1` | 25 | **0** | none |
| `--blue-light` | `#818cf8` | 25 | **0** | none |
| `--code-bg` | `#1e293b` | 24 | **0** | none |
| `--blue-dark` | `#4f46e5` | 20 | **0** | add to 8 |
| `--green` | `#22c55e` | 13 | 1 (`#16a34a`) | fix 1 |
| `--red` | `#ef4444` | 12 | **0** | none |
| `--amber` | `#f59e0b` | 11 | 1 (`#d97706`) | fix 1 |
| `--purple` | `#8b5cf6` | 6 | 2 (`#a855f7`, `#7c3aed`) | fix 2 |
| `--purple-dark` | `#7c3aed` | 5 | 1 (`#6d28d9`) | fix 1 |
| `--cyan` | `#06b6d4` | 5 | **0** | none |
| `--radius` | **`12px`** | 1, at the wrong value `14px` | 38 | add everywhere; correct CLAUDE.md |
| `--transition` | `0.3s cubic-bezier(0.4, 0, 0.2, 1)` | 1 (`blog/index.html:18`, the incumbent notation) | 38 | add everywhere |
| `--measure` / `--wide` | `720px` / `860px` | 0 (used as literals: 74 / 26) | 39 | add everywhere |

**Total genuine value changes: 9.** Everything else is an addition of a token that is either absent
or already correct. That is why a 39-file sweep here cannot change rendering.

---

## 2. Tokens to DELETE — pure aliases

| Delete | Because it equals | Files |
|---|---|---|
| `--indigo` `#6366f1` | `--blue` | 4 |
| `--muted` `#64748b` | `--slate-light` | 2 |
| `--violet` `#7c3aed` | `--purple-dark` | 1 |

`--teal2` `#14b8a6` (1 file) is a **second teal, not an alias** — `blog/openclaw-memory-architecture.html:13`
declares `--teal:#0d9488` and `--teal2:#14b8a6` side by side. `blog/sre-fundamentals.html:19`
declares `--teal: #14b8a6`. Pick `#0d9488` for `--teal` and fold `--teal2` into the Teal hero
gradient stops.

---

## 3. Tokens that exist but are NOT in the canonical set

These appear in a handful of files and are not aliases. Fold them into the six status colours
rather than promoting them — the point of a six-colour status palette is that a reader can learn it.

| Token | Value | Files | Fold into |
|---|---|---|---|
| `--emerald` | `#10b981` | 3 | `--green` |
| `--emerald-dark` | `#065f46` | 3 | keep only inside the Emerald hero gradient |
| `--orange` | `#f97316` | 3 | `--amber` |
| `--sky` | `#0ea5e9` | 2 | `--cyan` |
| `--purple-light` | `#a78bfa` | 1 | `--purple` |

---

## 4. Per-post brand tokens — the only allowed exception

A per-post token is legitimate **only** when it is an external product's brand colour, and it must
be namespaced with the product prefix so a grep can find and scope it.

| Token | Value | File |
|---|---|---|
| `--gh-dark` | `#0d1117` | `blog/github-actions.html` |
| `--gh-blue` | `#58a6ff` | `blog/github-actions.html` |
| `--gh-green` | `#3fb950` | `blog/github-actions.html` |
| `--gh-orange` | `#d29922` | `blog/github-actions.html` |
| `--docker-blue` | `#2496ed` | `blog/docker-compose.html` |

Declare them **after** the canonical block, never interleaved, so the canonical block stays a
byte-identical paste across all files.

---

## 5. `style.css` — hex inventory

`style.css` declares **zero** custom properties. (The seven `--` hits at lines 30, 34, 37, 154, 198,
390 and 589 are BEM modifiers like `.btn--pill` and `.hero__label--bold`, not variables.)

```bash
grep -o '#[0-9a-fA-F]\{6\}' style.css | sort | uniq -c | sort -rn
```

| Hex | Uses | Token |
|---|---|---|
| `#6366f1` | 14 | `--blue` |
| `#0f172a` | 9 | `--navy` |
| `#e8f0fe` | 7 | hero gradient stop 1 |
| `#64748b` | 5 | `--slate-light` |
| `#1e293b` | 5 | `--code-bg` |
| `#dde6fb` | 4 | gradient stop (style.css:118, 208, 351, 423) |
| `#c7d2fe` | 3 | hero gradient stop 3 |
| `#94a3b8` | 2 | `--gray` |
| `#4f46e5` | 2 | `--blue-dark` |
| `#f8fafc` | 1 | `--bg` |
| `#334155` | 1 | `--slate` |
| `#f0f4ff` | 1 | gradient stop (style.css:474) |
| `#eff3ff` | 1 | gradient stop (style.css:297) |
| `#d0d9f7` | 1 | gradient stop (style.css:118) |
| `#475569` | 1 | **off-palette** — snap to `--slate` `#334155` |

Every ink/ground/accent hex except `--blue-light` `#818cf8` already appears here as a literal.
Eight of the fifteen rows map to tokens, two are the canonical hero-gradient stops, four more are
landing-page gradient stops with no token, and `#475569` (1 use) is off-palette — snap it to
`--slate` `#334155`. (`style.css` also uses 3-digit `#fff` ×4, which the 6-digit grep misses.)

---

## 6. Radius

```bash
grep -ho 'border-radius: *[0-9]*px' index.html style.css blog/*.html \
  | tr -d ' ' | sort | uniq -c | sort -rn
```

```
168 border-radius:12px      <- --radius
 96 border-radius:8px       <- --radius-sm
 75 border-radius:10px      <- migrate to 12px
 54 border-radius:6px       <- migrate to 8px
 33 border-radius:20px      <- pills only (tags, chips)
 31 border-radius:16px      <- --radius-lg
 24 border-radius:5px       <- migrate to 6px/8px
 11 border-radius:4px
  7 border-radius:50px      <- pills
  5 border-radius:14px      <- BAN. CLAUDE.md documents this; it is wrong.
  3 border-radius:2px       <- hamburger / indicator bars (style.css:93, style.css:107,
                               blog/index.html:59); also the value the new :focus-visible
                               snippet will use
  3 border-radius:100px     <- pills
  2 border-radius:25px      <- pills
  1 border-radius:999px     <- pill
  1 border-radius:30px      <- pill
  1 border-radius:24px      <- migrate to 16px
```

Ladder: `--radius-sm: 8px` (tags, inline code, small chips) → `--radius: 12px` (cards, callouts,
`<pre>`) → `--radius-lg: 16px` (hero cover, large media). Pills (`20px`/`50px`/`100px`) are for
tag chips and buttons only.

---

## 7. Breakpoints

```bash
grep -ho '@media[^{]*' index.html style.css blog/*.html | sort | uniq -c | sort -rn
```

```
21 @media (max-width: 600px)      <- phone
15 @media (max-width: 768px)      <- tablet
 2 @media (max-width:768px)       <- same, unspaced; normalise
 2 @media (max-width: 480px)      <- retire, fold into 600px
 1 @media (max-width: 500px)      <- retire, fold into 600px
 1 @media (max-width: 1024px)     <- style.css:586 only, landing grids
```

`style.css` uses 1024 / 768 / 480 at lines 586, 592, 631. Keep 1024 there; retire the 480.
Always write the spaced form `(max-width: 600px)` so grep sweeps catch it.

---

## 8. Measures

```bash
grep -ho 'max-width:[[:space:]]*[0-9]*px' index.html blog/*.html style.css \
  | tr -d ' ' | sort | uniq -c | sort -rn | head -12
```

```
74 max-width:720px    <- --measure, .post-body
27 max-width:600px    <- breakpoint value, not a measure
26 max-width:860px    <- --wide, .blog-nav__inner
17 max-width:768px    <- breakpoint value
17 max-width:1200px   <- islands (openclaw-101, openclaw-agent-teams, openclaw-production,
                         beyond-plugins) + blog/index.html (listing, not an island)
16 max-width:380px    <- .post-hero__cover incumbent (13 house rules + 3 inline island covers)
13 max-width:800px    <- island containers (beyond-plugins, idle-self-improvement,
                         obsidian-ai-jarvis, openclaw-migration, openclaw-integrations,
                         openclaw-skills)
 9 max-width:700px    <- openclaw-migration .hero-image and 3 other files' cover boxes —
                         not a text measure
 7 max-width:520px    <- 4 house .post-hero__cover + 3 inline diagram boxes (openclaw-memory)
 6 max-width:760px    <- the two HOUSE .post-body deviants, see SKILL.md §0
 6 max-width:480px    <- 4 house .post-hero__cover + 2 breakpoint values
 3 max-width:500px    <- 1 breakpoint value + small content boxes
```

Further down the tail: `2 max-width:900px` (openclaw-memory's container, obsidian-ai-jarvis's hero)
and `1 max-width:1000px` (openclaw-security's container) — island measures to convert, SKILL.md §3.

---

## 9. Gradients

78 distinct `linear-gradient(135deg, …)` values across 130 occurrences.

```bash
grep -ho 'linear-gradient(135deg[^)]*)' index.html blog/*.html \
  | sed 's/[[:space:]]\+/ /g;s/, /,/g' | sort | uniq -c | sort -rn | head
```

Top of the ranking:

```
11 linear-gradient(135deg,rgba(99,102,241,0.03)     <- tint wash, fine
 9 linear-gradient(135deg,#e8f0fe 0%,#ddd6fe 50%,#c7d2fe 100%)   <- canonical light hero
 7 linear-gradient(135deg,#8b5cf6,#7c3aed,#a78bfa)  <- violet, 3-stop variant
 4 linear-gradient(135deg,#f59e0b,#d97706)
 4 linear-gradient(135deg,#8b5cf6 0%,#7c3aed 100%)  <- canonical violet
 4 linear-gradient(135deg,#3b82f6,#2563eb)
```

`blog/index.html:64` carries the only `40%`-stop copy of the canonical light hero; the 9 house
posts all use `50%`. Align `blog/index.html:64` to `50%`.

The five approved hero families are in SKILL.md §5. Everything else is either a small tint wash
(acceptable) or a one-off to retire on contact.
