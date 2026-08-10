# New blog post — pre-commit checklist

`CLAUDE.md` documents the three-step "Adding a New Blog Post" flow. These are the
steps it omits. Work top to bottom; the first item is the one that is always
forgotten. Re-verified **2026-08-10** against `7867c00`.

Start from `.claude/skills/page-design/assets/post-template.html` — the only post
template in the repo. It already satisfies items 2, 3, 5 and 6 below.

## 1. Recompute the five counters in `blog/index.html`

All five are **correct today** (`b9fb125` + Task 11), so any drift you see is yours.
Recompute — never increment, that is how they all went stale before.

| Counter | Today |
|---|---|
| `.blog-hero__stat` "N Categories" | 3 |
| `.blog-hero__stat` "N Series" | 2 |
| `.blog-hero__stat` "N Articles" | 37 |
| `.category__count` `#cat-technology` | 37 articles |
| `.series-count` `#series-openclaw` / `#series-devops` | 13 / 24 |

Line numbers are deliberately omitted — they have moved twice. Grep for the class.

```bash
grep -c 'class="card"' blog/index.html
python3 -c "
import re;s=open('blog/index.html',encoding='utf8').read()
for sid,b in re.findall(r'<section class=\"series-section\" id=\"([^\"]+)\">(.*?)</section>',s,re.S):
    print(sid, len(re.findall(r'class=\"card\"',b)))"
python3 .claude/skills/site-check/scripts/check_site.py | grep INV-02   # all must PASS
```

## 2. Cover image

- [ ] JPEG, not PNG. `sips -s format jpeg -s formatOptions 70 -Z 1600 src.png --out images/<slug>-cover.jpg`
- [ ] Under 200 KB. `ls -l images/<slug>-cover.jpg` — the 36 existing covers are all JPG, average 112 KB, largest 194 KB, **zero over 200 KB**. Do not be the first.
- [ ] Only diagrams (`*-arch.png`, `*-flow.png`, `*-levels.png`) stay PNG. Those are correctly 123–235 KB.
- [ ] The card image and the post hero image are the same file — don't add a second asset.

## 3. Every `<img>`

- [ ] `width` and `height` present, set to the **source** pixel size for both the card and the hero (`sips -g pixelWidth -g pixelHeight images/<file>`). That is the convention on disk. **120 of 120 images currently have all four attributes — do not be the 121st that breaks it.**
- [ ] `loading="lazy" decoding="async"` on the card image in `blog/index.html`. All 74 there are lazy.
- [ ] `loading="eager" fetchpriority="high" decoding="async"` on the post hero cover — it is the LCP element, never lazy.
- [ ] `alt=""` on the avatar and on any cover whose adjacent heading already says the same words. Never `alt="… Cover"` — that word carries no information (4 posts do this today).
- [ ] The alt describes *the picture actually shown*. `blog/index.html:492` uses `monitoring-cover.jpg` with `alt="OpenClaw Memory Architecture"` — don't repeat that.

## 4. Structure

- [ ] Exactly one `<h1>` (`blog/deployment-hosting.html` has two — check yours). `check_site.py` INV-11.
- [ ] No heading-level skips. `h2 → h4` is the default failure mode here: **12 of 37** posts do it (plus one `h1 → h3` in `openclaw-integrations.html`), and copying an existing post inherits its skips.
- [ ] Your card in `blog/index.html` uses `<h4 class="card__title">`, matching the other 37. Not `h2`, not `h3` — Task 11 gave the page a real ladder and `h3` would collide with `.series-title`.
- [ ] Article body wrapped in `<main id="main">` — **aspirational**: 0 of 42 files have `id="main"` today, so you would be first. Do it anyway.
- [ ] Skip link is the first thing after `<body>` — also aspirational (0 of 42), and useless until `<main id="main">` exists.
- [ ] In-post navigation is `<nav aria-label="…">`, not `<div class="series-nav">` / `<div class="post-nav">`, with `aria-current="page"` on the current item.

```bash
python3 -c "
import re,sys;p=sys.argv[1];lv=[int(m.group(1)) for m in re.finditer(r'<h([1-6])[\s>]',open(p,encoding='utf8').read())]
print('h1 count',lv.count(1),'skips',[(a,b) for a,b in zip(lv,lv[1:]) if b>a+1])" blog/<slug>.html
```

## 5. Language

- [ ] `<html lang="th">` (matches the other 37 posts; only the 5 index pages are `en`). `check_site.py` INV-13.
- [ ] `lang="en"` on English headings, code blocks and technical runs. There are zero inline switches on the site today, so you are setting the precedent rather than following one.

## 6. CSS in the embedded `<style>`

- [ ] The 4-line house a11y block is present — `:focus-visible`, `:focus:not(:focus-visible)`, `@media (prefers-reduced-motion: reduce)`, `text-wrap: balance`, plus `color-scheme: light` on `:root`. It is in **41 of 41** other embedded `<style>` blocks; the template ships it. Keep it byte-identical.
- [ ] Optionally also paste `assets/a11y-block.css` — the parity/skip-link rules that are **not** yet anywhere on disk. Do **not** paste a second focus ring.
- [ ] No `--blue #6366f1` used as text on a light background — use `--blue-dark #4f46e5`.
- [ ] No `var(--gray) #94a3b8` as text on white or `#f8fafc` — use `var(--slate-light) #64748b`. `--gray` is only safe on `--navy`.
- [ ] `.post-hero__meta` is `#fff`, not `rgba(255,255,255,0.6)`.
- [ ] If the hero gradient's lightest stop is lighter than about `#4c1d95`, add the scrim: `background: linear-gradient(rgba(0,0,0,.35), rgba(0,0,0,.35)), linear-gradient(135deg, …);`
- [ ] Every new `:hover` rule has a matching `:focus-visible` or `:focus-within`.

## 7. Markup hygiene

- [ ] No `<script>`. `index.html` is the only file on the site with JavaScript, so any control you add must work in pure CSS. `check_site.py` INV-12 enforces this and has no baseline entry.
- [ ] Mobile nav is reachable at ≤768px. If you need a toggle, copy the pure-CSS `.nav__toggle` checkbox + `.nav__burger` label pattern from `blog/index.html`. Do **not** copy the bare `.nav__links { display: none }` from `blog/obsidian-ai-jarvis.html` — that is the one file still broken on a phone.
- [ ] `rel="noopener noreferrer"` on every `target="_blank"` (45 of 57 on the site already have it; 12 do not).
- [ ] `aria-hidden="true"` on decorative emoji.
- [ ] Font `<link>` is the trimmed URL: `Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400&display=swap`, preceded by both `preconnect` links.

## 8. Look at it

```bash
python3 -m http.server 8000
```

- [ ] 375px wide: nav links reachable, no horizontal scroll.
- [ ] Tab from the top: every link and card shows the 2px `:focus-visible` ring. It ships on all 42 pages, so its absence on yours means you dropped the block.
- [ ] DevTools Network: the new cover is under 200 KB and below-the-fold covers are deferred.
- [ ] `git diff --stat` touches only the files you meant to touch.
