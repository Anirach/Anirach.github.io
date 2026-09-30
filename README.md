# anirach.com

**The personal site of Dr. Anirach Mingkhwan** — Associate Professor at King Mongkut's University of Technology North Bangkok (KMUTNB), PhD (Liverpool John Moores University, UK), researcher in Agentic AI, computer networks, and big data analytics.

🌐 **Live: [anirach.com](https://anirach.com)**

A hand-written static site — seven top-level pages, four per-book detail pages, and 123 self-contained blog posts catalogued on two pages: Tutorials (`/blog/`, six technical series) and Thoughts (`/thoughts/`, thirty-nine essays on living well and working well). No build system, no package manager, no dependencies, no JavaScript framework. Push to `main` and GitHub Pages publishes it.

---

## At a glance

| | |
|---|---|
| **Pages** | Home · Tutorials (`/blog/`) · Thoughts (`/thoughts/`) · Publications · Books · Projects & Apps · News & Updates |
| **Posts** | **123**, in 9 series across two catalogs, every one bilingual Thai/English |
| **Files** | 135 HTML files on disk (134 enumerated by the linter; `404.html` is deliberately excluded) |
| **Stack** | Plain HTML5 + CSS3, zero JavaScript. Google Fonts is the only external dependency |
| **Hosting** | GitHub Pages (classic Jekyll build) on the custom domain `anirach.com`, fronted by Cloudflare |
| **Build step** | None |
| **Tests** | Four scripts, run before every push — `check_site.py` alone carries 62 cross-file integrity checks. This is the test suite |

## The seven pages

| Page | What it holds |
|---|---|
| [`index.html`](index.html) | Single-scroll editorial portfolio: hero, about, latest-news strip, six research areas, featured book, curated live apps, contact |
| [`blog/`](blog/) | The **Tutorials** catalog — 84 cards in six technical series, plus all 123 post files |
| [`thoughts/`](thoughts/) | The **Thoughts** catalog — 39 essay cards in three series, each linking `../blog/<slug>.html` |
| [`publications/`](publications/) | The academic record: the Springer book *Libraries in Transformation*, 8 book chapters, and a selected-publications table |
| [`books/`](books/) | Books & writing: four works — *One Day of Light* (the free last-lecture event book, EN/TH editions with free PDF downloads served from `books/`), the published novel *Three Old Men: The Last Conversation*, and two complete bilingual manuscripts — each with its own detail page |
| [`projects/`](projects/) | Live apps (each verified working before it ships) and research-code repositories |
| [`news/`](news/) | Reverse-chronological timeline of publications, talks and appointments, plus a career timeline |

**The posts never move.** Every post is `blog/<slug>.html`, including the 39 essays that `/thoughts/` catalogues — the 2026-09-08 split separated the two *catalogs*, not the files.

`books/` was one "Books & Writing" page until 2026-08-23, when it split: academic content moved to the new `publications/`, and `books/` became the fiction section with one detail page per book. On 2026-08-24 it gained a fourth work, the Last Lecture companion book *One Day of Light*, whose EN/TH PDFs are downloadable for free from `books/`.

`script.js` is gone — deleted 2026-08-26. **The site loads no executable JavaScript at all**, and `check_site.py` INV-38 fails the build on any `<script>` that is not `application/ld+json` (schema.org metadata, which the browser parses as data and never executes — 128 pages carry one). Each of the script's four jobs has a CSS replacement in `style.css`: the scroll-reveal and the nav scroll state are scroll-driven CSS animations (`animation-timeline: view()` / `scroll(root)`), the landing page's mobile menu is `.nav__links:target`, and anchor scrolling is native `scroll-behavior: smooth`. The other pages' mobile menu is a pure-CSS checkbox toggle — a second mechanism, also without JavaScript.

## The two catalogs

Both are static, zero-JavaScript and **generated** by `scripts/reindex_blog.py` — re-run it rather than hand-ordering cards. Each is a hero, a sticky chip strip, a "Start here" feature, a row of series tiles, then one numbered-row-card section per series. There is no filtering, sorting or search UI.

**Tutorials — `/blog/`, hero reads 6 Series · 84 Articles**

| Series | Posts | Navigation |
|---|---|---|
| 🛡️ Engineering AI-Core Systems | 10 | chip strip · generated |
| 💻 Hermes Desktop Hands-On | 7 | chip strip · generated |
| 🧭 AI Transformation for Organizations | 20 | grouped chip strip (Reframe · Redesign · Engineer · Lead) · generated |
| ⚡ Hermes Agent in Practice | 10 | chip strip |
| 🤖 OpenClaw for Organizations | 13 | seven are a numbered chip-strip series; six stand alone with no nav |
| 🔧 DevOps & Vibe Coding | 24 | a single prev/next chain |

**Thoughts — `/thoughts/`, hero reads 3 Series · 39 Essays**

| Series | Essays | Navigation |
|---|---|---|
| 🌱 Wisdom for a Good Life | 20 | grouped chip strip, four arcs of five (Self · Mind · Work · Others) · generated |
| 🧭 Working Philosophies | 10 | chip strip, one working week Monday to Friday · generated |
| 🌅 Life Thought & Philosophy | 9 | chip strip, one day in three parts (Morning · Noon · Twilight) |

**Five of the nine series are generated** from a manifest plus per-post content sheets: `python3 scripts/build_series.py --series <name>`, with manifests in `scripts/series/` (`ai-core`, `ai-transformation`, `good-life`, `hermes-desktop`, `working`). For those, the manifest and the sheets are the edit surface — never the emitted post.

**Every post is bilingual.** All 123 carry a pure-CSS Thai ⇄ English switch: a `ไทย · English` pill in the hero swaps between two complete tracks of the same article. Thai is the default, there is no JavaScript, and the page-level `<html lang="th">` never changes — the English track is `lang="en"` inside it. The seven top-level pages and the four book detail pages are `lang="en"` chrome and wrap their Thai passages in `<span lang="th">`.

The Thoughts essays are written in a different register from the tutorials — literary Thai in the author's own voice, not code-switched technical prose. The brief, with ten rules and worked before/after pairs, is [`.claude/skills/blog-post/references/thai-essay-voice.md`](.claude/skills/blog-post/references/thai-essay-voice.md).

## Repository structure

```
.
├── index.html          # Landing page — the ONLY file that loads style.css
├── style.css           # Landing-page styles; carries the canonical :root token block
├── _config.yml         # Jekyll: keeps internal working docs out of the published site
├── CNAME               # anirach.com
├── sitemap.xml         # 134 URLs, generated · feed.xml — 123 items, generated · llms.txt · robots.txt
├── blog/               # index.html (the Tutorials catalog, 84 cards) + all 123 self-contained posts
├── thoughts/           # index.html (the Thoughts catalog — 39 essay cards linking ../blog/)
├── books/              # index.html + 4 per-book detail pages + 3 free PDFs, all self-contained
├── publications/  projects/  news/   # one self-contained index.html each
├── images/             # 431 files — 124 covers (800×800) + 8 book faces, 123 card thumbs (144×144),
│                       #   130 share cards (1200×630), diagrams, series figures, posters, profile photo
├── scripts/            # 13 generators and sweeps (build_series, reindex_blog, gen_feed, gen_sitemap,
│                       #   make_cover, make_figure, bilingualize, check_visibility, …)
├── docs/               # design spec, implementation plan, OpenClaw runbook (not published)
└── .claude/skills/     # the four maintenance skills (not published)
```

### Architecture: every page is an island

The single most important fact before editing:

```
index.html ──▶ style.css                 (the ONLY consumer of it)

blog/index.html   ──▶ its own <style> block, no JS
blog/<post>.html  ──▶ its own <style> block, no JS     × 123
thoughts/ books/ (index + 4 detail) publications/ projects/ news/ 404.html ──▶ same   × 10
```

Every page embeds its complete stylesheet. There is no shared partial, template engine or token file, so a "global" change means editing N files by hand — and nothing tells you when file 23 of 135 got missed. That is what the linter is for. The compensating upside: blast radius is exactly one file.

## Local development

No install, no build. Serve the **repository root**:

```bash
python3 -m http.server 8000     # → http://localhost:8000
```

> **Serve the root, not `blog/`.** Every blog page references images as `../images/…`.

> **Known local-dev trap.** The eight chip-strip series — 93 posts in all — link to each other with root-absolute, extensionless URLs (`/blog/openclaw-101`). GitHub Pages resolves those; `http.server` does not and returns 404. That is not a regression.

## Verification

Run all four from the repo root before pushing. All must pass:

```bash
python3 .claude/skills/site-check/scripts/check_site.py      # 62 cross-file integrity checks
python3 scripts/check_visibility.py --strict                 # search/AI-visibility, JSON-LD, metadata
python3 docs/openclaw/check-news-sync.py                     # news↔homepage sync, provenance, 4 counters
python3 .claude/skills/blog-post/assets/verify-wiring.py     # blog post wiring
```

`check_site.py` runs **62 checks — 43 fail-severity, 17 warn, 2 info** — and exits 0 when no fail-severity violation appears. Its baseline of pre-existing debt is **empty** since 2026-08-26 — the tree is clean (`0 new, 0 known`), so any violation it prints is new and any fail-severity one blocks the push. `INV-25` fails the build if a baseline entry is ever added and goes stale, so the safety net cannot silently rot. `INV-26` (added with the books split) ties every section-directory detail page to its own `index.html`: an orphan detail page, or an index card linking a file that does not exist, fails the build.

`check-news-sync.py` verifies the homepage strip mirrors the three newest news items, that every news item carries a `<!-- source: … -->` provenance comment, and that all **four** hand-typed counters match reality: `news/index.html` "7 updates", `publications/index.html` "8 chapters", and `books/index.html` "1 novel" and "2 complete" (it strips HTML comments first, so a commented-out card cannot satisfy a counter).

`feed.xml` and `sitemap.xml` are generated, not hand-written — `scripts/gen_feed.py` and `scripts/gen_sitemap.py`. INV-31 and INV-32 fail the build when either drifts from the catalogs. Run the sitemap in the commit *after* a content change, so the git `lastmod` dates exist.

## Deployment

```bash
git push origin main
```

That is the whole pipeline; GitHub Pages rebuilds in 1–3 minutes. `_config.yml` excludes `docs/` and `CLAUDE.md` from the published output — they stay in the repository but are not served. Anything beginning with `.` or `_` (including `.claude/`) is omitted by Jekyll automatically.

> **Cloudflare caches HTML for 10 minutes and assets for 4 hours.** After a deploy, append `?cb=$RANDOM` to check the real state before diagnosing a problem that is not there — and remember your own browser holds its copy for the same 10 minutes, so a stale tab needs a hard reload rather than a bug report.

## Performance notes

Two measured costs were paid down on 2026-09-10, and both are easy to reintroduce:

- **Fonts are requested with the variable *range* syntax.** `Inter:wght@300..900` gets one variable file; the semicolon form `Inter:wght@300;400;…;900` makes the API serve **one static file per weight** — 7 files and 331 KB for the latin subset against 1 file and 47 KB. Switching saved 189 KB per page, 56% of the font bytes. **Sarabun keeps the semicolon form**: it has no variable version, a range request returns HTTP 400, and all five of its static weights are used.
- **Catalog cards ship a 144px derivative through `srcset`.** The row card renders its cover in a 72px box, so an 800×800 source was ~11× oversampled. `/blog/` went from 3.63 MB to 0.42 MB, `/thoughts/` from 2.11 MB to 0.38 MB.

Both are documented with their measurements in the **a11y-perf** skill (R8b and R1b).

## Adding a new blog post

A post is not one file — it is a file plus a cover plus a share card plus a card plus counters plus its neighbours' nav links plus a feed item, a sitemap entry and an `llms.txt` line, **in two language tracks**, with no build step to catch a miss. The full recipe, including which of the four navigation patterns applies, is in [`.claude/skills/blog-post/SKILL.md`](.claude/skills/blog-post/SKILL.md). Start from `.claude/skills/page-design/assets/post-template.html` — the repo's single canonical template. For one of the five generated series, add a manifest row and run `build_series.py` instead; never hand-edit those posts.

## Maintenance

Four skills in [`.claude/skills/`](.claude/skills/) carry the verified detail:

| Skill | Covers |
|---|---|
| **page-design** | The house visual system — canonical tokens, type scale, component vocabulary, approved hero gradients, and the anti-patterns this repo has been burned by |
| **blog-post** | Adding, editing or removing a post without breaking the hand-wired navigation; plus the Thai essay voice brief |
| **a11y-perf** | Accessibility and performance rules with this site's real measured numbers |
| **site-check** | The linter, what every check means, and how to repair each failure |

Every number in those skills is load-bearing: a change that invalidates one must update it in the same commit. A confidently wrong measurement is worse than none, because it gets acted on.

News updates have their own runbook at [`docs/openclaw/latest-updates-runbook.md`](docs/openclaw/latest-updates-runbook.md), written for an autonomous agent. Its gate enforces that every news item carries a verified source — no structural check can tell a true item from an invented one, so instead an item cannot exist without a stated source.

## Contact

- 🎓 [Google Scholar](https://scholar.google.co.th/citations?user=htY3F_IAAAAJ&hl=en)
- 💻 [GitHub @Anirach](https://github.com/Anirach)
- 📘 [Facebook](https://www.facebook.com/anirach) · 📷 [Instagram](https://www.instagram.com/anirach/)

> Open to research collaborations, speaking engagements, and academic partnerships.

---

*No `LICENSE` file is present. Content and code are © Anirach Mingkhwan; all rights reserved by default.*
