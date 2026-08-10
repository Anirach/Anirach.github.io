# Component vocabulary — real markup

Every snippet here is copied from a real file in this repo, with the file and line noted. Copy
these; do not paraphrase them. Where a snippet is marked **NEW**, it is the proposed §4 primitive
that replaces a sprawl of one-off names — use it for new work, and migrate old names only when you
are already editing that file.

---

## 1. Chrome — `.blog-nav`

Markup, `blog/api-request-lifecycle.html:180-185`:

```html
<nav class="blog-nav">
  <div class="blog-nav__inner">
    <a href="./" class="blog-nav__back">‹ Blog</a>
    <div class="blog-nav__title">API Request Lifecycle</div>
  </div>
</nav>
```

CSS — this is the **fixed** variant (10 of 26 house files have it; the other 14 are missing the
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
.blog-nav__back:hover { color: var(--blue-dark); }   /* repo hard-codes #4f46e5 here — tokenise it */
.blog-nav__title {
  font-size: 0.85rem; font-weight: 600; color: var(--navy);
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 50%;
}
```

The glassy `rgba(248,250,252,0.85)` + `blur(20px)` `.blog-nav` block is byte-identical in 24 of the
26 house files and is the house look — do not change it. `openclaw-memory-architecture.html` and
`vibe-coding-devops-process.html` are minified forks (`.9` alpha, `blur(14px)`/`blur(16px)`,
`z-index:50`); `blog/index.html:32` uses `0.88` on `.nav`. 34 files use `backdrop-filter` somewhere.

`.nav` (used by `index.html`, `blog/index.html` and the island posts) is a **different component
with the same name in three places**. That collision is the main blocker on ever sharing a
stylesheet — see SKILL.md anti-pattern 2.

---

## 2. Header — `.post-hero`

Markup, `blog/api-request-lifecycle.html:187-201`, plus the image attributes that should be added:

```html
<header class="post-hero">
  <div class="post-hero__tags">
    <span class="post-hero__tag">API</span>
    <span class="post-hero__tag">HTTP</span>
    <span class="post-hero__tag">Backend</span>
  </div>
  <h1 class="post-hero__title">API Request Lifecycle — เมื่อกด Send เกิดอะไรขึ้นบ้าง?</h1>
  <div class="post-hero__meta">
    <span>By <strong>Anirach Mingkhwan</strong></span>
    <span class="post-hero__series">DevOps &amp; Vibe Coding 2026</span>
  </div>
  <div class="post-hero__cover">
    <img src="../images/api-lifecycle-cover.jpg" alt="API Request Lifecycle — cute dog illustration"
         width="1600" height="900" loading="eager" fetchpriority="high" decoding="async">
  </div>
</header>
```

```css
.post-hero {
  padding: 8rem 2rem 3rem;
  background: linear-gradient(135deg, #e8f0fe 0%, #ddd6fe 50%, #c7d2fe 100%);
  text-align: center;
}
.post-hero__tags { display: flex; gap: 0.5rem; justify-content: center; margin-bottom: 1.25rem; }
.post-hero__tag {
  font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em;
  color: var(--blue); background: rgba(99,102,241,0.1);
  padding: 0.3rem 0.75rem; border-radius: 20px;      /* pill — the one place 20px is right */
}
.post-hero__title {
  font-size: clamp(1.8rem, 5vw, 3rem); font-weight: 800; color: var(--navy);
  line-height: 1.2; margin-bottom: 1rem;
  max-width: var(--measure); margin-left: auto; margin-right: auto;
  text-wrap: balance;                                 /* add — currently 0 files */
}
.post-hero__meta {
  font-size: 0.85rem; color: var(--slate-light);
  display: flex; align-items: center; justify-content: center; gap: 1.5rem;
}
.post-hero__series { font-weight: 600; color: var(--blue); }
.post-hero__cover {
  max-width: 380px; margin: 2.5rem auto 0;   /* 380px is the incumbent (13 of 25 house rules);
                                                api-request-lifecycle itself has 480px — retire
                                                420/480/520/560 on contact */
  border-radius: var(--radius-lg); overflow: hidden;
  box-shadow: 0 20px 60px rgba(99,102,241,0.15);
  aspect-ratio: 16 / 9;                               /* add — kills CLS; matches the 1600×900 img */
}
.post-hero__cover img { width: 100%; height: 100%; object-fit: cover; display: block; }
```

`padding-top: 8rem` clears the 56px fixed nav. Pick the gradient from SKILL.md §5, never invent one.

---

## 3. Body — `.post-body`

```css
.post-body { max-width: var(--measure); margin: 0 auto; padding: 3rem 2rem 6rem; }
.post-body h2 {
  font-size: 1.6rem; font-weight: 800; color: var(--navy);
  margin: 3rem 0 1rem; padding-bottom: 0.5rem;
  border-bottom: 2px solid rgba(99,102,241,0.15);
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
(37 cards in `blog/index.html`, `card__tag` ×130 sitewide) — the model for all future component
naming. Reproduced verbatim from disk, including the inline placeholder gradient.

```html
<a href="openclaw-migration.html" class="card">
  <div class="card__image">
    <img src="../images/openclaw-migration-cover.jpg" alt="OpenClaw Migration"
         width="1600" height="900" loading="lazy" decoding="async">
  </div>
  <div class="card__body">
    <div class="card__tags">
      <span class="card__tag">OpenClaw</span>
      <span class="card__tag">Migration</span>
      <span class="card__tag">DevOps</span>
    </div>
    <h4 class="card__title">Self-Transferring OpenClaw Bot — ย้าย AI Agent ข้ามเครื่องแบบไม่พลาด 🚚</h4>
    <p class="card__excerpt">คู่มือย้าย bot จาก VPS Ubuntu ไป Mac Studio แบบ step-by-step</p>
    <div class="card__footer">
      <div class="card__author">
        <img src="../images/profile.jpg" alt="Anirach" class="card__avatar"
             width="64" height="64" loading="lazy" decoding="async">
        <div><div class="card__author-name">Anirach Mingkhwan</div></div>
      </div>
      <span class="card__read">Read →</span>
    </div>
  </div>
</a>
```

**The title is `<h4>`, not `<h2>`.** Task 11 (`635eb94`) gave `blog/index.html` a real ladder —
`h1` page title → `h2` ×3 `.category__title` → `h3` ×2 `.series-title` → `h4` ×37 `.card__title`.
Writing `<h2 class="card__title">` re-collides the card with the category band. Any tool that
greps for card titles must use `<h[1-6] class="card__title">`.

One fix still to make while you are in there:

- The live markup carries an **inline** `style="background: linear-gradient(...)"` on the cover
  `<img>` — a load placeholder. It is one of the 77 gradients. Move it to a class or drop it.

(The cover itself is fine now: `openclaw-migration-cover.jpg`, 186 KB, with
`width`/`height`/`loading`/`decoding` — `ec2827b` and `e8da9da` handled both.)

`.card` in `blog/index.html` means "blog listing card"; the 4 LISTING pages share the vocabulary
(`card` ×56, `card__title` ×50 sitewide). The same bare name is also used generically inside ~20
posts. Do not add a 19th `*-card` name; use `.card--<modifier>`.

---

## 5. Post footer navigation — three mutually exclusive patterns

Pick the one that matches the post's series. Never mix two in one file.

**A. `.post-nav`** — DevOps posts, relative `.html` links.
`blog/api-request-lifecycle.html`:

```css
.post-nav {
  max-width: var(--measure); margin: 0 auto; padding: 0 2rem 3rem;
  display: flex; gap: 1.5rem; flex-wrap: wrap;
}
```

This flex form is the incumbent — 22 of the 25 house files that declare `.post-nav` use it; the
three grid variants (the two minified files plus `deployment-hosting.html`) are drift, not the
pattern.

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

**B. `.series-nav`** — the 7 numbered OpenClaw posts, absolute extensionless links.
`blog/openclaw-101.html`:

```html
<div class="series-nav">
  <h3>OpenClaw for Organizations 2026</h3>
  <div class="series-links">
    <span class="current">#1 OpenClaw 101</span>
    <a href="/blog/openclaw-agent-teams">#2 Agent Teams</a>
    <a href="/blog/openclaw-memory">#3 Memory &amp; Knowledge</a>
    <a href="/blog/openclaw-security">#4 Security &amp; Access</a>
    <a href="/blog/openclaw-integrations">#5 Integrations</a>
    <a href="/blog/openclaw-skills">#6 Skills &amp; Automation</a>
    <a href="/blog/openclaw-production">#7 Production &amp; Scale</a>
  </div>
</div>
```

The extensionless `/blog/openclaw-*` links are correct — GitHub Pages resolves them, and all 7
targets exist. `/about`, `/projects`, `/research`, `/contact` and `/teaching` do **not** exist;
strip those links when you see them (SKILL.md anti-pattern 10).

**C. none** — `beyond-plugins`, `git-branching`, `idle-self-improvement`, `obsidian-ai-jarvis`,
`openclaw-migration`. Leave as-is unless the user asks for navigation.

Then the footer — the house footer is the dark navy bar, and all 23 house posts that have one
include the copyright span:

```html
<footer class="blog-footer">
  <a href="./">← Back to Blog</a>
  <span>© 2025 Anirach Mingkhwan — Associate Professor, KMUTNB</span>
</footer>
```

```css
.blog-footer { background: var(--navy); padding: 2rem 0; text-align: center; }
.blog-footer a { color: var(--blue-light); text-decoration: none; font-weight: 600; font-size: 0.9rem; }
.blog-footer span { color: var(--gray); font-size: 0.8rem; display: block; margin-top: 0.4rem; }
```

---

## 6. Callout — **NEW**, replaces the 14 box names

Replaces `diagram-box` (39), `arch-box` (27), `highlight-box` (15), `info-note` (10),
`compare-box` (4), `series-info` (4), `warning-box` (3), `alert` (3), `tip` (2), `insight-box` (2),
`analogy-box` (2), `case-study-box` (1), `danger-box` (1), `success-box` (1).

```html
<aside class="callout callout--warn">
  <div class="callout__title">ข้อควรระวัง</div>
  <p>Rate limit จะ reset ทุก 60 วินาที ไม่ใช่ทุกนาทีตามนาฬิกา</p>
</aside>
```

```css
.callout {
  border-left: 3px solid var(--blue);
  background: rgba(99,102,241,0.06);
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

Four modifiers, drawn from the six status tokens. If you need a fifth mood, you almost certainly
need one of these four.

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

## 8. Figure — **NEW**, the only sanctioned way to show a diagram

```html
<figure class="figure">
  <img class="figure__img" src="../images/openclaw-memory-arch.png"
       alt="OpenClaw memory architecture — session store, vector index, and long-term notes"
       width="1600" height="900" loading="lazy" decoding="async">
  <figcaption class="figure__caption">สถาปัตยกรรม memory ของ OpenClaw</figcaption>
</figure>
```

```css
.figure { margin: 2.5rem 0; }
.figure__img { width: 100%; height: auto; display: block;
               border-radius: var(--radius); border: 1px solid rgba(0,0,0,0.06); }
.figure__caption { font-size: 0.85rem; color: var(--slate-light);
                   text-align: center; margin-top: 0.75rem; }
```

**Diagrams are PNGs.** PNG is correct here precisely because diagrams are flat colour and text —
that is the one case where PNG beats JPG. Photographic and AI-generated *covers* are JPG.

Never rebuild a diagram out of divs. This repo tried twice and reverted twice.

---

## 9. Code

House uses plain `<pre>` — 26 of 26. Island uses `<div class="code-block">` — 10 of 10. Zero files
use both. New work uses `<pre><code>`.

```css
.post-body pre {
  background: var(--code-bg); color: #e2e8f0;
  border-radius: var(--radius); padding: 1.25rem 1.5rem;
  overflow-x: auto; margin: 1.5rem 0;
  font-family: var(--mono); font-size: 0.85rem; line-height: 1.7;
}
.post-body code { font-family: var(--mono); }
.post-body p > code {
  background: rgba(99,102,241,0.1); color: var(--blue-dark);
  padding: 0.15rem 0.4rem; border-radius: var(--radius-sm); font-size: 0.9em;
}
```

**Box-drawing characters inside `<pre>` or `.code-block` are legitimate** when they reproduce real
terminal output — for example `blog/openclaw-agent-teams.html:871-880`, a `subagents list` table
inside a `.code-block`. Preserve them. The rule against ASCII art applies to *diagrams built out of
characters in prose*, not to captured CLI output.

---

## 10. CSS file organisation

Keep the existing comment convention — 13 files, 66 uses:

```css
/* ── SECTION ── */
```

Order inside every `<style>` block, matching the house files:

1. `*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }`
2. `:root { … }` (canonical block, byte-identical across files; brand tokens after)
3. `html { scroll-behavior: smooth; }` and `body { … }`
4. `.blog-nav` …
5. `.post-hero` …
6. `.post-body` and its typography
7. components (`.callout`, `.compare`, `.figure`, `.card`)
8. `.post-nav` / `.series-nav` / `.blog-footer`
9. `:focus-visible` + `prefers-reduced-motion`
10. `@media (max-width: 768px)` then `@media (max-width: 600px)`
