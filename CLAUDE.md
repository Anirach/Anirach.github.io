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
│   ├── index.html      # Blog listing — fully static, zero JavaScript, a featured post + 2 series (no category band)
│   └── *.html          # 37 self-contained posts (own <style>, own :root, own nav markup)
├── books/              # Books & writing (nav label "Books") — all self-contained
│   ├── index.html      #   the section index: the last-lecture book + 1 published novel + 2 complete manuscripts
│   ├── one-day-of-light.html         # per-book detail page (+ one-day-of-light-{en,th}.pdf — free downloads, served from books/)
│   ├── three-old-men.html            # per-book detail page
│   ├── a-pocketful-of-questions.html # per-book detail page
│   └── the-thirteenth-seal.html      # per-book detail page
├── publications/index.html  # Academic: Springer book, 8 chapters, selected publications — self-contained
├── projects/index.html # Projects & Apps — self-contained page, own <style>/:root
├── news/index.html     # News & Updates — self-contained page, own <style>/:root
├── 404.html            # custom Not Found — LISTING chrome, noindex, NOT in sitemap.xml
├── robots.txt          # Allow all + Sitemap: line. VERIFIED 2026-08-26 post-deploy:
│                       #   the repo file REPLACES Cloudflare's Content Signals block
│                       #   outright — it is not prepended, as was first assumed
├── sitemap.xml         # 47 canonical URLs, hand-maintained — 404.html excluded
├── favicon.ico         # + apple-touch-icon.png (180×180) — both probed at the root by default
├── images/             # 64 files — covers (<slug>-cover.jpg; books/ titles carry both language faces as -cover-en/-th or -cover-front/-back), 9 share cards (og-*.jpg, <slug>-og.jpg — all 1200×630), diagram PNGs, posters, the event QR
├── docs/               # design spec, implementation plan, OpenClaw news runbook + gate
├── .claude/skills/     # page-design · blog-post · a11y-perf · site-check
├── _config.yml         # Jekyll excludes: docs/, CLAUDE.md (see Development)
└── CNAME               # anirach.com
```

**Every blog page is an island — and so is each of `books/` (its index and all four detail pages), `publications/`, `projects/`, `news/`.** None of them link `style.css` or `script.js`; each embeds its full stylesheet in a `<style>` block and defines its own `:root` variables (copied from the same canonical token set `style.css` also carries). Editing `style.css` affects only the landing page. Editing one post or one of the eight section-directory pages affects only that file — there is no shared partial, so changes that should apply "everywhere" must be repeated per file (this is what commit `4c180c9` "Standardize series navigation across all 7 OpenClaw posts" was doing).

### Content is organized as one featured post and two series

There are **no `.category` bands left**. The last one, "Technology", held 100% of the posts, so it
partitioned nothing — a reader met an emoji, the word "Technology" and "37 articles" (the same 37
the hero had just announced) before reaching any post. It was deleted on 2026-08-26; the Academic &
Philosophy and Lifestyle bands had gone earlier, as empty "First posts coming soon" placeholders
that sat for 16 days with nothing able to expire them.

`blog/index.html` is therefore, in order: hero → **one featured post** → two `.series-section`
blocks. No category-filter UI, no client-side JS.

- `#series-openclaw` — "OpenClaw for Organizations" (13 cards; 7 of them are the numbered series, the rest standalone)
- `#series-devops` — "DevOps & Vibe Coding" (24 cards)

The hero `.blog-hero__stats` reads **2 Series · 37 Articles**; there is deliberately no
"N Categories" stat, though INV-02e still verifies one if it is ever reinstated, and INV-02d still
fails on any empty `.category` band a future commit adds.

**The featured post is `class="feature"`, never `class="card"`.** Three separate regexes count
`class="card"` (`check_site.py` RE_CARD, `scripts/gen_feed.py`, blog-post's `verify-wiring.py`), so
a 38th match would inflate every counter and put a duplicate item in the feed. It spotlights the
newest post by git first-commit date — today `openclaw-migration`, which is already the first card,
so nothing is reordered. **Card order IS the prev/next chain and must never move.**

The heading ladder is `h1` hero → `h2` series (and the feature) → `h3` card title. It was a level
deeper until the category band went. `check_site.py` and `verify-wiring.py` read
`<(h[1-6]) class="card__title">` and follow any re-cut; `gen_feed.py` hard-coded `<h4>` and was
made level-agnostic in the same commit — a stale level there silently empties the feed.

### Three mutually exclusive in-post navigation patterns

Match the pattern to the post's series; do not mix them.

| Pattern | Used by | Markup | Link style |
|---|---|---|---|
| `.series-nav` chip strip | the 7 numbered OpenClaw posts | `<div class="series-nav">` + `.series-links` with `<a>` for others and `<span class="current">` for self | absolute, extensionless: `/blog/openclaw-memory` |
| `.post-nav` prev/next pair | DevOps posts + a few standalone | two `.post-nav__link` with `.post-nav__dir` (`← Previous` / `Next →`) and `.post-nav__title` | relative with extension: `openclaw-memory.html` |
| none | `beyond-plugins`, `git-branching`, `idle-self-improvement`, `obsidian-ai-jarvis`, `openclaw-migration` | — | — |

The numbered OpenClaw series order is fixed: `openclaw-101` → `agent-teams` → `memory` → `security` → `integrations` → `skills` → `production`. All 7 chips appear in all 7 posts. Adding a post to this series means editing all seven files.

## Conventions

- **Language**: `<html lang="th">` on posts. All 6 nav-bearing index pages (`index.html`, `blog/index.html`, `books/index.html`, `publications/index.html`, `projects/index.html`, `news/index.html`) and the 4 `books/` detail pages are `lang="en"`. Headings and technical terms in English, body prose in Thai (marked with `<span lang="th">` on the section pages).
- **CSS variables**: defined per-file in each blog page's own `:root`. Re-keyed to the book covers on 2026-08-26 (`scripts/retoken.py`, 28 tokens in 49 blocks): `--navy: #11304b`, `--blue: #226299` (a TEXT colour now — 6.4:1 on white), `--blue-dark: #1a4d7a`, `--blue-light: #4992b9` (**borders only**), `--slate: #334155`, `--slate-light: #526174`, `--bg: #faf7f0`, brand `--gold: #c4a46c` / `--gold-dark: #7a5f22` / `--cloud` / `--parchment`, and `--focus` (re-pointed to gold inside footers and `<pre>`, where the blue ring collapses to 2.12:1). `--font` (Inter + Sarabun for Thai), `--mono` (JetBrains Mono + Sarabun). Longer posts add semantic accents (`--green`, `--amber`, `--purple`, `--code-bg`). Copy the `:root` from the nearest sibling post rather than inventing one. `openclaw-101.html` predates this and uses raw hex throughout.
- **Fonts**: Google Fonts `<link>` per page — Inter 300–900, **Sarabun 400/600/700 for Thai** (looped, the Thai body-prose convention; added 2026-08-26 to 39 pages — the 10 island posts load no webfont at all and are deferred to the island conversion), plus JetBrains Mono 400–600 on posts with code.
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

`blog/index.html` carries three: the hero's `N Series` / `N Articles`, and a
`.series-count` per series (`N Categories` is retired with the bands). Nothing *computes* them, so they still drift whenever you add a post —
but they are no longer silent about it. `check_site.py` INV-02a/b/c/d/e recompute all of them from
the actual card counts and fail the build on any mismatch, and `--fix` rewrites the ones it can.

The same pattern exists outside `blog/`, with **four** counters checked by
`docs/openclaw/check-news-sync.py` instead: `news/index.html`'s `"N updates"`,
`publications/index.html`'s `"N chapters"` (the chapters label moved there in the 2026-08-23
books/publications split), and `books/index.html`'s `"N novel"` and `"N complete"`. The gate
strips HTML comments before counting, so a commented-out card can neither satisfy nor break a
counter. The `#last-lecture` section that leads `books/index.html` (One Day of Light)
deliberately carries **no** counter: the gate slices only `#published` and `#manuscripts`, and
`#last-lecture` sits above both, outside every slice — the precedent is `#academic`, which is
also counter-free. Do not "fix" it by adding one.

Current values, re-derive rather than trust: 2 Series · 37 Articles (13 OpenClaw + 24 DevOps) ·
7 news updates · 8 chapters (publications) · 1 novel + 2 complete (books).

`books/` detail pages have their own wiring check: `check_site.py` INV-26 fails if a
`books/*.html` detail page is not linked from `books/index.html`, or if the index links a
same-directory `.html` that does not exist. **Adding a future book** = copy a sibling detail page
(e.g. `books/three-old-men.html`) as the template, add its card (whole-card anchor with
`aria-labelledby="card-title-<slug>"`) to the right section of `books/index.html`, add the cover
as `images/<slug>-cover-en.jpg` + `-cover-th.jpg` (JPEG, ≤200 KB each — every `books/` title shows both
language faces, side by side on its card and stacked on its detail page), and update the `"N novel"` / `"N complete"` label in
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
- **site-check** — run `python3 .claude/skills/site-check/scripts/check_site.py` from the repo root before every push. 60 cross-file integrity checks; exit 0 means no **new** fail-severity violation (a baseline of pre-existing debt is carried, `0 new, 29 known` today — down from 55, as the 2026-08-26 redesign phases paid real debt down rather than baselining it). `INV-25` fails the build if a baseline entry goes stale, so the net cannot silently rot; `INV-26` ties every section-directory detail page (today: the four `books/*.html`) to its own index; `INV-27` enforces the social/canonical head block on all 47 pages. Added 2026-08-26 by the
critique work, each fault-injected before being trusted: `INV-28` (every `.post-hero` background is
Sunrise or Deep Blue — the 2 post families, down from 5 on 2026-08-26), `INV-29` (every post carries a home link and a footer
destination row, so no post is a dead end), `INV-30` (the skip link and its `id="main"` target
exist together), `INV-31`/`INV-32` (feed and sitemap drift).

**Progressive enhancement is now the rule on `index.html`.** `[data-reveal]` starts VISIBLE; the
hidden state is opt-in via a `.js-reveal` class that `script.js` adds to `<html>` as its first act.
Before 2026-08-26 the hidden state was the default and the script was the only thing that undid it,
so with JavaScript off **53% of the landing page rendered as empty coloured bands** (2,746 of
5,172px at 1440) — including the entire One Day of Light block, both PDF links and the seat
reservation. A `<noscript><style>` override was the obvious patch and was deliberately rejected: it
would have given `index.html` its first `<style>` block and broken the invariant that this page's
CSS lives entirely in `style.css` (7867c00). Never re-invert this.

**Complementary user-level design skills** (installed 2026-08-26 into `~/.claude/skills` — not in this
repo, may be absent on other machines): `fixing-metadata` + `seo` (the gap they found was closed by the
2026-08-26 sweep — see "Social metadata" below), `impeccable` (design critique/polish method),
`review-animations` (motion review, manual invoke), `color-expert` (OKLCH/contrast craft),
`dark-mode-design-expert` (dark-theme token architecture), plus the official `playground` plugin for
throwaway visual A/Bs. **House rules win every conflict**: the four project skills above stay
authoritative for tokens, type scale, components, and measured a11y numbers — third-party skills
advise, never override, and any change they motivate still goes through the owner's review-first flow.

News and the homepage "Latest updates" strip have a separate gate — `python3 docs/openclaw/check-news-sync.py` — which checks three things nothing else does: the strip lists the 3 newest news items in order, every news item carries a `<!-- source: … -->` provenance comment, and the four hand-typed counters match reality (`"N updates"` on news, `"N chapters"` on publications, `"N novel"` / `"N complete"` on books). The full procedure for adding news is `docs/openclaw/latest-updates-runbook.md`.

## Social metadata — the `<!-- social -->` block

Added 2026-08-26. Every one of the 47 enumerated pages carries a delimited block in `<head>`:

```html
<!-- social -->
<link rel="canonical" href="https://anirach.com/blog/<slug>.html">
<meta property="og:type" ...>  <!-- article | book | website | profile -->
...11 more tags...
<!-- /social -->
```

**Do not hand-edit one.** `check_site.py` **INV-27** (FAIL severity) recomputes the canonical path
from the file's own location and reads the real pixel size out of the JPEG/PNG header, so a wrong
`og:url` or a stale `og:image:width` fails the build. The delimiters make the block idempotently
replaceable by a sweep.

The canonical URL form is fixed and everything derives from it:

| Page | Canonical |
|---|---|
| root | `https://anirach.com/` |
| section index | `https://anirach.com/<dir>/` — trailing slash, never `/index.html` |
| blog post | `https://anirach.com/blog/<slug>.html` — **with** the extension |
| book detail | `https://anirach.com/books/<slug>.html` |

`.html` won over the extensionless form because 136 of the site's own links already use it, it is
the real on-disk path, and extensionless URLs 404 on the documented local dev server. The 7
`.series-nav` chips still link extensionless — that is fine and deliberate (INV-03 enforces it);
the canonical tag is what resolves the duplicate.

**`twitter:card` is chosen by cover shape**, not by preference: `summary_large_image` only at
≥1.5:1, otherwise `summary`. 25 of the 37 post covers are square, and a square cover in a large
card loses ~48% of its height — including the caption band these covers carry along the top.

**Three posts and all four books use a dedicated share card** rather than their own cover
(`images/<slug>-og.jpg`, 1200×630): the two posts whose covers are double-booked, the one post
with no image at all, and the four books whose portrait covers would lose ~65% of their height —
title band included — to a 1.91:1 centre crop. Each book card shows both language faces, English
left and Thai right, matching how the detail pages render them.

`404.html` is deliberately excluded from all of this: noindex, no social block, not in
`sitemap.xml`, not enumerated by `check_site.py`. Do not "fix" it by adding one.

**`sitemap.xml` is hand-maintained** — 47 `<loc>` entries with a per-file `lastmod` taken from
git. Nothing computes it; adding a page means adding its entry. This is the same drift profile as
the article counters, and only this sentence enforces it.

**Decisions taken deliberately, so they are not re-litigated every sweep:**

- **RSS feed: REVERSED 2026-08-26, with the original objection answered rather than ignored.**
  The standing decision was "no feed", because a hand-written one would drift like `sitemap.xml`
  and a generator would mean a build step. Both halves are now addressed: `feed.xml` is produced
  by `python3 scripts/gen_feed.py` **on demand** (no build step — the published tree is still
  plain static files), and `check_site.py` **INV-31** fails when the feed and the blog index
  disagree. The drift objection was also under-stated: `sitemap.xml` had no check whatsoever, so
  **INV-32** now covers it too. Regenerate the feed in the same commit as any new post.
- **The two free PDFs stay crawlable** but are excluded from `sitemap.xml`, so the detail page is
  what gets promoted. `robots.txt` carries the two commented-out `Disallow` lines to flip that.
- **`jekyll-seo-tag` is never the answer here** — these files have no front matter, so it emits
  nothing, and adding front matter would make Liquid evaluate the `{{ }}` code samples in 11 posts.
- **The `news/` event posters stay as direct `.jpg` links.** A shared image URL carries no
  metadata, but lightboxing a poster is a normal pattern and the book page is linked beside it.

**Cloudflare caches for 4 hours** (`max-age=14400` on assets, 600s on HTML). After a deploy that
adds a root file, the old 404 stays cached at the edge until it expires — `/favicon.ico` served a
cached 404 for a while after 2026-08-26 while the origin already had it. Append `?cb=$RANDOM` to
check the real state before diagnosing a deploy problem that is not there.

Two things remain the owner's to do, outside the repo: verify a Search Console property for
anirach.com, and set Cloudflare SSL/TLS to **Full** (GitHub holds no certificate for the custom
domain, so Cloudflare currently proxies to it over plain HTTP and every GitHub-issued redirect
targets `http://`). See `docs/openclaw/latest-updates-runbook.md` for the post-event copy expiry.

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
