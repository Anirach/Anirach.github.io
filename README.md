# anirach.com

**The personal portfolio and technical blog of Dr. Anirach Mingkhwan** — Associate Professor at King Mongkut's University of Technology North Bangkok (KMUTNB), PhD (Liverpool John Moores University, UK), researcher in Agentic AI, computer networks, and big data analytics.

🌐 **Live site: [anirach.com](https://anirach.com)**

A hand-written static site: three files for the landing page and 38 self-contained HTML files for the blog. No build system, no package manager, no dependencies, no JavaScript framework. Push to `main` and GitHub Pages publishes it.

---

## At a glance

| | |
|---|---|
| **Landing page** | A single-scroll "editorial magazine" portfolio — hero, about, six research areas, three projects, contact |
| **Blog** | **37 posts** across **2 series**, ~33,000 lines of hand-written HTML |
| **Stack** | Plain HTML5 + CSS3 + one 83-line vanilla-JS file. Google Fonts is the only external dependency |
| **Hosting** | GitHub Pages (classic build, `main` @ `/`) on the custom domain `anirach.com`, fronted by Cloudflare |
| **Build step** | None |

---

## The landing page

`index.html` is a full-viewport magazine cover followed by four editorial sections, in DOM order:

| Section | `id` | Contents |
|---|---|---|
| Hero | `hero` | Giant `ANIRACH` watermark, rotated label strip, a deliberately ghosted portrait, two-line name in fluid `clamp()` type |
| About | `about` | Editorial pull-quote, portrait watermark, bio card linking to Google Scholar |
| Research | `research` | Six glassmorphism cards: Agentic AI, Computer Networks, Big Data, Wireless Technologies, Information Security, Cloud Computing |
| Projects | `projects` | [n8n Server](https://n8n.anirach.com), [Doctor Chatty Bot](https://doctor-chatty-bot.lovable.app), and an "Agentic AI Research — Coming Soon" placeholder |
| Contact | `contact` | Pill links with inline SVG icons: Google Scholar, GitHub, Facebook, Instagram |

`script.js` (one IIFE, zero dependencies) drives five behaviours: nav scroll state, the mobile hamburger menu, an `IntersectionObserver` scroll-reveal with a 120 ms stagger, smooth anchor scrolling, and a hero-watermark parallax. All of it applies to the landing page only.

## The blog

`blog/index.html` is a static, zero-JavaScript listing page. Posts are grouped into two hand-curated series sections — there is no filtering, sorting, or search UI.

### 🤖 OpenClaw for Organizations — 13 posts

> Building intelligent AI systems that think, remember, and act autonomously — from foundational concepts to multi-agent production deployments.

Seven of these form a numbered series, linked by a `.series-nav` chip strip that appears identically inside all seven posts:

| # | Title | File |
|---|---|---|
| 1 | OpenClaw 101 | `openclaw-101.html` |
| 2 | Agent Teams | `openclaw-agent-teams.html` |
| 3 | Memory & Knowledge | `openclaw-memory.html` |
| 4 | Security & Access | `openclaw-security.html` |
| 5 | Integrations | `openclaw-integrations.html` |
| 6 | Skills & Automation | `openclaw-skills.html` |
| 7 | Production & Scale | `openclaw-production.html` |

The remaining six are standalone pieces in the same section: `beyond-plugins`, `claude-code-architecture`, `idle-self-improvement`, `obsidian-ai-jarvis`, `openclaw-memory-architecture`, `openclaw-migration`.

> ⚠️ `openclaw-memory.html` (series post #3) and `openclaw-memory-architecture.html` (a separate standalone post) are different articles with near-identical slugs. Easy to confuse.

### 🚀 DevOps & Vibe Coding — 24 posts

> A comprehensive journey through modern DevOps practices — from Git fundamentals to Kubernetes orchestration, CI/CD pipelines, and production-ready infrastructure.

These form a single linear prev/next reading chain (the listing page shows them newest-first, i.e. in reverse):

```
 1. git-branching                 13. gitops-argocd
 2. cicd-pipeline                 14. cloud-architecture
 3. docker-vs-vms                 15. sre-fundamentals
 4. api-request-lifecycle         16. github-actions
 5. kubernetes-orchestration      17. code-quality
 6. networking-fundamentals       18. automated-testing
 7. infrastructure-as-code        19. database-sql
 8. monitoring-observability      20. authentication-authorization
 9. linux-command-line            21. web-architecture
10. devops-security               22. frontend-performance
11. software-testing              23. deployment-hosting
12. docker-compose                24. vibe-coding-devops-process
```

### Content conventions

**The site is bilingual.** Headings, technical terms, code, and tag labels are in English; explanatory body prose is in Thai. All 37 posts declare `<html lang="th">`; the landing page and blog index declare `lang="en"`.

---

## Repository structure

```
.
├── index.html          # Landing page — the ONLY file that loads style.css or script.js
├── style.css           # 638 lines, landing page only. Plain hex colors — no :root, no var()
├── script.js           # 83 lines, one IIFE, five behaviours, zero dependencies
├── CNAME               # "anirach.com"
├── CLAUDE.md           # Working notes for Claude Code
├── README.md           # This file
├── blog/
│   ├── index.html      # Static listing: 2 series sections, 37 cards, no JavaScript
│   └── *.html          # 37 posts, each fully self-contained with an embedded <style>
└── images/             # 50 files (28 jpg, 22 png) — covers, diagram exports, profile photo
```

There is no `package.json`, lockfile, CI workflow, `.gitignore`, `.nojekyll`, `robots.txt`, `sitemap.xml`, `404.html`, RSS feed, or `LICENSE` file.

### Architecture: every page is an island

The single most important fact for anyone editing this repo:

```
index.html ──▶ style.css + script.js     (the ONLY consumer of either)

blog/index.html   ──▶ its own <style> block, no JS
blog/<post>.html  ──▶ its own <style> block, no JS      × 37
```

Every file under `blog/` embeds its complete stylesheet; there is no shared blog stylesheet, template engine, or token file. Consequences:

1. A blog-wide CSS change means editing N files — there is no single place to make it.
2. Nothing is computed: post counts, series order, and cross-links are all typed by hand.
3. The compensating upside: blast radius is exactly one file. Editing a post cannot break any other page.

Two design families coexist: the **indigo** family (`#6366f1` accent — landing page, blog index, and the 26 "canonical" posts, which share a `:root` token block, Inter + JetBrains Mono, and the `.blog-nav`/`.post-hero`/`.post-body`/`.post-nav` skeleton) and the **violet** family (`#8b5cf6` accent — the 11 OpenClaw-era posts, which use OS font stacks and their own component vocabulary).

---

## Local development

No install, no build. Serve the **repository root** with any static server:

```bash
python3 -m http.server 8000     # → http://localhost:8000
# or
npx serve .
```

> **Serve the root, not `blog/`.** Every blog page references images as `../images/…`; serving `blog/` directly breaks them all.

> **Known local-dev trap.** The seven numbered OpenClaw posts link to each other with root-absolute, extensionless URLs (`/blog/openclaw-101`). GitHub Pages resolves those to `.html`; `python3 -m http.server` does not and returns 404. If the OpenClaw series navigation appears broken locally, it is this — not a regression.

You will also see a `favicon.ico` 404 in the console; the repo has no favicon.

## Deployment

```bash
git add -A && git commit -m "..." && git push origin main
```

That is the whole pipeline. GitHub Pages runs its classic (Jekyll) build on every push; since nothing in the repo starts with `_` or `.`, nothing is dropped — but note that a future `_drafts/`-style directory would silently vanish from the build (no `.nojekyll` is present).

---

## Adding a new blog post

Everything is manual — five steps, three files. Skipping a step is how drift happens.

1. **Create `blog/<slug>.html`** by copying the closest existing post. Stay within one family: `web-architecture.html` is a good canonical starting point; `openclaw-skills.html` for the OpenClaw family. Keep `<html lang="th">` for Thai-body posts.
2. **Add a cover image** as `images/<slug>-cover.png` or `.jpg` — and compress it first (existing PNG covers average >1 MB, which is the repo's main weight problem).
3. **Add a card to the right `.series-section`** in `blog/index.html`, copying the exact `<a class="card">` anatomy of an existing card (three tags, author block, `Read →`). New DevOps posts go at the **top** of that section (newest-first listing).
4. **Update the hand-typed counters** in `blog/index.html`: the section's `.series-count` badge and the hero `<strong>N</strong> Articles` pill. Nothing computes these — see below.
5. **Wire navigation at both ends.** DevOps: add a `.post-nav` to your post *and* repoint the previous chain tail's `Next →`. OpenClaw numbered series: add a chip to the strip in **all** existing series posts. Standalone: at minimum a footer link back to the listing.

Don't add `data-reveal` to blog pages (the observer lives on the landing page only), and don't build diagrams as inline HTML/CSS or ASCII art — both approaches were tried and abandoned; diagrams are PNG exports in `images/`.

## Maintenance notes

Nothing in this repo is enforced by tooling, so cross-file consistency is checked by hand. Known open items:

- **The article counters on `blog/index.html` have drifted**: the hero says "33 Articles" and the OpenClaw badge says "12 articles"; the real counts are 37 total (13 + 24).
- **Several OpenClaw posts link to routes that don't exist** (`/about`, `/projects`, `/research`, `/contact`, `/teaching`) — 14 links across 6 files, all 404 in production; the landing page uses in-page anchors instead.
- **The DevOps chain has a loose head**: `git-branching.html` (post #1) has no prev/next block of its own.
- **The blog's mobile menu is non-functional**: blog pages render a hamburger button but carry no JavaScript to open it.
- **`images/` is ~20 MB**, with nine unreferenced legacy files and several covers over 1 MB, served without compression or `srcset`.

Verified clean: all 37 posts are linked from the index, every link resolves, and every referenced image exists on disk.

---

## Contact

- 🎓 [Google Scholar](https://scholar.google.co.th/citations?user=htY3F_IAAAAJ&hl=en)
- 💻 [GitHub @Anirach](https://github.com/Anirach)
- 📘 [Facebook](https://www.facebook.com/anirach)
- 📷 [Instagram](https://www.instagram.com/anirach/)

> Open to research collaborations, speaking engagements, and academic partnerships.

---

*No `LICENSE` file is present. Content and code are © Anirach Mingkhwan; all rights reserved by default.*
