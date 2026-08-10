# New blog post — pre-commit checklist

`CLAUDE.md` documents the three-step "Adding a New Blog Post" flow. These are the
steps it omits. Work top to bottom; the first item is the one that is always
forgotten.

## 1. Update the three counters in `blog/index.html`

They are already stale today, which is exactly how this keeps happening.

| Line | Currently says | Should say |
|---|---|---|
| 221 | `<strong>33</strong> Articles` | count of `class="card"` |
| 235 | `12 articles` (`#series-openclaw`) | cards inside `<section id="series-openclaw">` |
| 573 | `24 articles` (`#series-devops`) | cards inside `<section id="series-devops">` |

```bash
grep -c 'class="card"' blog/index.html
python3 -c "
import re;s=open('blog/index.html',encoding='utf8').read()
oc,dv=s.split('id=\"series-devops\"');print('openclaw',oc.split('id=\"series-openclaw\"')[1].count('class=\"card\"'),'devops',dv.count('class=\"card\"'))"
```

## 2. Cover image

- [ ] JPEG, not PNG. `sips -s format jpeg -s formatOptions 80 -Z 800 src.png --out images/<slug>-cover.jpg`
- [ ] Under 200 KB. `ls -l images/<slug>-cover.jpg` — the 20 existing JPG covers average 83 KB; the 15 PNG covers average 1137 KB and are the reason `blog/index.html` is 18.41 MB.
- [ ] Only diagrams (`*-arch.png`, `*-flow.png`, `*-levels.png`) stay PNG. Those are correctly 126–241 KB.
- [ ] The card image and the post hero image are the same file — don't add a second asset.

## 3. Every `<img>`

- [ ] `width` and `height` present (card slot is `352`×`220`; hero cover is the source size).
- [ ] `loading="lazy" decoding="async"` on the card image in `blog/index.html`.
- [ ] `fetchpriority="high" decoding="async"` and **no** `loading="lazy"` on the post hero cover — it is the LCP element.
- [ ] `alt=""` on the avatar and on any cover whose adjacent heading already says the same words. Never `alt="… Cover"` — that word carries no information (4 posts do this today).
- [ ] The alt describes *the picture actually shown*. `blog/index.html:492` uses `monitoring-cover.jpg` with `alt="OpenClaw Memory Architecture"` — don't repeat that.

## 4. Structure

- [ ] Exactly one `<h1>` (`blog/deployment-hosting.html` has two — check yours).
- [ ] No heading-level skips. `h2 → h4` is the default failure mode here: 11 of 37 posts do it (plus one `h1 → h3` in `openclaw-integrations.html`), and copying an existing post inherits its skips.
- [ ] Article body wrapped in `<main id="main">`.
- [ ] Skip link is the first thing after `<body>`.
- [ ] In-post navigation is `<nav aria-label="…">`, not `<div class="series-nav">` / `<div class="post-nav">`, with `aria-current="page"` on the current item.

```bash
python3 -c "
import re,sys;p=sys.argv[1];lv=[int(m.group(1)) for m in re.finditer(r'<h([1-6])[\s>]',open(p,encoding='utf8').read())]
print('h1 count',lv.count(1),'skips',[(a,b) for a,b in zip(lv,lv[1:]) if b>a+1])" blog/<slug>.html
```

## 5. Language

- [ ] `<html lang="th">` (matches the other 37 posts).
- [ ] `lang="en"` on English headings, code blocks and technical runs. There are zero inline switches on the site today, so you are setting the precedent rather than following one.

## 6. CSS in the embedded `<style>`

- [ ] `assets/a11y-block.css` pasted in (focus-visible, skip-link, reduced-motion).
- [ ] No `--blue #6366f1` used as text on a light background — use `--blue-dark #4f46e5`.
- [ ] No `var(--gray) #94a3b8` as text on white or `#f8fafc` — use `var(--slate-light) #64748b`. `--gray` is only safe on `--navy`.
- [ ] `.post-hero__meta` is `#fff`, not `rgba(255,255,255,0.6)`.
- [ ] If the hero gradient's lightest stop is lighter than about `#4c1d95`, add the scrim: `background: linear-gradient(rgba(0,0,0,.35), rgba(0,0,0,.35)), linear-gradient(135deg, …);`
- [ ] Every new `:hover` rule has a matching `:focus-visible` or `:focus-within`.

## 7. Markup hygiene

- [ ] No `<script>`. `index.html` is the only file on the site with JavaScript, so any control you add must work in pure CSS. A hamburger button in a `blog/` page is dead UI — see `blog/index.html:208`.
- [ ] Mobile nav is reachable at ≤768px. Don't copy `.nav__links { display: none }` from `blog/index.html:173` or `blog/obsidian-ai-jarvis.html:250`.
- [ ] `rel="noopener noreferrer"` on every `target="_blank"`.
- [ ] `aria-hidden="true"` on decorative emoji.
- [ ] Font `<link>` is the trimmed URL: `Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400&display=swap`, preceded by both `preconnect` links.

## 8. Look at it

```bash
python3 -m http.server 8000
```

- [ ] 375px wide: nav links reachable, no horizontal scroll.
- [ ] Tab from the top: skip link appears, then every link and card shows a visible ring.
- [ ] DevTools Network: the new cover is under 200 KB and below-the-fold covers are deferred.
- [ ] `git diff --stat` touches only the files you meant to touch.
