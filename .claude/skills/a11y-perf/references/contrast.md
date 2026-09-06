# Contrast reference — measured values for anirach.com

All ratios computed with the WCAG 2.x sRGB relative-luminance formula, with alpha
layers composited over their real backdrop. Body/meta text on this site is 12–18 px,
so the threshold is **4.5:1** unless a line says otherwise.

**Re-measured 2026-09-06 against `905d3a4`.** This file previously carried the pre-2026-08-26
indigo palette (`--blue #6366f1`, `--navy #0f172a`, `--bg #f8fafc`) and a table of ten hero
gradients. **None of those colours is on the site any more.** The palette was re-keyed to the
book covers by `scripts/retoken.py`, the ten heroes were collapsed to two families, and the
2026-09-05 AI Transformation series added a 30th token. Everything below is the current state.

## The palette — identical in all 87 `:root` blocks (86 embedded + `style.css`)

```css
:root {
  /* ink */    --navy: #11304b; --slate: #334155; --slate-light: #526174; --gray: #94a3b8;
  /* ground */ --bg: #faf7f0; --white: #ffffff; --code-bg: #1e293b;
  /* accent */ --blue: #226299; --blue-dark: #1a4d7a; --blue-light: #4992b9;
  /* brand */  --gold: #c4a46c; --gold-dark: #7a5f22; --coral: #c2410c;
               --cloud: #dee7e6; --parchment: #e9e1c4; --focus: #226299;
  /* status */ --green: #22c55e; --red: #ef4444; --amber: #f59e0b; --cyan: #06b6d4;
}
```

Every ratio in this file is therefore a *sitewide* ratio, not a per-file one: there are no
palette variants left to check. See `page-design/references/tokens.md` §1.

**Line numbers in the tables below are gone on purpose.** `blog/index.html` has been
re-cut several times and every line reference in this file had drifted. Grep for the class
name instead — e.g. `grep -n '\.series-count' blog/index.html`.

## A. Token contrast on every ground the site actually uses

Bold = fails AA for body text (4.5:1). The four light grounds are the ones a post body,
a card or a hero can sit on; `--navy` is the footer and the Deep Blue hero; `--code-bg`
is `<pre>`.

| token | white | `--bg` cream | `--cloud` | `--parchment` | `--navy` | `--code-bg` |
|---|---|---|---|---|---|---|
| `--navy #11304b` | 13.56 | 12.68 | 10.77 | 10.36 | **1.00** | **1.08** |
| `--slate #334155` | 10.35 | 9.68 | 8.22 | 7.91 | **1.31** | **1.41** |
| `--slate-light #526174` | 6.32 | 5.91 | 5.02 | 4.83 | **2.14** | **2.31** |
| `--gray #94a3b8` | **2.56** | **2.40** | **2.04** | **1.96** | 5.29 | 5.71 |
| `--blue #226299` | 6.41 | 5.99 | 5.09 | 4.90 | **2.12** | **2.28** |
| `--blue-dark #1a4d7a` | 8.80 | 8.22 | 6.99 | 6.72 | **1.54** | **1.66** |
| `--blue-light #4992b9` | **3.45** | **3.22** | **2.74** | **2.63** | **3.94** | **4.25** |
| `--gold #c4a46c` | **2.37** | **2.21** | **1.88** | **1.81** | 5.73 | 6.18 |
| `--gold-dark #7a5f22` | 6.02 | 5.63 | 4.78 | 4.60 | **2.25** | **2.43** |
| **`--coral #c2410c`** | **5.18** | **4.84** | **4.11** | **3.95** | **2.62** | **2.82** |
| `--green #22c55e` | **2.28** | **2.13** | **1.81** | **1.74** | 5.95 | 6.42 |
| `--red #ef4444` | **3.76** | **3.52** | **2.99** | **2.87** | **3.60** | **3.89** |
| `--amber #f59e0b` | **2.15** | **2.01** | **1.71** | **1.64** | 6.32 | 6.81 |
| `--cyan #06b6d4` | **2.43** | **2.27** | **1.93** | **1.85** | 5.59 | 6.03 |

Read the table as four standing rules:

- **`--gray` is a dark-ground token only.** 2.56:1 on white, 5.29:1 on navy — which is why
  `.footer span` may keep it and why you must never redefine the token globally to "fix"
  white. `#64748b` on `#11304b` is only **2.85:1** and would break the footer; `#6b7a8f`, the
  perennial suggestion, is **4.37:1** on white and fails anyway. Use `--slate-light` on light.
- **`--blue-light`, `--gold`, `--green`, `--amber`, `--cyan` and `--red` are never text on a
  light ground.** `--blue-light` is borders-only (its 32 former text uses moved to `--gold`,
  leaving 6 sitewide);
  `--gold` is decorative on light and `--gold-dark` is its text form; the status colours are
  fills and icons, and their text form is a dark variant.
- **`--focus` exists because the ring lands on the page ground.** `outline-offset: 3px`
  pushes it outside its element, so inside a navy footer or a `<pre>` the blue ring measures
  2.12:1. All 87 files re-point it: `.footer, .blog-footer, pre { --focus: var(--gold) }`
  → 5.73:1 on navy.
- **`--coral` is ground-dependent, and it is the newest trap.** See §A1.

### A1. `--coral #c2410c` — legal on white and cream, not on a tint

Added 2026-09-05 with the AI Transformation series as the 30th token. It is the only accent
in the palette that passes on two grounds and fails on the other two, so "coral passes" is
not a safe thing to remember.

| ground | ratio | verdict for 12–18 px body text |
|---|---|---|
| `#ffffff` white | **5.18** | pass |
| `--bg #faf7f0` cream | **4.84** | pass |
| `--cloud #dee7e6` | **4.11** | **fail** — large text / graphics only (3:1) |
| `--parchment #e9e1c4` | **3.95** | **fail** — large text / graphics only |
| `--navy #11304b` | **2.62** | fail — never coral on navy |
| figure tints (§A2) | **4.10 – 4.55** | treat as fail; only the green tint clears, at 4.55 |

White text *on* coral is 5.18:1, so `background: var(--coral); color: #fff` is a legal
badge. Coral text on any tinted chip is not.

**Nothing on the site currently uses `var(--coral)` in CSS.** All 20 AI Transformation posts
declare the token and none of them spends it: the colour is actually applied inside the drawn
covers and the 19 series figures, by `scripts/make_figure.py`'s `CORAL = (194, 65, 12)`. The
`:root` declaration exists so the two definitions cannot drift. If you are the first to write
`color: var(--coral)` into a stylesheet, this table is the thing to check first.

### A2. The figure tints — `scripts/make_figure.py`, not CSS

The series figures fill tiles with a token at low alpha over white. These are the composited
grounds, and the only text drawn on them is navy or slate-light:

| tint | alpha | composite | `--navy` | `--slate-light` | `--coral` | `--blue` |
|---|---|---|---|---|---|---|
| blue | 0.12 | `#e4ecf3` | 11.36 | 5.30 | **4.34** | 5.37 |
| green | 0.15 | `#def6e7` | 11.91 | 5.55 | 4.55 | 5.63 |
| gold | 0.30 | `#ede4d3` | 10.75 | 5.01 | **4.10** | 5.08 |
| coral | 0.14 | `#f6e4dd` | 11.02 | 5.14 | **4.21** | 5.21 |
| gray | 0.25 | `#e4e8ed` | 11.02 | 5.14 | **4.21** | 5.21 |

Navy and slate-light are safe on every tint, which is what the renderer uses. Coral is not —
if you extend `make_figure.py` to draw coral label text on a tinted tile, it has to be
≥18.66 px bold or ≥24 px to clear the 3:1 large-text bar.

A tint barely moves the backdrop: `rgba(34,98,153,.12)` over white composites to `#e4ecf3`,
whose relative luminance is **0.83 against white's 1.00** — so `--slate-light` reads 5.30:1
there against 6.32:1 on plain white, a 16% haircut, not a rescue. **Do not assume a tint
"helps"**; the text needs very nearly the contrast it would need on white.

## B. `blog/index.html` — every pair passes, re-measured 2026-09-06

This section used to be a list of nine failures. The token re-key closed all of them without
a single per-selector edit. Kept as a positive record so a future sweep does not "fix" a
passing pair back into a failing one.

| Ratio | Selector | Colour on ground |
|---|---|---|
| 13.56 | `.card__title`, `.feature__title` | `--navy` on `--white` |
| 8.80 | `.blog-jump a` (active) | `#fff` on `--blue-dark` |
| 7.34 | `.blog-jump a` | `--blue-dark` on `rgba(34,98,153,.08)`/`--bg` = `#e9ebe9` |
| 6.41 | `.card__read` | `--blue` on `--white` |
| 6.32 | `.card__tag`, `.card__excerpt`, `.nav__links a` | `--slate-light` on `--white` |
| 5.91 | `.series-description` | `--slate-light` on `--bg` |
| 5.73 | `.footer a` | `--gold` on `--navy` |
| 5.35 | `.series-count` | `--blue` on `rgba(34,98,153,.08)`/`--bg` = `#e9ebe9` |
| 5.29 | `.footer span` | `--gray` on `--navy` |
| 4.90–5.73 | `.blog-hero__stat strong`, `.blog-hero__label` | `--blue` across the sunrise hero's three stops |
| 4.83–5.65 | `.blog-hero__sub` | `--slate-light` across the same three stops |

The hero is the canonical Sunrise gradient
`linear-gradient(135deg, #eef3f3 0%, #dee7e6 50%, #e9e1c4 100%)`. **Check both end stops when
picking any hero colour** — a 135deg run means text can overlap either, and `#e9e1c4` is the
one that binds.

**One dead rule survives, and it is the only `var(--gray)`-on-light left on the page:**
`.card__series { color: var(--gray) }` at **2.56:1**. The class appears **0 times in markup**,
so it never renders. Delete the rule, or recolour it to `var(--slate-light)` (6.32) if the
element is ever added. Find it with `grep -n 'card__series' blog/index.html`; do not trust a
line number here.

## C. `.post-hero__meta` — two hero families, both passing

**Solved structurally on 2026-08-26 by `scripts/reheroize.py`, not pair-by-pair.** Ten hero
gradients became two, and `check_site.py` **INV-28** fails the build on any `.post-hero`
background that is neither. There are **zero** `rgba(255,255,255,0.x)` meta colours left.

| Family | Gradient | Posts | Meta colour | Worst stop | Ratio there |
|---|---|---|---|---|---|
| **Deep Blue** | `135deg, #11304b 0%, #1a4d7a 45%, #226299 100%` | 43 | `#fff` | `#226299` | **6.41** |
| **Sunrise** | `135deg, #eef3f3 0%, #dee7e6 50%, #e9e1c4 100%` | 33 | `var(--slate-light)` | `#e9e1c4` | **4.83** |

Other text on the same two grounds, for when you add an element to a hero:

| | on Deep Blue worst stop `#226299` | on Sunrise worst stop `#e9e1c4` |
|---|---|---|
| `#fff` | 6.41 | 1.15 — never |
| `--navy` | 2.12 — never | 10.36 |
| `--slate-light` | 2.14 — never | 4.83 (marginal; do not lighten) |
| `--gold` | 2.71 — never | 1.81 — never |
| `--coral` | 2.62 — never | **3.95 — large text only** |

```bash
python3 -c "
import re,glob,collections
c=collections.Counter()
for f in glob.glob('blog/*.html'):
    for m in re.finditer(r'\.post-hero__meta\s*\{([^}]*)\}', open(f,encoding='utf-8').read()):
        cm=re.search(r'color:\s*([^;]+)', m.group(1)); c[cm.group(1).strip() if cm else 'none']+=1
print(dict(c))"   # → {'#fff': 44, 'var(--slate-light)': 32, 'none': 71}
```

### C0. `.post-hero__tag` on Sunrise — the one open contrast defect, 33 posts

Measured 2026-09-06. The tag pill is `color: var(--blue)` on `rgba(34,98,153,0.1)`, i.e. a 10%
tint of itself over whichever hero stop sits behind it. All **33 Sunrise posts** use `var(--blue)`;
all 43 Deep Blue posts invert to light ink and are unaffected.

| Hero stop | Pill ground | `--blue` | `--blue-dark` |
|---|---|---|---|
| `#eef3f3` (0%) | `#e5eef2` | **5.00:1** | 6.70:1 |
| `#dee7e6` (50%) | `#d6e2e6` | **4.46:1** | 6.02:1 |
| `#e9e1c4` (100%) | `#e0dcc4` | **4.28:1** | 5.76:1 |

`.post-hero__tag` is `0.7rem` (11.2 px) at weight 600 — **small text**, so the bar is 4.5:1, not
3:1. The pill therefore passes over the cool end of the gradient and fails over the warm end. Its
real ratio depends on where the 135° gradient has got to behind a centred pill at that hero's
width, which is why this reads as marginal rather than flatly broken: the range is 4.28–5.00:1 and
only the top of it is safe.

Drop-in fix, one declaration per file, no markup change:

```css
    .post-hero__tag {
      /* was: color: var(--blue);  4.28-5.00:1 over the Sunrise gradient at 11.2px */
      color: var(--blue-dark);   /* 5.76-6.70:1 on every stop */
    }
```

`--blue-dark` is already in all 87 `:root` blocks, so this is a value swap and nothing else. The
repaired `page-design/assets/post-template.html` already specifies `--blue-dark` here, so new posts
do not inherit the defect. **Not swept yet** — 33 files, and worth doing in one commit with a
before/after screenshot rather than folded into unrelated work.

### C1. The scrim recipe — kept as method, not as a to-do

No hero on the site needs it today. It is here because it is the correct answer if a third
family is ever proposed with a light end stop, and because the wrong answer keeps getting
suggested.

**Raising the alpha does not rescue a light backdrop.** On a `#38bdf8`-class stop,
`rgba(255,255,255,0.6)` is 1.57:1, `0.92` is 2.02:1 and solid `#ffffff` is still only
2.14:1. Darken the backdrop instead:

```css
.post-hero {
  background:
    linear-gradient(rgba(0,0,0,.35), rgba(0,0,0,.35)),
    linear-gradient(135deg, #0369a1 0%, #0284c7 40%, #38bdf8 100%);
}
.post-hero__meta { color: #fff; }
```

A 0.35 black scrim with solid white puts the worst historical stop at **4.75:1**; a 0.45
scrim buys back `rgba(255,255,255,0.92)` at 5.52:1 if the softer meta look matters.
`rgba(255,255,255,0.6)` only clears AA on backdrops at or below roughly `#4c1d95` lightness.

### C2. The two-track trap

Every post carries its body twice — `.l-th` and `.l-en` — but **the hero, the meta row and
both nav strips belong to neither track**. A contrast fix applied inside one language
wrapper reaches half the page and looks correct in the browser you happen to have the switch
set to. Fix hero and nav CSS in the `<style>` block (one place, both tracks), and use
`python3 scripts/bilingualize.py --verify <slug>` after any per-post edit that touches body
markup.

## D. Computing a new pair

```bash
python3 - <<'EOF'
def lum(h):
    h=h.lstrip('#'); r,g,b=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    f=lambda c: c/12.92 if c<=0.03928 else ((c+0.055)/1.055)**2.4
    return 0.2126*f(r)+0.7152*f(g)+0.0722*f(b)
def cr(a,b):
    l1,l2=sorted([lum(a),lum(b)],reverse=True); return (l1+0.05)/(l2+0.05)
def over(fg,bg,a):   # composite a translucent fg over an opaque bg
    f=[int(fg.lstrip('#')[i:i+2],16) for i in (0,2,4)]
    b=[int(bg.lstrip('#')[i:i+2],16) for i in (0,2,4)]
    return '#%02x%02x%02x'%tuple(round(f[i]*a+b[i]*(1-a)) for i in range(3))

print(cr('#226299', '#ffffff'))                       # --blue on white:        6.41
print(cr('#c2410c', '#ffffff'))                       # --coral on white:       5.18
print(cr('#c2410c', over('#c2410c','#ffffff',0.14)))  # --coral on its own tint: 4.21
print(cr('#c4a46c', '#11304b'))                       # --gold on navy (--focus): 5.73
print(cr('#ffffff', over('#000000','#38bdf8',0.35)))  # scrimmed hero:          4.75
EOF
```

Rules of thumb this data supports, for when you need a value not in the tables:

- A translucent tint chip barely changes the backdrop — `rgba(34,98,153,.08)` over `--bg`
  composites to `#e9ebe9`, so the chip text needs almost the same contrast as it would on
  the cream. Don't assume the tint "helps".
- `rgba(255,255,255,0.6)` only clears AA on backdrops at or below roughly `#4c1d95`
  lightness. Above that, no alpha value works — darken the backdrop.
- Large text (≥18.66 px bold or ≥24 px) drops the bar to 3:1. On this site that rescues
  almost nothing — `.post-hero__meta` is 13.6 px, `.card__tag` is 0.72 rem and
  `.ref-tag` is 0.7 rem — but it is exactly what makes `--coral` usable inside a figure,
  where the type is drawn large.
- The four brand grounds are not interchangeable. Every ratio drops by roughly 20% going
  from white to `--parchment`; a colour that clears 4.5:1 on white by a hair will fail
  there.
