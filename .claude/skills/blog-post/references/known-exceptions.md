# Known exceptions and standing drift — things that look broken and are not

Read this before "fixing" anything you notice while editing a post. Every item below was
re-checked on **2026-08-10 against `7867c00`**, and each is cross-referenced to the
`check_site.py` invariant that baselines it — if an item here has no live violation, it is
stale and should be deleted, not left as a standing excuse. Inventing links to make these
symmetrical will corrupt the one navigation chain that currently verifies perfectly.

> **Standing rule:** any change that invalidates a number in a skill file must update that
> number in the same commit. That includes this file's drift tables and the `BASELINE` set
> in `assets/verify-wiring.py`.

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

**`deployment-hosting.html` has two `<h1>`** — the hero title and a near duplicate inside
the article body. It is the only post with `h1 != 1` (`check_site.py` INV-11 prints the
current line numbers; they have moved twice, so this file no longer quotes them).
Demoting the second to `<h2>` is a safe one-line fix if you are already in that file.

**`images/` has 9 orphans** left over from a prior template:
`Opic02.jpg bg.jpg overlay.png pic01.jpg pic02.jpg pic03.jpg pictop.png xpic01.jpg xpic03.jpg`.
Nothing references them. Deleting them is safe but unrelated to writing a post.

## Standing drift — real inconsistencies, not blockers

These are worth paying down deliberately, in a dedicated commit, never as a side effect
of adding a post. A new post should adopt the **plurality** form of each so the drift
does not grow.

| Thing | Variants on disk (37 posts) | Use in new posts | Guard |
|---|---|---|---|
| Footer container | `blog-footer` ×23, `footer` ×7, `post-footer` ×3, bare `<footer>` ×4 | `<footer class="blog-footer">` | INV-16 |
| Copyright | `© 2025` ×25, `© 2026` ×8 (5 posts write it as the `&copy;` entity), `© 2024` ×1 (openclaw-integrations.html), none ×3 (claude-code-architecture, idle-self-improvement, openclaw-migration) | `© 2026` | INV-15 |
| `<meta name="description">` | missing in 6 posts (idle-self-improvement + 5 numbered OpenClaw) | always write one | INV-14 |
| `.series-nav` `<h3>` | 6 say `📚 OpenClaw for Organizations 2026`, `openclaw-integrations.html` says `OpenClaw for Organizations 2026 — Series Navigation` | the emoji form | INV-03b |
| `.post-nav` container | `<div>` ×21, `<nav>` ×4 | `<div class="post-nav">` | INV-04c |
| `.post-nav__dir` wording | `← Previous`/`Next →` everywhere except `claude-code-architecture.html`'s `Related`/`See also` | the arrows | INV-04d |
| OpenClaw badge markup | `.series-badge` ×4, `.series-info` ×1, bare `<p>` ×1, `<strong>` ×1 | `.series-badge` | INV-20b |
| `post-hero__series` text | `DevOps & Vibe Coding 2026` ×21, `DevOps &amp; Vibe Coding 2026` ×2, `AI Developer Tools 2026` ×1 | literal `&` | — |

**Note on the copyright row:** `check_site.py`'s `RE_COPYRIGHT` matches only a literal `©`,
so INV-15 reports the 5 `&copy;` posts in its "no © line" bucket. The distribution above
was computed with `(?:©|&copy;)\s*(\d{4})` and is the true one. Do not "reconcile" the two
by editing this table down to what the linter prints.

**The `:root` row is gone: it is no longer drift.** `6670480` landed the canonical
24-token block in every post, and INV-22 PASSes. Always keep it, byte-identical.

Eight `.post-nav__title` labels no longer match their target's `card__title`. Worst case:
`devops-security.html` calls `linux-command-line.html` "Linux & Shell Essentials" when its
card says "Linux Command Line". Both linters list all eight at warn level and they agree
one-for-one (`verify-wiring.py` warns; `check_site.py` INV-10 baselines the same 8 pairs).

`verify-wiring.py` was **blind to this entire class of drift** until 2026-08-10: it
matched `<h2 class="card__title">` against cards that Task 11 had made `<h4>`, so it read
0 titles and printed CLEAN. It now matches any `h1`–`h6` and hard-fails a card whose title
heading it cannot find at all. If the two tools ever disagree on this list, one of them has
gone blind again — do not assume the quieter one is right.

Fix the two adjacent to any post you insert; fixing all eight is a separate commit.

## Fixed since this file was written — do not re-report

**`blog/index.html`'s dead mobile menu is gone.** It used to render a
`<button class="nav__hamburger">` with no handler in a file with zero `<script>`. Task 9
(`ad3c42d`, `c25c682`) replaced it with the pure-CSS `.nav__toggle` checkbox +
`.nav__burger` label pattern now shared by all 4 listing pages. `check_site.py` INV-12
verifies every toggle is wired and has **no baseline entry**, so a regression will fail
the build. `grep -rn 'nav__hamburger' --include='*.html' --exclude-dir=.claude .` returns
`index.html` only, and that one is genuinely wired to `script.js`.

(One mobile-nav defect does survive, in a file this skill rarely touches:
`blog/obsidian-ai-jarvis.html` hides `.nav__links` at ≤768px with no toggle at all. See
a11y-perf R2.)

## Still genuinely broken and worth telling the user about

**`deployment-hosting.html` has two `<h1>`** — see above (INV-11).

**Two covers are double-booked** — see above (INV-07a). The fix is two new images.

**`data-reveal` does nothing inside `blog/`.** `CLAUDE.md` says to add `data-reveal` for
scroll-triggered fade-in, but the handler lives in `script.js`, which only `index.html`
loads. `grep -o 'data-reveal' blog/index.html | wc -l` returns 0, and `check_site.py`
INV-21b PASSes only because nobody has added one. Do not add `data-reveal` attributes to
blog pages expecting animation.
