# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Personal portfolio and blog for Dr. Anirach Mingkhwan, served by GitHub Pages at anirach.com (`CNAME`). Hand-written static HTML/CSS/JS — no build system, no package manager, no dependencies, no tests, no CI.

## Development

No build step. Serve the repo root (relative paths like `../images/` require it):

```bash
python -m http.server 8000    # then open http://localhost:8000
# or
npx serve .
```

Deploy by pushing to `main` — GitHub Pages auto-deploys. There is no `.nojekyll`, so Jekyll's default processing applies; GitHub Pages also resolves extensionless URLs (`/blog/openclaw-101` → `openclaw-101.html`), which the OpenClaw series relies on.

`_config.yml` exists for exactly one purpose: `exclude: [docs, CLAUDE.md]` keeps internal working documents out of the **published** site (they stay in the repo). Jekyll already omits any path starting with `.` or `_`, so `.claude/` and `.superpowers/` are unreachable on the live site without being listed. Adding a new internal directory means adding it there too — verify with `curl -s -o /dev/null -w '%{http_code}' https://anirach.com/<path>` → 404.

## Architecture

```
/
├── index.html          # Portfolio landing page — the ONLY consumer of style.css + script.js
├── style.css           # Landing-page styles — carries the canonical 24-token :root block, same tokens every other page redefines in its own embedded <style>
├── script.js           # IIFE: nav scroll state, hamburger, IntersectionObserver reveal, hero parallax
├── blog/
│   ├── index.html      # Blog listing — fully static, zero JavaScript, 3 category bands (only Technology has posts)
│   └── *.html          # 37 self-contained posts (own <style>, own :root, own nav markup)
├── books/              # Novels (fiction; nav label "Novels") — all self-contained
│   ├── index.html      #   the section index: 1 published novel + 2 complete manuscripts
│   ├── three-old-men.html            # per-book detail page
│   ├── a-pocketful-of-questions.html # per-book detail page
│   └── the-thirteenth-seal.html      # per-book detail page
├── publications/index.html  # Academic: Springer book, 8 chapters, selected publications — self-contained
├── projects/index.html # Projects & Apps — self-contained page, own <style>/:root
├── news/index.html     # News & Updates — self-contained page, own <style>/:root
├── images/             # 56 files — covers (<slug>-cover.png|jpg), diagram PNGs, posters
├── docs/               # design spec, implementation plan, OpenClaw news runbook + gate
├── .claude/skills/     # page-design · blog-post · a11y-perf · site-check
├── _config.yml         # Jekyll excludes: docs/, CLAUDE.md (see Development)
└── CNAME               # anirach.com
```

**Every blog page is an island — and so is each of `books/` (its index and all three detail pages), `publications/`, `projects/`, `news/`.** None of them link `style.css` or `script.js`; each embeds its full stylesheet in a `<style>` block and defines its own `:root` variables (copied from the same canonical token set `style.css` also carries). Editing `style.css` affects only the landing page. Editing one post or one of the seven section-directory pages affects only that file — there is no shared partial, so changes that should apply "everywhere" must be repeated per file (this is what commit `4c180c9` "Standardize series navigation across all 7 OpenClaw posts" was doing).

### Content is organized as three categories, one of which holds two series

`blog/index.html` groups posts into three `.category` bands — there is no category-filter UI and no client-side JS on that page. Only **Technology** has posts; the other two are placeholders:

- **Technology** (`#cat-technology`, 37 articles) — contains two `.series-section` blocks:
  - `#series-openclaw` — "OpenClaw for Organizations" (13 cards; 7 of them are the numbered series, the rest standalone)
  - `#series-devops` — "DevOps & Vibe Coding" (24 cards)
- **Academic & Philosophy** (`#cat-academic`) — "First posts coming soon"
- **Lifestyle** (`#cat-lifestyle`) — "First posts coming soon"

The hero `.blog-hero__stats` mirrors this: 3 Categories, 2 Series, 37 Articles.

### Three mutually exclusive in-post navigation patterns

Match the pattern to the post's series; do not mix them.

| Pattern | Used by | Markup | Link style |
|---|---|---|---|
| `.series-nav` chip strip | the 7 numbered OpenClaw posts | `<div class="series-nav">` + `.series-links` with `<a>` for others and `<span class="current">` for self | absolute, extensionless: `/blog/openclaw-memory` |
| `.post-nav` prev/next pair | DevOps posts + a few standalone | two `.post-nav__link` with `.post-nav__dir` (`← Previous` / `Next →`) and `.post-nav__title` | relative with extension: `openclaw-memory.html` |
| none | `beyond-plugins`, `git-branching`, `idle-self-improvement`, `obsidian-ai-jarvis`, `openclaw-migration` | — | — |

The numbered OpenClaw series order is fixed: `openclaw-101` → `agent-teams` → `memory` → `security` → `integrations` → `skills` → `production`. All 7 chips appear in all 7 posts. Adding a post to this series means editing all seven files.

## Conventions

- **Language**: `<html lang="th">` on posts. All 6 nav-bearing index pages (`index.html`, `blog/index.html`, `books/index.html`, `publications/index.html`, `projects/index.html`, `news/index.html`) and the 3 `books/` detail pages are `lang="en"`. Headings and technical terms in English, body prose in Thai (marked with `<span lang="th">` on the section pages).
- **CSS variables**: defined per-file in each blog page's own `:root`. Common set: `--navy: #0f172a`, `--blue`/`--indigo: #6366f1`, `--slate: #334155`, `--slate-light: #64748b`, `--bg: #f8fafc`, `--font` (Inter), `--mono` (JetBrains Mono). Longer posts add semantic accents (`--green`, `--amber`, `--purple`, `--code-bg`). Copy the `:root` from the nearest sibling post rather than inventing one. `openclaw-101.html` predates this and uses raw hex throughout.
- **Fonts**: Google Fonts `<link>` per page — Inter 300–900, plus JetBrains Mono 400–600 on posts with code.
- **Diagrams**: render as PNG in `images/` and `<img>` them in. Inline HTML/CSS and ASCII-art diagrams have repeatedly broken layout and were replaced (`c270892`, `4ae2660`) — do not reintroduce them.
- **Images**: covers are `images/<slug>-cover.png|jpg`, referenced from posts as `../images/...` and from `blog/index.html` as `../images/...`. Card `<img>` tags carry an inline `style="background: linear-gradient(...)"` fallback.
- **Reveal animations**: `data-reveal` attribute — landing page only (driven by `script.js`).

## Adding a New Blog Post

1. Copy the closest existing post in the same series as a template — it carries the correct `:root`, nav markup, and footer.
2. Add the cover image as `images/<slug>-cover.png`.
3. Add a `.card` anchor to the correct `.series-section` in `blog/index.html`.
4. Wire navigation: for the numbered OpenClaw series, add the chip to all 7 `.series-nav` blocks; for DevOps, insert into the prev/next chain by editing the two neighbouring posts as well.
5. Update the counters (see below).

### Hand-typed counters — now enforced, but still hand-typed

`blog/index.html` carries four: the hero's `N Categories` / `N Series` / `N Articles`, and a
`.series-count` per series. Nothing *computes* them, so they still drift whenever you add a post —
but they are no longer silent about it. `check_site.py` INV-02a/b/c/d/e recompute all of them from
the actual card counts and fail the build on any mismatch, and `--fix` rewrites the ones it can.

The same pattern exists outside `blog/`, with **four** counters checked by
`docs/openclaw/check-news-sync.py` instead: `news/index.html`'s `"N updates"`,
`publications/index.html`'s `"N chapters"` (the chapters label moved there in the 2026-08-23
books/publications split), and `books/index.html`'s `"N novel"` and `"N complete"`. The gate
strips HTML comments before counting, so a commented-out card can neither satisfy nor break a
counter.

Current values, re-derive rather than trust: 3 Categories · 2 Series · 37 Articles (13 OpenClaw +
24 DevOps) · 7 news updates · 8 chapters (publications) · 1 novel + 2 complete (books).

`books/` detail pages have their own wiring check: `check_site.py` INV-26 fails if a
`books/*.html` detail page is not linked from `books/index.html`, or if the index links a
same-directory `.html` that does not exist. **Adding a future book** = copy a sibling detail page
(e.g. `books/three-old-men.html`) as the template, add its card (whole-card anchor with
`aria-labelledby="card-title-<slug>"`) to the right section of `books/index.html`, add the cover
as `images/<slug>-cover.jpg` (JPEG, ≤200 KB), and update the `"N novel"` / `"N complete"` label in
the same commit — then run both gates.

```bash
python3 .claude/skills/site-check/scripts/check_site.py --check INV-02a --check INV-02c   # blog
python3 .claude/skills/site-check/scripts/check_site.py --fix                             # repair blog counters
python3 docs/openclaw/check-news-sync.py                                                  # news + publications + books
```

## Project skills

Four skills live in `.claude/skills/` — use them; they carry the deep, verified detail this file only summarizes:

- **page-design** — the house visual system (canonical `:root` tokens, type scale, component vocabulary, approved hero gradients, modern-CSS adoption verdicts). Load before designing or restyling anything.
- **blog-post** — the end-to-end recipe for adding/editing a post, with a wiring verifier (`assets/verify-wiring.py`). The starter template itself is not here — it was consolidated into **page-design** (`assets/post-template.html`) as the repo's one canonical copy; see `.claude/skills/blog-post/assets/TEMPLATE-MOVED.md`.
- **a11y-perf** — accessibility and performance standing rules plus the measured remediation backlog (real contrast ratios, image weights, focus states).
- **site-check** — run `python3 .claude/skills/site-check/scripts/check_site.py` from the repo root before every push. 49 cross-file integrity checks; exit 0 means no **new** fail-severity violation (a baseline of pre-existing debt is carried, `0 new, 55 known` today). `INV-25` fails the build if a baseline entry goes stale, so the net cannot silently rot; `INV-26` ties every section-directory detail page (today: the three `books/*.html`) to its own index.

News and the homepage "Latest updates" strip have a separate gate — `python3 docs/openclaw/check-news-sync.py` — which checks three things nothing else does: the strip lists the 3 newest news items in order, every news item carries a `<!-- source: … -->` provenance comment, and the four hand-typed counters match reality (`"N updates"` on news, `"N chapters"` on publications, `"N novel"` / `"N complete"` on books). The full procedure for adding news is `docs/openclaw/latest-updates-runbook.md`.

## Verification

There is nothing to lint or test, so check links by hand after structural edits:

```bash
# every post file is linked from the index, and every index link resolves
comm -3 <(grep -o 'href="[a-z0-9-]*\.html"' blog/index.html | sed 's/href="//;s/"//' | sort -u) \
        <(ls blog/*.html | xargs -n1 basename | grep -v '^index.html$' | sort)

# which nav pattern each post uses (post-nav count, series-nav count, file)
for f in blog/*.html; do [ "$(basename $f)" = index.html ] && continue; \
  echo "$(grep -c 'class="post-nav__link"' $f) $(grep -c 'class="series-nav"' $f) $(basename $f)"; done | sort
```
