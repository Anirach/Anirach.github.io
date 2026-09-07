# Adding, renaming, or removing a post

Open this before touching `blog/`. Every step here exists because the linter catches its omission —
run `python3 .claude/skills/site-check/scripts/check_site.py` after each step, not just at the end.

Re-measured **2026-09-06**: 76 posts in five series (20 AI Transformation, 10 Hermes, 13 OpenClaw,
24 DevOps, 9 Life), 77 files in `blog/`, 87 HTML files on disk, 86 enumerated.

## First: which series? One of them is generated

**AI Transformation posts are NOT written by hand.** `scripts/build_series.py` emits all 20 from
`scripts/series/ai-transformation.json` plus the per-post content sheets in `.bilingual/`
(gitignored scratch), lifting its skeleton from `blog/hermes-101.html` at run time. Adding a 21st
is a manifest row and four commands — jump to "Adding an AI Transformation post" below and **do not
open twenty files to edit twenty chip strips**. That is the exact miss INV-03c exists to catch.

The other four series are hand-edited, and the rest of this file is about them.

## Pick the right template

Copy a **DevOps post that already has `<nav class="blog-nav">` + `.post-nav`** — for example
`blog/frontend-performance.html`. **All 76 posts** carry that header now and all 76 use exactly one
link, `href="./"`.

Copying one of the 7 OpenClaw series posts is no longer the trap it was. Their whole backlog is
paid: the 14 broken links (INV-05, `b9fb125`), the 5 missing meta descriptions (INV-14), the 4
ordinal-badge markups (INV-20b, Phase 3), the missing `:root` blocks (INV-22, `6670480`), the
hand-rolled headers and footers (INV-29/INV-16, 2026-08-26). What still argues against them is
cost, not quality: their strip is a fixed literal duplicated seven times, so a post that joins that
series costs 7 extra file edits.

Minimum the copy must get right: `<html lang="th">` (all 76 posts are `th`; the 10 English pages
are the 6 nav-bearing index pages and the 4 `books/` detail pages — INV-13), exactly one `<h1>`
(INV-11), a `<meta name="description">` (INV-14/INV-27), a cover image (INV-07c) **and its 1200×630
share card** (INV-35), and **both language tracks** — every post carries the pure-CSS TH ⇄ EN
switch, so a Thai-only post is a defect. `python3 scripts/bilingualize.py --post <slug>` does the
mechanical conversion; `--fill <slug>` splices the translation in; `--verify <slug>` is the per-file
check to drive to OK. `--verify` is also the only check that can see a half-converted post while a
sweep is in flight — the sitewide linters see one tree and cannot tell.

---

## Adding a DevOps post

### 1. Add the card at the END of `#series-devops`

The `#series-devops` card order **is** the prev/next chain — direct since the 2026-09-07
reading-order redesign (it was reversed before that), verified byte-identical over 24 nodes.
`blog/index.html` is canonical; the per-post navs are derived. Newest post = LAST card = chain
tail = highest `.card__num` ordinal. The card shape also changed with the redesign — copy a
sibling row card from the live section (ordinal span, split EN/TH title, `.card__meta` with
`<time>`), or better, run `python3 scripts/reindex_blog.py` after adding the post and let it
place and number the card.

Exact card shape (grep `id="series-devops"` for the section — no line numbers, they move every
launch; the anchor pattern `<a href="…" class="card">` with that attribute order is what the
counters and INV-01 match on). The title is split into lang-correct EN/TH spans — the hidden
`.card__sep` keeps the concatenated text identical for `gen_feed.py` and INV-10 — and the card
carries no byline, tags, or "Read →" since the 2026-09-07 redesign. No trailing emoji in the
title (the post `<h1>` may keep its own).

```html
      <!-- Card: Your Title -->
      <a href="your-post.html" class="card">
        <span class="card__num">25</span>
        <div class="card__image">
          <img src="../images/your-cover.jpg" alt="" width="800" height="800" loading="lazy" decoding="async">
        </div>
        <div class="card__body">
          <h3 class="card__title"><span class="card__en">Your Title</span><span class="card__sep"> — </span><span class="card__th" lang="th">Thai subtitle</span></h3>
          <p class="card__excerpt"><span lang="th">Thai one-sentence excerpt.</span></p>
          <p class="card__meta"><time datetime="2026-09-07">7 Sep 2026</time> · 12 min read</p>
        </div>
      </a>
```

### 2. Rewire exactly three things

Let `old_tail` be the post that was LAST in `#series-devops` before you appended
(`vibe-coding-devops-process.html` today — its next is `"./"`, marking it as the current tail).

1. `your-post.prev = old_tail.html`
2. `old_tail.next = your-post.html`  ← replaces its `href="./"`
3. `your-post.next = "./"`  ← the terminal moves to you

Nothing else changes. Never hand-author chain order; derive it from the card order.

Exact nav shape (`grep -n 'class="post-nav"' blog/frontend-performance.html` — no line numbers
here, the bilingual conversion moved every one of them):

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
  were stale here until `73032cb` rewrote them; 0 today, so copy, don't paraphrase). Use `&amp;`
  for `&` as the existing navs do. Like the card title, it stays monolingual — `RE_PLINK`
  truncates on a nested tag.
- The `style="text-align:right;"` on the Next anchor is present in 3 files and absent in the rest;
  either is fine, but the linter's anchor regex must tolerate it.

### 3. Resync the counters

```bash
python3 .claude/skills/site-check/scripts/check_site.py --fix
```

It recomputes **seven** sites and prints the current line numbers: the two `.blog-hero__stat`
values (`5` Series, `76` Articles) and all five `.series-count` spans (20 / 10 / 13 / 24 / 9). Do
not hand-increment — that is how 33 drifted from the real 37.

**The eighth site is the `.blog-jump` chip strip in the hero, and `--fix` does not touch it.** Each
chip's trailing `· N` must equal its section's card count. Nothing policed that strip until
2026-09-05 and the Life launch forgot its chip twice; INV-02f now fails the build. Edit it by hand,
in the same commit.

The `N Categories` stat and the `.category__count` are **gone** — the `.category` bands were
deleted on 2026-08-26 (the last one, Technology, held 100% of the posts). INV-02d and INV-02e
survive as guards against a future commit re-adding an empty band; they are not counters you
maintain.

### 4. Regenerate the derived files

```bash
python3 scripts/gen_feed.py       # INV-31 fails when feed.xml and the index disagree
python3 scripts/gen_sitemap.py    # INV-32; run it in the commit AFTER the content lands,
                                  #   so the git lastmod date exists
```

Then add the post's line to `llms.txt` by hand — `check_visibility.py`'s L2 check fails when a
carded post is missing from the map.

---

## Adding an OpenClaw series post (an 8th chip)

This is a 15-file edit, not a 2-file edit.

1. Write `blog/openclaw-<slug>.html` with the strip from
   `.claude/skills/site-check/assets/series-nav.html`, its own entry as
   `<span class="current">#8 Your Label</span>`. Keep it **flat** `.series-links` — the grouped
   `.series-links--grouped` shape belongs to AI Transformation only.
2. Add the new `<a href="/blog/openclaw-<slug>">#8 Your Label</a>` line to **all 7 existing** series
   posts, in the same position, with identical label text. INV-03 compares the full label sequence
   in order across all files, so a typo in one file is a violation.
3. Add the ordinal badge. There is one form now — Phase 3 (2026-08-26) converged all four old
   markups (`.series-badge` ×4, `.series-info` ×1, bare `<p>` ×1, `<strong>` ×1) and
   `openclaw-memory.html`'s `บทที่ 3` onto a single `.post-hero__tag` line reading
   `OpenClaw for Organizations 2026 • Post #8`, which INV-20a/20b/20c guard. It stays monolingual.
4. Add the card inside `<section class="series-section" id="series-openclaw">`. There is no
   `.category` wrapper any more — the last band ("Technology") held 100% of the posts and was
   deleted on 2026-08-26; the **five** series sections sit directly in `<main>` under the featured
   post.
5. Do **not** give the post a `.post-nav` as well — INV-08 enforces exclusivity (46 series-nav / 24
   post-nav / 6 no-nav = 76).
6. The series-post footers used to carry 14 broken `/about`, `/projects`, `/research`, `/teaching`,
   `/contact` hrefs; they were fixed in `b9fb125` and INV-05 fails on a recurrence. Copy from a
   sibling that is green today.
7. Give it both language tracks (`bilingualize.py --post` / `--fill` / `--verify`), then `--fix`
   the counters, hand-edit the `#series-openclaw` `.blog-jump` chip, and regenerate `feed.xml`,
   `sitemap.xml` and the `llms.txt` line.

## Adding a Hermes or Life post

The same shape, a different arithmetic: the Hermes strip has 10 members and the Life strip 9, so
the new chip goes into 10 (or 9) existing files plus the new one. **No `SERIES7`-style check covers
these by name** — INV-03/03b/20a all iterate a hardcoded OpenClaw list. INV-03c is what covers them,
and it is FAIL severity: it groups posts by their strip's `<h3>`, substitutes each post's own href
for its `current` chip, and requires every member's chip sequence to be identical, then requires
every chip to target a member of that same strip.

**Repair when it fires:** copy the strip from a sibling and move the `<span class="current">`. Do
not "fix" it by editing the one file the report names — the report names the file whose strip
*differs*, which may be the only correct one.

## Adding an AI Transformation post — generated, not hand-edited

Twenty near-identical grouped chip strips are exactly the thing a person cannot keep in sync, so
they are not maintained by hand at all.

```bash
# 1. add the row to scripts/series/ai-transformation.json (number, slug, chip label, title,
#    hero sub, tags, read time, cover, figures)
# 2. write the two content sheets: .bilingual/<slug>.th.html and .bilingual/<slug>.en.html
#    (prose only, in bilingualize.py's <!--TH-SECTION:id--> delimiter grammar; gitignored scratch)
python3 scripts/build_series.py --check              # manifest + skeleton sanity, draws nothing
python3 scripts/build_series.py --post <slug>        # emit the post, already two-track
python3 scripts/build_series.py --restrip            # rewrite ALL the chip strips from the manifest
python3 scripts/build_series.py --index-fragment     # the card markup to paste into blog/index.html
python3 scripts/build_series.py --llms-fragment      # the llms.txt lines
python3 scripts/build_series.py --covers-rows        # the covers.tsv rows
```

Then the same tail as every other series: `make_cover.py <slug>`, `--fix` the counters, hand-edit
the `#series-ai-transformation` `.blog-jump` chip, `gen_feed.py`, `gen_sitemap.py`, `llms.txt`.

**After launch, `--restrip` is the only thing that should touch a shipped file**, and it rewrites
nothing but the strip. The emitted posts are the committed truth; the sheets in `.bilingual/` are
scratch and are not committed. If INV-03c reports an AI Transformation strip, the repair is
`--restrip`, never twenty hand edits — and if `--restrip` would change a file you did not expect,
the manifest and the tree disagree and that is the thing to investigate.

---

## Renaming a post

The filename appears in more places than you expect. Sweep all of them:

```bash
grep -rn 'old-slug' blog/ index.html
```

- the card href in `blog/index.html`
- the neighbours' `.post-nav` `href` (both the post that names it as `next` and the one that names
  it as `prev`)
- every copy of its series strip — as `/blog/old-slug`, **without** `.html` (INV-09): 7 files for
  OpenClaw, 10 for Hermes, 9 for Life, and `build_series.py --restrip` for AI Transformation
- any in-body cross-links, **in both language tracks**
- `feed.xml`, `sitemap.xml` and `llms.txt` — regenerate the first two, hand-edit the third

Rename the cover in `images/` to match only if the post follows the `<slug>-cover.*` convention —
**12 of 76** deliberately do not (`iac-cover.jpg`, `auth-cover.jpg`, `sre-cover.jpg`,
`cicd-cover.jpg`, `linux-cli-cover.jpg`, `api-lifecycle-cover.jpg`, `security-cover.jpg`,
`gitops-cover.jpg`, `kubernetes-cover.jpg`, `monitoring-cover.jpg`, `networking-cover.jpg`,
`testing-cover.jpg`). If you do rename the image, update the `covers.tsv` row, the share card
`<slug>-og.jpg`, the post body **and** the card, or INV-07b and INV-35 both go red.

## Removing a post

1. Delete the file and its card.
2. Splice the chain: `prev_of_removed.next = next_of_removed`, `next_of_removed.prev =
   prev_of_removed`. If the removed post was the tail, restore `next="./"` on the new tail. For a
   chip series, drop its chip from **every** remaining member's strip instead (`--restrip` for AI
   Transformation, plus deleting the manifest row).
3. Delete its cover **and its `<slug>-og.jpg` share card** from `images/`, and its `covers.tsv` row.
   No cover is shared today — `github-actions-cover.jpg` and `monitoring-cover.jpg` each were until
   2026-08-26, when the two borrowers got drawn art of their own (INV-07a, now with no baseline
   entry).
4. `--fix` the counters, hand-edit that series' `.blog-jump` chip, regenerate `feed.xml` and
   `sitemap.xml`, and drop its `llms.txt` line.
