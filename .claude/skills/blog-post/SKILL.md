---
name: blog-post
description: End-to-end recipe for adding, editing, or removing a post in blog/ on the anirach.com static site — choosing the right template and nav pattern, the canonical document skeleton, the bilingual .post-body conventions, the exact card markup for blog/index.html, the two article counters, cover-image naming, and rewiring the prev/next chain neighbours. Use this whenever a request touches blog/*.html, blog/index.html, or images/*-cover.*, or mentions writing a blog post, a new article, a DevOps or OpenClaw series entry, retitling a post, changing a cover, or reordering the series — even if the user only asks for "just the HTML file" or "a quick edit", because every post is wired into 3-8 other hand-maintained files with no build step to catch a miss. Commits 7a0db83, 4c180c9, 2f7ea33 and 3c01503 were all cleanups of exactly these misses.
---

# Adding and editing blog posts

> ## Standing rule — numbers in this skill are load-bearing
>
> **Any change that invalidates a number in a skill file must update that number in the
> same commit.** This file's counts, the `BASELINE` set in `assets/verify-wiring.py`, and
> the drift tables in `references/known-exceptions.md` are all measurements of the repo at
> a moment in time. A confidently wrong count here gets acted on. Three sitewide sweeps
> (`6670480`, `ec2827b`, `e8da9da`) plus Task 11's heading re-cut landed without touching
> this skill — which is how `verify-wiring.py` spent a session matching
> `<h2 class="card__title">` against 37 cards that had been `h4` since `635eb94`, silently
> reporting CLEAN while `check_site.py` independently found 8 stale nav titles.
>
> **Last full re-measure: 2026-08-26 against `21d5cfc`.** Headline counts re-measured
> 2026-09-01 after the Life (9 posts) and Hermes (10 posts) launches: **56 posts, 4 series**;
> granular tables below that still say 37 reflect the 2026-08-26 census — re-derive before acting.

This site has **no build step, no templating, no partials**. Each of the 57 files in
`blog/` — 56 posts plus `index.html` — embeds its own `<style>`, its own copy of the nav
markup, and its own footer. (The wider site is 47 HTML files: these 38 plus `index.html`,
the five section indexes `books/`, `news/`, `projects/`, `publications/`, and the four
`books/*.html` per-book detail pages.)
Nothing validates the wiring between them. A post is not "a file" — it is a file plus a
card plus two counters plus two neighbours' nav links, and every one of those is edited
by hand.

Read the whole recipe before touching anything. The order matters: the card in
`blog/index.html` is the source of truth that everything else is derived from.

## Step 0 — run the verifier first, and again at the end

```bash
python3 .claude/skills/blog-post/assets/verify-wiring.py
```

Stdlib-only, no deps. On a clean checkout it prints `CLEAN` with no `known:` and no
`warn:` lines — its `BASELINE` is empty. Run it **before** you edit so you know the tree
was clean, and after every file you touch. Anything that appears as `FAIL:` or `warn:`
was caused by your change.

Baseline on a clean `main` (2026-08-26, `21d5cfc`):

```
posts=56  cards=56  series-nav=26  post-nav=24  no-nav=6

CLEAN — no new wiring breakage (0 warn).
```

**0** known failures — the two shared-cover keys died with the drawn-cover system
(2026-08-26) and the counter keys in `b9fb125`. **0** broken-link warnings. **0** stale nav
titles, matching `check_site.py` INV-10 one-for-one (its `norm()` now strips tags like
`check_site.norm_title`, so the two linters agree). If your run does not start from that,
something else is already in flight.

## Step 1 — pick the category and series, which picks the nav pattern

As of Task 11 (2026-08-10), `blog/index.html` groups posts into three top-level
**categories** — `#cat-technology`, `#cat-academic` (Academic & Philosophy),
`#cat-lifestyle` (Lifestyle) — each an `h2 class="category__title"` band. Technology is
the only one with content today; it contains the two **series** below (each an
`h3 class="series-title"`, one heading level under its category). Academic & Philosophy
and Lifestyle currently render a single quiet `.category__note` line instead of any
cards — see `references/known-exceptions.md`.

There are exactly three in-post nav patterns and they are mutually exclusive. Which one
you use is decided by which category/series the post belongs to.

**The template lives in the page-design skill.** `TEMPLATE` below always means
`.claude/skills/page-design/assets/post-template.html`. This skill used to ship its own
copy at `assets/post-template.html`; it rotted three sweeps behind and was deleted on
2026-08-10 — see `assets/TEMPLATE-MOVED.md`.

| Category / series | Section in `blog/index.html` | Nav pattern | Template |
|---|---|---|---|
| Technology → **DevOps & Vibe Coding** (24 posts) | `#series-devops` | `.post-nav` prev/next pair, relative `foo.html` links | `TEMPLATE` — **the default** |
| Technology → **Numbered OpenClaw** (7 posts) | `#series-openclaw` | `.series-nav` 7-chip strip, absolute `/blog/<slug>` links | copy `blog/openclaw-skills.html`; read `references/openclaw-series.md` first |
| Technology → **Standalone** (6 posts) | either section | no nav block at all | `TEMPLATE` with the `.post-nav` block deleted |
| **Academic & Philosophy** (0 posts) | new `.blog-grid` inside `#cat-academic` | standalone (no nav) until the category reaches 2 posts, then a per-category `.post-nav` prev/next chain, same shape as DevOps's | `TEMPLATE` with the `.post-nav` block deleted for the 1st post; restore it once a 2nd exists |
| **Lifestyle** (0 posts) | new `.blog-grid` inside `#cat-lifestyle` | same rule as Academic & Philosophy | same |

Card sections: `#series-openclaw` 13 cards, `#series-devops` 24 = 37 Technology cards ==
37 total (Academic & Philosophy and Lifestyle carry 0). The nav partition
(what `verify-wiring.py` prints) is 7 series-nav + 24 post-nav + 6 no-nav = 37. All 24
`#series-devops` cards carry a `.post-nav` (the chain head `git-branching.html` included,
since 2026-08-26); the 6 no-nav posts are all `#series-openclaw` cards.

**Adding the first post to Academic & Philosophy or Lifestyle** replaces that category's
`.category__note` paragraph with a `.blog-grid` (copy the shape from `#series-devops`'s
`.blog-grid`, minus the `.series-description`) holding one card, and its
`.category__count` becomes `"1 article"`. No `.post-nav` yet — the post is standalone.
**Adding the second post** to the same category is what introduces its `.post-nav`
prev/next chain (Step 7's DevOps recipe applies, scoped to that category's cards instead
of `#series-devops`'s). Do not build a chain for a lone post.

Default to the DevOps template even for an AI/agent topic, but a post carded under
`#series-openclaw` must NOT carry `.post-nav` chrome — `claude-code-architecture.html`
and `openclaw-memory-architecture.html` used to, and INV-17 flagged both until their
blocks were deleted on 2026-08-26 (`f5e53fb`); they are standalone now. The numbered
OpenClaw series costs 10 file edits instead of 4. Its old problems are **gone**: canonical
`:root` (`6670480`), the 14 broken links (`b9fb125`), the missing meta descriptions and
the 4 badge-markup forms (2026-08-26) — `check_site.py` INV-05, INV-09, INV-14 and
INV-20b all PASS.

A post must never carry two patterns. `verify-wiring.py` fails on `BOTH`.

## Step 2 — cover image

Every post needs a cover, and the post's cover must be the same file its card shows.
That is the one cover rule that is currently 100% green across all 37 posts — keep it that
way.

- Put the file in `images/` as **`images/<slug>-cover.jpg`**. There are 36 covers and
  **all of them are JPG** since `ec2827b`/`21c8a55`; average 112 KB, largest 194 KB, none
  over 200 KB. Never PNG for a photo or AI illustration — PNG is for diagrams only.
  23 of 37 posts use the `<slug>-cover` name; the other 14 use deliberate short names
  (`iac-cover.jpg`, `auth-cover.jpg`, `sre-cover.jpg`, `linux-cli-cover.jpg`,
  `api-lifecycle-cover.jpg`, …). **Do not rename existing files to match the slug**; that
  breaks two references for zero gain.
- Give the `<img>` `width`, `height`, `loading` and `decoding`. 130 of 130 images on the
  site have all four; a new post without them is a regression, not a gap.
- If `images/<slug>-cover.*` already exists, the post must use it. The verifier fails
  otherwise.
- Never reuse another post's cover. Two posts already share covers because no dedicated
  asset was drawn (see `references/known-exceptions.md`); if you have no image, say so and
  offer to generate one rather than pointing at a neighbour's.

Diagrams inside the body are **PNGs in `images/`**, referenced with this wrapper:

```html
<div style="margin:2rem 0;text-align:center;">
  <img src="../images/<slug>-diagram.png" alt="..." style="max-width:100%;border-radius:12px;box-shadow:0 8px 30px rgba(0,0,0,0.2);">
</div>
```

Inline HTML/CSS diagrams and ASCII art were both tried and both reverted — they kept
breaking layout and one of them silently ate surrounding content (f4f7e1b and 4fc85af
introduced them; c270892, 4ae2660 and 2f7ea33 cleaned up the damage). Do not reintroduce
them.

## Step 3 — create the post file

```bash
cp .claude/skills/page-design/assets/post-template.html blog/<slug>.html
```

That file is the **single** post template in this repo. It already carries the canonical
28-token `:root`, the 4-line a11y block (`:focus-visible`, `prefers-reduced-motion`,
`color-scheme`, `text-wrap`), `aspect-ratio` on the cover box, full image attributes, and
`var(--measure)`/`var(--wide)`/`var(--radius-lg)` instead of hardcoded pixels.

Then fill every `{{PLACEHOLDER}}`. The skeleton, in order, is:

```
<!DOCTYPE html> / <html lang="th">          ← posts are lang="th"; only the two index
<head>                                          pages are lang="en"
  <title>{EN title} — {TH subtitle} | Anirach Mingkhwan</title>
  <meta name="description" content="{Thai, ~1 sentence}">
  <!-- social --> … <!-- /social -->, then the JSON-LD BlogPosting <script>
  Google Fonts: Inter + JetBrains Mono
  <style> :root vars → blog-nav → post-hero → post-body → post-nav → blog-footer
          → optional components → @media (max-width: 600px) </style>
</head>
<body>
  <nav class="blog-nav">      href="./" back link + short title
  <header class="post-hero">  tags, the file's ONLY <h1>, meta line, cover img
  <article class="post-body"> the article
  <div class="post-nav">      prev / next pair
  <footer class="blog-footer">
```

Non-negotiables, each because something on disk got them wrong:

- **`lang="th"`.** All 56 posts are `th`; `index.html` and `blog/index.html` are `en`.
- **Exactly one `<h1>`**, the `.post-hero__title`. Do not repeat the title in the body —
  `deployment-hosting.html` did, and the duplicate was removed on 2026-08-26; every post
  has exactly one now, and INV-11 carries no baseline entry, so a regression will fail.
- **`<meta name="description">` in Thai.** All 66 pages carry one since the 2026-08-26
  metadata sweep (the 6 that did not are fixed). `check_site.py` **INV-27** now fails the
  build on a missing or empty one — this is no longer a warning you can defer.
- **The `<!-- social -->` block.** Every page has one — canonical, `og:*`,
  `article:published_time` + `article:author`, `twitter:card`/`twitter:image`/
  `twitter:image:alt`, robots, `theme-color`, icons — wrapped in the literal
  `<!-- social -->` … `<!-- /social -->` delimiters so a sweep can replace it
  idempotently. The template ships it with placeholders; fill them, do not delete
  them. INV-27 recomputes the canonical from the file path and reads the image's real
  pixel size out of the JPEG header, so `og:url` and `og:image:width/height` cannot be
  guessed. `og:image` and `twitter:image` both point at the dedicated 1200×630 share
  card `images/<slug>-og.jpg` (drawn by `scripts/make_cover.py`, checked by INV-35),
  which is why `twitter:card` is always `summary_large_image` — only a square image
  would need `summary` (the large card crops ~48% off one).
- **`<nav class="blog-nav">` with `<a href="./" class="blog-nav__back">‹ Blog</a>`.**
  All 26 posts that have this nav use `href="./"` and nothing else. Eleven posts have no
  `<nav class="blog-nav">` back link. Five of them (openclaw-101, -agent-teams,
  -integrations, -production, -security) link back with `href="/blog/"` — the trailing
  slash was added on 2026-08-26; the bare `/blog` cost two redirects, one of them an
  https→http downgrade. Never write a bare directory href;
  four more (beyond-plugins, idle-self-improvement, obsidian-ai-jarvis,
  openclaw-migration) reach the index through other header/footer links; only
  openclaw-memory and openclaw-skills have no route to the blog index at all. Do not
  add a twelfth.
- **Keep the `:root` block, byte-identical.** Every post has the canonical 28-token block
  since `6670480` — the "ten posts have none" note that used to be here is obsolete.
  `style.css` is not loaded by any blog page (only `index.html` loads it), so the `:root`
  in the post file is the only place these variables exist. `check_site.py` INV-22 PASSes;
  keep it that way.
- **No executable `<script>`, no `data-reveal`.** No page in `blog/` loads JavaScript;
  the one `<script>` type allowed is `application/ld+json` (data, never executed —
  `check_site.py` INV-38), which the JSON-LD block described below uses. `data-reveal`
  is inert there despite what `CLAUDE.md` suggests. If you need a mobile menu, use the
  pure-CSS `.nav__toggle` checkbox pattern from `blog/index.html` — INV-12 enforces
  that every toggle is actually wired.

### The JSON-LD BlogPosting block (in `<head>`, right after `<!-- /social -->`)

Every post carries a JSON-LD `BlogPosting` block since the 2026-09-02 search-visibility
overhaul — the old `itemprop`/`itemscope` microdata is gone sitewide; never re-add any.
The block ships in the template with placeholders; fill them, do not restructure it:

- `headline` = the `<h1>` text (no `" | Anirach Mingkhwan"` tail); `image` = the
  1200×630 share card; `mainEntityOfPage` = the canonical URL. The `author` is a
  `Person` object with `"@id": "https://anirach.com/#person"` and the inline name
  `"Anirach Mingkhwan"` — copy it verbatim.
- **`datePublished` == `article:published_time` == every `<time datetime>` in the
  page.** One `{{DATE}}` (YYYY-MM-DD) fills all of them; `dateModified` starts equal
  to `datePublished` and moves on a substantive edit.
- **Every post is bilingual since 2026-09-03**, so `"inLanguage"` is the array
  `["th", "en"]` and `<meta property="og:locale:alternate" content="en_US">` sits
  directly after `og:locale`. `check_visibility.py` S1 treats the substring
  `class="l-en"` as the definition of "bilingual" and fails (FAIL severity) when a post
  carries the markup without the metadata — they must land in the same commit. Scalar
  `"inLanguage": "th"` and a missing alternate are now the regression, not the default.
- The `type` attribute is double-quoted `"application/ld+json"` — the one `<script>`
  type INV-38 allows, because the browser parses it as data and never executes it.

`python3 scripts/check_visibility.py --strict` validates the required fields and the
date agreement (plus one `h1`, no skipped heading levels, title 20–60 chars and
description 70–160 advisory, unique titles) — it is part of the Step 8 checklist.

The palette is the canonical 28-token block, identical in all 49 `:root` blocks —
do not retype it, copy it from the template or from `style.css:5`. Full table:
`page-design/references/tokens.md` §1.

Recolour only the theme lines the template marks (`.post-hero` gradient plus the three
hero text colours), picking a gradient from `page-design/SKILL.md` §5 — never inventing
one. Everything else stays indigo so posts look like one site. Adding a single topic
accent var **after** the canonical block — `--docker-blue: #2496ed` in
`docker-compose.html` — is the established way to bring in a brand colour.

## Step 4 — writing the body

The house style is **English headings and technical terms, Thai explanatory prose**.
Not translation — code-switching within the sentence. Real examples from
`blog/docker-compose.html`:

```html
<h2>Docker Compose คืออะไร?</h2>
<p>Docker Compose คือเครื่องมือที่ช่วย <strong>กำหนด + รันหลาย containers พร้อมกัน</strong> ด้วยไฟล์ <code>docker-compose.yml</code></p>

<h2>🔀 Multi-Environment — Dev vs Production</h2>
<h3>วิธีที่ 1: Override Files</h3>
```

Conventions that hold across the corpus:

- `<h2>` is a section break, usually `{English noun phrase}` + Thai question or
  `— {Thai gloss}`, often led by one emoji. `<h3>` for sub-steps. `<hr>` between major
  sections.
- Technical nouns stay in English and get `<strong>` on first use. Commands, filenames
  and flags go in `<code>`.
- Code blocks are `<pre><code>` with **Thai comments**: `# ติดตั้ง dependencies`.
  No syntax-highlighting library exists; `.post-body pre code` styling is all there is.
- `<blockquote>` is the callout, conventionally opened with `<strong>💡 จำง่ายๆ:</strong>`
  or `<strong>💡 หมายเหตุ:</strong>`.
- Tables are plain `<thead>`/`<tbody>`; English column headers, Thai cells.
- Open with 2-3 short paragraphs: a callback to the previous post, a `🤔` hook question,
  then the one-line answer. Close with `<h2>สรุป</h2>`, a lead-in ending in `:`, and a
  `<ul>` of `<strong>Term</strong> = Thai one-liner` bullets.
- End the article with the series footer, before `</article>`:
  `<div class="post-series-footer">บทความจากซีรีส์ DevOps & Vibe Coding 2026</div>`
  (22 posts use exactly that string).
- A `🐕` on the last bullet is the running house joke. Keep it if the post is in the
  DevOps series.

## Answer-readiness (editorial, not lint)

These are editorial choices that make sections quotable by AI answer engines. **No
linter enforces them and none should** — English NLP heuristics are broken on Thai
prose, so any automated check would be noise. Apply them while writing, not in a sweep:

- Open each `h2` section with the direct answer in its first 40–60 words; elaboration
  comes after the answer, never before it.
- Prefer definition-style openers for concept sections: "X คือ… / X is a…".
- Use one comparison `<table>` where the post genuinely compares things — never
  decoratively.
- Use `<ol>` for procedures a reader performs in order; `<ul>` stays for everything
  else.

## Step 4b — the English track

**All 56 posts are bilingual, so a new one is not finished until it has an English
track.** Write the Thai article first and get it right; the English track is a faithful
mirror of finished prose, not a parallel draft.

Do not hand-build the switch. Run the converter:

```bash
python3 scripts/bilingualize.py --post <slug>     # all the mechanical edits
#   → writes .bilingual/<slug>.json, the Thai source of every placeholder
python3 scripts/bilingualize.py --fill <slug>     # splice .bilingual/<slug>.en.html back in
python3 scripts/bilingualize.py --verify <slug>   # the per-file checks; drive it to OK
```

Scaffolding inserts the checkbox, the hero pill, the ~26 lines of CSS (Deep Blue or
Sunrise, chosen from the post's own `.post-hero` gradient), `og:locale:alternate`, the
`inLanguage` array, both tables of contents, the `th-`/`en-` id split, and an `.l-en`
track of `%%EN-SECTION:id%%` placeholders. You write only the answer sheet — an HTML file
whose `<!--EN-TITLE-->`, `<!--EN-TOC:id-->`, `<!--EN-SECTION:id-->` and `<!--EN-FOOTER-->`
delimiters name what follows each one. `--fill` forces the `en-` ids and `#en-` anchors,
so the sheet never has to think about them.

What the English track must be:

- **Element-for-element identical to the Thai one.** `--verify` compares `h2`, `h3`,
  `pre`, `table` and `blockquote` counts between the tracks and fails on a mismatch —
  that check exists because "translate this section" quietly becomes "summarise this
  section" on a long post.
- **Complete.** Table cells, image alt text, the labels baked into inline-styled diagram
  divs, and the Thai `#` comments inside code blocks are all prose. `--verify` fails on
  any Thai character left in the EN track. The code itself, command names, paths, URLs,
  class names and ids are identical in both tracks.
- **In the house voice** — a professor writing for practitioners. Read the EN track of
  `blog/hermes-101.html` before starting; it is the register reference.

What stays monolingual, and why (each of these is read by a regex that concatenates or
truncates on a nested tag): the card title and excerpt in `blog/index.html`
(`gen_feed.py`'s `text_of` would emit `"ThaiEnglish"` into the feed), `.post-nav__title`
and `.post-nav__dir` (INV-10, `RE_PLINK`), the `.series-nav` chips and their `<h3>`
(INV-03/03b), the OpenClaw ordinal badge line (INV-20a is line-scoped), `<title>`, the
meta description, `og:title`/`og:description`/`og:image:alt`/`twitter:image:alt`
(T1/T2/T3) and the single `<time datetime>` (INV-36).

## Step 5 — the card in `blog/index.html`

New cards go at the **top** of their `.blog-grid`, immediately after the
`<div class="blog-grid">` line (blog/index.html:238 for `#series-openclaw`, and the
matching line inside `#series-devops`) — i.e. before the existing first
`<!-- Card: … -->` comment. Newest-first is not cosmetic — for the DevOps
series, `reversed(#series-devops card order)` **is** the prev/next chain, verified
byte-identical over all 24 nodes. Put the card in the wrong place and the chain is wrong.

Copy this exactly, including the odd indentation (the comment is indented 8, the anchor 6
— every card on the page is like that; do not tidy it):

```html
        <!-- Card: {Short English Name} -->
      <a href="{slug}.html" class="card">
        <div class="card__image">
          <img src="../images/{cover-file}" alt="{Short English Name}" style="background: linear-gradient(135deg, #1a4d7a, #7c3aed, #06b6d4);">
        </div>
        <div class="card__body">
          <div class="card__tags">
            <span class="card__tag">{Tag 1}</span>
            <span class="card__tag">{Tag 2}</span>
            <span class="card__tag">{Tag 3}</span>
          </div>
          <h4 class="card__title">{EN Title} — {TH subtitle} {emoji}</h4>
          <p class="card__excerpt">{one Thai sentence, no trailing period}</p>
          <div class="card__footer">
            <div class="card__author">
              <img src="../images/profile.jpg" alt="Anirach" class="card__avatar">
              <div>
                <div class="card__author-name">Anirach Mingkhwan</div>
              </div>
            </div>
            <span class="card__read">Read →</span>
          </div>
        </div>
      </a>
```

- **`<h4>`, not `<h2>`.** Task 11 (`635eb94` + `4a31036`) gave `blog/index.html` a real
  heading ladder — `h1` page title → `h2` ×3 `.category__title` → `h3` ×2 `.series-title`
  → `h4` ×37 `.card__title`. All 37 cards on disk are `h4`
  (`grep -c '<h4 class="card__title">' blog/index.html` → 37). An `h2` here collides with
  the category band; an `h3` collides with the series heading. Any tool that greps for
  card titles must use `<h[1-6] class="card__title">` with a backreference — hardcoding
  the level is what blinded `verify-wiring.py`.
- The `href` is relative with `.html` — `blog/index.html` never uses the extensionless
  form. Only the 7 OpenClaw series posts do, in their own chip strip.
- The `img src` must be byte-identical to the cover the post itself embeds, and the
  `<img>` needs `width`, `height`, `loading="lazy"` and `decoding="async"` — 130/130
  images on the site have all four.
- The inline `background:` gradient is a placeholder shown while the image loads; pick
  hues that match the post's hero gradient.
- `card__title` must equal the post's `<h1>` text. It is also the string the neighbours'
  `.post-nav__title` labels must copy — eight of those have already drifted.

## Step 6 — the counters

`blog/index.html` carries **six** hand-maintained counter sites since Task 11. **All six
are correct today** — `b9fb125` fixed the two that were stale — and `check_site.py`
INV-02a–INV-02e all PASS with no baseline entries, so anything you break here fails
immediately.

| Counter | Value today | Changes when you add a post? |
|---|---|---|
| `.blog-hero__stat` "N Categories" | — | the stat was deleted 2026-08-26; re-add it only if a second `.category` band ever ships, and INV-02e will then verify it |
| `.blog-hero__stat` "N Series" | 3 | only if you add a `.series-section` |
| `.blog-hero__stat` "N Articles" | 46 | **yes, always** |
| `.category__count` `#cat-technology` | 37 articles | **yes**, for a Technology post |
| `.series-count` `#series-openclaw` | 13 articles | yes, if the post lands there |
| `.series-count` `#series-devops` | 24 articles | yes, if the post lands there |
| `.series-count` `#series-life` | 9 | if the post lands there |

**No line numbers.** They have moved twice (Task 10 and Task 11) and every hardcoded one
in this skill had rotted. Grep for the class.

They drifted originally because people incremented them by hand. **Recompute instead:**

```bash
grep -c 'class="card"' blog/index.html                       # total → hero Articles
python3 - <<'EOF'
import re
s=open('blog/index.html',encoding='utf-8').read()
for sid,body in re.findall(r'<section class="series-section" id="([^"]+)">(.*?)</section>',s,re.S):
    print(sid, len(re.findall(r'class="card"',body)))
EOF
```

Set the hero stat, the `.category__count` and the relevant `.series-count` to what those
commands print. Adding the *first* post to Academic & Philosophy or Lifestyle changes that
category's band, grid, card and `.category__count` in ONE commit (INV-02d rejects an empty
band since 2026-08-26) — see
Step 1. INV-02d treats the coming-soon label as clean and flags both a stale number and a
literal `"0"`.

## Step 7 — rewire the neighbours (DevOps series only)

The chain is derived from card order, so never hand-author it. With the card already at
the top of `#series-devops`:

**Appending at the top** (the normal case). Let `T` be the post that was previously the
top card, i.e. the old chain tail.

1. New post: `prev → T.html`, `next → "./"`.
2. `T.html`: change its `next` from `"./"` to `<newslug>.html`. `T`'s `prev` is untouched.

Today `T` is `vibe-coding-devops-process.html`, whose `next` href is `"./"`.

**Inserting into the middle** — the case that breaks things. If the new card lands between
card `A` (above it) and card `B` (below it) in `#series-devops`, then in chain order `B`
comes before the new post and `A` comes after. **Three files change, not one:**

| File | `prev` | `next` |
|---|---|---|
| `<newslug>.html` | `B.html` | `A.html` |
| `B.html` | unchanged | `A.html` → `<newslug>.html` |
| `A.html` | `B.html` → `<newslug>.html` | unchanged |

Forgetting either neighbour leaves an asymmetric edge: one post's `next` points forward
while the target's `prev` still points past it. The verifier catches this as
`prev=… but the card below it is …`.

The exact block to write, from `blog/docker-compose.html:703-712`:

```html
  <!-- Post Navigation -->
  <div class="post-nav">
    <a href="{prev-slug}.html" class="post-nav__link">
      <div class="post-nav__dir">← Previous</div>
      <div class="post-nav__title">{prev post's card__title}</div>
    </a>
    <a href="{next-slug}.html" class="post-nav__link">
      <div class="post-nav__dir">Next →</div>
      <div class="post-nav__title">{next post's card__title}</div>
    </a>
  </div>
```

- Use `<div class="post-nav">`, not `<nav>` — 24 posts use `div`, 0 use `nav` (INV-04c reports a `<nav>` at warn level).
- The direction strings are exactly `← Previous` and `Next →` with literal arrow
  characters. `claude-code-architecture.html` invented `Related` / `See also`; do not copy it.
- Copy `.post-nav__title` from the target's `card__title` verbatim, minus trailing emoji.
  Eight labels had gone stale this way; all were rewritten on 2026-08-26 and INV-10 now
  reports any new one (warn level — read the status lines, not just the exit code).
- Some existing Next anchors carry `style="text-align:right;"`. Harmless; leave them if
  present, do not add new ones.

For the numbered OpenClaw series the equivalent step is editing all 7 chip strips —
see `references/openclaw-series.md`.

## Step 8 — checklist

Adding a DevOps post touches **4 files** (5 with a diagram):

1. `images/<slug>-cover.jpg` — new file, JPG, ≤200 KB, not shared with any other post.
2. `blog/<slug>.html` — from `page-design/assets/post-template.html`; one `<h1>`,
   `lang="th"`, meta description, the filled-in `<!-- social -->` block, canonical
   `:root`, the 4-line a11y block, `blog-nav`, `post-nav`, `blog-footer`, **and the
   English track** (Step 4b — `python3 scripts/bilingualize.py --post <slug>`, then
   `--fill`, then `--verify` until it prints OK).
3. `blog/index.html` — card at the top of the right `.blog-grid` with an
   `<h4 class="card__title">`, hero `Articles`, `.category__count` and the section's
   `.series-count` all **recomputed**.
4. The old top card's post file — its `next` changes from `"./"` to the new slug
   (plus a second neighbour if you inserted mid-chain).
5. `sitemap.xml` — regenerate, never hand-edit: `python3 scripts/gen_sitemap.py`
   (it replaced hand-maintaining the file; its `--check` mode and `check_site.py`
   INV-32 both fail on drift).
6. All three linters, from the repo root:
   ```bash
   python3 .claude/skills/blog-post/assets/verify-wiring.py     # no FAIL: lines
   python3 .claude/skills/site-check/scripts/check_site.py      # exit 0
   python3 scripts/check_visibility.py --strict                 # exit 0
   ```

Adding a numbered OpenClaw post touches **11 files**: the above, minus the post-nav
rewire, plus the `.series-nav` strip in all 7 existing series posts.

`CLAUDE.md` now does carry counts that a new post invalidates — the `images/` file count
and the sitemap's URL count. Update them in the same commit (page-design's standing rule).

## Editing an existing post

Match the blast radius to what you changed:

| Change | Also update |
|---|---|
| Title / `<h1>` | its `card__title` in `blog/index.html`, **and** the `.post-nav__title` label in whichever post links to it (`grep -l '{slug}.html' blog/*.html`) |
| Cover image | the `img src` in the post **and** in its card — they must stay identical |
| Slug / filename | the card `href`; both neighbours' `.post-nav` hrefs; any `/blog/<slug>` chip if it is a numbered OpenClaw post; `git mv` so history follows |
| Excerpt, tags | card only |
| Body prose | nothing else |
| Reordering the series | move the card, then re-derive every affected `prev`/`next` from the new card order — never edit nav links first |
| Deleting a post | remove the card, recompute both counters, and heal the chain by joining its two neighbours to each other |

When editing one of the 7 numbered OpenClaw posts, open
`references/openclaw-series.md` first — those files carry the `.blog-nav` back link since
the 2026-08-26 island→house conversion, but still have their own conventions you should
not make worse. (They *do* have the canonical `:root` now, and
their 14 broken links were fixed in `b9fb125`.)

Because there are no shared partials, a request to change styling "everywhere" means
editing up to 38 `<style>` blocks in `blog/` — 47 for the whole site. Say so and get
confirmation before starting; do not change one post and call it done.

## When something looks broken

`references/known-exceptions.md` lists what is intentionally asymmetric — today only the
six no-nav posts (the chain head `git-branching` now has a real `.post-nav`; the two
OpenClaw cards that wore DevOps chrome lost it and are no-nav) — and records that the
standing drift is gone: no shared covers, one footer variant (`blog-footer` ×37), one
copyright string, 0 stale nav titles, and no two-`<h1>` post. The old second bug —
`blog/index.html` rendering a hamburger with no JavaScript — was **fixed in Task 9** and
replaced with the pure-CSS checkbox toggle. Check that file before "fixing" anything you
did not introduce.
