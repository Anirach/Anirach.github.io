# Component vocabulary — real markup

Every snippet here is copied from a real file in this repo. Copy these; do not paraphrase them.
Where a snippet is marked **NEW** or **still 0 uses**, it is a proposed SKILL.md §4 primitive that
replaces a sprawl of one-off names — use it for new work, and migrate old names only when you are
already editing that file.

Line numbers have been dropped from the citations. They moved under `d44adb9` (TOC + ids),
`662e966` (island conversion) and the 2026-09-03 bilingual sweep, and a wrong line number is worse
than none — grep for the class instead.

Re-measured **2026-09-06** against `905d3a4`: 87 HTML files, 76 posts, all HOUSE, all bilingual.
Counts of anything *inside* `.post-body` are roughly **2×** their pre-2026-09-03 values, because
the article body exists once per language track.

---

## 1. Chrome — the three things before `<main>`, then `.blog-nav`

**The nav is not the first thing in `<body>` any more.** Two elements precede it in all 76 posts
and both are load-bearing for a linter. Copy the whole opening, not just the `<nav>`:

```html
<body>
<a href="#main" class="skip-link">Skip to content</a>
<input type="checkbox" id="langSwitch" class="lang-switch-box" aria-label="Switch language: Thai / English">

  <nav class="blog-nav">
    <div class="blog-nav__inner">
      <a href="../index.html" class="blog-nav__home">Anirach</a>
      <a href="./" class="blog-nav__back">‹ Blog</a>
      <div class="blog-nav__title">API Request Lifecycle</div>
    </div>
  </nav>

  <main id="main">
```

- **`.skip-link` + `id="main"` are a pair.** INV-30 fails if either exists without the other. All
  87 pages have both.
- **`.blog-nav__home` is not decoration.** It is the "no post is a dead end" half of INV-29
  (`d44adb9`); the other half is the `.blog-footer__nav` row in §5. A post without both fails the
  build. 76/76 carry them.
- **The checkbox must be a direct child of `<body>`, before `<main>`.** The TH ⇄ EN switch is a
  general sibling combinator (`#langSwitch:checked ~ main .l-en`), which reaches nothing above
  itself. Three posts had to have their `<main>` moved up to wrap the hero for exactly this reason
  (`deployment-hosting`, `openclaw-memory-architecture`, `vibe-coding-devops-process`, 2026-09-03).
- **Never rename `.lang-switch-box` / `.l-th` / `.l-en`.** They are verified clear of INV-12's
  menu-token regex (`hamburger|burger|nav__toggle|nav-toggle|navtoggle|menu-toggle|menu__toggle`);
  a rename that trips it makes the linter demand a `<script>` the site is forbidden to have.

CSS — this is the **fixed** variant (21 of the 76 posts have it; the other 55 are missing the
three flex properties on `.blog-nav__back`). Use this version:

```css
.blog-nav {
  position: fixed; top: 0; left: 0; right: 0; z-index: 100;
  background: rgba(248,250,252,0.85); backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(0,0,0,0.05);
}
.blog-nav__inner {
  max-width: var(--wide); margin: 0 auto; padding: 0 2rem; height: 56px;
  display: flex; align-items: center; justify-content: space-between;
}
.blog-nav__back {
  font-size: 0.85rem; font-weight: 500; color: var(--blue);
  text-decoration: none; display: flex; align-items: center; gap: 0.4rem;
}
.blog-nav__back:hover { color: var(--blue-dark); }   /* 64 files hard-code #1a4d7a here — same
                                                        value, still untokenised; 10 use the var */
.blog-nav__title {
  font-size: 0.85rem; font-weight: 600; color: var(--navy);
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 50%;
}
.blog-nav { view-transition-name: site-nav; }        /* bb9c7dc — pure CSS, no JS fallback */
```

The glassy `rgba(248,250,252,0.85)` + `blur(20px)` `.blog-nav` block is the house look — do not
change it. Re-measured across the 76 posts: **65 on that value, 9 on `rgba(250,247,240,0.85)`**
(the `--bg` tint, from the island conversion), plus the two minified forks
(`openclaw-memory-architecture.html` `blur(14px)`/`z-index:50`,
`vibe-coding-devops-process.html` `blur(16px)`). `blog/index.html` uses `0.88` on `.nav`. 87 files
use `backdrop-filter` somewhere.

`.nav` (used by `index.html` and by the 9 section pages) is a **different component with the same
name in two places**. It was three until `662e966` retired the island posts' third meaning. That
collision is still the main blocker on ever sharing a stylesheet — see SKILL.md anti-pattern 2.

---

## 2. Header — `.post-hero`

Markup, reproduced from `blog/api-request-lifecycle.html` as it stands after the bilingual
conversion. **The `<h1>` carries both languages; the nav and the ordinal badge do not** — INV-03,
INV-10 and `gen_feed.py` all read those with regexes that concatenate or truncate on a nested tag.

```html
<header class="post-hero">
  <div class="post-hero__tags">
    <span class="post-hero__tag">API</span>
    <span class="post-hero__tag">HTTP</span>
    <span class="post-hero__tag">Backend</span>
  </div>
  <h1 class="post-hero__title"><span class="l-th">API Request Lifecycle — เมื่อกด Send เกิดอะไรขึ้นบ้าง?</span><span class="l-en" lang="en">API Request Lifecycle — What Actually Happens When You Hit Send?</span></h1>
  <div class="post-hero__meta">
    <span>By <strong>Anirach Mingkhwan</strong></span>
    <span class="post-hero__series">DevOps &amp; Vibe Coding 2026</span>
    <span><time datetime="2026-03-07">7 Mar 2026</time></span>
  </div>
  <label for="langSwitch" class="lang-switch" title="สลับภาษา · Switch language"><span class="lang-th">ไทย</span><span class="lang-sep">·</span><span class="lang-en" lang="en">English</span></label>
  <div class="post-hero__cover">
    <img src="../images/api-lifecycle-cover.jpg" alt="API Lifecycle — เมื่อกด Send เกิดอะไรขึ้นบ้าง"
         width="800" height="800" loading="eager" fetchpriority="high" decoding="async">
  </div>
</header>
```

**Covers are 800×800.** The drawn-cover system (`1103b7a`, `ee6b708`) made every post cover a
square 800×800 JPG; the `1600 × 900` this snippet used to show was the AI-clip-art era.
`width`/`height` are the source pixel size. The `<time>` in `.post-hero__meta` must agree with
`feed.xml` and with `article:published_time` — INV-36 checks all three.

**`.lang-switch` is the visible pill; `.lang-switch-box` is the hidden checkbox in §1.** They are
different elements and the pill is a `<label for="langSwitch">`, so it works with no JS. Note the
name collision that is deliberate: `.lang-en` is a *span inside the pill*, `.l-en` is a *content
track*. Do not merge them.

```css
.post-hero {
  padding: 8rem 2rem 3rem;
  background: linear-gradient(135deg, #eef3f3 0%, #dee7e6 50%, #e9e1c4 100%);  /* Sunrise */
  text-align: center;                    /* or Deep Blue. Those are the only two — INV-28. */
}
.post-hero__tags { display: flex; gap: 0.5rem; justify-content: center; margin-bottom: 1.25rem; }
.post-hero__tag {
  font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em;
  color: var(--blue); background: rgba(34,98,153,0.1);   /* Sunrise heroes: 32 files.
                                                            Deep Blue heroes use
                                                            rgba(255,255,255,0.18) — 37 files,
                                                            because the tag sits on dark. */
  padding: 0.3rem 0.75rem; border-radius: 20px;      /* pill — the one place 20px is right */
}
.post-hero__title {
  font-size: clamp(1.8rem, 5vw, 3rem); font-weight: 800; color: var(--navy);
  line-height: 1.2; margin-bottom: 1rem;
  max-width: var(--measure); margin-left: auto; margin-right: auto;
  text-wrap: balance;                                 /* landed in e8da9da — 87/87 pages */
}
.post-hero__meta {
  font-size: 0.85rem; color: var(--slate-light);
  display: flex; align-items: center; justify-content: center; gap: 1.5rem;
}
.post-hero__series { font-weight: 600; color: var(--blue); }
.post-hero__cover {
  max-width: 380px; margin: 2.5rem auto 0;   /* 380px in 75 of 75 — the 420/480/520/560 forks
                                                are gone; do not reintroduce one */
  border-radius: var(--radius-lg, 16px); overflow: hidden;
  box-shadow: 0 20px 60px rgba(17,48,75,0.14);   /* --navy at 14% — 75 of 75, one value */
  aspect-ratio: 1 / 1;                       /* 75 of 75 declare a ratio; match the square cover */
}
.post-hero__cover img { width: 100%; height: 100%; object-fit: cover; display: block; }
```

`padding-top: 8rem` clears the 56px fixed nav. Pick the gradient from SKILL.md §5 — there are two,
and INV-28 fails the build on a third.

Note the `var(--radius-lg, 16px)` fallback form: it is what all 75 files write, and it is why
`grep -c 'var(--radius-lg)'` reports 3 rather than 78. Count with `var\(--radius-lg[,)]`.

---

## 3. Body — `.post-body`, and the two things inside it that every post now has

`.post-body` opens with a **pair** of `.post-toc` `<details>` blocks, one per language track, and
wraps every wide `<table>` or `<pre>` in a `.table-wrapper`. Both landed in `d44adb9`; the TOC is
in all 76 posts (152 blocks) and `.table-wrapper` is the single most-used class in the corpus at
346 occurrences.

```html
<article class="post-body">
  <details class="post-toc l-th" open>
    <summary>ในบทความนี้</summary>
    <ol>
      <li><a href="#th-api">API คืออะไร?</a></li>
      …
    </ol>
  </details>
  <details class="post-toc l-en" open>
    <summary>In this post</summary>
    <ol>
      <li><a href="#en-api">What Is an API?</a></li>
      …
    </ol>
  </details>
  …
```

**Heading ids are namespaced `th-` / `en-`, and each TOC links only into its own track.** Without
the prefix the two copies collide on one id and every anchor resolves to the Thai one. `d44adb9`
generated 376 of these ids against six counted heading shapes; a slug starting with a digit gets a
letter prefix, because `#3-cloud-providers` is a legal HTML id but not a valid CSS selector.

**One known exception, and do not copy it:** the `.references` section in the 20 AI Transformation
posts uses `<h2 id="references">` in *both* tracks, so those files carry a duplicate id. It is the
one place the namespacing rule was not applied. If you add a `.references` block to a new post,
use `th-references` / `en-references`.

```css
.post-body { max-width: var(--measure); margin: 0 auto; padding: 3rem 2rem 6rem; }
.post-body h2 {
  font-size: 1.6rem; font-weight: 800; color: var(--navy);
  margin: 3rem 0 1rem; padding-bottom: 0.5rem;
  border-bottom: 2px solid rgba(34,98,153,0.15);   /* 64 files. 3 still carry the pre-re-key
                                                      rgba(139,92,246,0.15) — fix on contact. */
}
.post-body h3 { font-size: 1.25rem; font-weight: 700; color: var(--navy); margin: 2.25rem 0 0.75rem; }
.post-body h4 { font-size: 1.05rem; font-weight: 700; color: var(--navy); margin: 1.75rem 0 0.6rem; }
.post-body p  { margin-bottom: 1.25rem; }
.post-body strong { font-weight: 700; color: var(--navy); }
.post-body a {
  color: var(--blue); text-decoration: underline;
  text-decoration-thickness: 1px; text-underline-offset: 2px;
}
```

No emoji in `<h2>`. At most about one emoji per section overall (SKILL.md anti-pattern 13).

---

## 4. Listing card — `.card`

`blog/index.html`, the `openclaw-migration.html` card (find it with
`grep -n 'openclaw-migration.html" class="card"' blog/index.html`). This is already textbook BEM
(76 cards in `blog/index.html`, `card__tag` ×257 sitewide) — the model for all future component
naming. Reproduced from disk, including the inline placeholder gradient.

```html
<a href="openclaw-migration.html" class="card">
  <div class="card__image">
    <img src="../images/openclaw-migration-cover.jpg" alt="" width="800" height="800"
         loading="lazy" decoding="async">
  </div>
  <div class="card__body">
    <div class="card__tags">
      <span class="card__tag">OpenClaw</span>
      <span class="card__tag">Migration</span>
      <span class="card__tag">DevOps</span>
    </div>
    <h3 class="card__title"><span lang="th">Self-Transferring OpenClaw Bot — ย้าย AI Agent ข้ามเครื่องแบบไม่พลาด 🚚</span></h3>
    <p class="card__excerpt"><span lang="th">คู่มือย้าย bot จาก VPS Ubuntu ไป Mac Studio แบบ step-by-step — backup, transfer, restore พร้อม self-check script ให้ bot ตรวจตัวเอง</span></p>
    <div class="card__footer">
      <div class="card__author">
        <img src="../images/profile.jpg" alt="" class="card__avatar" width="800" height="800"
             loading="lazy" decoding="async">
        <div><div class="card__author-name">Anirach Mingkhwan</div></div>
      </div>
      <span class="card__read">Read →</span>
    </div>
  </div>
</a>
```

**The title is `<h3>` today, and the level has moved twice.** It was `h2` originally; Task 11
(`635eb94`) pushed it to `h4` under 3 `.category` bands; the bands were deleted on 2026-08-26 and
the ladder tightened back to `h1` page title → `h2` (the `.feature__title` + 5 `.series-title`) →
`h3` ×76 `.card__title`. Any tool that greps for card titles must write
`<h[1-6] class="card__title">` and close it with a backreference — `verify-wiring.py` was blind for
exactly this reason, and `gen_feed.py` had `<h4>` hard-coded and silently emitted an empty feed.

**The card and the excerpt are monolingual, wrapped in `<span lang="th">` — not in `.l-th`/`.l-en`
tracks.** The listing is a single-language page and the switch does not exist there; a nested track
span inside `.card__title` would break the regexes that read it. Card `<img alt="">` is empty on
purpose: the anchor's accessible name comes from the title, so the cover is decorative.

Two notes on the images:

- The cover `<img>` in some cards carries an **inline** `style="background: linear-gradient(...)"` —
  a load placeholder, and one of the 38 remaining `135deg` gradients. Move it to a class or drop it.
- Covers and the avatar are both `800 × 800` since the drawn-cover system.
  `openclaw-migration-cover.jpg` is 33 KB — the 186 KB figure this section used to quote was the
  pre-`1103b7a` image.

`.card` in `blog/index.html` means "blog listing card"; the other section pages share the
vocabulary through modifiers (`card--row`, `card--quiet`, `card--feature`), which is the pattern to
copy. The same bare name is also used generically inside posts. Do not add a 19th `*-card` name;
use `.card--<modifier>`.

**The one card that is not a `.card`:** the spotlit post at the top of `blog/index.html` is
`class="feature"` with `.feature__media|__body|__eyebrow|__title|__excerpt`. Three separate regexes
count `class="card"` (`check_site.py` RE_CARD, `gen_feed.py`, `verify-wiring.py`), so giving the
feature that class would inflate every counter and duplicate a feed item. The HTML comment above it
says so — and because that comment contains the literal string `class="card"`, a raw
`grep -c 'class="card"' blog/index.html` returns **77** where the true card count is 76. Match the
full `<a href="…" class="card">` anchor, as RE_CARD does.

---

## 5. Post footer navigation — FOUR mutually exclusive patterns

Pick the one that matches the post's series. Never mix two in one file. INV-08 fails the build if a
post carries both a `.post-nav` and a `.series-nav`.

| Pattern | Members | Link form |
|---|---|---|
| A. `.post-nav` prev/next pair | the 24 DevOps posts | relative, with extension |
| B. `.series-nav` flat chip strip | 7 OpenClaw + 10 Hermes + 9 Life = 26 posts | absolute, extensionless |
| C. `.series-nav.series-links--grouped` | the 20 AI Transformation posts | absolute, extensionless |
| D. none | 6 standalone posts | — |

B and C together are the 46 `.series-nav` strips; 24 posts carry `.post-nav`; 6 carry neither.

**A. `.post-nav`** — DevOps posts, relative `.html` links.
`blog/api-request-lifecycle.html`:

```css
.post-nav {
  max-width: var(--measure); margin: 0 auto; padding: 0 2rem 3rem;
  display: flex; gap: 1.5rem; flex-wrap: wrap;
}
```

This flex form is the only form — all 24 files that declare `.post-nav` use it
(re-measured after `be68cae` converged the last two grid variants,
`vibe-coding-devops-process.html` and `deployment-hosting.html`, on it). `openclaw-memory-architecture.html`, the
other minified fork, no longer declares `.post-nav` at all — its DevOps-style block was deleted
2026-08-26 (`f5e53fb`) and the post is standalone.

The container is a `<div>`, never a `<nav>` — INV-04c. Both chain ends point at `./`. Editing the
chain means editing the two neighbours as well, and INV-04a/e/f check the symmetry and the order
against the `#series-devops` card order.

```html
<div class="post-nav">
  <a href="docker-vs-vms.html" class="post-nav__link">
    <div class="post-nav__dir">← Previous</div>
    <div class="post-nav__title">Docker Containers vs VMs — ต่างกันยังไง ใช้ตัวไหนดี?</div>
  </a>
  <a href="kubernetes-orchestration.html" class="post-nav__link">
    <div class="post-nav__dir">Next →</div>
    <div class="post-nav__title">Kubernetes — จัดการ Container ให้เป็นระบบด้วย K8s</div>
  </a>
</div>
```

**B. `.series-nav`, flat chip strip** — the 7 numbered OpenClaw posts, the 9 Life essays and the
10 Hermes guides. Absolute, extensionless links. Since `d44adb9` the strip is wrapped in a real
`<nav aria-label>` landmark and the current chip carries `aria-current="page"`:

```html
<nav aria-label="OpenClaw for Organizations">
<div class="series-nav">
  <h3>OpenClaw for Organizations 2026</h3>
  <div class="series-links">
    <span class="current" aria-current="page">#1 OpenClaw 101</span>
    <a href="/blog/openclaw-agent-teams">#2 Agent Teams</a>
    <a href="/blog/openclaw-memory">#3 Memory &amp; Knowledge</a>
    <a href="/blog/openclaw-security">#4 Security &amp; Access</a>
    <a href="/blog/openclaw-integrations">#5 Integrations</a>
    <a href="/blog/openclaw-skills">#6 Skills &amp; Automation</a>
    <a href="/blog/openclaw-production">#7 Production &amp; Scale</a>
  </div>
</div>
</nav>
```

The extensionless `/blog/<slug>` links are correct — GitHub Pages resolves them, INV-09 checks
every target. `/about`, `/research`, `/contact` and `/teaching` do **not** exist; strip those links
when you see them (SKILL.md anti-pattern 10).

**The strip is monolingual and identical in every member.** Do not wrap a chip label in `.l-th` /
`.l-en`, and do not reword one file's chip: INV-03 checks the OpenClaw seven, and **INV-03c**
checks the other three strips — each must be identical across its members, mark exactly itself
current, and link only to members. Adding a post to a flat-strip series means editing every file
in it.

**C. `.series-nav` with a GROUPED chip strip** — the 20 AI Transformation posts. Same `.series-nav`
container and the same chip styling; the only difference is that `.series-links` also carries
`--grouped` and holds four `.series-links__group` blocks of five, each led by a
`<p class="series-links__label">`. Twenty chips in one flat row was unreadable; the four labels are
the series' own arc (Reframe · Redesign · Engineer · Lead).

```html
<nav aria-label="AI Transformation for Organizations">
<div class="series-nav">
  <h3>🧭 AI Transformation for Organizations 2026</h3>
  <div class="series-links series-links--grouped">
    <div class="series-links__group">
      <p class="series-links__label">Reframe · เปลี่ยนกรอบคิด</p>
      <span class="current" aria-current="page">#1 Six Layers</span>
      <a href="/blog/ai-transformation-prediction">#2 Prediction</a>
      <a href="/blog/ai-transformation-learning-loop">#3 Learning Loop</a>
      <a href="/blog/ai-transformation-maturity">#4 Maturity</a>
      <a href="/blog/ai-transformation-portfolio">#5 Portfolio</a>
    </div>
    <div class="series-links__group">
      <p class="series-links__label">Redesign · ออกแบบองค์กรใหม่</p>
      <a href="/blog/ai-transformation-workflow">#6 Four Lanes</a>
      …four more…
    </div>
    …Engineer (#11–#15), Lead (#16–#20)…
  </div>
</div>
</nav>
```

```css
.series-links--grouped { display: grid; gap: 0.9rem; }
.series-links__group   { position: relative; display: flex; flex-wrap: wrap;
                         gap: 0.5rem; padding-left: 8.25rem; min-height: 2rem; }
.series-links__label   { position: absolute; left: 0; top: 0.45rem; width: 7.5rem;
                         margin: 0; font-size: 0.72rem; font-weight: 700;
                         text-transform: uppercase; letter-spacing: 0.08em;
                         color: var(--slate-light); line-height: 1.3; }
@media (max-width: 600px) {
  .series-links__group { padding-left: 0; }
  .series-links__label { position: static; width: auto; flex-basis: 100%;
                         margin-bottom: 0.1rem; }
}
```

Four rules govern this one, and each of them is why a check exists:

- **`--grouped` is a modifier, `__group` and `__label` are elements — `.series-links` is still the
  noun.** The §4 vocabulary is frozen; this is how you extend it (SKILL.md §4).
- **The chips must stay direct children of `.series-links__group`, and must contain no nested
  tags.** INV-03/03c read chip text with a regex; a `<span>` or an `<em>` inside a chip label
  concatenates or truncates it, and the strip stops matching its siblings.
- **The label is a `<p>`, not a heading.** The `<h3>` inside `.series-nav` is already the strip's
  heading; four more headings here would put four extra levels into every post's outline, and
  `d44adb9` had to delete three "Series Navigation" headings for precisely that reason. It is
  positioned out of flow into the left gutter on desktop and falls back to a full-width row on
  phones, so it reads as a gutter label rather than a section title either way.
- **The old parser stopped at the first `</div></div>`.** `Site._parse_navs` in `check_site.py`
  now walks div depth via `series_nav_body()`, and **INV-03d** is a linter self-check that it
  still survives the nesting. If you nest anything further inside a strip, run INV-03d first.

**Never hand-edit these twenty strips.** The series is generated: add the post to
`scripts/series/ai-transformation.json`, run `python3 scripts/build_series.py --post <slug>`, then
`python3 scripts/build_series.py --restrip` to rewrite the strip in the other twenty.

**D. none** — `beyond-plugins`, `claude-code-architecture`, `idle-self-improvement`,
`obsidian-ai-jarvis`, `openclaw-memory-architecture`, `openclaw-migration`. Leave as-is unless the
user asks for navigation. (`git-branching` left this list on 2026-08-26 when it became the DevOps
chain head; the two `-architecture` posts joined it the same day.)

Then the footer. It is now **two** parts, and INV-29 requires the second:

```html
<footer class="blog-footer">
  <nav class="blog-footer__nav" aria-label="Site">
    <a href="../index.html">Home</a>
    <a href="./">Blog</a>
    <a href="../publications/">Publications</a>
    <a href="../books/">Books</a>
    <a href="../projects/">Projects</a>
    <a href="../news/">News</a>
    <a href="../index.html#contact">Contact</a>
  </nav>
  <span>© 2026 Anirach Mingkhwan — Associate Professor, KMUTNB</span>
</footer>
```

```css
.blog-footer { background: var(--navy); padding: 2rem 0; text-align: center;
               view-transition-name: site-footer; }
.blog-footer a { color: var(--gold); text-decoration: none; font-weight: 600; font-size: 0.9rem; }
.blog-footer span { color: var(--gray); font-size: 0.8rem; display: block; margin-top: 0.4rem; }
```

The link colour is `var(--gold)` in 70 of the 71 posts that declare `.blog-footer a`, not
`var(--blue-light)` — the 2026-08-26 re-key made `--blue-light` borders-only, and `--focus` is
re-pointed to gold inside footers and `<pre>` where the blue ring collapses to 2.12:1. The one
outlier still writes `var(--purple-light)`; fix it on contact. The copyright reads
`© 2026 Anirach Mingkhwan — Associate Professor, KMUTNB` in all 77 files in `blog/`, and
INV-15/INV-16 check that year and the container class for uniformity.

---

## 6. Callout — **still 0 uses**, and the sprawl it should replace has grown

Re-measured today across `blog/` and `books/`. Halve these to get the authored count — the
bilingual conversion duplicates the article body, so every in-body class is matched twice:
`alert` (**346**, in 30 files), `diagram-box` (78), `arch-box` (54), `highlight-box` (30),
`info-note` (20), `compare-box` (8), `warning-box` (6), `tip` (4), `insight-box` (4),
`analogy-box` (4), `case-study-box` (2), `danger-box` (2), `success-box` (2). `series-info` is at
**0** and is retired, so it is 13 names now, not 14.

**`.alert` is the one that matters.** It went from 3 uses to 346 when the AI Transformation series
adopted it as its house caution box — it is now the single most-used bespoke name in the repo, and
it maps exactly onto `.callout--warn`. One class, 30 files: the cheapest first move in Phase 4b.

```html
<aside class="callout callout--warn">
  <div class="callout__title">ข้อควรระวัง</div>
  <p>Rate limit จะ reset ทุก 60 วินาที ไม่ใช่ทุกนาทีตามนาฬิกา</p>
</aside>
```

```css
.callout {
  border-left: 3px solid var(--blue);
  background: rgba(34,98,153,0.06);          /* the re-keyed --blue, not the old 99,102,241 */
  border-radius: var(--radius);
  padding: 1.25rem 1.5rem;
  margin: 2rem 0;
}
.callout__title { font-weight: 700; color: var(--navy); margin-bottom: 0.4rem; }
.callout--info { border-color: var(--cyan);        background: rgba(6,182,212,0.06); }
.callout--good { border-color: var(--green);       background: rgba(34,197,94,0.06); }
.callout--warn { border-color: var(--amber);       background: rgba(245,158,11,0.06); }
.callout--bad  { border-color: var(--red);         background: rgba(239,68,68,0.06); }
```

Byte-identical to the block in `assets/post-template.html`. Four modifiers, drawn from the six
status tokens. If you need a fifth mood, you almost certainly need one of these four.

**Any `rgba(99,102,241,…)` you find is pre-re-key indigo** and should become `rgba(34,98,153,…)`.
The same applies to the `.post-hero__tag` and inline-`code` tints further up this file if you
inherit them from an older copy.

**`.diagram-box` and `.arch-box` are dead weight** — remnants of the abandoned inline-HTML diagram
experiment (`f4f7e1b`, `4fc85af`, reverted by `c270892` and `4ae2660`). 19 files still carry them.
Delete on contact; the diagram itself belongs in a PNG (§8).

---

## 7. Compare — **NEW**, replaces `compare-box` / `compare-card`

```html
<div class="compare">
  <div class="compare__col compare__col--old">
    <div class="compare__label">แบบเดิม</div>
    <pre><code>docker run -p 8080:80 myapp</code></pre>
  </div>
  <div class="compare__col compare__col--new">
    <div class="compare__label">แบบใหม่</div>
    <pre><code>docker compose up -d</code></pre>
  </div>
</div>
```

```css
.compare { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin: 2rem 0; }
.compare__col { border-radius: var(--radius); padding: 1.25rem; background: var(--white);
                border: 1px solid rgba(0,0,0,0.06); }
.compare__col--old { border-left: 3px solid var(--red); }
.compare__col--new { border-left: 3px solid var(--green); }
.compare__label { font-size: 0.75rem; font-weight: 700; text-transform: uppercase;
                  letter-spacing: 0.08em; color: var(--slate-light); margin-bottom: 0.6rem; }
@media (max-width: 600px) { .compare { grid-template-columns: 1fr; } }
```

---

## 8. Figure — LIVE, the only sanctioned way to show a diagram

47 uses today: 38 in the 20 AI Transformation posts (19 figures × 2 language tracks), 8 on the
four `books/` detail pages (each jacket face), and 1 `.figure--qr`.

```html
<figure class="figure">
  <img class="figure__img" src="../images/openclaw-memory-arch.png"
       alt="OpenClaw memory architecture — session store, vector index, and long-term notes"
       width="2750" height="1375" loading="lazy" decoding="async">
  <figcaption class="figure__caption">สถาปัตยกรรม memory ของ OpenClaw</figcaption>
</figure>
```

`width`/`height` are the **source** pixel size — `openclaw-memory-arch.png` really is 2750×1375.
Writing a smaller display size there is what INV-33 catches: a `max-width` without `height: auto`
keeps the height attribute while the width shrinks, and the diagram renders squeezed.

```css
.figure { margin: 2.5rem 0; }
.figure__img { width: 100%; height: auto; display: block;
               border-radius: var(--radius); border: 1px solid rgba(0,0,0,0.06); }
.figure__caption { font-size: 0.85rem; color: var(--slate-light);
                   text-align: center; margin-top: 0.75rem; }
```

### 8b. The series-figure form — a `.figure` wrapped in a link

The AI Transformation figures add exactly one thing: an `<a>` around the `<img>` pointing at the
same PNG, so a reader on a phone can open the full-resolution drawing. No new class.

```html
<figure class="figure">
  <a href="../images/ai-transformation-fig-06-ai-data-factory.png">
    <img class="figure__img" src="../images/ai-transformation-fig-06-ai-data-factory.png"
         alt="แผนภาพหกช่องบริการของโรงงาน: Data products, Context services, Model services, Evaluation, Tool registry, Observability วางเหนือแถบสีเข้ม SHARED ASSURANCE"
         width="1400" height="700" loading="lazy" decoding="async">
  </a>
  <figcaption class="figure__caption">รูปที่ 6 · หกบริการของโรงงาน AI และข้อมูล — ชิ้นส่วนที่ใช้ซ้ำได้ทำให้รอบการเรียนรู้ที่ปลอดภัยรอบถัดไปสั้นลง</figcaption>
</figure>
```

Measured facts about that set, so a 20th figure matches the 19:

- **Filename**: `images/ai-transformation-fig-NN-<slug>.png`, zero-padded ordinal.
- **Size**: all 19 are **1400px wide**; heights are 840 (×11), 1000 (×5), 700 (×2), 560 (×1).
  Average 44 KB, largest 58 KB — an order of magnitude under the 200 KB cover budget, because they
  are flat art with a small palette.
- **Drawn, never hand-authored**: `scripts/make_figure.py` emits them, in the token palette
  (`CORAL = (194, 65, 12)` at `make_figure.py:99`, plus blue/green/gold/gray), with tints at
  `TINT_A = {"blue": 0.12, "green": 0.15, "gold": 0.30, "coral": 0.14, "gray": 0.25}`.
  Coral on that 14% coral wash measures **4.21:1** — fine for a 3px outline or a heading-size
  label, not for small type. See `tokens.md` §4.
- **Both tracks carry the figure**, so `alt` and `<figcaption>` are duplicated in Thai and English.
  The `alt` is a real description of what the drawing shows, not the caption repeated.

One modifier exists: `.figure--qr` (books/one-day-of-light.html `#event`) — a small flat-art QR
figure. It doubles the selector (`.figure.figure--qr`) so the detail pages' 800px cover-jacket
rule (`.figure { flex-basis: 240px }`) cannot inflate it, and swaps the cover shadow for a 1px
`#e2e8f0` border. The QR asset itself is regenerated from the decoded poster URL (round-trip
verified), PNG, 884 bytes.

**Diagrams are PNGs.** 25 PNGs live in `images/`: the 19 series figures, 5 older diagrams
(`*-arch.png`, `*-flow.png`, `*-levels.png`, 123–235 KB) and the QR. PNG is correct here precisely
because diagrams are flat colour and text — that is the one case where PNG beats JPG. Photographic
and drawn *covers* are JPG.

Never rebuild a diagram out of divs. This repo tried twice and reverted twice.

---

## 9. References — the sourced block that closes every AI Transformation post

40 blocks: one per language track in each of the 20 posts. It exists because that series makes
claims about law, standards and field evidence, and each claim has to say **what kind** of source
carries it and **which** sentence it supports.

```html
<section class="references" aria-labelledby="th-references">
  <h2 id="th-references">อ้างอิง</h2>
  <p class="references__note">ตรวจสอบทุกแหล่งเมื่อ 5 กันยายน 2026 (เวลาประเทศไทย) · ป้ายหลักฐานสี่แบบ:
    <strong>Law</strong> ตัวบทกฎหมายหรือประกาศทางการ · <strong>Standard</strong> มาตรฐานหรือกรอบทางการที่เผยแพร่แล้ว ·
    <strong>Study</strong> งานวิจัยหรือสัญญาณภาคสนาม · <strong>Synthesis</strong> การสังเคราะห์ของผู้เขียนหรือแหล่งที่ไม่ใช่งานวิจัย</p>
  <ol class="references__list">
    <li id="th-ref-2"><span class="ref-tag ref-tag--standard">Standard</span>
      National Institute of Standards and Technology.
      <cite>AI Risk Management Framework (AI RMF 1.0)</cite> — เผยแพร่ 26 มกราคม 2023.
      <a href="https://www.nist.gov/itl/ai-risk-management-framework">nist.gov</a> — เข้าถึง 2026-09-05.
      <span class="ref-supports">รองรับ: สี่ฟังก์ชัน Govern, Map, Measure, Manage …</span></li>
  </ol>
</section>
```

```css
.references { margin-top: 3rem; padding-top: 2rem; border-top: 1px solid #e2e8f0; }
.references__note { font-size: 0.85rem; color: var(--slate-light); margin-bottom: 1rem; }
.references__list { padding-left: 1.4rem; font-size: 0.9rem; line-height: 1.75; }
.references__list li { margin-bottom: 0.7rem; }
.ref-tag { display: inline-block; font-size: 0.7rem; font-weight: 700;
           letter-spacing: 0.06em; text-transform: uppercase; padding: 0.1rem 0.5rem;
           border-radius: 50px; margin-right: 0.4rem; vertical-align: 0.05em;
           background: rgba(34,98,153,0.1); color: var(--blue-dark); }
.ref-tag--law       { background: rgba(239,68,68,0.12);   color: #991b1b; }
.ref-tag--synthesis { background: rgba(196,164,108,0.22); color: var(--gold-dark); }
.ref-supports { display: block; color: var(--slate-light); font-size: 0.85rem; }
```

**The four evidence labels, and what each one promises.** The tag is a claim about the *kind* of
authority, not about how much you should trust it:

| Modifier | Label | Means |
|---|---|---|
| `.ref-tag--law` | Law | a statute, regulation or official notice — the binding floor |
| `.ref-tag--standard` | Standard | a published formal standard or framework (NIST AI RMF, ISO) |
| `.ref-tag--study` | Study | research, or a measured field signal |
| `.ref-tag--synthesis` | Synthesis | the author's own synthesis, or a non-research source |

Counts today: `--standard` 92, `--synthesis` 78, `--study` 66, `--law` 30 — 266 tags in all,
matching 266 `.ref-supports`. Every reference carries exactly one tag and exactly one supports
line.

`.ref-supports` is the other half of the contract: it names **which sentences, figures and tables**
in the article that source carries. That is what makes a claim checkable without reading the whole
piece, and it is why the block is `<section>` with `aria-labelledby` rather than a bare `<div>`.

Three things to know before you copy this:

- **Only two of the four modifiers are styled.** `--law` and `--synthesis` have rules; `--standard`
  and `--study` have none in any of the 20 files and fall through to the base `.ref-tag` blue. That
  is a real gap, not a subtlety — 158 of the 266 tags render identically. Adding the two missing
  rules is a safe, self-contained improvement.
- **The heading id is not namespaced.** All 20 posts write `<h2 id="references">` in *both* tracks,
  which is a duplicate id per document (40 occurrences of the same id across 20 files). The snippet
  above shows the corrected `th-`/`en-` form — use that for anything new, and prefer it if you are
  regenerating the series (§3).
- **The tag text is monolingual English** (`Law`, `Standard`, `Study`, `Synthesis`) inside both
  tracks; the `references__note` glossary explains them in the track's own language. Keep it that
  way — the tag is a label, not prose.

---

## 10. Code

Every post uses plain `<pre>` — 48 of the 76 carry code at all, and `class="code-block"` is at
**0 occurrences sitewide** since `662e966` converted the last 10 island files. New work uses
`<pre><code>`, and wraps a wide block in a `.table-wrapper` (§3).

```css
.post-body pre {
  background: var(--code-bg); color: #e2e8f0;
  border-radius: var(--radius); padding: 1.25rem 1.5rem;
  overflow-x: auto; margin: 1.5rem 0;
  font-family: var(--mono); font-size: 0.85rem; line-height: 1.7;
}
.post-body code {
  font-family: var(--mono);
  background: rgba(34,98,153,0.08); color: var(--blue-dark);
  padding: 0.15rem 0.4rem; border-radius: var(--radius-sm); font-size: 0.9em;
}
```

**The selector is `.post-body code`, not `.post-body p > code`** — the child-combinator form this
file used to show is at 0 occurrences; every shipped post uses the descendant form, so inline code
inside a `<li>` or a `<td>` gets the tint too. 60 files carry `rgba(34,98,153,0.08)`; 5 still carry
a pre-re-key tint (3 × violet `139,92,246`, 1 emerald, 1 cyan) — normalise on contact.

**Box-drawing characters inside `<pre>` are legitimate** when they reproduce real terminal output —
for example the `subagents list` table in `blog/openclaw-agent-teams.html`. Preserve them. The rule
against ASCII art applies to *diagrams built out of characters in prose*, not to captured CLI
output.

---

## 11. CSS file organisation

Keep the existing comment convention — now 87 files, 726 uses:

```css
/* ── SECTION ── */
```

Order inside every `<style>` block, matching the house files:

1. `*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }`
2. `:root { … }` (canonical 29-token block, byte-identical across files; product brand tokens
   after it. The one exception is `--coral`, which the 20 AI Transformation posts splice **into**
   the brand line between `--gold-dark` and `--cloud` — see `tokens.md` §4a)
3. `html { scroll-behavior: smooth; }` and `body { … }`
4. `.skip-link`, `.lang-switch-box` / `.lang-switch`, `.l-th` / `.l-en`
5. `.blog-nav` …
6. `.post-hero` …
7. `.post-body` and its typography, then `.post-toc` and `.table-wrapper`
8. components (`.callout`, `.compare`, `.figure`, `.card`, `.references`)
9. `.post-nav` / `.series-nav` (+ `--grouped`) / `.blog-footer`
10. `:focus-visible` + `prefers-reduced-motion`
11. `@media (max-width: 768px)` then `@media (max-width: 600px)`

The language block sits at 4 rather than at the end for a reason: `.l-en { display: none }` is the
default state of half the document, and burying it under 600 lines of component CSS is how a later
edit accidentally overrides it. `display: revert` — never `block` — because `.l-en` is used on
`<div>`, `<details>` and `<span>` alike.
