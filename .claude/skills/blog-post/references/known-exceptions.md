# Known exceptions and standing drift — things that look broken and are not

Read this before "fixing" anything you notice while editing a post. Every item below
was checked on 2026-08-10 against a clean `main`. Inventing links to make these
symmetrical will corrupt the one navigation chain that currently verifies perfectly.

## Deliberate exceptions — leave alone

**Two categories intentionally carry 0 cards.** Since Task 11 (2026-08-10),
`blog/index.html` groups posts into three `.category` bands: `#cat-technology` (all 37
existing posts, unchanged), `#cat-academic` (Academic & Philosophy) and `#cat-lifestyle`
(Lifestyle). The latter two render a single quiet `<p class="category__note">` line
("...— เร็ว ๆ นี้") instead of a `.blog-grid`, and their `.category__count` reads
`"First posts coming soon"` rather than a number — a fake `"0 articles"` count would
read as a bug. This is by design, not missing content; do not add placeholder cards to
fill them. `check_site.py`'s INV-02d treats a 0-card category with that exact label as
clean, and flags either a stale number left behind or a numeric "0" as a violation. See
`.claude/skills/blog-post/SKILL.md` Step 1 for how the first post in either category
should be added.

**`git-branching.html` is the chain head and has no nav at all.**
It is the oldest DevOps post. `cicd-pipeline.html:607` points `prev → git-branching.html`,
which cannot reciprocate. Adding a `.post-nav` to `git-branching.html` would be a
reasonable improvement, but it is not a bug and it is not your job while adding a post.

**Two `#series-openclaw` cards wear DevOps chrome.**
- `claude-code-architecture.html` — has a `.post-nav`-shaped block using a third
  direction vocabulary, `Related` / `See also` (lines 602-611), pointing at
  `openclaw-101.html` and `web-architecture.html`. It belongs to no chain.
- `openclaw-memory-architecture.html:224` — grafts `prev → deployment-hosting.html`,
  which is also claimed as `prev` by `vibe-coding-devops-process.html`. So
  `deployment-hosting.html` has two inbound `prev` edges.

Both are unreachable from the chain walk, by design. `verify-wiring.py` allowlists them.

**Five posts have no nav block of any kind.**
`beyond-plugins.html`, `git-branching.html`, `idle-self-improvement.html`,
`obsidian-ai-jarvis.html`, `openclaw-migration.html`. They are standalone pieces, not
series entries. The nav partition is exactly 7 series-nav + 25 post-nav + 5 none = 37.

**Two covers are shared by two posts each**, because no dedicated asset was ever drawn:
- `images/github-actions-cover.jpg` → `github-actions.html` + `vibe-coding-devops-process.html`
- `images/monitoring-cover.jpg` → `monitoring-observability.html` + `openclaw-memory-architecture.html`

Commit 3c01503 deleted duplicate hero `<img>` tags in 4 OpenClaw posts but never touched
these two. The right fix is to generate two new PNGs, not to re-point a card. Until then
they are baselined.

**`deployment-hosting.html` has two `<h1>`** — the hero title at line 164 and a near
duplicate at line 176 inside the article body. It is the only post with `h1 != 1`.
Deleting line 176 is a safe one-line fix if you are already in that file.

**`images/` has 9 orphans** left over from a prior template:
`Opic02.jpg bg.jpg overlay.png pic01.jpg pic02.jpg pic03.jpg pictop.png xpic01.jpg xpic03.jpg`.
Nothing references them. Deleting them is safe but unrelated to writing a post.

## Standing drift — real inconsistencies, not blockers

These are worth paying down deliberately, in a dedicated commit, never as a side effect
of adding a post. A new post should adopt the **plurality** form of each so the drift
does not grow.

| Thing | Variants on disk | Use in new posts |
|---|---|---|
| Footer container | `blog-footer` ×23, `footer` ×7, `post-footer` ×3, bare `<footer>` ×4 | `<footer class="blog-footer">` |
| Copyright | `© 2025` ×25, `© 2026` ×8 (4 of these write it as the `&copy;` entity), `© 2024` ×1 (openclaw-integrations.html), none ×3 (claude-code-architecture, idle-self-improvement, openclaw-migration) | `© 2026` |
| `<meta name="description">` | missing in 6 posts (idle-self-improvement + 5 OpenClaw) | always write one |
| `.series-nav` `<h3>` | 6 say `📚 OpenClaw for Organizations 2026`, `openclaw-integrations.html` says `OpenClaw for Organizations 2026 — Series Navigation` | the emoji form |
| `.post-nav` container | `<div>` ×21, `<nav>` ×4 | `<div class="post-nav">` |
| `:root` block | absent in 10 posts (7 OpenClaw + beyond-plugins, idle-self-improvement, openclaw-migration) | always include one |
| `post-hero__series` text | `DevOps & Vibe Coding 2026` ×21, `DevOps &amp; Vibe Coding 2026` ×2, `AI Developer Tools 2026` ×1 | literal `&` |

Eight `.post-nav__title` labels no longer match their target's `card__title`. Worst case:
`devops-security.html` calls `linux-command-line.html` "Linux & Shell Essentials" when
its card says "Linux Command Line". `verify-wiring.py` lists all eight at warn level.
Fix the two adjacent to any post you insert; fixing all eight is a separate commit.

## Two things that are genuinely broken and worth telling the user about

**`blog/index.html` has a dead mobile menu.** It renders `.nav__hamburger` (4 references)
and hides `.nav__links` at `@media (max-width: 768px)` (line 173), but the file contains
zero `<script>`. It is the only page in the repo with this defect — `index.html` is the
only file that loads `script.js`. On a phone the blog index has no navigation at all.
Fix by either deleting the button plus that media rule, or inlining the six lines from
`script.js` that toggle `#hamburger` / `#nav` / `#navLinks`.

**`data-reveal` does nothing inside `blog/`.** `CLAUDE.md` says to add `data-reveal` for
scroll-triggered fade-in, but the handler lives in `script.js`, which only `index.html`
loads. `grep -o 'data-reveal' blog/index.html | wc -l` returns 0. Do not add
`data-reveal` attributes to blog pages expecting animation.
