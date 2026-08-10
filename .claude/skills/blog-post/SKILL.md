---
name: blog-post
description: End-to-end recipe for adding, editing, or removing a post in blog/ on the anirach.com static site — choosing the right template and nav pattern, the canonical document skeleton, the bilingual .post-body conventions, the exact card markup for blog/index.html, the two article counters, cover-image naming, and rewiring the prev/next chain neighbours. Use this whenever a request touches blog/*.html, blog/index.html, or images/*-cover.*, or mentions writing a blog post, a new article, a DevOps or OpenClaw series entry, retitling a post, changing a cover, or reordering the series — even if the user only asks for "just the HTML file" or "a quick edit", because every post is wired into 3-8 other hand-maintained files with no build step to catch a miss. Commits 7a0db83, 4c180c9, 2f7ea33 and 3c01503 were all cleanups of exactly these misses.
---

# Adding and editing blog posts

This site has **no build step, no templating, no partials**. Each of the 38 files in
`blog/` — 37 posts plus `index.html` — embeds its own `<style>`, its own copy of the nav
markup, and its own footer.
Nothing validates the wiring between them. A post is not "a file" — it is a file plus a
card plus two counters plus two neighbours' nav links, and every one of those is edited
by hand.

Read the whole recipe before touching anything. The order matters: the card in
`blog/index.html` is the source of truth that everything else is derived from.

## Step 0 — run the verifier first, and again at the end

```bash
python3 .claude/skills/blog-post/assets/verify-wiring.py
```

Stdlib-only, no deps. On a clean checkout it prints `CLEAN` plus a list of `known:` and
`warn:` lines that are pre-existing and baselined. Run it **before** you edit so you know
what was already broken, and after every file you touch. Anything that appears as `FAIL:`
was caused by your change.

Baseline on a clean `main` (2026-08-10): `posts=37 cards=37 series-nav=7 post-nav=25
no-nav=5`, 4 known failures, 14 broken-link warnings in the OpenClaw series, 8 stale nav
titles. If your run does not start from that, something else is already in flight.

## Step 1 — pick the series, which picks the nav pattern

There are exactly three in-post nav patterns and they are mutually exclusive. Which one
you use is decided entirely by which series the post belongs to.

| Series | Section in `blog/index.html` | Nav pattern | Template |
|---|---|---|---|
| **DevOps & Vibe Coding** (24 posts) | `#series-devops` | `.post-nav` prev/next pair, relative `foo.html` links | `assets/post-template.html` — **the default** |
| **Numbered OpenClaw** (7 posts) | `#series-openclaw` | `.series-nav` 7-chip strip, absolute `/blog/<slug>` links | copy `blog/openclaw-skills.html`; read `references/openclaw-series.md` first |
| **Standalone** (5 posts) | either section | no nav block at all | `assets/post-template.html` with the `.post-nav` block deleted |

Card sections: `#series-openclaw` 13 cards, `#series-devops` 24 = 37. The nav partition
(what `verify-wiring.py` prints) is 7 series-nav + 25 post-nav + 5 no-nav = 37.
`git-branching.html` is a `#series-devops` card with no nav, so it appears in two rows
above.

Default to the DevOps template even for an AI/agent topic. Two posts already do exactly
that — `claude-code-architecture.html` and `openclaw-memory-architecture.html` are carded
under `#series-openclaw` but use `.post-nav` chrome. The numbered OpenClaw series is the
un-templated corner of the site (no `:root`, no `.blog-nav` back link, 14 broken links, 5
missing meta descriptions); adding to it costs 10 file edits instead of 4.

A post must never carry two patterns. `verify-wiring.py` fails on `BOTH`.

## Step 2 — cover image

Every post needs a cover, and the post's cover must be the same file its card shows.
That is the one cover rule that is currently 100% green across all 37 posts — keep it that
way.

- Put the file in `images/`. Prefer `images/<slug>-cover.png` or `.jpg` — 23 of 37 posts
  follow that. The other 14 use deliberate short names (`iac-cover.jpg`, `auth-cover.jpg`,
  `sre-cover.jpg`, `linux-cli-cover.jpg`, `api-lifecycle-cover.jpg`, …). **Do not rename
  existing files to match the slug**; that breaks two references for zero gain.
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
cp .claude/skills/blog-post/assets/post-template.html blog/<slug>.html
```

Then fill every `{{PLACEHOLDER}}`. The skeleton, in order, is:

```
<!DOCTYPE html> / <html lang="th">          ← posts are lang="th"; only the two index
<head>                                          pages are lang="en"
  <title>{EN title} — {TH subtitle} | Anirach Mingkhwan</title>
  <meta name="description" content="{Thai, ~1 sentence}">
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

- **`lang="th"`.** All 37 posts are `th`; `index.html` and `blog/index.html` are `en`.
- **Exactly one `<h1>`**, the `.post-hero__title`. Do not repeat the title in the body —
  `deployment-hosting.html` did and now has two (lines 164 and 176).
- **`<meta name="description">` in Thai.** Six posts are missing it.
- **`<nav class="blog-nav">` with `<a href="./" class="blog-nav__back">‹ Blog</a>`.**
  All 26 posts that have this nav use `href="./"` and nothing else. Eleven posts have no
  `<nav class="blog-nav">` back link. Five of them (openclaw-101, -agent-teams,
  -integrations, -production, -security) still link back with a bare `href="/blog"`;
  four more (beyond-plugins, idle-self-improvement, obsidian-ai-jarvis,
  openclaw-migration) reach the index through other header/footer links; only
  openclaw-memory and openclaw-skills have no route to the blog index at all. Do not
  add a twelfth.
- **Keep the `:root` block.** Ten posts have none and are stuck on hex literals.
  `style.css` is not loaded by any blog page (only `index.html` loads it), so the `:root`
  in the post file is the only place these variables exist.
- **No `<script>`, no `data-reveal`.** No page in `blog/` loads JavaScript. `data-reveal`
  is inert there despite what `CLAUDE.md` suggests.

The palette, from the template's `:root`:

```css
--navy: #0f172a;  --blue: #6366f1;  --blue-dark: #4f46e5;  --blue-light: #818cf8;
--slate: #334155; --slate-light: #64748b; --gray: #94a3b8;
--bg: #f8fafc;    --white: #ffffff; --code-bg: #1e293b;
```

Recolour only the three theme lines the template marks (`.post-hero` gradient,
`.post-hero__tag` colour, `.post-hero__series` colour). Everything else stays indigo so
posts look like one site. Adding a single topic accent var — `--docker-blue: #2496ed` in
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
          <img src="../images/{cover-file}" alt="{Short English Name}" style="background: linear-gradient(135deg, #4f46e5, #7c3aed, #06b6d4);">
        </div>
        <div class="card__body">
          <div class="card__tags">
            <span class="card__tag">{Tag 1}</span>
            <span class="card__tag">{Tag 2}</span>
            <span class="card__tag">{Tag 3}</span>
          </div>
          <h2 class="card__title">{EN Title} — {TH subtitle} {emoji}</h2>
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

- The `href` is relative with `.html` — `blog/index.html` never uses the extensionless
  form. Only the 7 OpenClaw series posts do, in their own chip strip.
- The `img src` must be byte-identical to the cover the post itself embeds.
- The inline `background:` gradient is a placeholder shown while the image loads; pick
  hues that match the post's hero gradient.
- `card__title` must equal the post's `<h1>` text. It is also the string the neighbours'
  `.post-nav__title` labels must copy — eight of those have already drifted.

## Step 6 — the counters

`blog/index.html` carries four hand-maintained counter sites (two of which change on a
normal post add: the hero Articles pill and your section's badge). Two are stale today:

- line 220 `<span class="blog-hero__stat"><strong>2</strong> Series</span>` — correct
- line 221 `<span class="blog-hero__stat"><strong>33</strong> Articles</span>` — **stale, actual is 37**
- line 235 `<span class="series-count">12 articles</span>` (`#series-openclaw`) — **stale, actual is 13**
- line 573 `<span class="series-count">24 articles</span>` (`#series-devops`) — correct

They drifted because people incremented them by hand. **Recompute instead:**

```bash
grep -c 'class="card"' blog/index.html                       # total → hero Articles
python3 - <<'EOF'
import re
s=open('blog/index.html',encoding='utf-8').read()
for sid,body in re.findall(r'<section class="series-section" id="([^"]+)">(.*?)</section>',s,re.S):
    print(sid, len(re.findall(r'class="card"',body)))
EOF
```

Set the hero stat and both `.series-count` values to what those commands print, including
fixing the two that are already wrong. `verify-wiring.py` baselines the current drift, so
correcting it will make the `known:` lines disappear — that is the desired direction.

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

- Use `<div class="post-nav">`, not `<nav>` — 21 posts use `div`, 4 use `nav`.
- The direction strings are exactly `← Previous` and `Next →` with literal arrow
  characters. `claude-code-architecture.html` invented `Related` / `See also`; do not copy it.
- Copy `.post-nav__title` from the target's `card__title` verbatim, minus trailing emoji.
  Eight labels have already gone stale this way.
- Some existing Next anchors carry `style="text-align:right;"`. Harmless; leave them if
  present, do not add new ones.

For the numbered OpenClaw series the equivalent step is editing all 7 chip strips —
see `references/openclaw-series.md`.

## Step 8 — checklist

Adding a DevOps post touches **4 files** (5 with a diagram):

1. `images/<slug>-cover.{png,jpg}` — new file, not shared with any other post.
2. `blog/<slug>.html` — from `assets/post-template.html`; one `<h1>`, `lang="th"`,
   meta description, `:root`, `blog-nav`, `post-nav`, `blog-footer`.
3. `blog/index.html` — card at the top of the right `.blog-grid`, hero `Articles` count
   and the section's `.series-count` **recomputed**.
4. The old top card's post file — its `next` changes from `"./"` to the new slug
   (plus a second neighbour if you inserted mid-chain).
5. `python3 .claude/skills/blog-post/assets/verify-wiring.py` → no `FAIL:` lines.

Adding a numbered OpenClaw post touches **10 files**: the above, minus the post-nav
rewire, plus the `.series-nav` strip in all 7 existing series posts.

Do not update `CLAUDE.md`'s counts unless asked; it does not carry any.

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
`references/openclaw-series.md` first — those files have no `:root`, no `.blog-nav`
back link, and their own set of already-broken links you should not make worse.

Because there are no shared partials, a request to change styling "everywhere" means
editing up to 38 `<style>` blocks. Say so and get confirmation before starting; do not
change one post and call it done.

## When something looks broken

`references/known-exceptions.md` lists what is intentionally asymmetric — the chain head
with no nav, the two off-chain OpenClaw cards, the five no-nav posts, the two shared
covers — plus the standing drift (4 footer variants, 4 copyright cohorts, 8 stale nav
titles) and the two genuine bugs worth reporting to the user (`blog/index.html` has a
hamburger button with no JavaScript; `deployment-hosting.html` has two `<h1>`). Check it
before "fixing" anything you did not introduce.
