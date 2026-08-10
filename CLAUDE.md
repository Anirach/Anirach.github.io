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

## Architecture

```
/
├── index.html          # Portfolio landing page — the ONLY consumer of style.css + script.js
├── style.css           # Landing-page styles only (plain hex colors, no :root variables)
├── script.js           # IIFE: nav scroll state, hamburger, IntersectionObserver reveal, hero parallax
├── blog/
│   ├── index.html      # Blog listing — fully static, zero JavaScript
│   └── *.html          # 37 self-contained posts (own <style>, own :root, own nav markup)
├── images/             # Cover images (<slug>-cover.png|jpg) + diagram PNGs
└── CNAME               # anirach.com
```

**Every blog page is an island.** Posts do not link `style.css` or `script.js`; each embeds its full stylesheet in a `<style>` block and defines its own `:root` variables. Editing `style.css` affects only the landing page. Editing one post affects only that post — there is no shared partial, so changes that should apply "everywhere" must be repeated per file (this is what commit `4c180c9` "Standardize series navigation across all 7 OpenClaw posts" was doing).

### Content is organized as two series

`blog/index.html` groups posts into two `.series-section` blocks — there is no category-filter UI and no client-side JS on that page:

- `#series-openclaw` — "OpenClaw for Organizations" (13 cards; 7 of them are the numbered series, the rest standalone)
- `#series-devops` — "DevOps & Vibe Coding" (24 cards)

### Three mutually exclusive in-post navigation patterns

Match the pattern to the post's series; do not mix them.

| Pattern | Used by | Markup | Link style |
|---|---|---|---|
| `.series-nav` chip strip | the 7 numbered OpenClaw posts | `<div class="series-nav">` + `.series-links` with `<a>` for others and `<span class="current">` for self | absolute, extensionless: `/blog/openclaw-memory` |
| `.post-nav` prev/next pair | DevOps posts + a few standalone | two `.post-nav__link` with `.post-nav__dir` (`← Previous` / `Next →`) and `.post-nav__title` | relative with extension: `openclaw-memory.html` |
| none | `beyond-plugins`, `git-branching`, `idle-self-improvement`, `obsidian-ai-jarvis`, `openclaw-migration` | — | — |

The numbered OpenClaw series order is fixed: `openclaw-101` → `agent-teams` → `memory` → `security` → `integrations` → `skills` → `production`. All 7 chips appear in all 7 posts. Adding a post to this series means editing all seven files.

## Conventions

- **Language**: `<html lang="th">` on posts (`lang="en"` on `index.html` and `blog/index.html`). Headings and technical terms in English, body prose in Thai.
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

### Manual counters — currently out of sync

Nothing computes these; they drift. In `blog/index.html`:

- `.blog-hero__stats` says **33** articles; there are actually **37** cards.
- `#series-openclaw` `.series-count` says **12 articles**; there are actually **13** cards.
- `#series-devops` `.series-count` says **24 articles** — correct.

Fix these when touching the index. Verify with:

```bash
grep -c 'class="card"' blog/index.html                              # total cards
awk '/id="series-openclaw"/,/id="series-devops"/' blog/index.html | grep -c 'class="card"'
```

## Project skills

Four skills live in `.claude/skills/` — use them; they carry the deep, verified detail this file only summarizes:

- **page-design** — the house visual system (canonical `:root` tokens, type scale, component vocabulary, approved hero gradients, modern-CSS adoption verdicts). Load before designing or restyling anything.
- **blog-post** — the end-to-end recipe for adding/editing a post, with a starter template (`assets/post-template.html`) and a wiring verifier (`assets/verify-wiring.py`).
- **a11y-perf** — accessibility and performance standing rules plus the measured remediation backlog (real contrast ratios, image weights, focus states).
- **site-check** — run `python3 .claude/skills/site-check/scripts/check_site.py` from the repo root before every push; it is this repo's only test suite.

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
