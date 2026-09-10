# Sitewide edits — file lists, scripts, verification

No partials exist, so every "global" change is an N-file edit. Run these from the repo
root, `/Users/anirach/Documents/Anirach.github.io`. macOS `sed` needs the empty
`-i ''` argument.

Always: work on a branch, run the verification grep afterwards, and eyeball
`git diff --stat` before committing.

## What N is today

> **Standing rule:** any change that invalidates a number here must update it in the
> same commit. Everything below was re-measured **2026-09-06 against `905d3a4`**.

**N = 87 HTML files** — 86 enumerated by `check_site.py` plus `404.html`, which it
deliberately skips. That is 76 posts + `blog/index.html`, the landing page, 5 section
indexes, 4 `books/` detail pages, and `404.html`.

**But there are three different Ns, and picking the wrong one is how a sweep half-lands:**

| The edit touches… | N | Why |
|---|---|---|
| a `<head>`, a `:root`, an embedded `<style>` block | **87** (86 + `style.css`) | one per file, no duplication |
| **post body prose or markup** | **87 × 2 language tracks** | every post holds its article twice, `.l-th` and `.l-en`. A regex that matched once per post before 2026-09-03 now matches twice |
| **the 20 AI Transformation posts** | **1 manifest + a script run** | those posts are *generated*. Hand-editing 20 of them is the error, not the work — see "The generated series" below |

The bilingual multiplier is the one that will surprise you. `blog/api-request-lifecycle.html`
reports two `h2 → h4` skips for a single `<h4>Request:</h4>`, because the heading exists in
both tracks. Fix both; `python3 scripts/bilingualize.py --verify <slug>` is the per-file
check that the tracks still agree, and it is the only thing that catches a one-track edit.

**Two hidden directories will corrupt a count, and only one class of tool sees them.**
`.claude/` carries the skills' own HTML templates and CSS assets; `.bilingual/` holds 138
scratch content sheets for the generated series. `grep -r` does not descend into either
(dot-directories are skipped unless you name one), so the greps below are safe as written.
**`find` and `pathlib.rglob` do descend**: `find . -name "*.html" -not -path "./.git/*"`
returns **169**, not 87. Every `find` and `rglob` in this file therefore carries all three
exclusions, and so must yours.

```bash
find . -name "*.html" -not -path "./.git/*" -not -path "./.claude/*" \
     -not -path "./.bilingual/*" | wc -l                              # 87
ls blog/*.html | wc -l                                                # 77 (76 posts + index)
ls images/ | wc -l ; du -sh images/                                   # 195 files, 11M

grep -rIo ":hover" --include="*.html" --include="*.css" --exclude-dir=.claude . | wc -l      # 548
grep -rl ":focus-visible"         --include="*.html" --include="*.css" --exclude-dir=.claude . | wc -l   # 87 (86 html + style.css)
grep -rl "prefers-reduced-motion" --include="*.html" --include="*.css" --exclude-dir=.claude . | wc -l   # 87
grep -rl "color-scheme"           --include="*.html" --include="*.css" --exclude-dir=.claude . | wc -l   # 87
grep -rl "text-wrap"              --include="*.html" --include="*.css" --exclude-dir=.claude . | wc -l   # 87
grep -rhoE '<script[^>]*>' --include="*.html" --exclude-dir=.claude . | sort | uniq -c       # 79 × ld+json, nothing else
grep -rl "<main"   --include="*.html" --exclude-dir=.claude . | wc -l                        # 87 / 87
grep -rl 'id="main"' --include="*.html" --exclude-dir=.claude . | wc -l                      # 87 / 87
grep -rl "skip-link" --include="*.html" --exclude-dir=.claude . | wc -l                      # 87 / 87
grep -roh 'target="_blank"' --include="*.html" --exclude-dir=.claude . | wc -l               # 92 (0 lack rel)
grep -rhoE '<html lang="[^"]*"' --include="*.html" --exclude-dir=.claude . | sort | uniq -c  # 11 en, 76 th
grep -rl "fonts.googleapis" --include="*.html" --exclude-dir=.claude . | wc -l               # 87 / 87
grep -rl 'class="nav__burger"' --include="*.html" --exclude-dir=.claude . | wc -l            # 10
ls images/*-cover.jpg | wc -l ; ls images/*-cover-*.jpg | wc -l ; ls images/*-cover.png 2>/dev/null | wc -l
                                                                      # 77 plain, 8 suffixed, 0 png
ls images/*-og.jpg | wc -l ; ls images/ai-transformation-fig-*.png | wc -l                   # 80 share cards, 19 figures
```

**Card counting needs the anchor regex, not `grep -c`.** `grep -c 'class="card"'
blog/index.html` returns **77**: `grep -c` counts lines, and one hit is the warning comment
above the featured post. The three real consumers all anchor on the tag:

```bash
python3 -c "
import re
s=open('blog/index.html',encoding='utf-8').read()
print('cards', len(re.findall(r'<a\s+href=\"[^\"]+\"\s+class=\"card\">', s)),
      'feature', len(re.findall(r'class=\"feature\">', s)))"      # → cards 76 feature 1
```

76 cards = 76 posts. The feature is a **second** link to one of them (today
`ai-transformation-layers`) and is deliberately `class="feature"` so it does not inflate the
counters or duplicate an item in `feed.xml`.

**`<img>` attributes need a multiline parse, not a line grep** — 20 `<img>` on the site
span multiple lines (mostly on the books/publications pages), and 37 posts contain a literal
`<img>` inside a CSS comment which is not a tag. The line grep says 316, the naive parse says
336, and **the true tag count is 299, all 299 compliant**:

```bash
python3 - <<'EOF'
import re, pathlib
n=ok=0
for p in pathlib.Path('.').rglob('*.html'):
    if any(x in p.parts for x in ('.claude','.git','.bilingual')): continue
    for m in re.finditer(r'<img\b[^>]*>', p.read_text(encoding='utf-8'), re.S):
        n+=1; ok+= all(a+'=' in m.group(0) for a in ('loading','decoding','width','height'))
print(ok, "/", n)      # → 299 / 336   (the 37-tag gap is the CSS-comment literal)
EOF
```

### Four obsolete warnings this file used to carry

- **"`grep -rIoE 'outline *:' … | wc -l` → 0 (UA ring intact)."** It now returns **87**.
  `:focus:not(:focus-visible) { outline: none; }` is part of the shipped block and is
  correct. Read the selector before treating an `outline` hit as a defect.
- **"A `sed` on `:root` silently misses 11 files."** Obsolete since `6670480`: every file
  except `index.html` has a `:root`, and `index.html`'s lives in `style.css:5`.
- **"The 10 island posts load no webfont."** Obsolete since 2026-08-26. **All 87 pages load
  Google Fonts**, all 87 use `display=swap`, all 87 carry both `preconnect` links, and all 86
  embedded-CSS pages set `body { font-family: var(--font) }`. The Inter + Sarabun system
  reaches every page; there is no font-less subset to work around.
- **"`index.html` is the only file with a `<script>`."** Obsolete since `bb9c7dc`
  (2026-08-26) deleted `script.js`. The site is zero-JavaScript, `check_site.py` **INV-38**
  fails the build on any `<script>` that is not `application/ld+json`, and the 79 script tags
  that exist are all that one type. Never write a loop that adds or edits JavaScript.

## The generated series — do NOT hand-edit 20 files

The 20 `blog/ai-transformation-*.html` posts are emitted by `scripts/build_series.py` from
`scripts/series/ai-transformation.json` plus per-post content sheets in `.bilingual/`. **The
emitted posts are the committed truth; the sheets are scratch.** For anything the manifest
owns — chip labels, titles, hero subs, tags, read times, covers, figures — edit the manifest
and re-emit:

```bash
python3 scripts/build_series.py --check                    # diff the skeleton it lifts from blog/hermes-101.html
python3 scripts/build_series.py --post <slug>              # re-emit one post
python3 scripts/build_series.py --restrip                  # rewrite ONLY the 20-chip grouped nav strip, everywhere
```

`--restrip` is the growth path for a 21st post and the only thing that should ever touch a
shipped file after launch. A sitewide a11y sweep that rewrites CSS inside a `<style>` block
is still a normal 87-file edit and does not need the builder — but **check whether the thing
you are about to sed is a manifest field first**, or the next `--post` run will revert you.

The AI Transformation posts are also the cleanest templates on the site: zero heading skips,
`<main id="main">`, both language tracks, a references block and 1–2 figures. Copy one of
those rather than an OpenClaw post.

## Insert a CSS block into every embedded `<style>`

**The focus / motion / color-scheme / text-wrap block is installed everywhere** — 86 embedded
`<style>` blocks + `style.css`. So is everything `assets/a11y-block.css` holds:
`.card:focus-within` (in the 6 card-bearing files — `blog/`, `books/`, `news/`, `projects/`,
`publications/`, `404.html`), the `.skip-link` rules (86 + `style.css`), and
`[data-reveal] { opacity: 1 !important }` at `style.css:902`. **There is nothing left to
insert.** The loop below is the delivery mechanism for a *future* block, kept because getting
its idempotence guard right is the part people get wrong.

**Pick a guard string unique to what you are inserting.** `if 'prefers-reduced-motion' in s:
continue` now matches every file, so a loop using it silently patches nothing and reports
success.

```bash
BLOCK=$(cat /path/to/new-block.css)
python3 - "$BLOCK" <<'EOF'
import sys, pathlib
block = "\n" + sys.argv[1] + "\n"
GUARD = 'my-unique-selector'                  # <- must be a string only the new block contains
for p in pathlib.Path('.').rglob('*.html'):
    if any(x in p.parts for x in ('.git', '.claude', '.bilingual')): continue
    s = p.read_text(encoding='utf8')
    if GUARD in s: continue                   # idempotent
    i = s.rfind('</style>')
    if i == -1:
        print('NO <style>:', p); continue     # index.html — its CSS is style.css
    p.write_text(s[:i] + block + s[i:], encoding='utf8')
    print('patched', p)
EOF

grep -rl 'my-unique-selector' --include="*.html" --exclude-dir=.claude . | wc -l   # expect 86
```

86, not 87: `index.html` has no embedded `<style>` and never gets one — that invariant was
defended explicitly in `7867c00`, when a `<noscript><style>` patch was rejected for exactly
this reason. Its CSS goes in `style.css`.

## Skip link and `<main id="main">` — both landed, 87/87

Nothing to do. `check_site.py` **INV-30** fails the build if the link and its target ever
come apart, so the pair cannot silently regress. The shipped link is:

```html
<a href="#main" class="skip-link">ข้ามไปเนื้อหาหลัก / Skip to content</a>
```

```bash
grep -rl "skip-link" --include="*.html" --exclude-dir=.claude . | wc -l   # 87
grep -rl 'id="main"' --include="*.html" --exclude-dir=.claude . | wc -l   # 87
```

**One thing to know before moving a `<main>`:** the TH ⇄ EN switch is
`#langSwitch:checked ~ main .l-en`, so **anything the switch must reach has to be inside
`<main>`**. Three posts — `deployment-hosting`, `openclaw-memory-architecture`,
`vibe-coding-devops-process` — had their `<main>` moved *up* to wrap the hero on 2026-09-03
for exactly this reason. Moving a `<main>` down past a `.l-th`/`.l-en` pair breaks the switch
silently and only in one language.

## `rel="noopener"` — done, 0 of 92 remain

```bash
python3 -c "
import re,pathlib
print(sum(1 for p in pathlib.Path('.').rglob('*.html')
          if not any(x in p.parts for x in ('.claude','.git','.bilingual'))
          for a in re.finditer(r'<a\b[^>]*>', p.read_text(encoding='utf-8'), re.S)
          if 'target=\"_blank\"' in a.group(0) and 'rel=' not in a.group(0)))"   # → 0
```

The BSD-`sed`-has-no-lookahead note still applies if it ever regresses: use `perl -pi -e`,
not `sed`, for `s/target="_blank"(?![^>]*rel=)/…/g`.

## Font URL — do NOT trim. The whole site is on two URLs.

**The old "trim 27 dual-family files" recipe is retired and would be a net loss.** Inter and
JetBrains Mono are *variable* fonts: `wght@300;400;…;900` and `wght@400` download identical
bytes, so the trim saves nothing and risks silently re-rendering six `style.css` headings at
400. Sarabun is static and was going the other way — 2026-08-26 *added* 500 and 800, which
the browser had been synthesising as faux-bold over Thai glyphs.

Every page is on one of exactly two URLs. Check a new page against them:

```
67 files  Inter:wght@300..900&family=Sarabun:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400..600&display=swap
20 files  Inter:wght@300..900&family=Sarabun:wght@400;500;600;700;800&display=swap
```

```bash
grep -rhoE 'href="https://fonts.googleapis.com/css2[^"]*"' --include="*.html" --exclude-dir=.claude . \
  | sort | uniq -c            # must print exactly the two lines above
grep -rnE "font-weight: *300" --include="*.html" --include="*.css" --exclude-dir=.claude .
# → 6 hits, all in style.css (index.html's headings). None in blog/.
```

## `.post-series-footer` and `.post-hero__meta` colours — both done

The 2026-08-26 Phase 1 sweep closed both, and they have stayed closed through two series
launches. Verify rather than re-run:

```bash
python3 -c "
import re,glob,collections
for sel in (r'\.post-series-footer', r'\.post-hero__meta'):
    c=collections.Counter()
    for f in glob.glob('blog/*.html'):
        for m in re.finditer(sel+r'\s*\{([^}]*)\}', open(f,encoding='utf-8').read()):
            cm=re.search(r'color:\s*([^;]+)', m.group(1)); c[cm.group(1).strip() if cm else 'none']+=1
    print(sel, dict(c))"
# .post-series-footer {'var(--slate-light)': 61}
# .post-hero__meta    {'#fff': 44, 'var(--slate-light)': 32, 'none': 71}
```

Zero `var(--gray)` and zero `rgba(255,255,255,0.x)`. `check_site.py` **INV-28** keeps the two
hero families (43 Deep Blue, 33 Sunrise) from growing a third, which is what made the
per-file colour fix stick. The perl recipes that did the sweep are in git; do not re-run them.

## Heading defects to fix by hand

`deployment-hosting`'s duplicate `<h1>` is gone — all 76 posts have exactly one, INV-11
PASSes. **31 posts have a level skip, and they are two different jobs.**

**(a) 20 posts: `h1 → h3` on the series strip.** The chip strip's heading —
`<h3>🌅 Life Thought &amp; Philosophy 2026</h3>` — sits directly under the hero `<h1>`.
One line per file: demote to a `<p>` or promote to `<h2>`. It is the same shape in all 20, so
this one *is* scriptable, but check each strip's exact string first — INV-03c parses these.

```
hermes-101  hermes-agent-teams  hermes-automation  hermes-desktop-fleet  hermes-integrations
hermes-memory  hermes-models-cost  hermes-production  hermes-security  hermes-skills
morning-waking  morning-working  morning-toward-noon
noon-first-fire  noon-high-heat  noon-long-light
twilight-true-north  twilight-open-hand  twilight-before-dark
openclaw-integrations
```

**(b) 11 posts: real `h2 → h4` breaks in the prose.** Counts re-measured 2026-09-06.
**Every count here is doubled by bilingualisation** — the number is *tags*, and each tag
exists once per language track, so `api-request-lifecycle`'s "2" is one `<h4>Request:</h4>`
written twice. Fix both copies or the tracks diverge.

```
idle-self-improvement   8      openclaw-101             4
obsidian-ai-jarvis      6      openclaw-memory          4
openclaw-agent-teams    6      openclaw-skills          4
openclaw-migration      6      api-request-lifecycle    2
beyond-plugins          2      devops-security          2
networking-fundamentals 2
```

The 20 AI Transformation posts have **zero** skips. Re-detect after editing:

```bash
python3 - <<'EOF'
import re, pathlib
for p in sorted(pathlib.Path('blog').glob('*.html')):
    if p.name == 'index.html': continue
    lv = [int(m.group(1)) for m in re.finditer(r'<h([1-6])[\s>]', p.read_text(encoding='utf8'))]
    skips = [(a,b) for a,b in zip(lv, lv[1:]) if b > a + 1]
    if skips or lv.count(1) != 1:
        print(f"{p.name:42s} h1x{lv.count(1)}  skips={len(skips)}")
EOF
python3 scripts/bilingualize.py --verify <slug>     # after any per-post markup edit
```

### `blog/index.html` is already fixed — DO NOT RUN THE OLD RECIPE

This file used to carry a `perl -pi` one-liner rewriting `<h2 class="card__title">` to
`<h3>`, and a later warning to leave the titles at `<h4>`. **Both are wrong now.** The
ladder went a level shallower on 2026-08-26 when the category bands were deleted:

```bash
python3 -c "import re,collections; s=open('blog/index.html').read(); print(collections.Counter(int(m.group(1)) for m in re.finditer(r'<h([1-6])\b[^>]*>', s)))"
# → Counter({3: 76, 2: 6, 1: 1})
#   h1 page title -> h2 ×6 (5 .series-title + the feature) -> h3 ×76 .card__title
```

Three consumers read the level with `<(h[1-6]) class="card__title">` and follow a re-cut;
`gen_feed.py` was hard-coded to `<h4>` and silently emptied the feed until it was made
level-agnostic. **Grep for the class, never the level**, and never hardcode a level in a
recipe here again — this is the third time the file has said something different.

## Emoji icons and avatar alts — both done

```bash
grep -c '<span class="series-icon" aria-hidden="true">' blog/index.html   # → 5
grep -c 'alt="" class="card__avatar"' blog/index.html                    # → 76
grep -rln 'alt="[^"]*Cover"' --include='*.html' --exclude-dir=.claude .  # → nothing
```

The `.research__icon` divs in `index.html` no longer exist — the emoji research tiles were
replaced by numbered arcs whose marks are inline `<svg aria-hidden="true">`. The old
`perl -pi` recipes for both are retired; they match nothing.

**Where decorative-alt risk lives now: the 19 series figures.** Each appears once per
language track with a *translated* alt, and the wrapping `<a href="…png">` has no other text,
so the alt is the link's entire accessible name. Two alts per figure, both full sentences.

## Counters — recompute, never hardcode

**Six** counter sites in `blog/index.html` today and all are correct; `check_site.py`
INV-02a–INV-02f all PASS. The "N Categories" stat and `#cat-technology`'s article count went
with the category bands on 2026-08-26 — the last band held 100% of the posts, so it
partitioned nothing. INV-02f arrived with the fifth series and checks the `.blog-jump` chips,
which nothing had ever policed.

Current values, re-derive rather than trust: **5 Series · 76 Articles**, and per section
`#series-ai-transformation` 20, `#series-hermes` 10, `#series-openclaw` 13, `#series-devops`
24, `#series-life` 9.

```bash
python3 -c "
import re
s=open('blog/index.html',encoding='utf-8').read()
print('cards', len(re.findall(r'<a\s+href=\"[^\"]+\"\s+class=\"card\">', s)))
for sid,body in re.findall(r'<section class=\"series-section\" id=\"([^\"]+)\">(.*?)</section>',s,re.S):
    print(sid, len(re.findall(r'<a\s+href=\"[^\"]+\"\s+class=\"card\">',body)))"
python3 .claude/skills/site-check/scripts/check_site.py --check INV-02a --check INV-02f
```

Four more counters live outside `blog/` and are checked by a different gate —
`"N updates"` on `news/`, `"N chapters"` on `publications/`, `"N novel"` and `"N complete"`
on `books/`:

```bash
python3 docs/openclaw/check-news-sync.py
```

## Post-change smoke test

There is no CI and no test suite, so this is the whole safety net:

```bash
python3 -m http.server 8000 &
open http://localhost:8000/blog/index.html
```

Check at 375px and 1440px width, tab through the nav and the first three cards (the 2px
`:focus-visible` ring must be visible on each — it ships on every page, so its *absence* is
the regression), **flip the ไทย · English pill on a post and re-check the same things in the
other track**, and confirm the network panel shows the covers deferred: **152 of the 153
`<img>` tags on `blog/index.html` are `loading="lazy"`**, so a first paint should fetch
roughly the first viewport's worth (**≈0.65 MB**), not the full **3.43 MB** the page
references. The one eager image is the featured card's share card — it is the LCP element and
carries `fetchpriority="high"` deliberately.

And run the linters, which are the actual test suite:

```bash
python3 .claude/skills/site-check/scripts/check_site.py      # 61 checks, expect exit 0
python3 scripts/check_visibility.py --strict                 # search/AI visibility, expect exit 0
python3 .claude/skills/blog-post/assets/verify-wiring.py     # expect no FAIL lines
```
