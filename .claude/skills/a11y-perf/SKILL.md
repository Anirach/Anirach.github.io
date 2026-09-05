---
name: a11y-perf
description: Accessibility and performance rules for the anirach.com static site (86 hand-written HTML files, no build step, per-file embedded CSS). Use this whenever you touch any .html file in this repo, add or edit a blog post under blog/, add or swap an image in images/, edit a :root palette or a .post-hero gradient, change nav markup, or are asked about contrast, alt text, focus states, keyboard access, page weight, image size, fonts, or Lighthouse/Core Web Vitals — even if the user does not mention accessibility or performance at all, and even for a "just add a card to blog/index.html" request. It carries this site's real measured numbers (blog/index.html is 3.43 MB referenced across 153 img tags, every one lazy except the featured LCP card (2026-09-05: the 20-post AI Transformation series); the palette was re-keyed to the book covers 2026-08-26 so --blue #226299 now PASSES as text, while --blue-light is borders-only and the focus ring is scoped; the :focus-visible/reduced-motion/color-scheme baseline is landed in 86/86 pages; .post-hero__meta and .post-series-footer contrast are both DONE as of 2026-08-26) plus verified drop-in fixes, so use it instead of deriving generic WCAG advice.
---

# Accessibility & performance for anirach.com

This site has no build step, no partials and no tests. Every page in `blog/` carries
its own `<style>`, its own `:root` and its own copy of the nav. A "global" fix is an
N-file edit, and nothing catches a regression except you. That is why these rules are
written as concrete values you can paste, not principles you have to re-derive.

Everything below was measured on this repo. Re-run the command if you doubt a number.

> ## Standing rule — numbers in this skill are load-bearing
>
> **Any change that invalidates a number in a skill file must update that number in
> the same commit.** This file exists to save the next session from re-deriving
> measurements; a confidently wrong measurement is worse than none, because it gets
> acted on. Three sitewide sweeps (`6670480`, `ec2827b`, `e8da9da`) landed without
> touching this file, which is how it spent a session claiming "0 `:focus-visible`
> rules" and "0 of 118 images have `loading`" about a repo with 42 focus blocks and
> 120/120 fully attributed images.
>
> **Last full re-measure: 2026-08-24 against `7daf3a4`** (One Day of Light — the site is 47
> files now: `books/one-day-of-light.html` joined as a fourth `books/` detail page, with two
> downloadable PDFs in `books/` and two paired-edition covers in `images/`; the same-day dual-cover
> sweep then gave every `books/` title both language faces — 8 suffixed cover files). Every count below has its
> command next to it. If you sweep, re-run them and edit this file in the same commit.

## What is DONE — do not re-plan these

`ec2827b` + `21c8a55` (covers), `e8da9da` (a11y/perf baseline) and `b9fb125` (counters,
dead links) closed most of the original remediation list. Marked below as **[DONE]**.
The genuinely outstanding work is **R4 (palette contrast on light backgrounds)** and
**R6 (semantics, labels, landmarks, heading skips)** — plus skip links and `<main>`,
which are the unfinished half of R5. **R3 (hero-meta contrast) closed 2026-08-26**; so
did **R8**, whose premise turned out to be backwards — the fix was *adding* the two
Sarabun weights the site was synthesising, not trimming variable-font weights that cost
nothing.

---

## Standing rules — apply when writing or editing any page

### 1. Covers ship as JPEG at ≤200 KB. Never PNG. **[DONE — hold the line]**

`ec2827b` re-encoded the 15 oversized PNG covers to JPG and `21c8a55` re-ran the four
that still cleared 200 KB at `formatOptions 70`; the three 2026-08-23 book covers shipped
compliant. Today there are **0 PNG covers and 85
JPG covers (77 `*-cover.jpg` + 8 suffixed), average 46 KB, largest 174 KB, none over 200 KB.**

```bash
ls images/*-cover.png 2>/dev/null | wc -l                     # → 0
find images -name '*-cover.*' -size +200k                     # → nothing
ls -l images/*-cover.jpg | awk '{s+=$5;n++} END {print n" jpg, avg "int(s/n/1024)" KB"}'
# → 77 jpg, avg 42 KB    (unsuffixed only — see the blind spot below)
```

Before adding a cover, run `ls -lS images/ | head` and compare. Hard-fail any cover
over 200 KB. To produce one:

```bash
sips -s format jpeg -s formatOptions 70 -Z 1600 new-cover.png --out images/new-cover.jpg
```

PNG is correct for the five *diagram* images only — `*-arch.png`, `*-flow.png`,
`*-levels.png` — which are right at 123–235 KB. Do not convert those; PNG preserves the
crisp lines that a JPEG smears. (Diagrams are PNG for a reason: inline HTML/CSS and
ASCII-art diagrams were tried and reverted in f4f7e1b, 4fc85af, c270892 and 4ae2660
because they kept breaking layout.)

**Blind spot in the census above:** the eight paired book faces —
`one-day-of-light-cover-en/-th.jpg` (67 KB each), `a-pocketful-of-questions-cover-en/-th.jpg`
(73 / 77 KB), `the-thirteenth-seal-cover-en/-th.jpg` (54 / 62 KB) and
`three-old-men-cover-front/-back.jpg` (175 / 120 KB) — end in `-cover-<face>.jpg` and so match
neither the `*-cover.jpg` ls nor the `*-cover.*` find. Audit them with
`ls -l images/*-cover-*.jpg` (→ 8 files, avg 86 KB, all compliant).

**Downloadable PDFs live in their section's directory** (the
`books/one-day-of-light-en.pdf` pattern), **≤10 MB each, metadata set (Title/Author)**.
`check_site.py` INV-05 verifies each PDF `href` resolves; **no orphan scan covers PDFs**
— INV-06a reads `images/` only — so every PDF must stay referenced, and removing a page
removes its PDFs in the same commit.

### 2. Every `<img>` gets `width`, `height`, `loading` and `decoding`. **[DONE — hold the line]**

**299 of 299 `<img>` tags carry all four**, since `e8da9da` (the books/publications pages
and `books/one-day-of-light.html` shipped compliant). 83 also carry
`fetchpriority`. This and `alt` coverage are the only two 100%-complete practices on the
site; a new post that omits them is a regression, not a gap.

```bash
python3 - <<'EOF'
import re, pathlib
n=ok=0
for p in pathlib.Path('.').rglob('*.html'):
    if '.claude' in p.parts or '.git' in p.parts: continue
    for m in re.finditer(r'<img\b[^>]*>', p.read_text(encoding='utf-8'), re.S):
        n+=1; ok+= all(a+'=' in m.group(0) for a in ('loading','decoding','width','height'))
print(ok, "/", n)          # → 299 / 336
EOF
```

**Use that multiline parse, not `grep -oh "<img[^>]*>"`** — the line-based grep reports
316 against the parse's 336, because 20 `<img>` are written across multiple lines (mostly on the
books/publications pages). Both totals also count a literal `<img>` written inside a CSS comment in
37 posts, which is not a tag: **the real tag count is 299, and all 299 are compliant.** Quoting
316, or 336, where the answer is 299 is exactly the kind of small wrongness that makes a reader
stop trusting this file.

Card images in `blog/index.html` sit in a 352×220 CSS px slot (1200px section −
2×2.5rem padding = 1120; `repeat(auto-fill, minmax(340px,1fr))` with `gap:2rem` →
3 cols of 352px; `.card__image { aspect-ratio: 16/10 }` → 220px). Source covers are **800×800 on all 76 post covers** (the 77th `*-cover.jpg` is the Springer jacket, `libraries-in-transformation-cover.jpg` at 306×461) as of 2026-08-26 — the drawn cover
system (`scripts/make_cover.py` + `scripts/covers.tsv`) replaced 35 AI clip-art
images at mixed canvases (1024×1024, 1024×680, 800×446, …) with one. `object-fit:
cover` into the 16:10 slot throws away 37.5% of a square source, which is why the
renderer keeps every glyph and every motif inside a SAFE BAND of y∈[0.20,0.80],
x∈[0.12,0.88]; the crop eats only ground. Check
the actual file with `sips -g pixelWidth -g pixelHeight` before quoting a waste figure.

```html
<!-- blog/index.html card: below the fold, fixed slot -->
<img src="../images/openclaw-101-cover.jpg" alt="" width="800" height="800"
     loading="lazy" decoding="async">

<!-- post hero cover: above the fold, do NOT lazy-load the LCP element -->
<img src="../images/openclaw-101-cover.jpg" alt="OpenClaw 101 architecture overview"
     width="800" height="800" loading="eager" fetchpriority="high" decoding="async">
```

`width`/`height` are the **source** pixel size, not the CSS slot size — that is the
convention already on disk (the live card for this cover writes `1024`×`1024`), and it
is what makes the intrinsic aspect ratio correct. Get it from
`sips -g pixelWidth -g pixelHeight images/<file>`. **Every cover is `.jpg` now**; there
are no `-cover.png` files left.

### 3. No page except `index.html` may ship a control that needs JavaScript.

`index.html` is still the only file on the site with a `<script>`:

```bash
grep -rl "<script" --include="*.html" --exclude-dir=.claude .   # → index.html
```

`script.js` binds `document.getElementById('hamburger')`, an id that exists only in
`index.html`. A hamburger *button* pasted into any other page is decorative scenery over
a hidden menu.

**Task 9 solved this properly and the pattern is now the house standard.** The 9
island-chrome pages (the 5 listing pages `blog/`, `books/`, `news/`, `projects/`,
`publications/` plus the 4 `books/*.html` detail pages) each carry a pure-CSS toggle — a
visually
hidden `<input type="checkbox" id="navToggle" class="nav__toggle">`, a
`<label for="navToggle" class="nav__burger">☰</label>`, and
`.nav__toggle:checked ~ .nav__links { display: flex; }` inside the 800px media query
(moved up from 768px in `5178252`: the 6-link desktop bar broke in the 769–771px band). No
JS, keyboard-operable, and `.nav__toggle:focus-visible + .nav__burger` gives the label a
visible ring. `check_site.py` INV-12 ("every menu-toggle control is wired: JS toggles need
`<script>`, CSS toggles need their label+checkbox pair") PASSes today and has **no
baseline entry**, so a regression will fail.

Copy that pattern. Never ship a `<button class="nav__hamburger">` outside `index.html`.

### 4. `--blue #226299` is a TEXT colour now. `--blue-light` is borders only. **[RE-KEYED 2026-08-26]**

> **`.post-series-footer` and `.post-hero__meta` are DONE (2026-08-26, whole-site Phase 1).**
> The 22 `.post-series-footer` rules that read `var(--gray)` at 2.40:1 are now `var(--slate-light)`
> (5.91:1), and the 24 `.post-hero__meta` rules that read `rgba(255,255,255,0.6–0.95)` are now
> `#fff` — 5.47–7.68:1 on every surviving dark family. The 9 Sunrise posts keep
> `var(--slate-light)` on cream and are correct. R3 and R4's paragraphs below are HISTORY.

Still fully outstanding — this is the largest live a11y defect on the site.

**This rule inverted on 2026-08-26.** The palette was re-keyed to the book covers, and the token
that used to be the site's largest a11y defect now passes everywhere: `--blue #226299` is 6.41:1 on
white, 5.99 on the `--bg` cream, 5.09 on cloud and 4.90 on parchment — links, chips and small text
are all legal. `--blue-dark #1a4d7a` is 8.80:1 and stays the hover/pressed state.

**Two roles need care, both verified live:**
- `--blue-light #4992b9` is **borders only** (3.45:1 on white, 3.94 on navy). Its 32 former uses
  were all footer link text; they moved to `--gold` (5.73:1 on the new navy).
- The focus ring carries `outline-offset: 3px`, so it lands on the *page* ground. Inside a navy
  footer `--blue` collapses to 2.12:1, so a 28th token exists: `--focus`, re-pointed by
  `.footer, .blog-footer, pre { --focus: var(--gold) }`.

Historical, for context — the old value's failures, which is why the re-key happened:
`--blue #6366f1` failed WCAG AA in **every** light-background use: 4.47:1 on white,
4.09:1 on the tag chip, 3.87:1 on the series-count chip, 3.90:1 and 2.99:1 on the two
ends of the old hero gradient.
`var(--blue)` is used 279 times against `var(--blue-dark)`'s 60; most of those 279 are
legitimately borders and backgrounds, but every *text* use is a fail. (The 2026-08
section pages and `style.css`'s `.btn--primary`/`.nav__cta` already made the
`--blue-dark` switch, which is most of why its count rose from 23 to 60.)

That gradient no longer exists either — the light family is now the sunrise
`#eef3f3 → #dee7e6 → #e9e1c4`, on which `--navy` measures 10.4–11.3:1 (measured live on the
landing hero). `references/contrast.md` still holds the OLD palette's table and is stale.

### 5. A visible focus ring exists everywhere. **[DONE]** Hover/focus parity **[DONE 2026-08-26]**

`e8da9da` installed this block, and the books/publications pages shipped with it — today it
is in **47 embedded `<style>` blocks + `style.css`** = all 48
pages:

```css
:focus-visible { outline: 2px solid var(--blue); outline-offset: 3px; border-radius: 2px; }
:focus:not(:focus-visible) { outline: none; }
```

```bash
grep -L ':focus-visible' style.css blog/*.html books/*.html news/index.html projects/index.html publications/index.html
# → empty.  index.html correctly has none of its own: its CSS is style.css.
```

**Two things this changes about how you must report focus problems.**

1. **`outline: none` now exists, 47 times, and it is correct.** It is scoped to
   `:focus:not(:focus-visible)`, i.e. it suppresses the ring for mouse and programmatic
   focus only, never for keyboard. The old advice in this file — "`outline` is never set
   to `none` anywhere, verify before claiming a focus failure" — will now find 47 matches
   and mislead you into the opposite error. Read the selector, not the declaration.
2. **Parity landed 2026-08-26.** There are **227 `:hover` rules** (the old figure of 144 was
   an undercount). `.card:focus-within` — plus `.research__card` / `.projects__card` on the
   landing — now mirror the lift, the image scale and the colour shift across 7 files, so a
   keyboard user gets the same affordance a mouse user does.

`assets/a11y-block.css` holds the parity rules (`.card:focus-within` lift, the skip link)
that are still *not* on disk. It deliberately does **not** repeat the ring — that shipped.

### 6. Text on a dark hero must clear AA against the gradient's **lightest** stop.

Still outstanding, unchanged by any sweep. `rgba(255,255,255,0.6)` is **still** the
`.post-hero__meta` colour in **15** files (plus `.7` and `.75` variants in the two
minified posts) and it fails on 8 of the 10 gradients in use, down to 1.57:1 on
`#38bdf8`. Raising the alpha does not save the light gradients — solid `#ffffff` on
`#38bdf8` is still only **2.14:1**. Anything below roughly `#4c1d95` lightness needs the
gradient darkened, not the text brightened. See R3 and `references/contrast.md`.

```bash
grep -rhoE '\.post-hero__meta *\{[^}]*color: *[^;]+' blog/*.html \
  | grep -oE 'color: *[^;]+' | sort | uniq -c      # → 15× rgba(255,255,255,0.6), +2 minified
```

### 7. Thai page, English headings — mark the switch.

**37 of 47** files are `<html lang="th">` (the 10 `en` files: the landing page, the 5 section
indexes, and the 4 `books/` detail pages), with English
headings, code and technical terms. The `en` pages now do this right — they wrap their Thai
passages in `<span lang="th">` (61 switches across the 10 files) — but the 37 Thai posts still
have **zero** inline `lang="en"` switches on their English headings.
A Thai screen-reader voice reading "Kubernetes Orchestration" is unintelligible.
`check_site.py` INV-13 enforces the page-level split; nothing enforces the inline one.

```bash
grep -rhoE '<html lang="[^"]*"' --include="*.html" --exclude-dir=.claude . | sort | uniq -c
# → 10 en, 37 th
```

```html
<h2 lang="en">Kubernetes Orchestration</h2>
<pre lang="en"><code>kubectl apply -f deploy.yaml</code></pre>
```

### 8. One `<h1>`, no level skips, content in `<main id="main">`.

The default failure mode here is `h2 → h4`: **12 of 37 posts** do it, plus one `h1 → h3`
in `blog/openclaw-integrations.html` — **13 posts with a heading defect**, one of which
(`deployment-hosting.html`) is the two-`<h1>` case rather than a skip. `<main>` exists in
**16 of 47** files, and the 5 `books/` pages (index + 4 detail, `ea3c8e8` + `7daf3a4`) are the only ones
with `<main id="main">` — the other 11 `<main>`s still lack the `id`, so a sitewide skip
link still has no
target. When copying an existing post as a template, check its heading ladder first — you
will inherit the skip.

```bash
python3 - <<'EOF'
import re, pathlib
for p in sorted(pathlib.Path('blog').glob('*.html')):
    if p.name == 'index.html': continue
    lv=[int(m.group(1)) for m in re.finditer(r'<h([1-6])[\s>]', p.read_text(encoding='utf8'))]
    sk=[(a,b) for a,b in zip(lv,lv[1:]) if b>a+1]
    if sk or lv.count(1)!=1: print(f"{p.name:40s} h1x{lv.count(1)} skips={len(sk)}")
EOF
```

`blog/index.html` itself is **clean** since Task 11 — `Counter({4: 37, 2: 3, 3: 2, 1: 1})`,
a real `h1 → h2 → h3 → h4` ladder. Do not "fix" its card titles back to `h2`/`h3`.

### 9. Don't "fix" what is already correct.

These are right; flagging them wastes the user's time:

- `display=swap` present on **37/37** font-loading files.
- Both `preconnect` links present on **37/37**.
- `<meta name="viewport" content="width=device-width, initial-scale=1.0">` identical on
  all **47** files — pinch-zoom is not blocked.
- All **137/137** `<img>` tags have an `alt` attribute (the *quality* is the problem, not
  the presence) **and** `loading`, `decoding`, `width`, `height`.
- `:focus-visible`, `prefers-reduced-motion`, `color-scheme: light` and `text-wrap:
  balance` on all 48 pages (47 embedded + `style.css`) — rule 5.
- `outline: none` scoped to `:focus:not(:focus-visible)` — correct, not a defect.
- `script.js:12` guards the scroll work with
  `window.matchMedia('(prefers-reduced-motion: reduce)').matches`.
- All 5 counters in `blog/index.html` and every absolute route — `check_site.py` INV-02a–e
  and INV-05 all PASS.
- The pure-CSS `.nav__toggle` menu on the 9 island-chrome pages — rule 3.
- The whole-card anchors on `books/index.html` carrying
  `aria-labelledby="card-title-<slug>"` so the accessible name is the title, not the
  card's entire text (`5178252` + `7daf3a4`, 4 cards) — a different mechanism from R6's
  stretched-link recipe, but it solves the same long-accessible-name defect; leave it.
- Every cover is JPG and under 200 KB — rule 1.
- `index.html` having no embedded `<style>` block. Prove it with
  `grep -c '</style>' index.html` → `0`; `grep -c '<style'` returns 1 because of a comment
  saying exactly this.
- Embedded `<style>` avoids an extra round trip; 5–16 KB is a fine cost.

### 10. State the file count before starting, and script the edit.

There are no partials. **The site is 87 HTML files** — 86 enumerated by `check_site.py` plus `404.html`, which it deliberately skips. Before proposing a sitewide change,
count and say the number out loud so the user can judge scope:

```bash
find . -name "*.html" -not -path "./.git/*" -not -path "./.claude/*" \
     -not -path "./.bilingual/*" | wc -l                                    # → 87
```

| Change | Files still needing it |
|---|---|
| Palette / `:root` patch | **0** — landed in all 47 (`6670480` + the compliant 2026-08 pages) |
| `:focus-visible` + reduced-motion + `color-scheme` + `text-wrap` | **0** — landed in 47 + `style.css` (`e8da9da`, plus `404.html`) |
| `<main id="main">` wrap | **42** — 31 have no `<main>`, 11 have one without the `id`; only the 5 `books/` pages are done |
| Skip link | **47** — 0 exist; the 5 `books/` pages now have the `id="main"` target, the other 42 do not |
| `.post-hero__meta` colour | 15 (+2 minified variants) |
| `.post-series-footer` colour | 22 |
| Font URL trim | 27 |
| `rel="noopener"` | 12 links across 6 files |

Write a loop or `sed` script, never 47 sequential Edit calls. The 2026-08-26 metadata
sweep is the worked example: one idempotent Python pass rewrote a delimited `<head>` block
in all 47 pages, and `check_site.py` INV-27 verifies the result rather than trusting it.

**The old "`sed` on `:root` misses 11 files" warning is obsolete** — every file except
`index.html` now has a `:root`, and `index.html`'s lives in `style.css`. What is still
true about those same 10 island posts is that they **load no webfont** and declare their
own stacks (`'Segoe UI', Tahoma, Geneva, Verdana` in `blog/openclaw-memory.html`;
`-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto` in `blog/beyond-plugins.html`), so
the Inter design system does not reach them: **38 of 48 files load Google Fonts, 10 do
not.** Loops and verification commands: `references/n-file-edits.md`.

---

## Remediation — outstanding defects, worst first

### R1. `blog/index.html` page weight — **[DONE]**

Was 18.41 MB, then 4.07 MB, then 2.47 MB. Now **3.43 MB of referenced bytes, every one of
the 153 `<img>` tags lazy except one** — the 20-post AI Transformation series (2026-09-05)
added 20 drawn covers and a share card, and the featured card at the top of the page is
deliberately `loading="eager" fetchpriority="high"`, because it is the LCP element.

```bash
python3 - <<'EOF'
import re, os
s=open('blog/index.html',encoding='utf-8').read()
tags=re.findall(r'<img\b[^>]*>', s, re.S)
u={}
for t in tags:
    f=os.path.normpath(os.path.join('blog', re.search(r'src="([^"]+)"',t).group(1)))
    u[f]=os.path.getsize(f)
h=os.path.getsize('blog/index.html')
print(f"img tags {len(tags)}  unique {len(u)}  lazy {sum('loading=\"lazy\"' in t for t in tags)}")
print(f"html {h:,}  images {sum(u.values()):,}  total {h+sum(u.values()):,}")
EOF
# → img tags 153  unique 78  lazy 152
#   html 149,637  images 3,444,584  total 3,594,221   (3.43 MiB)
```

Three numbers matter and they are not the same number — quote the right one:

| Figure | Value | Meaning |
|---|---|---|
| referenced total | **3.43 MB** | every byte the page can eventually pull. Was 18.41 MB, then 4.07 MB, then 1.59 MB, then 2.47 MB. |
| eager payload | **206 KB** | the HTML (146 KB) plus the single eager image, the featured share card (60 KB). **The other 152 `<img>` tags are `loading="lazy"`**, so nothing else is fetched up front. |
| realistic first viewport | **≈0.65 MB** | HTML + the feature + the first ~10 cards' covers, which a browser fetches because lazy images near the viewport still load. |

Saying "the blog index is 3.4 MB" overstates what a visitor downloads by ~5×; saying
"146 KB" understates it. Say 3.43 MB referenced / ≈0.65 MB first viewport.

`ec2827b` + `21c8a55` did the cover re-encode; `e8da9da` added the attributes. Heaviest
posts now: `blog/idle-self-improvement.html`, `openclaw-migration.html`,
`obsidian-ai-jarvis.html` — each ~190 KB of cover plus <43 KB of HTML, not ~1.7 MB.

### R2. Mobile navigation — **[MOSTLY DONE]**

The `blog/index.html` dead hamburger is **gone**. Task 9 (`ad3c42d`, `c25c682`) replaced
it with the pure-CSS checkbox toggle now shared by all 9 island-chrome pages (rule 3), and
`check_site.py` INV-12 guards it with no baseline entry:

```bash
grep -rn 'nav__hamburger' --include='*.html' --exclude-dir=.claude .
# → index.html only, and that one is wired to script.js
```

**Still outstanding — one file.** `blog/obsidian-ai-jarvis.html` hides
`.nav__links { display: none; }` inside `@media (max-width: 768px)` with no toggle of any
kind and no JS. Its nav simply vanishes on a phone. It is an ISLAND file, so it did not
get the listing-page toggle. Cheapest correct fix, keeping it script-free:

```css
@media (max-width: 768px) {
  .nav__links {
    display: flex; gap: 1rem; font-size: 0.8rem;
    overflow-x: auto; -webkit-overflow-scrolling: touch;
  }
}
```

or port the `.nav__toggle` + `.nav__burger` pair from `blog/index.html`. Leave
`index.html` alone — its hamburger is the one that works.

### R3. Hero meta text unreadable on 8 of 10 gradients — **[OUTSTANDING]**

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

### R4. Palette contrast on light backgrounds — **[OUTSTANDING]**

Apply per use site, not by redefining the token. **Do not change `--gray` globally** —
`.footer span` uses `var(--gray)` on `--navy #11304b` where `#94a3b8` is a healthy 5.29:1, and any value dark enough to pass on white
(`#64748b` → 4.76:1) drops the footer to 3.75:1 and fails. The often-suggested
`#6b7a8f` is not a fix either: 4.37:1 on white, still a fail.

All of these are **still on disk unchanged** — re-verified 2026-08-10. Task 11 added a
sixth site, `.category__count`, which repeats the same `var(--blue)` mistake.

```css
/* blog/index.html — light-background text */
.card__tag,
.card__read,
.series-count,
.category__count,
.blog-hero__stat strong  { color: var(--blue-dark); }    /* #1a4d7a  8.80:1 */
.blog-hero__label        { color: #4338ca; }             /* 5.30:1 on #c7d2fe */
.blog-hero__sub          { color: #475569; }             /* 5.08:1 on #c7d2fe */
```

(`.card__series`, declared with `var(--gray)` at 2.56:1, is a dead rule — the class
appears 0 times in markup, so it never renders. Recolour to `var(--slate-light)` only if
the element is ever added, or delete the rule. Find it with
`grep -n 'card__series' blog/index.html`; do not trust a line number here, the file has
been re-cut twice.)

Same substitution for `.post-series-footer { color: var(--gray) }` — a block-aware parse
found **22 rules on `var(--gray)`** at 2.40:1 on the cream ground. **All 22 were
switched to `var(--slate-light)` (5.91:1) on 2026-08-26** — this command should now
print `{'var(--slate-light)': 22}`.
Switch them to `var(--slate-light)`. A line-based grep reports 13 here because 9 of the
rules span lines; use the parse:

```bash
python3 -c "
import re,glob,collections
c=collections.Counter()
for f in glob.glob('blog/*.html'):
    for m in re.finditer(r'\.post-series-footer\s*\{([^}]*)\}', open(f,encoding='utf-8').read()):
        cm=re.search(r'color:\s*([^;]+)', m.group(1)); c[cm.group(1).strip() if cm else 'none']+=1
print(dict(c))"          # → {'var(--gray)': 22}
```
(`blog/claude-code-architecture.html` uses the class with no rule for it — nothing to
change there.)
On the 9 posts with the light `#e8f0fe → #ddd6fe → #c7d2fe` hero (kubernetes,
git-branching, cicd-pipeline, docker-vs-vms, infrastructure-as-code, linux-command-line,
monitoring-observability, networking-fundamentals, api-request-lifecycle),
`.post-hero__meta { color: var(--slate-light) }` is 3.19:1 — change to `#475569`, and
`.post-hero__series { color: var(--blue) }` is 2.99:1 — change to `#4338ca`.

### R5. Focus and motion infrastructure — **[DONE]**; skip links and `<main>` — **[OUTSTANDING]**

**Landed in `e8da9da`:** `:focus-visible` (47 pages), `prefers-reduced-motion` (47),
`color-scheme: light` (47), `text-wrap: balance` (47), and the `matchMedia` guard at
`script.js:12` for the scroll work CSS cannot reach. That covers **143 `transition:`
declarations, 52 `translateY` lifts, `scroll-behavior: smooth` in 35 files** and the one
infinite animation (`pulseArrow`, `blog/openclaw-migration.html`).

**Still missing, and they are a pair — neither is useful alone:**

| Thing | Count today | Why it is blocked on the other |
|---|---|---|
| `<a href="#main" class="skip-link">` | **48 of 48 — DONE** | landed 2026-08-26 with its `<main id="main">` target |
| `<main id="main">` | `<main>` in **16 of 47**, `id="main"` in **5** (the `books/` pages, `ea3c8e8` + `7daf3a4`) | 11 `<main>`s need only the `id`; 31 files need the wrap |

Do `<main id="main">` first, then the skip link. The wrap is not safely scriptable — the
insertion point differs per file — so do a handful at a time and diff each.
`references/n-file-edits.md` has the file list and the loops.

**Also still missing: the no-JS safety net for `index.html`.** `style.css:68` hides 14
`[data-reveal]` elements behind `opacity: 0` and only `script.js`'s IntersectionObserver
reveals them. If JS fails, a third of the landing page is permanently invisible, and
there is no `<noscript>` anywhere on the site. The shipped reduced-motion block does
**not** include the `[data-reveal] { opacity: 1 !important }` override —
`assets/a11y-block.css` does, and that override is now the main reason to paste it.

### R6. Semantics and labels

Ordered by how much they degrade a screen-reader pass:

- **Card link accessible names run 216–381 characters (median 260).** The whole card is one `<a>`, so
  the name reads cover alt + 3 tags + title + excerpt + avatar alt + author + "Read →".
  Fix: heading-level the title, scope the link to it, keep the card clickable with a
  stretched pseudo-element.
  ```html
  <div class="card">
    <div class="card__image">
      <img src="../images/openclaw-101-cover.jpg" alt="" width="800" height="800"
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
  describe (a page of 39 sibling `<h2>`s and no `<h3>`) is already fixed by that ladder;
  this bullet is now only about the long accessible-name problem.
- **Decorative alts.** Set `alt=""` on the **37** identical `alt="Anirach"`
  `.card__avatar` images in `blog/index.html`, and on any cover whose adjacent heading
  repeats the words. Replace the **4** noise alts ending in "Cover" with a description or
  `alt=""` — `grep -rn 'alt="[^"]*Cover"' --include='*.html' --exclude-dir=.claude .`
  finds them in `openclaw-101`, `openclaw-agent-teams`, `openclaw-memory` and
  `openclaw-skills`.
- **Wrong image — fixed 2026-08-26.** The `openclaw-memory-architecture` card in
  `blog/index.html` used to show `../images/monitoring-cover.jpg` with
  `alt="OpenClaw Memory Architecture"` — an alt describing the post, not the picture, the
  downstream symptom of a shared cover. The drawn-cover system gave it its own
  `openclaw-memory-architecture-cover.jpg` with `alt=""`; `check_site.py` INV-07a now
  carries no baseline entry and fails on any new sharing.
- **`<main id="main">`** — 31 files have no `<main>`, 11 have one without the `id`; only
  the 5 `books/` pages are complete.
  See R5.
- **`<nav>` for the two in-post nav patterns.** `<div class="series-nav">` (7 numbered
  OpenClaw posts) and `<div class="post-nav">` (DevOps posts) are both `<div>`, so
  neither is a navigation landmark. Make them `<nav aria-label="ซีรีส์ OpenClaw">` /
  `<nav aria-label="โพสต์ก่อนหน้า/ถัดไป">` and put `aria-current="page"` on the
  current chip — today it's a bare `<span class="current">#4 Security & Access</span>`
  (find it with `grep -n 'class="current"' blog/openclaw-security.html`), written on disk
  with a literal `&`.
- **Emoji icons announced as content.** ~~the 6 `.research__icon` divs in
  `index.html`~~ — **moot 2026-08-26**: the emoji research tiles were replaced by
  numbered arcs whose marks are inline `<svg aria-hidden="true">`, so there are **0**
  `.research__icon` divs left. Still open: the 2 `.series-icon` spans in
  `blog/index.html`, which carry `aria-hidden` in **0** places.
- ~~12 `target="_blank"` anchors with no `rel`~~ — **DONE 2026-08-26, 0 remain.** All 70
  `target="_blank"` anchors sitewide now carry `rel="noopener"`.

  ```bash
  python3 -c "
  import re,pathlib
  m=[str(p) for p in pathlib.Path('.').rglob('*.html') if '.claude' not in p.parts
     for a in re.finditer(r'<a\b[^>]*>', p.read_text(encoding='utf-8'), re.S)
     if 'target=\"_blank\"' in a.group(0) and 'rel=' not in a.group(0)]
  print(len(m), sorted(set(m)))"
  ```
- **Two `<h1>` in `blog/deployment-hosting.html`** — the `.post-hero__title` and a near
  duplicate in the body. `check_site.py` INV-11 reports the current line numbers; do not
  hardcode them here, they have moved twice. Demote the second to `<h2>`.
- **Heading skips in 13 posts:** `h2 → h4` in 12, plus `h1 → h3` in
  `blog/openclaw-integrations.html`. Rule 8 has the detector; per-file counts are in
  `references/n-file-edits.md`.

### R7. Counters in `blog/index.html` — **[DONE]**

`b9fb125` fixed the two stale ones and Task 11 added two more sites. **All five are
correct today** and `check_site.py` INV-02a–INV-02e all PASS with no baseline entries:
2 Series, 37 Articles, `#cat-technology` 37, `#series-openclaw` 13,
`#series-devops` 24.

```bash
grep -c 'class="card"' blog/index.html                                # → 37
python3 .claude/skills/site-check/scripts/check_site.py | grep 'INV-02'  # → all PASS
```

It is still the step that is always forgotten on a *new* post, which is why it is item 1
on `assets/new-post-checklist.md`. **Recompute, never increment** — incrementing by hand
is how all of them went stale in the first place.

### R8. Font weights — **the premise was backwards, and the real defect is fixed**

This rule used to say: trim the unused weights (Inter 300, JetBrains Mono 500) to save bytes.
**That saving is zero.** Google Fonts serves Inter and JetBrains Mono as *variable* fonts — one
file covering the whole axis — so `wght@300;400;…;900` and `wght@400` download exactly the same
bytes. Re-measured 2026-08-26: 48 files load webfonts, all 48 request 300, and `style.css` uses
weight 300 in 6 declarations. Trimming it from the other 47 buys nothing and risks the documented
trap below.

**Sarabun is the one that mattered, and it is static.** An unrequested weight is *synthesised* by
the browser — faux-bold, which smears Thai glyphs far more visibly than Latin ones. The site
declared:

| Weight | Declarations | Was loaded? |
|---|---|---|
| 400 | 6 | yes |
| 500 | 43 | **no — synthesised** |
| 600 | 407 | yes |
| 700 | 330 | yes |
| 800 | 122 | **no — synthesised** |

Fixed on 2026-08-26 across all 48 pages:

```
Sarabun:wght@400;600;700   ->   Sarabun:wght@400;500;600;700;800
```

Verified in the browser with `document.fonts`: five real Sarabun faces now load where three did.

**Still true, and still a trap:** never trim 300 from `index.html`'s Inter URL — six headings in
`style.css` would silently re-render at 400. Keep both `preconnect` lines and `display=swap`
(correct on all 48). JetBrains Mono is on 37 files and its weight 500 is unused, but it is variable,
so removing it saves nothing either.

---

## The motivating example — now half-resolved, and better for it

`blog/frontend-performance.html` preaches `srcset`, `font-display`,
`<link rel="preload">` for fonts and "max 2 fonts" to its readers. Its own cover image
used to be:

```html
<img src="../images/frontend-performance-cover.jpg" alt="Frontend Performance & Modern Frameworks">
```

`e8da9da` fixed it, and it now reads:

```html
<img src="../images/frontend-performance-cover.jpg" alt="Frontend Performance & Modern Frameworks"
     width="800" height="800" loading="eager" fetchpriority="high" decoding="async">
```

**What is still hypocritical:** the page's own `<head>` loads 10 weights across 2
families (R8), it uses no `srcset` outside its own code samples, and it has no
`rel="noopener"` on its external links (R6). Two of the four charges have been dropped —
say so. Overstating a fixed defect is how a skill file loses its reader.

The general lesson survives the specific fix: **check the current file before quoting it
as an example of anything.**

---

## Files in this skill

- `assets/a11y-block.css` — the a11y CSS that is **not yet on disk**: the
  `.card:focus-within` hover/focus parity rules, the skip link, and the
  `[data-reveal] { opacity: 1 !important }` no-JS net. The focus ring and the
  reduced-motion block it used to carry shipped in `e8da9da`; the file no longer
  duplicates them. Open it whenever you touch a page's CSS.
- `assets/new-post-checklist.md` — run through this before committing a new post in
  `blog/`. It extends the "Adding a New Blog Post" flow in `CLAUDE.md`, which omits
  every a11y/perf step.
- `references/contrast.md` — every computed contrast pair on the site, the gradient
  scrim table, and the Python snippet to compute new ones. Open before choosing any
  colour.
- `references/n-file-edits.md` — verified loops and `sed` scripts for the sitewide
  edits, the exact file lists, and the grep commands that prove a fix landed. Open
  before any change that touches more than three files.
