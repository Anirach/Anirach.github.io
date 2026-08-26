# anirach.com

**The personal site of Dr. Anirach Mingkhwan** — Associate Professor at King Mongkut's University of Technology North Bangkok (KMUTNB), PhD (Liverpool John Moores University, UK), researcher in Agentic AI, computer networks, and big data analytics.

🌐 **Live: [anirach.com](https://anirach.com)**

A hand-written static site — six top-level pages, four per-book detail pages, and 37 self-contained blog posts. No build system, no package manager, no dependencies, no JavaScript framework. Push to `main` and GitHub Pages publishes it.

---

## At a glance

| | |
|---|---|
| **Pages** | Home · Blog · Publications · Books · Projects & Apps · News & Updates |
| **Blog** | **37 posts** in 3 categories (Technology holds 2 series; Academic & Philosophy and Lifestyle are awaiting their first posts) |
| **Stack** | Plain HTML5 + CSS3 + one 83-line vanilla-JS file. Google Fonts is the only external dependency |
| **Hosting** | GitHub Pages (classic Jekyll build) on the custom domain `anirach.com`, fronted by Cloudflare |
| **Build step** | None |
| **Tests** | `.claude/skills/site-check/scripts/check_site.py` — 57 cross-file integrity checks. This is the test suite |

## The six pages

| Page | What it holds |
|---|---|
| [`index.html`](index.html) | Single-scroll editorial portfolio: hero, about, latest-news strip, six research areas, featured book, curated live apps, contact |
| [`blog/`](blog/) | 37 posts under three category bands — see below |
| [`publications/`](publications/) | The academic record: the Springer book *Libraries in Transformation*, 8 book chapters, and a selected-publications table |
| [`books/`](books/) | Books & writing (nav label "Books"): four works — *One Day of Light* (the free last-lecture event book, EN/TH editions with free PDF downloads served from `books/`), the published novel *Three Old Men: The Last Conversation*, and two complete bilingual manuscripts — each with its own detail page (`books/one-day-of-light.html`, `books/three-old-men.html`, `books/a-pocketful-of-questions.html`, `books/the-thirteenth-seal.html`) |
| [`projects/`](projects/) | Live apps (each verified working before it ships) and research-code repositories |
| [`news/`](news/) | Reverse-chronological timeline of publications, talks and appointments, plus a career timeline |

`books/` was one "Books & Writing" page until 2026-08-23, when it split: academic content moved to the new `publications/`, and `books/` became the fiction section with one detail page per book. On 2026-08-24 it gained a fourth work, the Last Lecture companion book *One Day of Light*, whose EN/TH PDFs are downloadable for free from `books/`.

`script.js` (one IIFE, zero dependencies) drives five behaviours — nav scroll state, the mobile hamburger, an `IntersectionObserver` scroll-reveal with a 120 ms stagger, smooth anchor scrolling, and a hero-watermark parallax. **It runs on the landing page only.** The other nine pages (five section indexes and the four book detail pages) carry no JavaScript at all, by design; their mobile menu is a pure-CSS checkbox toggle.

## The blog

`blog/index.html` is a static, zero-JavaScript listing grouped into three categories. There is no filtering, sorting or search UI.

- **🤖 Technology — 37 posts**, containing two series: *OpenClaw for Organizations* (13, seven of them a numbered series linked by a chip strip) and *DevOps & Vibe Coding* (24, a single prev/next chain).
- **🎓 Academic & Philosophy** — first posts coming soon.
- **☕ Lifestyle** — first posts coming soon.

**The site is bilingual.** Headings, technical terms, code and tag labels are in English; explanatory prose is in Thai. All 37 posts declare `<html lang="th">`; the six top-level pages and the four book detail pages declare `lang="en"` and wrap Thai passages in `<span lang="th">`.

## Repository structure

```
.
├── index.html          # Landing page — the ONLY file that loads style.css or script.js
├── style.css           # Landing-page styles; carries the canonical :root token block
├── script.js           # 83 lines, one IIFE, five behaviours, zero dependencies
├── _config.yml         # Jekyll: keeps internal working docs out of the published site
├── CNAME               # anirach.com
├── blog/               # index.html (3 categories, 37 cards) + 37 self-contained posts
├── books/              # Books & writing: index.html + 4 per-book detail pages + 2 free PDFs (EN/TH), all self-contained
├── publications/  projects/  news/   # one self-contained index.html each
├── images/             # 58 files — covers, diagrams, posters, profile photo
├── docs/               # design spec, implementation plan, OpenClaw runbook (not published)
└── .claude/skills/     # the four maintenance skills (not published)
```

### Architecture: every page is an island

The single most important fact before editing:

```
index.html ──▶ style.css + script.js     (the ONLY consumer of either)

blog/index.html   ──▶ its own <style> block, no JS
blog/<post>.html  ──▶ its own <style> block, no JS     × 37
books/ (index + 4 detail) publications/ projects/ news/ ──▶ same   × 8
```

Every page embeds its complete stylesheet. There is no shared partial, template engine or token file, so a "global" change means editing N files by hand — and nothing tells you when file 23 of 47 got missed. That is what the linter is for. The compensating upside: blast radius is exactly one file.

## Local development

No install, no build. Serve the **repository root**:

```bash
python3 -m http.server 8000     # → http://localhost:8000
```

> **Serve the root, not `blog/`.** Every blog page references images as `../images/…`.

> **Known local-dev trap.** The seven numbered OpenClaw posts link to each other with root-absolute, extensionless URLs (`/blog/openclaw-101`). GitHub Pages resolves those; `http.server` does not and returns 404. That is not a regression.

## Verification

Run all three from the repo root before pushing. All must pass:

```bash
python3 .claude/skills/site-check/scripts/check_site.py      # 57 cross-file integrity checks
python3 docs/openclaw/check-news-sync.py                     # news↔homepage sync, provenance, 4 counters
python3 .claude/skills/blog-post/assets/verify-wiring.py     # blog post wiring
```

`check_site.py` exits 0 when no **new** fail-severity violation appears. It carries a baseline of pre-existing debt (`0 new, 29 known` today) — **`0 new` is what matters**, and `INV-25` fails the build if any baseline entry goes stale, so the safety net cannot silently rot. `INV-26` (added with the books split) ties every section-directory detail page to its own `index.html`: an orphan detail page, or an index card linking a file that does not exist, fails the build.

`check-news-sync.py` verifies the homepage strip mirrors the three newest news items, that every news item carries a `<!-- source: … -->` provenance comment, and that all **four** hand-typed counters match reality: `news/index.html` "7 updates", `publications/index.html` "8 chapters", and `books/index.html` "1 novel" and "2 complete" (it strips HTML comments first, so a commented-out card cannot satisfy a counter).

## Deployment

```bash
git push origin main
```

That is the whole pipeline; GitHub Pages rebuilds in 1–3 minutes. `_config.yml` excludes `docs/` and `CLAUDE.md` from the published output — they stay in the repository but are not served. Anything beginning with `.` or `_` (including `.claude/`) is omitted by Jekyll automatically.

## Adding a new blog post

Five hand edits across three files — the post, its cover, and `blog/index.html` (card + counters), plus rewiring the neighbouring posts' prev/next links. The full recipe, including which of the three navigation patterns applies, is in [`.claude/skills/blog-post/SKILL.md`](.claude/skills/blog-post/SKILL.md). Start from `.claude/skills/page-design/assets/post-template.html` — the repo's single canonical template.

## Maintenance

Four skills in [`.claude/skills/`](.claude/skills/) carry the verified detail:

| Skill | Covers |
|---|---|
| **page-design** | The house visual system — canonical tokens, type scale, component vocabulary, approved hero gradients, and the anti-patterns this repo has been burned by |
| **blog-post** | Adding, editing or removing a post without breaking the hand-wired navigation |
| **a11y-perf** | Accessibility and performance rules with this site's real measured numbers |
| **site-check** | The linter, what every check means, and how to repair each failure |

News updates have their own runbook at [`docs/openclaw/latest-updates-runbook.md`](docs/openclaw/latest-updates-runbook.md), written for an autonomous agent. Its gate enforces that every news item carries a verified source — no structural check can tell a true item from an invented one, so instead an item cannot exist without a stated source.

## Contact

- 🎓 [Google Scholar](https://scholar.google.co.th/citations?user=htY3F_IAAAAJ&hl=en)
- 💻 [GitHub @Anirach](https://github.com/Anirach)
- 📘 [Facebook](https://www.facebook.com/anirach) · 📷 [Instagram](https://www.instagram.com/anirach/)

> Open to research collaborations, speaking engagements, and academic partnerships.

---

*No `LICENSE` file is present. Content and code are © Anirach Mingkhwan; all rights reserved by default.*
