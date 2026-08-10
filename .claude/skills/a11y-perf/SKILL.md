---
name: a11y-perf
description: Accessibility and performance rules for the anirach.com static site (39 hand-written HTML files, no build step, per-file embedded CSS). Use this whenever you touch any .html file in this repo, add or edit a blog post under blog/, add or swap an image in images/, edit a :root palette or a .post-hero gradient, change nav markup, or are asked about contrast, alt text, focus states, keyboard access, page weight, image size, fonts, or Lighthouse/Core Web Vitals — even if the user does not mention accessibility or performance at all, and even for a "just add a card to blog/index.html" request. It carries this site's real measured numbers (blog/index.html is 18.41 MB; --blue #6366f1 fails AA in every light context; 0 :focus rules against 91 :hover; the blog/index.html hamburger has no handler) plus verified drop-in fixes, so use it instead of deriving generic WCAG advice.
---

# Accessibility & performance for anirach.com

This site has no build step, no partials and no tests. Every page in `blog/` carries
its own `<style>`, its own `:root` and its own copy of the nav. A "global" fix is an
N-file edit, and nothing catches a regression except you. That is why these rules are
written as concrete values you can paste, not principles you have to re-derive.

Everything below was measured on this repo. Re-run the command if you doubt a number.

---

## Standing rules — apply when writing or editing any page

### 1. Covers ship as JPEG q80 at ≤800px. Never PNG.

The 15 PNG cover images average **1137 KB**; the 20 JPG covers average **83 KB** — a
13.7× gap for visually identical AI illustrations. They are the reason
`blog/index.html` weighs 18.41 MB.

```bash
ls -l images/*-cover.png | awk '{s+=$5;n++} END {print n" png, avg "int(s/n/1024)" KB"}'
ls -l images/*-cover.jpg | awk '{s+=$5;n++} END {print n" jpg, avg "int(s/n/1024)" KB"}'
# → 15 png, avg 1137 KB
# → 20 jpg, avg 83 KB
```

Before adding a cover, run `ls -lS images/ | head` and compare. Hard-fail any cover
over ~200 KB. To produce one:

```bash
sips -s format jpeg -s formatOptions 80 -Z 800 new-cover.png --out images/new-cover.jpg
```

PNG is correct for the five *diagram* images only — `*-arch.png`, `*-flow.png`,
`*-levels.png` — which are already right at 126–241 KB. Do not convert those; PNG
preserves the crisp lines that a q80 JPEG smears. (Diagrams are PNG for a reason:
inline HTML/CSS and ASCII-art diagrams were tried and reverted in f4f7e1b, 4fc85af,
c270892 and 4ae2660 because they kept breaking layout.)

### 2. Every `<img>` gets `width`, `height`, `loading` and `decoding`.

Zero of the 118 `<img>` tags on this site have any of them today, so every image is
eagerly downloaded and every card reflows on load.

```bash
grep -roh "<img[^>]*>" --include="*.html" . | grep -c "loading="   # → 0
```

Card images in `blog/index.html` sit in a 352×220 CSS px slot (1200px section −
2×2.5rem padding = 1120; `repeat(auto-fill, minmax(340px,1fr))` with `gap:2rem` →
3 cols of 352px; `.card__image { aspect-ratio: 16/10 }` → 220px). Source covers are
square on 24 of 35 files (13× 800×800, 11× 1024×1024) and landscape on the other 11
(1024×680, 800×446, 1024×509, …). On a square source, `object-fit:cover` into the
16:10 slot throws away 37.5% of the pixels; on the landscape ones only ~6%. Check
the actual file with `sips -g pixelWidth -g pixelHeight` before quoting a waste figure.

```html
<!-- blog/index.html card: below the fold, fixed slot -->
<img src="../images/openclaw-101-cover.png" alt="" width="352" height="220"
     loading="lazy" decoding="async">

<!-- post hero cover: above the fold, do NOT lazy-load the LCP element -->
<img src="../images/openclaw-101-cover.png" alt="OpenClaw 101 architecture overview"
     width="1024" height="1024" fetchpriority="high" decoding="async">
```

(`openclaw-101-cover` exists only as a 1024×1024 PNG today — point at `.jpg` only
after R1's PNG→JPEG conversion has run, or use a cover that is already JPEG, e.g.
`../images/kubernetes-cover.jpg`.)

### 3. No page except `index.html` may ship a control that needs JavaScript.

`index.html` is the only file on the site with a `<script>`:

```bash
grep -rl "<script" --include="*.html" .   # → index.html
```

`script.js` binds `document.getElementById('hamburger')`, an id that exists only at
`index.html:28`. So a hamburger button pasted into any other page is decorative
scenery over a hidden menu — see remediation R2. If a design needs a toggle on a
`blog/` page, either solve it in CSS (horizontal-scrolling nav strip) or don't ship
the control.

### 4. Use `--blue-dark #4f46e5` for text; `--blue #6366f1` is a background colour.

`--blue #6366f1` fails WCAG AA in **every** light-background use on this site:
4.47:1 on white, 4.09:1 on the tag chip, 3.87:1 on the series-count chip, 3.90:1 and
2.99:1 on the two ends of the hero gradient. `--blue-dark #4f46e5` — already in the
palette at `blog/index.html:14` — clears all of those except the hero gradient.

On the light hero gradient `#e8f0fe → #ddd6fe → #c7d2fe` even `#4f46e5` is only
4.22:1 at the darkest stop. Use `#4338ca` there (5.30:1).

Keep `#6366f1` for borders, backgrounds, shadows and gradient stops. Full table in
`references/contrast.md`.

### 5. Every `:hover` affordance needs a `:focus-visible` twin.

91 `:hover` rules, 0 `:focus` rules. Mouse users get card lift, image scale and a
colour shift; keyboard users get none of it.

Be honest about the severity when you report this: `outline` is **never** set to
`none` or `0` anywhere on the site (`grep -rIoE "outline *:" --include="*.html"
--include="*.css" --exclude-dir=.claude .` → 0 matches; without the exclusion you
count this skill's own assets), so the browser's default focus ring still draws
and prose links are still underlined via `.post-body a` in 20 posts. This is a
hover/focus *parity* gap, not a keyboard blackout. Verify `outline:none` before ever
claiming a focus failure — crying "keyboard inaccessible" on a site with a working
default ring trains over-reporting and burns the user's trust in the real findings.

Paste-in block: `assets/a11y-block.css`.

### 6. Text on a dark hero must clear AA against the gradient's **lightest** stop.

`rgba(255,255,255,0.6)` is the `.post-hero__meta` colour in 15 files and it fails on
8 of the 10 gradients in use, down to 1.57:1 on `#38bdf8`. Raising the alpha does not
save the light gradients — solid `#ffffff` on `#38bdf8` is still only **2.14:1**.
Anything below roughly `#4c1d95` lightness needs the gradient darkened, not the text
brightened. See R3 and `references/contrast.md`.

### 7. Thai page, English headings — mark the switch.

37 of 39 files are `<html lang="th">` with English headings, code and technical terms,
and there are zero inline `lang=` switches. A Thai screen-reader voice reading
"Kubernetes Orchestration" is unintelligible.

```html
<h2 lang="en">Kubernetes Orchestration</h2>
<pre lang="en"><code>kubectl apply -f deploy.yaml</code></pre>
```

### 8. One `<h1>`, no level skips, content in `<main id="main">`.

The default failure mode here is `h2 → h4`: 11 of 37 posts do it (plus one `h1 → h3`
in `blog/openclaw-integrations.html`). `<main>` exists in
only 8 of 39 files. When copying an existing post as a template, check its heading
ladder first — you will inherit the skip.

### 9. Don't "fix" what is already correct.

These are right; flagging them wastes the user's time:

- `display=swap` present on **29/29** font-loading files.
- Both `preconnect` links present on **29/29**.
- `<meta name="viewport" content="width=device-width, initial-scale=1.0">` identical
  on all 39 files — pinch-zoom is not blocked.
- All 118 `<img>` tags have an `alt` attribute (the *quality* is the problem, not the
  presence).
- Embedded `<style>` avoids an extra round trip; 5–16 KB is a fine cost.

### 10. State the file count before starting, and script the edit.

There are no partials. Before proposing a sitewide change, count the files and say the
number out loud so the user can judge scope:

| Change | Files |
|---|---|
| Palette / `:root` patch | **28** (11 files have no `:root` — see below) |
| Skip link + reduced-motion block | 39 |
| `<main id="main">` wrap | 31 |
| Font URL trim | 27 |
| `rel="noopener"` | 21 links |
| `.post-hero__meta` colour | 15 |

Write a loop or `sed` script, never 39 sequential Edit calls. **A `sed` on `:root`
silently misses 11 files** — `index.html` plus `blog/beyond-plugins.html`,
`idle-self-improvement`, `openclaw-101`, `openclaw-agent-teams`,
`openclaw-integrations`, `openclaw-memory`, `openclaw-migration`,
`openclaw-production`, `openclaw-security`, `openclaw-skills`. Those same 10 posts
also load no webfont and declare their own stacks (`'Segoe UI', Tahoma, Geneva,
Verdana` at `blog/openclaw-memory.html:15`; `-apple-system, BlinkMacSystemFont,
'Segoe UI', Roboto` at `blog/beyond-plugins.html:11`), so the Inter design system does
not reach them at all. Loops and verification commands: `references/n-file-edits.md`.

---

## Remediation — outstanding defects, worst first

### R1. `blog/index.html` is 18.41 MB on one page load

74 `<img>` requests for 36 unique files, none lazy, 18.36 MB of it images.

```bash
# reproduce: python3 over blog/index.html resolving every <img src> to a file size
# → img tags: 74 / unique files: 36 / unique image bytes: 19,247,246 (18.36 MB)
#   html: 58,715 / TOTAL: 19,305,961 (18.41 MB)
```

Fix, verified end to end — re-encode the 15 PNG covers and repoint the references:

```bash
cd /Users/anirach/Documents/Anirach.github.io/images
for f in *-cover.png; do
  sips -s format jpeg -s formatOptions 80 -Z 800 "$f" --out "${f%.png}.jpg"
done
cd ..
# repoint every reference, then delete the PNGs once git shows the diff is clean
grep -rl -- "-cover.png" --include="*.html" --exclude-dir=.claude . \
  | xargs sed -i '' -E 's/(-cover)\.png/\1.jpg/g'
grep -rc -- "-cover.png" --include="*.html" --exclude-dir=.claude . | grep -v ':0$'   # must print nothing
rm images/*-cover.png
```

Measured result of that exact `sips` loop: 16.66 MB → 1.59 MB, **15.07 MB saved
(90.4%)**. Worst single file `obsidian-ai-jarvis-cover.png` 1,644,242 → 140,825 bytes.
`blog/index.html` drops from 18.41 MB to **≈3.35 MB**; adding `loading="lazy"` (rule 2)
takes the initial payload far below that.

Then apply rule 2 to all 118 images. Second-heaviest pages after this:
`blog/idle-self-improvement.html` 1732 KB, `openclaw-migration.html` 1661 KB,
`obsidian-ai-jarvis.html` 1649 KB — all HTML under 43 KB, all weight in covers.

### R2. Dead mobile navigation

`blog/index.html:173-174` inside `@media (max-width: 768px)`:

```css
.nav__links    { display: none; }   /* 5 links gone */
.nav__hamburger { display: flex; }  /* button shown */
```

The button at `blog/index.html:208` is `<button class="nav__hamburger"
aria-label="Menu">` — no `id`, no `aria-expanded`, no `aria-controls`, no handler, and
the file has no `<script>`. Five nav links are unreachable on mobile.

`blog/obsidian-ai-jarvis.html:250` is worse: `.nav__links { display: none }` at ≤768px
with no hamburger at all and no JS — the nav simply vanishes.

Cheapest correct fix, keeps both files script-free (rule 3):

```css
@media (max-width: 768px) {
  .nav__hamburger { display: none; }              /* remove the lie */
  .nav__links {
    display: flex; gap: 1rem; font-size: 0.8rem;
    overflow-x: auto; -webkit-overflow-scrolling: touch;
  }
}
```

Delete the `<button class="nav__hamburger">` markup from `blog/index.html:208` while
you are there. Leave `index.html` alone — its hamburger is the one that works.

### R3. Hero meta text unreadable on 8 of 10 gradients

Two different fixes, because two different things are wrong.

**(a) The 11 dark-enough gradients — just drop the alpha.** In these files, solid
white clears AA (green `#047857` 5.48:1, teal `#0f766e` 5.47:1, automated-testing
`#4338ca` 7.90:1, auth `#3730a3` 9.93:1, gitops `#4c1d95` 10.95:1, github `#21262d`
15.22:1):

```css
.post-hero__meta { color: #fff; }   /* was rgba(255,255,255,0.6) */
```

**(b) The 4 light-end-stop gradients need a scrim.** In
`blog/cloud-architecture.html` (`#38bdf8`), `blog/deployment-hosting.html`
(`#06b6d4`), `blog/claude-code-architecture.html` (`#a78bfa`) and
`blog/frontend-performance.html` (`#818cf8`), no alpha value works — solid white is
2.14–2.98:1. Layer a black scrim over the existing gradient and keep the palette:

```css
.post-hero {
  background:
    linear-gradient(rgba(0,0,0,.35), rgba(0,0,0,.35)),
    linear-gradient(135deg, #0369a1 0%, #0284c7 40%, #38bdf8 100%);
}
.post-hero__meta { color: #fff; }
```

With a 0.35 scrim and solid white the worst stop becomes **4.75:1** (cloud) and every
other gradient is above it. Apply the same treatment to
`blog/openclaw-memory-architecture.html:22` (`#14b8a6`, currently `rgba(255,255,255,.7)`)
and `blog/vibe-coding-devops-process.html:23` (`#06b6d4`, currently
`rgba(255,255,255,.75)`).

Ignore the frequently-repeated claim that `rgba(255,255,255,0.92)` fixes this. It
does not: on `#38bdf8` it is 2.02:1.

### R4. Palette contrast on light backgrounds

Apply per use site, not by redefining the token. **Do not change `--gray` globally** —
`.footer span` at `blog/index.html:145` uses `var(--gray)` on `--navy #0f172a` where
`#94a3b8` is a healthy 6.96:1, and any value dark enough to pass on white
(`#64748b` → 4.76:1) drops the footer to 3.75:1 and fails. The often-suggested
`#6b7a8f` is not a fix either: 4.37:1 on white, still a fail.

```css
/* blog/index.html — light-background text */
.card__tag,
.card__read,
.series-count,
.blog-hero__stat strong  { color: var(--blue-dark); }    /* #4f46e5  5.16–6.29:1 */
.blog-hero__label        { color: #4338ca; }             /* 5.30:1 on #c7d2fe */
.blog-hero__sub          { color: #475569; }             /* 5.08:1 on #c7d2fe */
```

(`.card__series`, defined at `blog/index.html:135` with `var(--gray)` at 2.56:1, is
a dead rule — the class appears 0 times in markup, so it never renders. Recolour to
`var(--slate-light)` only if the element is ever added, or delete the rule.)

Same substitution for `.post-series-footer { color: var(--gray) }`, present in **22**
post files on `#fff`/`#f8fafc` at 2.56:1/2.45:1 — switch those to `var(--slate-light)`.
(`blog/claude-code-architecture.html` uses the class with no rule for it — nothing to
change there.)
On the 9 posts with the light `#e8f0fe → #ddd6fe → #c7d2fe` hero (kubernetes,
git-branching, cicd-pipeline, docker-vs-vms, infrastructure-as-code, linux-command-line,
monitoring-observability, networking-fundamentals, api-request-lifecycle),
`.post-hero__meta { color: var(--slate-light) }` is 3.19:1 — change to `#475569`, and
`.post-hero__series { color: var(--blue) }` is 2.99:1 — change to `#4338ca`.

### R5. Missing focus, reduced-motion and skip-link infrastructure

0 `:focus-visible` rules, 0 `prefers-reduced-motion` blocks, 0 skip links, against 64
`transition:` declarations, `scroll-behavior: smooth` in 27 files and one infinite
animation (`pulseArrow`, `blog/openclaw-migration.html:54`).

Worst case is `index.html`: `style.css:48-52` hides 9 elements behind
`[data-reveal] { opacity: 0 }` and only `script.js`'s IntersectionObserver reveals
them. If JS fails, a third of the landing page is permanently invisible, and there is
no `<noscript>` anywhere on the site.

Paste `assets/a11y-block.css` into every `<style>` block, and the skip-link anchor
after each `<body>`. The reduced-motion block in it includes
`[data-reveal] { opacity: 1 !important }`, which doubles as the no-JS safety net for
`style.css`.

### R6. Semantics and labels

Ordered by how much they degrade a screen-reader pass:

- **Card link accessible names run 216–381 characters (median 260).** The whole card is one `<a>`, so
  the name reads cover alt + 3 tags + title + excerpt + avatar alt + author + "Read →".
  Fix: heading-level the title, scope the link to it, keep the card clickable with a
  stretched pseudo-element.
  ```html
  <div class="card">
    <div class="card__image">
      <img src="../images/openclaw-101-cover.png" alt="" width="352" height="220"
           loading="lazy" decoding="async">
    </div>
    <h4 class="card__title"><a href="openclaw-101.html" class="card__link">Title…</a></h4>
  </div>
  ```
  ```css
  .card { position: relative; }
  .card__link::after { content: ""; position: absolute; inset: 0; }
  ```
  Use `<h4>`, not `<h3>` — Task 11 (2026-08-10) already gave `blog/index.html` a real
  ladder (`h1` page title → `h2` ×3 category titles → `h3` ×2 `.series-title` headings
  → `h4` ×37 `.card__title`s, verified with
  `python3 -c "import re,collections; s=open('blog/index.html').read(); print(collections.Counter(int(m.group(1)) for m in re.finditer(r'<h([1-6])\b[^>]*>', s)))"`
  → `{1: 1, 2: 3, 3: 2, 4: 37}`), so wrapping a card title in `<h3>` would re-collide it
  with the series headings it sits under. The flat-outline problem this bullet used to
  describe (39 `<h2>` / 0 `<h3>`, card titles siblings of `.series-title`) is already
  fixed by that ladder; this bullet is now only about the long accessible-name problem.
- **Decorative alts.** Set `alt=""` on the 37 identical `alt="Anirach"`
  `.card__avatar` images, and on any cover whose adjacent heading repeats the words.
  Replace the 4 noise alts ending in "Cover" (`openclaw-101.html:383`,
  `openclaw-memory.html:331`, `openclaw-agent-teams.html:445`,
  `openclaw-skills.html:267`) with a description of the image or `alt=""`.
- **Wrong image.** `blog/index.html:492` shows `../images/monitoring-cover.jpg` with
  `alt="OpenClaw Memory Architecture"` on the memory-architecture card. The alt
  describes the post, not the picture. Either give the post its own cover or fix the alt.
- **`<main id="main">`** in the 31 files that lack it.
- **`<nav>` for the two in-post nav patterns.** `<div class="series-nav">` (7 numbered
  OpenClaw posts) and `<div class="post-nav">` (DevOps posts) are both `<div>`, so
  neither is a navigation landmark. Make them `<nav aria-label="ซีรีส์ OpenClaw">` /
  `<nav aria-label="โพสต์ก่อนหน้า/ถัดไป">` and put `aria-current="page"` on the
  current chip — today it's a bare `<span class="current">#4 Security & Access</span>`
  (e.g. `blog/openclaw-security.html:1106`), written on disk with a literal `&`.
- **8 emoji icons announced as content.** Add `aria-hidden="true"` to the 6
  `.research__icon` divs at `index.html:87-117` and the 2 `.series-icon` spans at
  `blog/index.html:232,570`. `index.html:37` and `:61` already do this correctly.
- **21 `target="_blank"` links, 0 with `rel`.** Add `rel="noopener noreferrer"`.
- **Two `<h1>` in `blog/deployment-hosting.html`** — line 164 (`.post-hero__title`)
  and line 176. Demote line 176 to `<h2>`.
- **`h2 → h4` skips** in 11 posts, plus `h1 → h3` in `blog/openclaw-integrations.html`
  (h1 at line 272, next heading is h3 at line 282). Full list in
  `references/n-file-edits.md`.

### R7. Stale counters in `blog/index.html`

| Line | Says | Actual |
|---|---|---|
| 221 | `<strong>33</strong> Articles` | **37** |
| 235 | `12 articles` (`#series-openclaw`) | **13** |
| 573 | `24 articles` (`#series-devops`) | 24 ✓ |

```bash
grep -c 'class="card"' blog/index.html   # → 37
```

This is the step that is always forgotten. It is item 1 on
`assets/new-post-checklist.md` for that reason.

### R8. Dead font weights

27 files request
`Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600`.
Inter 300 is loaded by 29 files and used by exactly one — `index.html`, via
`style.css:231, 311, 365, 438, 485`. It is dead weight in the other 28; never trim
300 from `index.html`'s Inter-only URL or five headings silently re-render at 400.
JetBrains Mono **500** is unused. Mono **600** is used once —
`blog/sre-fundamentals.html:89` `.slo-card__example` — so either keep `wght@400;600`
for the mono family, or restyle that one rule to 700 (already loaded) before
trimming to `wght@400`. The trim below targets only the 27 dual-family blog files,
which use no weight 300:

```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400&display=swap" rel="stylesheet">
```

Keep the two `preconnect` lines and `display=swap` — already correct on 29/29.

---

## The motivating example

`blog/frontend-performance.html` tells readers to use `srcset` (line 1025),
`font-display` (1059), `<link rel="preload">` for fonts (1236) and "max 2 fonts"
(1350). Its own `<head>` at lines 8–10 loads 10 weights across 2 families, and its
only image at line 214 is:

```html
<img src="../images/frontend-performance-cover.jpg" alt="Frontend Performance & Modern Frameworks">
```

No `width`, no `height`, no `loading`, no `srcset`. Fix that page first when
demonstrating rule 2 — it is the most persuasive argument this skill can make.

---

## Files in this skill

- `assets/a11y-block.css` — the focus-visible, reduced-motion and skip-link CSS to
  paste into every `<style>` block. Open it whenever you touch a page's CSS.
- `assets/new-post-checklist.md` — run through this before committing a new post in
  `blog/`. It extends the "Adding a New Blog Post" flow in `CLAUDE.md`, which omits
  every a11y/perf step.
- `references/contrast.md` — every computed contrast pair on the site, the gradient
  scrim table, and the Python snippet to compute new ones. Open before choosing any
  colour.
- `references/n-file-edits.md` — verified loops and `sed` scripts for the sitewide
  edits, the exact file lists, and the grep commands that prove a fix landed. Open
  before any change that touches more than three files.
