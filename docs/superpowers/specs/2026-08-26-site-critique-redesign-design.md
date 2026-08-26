# Design: anirach.com — Critique-Driven Redesign (identity, front door, blog, islands, system)

**Date:** 2026-08-26
**Status:** Critique complete (dual-agent impeccable run, 18/36). Owner decisions 1–4 taken; the
four open decisions in §7 were delegated back and are all SETTLED 2026-08-26. Phase 1 is built and
verified locally; awaiting the owner's look before it is pushed.
**Owner:** Dr. Anirach Mingkhwan
**Supersedes nothing** — extends `2026-08-10-personal-platform-redesign-design.md` (structure stands).

## 1. Why

An `impeccable critique` of the whole site (2026-08-26, two isolated assessments: a design-director
review and a detector/browser-evidence run) scored **18/36 — Acceptable**, verdict **MIXED**: the
book pages are authored, the landing/blog/projects are a framework-default developer portfolio in a
professor's name. Measured facts behind the score, each re-verified against source before this spec
was written:

| Finding | Evidence |
|---|---|
| Landing name fails contrast | `h1.hero__name` white on `#e8f0fe→#c7d2fe`: **1.1–1.5:1** (large text needs 3:1); zero-offset glow; "MINGKHWAN" weight 400 |
| Mobile first viewport is empty | `.hero { min-height:100vh }` + portrait `margin-top:7rem` at ≤768px → ~450px of gradient before content at 375px |
| Rotated hero labels clip | "NETWORK SPECIALI" cut off at 1440×900 |
| The Last Lecture is invisible from the front door | `<title>` "Associate Professor & AI Researcher"; `#book` features the 2024 Springer volume; One Day of Light is one `.latest__list` line linking to `news/` |
| Blog is undated | 0 of 37 posts carry `<time>`; 1 post has a year in `.post-hero__meta` |
| Blog index unusable on phones | 22,875px tall at 375px; `.card__tag` at **10.88px** ×111 (`font-size: 0.68rem`); tags not links; hero counts "3 Categories" with two empty bands |
| Island posts (11) | different chrome/font/logo, header ~1,400px tall at 375px, hidden or absent mobile nav, ~10 posts with no route back to the blog |
| No Thai typeface | only `blog/openclaw-security.html` loads Noto Sans Thai; 46/47 pages render Thai in OS fallback |
| No favicon, no `og:image`, no `404.html` | `/favicon.ico` 404 on every page; 0/47 pages have og:/twitter:/canonical; a mistyped URL lands on GitHub's page |
| Not one system | 15 post-hero gradients; 6 copyright strings; landing nav 8 destinations vs 6 elsewhere; Scholar pill the only CTA on every page |

Detector noise excluded from the score (false positives on a light-themed hand-written site): 78
"side-tab" hits that are ordinary blockquote left-rules, 8 "glow on dark page" hits on pages measured
as light, 3 of 4 "buzzword" hits (an academic term, a table cell, a quoted prompt).

## 2. Decisions (settled with the owner, 2026-08-26)

| Decision | Choice |
|---|---|
| First cluster | **The front door** — hero legibility + mobile first viewport + the Last Lecture on the homepage |
| Identity | **Re-key the palette to the book covers** (amber · navy · cloud-blue), reviewed as a token proposal (§3) before any of the 47 files change |
| Homepage during the event window (until 19 Sep 2026) | **One Day of Light replaces the Springer feature** — cover pair, one Thai + one English line, Download PDF + Reserve a seat; Springer returns after the event |
| Scope | **All five priority issues**, sequenced (§5), each reviewed before it goes live |

Standing rules that still bind (from the 2026-08-10 spec and CLAUDE.md): no build step, no framework,
no JavaScript outside `index.html`, every page self-contained, `check_site.py` green before every
push, counters recomputed never incremented, the four project skills authoritative over any
third-party skill, and **the owner reviews before large diffs land** (memory:
site-modernization-direction).

## 3. Identity: the token proposal

Colours are sampled from the covers on disk (`images/*-cover-*.jpg`), not invented. Every text role
below is WCAG-checked on every ground it can sit on; numbers are computed, not estimated.

### 3.1 Sources

| Cover | Dominant | Title / accent |
|---|---|---|
| One Day of Light | cream paper `#faf7f0` · cloud `#dee7e6` · parchment `#e9e1c4` | title navy `#141826`, title amber `#c4a46c` |
| Three Old Men (printed jacket) | white · navy `#11304b` · blue `#226299` · sky `#4992b9` | gold lettering `#ffc614` |
| A Pocketful of Questions | dusk navy `#1f2540` · dusk gold `#eecf97` | — |
| The Thirteenth Seal | charcoal `#0d0e13`–`#1b1d23` | red cell |

### 3.2 The canonical `:root` — SHIPPED (28 tokens; was 24 — `--focus` added by the §7.4 corrections)

Changed values are marked. Unchanged tokens keep their measured contrast history.

```css
:root {
  color-scheme: light;
  /* ink */
  --navy: #11304b;          /* was #0f172a — Three Old Men's ink. 12.7:1 on cream */
  --slate: #334155;         /* unchanged — 9.7:1 on cream */
  --slate-light: #526174;   /* was #64748b, which drops to 4.45:1 on cream — 5.9:1 cream, 5.0 cloud, 4.8 parchment */
  --gray: #94a3b8;          /* unchanged — 5.3:1 on the new navy (footer meta) */
  /* ground */
  --bg: #faf7f0;            /* was #f8fafc — the book's paper */
  --white: #ffffff;
  --code-bg: #1e293b;       /* unchanged */
  /* accent */
  --blue: #226299;          /* was #6366f1 (4.47:1 FAIL as text) — 6.4 white · 6.0 cream · 4.9 parchment: passes as small text everywhere */
  --blue-dark: #1a4d7a;     /* was #4f46e5 — hover/pressed; 8.8:1 on white, white-on-it 8.8:1 */
  --blue-light: #4992b9;    /* was #818cf8 — borders and large text only (3.45:1 on white; 3.9 on navy) */
  /* brand (new) — never a seventh status colour; --amber stays the warning status */
  --gold: #c4a46c;          /* One Day of Light's title amber — rules, marks, chip grounds, the motto spark; NEVER small text (2.2:1) */
  --gold-dark: #7a5f22;     /* the text-safe gold — eyebrows, labels; 5.6:1 on cream */
  --cloud: #dee7e6;         /* hero ground */
  --parchment: #e9e1c4;     /* hero ground, warm end */
  /* status — unchanged, use only these six */
  --green: #22c55e; --red: #ef4444; --amber: #f59e0b;
  --cyan: #06b6d4; --purple: #8b5cf6; --purple-dark: #7c3aed;
  /* type */
  --font: 'Inter', 'Sarabun', -apple-system, BlinkMacSystemFont, sans-serif;  /* §7.1 settled: Sarabun */
  --mono: 'JetBrains Mono', 'Fira Code', 'Sarabun', monospace;  /* Thai in <code> fell to Courier New on 34 pages */
  /* form — unchanged */
  --radius: 12px; --radius-sm: 8px; --radius-lg: 16px;
  --measure: 720px; --wide: 860px;
  --transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
```

### 3.3 Contrast table (computed 2026-08-26)

| Pair | Ratio | Verdict |
|---|---|---|
| navy `#11304b` on cream / cloud / parchment / white | 12.68 / 10.77 / 10.36 / 13.56 | text everywhere |
| slate `#334155` on cream | 9.68 | body text |
| slate-light `#526174` on cream / white / cloud / parchment | 5.91 / 6.32 / 5.02 / 4.83 | secondary text everywhere |
| blue `#226299` on white / cream / cloud / parchment | 6.41 / 5.99 / 5.09 / 4.90 | links, chips, small text everywhere |
| white on blue `#226299` | 6.41 | button text (also the lightest stop of the deep gradient) |
| white on blue-dark `#1a4d7a` | 8.80 | hover button |
| gold-dark `#7a5f22` on cream | 5.63 | eyebrow / label text |
| gold `#c4a46c` on navy `#11304b` | 5.73 | footer links on the navy footer |
| gray `#94a3b8` on navy `#11304b` | 5.29 | footer meta |
| gold `#c4a46c` on cream | 2.21 | **decorative only** |
| blue-light `#4992b9` on white / navy | 3.45 / 3.94 | **borders only** — its 32 former text uses moved to `--gold` |
| focus ring `#226299` on navy `#11304b` | 2.12 | why `--focus` is re-pointed to gold inside footers |

### 3.4 Gradients (the five approved families, re-keyed)

| Family | Was | Proposed | Text on it |
|---|---|---|---|
| Default / light (landing hero, blog index, 11 DevOps posts) | `#e8f0fe → #ddd6fe → #c7d2fe` | `linear-gradient(160deg, #eef3f3 0%, #dee7e6 45%, #e9e1c4 100%)` — the sunrise | navy ≥ 10.4:1 |
| Indigo deep (security/auth, publications hero) | `#1e1b4b → #312e81 → #3730a3` | `linear-gradient(135deg, #11304b 0%, #1a4d7a 45%, #226299 100%)` | white ≥ 6.4:1 at the lightest stop |
| Emerald (books identity, 2 posts) | unchanged in Phase 1 | decide in Phase 4 (§5) — candidates: keep, or dusk-navy `#1f2540 → #383d55` from the Pocketful cover | — |
| Violet (OpenClaw series) | unchanged in Phase 1 | decide in Phase 4 | — |
| Teal (SRE) | unchanged in Phase 1 | decide in Phase 4 | — |

### 3.5 Typography

Inter stays for Latin (house; 26 house posts + all listing/detail pages already load it). Add a Thai
face to every Google Fonts `<link>` and to `--font` so Thai prose stops falling to whichever OS
face the reader has. Choice pending §7.1 — the plan defaults to **Sarabun 400/600/700** (looped,
the Thai standard, best for long prose) with **Noto Sans Thai** as the loopless alternative.

### 3.6 Literals that must follow the tokens

Tokens are declared per file but many colours are written as literals. The sweep (Plan 1, Task 3)
replaces these everywhere outside `:root`, by census, not by memory:

| Literal | Occurrences (to be re-counted at sweep time) | Becomes |
|---|---|---|
| `#6366f1` | text/border/shadow uses | `var(--blue)` where it is a colour role; `#226299` inside gradients |
| `rgba(99,102,241,` | card shadows, chip grounds, borders | `rgba(34,98,153,` |
| `#4f46e5` / `rgba(79,70,229,` | hover states | `#1a4d7a` / `rgba(26,77,122,` |
| `#818cf8` | footer links, light accents | `var(--gold)` on the navy footer; `#4992b9` elsewhere |
| `#4338ca` (light-hero label) | a11y-perf R4 substitution | `var(--blue-dark)` — the new default hero ground no longer needs the special case |
| `#e8f0fe 0%, #ddd6fe 50%, #c7d2fe 100%` (and the 40%-stop fork if it reappears) | the default family | §3.4 default |

## 4. Front door (Phase 1) — what changes on `index.html` / `style.css`

- **Hero**: ground = default gradient (§3.4); `.hero__name` in `var(--navy)`, no text-shadow;
  `.hero__name--light` weight 500; watermark `.hero__bg-text` in `rgba(17,48,75,0.05)`; rotated
  labels re-worded to what is true *now* — `Associate Professor · Author` and `The Last Lecture ·
  19 September 2026` — and constrained (`max-width: calc(100vh - 14rem)`) so they can never clip;
  at ≤768px `min-height: auto`, portrait `margin-top: 1.5rem`, so portrait + name land in the first
  viewport.
- **Featured**: `#book` becomes One Day of Light — cover pair (EN + TH), label `☀️ For the Last
  Lecture · 19 September 2026`, title with Thai, one English and one Thai line (the approved
  `books/index.html` card excerpts), buttons: **Download — English PDF (2.6 MB)** · **ดาวน์โหลด
  ฉบับภาษาไทย (2.5 MB)** · **Reserve a seat →** (the verified Google Form), and a quiet link
  *About the book →*. One line beneath keeps the Springer volume reachable: *Academic: Libraries in
  Transformation (Springer, 2024) →* to `publications/`.
- **Head**: `<title>` → `Anirach Mingkhwan — Professor, Author · One Day of Light`; description
  rewritten; favicon (§4.1); social metadata (§4.2).
- **Latest strip**: untouched (news gate SYNC).

### 4.1 Favicon
`favicon.svg` at the repo root: navy `#11304b` rounded square, a gold `#c4a46c` half-disc rising
from a horizon line — the One Day of Light sun. Linked from all 47 pages (`<link rel="icon"
type="image/svg+xml" href="/favicon.svg">` — absolute path, works from every directory).

### 4.2 Social metadata
`images/og-default.jpg` (1200×630): the two One Day of Light covers on cream — no text, so no font
dependency. `og:title`, `og:description`, `og:image`, `og:url`, `twitter:card=summary_large_image`
and `<link rel="canonical">` on the 11 nav-bearing/detail pages (`index.html`, 5 section indexes,
4 `books/` detail pages, plus `404.html` gets no og). Canonical policy: **extensionless for the
blog series that already relies on it; `.html` everywhere else** — exactly the URLs the site links
today. Posts get canonical + og in Phase 2 with their dates.

### 4.3 `404.html`
A house LISTING-chrome page (copy `news/index.html` chrome): "Page not found · ไม่พบหน้านี้", the six
nav destinations as a list, and the search-free hint "Blog posts live under /blog/". GitHub Pages
serves a root `404.html` automatically.

## 5. Phases (each is its own plan file; each ends reviewed, gated, pushed)

| Phase | Plan | Scope | Files | Gate |
|---|---|---|---|---|
| 1 — Front door + tokens | `plans/2026-08-26-phase-1-front-door.md` | §3 tokens into all 47 `:root` blocks (byte-identical → scripted) + literal census; hero; featured ODL; favicon; social meta; 404 | `style.css`, `index.html`, 46 `:root` blocks, 11 heads, `favicon.svg`, `404.html`, `images/og-default.jpg`, skills | check_site green; news gate PASS; browser: name ≥ 4.5:1 measured, first viewport at 375 shows portrait+name; re-critique of `index.html` |
| 2 — Blog on phones | `plans/…-phase-2-blog-mobile.md` | dates on 37 cards + 37 heroes (derived from git first-commit, owner confirms the list); `.card__tag` ≥ 0.75rem; `card--row` at ≤768px; two-link jump bar; empty bands per §7.3; posts get canonical + og | `blog/index.html`, 37 posts | INV-02 counters; 375px height ≤ 40% of today |
| 3 — Islands → house | `plans/…-phase-3-islands.md` | 11 posts converted with `page-design/assets/post-template.html`; `obsidian-ai-jarvis` first; content byte-preserved | 11 posts | INV-04/09/26; mobile nav works on all 37 |
| 4 — One system | `plans/…-phase-4-system.md` | Thai face on 47 pages; one gradient per family (§3.4 decisions); one footer string and year; section CTAs (books → Download the book); ODL page ends on motto + downloads; sticky cover column | 47 files | gradient census = 5 rows; footer census = 1 |
| 5 — Verify | inline | full `impeccable critique` re-run; a11y-perf tables re-measured; skills re-counted per the standing rule | skills, CLAUDE.md | target ≥ 27/36 (75%, "Good") |

## 6. Success criteria

- Landing: `h1.hero__name` computed contrast ≥ 4.5:1 at both widths; first viewport at 375×812
  contains portrait and full name; no clipped label at 1440×900, 1280×720, 1024×768.
- Every page: favicon resolves; `og:image` present on the 11 pages; `404.html` served.
- Palette: `grep -c '#6366f1\|rgba(99,102,241'` across the tree → **0** outside comments.
- `:root` uniformity diff (page-design §1 command) → no output, 47/47.
- Both gates green; no new baseline entries; live URLs 200 after push.
- Re-critique ≥ 27/36 after Phase 4; ≥ 22/36 after Phase 1 alone.

## 7. Open owner decisions (asked 2026-08-26)

1. **Thai typeface** — SETTLED 2026-08-26: **Sarabun**, measured rather than argued. In Chrome the
   mixed-line box is *identical* for Inter-only, Inter+Sarabun and Inter+Noto at every line-height
   the site uses (30.59px at 17px/1.8), because the site sets unitless line-heights everywhere —
   so the "metric compatibility" criterion is a tie at zero, and the categorical difference decides
   it: Noto Sans Thai is loopless (ไม่มีหัว), a display idiom in Thailand, while Thai long-form body
   convention is looped. Added to 39 pages (`Sarabun:wght@400;600;700`) and to BOTH token stacks.
   `--mono` needed it too: 34 pages set Thai inside `<code>`, which was falling back to Courier New.
   The 10 island posts load no webfont at all and are deferred to Phase 3 with the rest of their
   conversion — ~40,500 Thai characters there still render in OS fallback until then.
2. **The books section's name** — SETTLED 2026-08-26: **Books**, everywhere (nav, `<title>`,
   `<h1>`, `og:title`, the 404 card, the four detail pages' back link). *Novels* was false of the
   flagship — One Day of Light is a last-lecture companion booklet, not fiction — and *Fiction*
   fails the same test. The index's hero eyebrow is deleted rather than reworded: no other section
   index has one, and after the rename it duplicated the `<h1>` verbatim. The `.books-hero__label`
   CSS stays, because the four detail pages use it for status text. 25 lines across 12 files;
   no gate reads nav anchor text, so `grep -rn 'Novels'` returning nothing IS the test.
3. **Empty blog categories** — SETTLED 2026-08-26: **both bands deleted, and the "Categories" hero
   stat deleted with them** (a lone "1 Categories" reads worse than silence). The placeholders had
   sat 16 days with nothing able to expire them while the hero counted them as real. The linter got
   *stricter*, not looser, and no check was removed: INV-02d now fails on any empty band at all
   (was: "an empty band must carry the label 'First posts coming soon'"), and INV-02e became
   optional-but-verified (absent is fine; present must recompute). Both were fault-injected to
   prove they still fail. Trade-off accepted: the first Academic/Lifestyle post must ship its band,
   grid, card and count in one commit.
4. **Token proposal §3.2** — SETTLED 2026-08-26: **approved with corrections** after an adversarial
   pass recomputed all 21 ratios (all correct, max Δ 0.005) and then traced the tokens into their
   real roles, which found two regressions the palette alone would have shipped:
   - **`--blue-light` had no border uses at all** — all 32 uses were footer link text on the navy
     ground, which the new navy would have dropped to 3.94:1 (FAIL). Fixed by selector:
     `.footer a, .blog-footer a { color: var(--gold) }` = 5.73:1, measured live.
   - **The focus ring failed inside footers** — `outline-offset: 3px` lands it on the page ground,
     where the new blue on the new navy is 2.12:1 (FAIL SC 1.4.11). Fixed with a 28th token,
     `--focus`, scoped: `.footer, .blog-footer, pre { --focus: var(--gold) }`.
   Also added to the sweep: a full hue map (the spec's literal list missed `#0f172a` ×62,
   `#f8fafc` ×23, `#64748b` ×9, `rgba(15,23,42,` ×22 and the whole periwinkle family in
   `style.css`, which the canonical-gradient rule could not see), two gradients that would have
   collapsed into a dead flat band once two of their stops mapped to the same value, and three
   files the spec never listed: `404.html` and the two skill asset templates.

## 8. Out of scope

Dark mode (unblocked; a Phase 6 candidate now that `color-expert` and `dark-mode-design-expert`
are installed), search/RSS, a real research-arc rewrite of the landing grid (content is the
owner's), converting the two shared blog covers.
