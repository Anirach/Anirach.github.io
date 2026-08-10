# Contrast reference — measured values for anirach.com

All ratios computed with the WCAG 2.x sRGB relative-luminance formula, with alpha
layers composited over their real backdrop. Body/meta text on this site is 12–18 px,
so the threshold is **4.5:1** unless a line says otherwise.

## The palette — identical in all 42 `:root` blocks since `6670480`

```css
:root {
  --navy: #0f172a; --blue: #6366f1; --blue-dark: #4f46e5; --blue-light: #818cf8;
  --slate: #334155; --slate-light: #64748b; --gray: #94a3b8;
  --bg: #f8fafc; --white: #ffffff;
}
```

Every ratio in this file is therefore a *sitewide* ratio, not a per-file one: there are no
palette variants left to check. See `page-design/references/tokens.md` §1.

**Line numbers in the tables below are gone on purpose.** `blog/index.html` has been
re-cut twice (Task 10 and Task 11) and every line reference in this file had drifted.
Grep for the class name instead — e.g. `grep -n '\.series-count' blog/index.html`.

## A. Token contrast, light backgrounds

| Colour | on `#ffffff` | on `--bg #f8fafc` | Verdict |
|---|---|---|---|
| `--gray #94a3b8` | **2.56** | **2.45** | fail both |
| `#6b7a8f` (a commonly suggested "fix") | **4.37** | **4.18** | **fail — do not use** |
| `--slate-light #64748b` | 4.76 | 4.55 | pass (use this for `--gray` sites) |
| `--slate #334155` | 10.35 | 9.90 | pass |
| `--blue #6366f1` | **4.47** | 4.27 | **fail** |
| `--blue-dark #4f46e5` | 6.29 | 6.01 | pass |

`--gray` is fine on dark: `#94a3b8` on `--navy #0f172a` is **6.96:1** — which is why
you must not redefine the token globally. `#64748b` on `#0f172a` is only 3.75:1 and
would break `.footer span` (`grep -n '\.footer span' blog/index.html`).

## B. Failing pairs on `blog/index.html`

| Ratio | Selector | Current | Use instead |
|---|---|---|---|
| **2.56** | `.card__series` — **dead rule: the class appears 0 times in markup** | `var(--gray)` on `#fff` | delete the rule, or `var(--slate-light)` → 4.76 if the element is ever added |
| **2.99** | `.blog-hero__label` | `#6366f1` on `#c7d2fe` | `#4338ca` → 5.30 |
| **3.19** | `.blog-hero__sub` | `#64748b` on `#c7d2fe` | `#475569` → 5.08 |
| **3.67** | `.blog-hero__stat strong` | `#6366f1` on `rgba(255,255,255,.5)`/`#c7d2fe` = `#e3e8fe` | `#4f46e5` → 5.16 |
| **3.87** | `.series-count` | `#6366f1` on `rgba(99,102,241,.08)/#f8fafc` = `#eceefb` | `#4f46e5` → 5.45 |
| **3.90** | `.blog-hero__label` | `#6366f1` on `#e8f0fe` | `#4338ca` → 6.90 |
| **4.09** | `.card__tag` | `#6366f1` on `rgba(99,102,241,.07)/#fff` = `#f4f4fe` | `#4f46e5` → 5.75 |
| **4.15** | `.blog-hero__sub` | `#64748b` on `#e8f0fe` | `#475569` → 6.61 |
| **4.47** | `.card__read` | `#6366f1` on `#fff` (marginal) | `#4f46e5` → 6.29 |

`.blog-hero__sub` and `.blog-hero__label` fail across the **whole** hero gradient, not
just one end — check both stops when picking a replacement. The gradient is now the
canonical `linear-gradient(135deg, #e8f0fe 0%, #ddd6fe 50%, #c7d2fe 100%)`; the `40%`
middle-stop fork this file used to cite was fixed in `b9fb125`, which does not change any
ratio here (the end stops are the same).

Passing already, leave alone: `.card__excerpt` 4.76, `.footer a #818cf8` on navy 5.98,
`.card:hover .card__read #4f46e5` 6.29, `.footer span` 6.96, `.blog-hero__stat` 8.53,
body text 9.90, `.card__title` 17.85. Two are marginal (`.nav__links a` 4.55,
`.series-description` 4.55) — don't lighten them further.

## C. `.post-hero__meta` on dark gradients

Current value in **15** files: `rgba(255,255,255,0.6)`, plus `.7` in
`openclaw-memory-architecture.html` and `.75` in `vibe-coding-devops-process.html`.
Re-verified 2026-08-10 — **no sweep has touched this; it is all still outstanding.**
Ratios are against the gradient's **worst (lightest) stop**, since 135deg text can
overlap it.

| Worst stop | a=0.60 | a=0.92 | solid `#fff` | `#fff` + 0.35 black scrim |
|---|---|---|---|---|
| `#38bdf8` cloud | **1.57** | **2.02** | **2.14** | 4.75 |
| `#06b6d4` deploy | **1.68** | **2.25** | **2.43** | 5.30 |
| `#14b8a6` monitor | **1.72** | **2.31** | **2.49** | 5.36 |
| `#a78bfa` openclaw | **1.89** | **2.54** | **2.72** | 5.78 |
| `#818cf8` frontend-perf | **2.01** | **2.77** | **2.98** | 6.20 |
| `#047857` green | **3.00** | 4.90 | 5.48 | 9.76 |
| `#0f766e` teal | **3.01** | 4.90 | 5.47 | 9.69 |
| `#4338ca` automated-testing | **3.86** | 6.94 | 7.90 | 12.45 |
| `#3730a3` auth | 4.61 | 8.64 | 9.93 | 14.20 |
| `#4c1d95` gitops | 4.88 | 9.49 | 10.95 | 15.04 |
| `#21262d` github | 6.39 | 13.09 | 15.22 | 17.67 |

**The takeaway that keeps getting stated wrongly:** raising the alpha to 0.92 does
*not* rescue the top five rows. Solid white doesn't either. Those gradients must be
darkened. A `linear-gradient(rgba(0,0,0,.35), rgba(0,0,0,.35))` layered above the
colour gradient brings every hero on the site to ≥4.75:1 with solid white text and
preserves the designed hue. A 0.45 scrim allows `rgba(255,255,255,0.92)` back (worst
case 5.52) if the softer meta look matters.

### Which file has which hero gradient

```
blog/cloud-architecture.html             #0369a1 → #0284c7 → #38bdf8    scrim needed
blog/deployment-hosting.html             #0891b2 → #0e7490 → #06b6d4    scrim needed
blog/claude-code-architecture.html       #7c3aed → #8b5cf6 → #a78bfa    scrim needed
blog/frontend-performance.html           #7c3aed → #6366f1 → #818cf8    scrim needed
blog/openclaw-memory-architecture.html   #0f766e → #0d9488 → #14b8a6    scrim needed (meta is rgba(255,255,255,.7) at :22)
blog/vibe-coding-devops-process.html     #4f46e5 → #7c3aed → #06b6d4    scrim needed (meta is rgba(255,255,255,.75) at :23)
blog/software-testing.html               #064e3b → #065f46 → #047857    solid #fff is enough
blog/sre-fundamentals.html               #134e4a → #115e59 → #0f766e    solid #fff is enough
blog/code-quality.html                   #052e16 → #064e3b → #065f46    solid #fff is enough
blog/database-sql.html                   #052e16 → #064e3b → #065f46    solid #fff is enough
blog/automated-testing.html              #1e1b4b → #312e81 → #4338ca    solid #fff is enough
blog/authentication-authorization.html   #1e1b4b → #312e81 → #3730a3    solid #fff is enough
blog/devops-security.html                #0f172a → #1e1b4b → #312e81    solid #fff is enough
blog/docker-compose.html                 #0c1929 → #1a2744 → #1e3a5f    solid #fff is enough
blog/gitops-argocd.html                  #1a0533 → #2d1b69 → #4c1d95    already passes at a=0.6
blog/github-actions.html                 #0d1117 → #161b22 → #21262d    already passes at a=0.6
blog/web-architecture.html               var(--navy) → #1e293b → var(--slate)   solid #fff is enough
```

Nine posts use the **light** hero `#e8f0fe → #ddd6fe → #c7d2fe` with dark text —
api-request-lifecycle, cicd-pipeline, docker-vs-vms, git-branching,
infrastructure-as-code, kubernetes-orchestration, linux-command-line,
monitoring-observability, networking-fundamentals. There the defects are the reverse:
`.post-hero__meta { color: var(--slate-light) }` is 3.19:1 (use `#475569`, 5.08) and
`.post-hero__series { color: var(--blue) }` is 2.99:1 (use `#4338ca`, 5.30).

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

print(cr('#4f46e5', '#ffffff'))                       # 6.29
print(cr('#6366f1', over('#6366f1','#ffffff',0.07)))  # tinted chip: 4.09
print(cr('#ffffff', over('#000000','#38bdf8',0.35)))  # scrimmed hero: 4.75
EOF
```

Rules of thumb this data supports, for when you need a value not in the tables:

- A translucent tint chip barely changes the backdrop — `rgba(99,102,241,.07)` over
  white composites to `#f4f4fe`, so the chip text needs almost the same contrast as it
  would on plain white. Don't assume the tint "helps".
- `rgba(255,255,255,0.6)` only clears AA on backdrops at or below roughly `#4c1d95`
  lightness. Above that, no alpha value works — darken the backdrop.
- Large text (≥18.66px bold or ≥24px) drops the bar to 3:1, which rescues nothing on
  this site: `.post-hero__meta` is 13.6px and `.card__series` is 11.52px.
