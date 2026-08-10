# Drift budget — the warn-level backlog

Open this when the user wants to pay down cosmetic inconsistency, or when you need to know whether a
warn-level violation is pre-existing. These do not block a push. Every count below was computed from
the tree; re-verify with the quoted command before repeating a number.

Baseline shape: 37 posts in `blog/`, 38 HTML files in `blog/`, 39 repo-wide, 358 internal
`href|src` refs, 50 files in `images/`. Nav partition: 7 `.series-nav` + 25 `.post-nav` + 5 no-nav.

## The pattern behind almost all of it

The 7 OpenClaw series posts (`openclaw-101`, `-agent-teams`, `-memory`, `-security`, `-integrations`,
`-skills`, `-production`) are the un-templated corner of the site. They hand-roll their own header,
their own footer, their own ordinal badge, and their own site nav — and they supply:

- all **14** broken internal links (INV-05)
- **5** of the **6** missing meta descriptions (INV-14)
- **7** of the **10** posts with no `:root` (INV-22)
- all **4** ordinal-badge markup variants (INV-20)
- the one drifted series heading (INV-03b)

Fixing them as a group is a bigger win than fixing them one at a time. Everything else in this file
is a long tail.

## Inventory

### INV-03b — series heading drift (1)
`blog/openclaw-integrations.html` heads its strip `OpenClaw for Organizations 2026 — Series
Navigation`; the other six say `📚 OpenClaw for Organizations 2026`. One-line fix.

### INV-04c — post-nav container tag (4)
`<nav class="post-nav">` instead of `<div class="post-nav">` in `claude-code-architecture.html`,
`deployment-hosting.html`, `openclaw-memory-architecture.html`, `vibe-coding-devops-process.html`.
Renders identically. Normalise only in a dedicated commit, and keep the linter matching
`<(div|nav)\s+class="post-nav">` regardless — 21 files use `div`.

### INV-04d — non-standard direction labels (2)
`blog/claude-code-architecture.html:602-609` uses `Related` / `See also` pointing at
`openclaw-101.html` and `web-architecture.html`. This is a post-nav-shaped block that belongs to no
chain — **intentional, allowlisted**. Do not convert it into `← Previous` / `Next →`; that would
splice an off-chain post into the 24-node path and break INV-04e.

### INV-06a — orphan images (9)
```bash
Opic02.jpg  bg.jpg  overlay.png  pic01.jpg  pic02.jpg  pic03.jpg  pictop.png  xpic01.jpg  xpic03.jpg
```
Leftovers from a prior HTML template. Verify with `grep -rn '<name>' blog/ index.html style.css`
before deleting — the reference scanner reads `src=`, `href=`, and `url(…)`, so a name appearing only
inside a JS string would be missed.

### INV-10 — stale `.post-nav__title` labels (8)
The nav label no longer matches the target's `.card__title`. Worst case:
`blog/devops-security.html` labels its Next target *"Linux & Shell Essentials — พื้นฐานที่ DevOps
ต้องรู้"* while the card reads *"Linux Command Line — คำสั่งพื้นฐานที่ DevOps ต้องรู้"*. Copy the card
title verbatim (HTML-escaped) rather than rewriting it.

Comparison needs `html.unescape` + whitespace collapse + emoji strip; without that, `&amp;` vs `&`
alone produces ~14 false positives.

### INV-14 — missing `<meta name="description">` (6)
`idle-self-improvement.html`, `openclaw-101.html`, `openclaw-agent-teams.html`,
`openclaw-memory.html`, `openclaw-security.html`, `openclaw-skills.html`.

```bash
for f in blog/*.html; do grep -q 'name="description"' "$f" || echo "$f"; done
```

### INV-15 — footer copyright year (3 cohorts, by literal `©`)
25 posts say `© 2025`, 4 say `© 2026`, and 8 have no literal `©` — but 5 of those 8 do carry a
copyright written as the `&copy;` entity (4× `&copy; 2026`, 1× `&copy; 2024`; see
blog-post/references/known-exceptions.md), so only 3 posts have no copyright at all. Pick one
year and one encoding before editing 37 files.

### INV-16 — footer container class (4 variants)
`<footer class="blog-footer">` ×23, `<footer class="footer">` ×7, `<footer class="post-footer">` ×3,
bare `<footer>` ×4. Each variant is styled by that page's own embedded `<style>` block, so
normalising the class also means normalising 37 CSS rules — this is the most expensive item here.
Not worth doing unless a redesign is already in flight.

### INV-17 — card section vs nav family (2)
`claude-code-architecture.html` and `openclaw-memory-architecture.html` have cards in
`#series-openclaw` but carry DevOps `.post-nav` chrome, and are the only 2 nodes unreachable from the
chain walk. `claude-code-architecture` is allowlisted (off-chain by design);
`openclaw-memory-architecture` is a genuine defect — it also causes the live INV-04a and INV-04f
failures by claiming `deployment-hosting.html` as its `prev` when that post's `next` is
`vibe-coding-devops-process.html`.

Converse checks are clean: no `#series-devops` card uses the chip strip (INV-18), and all 7 numbered
posts live in `#series-openclaw` (INV-19).

### INV-20 — ordinal badge markup (4 formats, 0 numeric errors)
| post | value | markup |
|------|-------|--------|
| openclaw-101 | Post #1 | `.series-badge` |
| openclaw-agent-teams | Post #2 | `.series-badge` |
| openclaw-memory | **บทที่ 3** | `.series-badge` |
| openclaw-security | Post #4 | `<div class="series-info">` |
| openclaw-integrations | Post #5 of 7 | bare `<p>` |
| openclaw-skills | Post #6 | `<strong>` |
| openclaw-production | Post #7 (Final) | `.series-badge` |

All seven numbers match series-nav position. Only the presentation drifts.

### INV-22 — posts with no `:root` (10)
`beyond-plugins.html`, `idle-self-improvement.html`, `openclaw-101.html`,
`openclaw-agent-teams.html`, `openclaw-integrations.html`, `openclaw-memory.html`,
`openclaw-migration.html`, `openclaw-production.html`, `openclaw-security.html`,
`openclaw-skills.html`.

Two corrections to CLAUDE.md that this check exposes:

- `style.css` has **0** `:root` blocks and **0** `var(` uses — it is plain hex literals only. The
  `--navy` / `--blue` / `--slate` / `--bg` convention lives inside `blog/` pages' embedded styles,
  not in the root stylesheet.
- `data-reveal` is inert in `blog/`. `script.js` is loaded **only** by root `index.html`; no blog
  page has a `<script>` tag at all, and `grep -o 'data-reveal' blog/index.html | wc -l` returns 0.
  Adding `data-reveal` to a blog page does nothing.

### Header variants (informational, no INV id)
26 posts carry `<nav class="blog-nav">` with exactly one link, `href="./"` — a perfectly uniform
header. The remaining 11 (the 7 series posts + `beyond-plugins`, `idle-self-improvement`,
`obsidian-ai-jarvis`, `openclaw-migration`) each hand-roll a different header, and 10 posts have no
"back to blog" link anywhere. Any new-post workflow should steer authors to the `blog-nav` template.

## Suggested order to pay it down

1. **INV-05** (14 broken links) — the only warn-adjacent item that affects readers; it is fail-level
   for a reason. One mapping table, 7 files.
2. **INV-10** (8 stale nav titles) — cheap, mechanical, visible.
3. **INV-14** (6 meta descriptions) — cheap, affects search results.
4. **INV-06a** (9 orphan images) — one delete commit.
5. **INV-03b / INV-20** — one-liners in the series posts; do them while you are already in there.
6. **INV-15 / INV-16 / INV-22** — 37-file sweeps. Only worth it alongside a redesign.
