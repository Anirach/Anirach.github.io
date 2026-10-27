<p align="center">
  <img src="https://img.shields.io/badge/anirach.com-Live-1D4ED8?style=for-the-badge" alt="anirach.com live">
  <img src="https://img.shields.io/badge/Zero-JavaScript-111827?style=for-the-badge" alt="Zero JavaScript">
  <img src="https://img.shields.io/badge/Build_step-None-7C3AED?style=for-the-badge" alt="No build step">
  <img src="https://img.shields.io/badge/Posts-145_bilingual-059669?style=for-the-badge" alt="145 bilingual posts">
  <img src="https://img.shields.io/badge/GitHub_Pages-Deploy_on_push-0EA5E9?style=for-the-badge&logo=github&logoColor=white" alt="GitHub Pages">
</p>

<h1 align="center">🌅 anirach.com</h1>

<p align="center">
  <strong>The personal site of Dr. Anirach Mingkhwan — independent AI consultant, author, and former Dean of FITM, KMUTNB.</strong>
  <br>
  <em>A consultant profile, 145 bilingual Thai/English posts in 11 series, four books and an academic record — hand-written, zero-JavaScript, no build step.</em>
</p>

<p align="center">
  <a href="#-the-problem">The Problem</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-how-it-works">How It Works</a> •
  <a href="#-verification">Verification</a> •
  <a href="#-development">Development</a> •
  <a href="#%EF%B8%8F-conventions-and-gotchas">Gotchas</a>
</p>

---

## 🤔 The Problem

A static site with no build step buys simplicity and pays for it in one specific way: **nothing is shared, so nothing is enforced.**

- every page embeds its own complete stylesheet — there is no partial, template engine or token file
- a "global" change is therefore an N-file edit, by hand, across 157 files
- nothing tells you when file 23 of 157 got missed
- counters, navigation chains, feed items and sitemap URLs are hand-wired across files that never import one another
- and every post is bilingual, so each prose edit has a mirror that can silently drift

**This repository answers that with a linter instead of a framework.** 62 cross-file integrity checks are the test suite, and the baseline of accepted debt is empty — so any violation printed is new.

---

## ✨ What This Repo Does Differently

| Concern | The usual static-site answer | Here |
|:---|:---|:---|
| **Consistency across pages** | A template engine or partials | Nothing shared — but **62 checks** fail the build on drift, baseline empty since 2026-08-26 |
| **Interactivity** | A framework, or at least some JS | **Zero executable JavaScript.** `INV-38` fails the build on any `<script>` that is not `application/ld+json` |
| **Reveal animations, mobile menu** | IntersectionObserver + click handlers | Scroll-driven CSS (`animation-timeline: view()`), `:target`, and a checkbox toggle |
| **Bilingual content** | An i18n library, or two URLs per page | One URL, two tracks, a pure-CSS `ไทย · English` switch — four CSS lines |
| **Long series of posts** | Hand-copied templates that rot | **7 series are generated** from a manifest + per-post content sheets + a skeleton read at run time |
| **Catalog pages** | Hand-ordered cards | `reindex_blog.py` regenerates both catalogs; re-run it rather than hand-fixing order |
| **Feed and sitemap** | Hand-maintained, quietly stale | Generated on demand; `INV-31` / `INV-32` fail the build when either drifts |
| **Image weight** | Ship the full cover everywhere | A 144px `-thumb.jpg` via `srcset` — the Tutorials catalog went 3.63 MB → 0.42 MB |
| **Web fonts** | Request every weight | Variable **range** syntax (`wght@300..900`) — one file, not seven; 189 KB saved per page |
| **Coding tutorials** | Code pasted into the lesson | Each series pairs with a runnable GitHub companion, pinned to a commit |
| **Dated content** | Goes stale silently | A runbook names every file to revise when an announced event passes |

---

## 🗺️ Site Map

| Page | What it holds |
|:---|:---|
| [`index.html`](index.html) | Single-scroll **consultant profile**: hero, services, engagement approach, selected work, about and career, research, free library, latest news, contact |
| [`blog/`](blog/) | The **Tutorials** catalog — 106 cards in 8 technical series, plus all 145 post files |
| [`thoughts/`](thoughts/) | The **Thoughts** catalog — 39 essay cards in 3 series, each linking `../blog/<slug>.html` |
| [`publications/`](publications/) | The academic record: the Springer book *Libraries in Transformation*, 8 book chapters, selected publications |
| [`books/`](books/) | Four works, each with a detail page — *One Day of Light* (free EN/TH PDFs), the novel *Three Old Men*, and two complete bilingual manuscripts |
| [`projects/`](projects/) | Live apps, each verified working before it ships, and research-code repositories |
| [`news/`](news/) | Reverse-chronological timeline of publications, talks and appointments |

> **The posts never move.** Every post is `blog/<slug>.html`, including the 39 essays that `/thoughts/` catalogues. The 2026-09-08 split separated the two *catalogs*, not the files.

---

## 📚 The Catalogs

**Tutorials — `/blog/`, hero reads `8 Series · 106 Articles`**

| Series | Posts | Navigation | Generated |
|:---|:---:|:---|:---:|
| 🧩 AI-Core Functional Workflows | 12 | chip strip | ✅ |
| 🔬 AI-Core + Jev in Practice | 10 | chip strip | ✅ |
| 🛡️ Engineering AI-Core Systems | 10 | chip strip | ✅ |
| 💻 Hermes Desktop Hands-On | 7 | chip strip | ✅ |
| 🧭 AI Transformation for Organizations | 20 | grouped chip strip (Reframe · Redesign · Engineer · Lead) | ✅ |
| ⚡ Hermes Agent in Practice | 10 | chip strip | — |
| 🤖 OpenClaw for Organizations | 13 | 7 numbered, 6 standalone with no nav | — |
| 🔧 DevOps & Vibe Coding | 24 | a single prev/next chain | — |

**Thoughts — `/thoughts/`, hero reads `3 Series · 39 Essays`**

| Series | Essays | Shape | Generated |
|:---|:---:|:---|:---:|
| 🌱 Wisdom for a Good Life | 20 | four arcs of five — Self · Mind · Work · Others | ✅ |
| 🧭 Working Philosophies | 10 | one working week, Monday to Friday | ✅ |
| 🌅 Life Thought & Philosophy | 9 | one day in three parts — Morning · Noon · Twilight | — |

**All 145 posts are bilingual.** A `ไทย · English` pill swaps between two complete tracks of the same article. Thai is the default, there is no JavaScript, and the page-level `<html lang="th">` never changes — the English track is `lang="en"` inside it.

The Thoughts essays are written in a different register from the tutorials: literary Thai in the author's own voice, not code-switched technical prose. The brief, with ten rules and worked before/after pairs, is [`thai-essay-voice.md`](.claude/skills/blog-post/references/thai-essay-voice.md).

---

## 🏗️ Architecture

### Every page is an island

The single most important fact before editing:

```
index.html ──▶ style.css                 (the ONLY consumer of it)

blog/index.html   ──▶ its own <style> block, no JS
blog/<post>.html  ──▶ its own <style> block, no JS     × 145
thoughts/ books/ (index + 4 detail) publications/ projects/ news/ 404.html ──▶ same   × 10
```

Editing `style.css` affects **only** the landing page. Editing one post affects **only** that file. The upside of having no shared partial: blast radius is exactly one file. The cost: a change that should apply everywhere must be scripted, then verified.

### By the numbers

| | Count |
|:---|---:|
| HTML files on disk | 157 |
| …enumerated by the linter (`404.html` is deliberately excluded) | 156 |
| Blog posts, all bilingual | 145 |
| Series across the two catalogs | 11 |
| Images | 496 |
| …covers (800×800) · book faces | 146 · 8 |
| …card thumbs (144×144) · share cards (1200×630) · series figures | 145 · 149 · 37 |
| Feed items · sitemap URLs | 145 · 156 |
| Generator and sweep scripts | 15 |
| Integrity checks | 62 (43 fail · 17 warn · 2 info) |

---

## 🔄 How It Works

### Generated series

Seven series are emitted whole rather than hand-copied. `scripts/build_series.py` takes three inputs:

| Input | What it carries |
|:---|:---|
| **Manifest** — `scripts/series/<name>.json` | the fixed strings: numbers, slugs, chip labels, titles, hero subs, tags, read times, covers, figures |
| **Content sheets** — `.bilingual/<slug>.{th,en}.html` | prose only, in the delimiter grammar `bilingualize.py` already uses |
| **Skeleton** — a real post, read at **run time** | the `<style>` block, so it is a template rather than a copy that rots; `--check` diffs what it lifted |

```bash
python3 scripts/build_series.py --series good-life --check          # manifest + skeleton sanity
python3 scripts/build_series.py --series good-life --post <slug>    # emit one post
python3 scripts/build_series.py --series good-life --restrip        # rewrite every chip strip
python3 scripts/build_series.py --series good-life --sync-read-min  # read times from the prose
```

**The emitted posts are the committed truth; the sheets in `.bilingual/` are scratch** and are gitignored. For a generated series a prose edit goes through the sheet and `--post`, never through the emitted file.

### The catalogs

```bash
python3 scripts/reindex_blog.py --repo . --out blog/index.html
python3 scripts/reindex_blog.py --repo . --out thoughts/index.html --catalog thoughts
```

Both are idempotent. The Thoughts catalog **lifts its `<style>` from the blog catalog at run time**, so the two cannot drift apart — which also means a new series on `/blog/` brings its `:target` selectors across on the next regeneration.

### Feed and sitemap

```bash
python3 scripts/gen_feed.py      # reads both catalogs
python3 scripts/gen_sitemap.py   # lastmod from each file's last git commit
```

Run the sitemap in the commit **after** a content change, so the git dates exist.

---

## 🚀 Quick Start

### Prerequisites

Python 3, standard library only. No install, no package manager, no dependencies.

```bash
git clone https://github.com/Anirach/Anirach.github.io.git
cd Anirach.github.io
python3 -m http.server 8000     # → http://localhost:8000
```

> **Serve the repository root, not `blog/`.** Every blog page references images as `../images/…`.

> **Known local-dev trap.** The chip-strip series link to each other with root-absolute, **extensionless** URLs (`/blog/openclaw-101`). GitHub Pages resolves those; `http.server` does not, and returns 404. That is not a regression.

---

## ✅ Verification

Run all four from the repository root before pushing. All must pass.

```bash
python3 .claude/skills/site-check/scripts/check_site.py      # 62 cross-file integrity checks
python3 scripts/check_visibility.py --strict                 # search/AI visibility, JSON-LD, metadata
python3 docs/openclaw/check-news-sync.py                     # news ↔ homepage sync, provenance, 4 counters
python3 .claude/skills/blog-post/assets/verify-wiring.py     # blog post wiring
```

| Gate | What only it catches |
|:---|:---|
| `check_site.py` | card ↔ post ↔ cover wiring, counters, chip strips, prev/next chains, hero gradients, social blocks, the zero-JS rule |
| `check_visibility.py` | JSON-LD shape, `inLanguage` against the bilingual markup, `llms.txt` drift, heading ladders |
| `check-news-sync.py` | the homepage strip mirrors the 3 newest news items, every item carries a `<!-- source: … -->` comment, and 4 hand-typed counters match |
| `verify-wiring.py` | per-post navigation pattern, stale nav titles, broken links inside `blog/` |

`check_site.py` exits 0 when no fail-severity violation appears. **Its baseline of accepted debt is empty**, so any violation it prints is new, and `INV-25` fails the build if a baseline entry is ever added and goes stale.

---

## 🧑‍💻 Development

### Project structure

```
.
├── index.html              # consultant profile — the ONLY file that loads style.css
├── style.css               # landing-page styles + the canonical :root token block
├── blog/                   # the Tutorials catalog + all 145 post files
├── thoughts/               # the Thoughts catalog (39 cards → ../blog/)
├── books/ publications/ projects/ news/     # one self-contained index.html each
├── images/                 # 496 files — covers, thumbs, share cards, figures, posters
├── examples/               # the two runnable tutorial labs (teaching source, not a site dependency)
├── downloads/              # the reviewed lab ZIPs
├── scripts/                # 15 generators and sweeps
│   └── series/             # 7 manifests, one per generated series
├── docs/                   # specs, plans, the news runbook + its gate (not published)
├── .claude/skills/         # the four maintenance skills (not published)
├── feed.xml  sitemap.xml  llms.txt  robots.txt
└── CNAME                   # anirach.com
```

### Scripts

| Script | Does |
|:---|:---|
| `build_series.py` | emits a whole generated series from manifest + sheets + skeleton |
| `reindex_blog.py` | regenerates either catalog page |
| `gen_feed.py` · `gen_sitemap.py` | regenerate `feed.xml` · `sitemap.xml` |
| `bilingualize.py` | converts a post to two tracks, splices a translation, `--verify` per file |
| `make_cover.py` | draws the 800×800 cover and the 1200×630 share card together |
| `make_figure.py` | draws series figures as palette PNGs |
| `check_visibility.py` | the search/AI-visibility scanner |
| `retoken.py` · `reheroize.py` | sitewide palette and hero sweeps |

### Maintenance skills

Four skills in [`.claude/skills/`](.claude/skills/) carry the verified detail this README only summarises:

| Skill | Covers |
|:---|:---|
| **page-design** | canonical tokens, type scale, component vocabulary, approved hero gradients, and the anti-patterns this repo has been burned by |
| **blog-post** | adding, editing or removing a post without breaking the hand-wired navigation; plus the Thai essay voice brief |
| **a11y-perf** | accessibility and performance rules with this site's real measured numbers |
| **site-check** | the linter, what every check means, and how to repair each failure |

> **Every number in those skills is load-bearing.** A change that invalidates one must update it in the same commit. A confidently wrong measurement is worse than none, because it gets acted on.

---

## 🧪 Tutorial Labs and Companions

**Standing delivery default (owner preference, 2026-10-23).** A coding tutorial pairs the website lesson with a **runnable GitHub companion**. Each chapter links directly to its matching code files and tests. The companion README must cover prerequisites, exact commands, expected results, troubleshooting and lesson-to-code mapping; commands are verified from a clean copy, and secrets and generated output stay out of publication. Website and companion publication stay within the scope authorised for that task.

| Series | Lessons | Status | Companion | Local mirror · ZIP |
|:---|:---:|:---|:---|:---|
| **AI-Core Functional Workflows** | 12 | **Published** | [`ai-core-functional-tutorial`](https://github.com/Anirach/ai-core-functional-tutorial), pinned at commit `869487af4cf0` | `examples/ai-core-functional-lab/` · `downloads/ai-core-functional-lab.zip` |
| **AI-Core + Jev in Practice** | 10 | **Local draft — not published** | [`ai-core-jev-tutorial`](https://github.com/Anirach/ai-core-jev-tutorial) | `examples/ai-core-jev-lab/` · `downloads/ai-core-jev-lab.zip` |

Both labs are **offline by default**: fixtures need no SDK, credentials, network or paid API call, and no paid live API call has been tested. All fixture metrics and most cost inputs are explicitly fictional. The Jev lab's optional live adapter pins `@typesafe-ai/sdk@0.7.0` / `jev-1.13.0` and is **not** live-verified. The labs are Node 22.18+ teaching material; the website pages still execute no JavaScript.

> ⚠️ **The ten-part AI-Core + Jev series must not be included in a publication without separate approval.** It is currently wired into the catalog, feed and sitemap in this repository — decide whether to publish or unwire it before pushing.

---

## 🛠️ Common Workflows

### Add a post

A post is not one file. It is a file **plus** a cover, a share card, a thumb, a catalog card, counters, its neighbours' nav links, a feed item, a sitemap entry and an `llms.txt` line — **in two language tracks**, with no build step to catch a miss. The full recipe, including which of the four navigation patterns applies, is in [`blog-post/SKILL.md`](.claude/skills/blog-post/SKILL.md). Start from `.claude/skills/page-design/assets/post-template.html`, the repo's single canonical template.

For one of the seven generated series, add a manifest row and run `build_series.py` instead. Never hand-edit a generated post.

### Repair the counters

```bash
python3 .claude/skills/site-check/scripts/check_site.py --fix   # rewrites blog counters only
python3 scripts/reindex_blog.py --repo . --out blog/index.html  # tiles and ordering
```

### Add a news item

The runbook is [`latest-updates-runbook.md`](docs/openclaw/latest-updates-runbook.md), written for an autonomous agent. Its gate enforces that every news item carries a verified source — no structural check can tell a true item from an invented one, so instead an item cannot exist without a stated source.

### Expire dated content

When an announced event passes, nothing computes the copy for you. The same runbook names every file to revise, and records what the last expiry's checklist missed. The lesson it ends on: **grep for the dead call-to-action, not just for the date** — and remember that removing a CTA can orphan its image.

---

## ⚠️ Conventions and Gotchas

- **The site loads no executable JavaScript, and that is enforced.** `script.js` was deleted 2026-08-26; `INV-38` fails the build on any `<script>` that is not `application/ld+json`. Each of the script's four jobs has a CSS replacement in `style.css`.
- **The reveal keyframe has a `from` and deliberately no `to`.** An element at rest is therefore in its natural state, so a browser without `animation-timeline` simply shows the content. Never "complete" the keyframe, and never re-invert the default — before the fix, 53% of the landing page rendered as empty coloured bands with JS off.
- **Sarabun keeps the semicolon font syntax on purpose.** Inter and JetBrains Mono use the variable range form (`wght@300..900`); Sarabun has no variable version and a range request returns **HTTP 400**. All five of its static weights are used, and an unrequested one gets faux-bolded, which smears Thai glyphs.
- **`srcset` is a comma-separated candidate list, not a path.** Three link resolvers had to learn that when the catalog thumbs landed, or the site's first `srcset` reports 123 broken links.
- **Card `src` stays the full cover.** `INV-07b` reads the `src` basename and requires it to equal the post's own cover; the thumb is offered as a `srcset` candidate, so a browser without support still gets a valid image.
- **Navigation belongs to neither language track.** Chip strips, prev/next pairs and card titles stay monolingual, because the linters read them with regexes that would concatenate or truncate on a nested tag.
- **The featured post is `class="feature"`, never `class="card"`.** Three separate regexes count `class="card"`; one extra match inflates every counter and duplicates a feed item.
- **`.bilingual/` is gitignored and unversioned.** A botched content sheet has no history — back it up before a sweep.
- **`404.html` is deliberately excluded** from the social block, the sitemap and the linter's enumeration. Do not "fix" it by adding one.

---

## 🚢 Deployment Notes

```bash
git push origin main
```

That is the whole pipeline; GitHub Pages rebuilds in 1–3 minutes. `_config.yml` excludes `docs/` and `CLAUDE.md` from the published output — they stay in the repository but are not served. Anything beginning with `.` or `_` (including `.claude/`) is omitted by Jekyll automatically.

> **Cloudflare caches HTML for 10 minutes and assets for 4 hours.** After a deploy, append `?cb=$RANDOM` to check the real state before diagnosing a problem that is not there — and remember your own browser holds its copy for the same 10 minutes, so a stale tab needs a hard reload rather than a bug report.

Still the owner's, outside the repository: verifying a Search Console property, and a Rich-Results spot-check after structured-data changes.

---

## 🔍 Troubleshooting

| Symptom | Likely cause | Suggested fix |
|:---|:---|:---|
| Chip-strip links 404 locally | `http.server` does not resolve extensionless URLs | Not a regression — GitHub Pages resolves them |
| Images missing in the browser | Serving `blog/` instead of the repository root | Serve the root; posts reference `../images/…` |
| A counter fails the build | A card was added without re-running the generator | `check_site.py --fix`, then `reindex_blog.py` |
| `INV-06a` reports an orphan image | A removed block was the image's last reference | Delete the image, or restore the reference |
| The feed looks empty | A heading level was re-cut and a parser hard-codes it | Grep for the class, never the level |
| A generated post reverts after an edit | It was hand-edited instead of its sheet | Edit `.bilingual/<slug>.th.html`, then `--post` |
| The live site shows old copy | Browser or edge cache | Hard reload, or `?cb=$RANDOM` to bypass |

---

## 🎯 Repository Intent

This repository is best understood as **a publishing system that happens to have no build step**:

- part consultant profile and professional front door
- part bilingual technical library — 145 posts across 11 series
- part generated-content pipeline — 7 series emitted from manifests
- part self-checking test suite — 62 invariants standing in for the framework that is not there

It is most valuable as a demonstration that **a site can stay consistent at this size without a build system, provided the consistency is measured rather than assumed.**

---

## 📬 Contact

- 🎓 [Google Scholar](https://scholar.google.co.th/citations?user=htY3F_IAAAAJ&hl=en)
- 💻 [GitHub @Anirach](https://github.com/Anirach)
- 📘 [Facebook](https://www.facebook.com/anirach) · 📷 [Instagram](https://www.instagram.com/anirach/)

> Open to AI consulting engagements, research collaborations, speaking and workshops.

---

## 📄 License

No `LICENSE` file is present. Content and code are © Anirach Mingkhwan; all rights reserved by default.
