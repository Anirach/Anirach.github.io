# Design: anirach.com — Personal Platform Redesign

**Date:** 2026-08-10
**Status:** Approved by owner (structure, taxonomy, books scope, language, Approach A, full design)
**Owner:** Dr. Anirach Mingkhwan

## 1. Goal

Expand anirach.com from "portfolio + tech blog" into a personal platform that is nice, modern,
friendly, informational, and useful: news/updates about the owner, access to his writing and
books, a blog spanning Technology / Academic & Philosophy / Lifestyle, and a curated list of
live apps. Hosted on GitHub Pages; all GitHub Pages rules respected.

## 2. Decisions (settled with the owner)

| Decision | Choice |
|---|---|
| Architecture | **Approach A** — extend the hand-written static-HTML architecture. No Jekyll, no build step. The four project skills (`page-design`, `blog-post`, `a11y-perf`, `site-check`) and `check_site.py` remain the guardrails. |
| Structure | **Multi-page**: Home + `/blog/` + `/books/` + `/projects/` + `/news/` |
| Blog taxonomy | **Category sections on one blog index** (no JS, extends the existing `.series-section` pattern) |
| Books scope | All four: authored books · academic publications · recommended reading · books in progress |
| Language | **Bilingual** like the blog: English headings/technical terms, Thai explanatory prose |
| Dead app | `n8n.anirach.com` returns HTTP 500 (verified 2026-08-10) → **remove its card**; easy to restore later |

## 3. Site map

```
/                        Home (redesigned landing)
/blog/                   Blog index — three category sections
/blog/*.html             37 existing posts — URLs and content untouched
/books/                  Books & Writing
/projects/               Projects & Apps
/news/                   News & Updates
```

Main nav (`Home · Blog · Books · Projects · News · Contact`) appears on exactly 5 pages:
`index.html`, `blog/index.html`, `books/index.html`, `projects/index.html`, `news/index.html`.
The 37 posts keep their minimal `.blog-nav` back-bar — no per-post nav sweep.

New pages are HOUSE files per the `page-design` skill: canonical `:root`, Inter + JetBrains
Mono, 720px measure (860px allowed for card grids), approved gradients only, glassy nav,
`:focus-visible`, `prefers-reduced-motion`, lazy images with dimensions, `text-wrap: balance`.

## 4. Page specifications

### 4.1 Home (`index.html`) — redesign, not rebuild

Keep: editorial hero (identity works), About block, six research cards, contact pills, the
reveal/parallax behaviour. Change:

- **Latest strip** (new, after About): 3 most recent news items, one line each, linking to
  `/news/`. Hand-maintained; newest first.
- **Featured book** (new): card for *Libraries in Transformation* — cover image, one-paragraph
  bilingual blurb, "68+ citations · ~10,000 accesses" stat line, links to Springer + `/books/`.
- **Projects grid**: n8n card removed. Cards: Doctor Chatty Bot, NCD-Care+, and a "See all
  projects →" link card to `/projects/`. (NCD Health+ lives on `/projects/` only, and only
  after the §4.4 browser check passes.)
- **Nav**: add Books / Projects / News links; fix `href="#"` on the logo → `href="index.html"`
  (also fixes the `querySelector('#')` JS error).
- Footer year 2025 → 2026.
- Apply design-system Phases 1–3 to `index.html`, `style.css`, `script.js` (tokens are additive;
  dead BLOG CSS block may be removed as part of the sweep).

### 4.2 Blog index (`blog/index.html`) — reorganize into three category sections

```
🤖 Technology            ← umbrella header; the two existing .series-section blocks
                            (OpenClaw for Organizations, DevOps & Vibe Coding) sit under it
                            unchanged apart from corrected counters
🎓 Academic & Philosophy  ← new .series-section; launches with a "first posts coming soon"
                            note styled as a quiet card (no fake posts)
☕ Lifestyle              ← new .series-section; same launch state
```

- Category headers use the existing `.series-header` idiom (icon + title + count).
- Hero stats recomputed and corrected (currently stale: says 33; actual 37).
- Still **zero JavaScript** on this page.
- New posts in the new categories follow the `blog-post` skill (house template, card in the
  right section, counters, nav pattern: `.post-nav` prev/next within their category chain
  once ≥2 posts exist; standalone until then).

### 4.3 Books & Writing (`books/index.html`) — new

Order of sections:

1. **The book** (flagship card): *Libraries in Transformation: Navigating to AI-Powered
   Libraries* — Phayung Meesad & Anirach Mingkhwan, Springer *Studies in Big Data* vol. 157,
   2024, 447 pp. ISBNs 978-3-031-69215-4 (hb) / 978-3-031-69216-1 (eBook).
   DOI https://doi.org/10.1007/978-3-031-69216-1. Stat line: "~10,000 accesses · 68 citations
   (Springer, Aug 2026)". Buy/read links: Springer, Amazon.de, Barnes & Noble, Waterstones,
   Blackwell's, VitalSource. Cover image required (source from Springer or owner; compressed
   JPG ≤200 KB).
2. **Chapters** (5 verified Springer chapters, newest first) — including the two sole-authored
   persona-extraction papers (NLPIR 2025 / AUTSYS 2025, both pub. Jul 2026), Dual Graph
   Representation (AUTSYS-2024), Recommender Systems Based on Text-Representing Centroids
   (*The Autonomous Web*, 2022), Real-Time Mobile PM2.5 Monitoring (AUTSYS 2025). Each with
   Springer link.
3. **Selected publications**: top-cited table (10 rows, from Scholar Aug 2026; profile stats
   653 citations · h-index 13 · i10-index 20) + a "Recent (2024–2026)" list showing the AI
   arc (RAG centroids, chatbot dialogues, X-WiKi). Link to full Google Scholar profile.
   **Exclusion rule:** the mis-attributed Bitcoin-finance entry on the Scholar profile is
   never listed.
4. **Books in progress**: slot for *Three Old Men: The Last Conversation* (complete ~130-page
   manuscript) — **include only if the owner opts in** (pending). Otherwise section shows the
   PhD thesis lineage note or is omitted.
5. **Recommended reading**: built when the owner provides 3–8 titles with one-line notes
   (pending). Section omitted until content exists — no placeholder shelf.

### 4.4 Projects & Apps (`projects/index.html`) — new

Two tiers, each card with name, tag, bilingual description, status badge, link:

- **Live apps** (badge 🟢 Live; only URLs verified working at build time):
  Doctor Chatty Bot (`doctor-chatty-bot.lovable.app`, verified 200) ·
  NCD-Care+ (`ncd-care-plus.vercel.app`, verified 200, research-grade CDS) ·
  NCD Health+ (`ncd-health-plus.vercel.app`) **only after a real-browser check** —
  fetch caught it mid-spinner.
- **Research code** (badge 🔬 Research; links to GitHub):
  cortex-memory · cortex-openclaw (pairs with the OpenClaw blog series) ·
  ai-os-rag-workshop (badge 🎓 Workshop; bilingual, MIT) ·
  rag-second-brain (labelled "research prototype", per its own README).
- **Removed**: n8n Server card (HTTP 500), "Coming Soon" placeholder.
- Liveness policy: every Live-tier URL is probed at build time; a card is never published
  pointing at a non-200 app. `site-check` gains a manual note (not an automated check —
  external URLs are out of linter scope).

### 4.5 News & Updates (`news/index.html`) — new

Reverse-chronological timeline; each item: date, bilingual one-liner, optional link.
Launch content (all verified with sources):

- 2026 — four 2025/2026 publications land (persona-extraction ×2, PM2.5 platform, Dual Graph)
- Dec 2025 — Program Committee, DEFI 2025 (VKU, Da Nang)
- Nov 2024 — *Libraries in Transformation* published (Springer)
- May 2024 — Invited speaker, TLC36 (Thailand Library Consortium), "The Transformative Impact
  of AI on Revolutionizing Operations in Libraries"
- Optional bottom block: career timeline (Dean of FITM 2012–2020, PhD LJMU 2004, …) — include;
  it is public and verified from his TLC36 speaker bio.

Maintenance model: owner tells Claude "add news: …"; Claude adds the timeline item and, if it
is among the 3 newest, updates the Home Latest strip. Recurring sources for finding new items
are documented in the spec appendix of the implementation plan (Scholar by-date, FITM site,
DEFI/AUTSYS series, TLC events).

## 5. GitHub Pages constraints (respected by design)

- Static files only; no server-side code. All dynamic-looking features are links out to
  externally hosted apps.
- No new directories starting with `_` or `.` in the published tree (default Jekyll build).
- Site size well under 1 GB; image slimming (Phase 1) keeps bandwidth within the soft
  100 GB/month limit.
- Custom domain via existing CNAME; HTTPS fronted by Cloudflare.

## 6. Out of scope / deferred

- Jekyll migration (Approach B) — consciously rejected; revisit only if maintenance pain grows.
- Dark mode — blocked on tokens landing everywhere (page-design skill, LATER verdict).
- Converting the 11 island posts to house style (design-system Phase 4).
- RSS feed, search, comments — not requested; candidates for a later cycle.
- Publishing the novel manuscript and the recommended-reading shelf — pending owner content.

## 7. Build phases (each = one reviewable commit + `check_site.py` run)

1. **Foundation** — design-system Phase 1+2 on existing files: canonical tokens everywhere,
   re-encode 15 oversized PNG covers to JPG (~18.4 MB → ~3 MB blog index), fix 3 stale
   counters, fix 14 dead absolute links, align the forked gradient, fix nav-logo JS bug and
   hamburger CSS. Zero-to-minimal visual change.
2. **New pages** — `books/`, `projects/`, `news/` with content from §4; nav updated on the 5
   nav-bearing pages; new cover/book images added compressed.
3. **Home redesign** — §4.1.
4. **Blog reorganization** — §4.2.
5. **Polish & launch** — design-system Phase 3 sitewide (`:focus-visible`,
   `prefers-reduced-motion`, `color-scheme`, `text-wrap: balance`, `aspect-ratio`),
   screenshots, final `check_site.py` (must be green apart from documented baseline), push.

`site-check`'s counter checks and link checks must pass at the end of every phase; the linter
gains awareness of the new pages (nav consistency across the 5 nav-bearing pages, new
counters) as part of Phase 2.

## 8. Success criteria

- All five pages render correctly on phone + desktop, both with keyboard and pointer.
- Every published link resolves (internal: linter-verified; Live-tier apps: probed at publish).
- Blog index shows three categories; all 37 legacy posts reachable exactly as before.
- Books page lists only verified, correctly attributed works.
- News page has ≥4 real dated items at launch.
- `blog/index.html` payload drops from ~18.4 MB to ≤4 MB.
- No GitHub Pages rule violated (static, no `_` dirs, size/bandwidth headroom).

## 9. Owner-content backlog (non-blocking)

| Item | Needed for | Status |
|---|---|---|
| Recommended books (3–8 titles + one-liners) | Books §5 | pending |
| Novel opt-in decision | Books §4 | pending |
| Non-public news items | News | pending |
| First Lifestyle / Academic-Philosophy posts | Blog | pending |
