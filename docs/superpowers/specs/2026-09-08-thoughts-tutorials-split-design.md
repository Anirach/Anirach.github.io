# Thoughts / Tutorials split — design

**Date:** 2026-09-08 · **Status:** implemented in the working tree, uncommitted, awaiting owner review

## 1. Problem

`blog/index.html` is titled "Thoughts & Tutorials" and lists seven series. Six of them are
technical courses (DevOps, OpenClaw, Hermes Agent, Hermes Desktop, AI Transformation, AI-Core
Systems — 84 posts). The seventh, Life Thought & Philosophy, is nine essays that walk one day of
the book *One Day of Light*. The essays sit at the foot of a 13,000px technical catalog, under a
sticky bar of engineering chips, and neither audience is served: a reader who came for the essays
scrolls past six courses, and a reader who came for a course meets "Twilight · The Open Hand" as
the last thing on the page.

## 2. Decision

Two catalog pages, one per kind of writing. The post files do not move.

| | Tutorials | Thoughts |
|---|---|---|
| URL | `/blog/` (unchanged) | `/thoughts/` (new top-level section) |
| Nav label | **Tutorials** (was "Blog") | **Thoughts** |
| Content | the six technical series, 84 posts | the nine Life essays |
| Hero family | Sunrise (unchanged) | Sunrise, with a low gold "sun" glow layered over the same three stops |
| Page family | LISTING | LISTING |
| Generator | `scripts/reindex_blog.py` (unchanged contract, new copy + series tiles) | hand-written; the series is complete (9 of 9 since 2026-09-01) |

The nine essays keep their `/blog/<slug>.html` URLs, canonical tags, share cards, chip strip and
feed entries. Moving them would break nine canonical URLs, the nine-chip `.series-nav` strip that
links `/blog/morning-waking` absolutely, `scripts/bilingualize.py` (which reads
`blog/morning-waking.html` as its Sunrise skeleton) and every inbound link. A catalog page is
allowed to card a post that lives in another directory; the linter is taught that, not the posts.

**Naming assumption, easy to reverse:** the nav label "Blog" becomes "Tutorials" everywhere
("Blog" survives only in the URL and the feed title, which covers both pages). If the owner
prefers to keep "Blog", it is one label sweep — every occurrence is the literal string
`>Tutorials<` or `‹ Tutorials`.

## 3. Information architecture

Nav order on every nav-bearing page, the four book detail pages and `404.html`:

```
Tutorials · Thoughts · Publications · Books · Projects · News · Contact
```

The landing page keeps its in-page anchors first (`Research · About |`) and gains the same two
labels in place of Blog. Its footer "Sections" row does the same.

Every post footer's `.blog-footer__nav` row grows from seven to eight destinations:
`Home · Tutorials · Thoughts · Publications · Books · Projects · News · Contact`. The two other
"Blog" strings a post carries — the `‹ Blog` back link in `.blog-nav` and the footer's
`← Back to Blog` — become `‹ Tutorials` / `← Back to Tutorials` on the 84 technical posts and
`‹ Thoughts` / `← Back to Thoughts` (href `../thoughts/`) on the nine essays. The Life posts'
`.series-nav` strip, series footer and hero are unchanged.

Entry points into Thoughts beyond the nav: the landing page's *One Day of Light* block gains a
"Read the nine essays" link; `404.html` gains a Thoughts card; the Tutorials hero sub-line links to
Thoughts and vice versa.

### Nav width

Two labels widen every nav. The section-chrome nav (11 pages: 6 listing incl. `thoughts/`,
4 detail, `404.html`) last fit at 772px with six links, so its 800px mobile takeover no longer
clears the desktop bar. The takeover breakpoint is raised to the measured fit width plus headroom
and kept byte-identical across all 11 pages; the landing page's 1080px block is re-measured the
same way. Measurement is done in a real browser (`scrollWidth` of `.nav__inner` against the
viewport), not estimated.

## 4. `thoughts/index.html`

A LISTING page copied from `blog/index.html`'s skeleton (same `.nav`, `:root`, fonts, a11y tail,
skip link, `<main id="main">`, footer), `lang="en"`, canonical `https://anirach.com/thoughts/`,
its own 1200×630 share card `images/og-thoughts.jpg` drawn by `scripts/make_og_thoughts.py`.

Structure, top to bottom:

1. **Hero** — label `Anirach Mingkhwan · Life Thought & Philosophy · ไทย ⇄ English`, h1
   "Thoughts", one sentence in English and one in Thai, no counted stats (the count lives in the
   linter-checked `.series-count` below). A link to Tutorials in the sub-line.
2. **Companion band** — the book the essays grow from: both cover faces (EN left, TH right, as on
   `books/`), title, one line, links to the detail page and the two free PDFs. Not a card
   (no `class="card"`), so no counter or feed regex sees it.
3. **One `<section class="series-section" id="series-life">`** — h2 `One Day of Light`, a
   `.series-count` of `9 essays`, a description that says the essays are meant to be read in
   order (the finale keeps a secret). Inside, three parts as `<h3 class="part-title">` —
   Morning · เช้า (for the life), Noon · เที่ยง (for the work), Twilight · สนธยา (for what
   remains) — each followed by exactly three cards.
4. **Cards** — a 3-up grid, one row per part, the full 800×800 cover shown uncropped (the title
   and Thai caption are drawn into the art; any crop cuts one of them), ordinal, EN title / TH
   title, a two-line Thai excerpt, date and read time. Markup keeps the exact grammar every parser
   reads: `<a href="../blog/<slug>.html" class="card">`, first `<img>` is the cover,
   `<h4 class="card__title">`, `<p class="card__excerpt">`, `<time datetime>`. Card titles are
   `h4` because the ladder here is page → series → part → essay.
5. **Footer** — the LISTING footer.

Part identity is a 3px top rule on each part's cards — cloud blue, gold, navy — so the page reads
as one day moving from dawn to dusk without a third gradient family.

## 5. `blog/index.html` (Tutorials)

- Hero: h1 "Tutorials", sub "Six series on DevOps, AI agents and AI-core engineering …" with a
  link to Thoughts; stats `6 Series · 84 Articles`.
- Jump bar: the Life chip is gone; RSS stays.
- **Series tiles** — a new "Choose a series" block between the spotlight and the sections: six
  `<a class="series-tile" href="#series-…">` (icon, name, N articles, total reading time summed
  from the cards, one-line description). Never `class="card"`.
- The `#series-life` section is removed. Everything else — spotlight, numbered row cards, DevOps
  chain order — is untouched.
- `scripts/reindex_blog.py` emits all of the above and stays idempotent on its own output.

## 6. Linter and generators

`check_site.py` gains a **catalog** concept: every nav-bearing page whose body contains
`<section class="series-section"` is a post catalog (today `blog/index.html` and
`thoughts/index.html`). `Site` parses each catalog and exposes merged views (`site.cards`,
`site.card_page`, `site.card_pos`, `site.sections` with the page attached) so the existing checks
keep working:

- INV-01a: every post is carded on some catalog; the existing duplicate-card check means no post
  may be carded twice.
- INV-02a/b: required on `blog/index.html`; on any other catalog a hero stat is verified only if
  present. The label `Essays` is accepted alongside `Articles`.
- INV-02c: `.series-count` accepts `essays?` as well as `articles?`.
- INV-02f: the jump strip is required on `blog/index.html` and checked wherever it exists.
- INV-07b, INV-10, INV-36, `--fix`: run per catalog page; line numbers point at the right file.
- INV-23/24/27/13/30/32 need no change — `thoughts/` is discovered as a section directory.
- INV-31: the feed must list exactly the union of both catalogs.

`scripts/gen_feed.py` reads both catalogs. `scripts/gen_sitemap.py` adds `thoughts` to its
section list. `scripts/check_visibility.py` L2 reads series titles from every catalog.
`.claude/skills/blog-post/assets/verify-wiring.py` reads both catalogs. `llms.txt` re-heads the
six technical series as "Tutorials — …", the essays as "Thoughts — …", and adds the section link.

## 7. Documentation

`CLAUDE.md`, `README.md` and the four project skills carry counts and names this change
invalidates (7 Series · 93 Articles, "5 LISTING pages", `#series-life` on the blog index, the
nav label). Those lines are updated in the same change, per the skills' standing rule.

## 8. Testing

```bash
python3 .claude/skills/site-check/scripts/check_site.py            # exit 0, 0 new
python3 scripts/check_visibility.py --strict                       # exit 0
python3 .claude/skills/blog-post/assets/verify-wiring.py           # CLEAN
python3 docs/openclaw/check-news-sync.py                           # unchanged, green
python3 scripts/gen_feed.py --check && python3 scripts/gen_sitemap.py --check
python3 scripts/reindex_blog.py --repo . --out /tmp/idx.html && diff -q /tmp/idx.html blog/index.html
```

Plus, in a browser: both catalogs at 1440 / 1024 / 768 / 390, the nav at the new breakpoint
boundary ±1px on a section page and on the landing page, and a contrast check of every text
colour placed over the Thoughts hero glow.

## 9. Out of scope

Moving the essay files, a Thoughts-only RSS feed, changing any post body, the Life posts'
chip strip, and the feed's item order.

## 10. Measurements (2026-09-08, Chrome headless via Playwright, `file://`)

| What | Result | Decision |
|---|---|---|
| Section-chrome nav, 7 links + Scholar pill | last fits at **921px** (was 772px with 6 links) | takeover `@media (max-width: 950px)` on all 11 pages, byte-identical |
| Landing nav, 9 links + divider + pill, gap 2.2rem | needs **1205px** | gap reduced to **1.5rem** |
| Landing nav, gap 1.5rem | needs **1103px** | takeover `@media (max-width: 1140px)` (same ~37px headroom as 1080 had over 1044) |
| Thoughts hero text over the sun and glow, text hidden and the worst ground pixel sampled | label 6.79:1 · title 10.39:1 · sub 7.96:1 · aside 6.46:1 at 1440; at 390 the aside over the sun is **4.82:1** (blue-dark link) and slate is darker still | all AA; the sun stays at opacity 0.55 |
| `blog/index.html` regenerated by `reindex_blog.py`, then regenerated from its own output | byte-identical | idempotence holds |
| Share card `images/og-thoughts.jpg` | 1200×630, 54 KB | INV-27 validates the dimensions |

Gates after the change: `check_site.py` 62/62 (INV-02g new), `check_visibility.py --strict` 0 fail
(overall 99), `verify-wiring.py` CLEAN, `check-news-sync.py` PASS, feed 93 items, sitemap 104 URLs.
