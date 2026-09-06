# New blog post — pre-commit checklist

`CLAUDE.md` documents the "Adding a New Blog Post" flow. These are the steps it omits.
Work top to bottom; item 1 is still the one that is always forgotten.
Re-verified **2026-09-06** against `905d3a4` — 76 posts, five series, all bilingual.

## 0. First: which series, and is it generated?

This question comes before everything else, because for one series the answer is "you do not
hand-write the file at all".

| Series | Cards | Nav pattern | How a post is added |
|---|---|---|---|
| **AI Transformation for Organizations** | 20 | grouped `.series-nav`, 4 labelled groups of 5 | **generated.** Add a row to `scripts/series/ai-transformation.json`, write the content sheets in `.bilingual/<slug>.{th,en}.html`, then `python3 scripts/build_series.py --post <slug>` followed by `--restrip` to rewrite the chip strip in the other twenty. **Never hand-edit 20 grouped strips**, and never hand-edit a manifest-owned field in an emitted file — the next `--post` reverts you |
| **Hermes Agent in Practice** | 10 | `.series-nav`, 10 chips | hand-written; add the chip to all 10 files |
| **OpenClaw for Organizations** | 13 (7 numbered) | `.series-nav`, 7 chips | hand-written; add the chip to all 7 numbered files |
| **DevOps & Vibe Coding** | 24 | `.post-nav` prev/next | hand-written; edit the two neighbours as well |
| **Life Thought & Philosophy** | 9 | `.series-nav`, 9 chips | hand-written; add the chip to all 9 files |

**Do not start from `.claude/skills/page-design/assets/post-template.html` without reading
it first.** Checked 2026-09-06, it is behind the shipped pages on five counts: no skip link,
no `<main id="main">`, none of the TH ⇄ EN apparatus, no `<details class="post-toc">`, a
three-weight `Sarabun:wght@400;600;700` font URL where every shipped page requests five, and
a `:root` that still carries `--purple: #8b5cf6` and no `--coral`. **Copy the nearest sibling
post in the target series instead** — it carries the correct `:root`, nav markup, both
language tracks and the footer. The 20 AI Transformation posts are the cleanest examples on
the site (zero heading skips, both tracks, figures, references block).

## 1. Recompute the counters in `blog/index.html`

Six sites, all correct today, so any drift you see is yours. Recompute — never increment,
that is how they all went stale before. `check_site.py` INV-02a–INV-02f fail the build on a
mismatch and `--fix` repairs the ones it can.

| Counter | Today |
|---|---|
| `.blog-hero__stat` "N Series" | 5 |
| `.blog-hero__stat` "N Articles" | 76 |
| `.series-count` × 5 | ai-transformation 20 · hermes 10 · openclaw 13 · devops 24 · life 9 |
| `.blog-jump` chip `· N` × 5 | must equal each section's card count (INV-02f) |

There is deliberately **no "N Categories" stat** — the category bands were deleted on
2026-08-26 because the last one held 100% of the posts. Do not reinstate one.

Line numbers are deliberately omitted — they have moved several times. Grep for the class.

```bash
python3 -c "
import re
s=open('blog/index.html',encoding='utf-8').read()
print('cards', len(re.findall(r'<a\s+href=\"[^\"]+\"\s+class=\"card\">', s)))
for sid,b in re.findall(r'<section class=\"series-section\" id=\"([^\"]+)\">(.*?)</section>',s,re.S):
    print(sid, len(re.findall(r'<a\s+href=\"[^\"]+\"\s+class=\"card\">',b)))"
python3 .claude/skills/site-check/scripts/check_site.py | grep INV-02   # all must PASS
```

**Do not count with `grep -c 'class="card"'`** — it returns 77, because `grep -c` counts
lines and one hit is the warning comment above the featured post. And **your card is
`class="card"`, never `class="feature"`**: the feature is a second link to an existing post,
and a second `class="feature"` would break the feed.

## 2. Images

- [ ] **Cover:** JPEG, not PNG. `images/<slug>-cover.jpg`, 800×800, under 200 KB. The 77
      existing plain covers average **42 KB** and the largest is **54 KB** — you have plenty
      of headroom, so do not be the first over the line.
      `sips -s format jpeg -s formatOptions 70 -Z 1600 src.png --out images/<slug>-cover.jpg`
- [ ] **Share card:** `images/<slug>-og.jpg`, **exactly 1200×630**. All 80 existing ones are.
      `check_site.py` INV-27 reads the real pixel size out of the JPEG header, so a wrong
      `og:image:width` fails the build; INV-35 checks the cover and the share card together.
      `scripts/make_cover.py` draws both from one row of `scripts/covers.tsv`.
- [ ] **Series figures** (AI Transformation, and anything that adopts the pattern):
      `images/ai-transformation-fig-*.png`, **1400 px wide**, **8-bit palette PNG**, produced
      by `scripts/make_figure.py`. The 19 existing figures average **44 KB**, largest 58 KB.
      Never re-save one through `sips` — a truecolour round-trip roughly triples it for no
      visible gain on flat fills and hard edges.
- [ ] Only the 5 legacy diagrams (`*-arch.png`, `*-flow.png`, `*-levels.png`) stay PNG for
      historical reasons; they are 123–235 KB and are the reason new figures are palette PNGs.
- [ ] The card image and the post hero image are the same file — don't add a second asset.

## 3. Every `<img>`

- [ ] `width` and `height` present, set to the **source** pixel size
      (`sips -g pixelWidth -g pixelHeight images/<file>`). **299 of 299 `<img>` tags on the
      site have all four attributes — do not be the 300th that breaks it.**
- [ ] `loading="lazy" decoding="async"` on the card image in `blog/index.html`. **152 of the
      153 there are lazy.**
- [ ] `loading="eager" fetchpriority="high" decoding="async"` on the post hero cover — it is
      the LCP element, never lazy. The single eager image on `blog/index.html` is the
      featured card's share card, for the same reason.
- [ ] `loading="lazy" decoding="async"` + explicit `width`/`height` on every figure.
- [ ] `alt=""` on the avatar (all 76 on `blog/index.html` are) and on any cover whose adjacent
      heading already says the same words. Never `alt="… Cover"` — 0 remain on the site.
- [ ] **A figure needs two alts, one per language track, and both must be full sentences.**
      The figure is wrapped in `<a href="…png">` with no other text, so the alt *is* the
      link's entire accessible name. `alt="diagram"` produces a link announced as
      "diagram, link".
- [ ] The alt describes *the picture actually shown*, not the post. INV-07a fails on a shared
      cover, which is what used to produce that mismatch.

## 4. Structure

- [ ] Exactly one `<h1>`. All 76 posts pass this today (`check_site.py` INV-11).
- [ ] No heading-level skips. **31 of 76 posts have one and copying a post inherits it.**
      20 are the series strip's `<h3>` sitting under the `<h1>`; 11 are real `h2 → h4` body
      breaks. The 20 AI Transformation posts have zero — copy one of those.
- [ ] Your card in `blog/index.html` uses **`<h3 class="card__title">`**, matching the other
      76. Not `h2` — that level belongs to the 5 `.series-title` headings and the feature.
      The ladder went a level shallower on 2026-08-26; **grep the class, never assume a
      level**, because `gen_feed.py`, `check_site.py` and `verify-wiring.py` all read it.
- [ ] Article body wrapped in `<main id="main">` and a skip link as the first thing after
      `<body>`. **Both are on all 87 pages** and INV-30 fails if they come apart — so this is
      a copy-it-correctly item, not an aspiration.
- [ ] **`<main>` must enclose everything the language switch touches**, including the hero:
      the selector is `#langSwitch:checked ~ main .l-en`, and a general sibling combinator
      reaches nothing above itself. Three posts had to have their `<main>` moved up for this.
- [ ] In-post navigation is still `<div class="series-nav">` / `<div class="post-nav">`, not
      `<nav>` — that landmark fix is one of the two outstanding site-wide items and INV-04c
      currently *requires* `.post-nav` to be a `<div>`. Match the neighbours; do not
      unilaterally convert one file.
- [ ] Navigation, the hero ordinal badge and the card title belong to **neither** language
      track. Keep them monolingual — INV-03, INV-10 and `gen_feed.py` read them with regexes
      that concatenate or truncate on a nested tag.

```bash
python3 -c "
import re,sys;p=sys.argv[1];lv=[int(m.group(1)) for m in re.finditer(r'<h([1-6])[\s>]',open(p,encoding='utf8').read())]
print('h1 count',lv.count(1),'skips',[(a,b) for a,b in zip(lv,lv[1:]) if b>a+1])" blog/<slug>.html
```

## 5. Language — the post is bilingual, so everything below is × 2

- [ ] `<html lang="th">` (all 76 posts). The page-level `lang` never flips — it cannot,
      without JavaScript. `check_site.py` INV-13.
- [ ] The TH ⇄ EN apparatus: a visually hidden checkbox as a **direct child of `<body>`,
      before `<main>`**, two tracks `.l-th` / `.l-en`, a `<div class="l-en" lang="en">` on
      the English body, and the `ไทย · English` pill. Copy the input verbatim — **it is
      off-canvas, not `display:none`, and it carries its own accessible name**:
      `<input type="checkbox" id="langSwitch" class="lang-switch-box" aria-label="Switch language: Thai / English">`
      with `.lang-switch-box { position: absolute; left: -9999px; }`. `display:none` would
      make it unfocusable; dropping the `aria-label` would announce it as a bare checkbox.
- [ ] `display: revert`, never `display: block`, in the `:checked` rules — `.l-en` is used on
      `<div>`, `<details>` and `<span>` alike.
- [ ] Heading ids namespaced `th-` / `en-` so the two copies do not collide, and each TOC
      links only into its own track.
- [ ] Do not rename `lang-switch` / `l-th` / `l-en`. Those names are verified clear of
      INV-12's menu-token regex (`hamburger|burger|nav__toggle|nav-toggle|navtoggle|menu-toggle|menu__toggle`).
- [ ] JSON-LD `inLanguage: ["th","en"]` and the `og:locale:alternate` `en_US` line land in the
      same commit as the markup — `check_visibility.py` S1 keys off `class="l-en"` and fails
      when the two disagree.
- [ ] `lang="en"` on English headings, code blocks and technical runs **inside the Thai
      track**. **250 such headings on the site carry no `lang="en"`**, so you are following a
      bad precedent rather than setting one — do it right in the new file.

```bash
python3 scripts/bilingualize.py --verify <slug>   # the only check that catches a one-track edit
```

## 6. CSS in the embedded `<style>`

- [ ] The house a11y block is present — `:focus-visible` on `var(--focus)`,
      `.footer, .blog-footer, pre { --focus: var(--gold) }`, `:focus:not(:focus-visible)`,
      `@media (prefers-reduced-motion: reduce)`, `text-wrap: balance`, and `color-scheme:
      light` on `:root`. It is in **all 86** other embedded `<style>` blocks. Keep it
      byte-identical; do **not** paste a second focus ring.
- [ ] `.skip-link` rules present (86 files + `style.css` have them).
- [ ] The `:root` is the current 29-token set, copied from the nearest sibling post — **not**
      from `post-template.html`, whose `--purple` is still the old indigo. AI Transformation
      posts add a 29th, `--coral: #c2410c`.
- [ ] **Colour rules that still bite, all re-measured 2026-09-06:**
      `--gray #94a3b8` is **2.56:1** on white — dark grounds only; use `--slate-light #526174`
      (6.32:1) on light. `--blue-light` is **borders only** (3.45:1). `--gold` is decorative on
      light (2.37:1); `--gold-dark` is its text form (6.02:1). **`--coral` passes on white
      (5.18:1) and cream (4.84:1) but fails on `--cloud` (4.11), `--parchment` (3.95) and every
      figure tint (4.10–4.55) — large text or graphics only there, never body copy.**
- [ ] `.post-hero` uses one of the **two** approved families — Deep Blue
      `135deg, #11304b, #1a4d7a 45%, #226299` or Sunrise `135deg, #eef3f3, #dee7e6 50%, #e9e1c4`.
      `check_site.py` INV-28 fails on a third. No scrim is needed on either.
- [ ] `.post-hero__meta` is `#fff` on Deep Blue (6.41:1 at the worst stop) or
      `var(--slate-light)` on Sunrise (4.83:1). Never `rgba(255,255,255,0.x)` — zero remain.
- [ ] `.post-series-footer` is `var(--slate-light)`, never `var(--gray)` — all 61 rules are.
- [ ] Every new `:hover` rule has a matching `:focus-visible` or `:focus-within`.

## 7. Markup hygiene

- [ ] **No `<script>` except `type="application/ld+json"`, with double quotes.**
      `check_site.py` **INV-38** fails the build otherwise. `script.js` was deleted
      2026-08-26; the site is zero-JavaScript and every control you add must work in pure CSS.
      79 pages carry the JSON-LD BlogPosting block; that is data, not code.
- [ ] Mobile nav reachable at ≤768px. Posts keep their nav links visible and shrink them —
      that is the pattern to copy. Do **not** copy the bare `.nav__links { display: none }`
      from `blog/obsidian-ai-jarvis.html:275`, the one file on the site still broken on a
      phone. If you genuinely need a toggle, port the `.nav__toggle` checkbox +
      `.nav__burger` label pair from `blog/index.html` (the 800px media query, not 768px).
- [ ] `rel="noopener"` on every `target="_blank"` — **92 of 92** on the site have it.
- [ ] `aria-hidden="true"` on decorative emoji.
- [ ] Font `<link>` is one of the two URLs the whole site uses, preceded by both `preconnect`
      links: `Inter:wght@300;400;500;600;700;800;900&family=Sarabun:wght@400;500;600;700;800`
      plus `&family=JetBrains+Mono:wght@400;500;600` if the post has code, then `&display=swap`.
      **Never trim Inter 300** (six `style.css` headings would re-render at 400) and never trim
      a Sarabun weight — Sarabun is a static family, so an unrequested weight is *synthesised*
      as faux-bold, which smears Thai glyphs.
- [ ] The `<!-- social -->` block and the JSON-LD BlogPosting after it. **Do not hand-edit
      the social block** — INV-27 recomputes the canonical path from the file's own location
      and reads the real image dimensions.

## 8. Look at it — in both languages

```bash
python3 -m http.server 8000
```

- [ ] 375px wide: nav links reachable, no horizontal scroll.
- [ ] Tab from the top: the skip link appears first, then every link and card shows the 2px
      `:focus-visible` ring. It ships on all 87 pages, so its absence on yours means you
      dropped the block.
- [ ] **Flip the ไทย · English pill and repeat both checks.** Half the page is `display:
      none` at any moment; a defect in the hidden track is invisible until someone flips it.
- [ ] DevTools Network: the new cover is under 200 KB, the share card is 1200×630, and
      below-the-fold covers and figures are deferred.
- [ ] `git diff --stat` touches only the files you meant to touch.

## 9. Run the gates

```bash
python3 .claude/skills/site-check/scripts/check_site.py      # 61 checks, expect exit 0
python3 scripts/check_visibility.py --strict                 # expect exit 0
python3 scripts/bilingualize.py --verify <slug>              # both tracks agree
python3 scripts/gen_feed.py && python3 scripts/gen_sitemap.py   # regenerate in the same commit
python3 docs/openclaw/check-news-sync.py                     # only if you touched news/books/publications
```

The feed and the sitemap are **generated**, not hand-maintained: INV-31 and INV-32 fail the
build when either drifts from `blog/index.html`. Run `gen_sitemap.py` in the commit *after*
the content change, so the git dates it reads exist. Today: 86 `<loc>`, 76 `<item>`.
`llms.txt` is hand-maintained and `check_visibility.py` L2 fails when a carded post is
missing from it — add yours.
