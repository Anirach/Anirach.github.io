# Adding, renaming, or removing a post

Open this before touching `blog/`. Every step here exists because the linter catches its omission —
run `python3 .claude/skills/site-check/scripts/check_site.py` after each step, not just at the end.

## Pick the right template

Copy a **DevOps post that already has `<nav class="blog-nav">` + `.post-nav`** — for example
`blog/frontend-performance.html`. 26 of 37 posts carry that header and all 26 use exactly one link,
`href="./"`; it is the only uniform structure in the repo.

Do **not** copy one of the 7 OpenClaw series posts. They are the un-templated corner: 10 posts in
the repo have no `href="./"` anywhere and all 7 series posts are among them; they account for the 14
broken links (INV-05), 5 of 6 missing meta descriptions (INV-14), 4 different ordinal-badge markups
(INV-20), and 7 of 10 posts with no `:root` (INV-22).

Minimum the copy must get right: `<html lang="th">` (all 37 posts are `th`; the two index pages are
`en` — INV-13), exactly one `<h1>` (INV-11), a `<meta name="description">` (INV-14), and a cover
image (INV-07c).

---

## Adding a DevOps post

### 1. Add the card at the TOP of `#series-devops`

`reversed(#series-devops card order)` **is** the prev/next chain — verified byte-identical over 24
nodes. `blog/index.html` is canonical; the per-post navs are derived. Newest post = first card =
chain tail.

Exact card shape (from `blog/index.html:578-600`; the anchor pattern
`<a href="…" class="card">` with that attribute order is what the counters and INV-01 match on):

```html
        <!-- Card: Your Title -->
      <a href="your-post.html" class="card">
        <div class="card__image">
          <img src="../images/your-cover.jpg" alt="Your Title" style="background: linear-gradient(135deg, #4f46e5, #7c3aed, #06b6d4);">
        </div>
        <div class="card__body">
          <div class="card__tags">
            <span class="card__tag">DevOps</span>
          </div>
          <h2 class="card__title">Your Title — Thai subtitle ⚡</h2>
          <p class="card__excerpt">Thai one-paragraph excerpt.</p>
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

### 2. Rewire exactly three things

Let `old_top` be the post that was first in `#series-devops` before you inserted
(`vibe-coding-devops-process.html` today — its next is `"./"`, marking it as the current tail).

1. `your-post.prev = old_top.html`
2. `old_top.next = your-post.html`  ← replaces its `href="./"`
3. `your-post.next = "./"`  ← the terminal moves to you

Nothing else changes. Never hand-author chain order; derive it from the card order.

Exact nav shape (from `blog/frontend-performance.html:1374-1383`):

```html
  <div class="post-nav">
    <a href="PREV.html" class="post-nav__link">
      <div class="post-nav__dir">← Previous</div>
      <div class="post-nav__title">PREV card title, HTML-escaped</div>
    </a>
    <a href="NEXT.html" class="post-nav__link" style="text-align:right;">
      <div class="post-nav__dir">Next →</div>
      <div class="post-nav__title">NEXT card title, HTML-escaped</div>
    </a>
  </div>
```

- `.post-nav__dir` must be exactly `← Previous` / `Next →` (INV-04d).
- `.post-nav__title` must equal the target's `.card__title` in `blog/index.html` (INV-10 — 8 posts
  are already stale here; copy, don't paraphrase). Use `&amp;` for `&` as the existing navs do.
- The `style="text-align:right;"` on the Next anchor is present in 3 files and absent in the rest;
  either is fine, but the linter's anchor regex must tolerate it.

### 3. Resync the counters

```bash
python3 .claude/skills/site-check/scripts/check_site.py --fix
```

Updates `blog/index.html:221` (total Articles) and `:573` (`#series-devops` count). Do not
hand-increment — that is how 33 drifted from the real 37.

---

## Adding an OpenClaw series post (an 8th chip)

This is a 9-file edit, not a 2-file edit.

1. Write `blog/openclaw-<slug>.html` with the strip from
   `.claude/skills/site-check/assets/series-nav.html`, its own entry as
   `<span class="current">#8 Your Label</span>`.
2. Add the new `<a href="/blog/openclaw-<slug>">#8 Your Label</a>` line to **all 7 existing** series
   posts, in the same position, with identical label text. INV-03 compares the full 7-label sequence
   in order across all files, so a typo in one file is a violation.
3. Add the ordinal badge. Numerically all 7 are correct today, but the markup is expressed 4 ways
   (`.series-badge` ×4, `.series-info` ×1, bare `<p>` ×1, `<strong>` ×1) and `openclaw-memory.html`
   writes `บทที่ 3` instead of `Post #3`. Use `.series-badge` with `Post #8`.
4. Add the card inside `<section class="series-section" id="series-openclaw">`.
5. Do **not** give the post a `.post-nav` as well — INV-08 enforces exclusivity (7 series-nav / 25
   post-nav / 5 no-nav = 37).
6. Fix the links you are about to copy: the series-post footers contain the 14 broken
   `/about`, `/projects`, `/research`, `/teaching`, `/contact` hrefs. Use `../index.html#about` etc.,
   as `blog/index.html:200-204` does.
7. `--fix` to resync `:221` and `:235`.

---

## Renaming a post

The filename appears in more places than you expect. Sweep all of them:

```bash
grep -rn 'old-slug' blog/ index.html
```

- the card href in `blog/index.html`
- the neighbours' `.post-nav` `href` (both the post that names it as `next` and the one that names
  it as `prev`)
- all 7 copies of the series strip, if it is an OpenClaw post — as `/blog/old-slug`, **without**
  `.html` (INV-09)
- any in-body cross-links

Rename the cover in `images/` to match only if the post follows the `<slug>-cover.*` convention — 14
of 37 deliberately do not (`iac-cover.jpg`, `auth-cover.jpg`, `sre-cover.jpg`, `cicd-cover.png`,
`linux-cli-cover.jpg`, …). If you do rename the image, update both the post body and the card, or
INV-07b goes red.

## Removing a post

1. Delete the file and its card.
2. Splice the chain: `prev_of_removed.next = next_of_removed`, `next_of_removed.prev =
   prev_of_removed`. If the removed post was the tail, restore `next="./"` on the new tail.
3. Delete its cover from `images/` unless another post shares it — `github-actions-cover.jpg` and
   `monitoring-cover.jpg` are each used by two posts today (INV-07a).
4. `--fix` the counters.
