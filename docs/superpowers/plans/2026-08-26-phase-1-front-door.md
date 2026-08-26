# Phase 1 — Front Door & Identity Re-key: Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the front door legible, personal and current — re-key the palette to the book covers, fix the hero's failing contrast and empty mobile viewport, feature *One Day of Light* for the event window, and give all 47 pages a favicon, social preview and a real 404.

**Architecture:** Hand-written static HTML/CSS, no build step. Every page embeds its own `<style>` and its own `:root`, so a "global" colour change is a **token-value substitution across 48 files** (47 HTML + `style.css`), applied by script and verified by census — never a block rewrite, which would destroy per-file indentation and the two minified blocks. Only `index.html` has JavaScript, and that stays true.

**Tech Stack:** HTML5/CSS3, one vanilla-JS file (`script.js`, landing only), Python 3 stdlib for the sweep and the linter, macOS `sips`/Pillow for images, GitHub Pages.

**Spec:** `docs/superpowers/specs/2026-08-26-site-critique-redesign-design.md` — authoritative for tokens, contrast numbers, and the phase list. Read §3 before Task 1 and §4 before Tasks 2–5.

## Global Constraints

- **Owner review gate:** Task 1 ends by *stopping* for the owner's approval of the palette on real screenshots. Do not proceed to Task 2 until they approve (memory: `site-modernization-direction` — "review before applying to live site").
- Every task starts with `python3 .claude/skills/site-check/scripts/check_site.py` (record `N new, M known`) and ends with the same command showing **no new** fail-severity violation.
- Every task that touches `news/`, `books/index.html`, `publications/`, or `index.html`'s Latest strip also runs `python3 docs/openclaw/check-news-sync.py` → PASS.
- No JavaScript may be added to any file except `index.html`. `grep -rl "<script" --include="*.html" --exclude-dir=.claude .` must return exactly `index.html`.
- No new file or directory starting with `_` or `.` in the published tree.
- Images: covers ≤200 KB; JPG for photographic, PNG/SVG for flat art. `og-default.jpg` ≤300 KB (it is not a cover; it is a social card).
- All `<img>` keep `alt`, `width`, `height`, `loading`, `decoding` — currently **137/137**; that number must not drop.
- Contrast floor: 4.5:1 for text under 24px, 3:1 for ≥24px or bold ≥18.66px. Every colour introduced here is pre-computed in spec §3.3; do not invent a value that is not in that table.
- The 37 post URLs never change. Counters are recomputed, never incremented.
- Commits: one per task, message prefixed `Phase 1:`, ending with `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>`.
- Before any HTML/CSS edit, read `.claude/skills/page-design/SKILL.md` §0–§5 and `.claude/skills/a11y-perf/SKILL.md` rules 1–8. **House skills win every conflict with a third-party skill.**

---

## File Structure

| File | Responsibility in this phase |
|---|---|
| `scripts/retoken.py` *(new, repo-internal)* | The one-shot token+literal sweep and its `--verify` census. Lives in a new top-level `scripts/` dir, added to `_config.yml` excludes so it never publishes. |
| `style.css` | Landing-page CSS + the canonical `:root`. Hero rules change here. |
| `index.html` | Hero markup/copy, the featured card, head metadata. |
| 46 HTML files with an embedded `:root` | Token values only (scripted). No hand edits. |
| `favicon.svg` *(new, root)* | Site icon, linked from all 47 pages. |
| `images/og-default.jpg` *(new)* | 1200×630 social card. |
| `404.html` *(new, root)* | Not-found page in LISTING chrome. |
| `docs/superpowers/specs/2026-08-26-site-critique-redesign-design.md` | The spec; amended only if the owner changes a token. |
| `.claude/skills/{page-design,a11y-perf}/**`, `CLAUDE.md` | Re-measured counts and the new palette (standing rule). |

---

## Task 1: Re-key the palette across all 48 files

**Files:**
- Create: `scripts/retoken.py`
- Modify: `style.css` (`:root` + literals), 46 HTML files with an embedded `:root`, `_config.yml`
- Verify: `.claude/skills/site-check/scripts/check_site.py`

**Interfaces:**
- Produces: the 27-token canonical `:root` of spec §3.2 in all 47 blocks, and zero surviving old-palette literals. Later tasks assume `var(--navy)`, `var(--gold)`, `var(--gold-dark)`, `var(--cloud)`, `var(--parchment)` exist everywhere.
- Consumes: nothing.

- [ ] **Step 1: Record the baseline**

```bash
python3 .claude/skills/site-check/scripts/check_site.py | tail -3
python3 docs/openclaw/check-news-sync.py | tail -1
git status --porcelain
```
Expected: `0 new, 55 known` · `PASS` · clean tree (an untracked `__pycache__` is fine; add it to `.gitignore` in Step 9).

- [ ] **Step 2: Record the pre-sweep census — these are the numbers the sweep must drive to zero**

```bash
for pat in '#6366f1' 'rgba(99,102,241' '#4f46e5' '#818cf8' '#4338ca'; do
  printf '%-20s %s\n' "$pat" "$(grep -rho --include='*.html' --include='*.css' -F "$pat" index.html style.css blog books publications projects news | wc -l | tr -d ' ')"
done
```
Expected (2026-08-26): `#6366f1 77` · `rgba(99,102,241 373` · `#4f46e5 94` · `#818cf8 52` · `#4338ca 4`. If these differ, the tree moved — re-derive and note the new numbers in the commit message.

- [ ] **Step 3: Write the sweep script**

Create `scripts/retoken.py`:

```python
#!/usr/bin/env python3
"""One-shot palette re-key for anirach.com (spec 2026-08-26 §3).

Substitutes TOKEN VALUES in place — never rewrites a :root block — so each
file keeps its own indentation and the two minified blocks
(blog/openclaw-memory-architecture.html, blog/vibe-coding-devops-process.html)
stay minified. Then rewrites the old-palette literals that live outside :root.

Usage:
    python3 scripts/retoken.py --dry-run     # report only, touch nothing
    python3 scripts/retoken.py --apply       # rewrite files
    python3 scripts/retoken.py --verify      # census: must print all zeros
"""
import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

TARGETS = ["index.html", "style.css", "blog/*.html", "books/*.html",
           "publications/index.html", "projects/index.html", "news/index.html"]

# --- 1. token values: name -> (old, new) ------------------------------------
TOKENS = {
    "--navy":        ("#0f172a", "#11304b"),
    "--slate-light": ("#64748b", "#526174"),
    "--bg":          ("#f8fafc", "#faf7f0"),
    "--blue":        ("#6366f1", "#226299"),
    "--blue-dark":   ("#4f46e5", "#1a4d7a"),
    "--blue-light":  ("#818cf8", "#4992b9"),
}
# --- 2. tokens to ADD after --blue-light's declaration ----------------------
NEW_TOKENS = [("--gold", "#c4a46c"), ("--gold-dark", "#7a5f22"),
              ("--cloud", "#dee7e6"), ("--parchment", "#e9e1c4")]

# --- 3. literals outside :root ---------------------------------------------
LITERALS = [
    # the default hero gradient (11 uses) -> the sunrise
    ("#e8f0fe 0%, #ddd6fe 50%, #c7d2fe 100%", "#eef3f3 0%, #dee7e6 45%, #e9e1c4 100%"),
    # the deep indigo family -> deep blue
    ("#1e1b4b 0%, #312e81 40%, #3730a3 100%", "#11304b 0%, #1a4d7a 45%, #226299 100%"),
    ("rgba(99,102,241,", "rgba(34,98,153,"),
    ("rgba(99, 102, 241,", "rgba(34, 98, 153,"),
    ("rgba(79,70,229,", "rgba(26,77,122,"),
    ("#4338ca", "#1a4d7a"),
    ("#6366f1", "#226299"),
    ("#4f46e5", "#1a4d7a"),
    ("#818cf8", "#4992b9"),
]

ROOT_RE = re.compile(r":root\s*\{.*?\}", re.S)


def files():
    seen = []
    for pat in TARGETS:
        seen.extend(sorted(ROOT.glob(pat)))
    return seen


def retoken_root(block: str) -> tuple[str, int]:
    """Replace token values inside one :root block; append the new tokens."""
    n = 0
    for name, (old, new) in TOKENS.items():
        # matches "--navy: #0f172a" and "--navy:#0f172a"
        pat = re.compile(r"(" + re.escape(name) + r"\s*:\s*)" + re.escape(old) + r"\b")
        block, k = pat.subn(lambda m: m.group(1) + new, block)
        n += k
    if "--gold" not in block:
        anchor = re.search(r"(--blue-light\s*:\s*#[0-9a-fA-F]{6};)", block)
        if anchor:
            minified = "\n" not in block.split("{", 1)[1].strip()[:80]
            sep = "" if minified else "\n      "
            add = "".join(f"{sep}{k}: {v};" if not minified else f"{k}:{v};"
                          for k, v in NEW_TOKENS)
            block = block[:anchor.end()] + add + block[anchor.end():]
            n += len(NEW_TOKENS)
    return block, n


def process(text: str) -> tuple[str, int, int]:
    root_hits = 0
    m = ROOT_RE.search(text)
    if m:
        new_block, root_hits = retoken_root(m.group(0))
        text = text[:m.start()] + new_block + text[m.end():]
    lit_hits = 0
    # protect the :root block from the literal pass: split it out, patch the rest
    m = ROOT_RE.search(text)
    head, block, tail = (text[:m.start()], m.group(0), text[m.end():]) if m else (text, "", "")
    for old, new in LITERALS:
        for part_i, part in enumerate((head, tail)):
            k = part.count(old)
            if k:
                lit_hits += k
                if part_i == 0:
                    head = head.replace(old, new)
                else:
                    tail = tail.replace(old, new)
    return head + block + tail, root_hits, lit_hits


def verify() -> int:
    stale = {}
    for f in files():
        t = f.read_text(encoding="utf-8")
        for pat in ("#6366f1", "rgba(99,102,241", "rgba(99, 102, 241",
                    "#4f46e5", "#818cf8", "#4338ca", "#0f172a", "#f8fafc", "#64748b"):
            c = t.count(pat)
            if c:
                stale.setdefault(pat, []).append(f"{f.relative_to(ROOT)}:{c}")
    for pat, where in sorted(stale.items()):
        print(f"STALE {pat}: {', '.join(where)}")
    print("clean" if not stale else f"{len(stale)} stale pattern(s)")
    return 0 if not stale else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--verify", action="store_true")
    a = ap.parse_args()
    if a.verify:
        return verify()
    tot_r = tot_l = 0
    for f in files():
        t = f.read_text(encoding="utf-8")
        new, r, l = process(t)
        tot_r += r
        tot_l += l
        if r or l:
            print(f"{f.relative_to(ROOT)}: {r} token value(s), {l} literal(s)")
            if a.apply:
                f.write_text(new, encoding="utf-8")
    print(f"TOTAL: {tot_r} token values, {tot_l} literals across {len(files())} files")
    if not a.apply:
        print("(dry run — nothing written)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Dry-run and read the report**

Run: `python3 scripts/retoken.py --dry-run | tail -5`
Expected: every file listed, `TOTAL: ~470 token values, ~600 literals across 48 files`, ending `(dry run — nothing written)`. If any `blog/*.html` reports `0 token value(s)`, its `:root` did not match — stop and inspect that file before applying.

- [ ] **Step 5: Apply, then verify the census is zero**

```bash
python3 scripts/retoken.py --apply | tail -3
python3 scripts/retoken.py --verify
```
Expected: `--verify` prints `clean`. Any `STALE` line names the file and count — fix it by hand and re-verify before continuing.

- [ ] **Step 6: Prove the 47 `:root` blocks are still uniform**

```bash
python3 - <<'PY'
import re, pathlib
vals = {}
for f in list(pathlib.Path('.').glob('blog/*.html')) + list(pathlib.Path('.').glob('books/*.html')) + \
         [pathlib.Path(p) for p in ('style.css','publications/index.html','projects/index.html','news/index.html')]:
    m = re.search(r':root\s*\{.*?\}', f.read_text(encoding='utf-8'), re.S)
    if not m: continue
    for name, v in re.findall(r'(--[a-z0-9-]+)\s*:\s*([^;]+);', m.group(0)):
        vals.setdefault(name, {}).setdefault(v.strip(), []).append(str(f))
bad = {k: v for k, v in vals.items() if len(v) > 1}
print("tokens:", len(vals), "| blocks:", max(len(w) for v in vals.values() for w in v.values()))
for k, v in bad.items(): print("DIVERGENT", k, {vv: len(w) for vv, w in v.items()})
print("uniform" if not bad else "NOT UNIFORM")
PY
```
Expected: `tokens: 27` … `uniform`.

- [ ] **Step 7: Exclude `scripts/` from the published site**

In `_config.yml`, add `  - scripts     # one-shot maintenance scripts (internal)` under `exclude:`.

Run: `grep -A4 '^exclude:' _config.yml`
Expected: three entries — `docs`, `CLAUDE.md`, `scripts`.

- [ ] **Step 8: Run both gates**

```bash
python3 .claude/skills/site-check/scripts/check_site.py | tail -2
python3 docs/openclaw/check-news-sync.py | tail -1
```
Expected: `0 new, 55 known` (unchanged from Step 1) and `PASS`.

- [ ] **Step 9: Screenshot the palette on five representative pages, both widths**

```bash
(python3 -m http.server 8140 >/dev/null 2>&1 &) ; sleep 1
```
Then, with the Playwright browser, capture `/`, `/blog/`, `/books/`, `/books/one-day-of-light.html`, `/blog/api-request-lifecycle.html` at 1440×900 and 375×812 into `.playwright-mcp/retoken-<page>-<width>.png`. Sample the computed contrast of `.card__read`, `.card__tag`, body text and any `.btn--primary` on each; every value must clear its floor from spec §3.3.

Also add `__pycache__/` to `.gitignore` if absent.

Stop the server: `pkill -f 'http.server 8140'`.

- [ ] **Step 10: Commit**

```bash
git add scripts/retoken.py _config.yml .gitignore style.css index.html blog books publications projects news
git commit -m "Phase 1: re-key the palette to the book covers (47 :root blocks + literals)

Tokens per spec 2026-08-26 §3.2: --navy #11304b, --bg #faf7f0,
--blue #226299, --blue-dark #1a4d7a, --blue-light #4992b9,
--slate-light #526174, plus --gold/--gold-dark/--cloud/--parchment.
Applied by scripts/retoken.py (value substitution, not block rewrite,
so the two minified :root blocks stay minified). Old-palette literal
census driven to zero; 27 tokens uniform across 47 blocks.

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

- [ ] **Step 11: STOP — owner review gate**

Present the ten screenshots side by side with the pre-sweep look and ask the owner to approve the palette before Task 2. **Do not push and do not start Task 2 until they answer.** If they reject a value, amend spec §3.2, re-run `--apply` with the corrected `TOKENS`, and re-verify from Step 5.

---

## Task 2: Fix the hero — legibility and the empty mobile viewport

**Files:**
- Modify: `style.css:144-235` (hero block), `style.css:692-698` (≤768px hero block), `index.html:hero section`

**Interfaces:**
- Consumes: `var(--navy)`, `var(--cloud)`, `var(--parchment)` from Task 1.
- Produces: a hero whose `h1` measures ≥ 4.5:1 and whose first 375×812 viewport contains portrait and full name.

- [ ] **Step 1: Record the failing measurement**

Serve the site (`python3 -m http.server 8140`), open `/` at 1440×900, and run in the browser:

```js
(() => {
  const el = document.querySelector('.hero__name');
  const cs = getComputedStyle(el);
  return { color: cs.color, shadow: cs.textShadow, weight: cs.fontWeight,
           heroMinH: getComputedStyle(document.querySelector('.hero')).minHeight };
})()
```
Expected (the defect): `color: rgb(255,255,255)`, a non-`none` `textShadow`, `minHeight: 100vh`.

- [ ] **Step 2: Rewrite the hero rules in `style.css`**

Replace the `.hero`, `.hero__bg-text`, `.hero__labels`, `.hero__name` and `.hero__name--light` declarations with:

```css
.hero {
  position: relative;
  min-height: 100vh;
  display: flex; flex-direction: column;
  align-items: center; justify-content: flex-end;
  /* the sunrise: cloud -> parchment, the One Day of Light cover's own light */
  background: linear-gradient(160deg, #eef3f3 0%, var(--cloud) 45%, var(--parchment) 100%);
  overflow: hidden;
  padding-bottom: 4rem;
}
.hero__bg-text {
  position: absolute;
  top: 50%; left: 50%;
  transform: translate(-50%, -55%);
  font-size: clamp(6rem, 18vw, 22rem);
  font-weight: 900;
  letter-spacing: -0.03em;
  color: rgba(17,48,75,0.05);      /* navy at 5% — a watermark, not text */
  white-space: nowrap;
  pointer-events: none;
  user-select: none;
  z-index: 1;
}
.hero__labels {
  position: absolute;
  left: 3rem; top: 50%;
  transform: translateY(-50%) rotate(-90deg);
  transform-origin: left center;
  display: flex; gap: 0.5em;
  /* the rotated strip is as long as the viewport is tall; cap it so it can
     never clip mid-word (it read "NETWORK SPECIALI" at 1440x900) */
  max-width: calc(100vh - 14rem);
  overflow: hidden;
  white-space: nowrap;
  z-index: 5;
}
.hero__name {
  font-size: clamp(3.5rem, 9vw, 8.5rem);
  font-weight: 900;
  line-height: 0.92;
  letter-spacing: -0.03em;
  color: var(--navy);              /* was #fff on lavender: 1.1:1 */
  text-shadow: none;
  text-wrap: balance;
}
.hero__name--light {
  font-weight: 500;                /* was 400 — 900/400 read as two different names */
  letter-spacing: -0.01em;
  color: var(--slate);             /* 9.7:1 on the light end of the gradient */
}
```

- [ ] **Step 3: Fix the mobile hero in the ≤768px block**

Replace the four hero lines inside `@media (max-width: 768px)` with:

```css
  /* Hero — the phone's first viewport must hold the portrait AND the name.
     100vh + a 7rem portrait offset put ~450px of empty gradient above the fold. */
  .hero { min-height: auto; padding-top: 6rem; padding-bottom: 3rem; }
  .hero__labels { display: none; }
  .hero__portrait { width: 70vw; margin-top: 1.5rem; }
  .hero__name { font-size: clamp(2.5rem, 12vw, 5rem); }
  .hero__name-row { margin-top: -1.5rem; }
```

- [ ] **Step 4: Update the hero labels to what is true now**

In `index.html`, replace the four `.hero__label` spans with:

```html
      <span class="hero__label">Associate Professor ·</span>
      <span class="hero__label hero__label--bold">Author</span>
      <span class="hero__label">· The Last Lecture ·</span>
      <span class="hero__label hero__label--bold">19 September 2026</span>
```

- [ ] **Step 5: Measure the fix**

Reload `/` at 1440×900 and run:

```js
(() => {
  const lum = h => { const c = h.match(/\d+/g).map(n => n/255).map(v => v <= .03928 ? v/12.92 : ((v+.055)/1.055)**2.4);
    return .2126*c[0] + .7152*c[1] + .0722*c[2]; };
  const el = document.querySelector('.hero__name');
  const fg = lum(getComputedStyle(el).color);
  const bg = lum(getComputedStyle(document.querySelector('.hero')).backgroundColor.startsWith('rgba(0, 0, 0, 0)')
      ? 'rgb(222,231,230)' : getComputedStyle(document.querySelector('.hero')).backgroundColor);
  const cr = (Math.max(fg,bg)+.05)/(Math.min(fg,bg)+.05);
  const lbl = document.querySelector('.hero__labels').getBoundingClientRect();
  return { contrast: +cr.toFixed(2), labelsFitOnScreen: lbl.top >= 0 && lbl.bottom <= innerHeight };
})()
```
Expected: `contrast` ≥ 10 (navy on cloud is 10.77:1 — the gradient midpoint), `labelsFitOnScreen: true`.

Then at 375×812, confirm the portrait's bottom and the full `h1` are both above 812px:

```js
(() => { const p = document.querySelector('.hero__portrait').getBoundingClientRect();
  const n = document.querySelector('.hero__name').getBoundingClientRect();
  return { portraitBottom: Math.round(p.bottom), nameBottom: Math.round(n.bottom), viewport: innerHeight }; })()
```
Expected: `nameBottom` ≤ `viewport`.

- [ ] **Step 6: Check the whole landing page did not regress**

Screenshot `/` full-page at both widths; confirm no horizontal scroll (`document.documentElement.scrollWidth === innerWidth`) and that the About/Research/Contact sections still reveal (they depend on `script.js`).

- [ ] **Step 7: Gates and commit**

```bash
python3 .claude/skills/site-check/scripts/check_site.py | tail -2
git add style.css index.html
git commit -m "Phase 1: hero legibility and a mobile first viewport that shows the name

.hero__name was #fff on a lavender gradient (1.1:1 measured) with a
zero-offset glow; it is now var(--navy) on the sunrise gradient
(10.8:1). MINGKHWAN goes 400 -> 500 so the two lines read as one name.
The rotated label strip is capped to the viewport height so it can no
longer clip mid-word, and its copy now names the Last Lecture. At
<=768px the hero drops min-height:100vh and the 7rem portrait offset,
so portrait and name land in the first screen.

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

## Task 3: Feature *One Day of Light* on the homepage

**Files:**
- Modify: `index.html` (`#book` section), `style.css` (`.book__*` rules, add `.book__covers` + `.book__actions`)

**Interfaces:**
- Consumes: `images/one-day-of-light-cover-{en,th}.jpg`, `books/one-day-of-light-{en,th}.pdf`, the verified reservation URL, `var(--gold)`.
- Produces: the event-window featured card. Task 6's docs sweep records that it must revert after 19 Sep.

- [ ] **Step 1: Replace the `#book` card markup**

In `index.html`, replace the `.book__card` div's contents with:

```html
      <div class="book__card" data-reveal>
        <div class="book__covers">
          <img src="images/one-day-of-light-cover-en.jpg"
               alt="Front cover of the English edition of One Day of Light: a flat-vector sunrise with a faceted golden half-sun over pale blue cloud bands, and a small figure walking the horizon carrying a lamp."
               width="667" height="1000" loading="lazy" decoding="async">
          <img src="images/one-day-of-light-cover-th.jpg"
               alt="Front cover of the Thai edition, แสงของวันหนึ่ง, with the same sunrise artwork."
               width="667" height="1000" loading="lazy" decoding="async">
        </div>
        <div class="book__text">
          <p class="book__label">☀️ For the Last Lecture · 19 September 2026</p>
          <h3 class="book__title">One Day of Light <span lang="th">แสงของวันหนึ่ง</span></h3>
          <p class="book__meta">A Last Lecture on Life, Work, and What Remains · English &amp; Thai editions · free PDF</p>
          <p class="book__desc">“Every life is one day long.” Twenty-one short chapters in three parts — Morning for the life, Noon for the work, Twilight for what remains inside.</p>
          <p class="book__desc"><span lang="th">หนังสือเล่มเล็กที่วางโครงเหมือนหนึ่งวันของชีวิต ยี่สิบเอ็ดบทสั้นในสามภาค เขียนขึ้นเป็นหนังสือประกอบปัจฉิมกถา และเปิดให้ดาวน์โหลดฟรีทั้งฉบับภาษาอังกฤษและภาษาไทย</span></p>
          <div class="book__actions">
            <a href="books/one-day-of-light-en.pdf" class="btn btn--pill btn--primary" download>Download — English PDF, 2.6 MB</a>
            <a href="books/one-day-of-light-th.pdf" class="btn btn--pill btn--primary" download><span lang="th">ดาวน์โหลด ฉบับภาษาไทย</span> — PDF, 2.5 MB</a>
            <a href="https://docs.google.com/forms/d/e/1FAIpQLSfygSd_zRRk1gOirfE3I4jXl4Y2pRExtyDD0SylH73eumoAFA/viewform" target="_blank" rel="noopener" class="btn btn--pill btn--ghost">Reserve a seat →</a>
          </div>
          <p class="book__links">
            <a href="books/one-day-of-light" class="book__more">About the book ›</a>
            <a href="publications/" class="book__doi">Academic: <em>Libraries in Transformation</em> (Springer, 2024) ›</a>
          </p>
        </div>
      </div>
```

- [ ] **Step 2: Add the two new CSS rules to `style.css`, beside the existing `.book__*` block**

```css
/* Two editions, two jackets — the same dual-cover plate books/index.html uses. */
.book__covers { display: flex; gap: 1rem; align-items: flex-start; }
.book__covers img {
  width: calc(50% - 0.5rem); height: auto; display: block;
  border-radius: var(--radius-sm);
  box-shadow: 0 12px 32px rgba(17,48,75,0.18);
}
.book__actions { display: flex; flex-wrap: wrap; gap: 0.75rem; margin-bottom: 1.25rem; }
.btn--ghost {
  background: transparent; color: var(--blue-dark);
  box-shadow: inset 0 0 0 2px var(--blue-dark);
}
.btn--ghost:hover { background: var(--blue-dark); color: #fff; }
.book__more { color: var(--blue-dark); font-weight: 600; font-size: 0.9rem; }
```

Then, in the existing `.book__cover` rule, keep it (it is still used by nothing after this change — delete it only if `grep -c 'book__cover"' index.html` returns 0).

- [ ] **Step 3: Update the head**

In `index.html`, set:

```html
  <title>Anirach Mingkhwan — Professor, Author · One Day of Light</title>
  <meta name="description" content="Dr. Anirach Mingkhwan — Associate Professor at KMUTNB, AI and network researcher, and author. One Day of Light, the companion book to his Last Lecture on 19 September 2026, is free to download in English and Thai.">
```

- [ ] **Step 4: Verify the links resolve and the buttons work**

```bash
python3 .claude/skills/site-check/scripts/check_site.py --check INV-05 | tail -2
```
Expected: PASS (INV-05 resolves `books/one-day-of-light-en.pdf` etc. on disk).

In the browser at 1440 and 375: both covers render, all three buttons are ≥44px tall, the reservation link opens the Google Form, and `document.documentElement.scrollWidth === innerWidth` at 375.

- [ ] **Step 5: Gates and commit**

```bash
python3 .claude/skills/site-check/scripts/check_site.py | tail -2
python3 docs/openclaw/check-news-sync.py | tail -1
git add index.html style.css
git commit -m "Phase 1: feature One Day of Light on the homepage for the event window

The front page said 'AI Researcher' and promoted the 2024 Springer
volume while the Last Lecture book appeared only as one Latest-updates
line. Until 19 September the featured card is the book: both covers,
one English and one Thai line, both free PDFs, and the seat
reservation. Libraries in Transformation stays one click away.

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

## Task 4: Favicon, social preview, canonical

**Files:**
- Create: `favicon.svg`, `images/og-default.jpg`
- Modify: head of `index.html`, `blog/index.html`, `books/index.html`, `books/{one-day-of-light,three-old-men,a-pocketful-of-questions,the-thirteenth-seal}.html`, `publications/index.html`, `projects/index.html`, `news/index.html` (11 files)

**Interfaces:**
- Produces: `/favicon.svg` and `/images/og-default.jpg`, referenced by absolute path so they resolve from every directory.

- [ ] **Step 1: Create `favicon.svg`**

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-label="Anirach Mingkhwan">
  <rect width="64" height="64" rx="14" fill="#11304b"/>
  <path d="M14 42a18 18 0 0 1 36 0z" fill="#c4a46c"/>
  <rect x="10" y="44" width="44" height="3" rx="1.5" fill="#faf7f0"/>
</svg>
```

- [ ] **Step 2: Build the social card**

```bash
python3 - <<'PY'
from PIL import Image
W, H = 1200, 630
card = Image.new("RGB", (W, H), (250, 247, 240))
for i, name in enumerate(("en", "th")):
    c = Image.open(f"images/one-day-of-light-cover-{name}.jpg")
    h = 460
    c = c.resize((round(c.width * h / c.height), h), Image.LANCZOS)
    card.paste(c, (W // 2 + (-c.width - 20 if i == 0 else 20), (H - h) // 2))
card.save("images/og-default.jpg", "JPEG", quality=82, optimize=True, progressive=True)
import os; print(card.size, os.path.getsize("images/og-default.jpg"), "bytes")
PY
```
Expected: `(1200, 630)` and under 300,000 bytes.

- [ ] **Step 3: Add the head block to all 11 pages**

For each page, insert after its `<meta name="description">` (substituting the per-page values from the table below):

```html
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="canonical" href="https://anirach.com/PATH">
  <meta property="og:type" content="website">
  <meta property="og:title" content="TITLE">
  <meta property="og:description" content="DESC">
  <meta property="og:url" content="https://anirach.com/PATH">
  <meta property="og:image" content="https://anirach.com/images/og-default.jpg">
  <meta name="twitter:card" content="summary_large_image">
```

| File | PATH | og:title |
|---|---|---|
| `index.html` | `` | Anirach Mingkhwan — Professor, Author |
| `blog/index.html` | `blog/` | Blog — Anirach Mingkhwan |
| `books/index.html` | `books/` | Novels & Writing — Anirach Mingkhwan |
| `books/one-day-of-light.html` | `books/one-day-of-light` | One Day of Light — free companion book to the Last Lecture |
| `books/three-old-men.html` | `books/three-old-men.html` | Three Old Men: The Last Conversation |
| `books/a-pocketful-of-questions.html` | `books/a-pocketful-of-questions.html` | A Pocketful of Questions |
| `books/the-thirteenth-seal.html` | `books/the-thirteenth-seal.html` | The Thirteenth Seal |
| `publications/index.html` | `publications/` | Publications — Anirach Mingkhwan |
| `projects/index.html` | `projects/` | Projects & Apps — Anirach Mingkhwan |
| `news/index.html` | `news/` | News & Updates — Anirach Mingkhwan |

`og:description` = that page's existing `<meta name="description">` content, verbatim.

For `books/one-day-of-light.html` only, also override the image with the book's own cover:
`<meta property="og:image" content="https://anirach.com/images/one-day-of-light-cover-en.jpg">`.

- [ ] **Step 4: Verify**

```bash
for f in index.html blog/index.html books/index.html books/one-day-of-light.html \
         books/three-old-men.html books/a-pocketful-of-questions.html books/the-thirteenth-seal.html \
         publications/index.html projects/index.html news/index.html; do
  printf '%-45s icon=%s canonical=%s og:image=%s\n' "$f" \
    "$(grep -c 'rel="icon"' $f)" "$(grep -c 'rel="canonical"' $f)" "$(grep -c 'og:image' $f)"
done
```
Expected: every row `icon=1 canonical=1 og:image=1`.

- [ ] **Step 5: Gates and commit**

```bash
python3 .claude/skills/site-check/scripts/check_site.py | tail -2
git add favicon.svg images/og-default.jpg index.html blog/index.html books publications projects news
git commit -m "Phase 1: favicon, Open Graph and canonical on the 11 nav-bearing pages

/favicon.ico 404'd on all 47 pages and 0 pages carried og:/canonical,
so every shared link rendered as a bare URL. Adds an SVG mark (navy
ground, the One Day of Light sun) and a 1200x630 card showing both
covers. Canonical policy: extensionless where the site already links
that way, .html elsewhere.

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

## Task 5: A real 404 page

**Files:**
- Create: `404.html`

**Interfaces:**
- Consumes: LISTING chrome copied byte-for-byte from `news/index.html` (nav, footer, `:root`, the 800px nav-takeover block).

- [ ] **Step 1: Build the page**

Copy `news/index.html` to `404.html`, then replace everything between `<main …>` and `</main>` with:

```html
    <main class="news-main" id="main">
      <section class="books-section">
        <div class="series-header">
          <div class="series-header__left">
            <span class="series-icon" aria-hidden="true">🧭</span>
            <h1 class="series-title">Page not found</h1>
          </div>
        </div>
        <p>That page isn’t here — it may have moved, or the link may be mistyped.</p>
        <p><span lang="th">ไม่พบหน้าที่คุณกำลังมองหา อาจถูกย้ายหรือลิงก์พิมพ์ผิด</span></p>
        <p>Try one of these:</p>
        <ul>
          <li><a href="/">Home</a> — about Anirach Mingkhwan</li>
          <li><a href="/blog/">Blog</a> — 37 articles on AI, DevOps and OpenClaw</li>
          <li><a href="/publications/">Publications</a> — the Springer book and chapters</li>
          <li><a href="/books/">Novels</a> — including <a href="/books/one-day-of-light">One Day of Light</a>, free to download</li>
          <li><a href="/projects/">Projects</a> · <a href="/news/">News</a></li>
        </ul>
      </section>
    </main>
```

Set `<title>Page not found — Anirach Mingkhwan</title>`, a matching description, and the favicon link (no og tags on a 404).

- [ ] **Step 2: Verify structure and chrome parity**

```bash
diff <(sed -n '/<nav class="nav"/,/<\/nav>/p' news/index.html) <(sed -n '/<nav class="nav"/,/<\/nav>/p' 404.html) && echo "nav identical"
grep -c '<h1' 404.html          # expect 1
grep -c '<script' 404.html      # expect 0
```

- [ ] **Step 3: Confirm it renders and the linter accepts it**

Serve locally, open `/404.html` at both widths, click every link. Then:

```bash
python3 .claude/skills/site-check/scripts/check_site.py | tail -2
```
Expected: `0 new, N known`. If INV-26 or the nav-consistency check flags `404.html` (it is a new root page, not a section index), record the exact rule and either fix the page or add the rule's expectation — do **not** baseline it away.

- [ ] **Step 4: Commit**

```bash
git add 404.html
git commit -m "Phase 1: add a real 404 page

A mistyped URL landed on GitHub's generic page with no route back.
LISTING chrome copied from news/index.html, bilingual, six
destinations, zero JavaScript.

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

## Task 6: Sweep the docs, re-measure, push, verify live

**Files:**
- Modify: `.claude/skills/page-design/SKILL.md` (§1 token block, §5 gradients, censuses), `.claude/skills/page-design/references/tokens.md`, `.claude/skills/a11y-perf/SKILL.md` (rule 4, R3/R4 tables, image counts), `.claude/skills/site-check/references/drift-budget.md`, `CLAUDE.md`, the spec's Status line

**Interfaces:**
- Consumes: everything above. Produces: skills that match the shipped site (the standing rule — a wrong number is worse than none).

- [ ] **Step 1: Re-derive every number the docs quote**

```bash
find . -name '*.html' -not -path './.git/*' -not -path './.claude/*' -not -path './.playwright-mcp/*' | wc -l
ls images | wc -l
python3 - <<'PY'
import re, pathlib
n=ok=0
for p in pathlib.Path('.').rglob('*.html'):
    if {'.claude','.git','.playwright-mcp'} & set(p.parts): continue
    for m in re.finditer(r'<img\b[^>]*>', p.read_text(encoding='utf-8'), re.S):
        n+=1; ok+= all(a+'=' in m.group(0) for a in ('loading','decoding','width','height'))
print(f"imgs {ok}/{n}")
PY
grep -ho 'linear-gradient(135deg, *#[0-9a-f]*' index.html style.css blog/*.html books/*.html news/index.html projects/index.html publications/index.html | sort | uniq -c | sort -rn | head
```

- [ ] **Step 2: Update the skills**

- `page-design` §1: replace the canonical block with spec §3.2's 27 tokens; note the count change 24 → 27 and that `--gold` is brand, not a seventh status colour.
- `page-design` §5: replace the five gradient values with §3.4's; note that only Default and Indigo-deep were re-keyed in Phase 1.
- `a11y-perf` rule 4: `--blue` is now `#226299` and **passes as text** (6.4:1 white / 6.0 cream); delete the "use `--blue-dark` for text" workaround and the `#4338ca` special case, and update R3/R4's tables to the new grounds.
- `drift-budget.md`: new baseline shape (file counts, `images/` count), and note 404.html as a new root page.
- `CLAUDE.md`: the tree gains `favicon.svg`, `404.html`, `scripts/`; the `_config.yml` line gains `scripts`; add one line that the homepage feature card is event-scoped and reverts after 19 Sep 2026.

- [ ] **Step 3: Re-run the critique's mechanical half on the changed pages**

```bash
node /Users/anirach/.claude/skills/impeccable/scripts/detect.mjs --json index.html 404.html | tail -5
```
Record the count; the pre-Phase-1 figure for `index.html` was 3 CLI findings (all in the noise classes documented in the spec).

- [ ] **Step 4: Both gates, then push**

```bash
python3 .claude/skills/site-check/scripts/check_site.py | tail -2
python3 docs/openclaw/check-news-sync.py | tail -1
git add -A .claude CLAUDE.md docs
git commit -m "Phase 1: sweep skills and CLAUDE.md to the shipped palette and pages

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
git push origin main
```

- [ ] **Step 5: Verify live**

```bash
until curl -s https://anirach.com/ | grep -q 'One Day of Light'; do sleep 20; done
for u in "" favicon.svg 404.html images/og-default.jpg books/one-day-of-light-en.pdf; do
  printf '%-40s %s\n' "/$u" "$(curl -s -o /dev/null -w '%{http_code}' https://anirach.com/$u)"
done
curl -s -o /dev/null -w 'nonexistent -> %{http_code}\n' https://anirach.com/no-such-page
curl -s https://anirach.com/ | grep -o 'og:image[^>]*' | head -1
```
Expected: `/` 200, `favicon.svg` 200, `404.html` 200, `og-default.jpg` 200, the PDF 200, a nonexistent path → 404 (served by our page), and the og:image tag present.

- [ ] **Step 6: Re-score**

Re-run the design-director half of the critique on `/` only and record the new heuristic scores in the spec's Status line. Target for Phase 1 alone: **≥ 22/36**.

---

## Self-Review

**Spec coverage:** §3 tokens → Task 1. §4 hero → Task 2. §4 featured → Task 3. §4.1 favicon + §4.2 social → Task 4. §4.3 404 → Task 5. §5 Phase-1 row + the standing docs rule → Task 6. §7 open decisions are *not* implemented here by design — items 1–3 belong to Phases 2 and 4; item 4 (token approval) is Task 1 Step 11's gate.

**Placeholder scan:** none — every step carries the literal code, command, or expected output.

**Type consistency:** `--gold`, `--gold-dark`, `--cloud`, `--parchment` are introduced in Task 1 Step 3's `NEW_TOKENS` and consumed by name in Tasks 2 (`var(--cloud)`, `var(--parchment)`) and 3 (`var(--blue-dark)`); `.book__covers`, `.book__actions`, `.btn--ghost`, `.book__more` are defined in Task 3 Step 2 and used in Step 1's markup. `scripts/retoken.py` is created in Task 1 and re-referenced only by `--verify`.
