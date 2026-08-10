# anirach.com Personal Platform Redesign — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Expand anirach.com into a five-page personal platform (Home, Blog with three categories, Books & Writing, Projects, News) on the existing hand-written static-HTML architecture.

**Architecture:** Approach A — no build system, no Jekyll layouts, every page self-contained with embedded CSS. New pages are HOUSE files per the `page-design` skill. Cross-file integrity is guarded by `.claude/skills/site-check/scripts/check_site.py` (run before and after every task).

**Tech Stack:** Hand-written HTML5/CSS3, one vanilla-JS file (`script.js`, landing page only), GitHub Pages (classic build), macOS `sips` for image re-encoding, Python 3 stdlib for the linter.

## Global Constraints

- Spec: `docs/superpowers/specs/2026-08-10-personal-platform-redesign-design.md` — authoritative for content and structure.
- Every task starts with `python3 .claude/skills/site-check/scripts/check_site.py --quiet` (capture baseline) and ends with the same command showing **no new failures** vs. baseline.
- The 37 existing post URLs must never change. `blog/*.html` post files are not edited except where a task names them explicitly.
- All new pages: `<html lang="en">` for index-style pages with bilingual body copy (EN headings, Thai prose), canonical `:root` from `page-design` §1, Inter + JetBrains Mono via Google Fonts with both `preconnect` hints, `:focus-visible` + `prefers-reduced-motion` + `color-scheme: light` + `text-wrap: balance` snippets from `page-design` §6, all `<img>` with `alt`, `width`, `height`, `loading`, `decoding`.
- No new file or directory whose name starts with `_` or `.` inside the published tree (GitHub Pages Jekyll build would drop it). `docs/` is allowed to publish.
- Images: covers ≤200 KB, JPG for photographic/AI art, PNG only for flat-color diagrams (`page-design` anti-pattern 5).
- Never list the mis-attributed Bitcoin-finance Scholar entry (spec §4.3).
- Commits: one per task, message prefixed by phase, ending with `Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>`.
- Before EVERY task that edits HTML/CSS: read `.claude/skills/page-design/SKILL.md` §0–§5 (HOUSE/ISLAND check, tokens, components). Before blog-index edits: `.claude/skills/blog-post/SKILL.md`.

---

## Phase 1 — Foundation

### Task 1: Commit the session deliverables and capture the red baseline

**Files:**
- Commit (already on disk, untracked/modified): `README.md`, `CLAUDE.md`, `.claude/skills/**`
- Create: `docs/superpowers/plans/2026-08-10-personal-platform-redesign.md` (this file)

**Interfaces:**
- Produces: a clean working tree and a recorded linter baseline that every later task compares against.

- [ ] **Step 1: Verify what is uncommitted**

Run: `git status --porcelain`
Expected: ` M CLAUDE.md`, `?? .claude/`, `?? README.md`, `?? docs/superpowers/plans/`

- [ ] **Step 2: Record the pre-work linter baseline**

Run: `python3 .claude/skills/site-check/scripts/check_site.py --quiet > /tmp/site-check-baseline.txt; echo "exit=$?"; tail -8 /tmp/site-check-baseline.txt`
Expected: `exit=1`, FAILING: `INV-02a, INV-02c` (the two stale counters), 81 known-baseline violations. Anything else → STOP and investigate before proceeding.

- [ ] **Step 3: Commit**

```bash
git add README.md CLAUDE.md .claude/ docs/superpowers/plans/
git commit -m "chore: add README, project skills, CLAUDE.md updates, and implementation plan

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>"
```

### Task 2: Canonical `:root` token sweep (design-system Phase 1)

**Files:**
- Modify: all 28 `blog/*.html` files that already have a `:root`, the 11 island posts (add tokens + convert hex literals), `blog/index.html`, `style.css` (normalise its 9 matching hexes; do NOT add `:root` — it has none by design until this task adds one at the top)
- Reference: `.claude/skills/page-design/references/tokens.md` (deviation table, delete list), `.claude/skills/a11y-perf/references/n-file-edits.md` (verified sweep loops with proving greps)

**Interfaces:**
- Produces: every published page defines the canonical token set below; later tasks reference `var(--blue)`, `var(--radius)` etc. and rely on these exact values.

- [ ] **Step 1: Capture per-file screenshots for 3 sentinel pages (visual no-op proof)**

Run: `python3 -m http.server 8123 &` then screenshot `http://localhost:8123/`, `/blog/`, `/blog/web-architecture.html` (browser MCP or manual). Save to `/tmp/before-tokens/`.

- [ ] **Step 2: Apply the canonical `:root`**

The canonical block (paste verbatim, from `page-design` §1):

```css
:root {
  /* ink */
  --navy: #0f172a; --slate: #334155; --slate-light: #64748b; --gray: #94a3b8;
  /* ground */
  --bg: #f8fafc; --white: #ffffff; --code-bg: #1e293b;
  /* accent */
  --blue: #6366f1; --blue-dark: #4f46e5; --blue-light: #818cf8;
  /* status — use only these six, never invent a seventh */
  --green: #22c55e; --red: #ef4444; --amber: #f59e0b;
  --cyan: #06b6d4; --purple: #8b5cf6; --purple-dark: #7c3aed;
  /* type */
  --font: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  --mono: 'JetBrains Mono', 'Fira Code', monospace;
  /* form */
  --radius: 12px; --radius-sm: 8px; --radius-lg: 16px;
  --measure: 720px; --wide: 860px;
  --transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
```

Method per file group (loops with proving greps are in `a11y-perf/references/n-file-edits.md` — use them, they carry the `.claude`-exclusion guards):
1. 28 files with existing `:root`: replace the block wholesale; re-add any file-local brand tokens (`--docker-blue`, `--gh-*`) after it; delete alias tokens `--indigo`/`--muted`/`--violet` and replace their `var()` uses with `var(--blue)`/`var(--slate-light)`/`var(--purple-dark)`.
2. 11 island posts: insert the block at the top of their `<style>`; do NOT convert their literal hexes yet (that is Phase-4 territory, out of scope here — tokens are additive only).
3. `style.css`: insert the block at the top; normalise the one off-palette hex `#475569` (1 use) to `#64748b`.
4. `blog/index.html`: replace its variant `:root` (keeps `--radius` but corrected to `12px`).

- [ ] **Step 3: Prove zero rendering change**

Re-screenshot the 3 sentinel pages into `/tmp/after-tokens/`; compare visually. Run the token-conflict proof:
`grep -h -- '--navy:' blog/*.html style.css | sort -u` → exactly one value `#0f172a`. Repeat for `--slate`, `--bg`, `--blue`.

- [ ] **Step 4: Lint**

Run: `python3 .claude/skills/site-check/scripts/check_site.py --quiet`
Expected: identical failure set to `/tmp/site-check-baseline.txt`.

- [ ] **Step 5: Commit**

```bash
git add -A blog/ style.css
git commit -m "phase1: land canonical :root tokens in all pages (zero visual change)

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>"
```

### Task 3: Re-encode the 15 oversized PNG covers to JPG

**Files:**
- Modify: `images/` (15 new `.jpg` files; delete the replaced `.png` files), every HTML file referencing those 15 covers (`blog/index.html` + each post's hero)
- Reference: `.claude/skills/a11y-perf/SKILL.md` R1 (the verified `sips` pipeline: 17,477,332 → 1,670,431 bytes measured on copies)

**Interfaces:**
- Produces: `images/<name>-cover.jpg` files that Task 9/10 reference; total `blog/index.html` payload ≤4 MB.

- [ ] **Step 1: List the 15 targets and their referrers**

Run: `find images -name '*.png' -size +500k | sort` — expect 15 files (largest: `obsidian-ai-jarvis-cover.png` 1.57 MB). For each, find referrers: `grep -rl "$(basename $f)" index.html blog/ --include='*.html'`.

- [ ] **Step 2: Convert on copies, then swap**

```bash
mkdir -p /tmp/cover-convert && for f in $(find images -name '*.png' -size +500k); do
  base=$(basename "$f" .png)
  sips -s format jpeg -s formatOptions 80 "$f" --out "images/${base}.jpg" >/dev/null
  echo "${base}: $(stat -f%z "$f") -> $(stat -f%z "images/${base}.jpg")"
done
```
Expected: every output ≤250 KB. Any output >250 KB: re-run that file with `formatOptions 70`.

- [ ] **Step 3: Rewrite references, then delete the PNGs**

For each converted `<base>`: `grep -rl "images/${base}.png" index.html blog/*.html` → replace `.png` with `.jpg` in each (Edit tool, exact-string). Then `git rm` the 15 PNGs.
Guard: `grep -r "${base}.png" index.html blog/ --include='*.html'` → 0 hits before deleting each.

- [ ] **Step 4: Verify payload and lint**

Run: `python3 -c "
import re
total=0
for m in set(re.findall(r'src=\"\.\./(images/[^\"]+)\"', open('blog/index.html').read())):
    import os; total+=os.path.getsize(m)
print(total/1e6,'MB')"`
Expected: ≤4.0 MB (spec success criterion). Then `check_site.py --quiet` → no new failures (INV-07 cover checks must stay green: post hero and index card were rewritten together).

- [ ] **Step 5: Commit**

```bash
git add -A images/ blog/ index.html
git commit -m "phase1: re-encode 15 oversized PNG covers to JPG (blog index 18.4MB -> <4MB)

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>"
```

### Task 4: Fix counters, the forked gradient, and the 14 dead absolute links

**Files:**
- Modify: `blog/index.html` (lines ~221/235 counters via `--fix`; line ~64 gradient stop), and the 6 OpenClaw files carrying dead links: `blog/openclaw-101.html`, `blog/openclaw-agent-teams.html`, `blog/openclaw-integrations.html`, `blog/openclaw-memory.html`, `blog/openclaw-production.html`, `blog/openclaw-security.html`
- Modify: `.claude/skills/site-check/scripts/check_site.py` (remove the now-fixed entries from `BASELINE`, lines 153–260 region)

**Interfaces:**
- Produces: a fully green-on-counters linter; later tasks' baselines assume INV-02a/02c pass.

- [ ] **Step 1: Counters**

Run: `python3 .claude/skills/site-check/scripts/check_site.py --fix`
Expected output: rewrites hero `33 → 37` Articles and `#series-openclaw` `12 → 13`; diff-style summary printed. Verify: `grep -o '<strong>[0-9]*</strong> Articles' blog/index.html` → `37`.

- [ ] **Step 2: Gradient fork**

In `blog/index.html` (~line 64): change `linear-gradient(135deg, #e8f0fe 0%, #ddd6fe 40%, #c7d2fe 100%)` middle stop `40%` → `50%`.

- [ ] **Step 3: Dead links**

The 14 links point at `/about`, `/projects`, `/research`, `/contact`, `/teaching`, plus `href="../about/"` at `blog/openclaw-memory.html:318`. Replace each with the real in-page-anchor equivalents:
`/about` → `/#about` · `/projects` → `/#projects` · `/research` → `/#research` · `/contact` → `/#contact` · `/teaching` → `/#research` (no teaching section exists; research is the closest real destination) · `../about/` → `/#about`.
Find them: `grep -rnoE 'href="(/(about|projects|research|contact|teaching)/?|\.\./about/)"' blog/*.html` → expect 14 rows before, 0 after.

- [ ] **Step 4: Shrink the linter baseline**

In `check_site.py` `BASELINE`, delete the INV-05 dead-route keys and any counter keys just fixed. Run `python3 .claude/skills/site-check/scripts/check_site.py --quiet` → **exit 0**. If any other baseline entry now double-counts, adjust and re-run until exit 0 with an honest (smaller) baseline.

- [ ] **Step 5: Commit**

```bash
git add blog/ .claude/skills/site-check/scripts/check_site.py
git commit -m "phase1: fix stale counters, forked hero gradient, and 14 dead absolute links

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>"
```

### Task 5: Landing-page defect fixes

**Files:**
- Modify: `index.html` (line 18 logo href; line 187 footer year), `script.js` (guard), `style.css` (hamburger `.active` rules; delete dead BLOG block lines 469–561 and the four orphan `.*__label` rules)

**Interfaces:**
- Produces: `index.html` nav markup that Task 9 extends with new links.

- [ ] **Step 1: Logo href + JS guard**

`index.html:18`: `<a href="#" class="nav__logo">` → `<a href="index.html" class="nav__logo">`.
`script.js` smooth-scroll block (lines 61–70): guard the selector —

```js
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    const href = this.getAttribute('href');
    if (href.length < 2) return;               // bare "#" — let the browser be
    const target = document.querySelector(href);
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});
```

- [ ] **Step 2: Hamburger X animation**

Append to the nav section of `style.css` (the JS already toggles `.active`):

```css
.nav__hamburger.active span:nth-child(1) { transform: translateY(7px) rotate(45deg); }
.nav__hamburger.active span:nth-child(2) { opacity: 0; }
.nav__hamburger.active span:nth-child(3) { transform: translateY(-7px) rotate(-45deg); }
.nav__hamburger span { transition: transform 0.3s, opacity 0.3s; }
```

- [ ] **Step 3: Dead CSS removal**

Delete `style.css` lines 469–561 (the `/* BLOG */` block — 13 selectors `.blog` … `.blog__read-more`; verify the range by reading first, the token sweep may have shifted line numbers) and the rules for `.about__label`, `.research__label`, `.projects__label`, `.contact__label`. Guard: `grep -cE 'class="blog|__label' index.html` → 0 (nothing referenced them).

- [ ] **Step 4: Footer year**

`index.html:187`: `© 2025` → `© 2026`.

- [ ] **Step 5: Verify in browser + lint + commit**

Serve, click the logo (no console error, scrolls/navigates home), toggle hamburger at 500px width (bars form an X). `check_site.py --quiet` → exit 0.

```bash
git add index.html script.js style.css
git commit -m "phase1: fix nav-logo JS error, hamburger animation, dead CSS, footer year

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>"
```

---

## Phase 2 — New pages

**Shared nav block for the 5 nav-bearing pages** (defined once here; every page task copies it verbatim, adjusting the path prefix and the `class="active"` placement):

```html
<nav class="nav">
  <div class="nav__inner">
    <a href="{PREFIX}index.html" class="nav__logo">Anirach</a>
    <div class="nav__links" id="navLinks">
      <a href="{PREFIX}blog/">Blog</a>
      <a href="{PREFIX}books/">Books</a>
      <a href="{PREFIX}projects/">Projects</a>
      <a href="{PREFIX}news/">News</a>
      <a href="{PREFIX}index.html#contact">Contact</a>
    </div>
    <div class="nav__right">
      <a href="https://scholar.google.co.th/citations?user=htY3F_IAAAAJ&hl=en" target="_blank" rel="noopener" class="nav__cta">Google Scholar ›</a>
      <button class="nav__hamburger" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button>
    </div>
  </div>
</nav>
```

`{PREFIX}` = `` (empty) on `index.html`, `../` on the four sub-pages. On each page, its own link gets `class="active"`. New sub-pages embed the `.nav` CSS from `blog/index.html` (glassy: `background: rgba(248,250,252,0.88); backdrop-filter: blur(20px)`), and — since sub-pages carry no JS — the hamburger is a no-JS `<details>`-based fallback: wrap `.nav__links` in `<details class="nav__mobile"><summary aria-label="Menu">☰</summary>…</details>` shown only ≤768px. (Keeps the "zero JS on blog pages" rule while making mobile nav actually work — the current dead hamburger on `blog/index.html` is replaced by the same pattern.)

**Shared page skeleton for the 3 new pages** — copy the head/foot of `blog/index.html` (post-Task-2 version: canonical tokens, Inter link, both preconnects), swap in the nav above, and append the `page-design` §6 modern-CSS snippets verbatim (`:focus-visible`, `prefers-reduced-motion`, `color-scheme`, `text-wrap: balance`). Footer: `© 2026 Anirach Mingkhwan — Associate Professor, KMUTNB` with a `← Home` link.

### Task 6: `books/index.html`

**Files:**
- Create: `books/index.html`, `images/libraries-in-transformation-cover.jpg`
- Reference: `.claude/skills/page-design/references/components.md` (card markup)

**Interfaces:**
- Produces: `/books/` URL that nav links target; the book-cover image that Task 10's featured-book card reuses.

- [ ] **Step 1: Source the book cover**

Try: `curl -sL -o /tmp/lit-cover.jpg "https://media.springernature.com/w306/springer-static/cover-hires/book/978-3-031-69216-1"` — verify it is a real JPEG ≥10 KB (`file /tmp/lit-cover.jpg`). If Springer blocks it, screenshot the cover from the Springer page via browser MCP, or fall back to a typographic cover card (navy ground, title set in Inter 800) — never ship a broken `<img>`. Compress: `sips -s format jpeg -s formatOptions 80 -Z 800 /tmp/lit-cover.jpg --out images/libraries-in-transformation-cover.jpg` → ≤120 KB.

- [ ] **Step 2: Build the page**

Sections in order (all content verified in the spec — copy exactly from spec §4.3):

1. Hero (Indigo-deep approved gradient): title "Books & Writing", Thai subline "หนังสือ บทความ และงานเขียนทางวิชาการ".
2. **The book** — feature card: cover (`width="306" height="460" loading="eager" fetchpriority="high"`), full title, authors "Phayung Meesad · Anirach Mingkhwan", Springer Studies in Big Data vol. 157 · 2024 · 447 pp., stat chips "~10,000 accesses" / "68 citations (Springer, Aug 2026)", bilingual blurb (EN one-liner + 2 Thai sentences on AI-powered libraries), link row: Springer (DOI `https://doi.org/10.1007/978-3-031-69216-1`), Amazon.de, Barnes & Noble, Waterstones, Blackwell's, VitalSource — exact URLs in spec §4.3 item 1; all `target="_blank" rel="noopener"`.
3. **Chapters** — 5 rows, newest first, each: title (linked to its Springer URL from spec §4.3 item 2), venue+volume, year, author note ("sole author" on the two persona papers). Mark the two 2025/2026 persona-extraction chapters with a `--purple` accent chip "Agentic AI".
4. **Selected publications** — the 10-row top-cited table from spec §4.3 item 3 (columns: Paper · Venue · Year · Citations, `tabular-nums`), stats line "653 citations · h-index 13 · i10-index 20 (Scholar, Aug 2026)", then "Recent 2024–2026" 3-item list (RAG centroids · chatbot dialogues · X-WiKi), then a `.btn--pill` link to the Scholar profile.
5. **Books in progress** — OMIT at build time (owner decision pending). Leave an HTML comment `<!-- books-in-progress slot: pending owner opt-in, see spec §4.3.4 -->`.
6. **Recommended reading** — OMIT; comment `<!-- recommended-reading slot: pending owner list, see spec §9 -->`.

- [ ] **Step 3: Verify + commit**

Serve locally; check: title renders, cover loads, all 6 retail links respond (curl HEAD each → 200/301/403-bot-block are all acceptable; 404 is not). Keyboard-tab through the page — focus ring visible. `check_site.py --quiet` → no new failures.

```bash
git add books/ images/libraries-in-transformation-cover.jpg
git commit -m "phase2: add Books & Writing page (Springer book, chapters, publications)

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>"
```

### Task 7: `projects/index.html`

**Files:**
- Create: `projects/index.html`

**Interfaces:**
- Consumes: shared nav/skeleton (Phase-2 preamble).
- Produces: `/projects/` URL; the card set that Task 10's home preview mirrors (first two Live cards).

- [ ] **Step 1: Browser-verify NCD Health+ (spec gate)**

Open `https://ncd-health-plus.vercel.app` in a real browser (browser MCP). PASS = dashboard renders past the loading spinner within ~10 s. FAIL = omit its card and leave `<!-- ncd-health-plus: excluded, failed browser check <date> -->`.

- [ ] **Step 2: Probe every Live-tier URL (liveness policy)**

```bash
for u in https://doctor-chatty-bot.lovable.app https://ncd-care-plus.vercel.app https://ncd-health-plus.vercel.app; do
  echo "$u → $(curl -s -o /dev/null -w '%{http_code}' -L --max-time 15 $u)"; done
```
Any non-200 → that card is omitted this build.

- [ ] **Step 3: Build the page**

Hero (Violet approved gradient): "Projects & Apps", Thai subline "แอปและโปรเจกต์ที่สร้างและใช้งานจริง". Then two sections:

**Live apps** (`.card` grid, status chip 🟢 Live):
- **Doctor Chatty Bot** — tag `AI / Healthcare` — EN line "Thai medical-assistant chatbot" + Thai line "ผู้ช่วยแพทย์อัจฉริยะ พร้อมให้คำปรึกษาสุขภาพ" → `https://doctor-chatty-bot.lovable.app`
- **NCD-Care+** — tag `Clinical AI / Research` — "Hospital-grade clinical decision support on the NCD-CIE causal inference engine (knowledge graph, what-if simulation)" + Thai line → `https://ncd-care-plus.vercel.app`
- **NCD Health+** (if Step 1 passed) — tag `Health / Research` — "Risk prediction & what-if platform — companion app to the AIiH 2026 submission" + Thai line → `https://ncd-health-plus.vercel.app`

**Research code** (chip 🔬 Research / 🎓 Workshop, links to GitHub):
- **CORTEX Memory** — `github.com/Anirach/cortex-memory` — "Self-improving cognitive memory architecture for AI agents (working/episodic/semantic/procedural memory)"
- **CORTEX × OpenClaw** — `github.com/Anirach/cortex-openclaw` — "CORTEX memory integration for OpenClaw — Context Engine, Agent Tools, REST API, MCP" + inline link "อ่านซีรีส์ OpenClaw ทั้ง 7 ตอน →" to `../blog/#series-openclaw`
- **AI-OS RAG Workshop** 🎓 — `github.com/Anirach/ai-os-rag-workshop` — "3-day bilingual workshop: AI Operating System with RAG + Knowledge Graph on a local open-source stack (MIT)"
- **RAG Second Brain** — `github.com/Anirach/rag-second-brain` — labelled "research prototype" (its own README's words)

No n8n card. No "Coming Soon" card.

- [ ] **Step 4: Verify + commit**

Tab-through + mobile width check; `check_site.py --quiet` no new failures.

```bash
git add projects/
git commit -m "phase2: add Projects page (verified-live apps + research code; n8n removed)

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>"
```

### Task 8: `news/index.html`

**Files:**
- Create: `news/index.html`

**Interfaces:**
- Produces: `/news/` URL; the 3 newest items' one-liners that Task 10's Latest strip copies verbatim.

- [ ] **Step 1: Build the page**

Hero (Default-light approved gradient, navy title): "News & Updates", Thai subline "ข่าวสารและความเคลื่อนไหว". Timeline (`.news-item` = date chip + bilingual line + optional link), newest first — content from spec §4.5, all verified:

1. **Jul 2026** — Two sole-authored Springer chapters published: *Evidence-Bound Persona Extraction with LLMs* (NLPIR 2025, LNNS 1904) and *The Persona Extraction Architecture* (AUTSYS 2025, LNNS 1979) → link both Springer pages
2. **2025–2026** — New publications: *Real-Time Mobile PM2.5 Monitoring Platform* (AUTSYS 2025) · *Dual Graph Representation for Semantic Extraction* (AUTSYS-2024 volume, Oct 2025)
3. **Dec 2025** — Program Committee member, DEFI 2025 — The Digital Economy and Fintech Innovation, VKU, Da Nang, Vietnam
4. **Nov 2024** — 📘 *Libraries in Transformation: Navigating to AI-Powered Libraries* published (Springer, Studies in Big Data 157) → `../books/`
5. **May 2024** — Invited speaker, TLC36 (36th Thailand Library Consortium): "The Transformative Impact of AI on Revolutionizing Operations in Libraries"

Below the timeline, a **Career timeline** block (spec §4.5 optional → include): Dean, Faculty of Industrial Technology and Management, KMUTNB (2012–2020) · Associate Dean for R&D (2007–2012) · Associate Dean for Academic Affairs (2004–2007) · PhD Computer Network, Liverpool John Moores University (2004) · Head of IT Department (1998–2000) · KMUTNB CIT Center — Network Administrator / System Programmer (1992–1998).

Maintenance comment at the top of the timeline markup:
`<!-- To add news: copy a .news-item, put it FIRST, then update the Latest strip on ../index.html if this item is now among the 3 newest. -->`

- [ ] **Step 2: Verify + commit**

`check_site.py --quiet` no new failures; tab-through.

```bash
git add news/
git commit -m "phase2: add News & Updates page (verified items + career timeline)

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>"
```

### Task 9: Wire the nav on the two existing nav-bearing pages + extend the linter

**Files:**
- Modify: `index.html` (nav links), `blog/index.html` (nav links + `<details>` mobile fallback replacing the dead hamburger), `.claude/skills/site-check/scripts/check_site.py`

**Interfaces:**
- Consumes: the shared nav block (Phase-2 preamble), pages from Tasks 6–8.
- Produces: INV-22 (5-page nav consistency) in the linter, used by every later task's checks.

- [ ] **Step 1: Update `index.html` nav**

Insert `Books / Projects / News` links (root-prefix form: `blog/`, `books/`, `projects/`, `news/`, `#contact` stays an anchor). Keep `#research/#about/#projects` anchors for the on-page sections BUT rename the nav anchor for the projects *section* to avoid confusion with `/projects/`: the section link text becomes "Highlights" pointing at `#projects` (the on-page grid), and "Projects" now means the `/projects/` page.

- [ ] **Step 2: Update `blog/index.html` nav**

Same link set with `../` prefix; wrap `.nav__links` in the `<details class="nav__mobile">` fallback (styles: `summary` visible ≤768px only; `details[open] .nav__links { display:flex; flex-direction:column; }`); delete the dead `<button class="nav__hamburger">` from this file.

- [ ] **Step 3: Extend `check_site.py` — INV-22 nav consistency**

Add a fail-severity check: the 5 files `index.html`, `blog/index.html`, `books/index.html`, `projects/index.html`, `news/index.html` each contain hrefs resolving to all five destinations (home, blog, books, projects, news) and every relative nav href resolves to an existing file/dir. Also register the three new pages in the link-resolution walk. Mutation-test it: break one nav href in a `/tmp` copy of the repo → check FAILs; restore.

- [ ] **Step 4: Verify + commit**

`check_site.py --quiet` → exit 0. Click every nav link on all 5 pages locally.

```bash
git add index.html blog/index.html .claude/skills/site-check/scripts/check_site.py
git commit -m "phase2: wire 5-page navigation + INV-22 nav-consistency check

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>"
```

---

## Phase 3 — Home redesign

### Task 10: Latest strip, featured book, curated projects grid

**Files:**
- Modify: `index.html`, `style.css`

**Interfaces:**
- Consumes: `images/libraries-in-transformation-cover.jpg` (Task 6), news one-liners (Task 8), live-app cards (Task 7).

- [ ] **Step 1: Latest strip (after the About section)**

```html
<section class="latest" id="latest">
  <div class="latest__inner">
    <h2 class="latest__heading">Latest <strong>updates</strong></h2>
    <ul class="latest__list">
      <li><span class="latest__date">Jul 2026</span><a href="news/">Two sole-authored Springer chapters on evidence-bound persona extraction published</a></li>
      <li><span class="latest__date">Dec 2025</span><a href="news/">Program Committee, DEFI 2025 — VKU, Da Nang</a></li>
      <li><span class="latest__date">Nov 2024</span><a href="news/">📘 Libraries in Transformation published by Springer</a></li>
    </ul>
    <a href="news/" class="btn btn--pill btn--primary">All news <span class="btn__arrow">›</span></a>
  </div>
</section>
```

CSS in `style.css`: `.latest__inner { max-width: 860px; margin: 0 auto; padding: 4rem 2.5rem; }`, list rows `display:flex; gap:1.25rem; padding:0.9rem 0; border-bottom:1px solid #e2e8f0;`, date chip `font-weight:600; color:#6366f1; min-width:90px;`. Match the section-heading pattern (`clamp(2rem, 4vw, 3.5rem)` with `<strong>`).

- [ ] **Step 2: Featured book (after Research section)**

Card: cover `<img src="images/libraries-in-transformation-cover.jpg" alt="Libraries in Transformation book cover" width="306" height="460" loading="lazy" decoding="async">` left, right column: title, "Springer · Studies in Big Data 157 · 2024", stat chips "~10,000 accesses / 68 citations", one EN + one Thai sentence, links "Read more → books/" and Springer DOI. Reuse `.about__card` visual language (white card, `--radius-lg`, soft shadow).

- [ ] **Step 3: Projects grid rework**

Replace the three existing cards with: Doctor Chatty Bot (kept, same copy), **NCD-Care+** (new: tag `Clinical AI`, EN+Thai lines from Task 7, link `https://ncd-care-plus.vercel.app`), and a third *link card* "See all projects →" to `projects/` (tag `More`, no external link). Delete the n8n card and the Coming-Soon card entirely.

- [ ] **Step 4: Verify + commit**

Serve; check reveal animation still fires on new sections (add `data-reveal` to the new cards — this is `index.html`, the one page where it works). Lint exit 0.

```bash
git add index.html style.css
git commit -m "phase3: home redesign — latest strip, featured book, curated live projects

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>"
```

---

## Phase 4 — Blog reorganization

### Task 11: Three category sections on `blog/index.html`

**Files:**
- Modify: `blog/index.html`, `.claude/skills/site-check/scripts/check_site.py` (baseline/counter awareness), `.claude/skills/blog-post/SKILL.md` + `.claude/skills/blog-post/references/known-exceptions.md` (document the new sections)

**Interfaces:**
- Produces: category anchors `#cat-technology`, `#cat-academic`, `#cat-lifestyle` that future posts' cards land under; `#series-openclaw` / `#series-devops` anchors preserved inside Technology.

- [ ] **Step 1: Restructure**

Wrap the two existing `.series-section` blocks in a category band:

```html
<div class="category" id="cat-technology">
  <div class="category__header">
    <span class="category__icon">🤖</span>
    <h2 class="category__title">Technology</h2>
    <span class="category__count">37 articles</span>
  </div>
  <!-- existing #series-openclaw and #series-devops .series-section blocks move here UNCHANGED -->
</div>

<div class="category" id="cat-academic">
  <div class="category__header">
    <span class="category__icon">🎓</span>
    <h2 class="category__title">Academic &amp; Philosophy</h2>
    <span class="category__count">First posts coming soon</span>
  </div>
  <p class="category__note">แนวคิด ปรัชญา และมุมมองทางวิชาการ — เร็ว ๆ นี้</p>
</div>

<div class="category" id="cat-lifestyle">
  <div class="category__header">
    <span class="category__icon">☕</span>
    <h2 class="category__title">Lifestyle</h2>
    <span class="category__count">First posts coming soon</span>
  </div>
  <p class="category__note">เรื่องราวชีวิต การอ่าน และสิ่งที่สนใจ — เร็ว ๆ นี้</p>
</div>
```

CSS: `.category { max-width: 1200px; margin: 0 auto 3rem; padding: 0 2.5rem; }`, `.category__header` mirrors `.series-header` but one size up (`.category__title { font-size: 1.7rem; font-weight: 800; }`); `.category__note` is a quiet single line (`color: var(--slate-light); font-size: 0.95rem;`) — NOT a fake card. Demote the two inner `.series-title` h2s to h3 (`<h3 class="series-title">`) so the ladder stays h1 → h2 (category) → h3 (series) — update the CSS selector to cover `h3.series-title` at the same size.

- [ ] **Step 2: Hero stats**

Update `.blog-hero__stats` to `<strong>3</strong> Categories · <strong>2</strong> Series · <strong>37</strong> Articles`.

- [ ] **Step 3: Update the linter + blog-post skill**

`check_site.py`: teach INV-02 to read the new markup (`category__count` for Technology = sum of its series cards; hero Articles = total cards). Mutation-test on a `/tmp` copy (set Technology count to 36 → FAIL). `blog-post/SKILL.md` Step 2 series table gains the two new categories (nav pattern: standalone until a category has ≥2 posts, then `.post-nav` chain per category); `known-exceptions.md` notes the "coming soon" sections carry 0 cards by design.

- [ ] **Step 4: Verify + commit**

`check_site.py --quiet` → exit 0. Anchors `blog/#series-openclaw` (used by Task 7's card) still resolve.

```bash
git add blog/index.html .claude/skills/
git commit -m "phase4: reorganize blog into Technology / Academic & Philosophy / Lifestyle

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>"
```

---

## Phase 5 — Polish & launch

### Task 12: Modern-CSS snippets on the existing pages

**Files:**
- Modify: `index.html`+`style.css`, `blog/index.html`, all 37 `blog/*.html` posts (append-only `<style>` addition), `script.js`
- Reference: `.claude/skills/page-design/SKILL.md` §6 (the three snippets, verbatim), `.claude/skills/a11y-perf/references/n-file-edits.md` (sweep loops)

**Interfaces:**
- Produces: sitewide keyboard focus, motion opt-out, `color-scheme`, balanced headings; `aspect-ratio` on `.post-hero__cover`.

- [ ] **Step 1: Append the three snippets** (new pages already have them from Phase 2)

To every `<style>` block in `blog/*.html` + `blog/index.html` + `style.css`, append verbatim:

```css
:focus-visible { outline: 2px solid var(--blue); outline-offset: 3px; border-radius: 2px; }
:focus:not(:focus-visible) { outline: none; }
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: .01ms !important; animation-iteration-count: 1 !important;
    transition-duration: .01ms !important; scroll-behavior: auto !important;
  }
}
:root { color-scheme: light; }
h1, h2, h3, .post-hero__title, .card__title { text-wrap: balance; }
```

(Island posts got tokens in Task 2, so `var(--blue)` resolves everywhere.) Use the verified loop from `n-file-edits.md`; proving grep after: `grep -L ':focus-visible' blog/*.html index.html` → empty.

- [ ] **Step 2: `aspect-ratio` on hero covers + `script.js` motion guard**

Add `.post-hero__cover { aspect-ratio: 16/10; }` alongside each of the 25 house declarations (skip if a file's cover art is square — check the image, use `1/1`). In `script.js`, wrap the parallax + reveal-stagger in:

```js
const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
```
— parallax: `if (!reduceMotion)` around the scroll listener registration; reveal: stagger delay `reduceMotion ? 0 : idx * 120`.

- [ ] **Step 3: Lazy-load the remaining images**

Sweep all `<img>` without `loading=` in `blog/*.html` (the card avatars and in-post images): add `loading="lazy" decoding="async"` + `width`/`height` measured via `sips -g pixelWidth -g pixelHeight`. Above-the-fold hero covers get `loading="eager" fetchpriority="high"` instead. Proving grep: `grep -c 'loading=' blog/index.html` ≥ 74.

- [ ] **Step 4: Lint + commit**

`check_site.py --quiet` → exit 0.

```bash
git add -A blog/ index.html style.css script.js
git commit -m "phase5: sitewide focus-visible, reduced-motion, color-scheme, lazy images

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>"
```

### Task 13: Final verification and launch

**Files:**
- No new files; push only.

- [ ] **Step 1: Full linter + link audit**

`python3 .claude/skills/site-check/scripts/check_site.py` (verbose) → exit 0, and `python3 .claude/skills/blog-post/assets/verify-wiring.py` → CLEAN. External probes: the 6 book retail links, 3 live-app URLs, Scholar → no 404s.

- [ ] **Step 2: Browser pass (browser MCP)**

All 5 pages at 375px and 1280px: nav works (including `<details>` mobile menu), keyboard-tab shows focus rings, no console errors, screenshots saved to `/tmp/launch-screens/`.

- [ ] **Step 3: Spec success-criteria checklist**

Walk spec §8 line by line; every criterion must check off (payload ≤4 MB, ≥4 news items, 3 categories, 37 legacy posts reachable, no `_` dirs: `find . -name '_*' -not -path './.git/*'` → empty).

- [ ] **Step 4: Push (deploys to GitHub Pages)**

```bash
git push origin main
```

Then probe production: `for p in "" blog/ books/ projects/ news/; do echo "https://anirach.com/$p → $(curl -s -o /dev/null -w '%{http_code}' https://anirach.com/$p)"; done` → five 200s (allow a few minutes for Pages build).

- [ ] **Step 5: Report**

Deliver to the owner: before/after screenshots, payload numbers, the owner-content backlog reminder (recommended books · novel decision · first Lifestyle/Academic posts).

---

## Self-review record

- **Spec coverage:** §4.1→Task 10+5, §4.2→Task 11, §4.3→Task 6, §4.4→Task 7, §4.5→Task 8, §5→global constraints + Task 13 `_`-check, §7 phases→Tasks 2–13 in order, §8→Task 13 Step 3, §9→Task 13 Step 5. Books §4.3 items 4–5 intentionally ship as HTML-comment slots (owner content pending — spec says omit, no placeholder shelf).
- **Placeholder scan:** the two HTML comments in Task 6 are spec-mandated deferred-content slots, not plan placeholders. No TBDs.
- **Type consistency:** nav block identical across Tasks 6–10 (`{PREFIX}` convention); category anchors `#cat-*` defined in Task 11 and not referenced earlier; `images/libraries-in-transformation-cover.jpg` name identical in Tasks 6 and 10; INV-22 defined in Task 9, relied on from Task 9 onward only.
