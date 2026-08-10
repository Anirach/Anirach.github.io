# Sitewide edits — file lists, scripts, verification

No partials exist, so every "global" change is an N-file edit. Run these from the repo
root, `/Users/anirach/Documents/Anirach.github.io`. macOS `sed` needs the empty
`-i ''` argument.

Always: work on a branch, run the verification grep afterwards, and eyeball
`git diff --stat` before committing.

## Baseline counters — re-run these, don't trust a stale number

> **Standing rule:** any change that invalidates a number here must update it in the
> same commit. Everything below was re-measured **2026-08-10 against `7867c00`**.

Always exclude `.claude/` — the skill directories carry HTML templates and CSS
assets that match most of these patterns and inflate every count.

```bash
find . -name "*.html" -not -path "./.git/*" -not -path "./.claude/*" | wc -l          # 42
grep -rIo ":hover"  --include="*.html" --include="*.css" --include="*.js" --exclude-dir=.claude . | wc -l   # 115
grep -rl ":focus-visible"         --include="*.html" --include="*.css" --exclude-dir=.claude . | wc -l      # 42 (41 html + style.css)
grep -rl "prefers-reduced-motion" --include="*.html" --include="*.css" --exclude-dir=.claude . | wc -l      # 42
grep -rl "color-scheme"           --include="*.html" --include="*.css" --exclude-dir=.claude . | wc -l      # 42
grep -rl "<script" --include="*.html" --exclude-dir=.claude .                         # index.html only
grep -rl "<main"   --include="*.html" --exclude-dir=.claude . | wc -l                 # 11 / 42
grep -rl 'id="main"' --include="*.html" --exclude-dir=.claude . | wc -l               #  0 / 42
grep -rl "skip-link" --include="*.html" --exclude-dir=.claude . | wc -l               #  0 / 42
grep -roh 'target="_blank"' --include="*.html" --exclude-dir=.claude . | wc -l        # 57 (12 lack rel)
grep -rhoE '<html lang="[^"]*"' --include="*.html" --exclude-dir=.claude . | sort | uniq -c  # 5 en, 37 th
grep -rl "fonts.googleapis" --include="*.html" --exclude-dir=.claude . | wc -l        # 32 / 42
grep -c 'class="card"' blog/index.html                                                # 37
ls images/*-cover.jpg | wc -l ; ls images/*-cover.png 2>/dev/null | wc -l             # 36 jpg, 0 png
du -sh images/                                                                        # 5.6M
```

**`<img>` attributes need a multiline parse, not a line grep** — one `<img>` on the site
spans two lines, so `grep -oh "<img[^>]*>"` reports 119 where the truth is 120:

```bash
python3 - <<'EOF'
import re, pathlib
n=ok=0
for p in pathlib.Path('.').rglob('*.html'):
    if '.claude' in p.parts or '.git' in p.parts: continue
    for m in re.finditer(r'<img\b[^>]*>', p.read_text(encoding='utf-8'), re.S):
        n+=1; ok+= all(a+'=' in m.group(0) for a in ('loading','decoding','width','height'))
print(ok, "/", n)      # → 120 / 120
EOF
```

### Two obsolete warnings this file used to carry

- **"`grep -rIoE 'outline *:' … | wc -l` → 0 (UA ring intact)."** It now returns **42**.
  `:focus:not(:focus-visible) { outline: none; }` is part of the shipped block and is
  correct. Read the selector before treating an `outline` hit as a defect.
- **"A `sed` on `:root` silently misses 11 files."** Obsolete since `6670480`: every file
  except `index.html` has a `:root`, and `index.html`'s lives in `style.css:5`. What is
  still true about the same 10 island posts is that they load **no webfont**.

## The 10 island posts with no webfont

They declare their own `font-family` and never load Inter, so the design system's type
does not reach them (their *tokens* do — see above).

```
blog/beyond-plugins.html          -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif
blog/idle-self-improvement.html
blog/openclaw-101.html
blog/openclaw-agent-teams.html
blog/openclaw-integrations.html
blog/openclaw-memory.html         'Segoe UI', Tahoma, Geneva, Verdana, sans-serif
blog/openclaw-migration.html
blog/openclaw-production.html     names 'Inter' but never loads it
blog/openclaw-security.html       names 'Inter' but never loads it
blog/openclaw-skills.html
```

Regenerate at any time:

```bash
for f in $(find . -name "*.html" -not -path "./.git/*" -not -path "./.claude/*"); do
  grep -q "fonts.googleapis" "$f" || echo "$f"
done
```

## Insert a CSS block into every embedded `<style>`

**The focus/motion/color-scheme/text-wrap block is already installed everywhere** —
`e8da9da` put it in 41 embedded `<style>` blocks + `style.css`. Do not re-run this loop
for that block. What `assets/a11y-block.css` now holds is only the parts *not* on disk
(`.card:focus-within` parity, the skip link, the `[data-reveal]` no-JS net), so this
loop remains the delivery mechanism for those.

`assets/a11y-block.css` has no `:root` dependency beyond `--blue-dark` / `--navy` /
`--radius-sm`, and falls back with literals anyway — safe in all 42 files.

**The `if 'prefers-reduced-motion' in s: continue` idempotence guard below now matches
every file**, because the shipped block contains that string. Change the guard to a
string unique to what you are inserting (e.g. `'card:focus-within'`) or the loop will
silently patch nothing and report success.

```bash
BLOCK=$(cat .claude/skills/a11y-perf/assets/a11y-block.css)
python3 - "$BLOCK" <<'EOF'
import sys, pathlib, re
block = "\n" + sys.argv[1] + "\n"
for p in pathlib.Path('.').rglob('*.html'):
    if '.git' in p.parts: continue
    if '.claude' in p.parts: continue            # never rewrite the skills' own templates
    s = p.read_text(encoding='utf8')
    if 'prefers-reduced-motion' in s:            # idempotent
        continue
    i = s.rfind('</style>')
    if i == -1:
        print('NO <style>:', p); continue
    p.write_text(s[:i] + block + s[i:], encoding='utf8')
    print('patched', p)
EOF

grep -rl "card:focus-within" --include="*.html" --exclude-dir=.claude . | wc -l   # expect 41
# already-shipped block, for reference — these are 42 (41 html + style.css) today:
grep -rl "prefers-reduced-motion" --include="*.html" --include="*.css" --exclude-dir=.claude . | wc -l
grep -rl "focus-visible"          --include="*.html" --include="*.css" --exclude-dir=.claude . | wc -l
```

## Skip link after every `<body>`

```bash
python3 - <<'EOF'
import pathlib
LINK = '\n<a href="#main" class="skip-link">ข้ามไปเนื้อหาหลัก / Skip to content</a>'
for p in pathlib.Path('.').rglob('*.html'):
    if '.git' in p.parts: continue
    if '.claude' in p.parts: continue   # never rewrite the skills' own templates
    s = p.read_text(encoding='utf8')
    if 'skip-link' in s: continue
    i = s.find('<body')
    j = s.find('>', i)
    p.write_text(s[:j+1] + LINK + s[j+1:], encoding='utf8')
EOF
grep -rl "skip-link" --include="*.html" --exclude-dir=.claude . | wc -l   # expect 42
```

**Do the target first.** The link is useless without one, and today **0 of 42** files
have `id="main"`. 31 files have no `<main>` at all and must get `<main id="main">`
wrapped around the article body — not safely scriptable, because the wrap point differs
per file. Do a handful at a time and diff each. The **11** that already have `<main>`
need only the `id`:

```
blog/index.html  blog/beyond-plugins.html  blog/idle-self-improvement.html
blog/openclaw-101.html  blog/openclaw-agent-teams.html  blog/openclaw-integrations.html
blog/openclaw-migration.html  blog/openclaw-security.html
books/index.html  news/index.html  projects/index.html
```

Regenerate: `grep -rl '<main' --include='*.html' --exclude-dir=.claude . | sort`

## `rel="noopener noreferrer"` on the 12 external links that lack it

57 `target="_blank"` anchors exist; **45 already have `rel`**. The 12 that do not are in
`blog/api-request-lifecycle.html`, `blog/devops-security.html`,
`blog/kubernetes-orchestration.html`, `blog/linux-command-line.html`,
`blog/monitoring-observability.html` and `blog/obsidian-ai-jarvis.html`.

```bash
grep -rl 'target="_blank"' --include="*.html" --exclude-dir=.claude . \
  | xargs sed -i '' -E 's/target="_blank"(?![^>]*rel=)/target="_blank" rel="noopener noreferrer"/g' 2>/dev/null \
  || grep -rl 'target="_blank"' --include="*.html" --exclude-dir=.claude . \
     | xargs perl -pi -e 's/target="_blank"(?![^>]*rel=)/target="_blank" rel="noopener noreferrer"/g'

python3 -c "
import re,pathlib
print(sum(1 for p in pathlib.Path('.').rglob('*.html') if '.claude' not in p.parts
          for a in re.finditer(r'<a\b[^>]*>', p.read_text(encoding='utf-8'), re.S)
          if 'target=\"_blank\"' in a.group(0) and 'rel=' not in a.group(0)))"   # before 12, after 0
```

(BSD `sed` has no lookahead — the `perl` fallback is the one that will actually run.)

## Font URL trim — 27 dual-family files

Drops Inter 300 and JetBrains Mono 500/600 from the 27 dual-family blog files.
Inter 300 is used by exactly one file — `index.html`, via `style.css:231, 311, 365,
438, 485` — whose Inter-only URL this perl does not match; never trim 300 there or
five headings silently re-render at 400. JetBrains Mono 500 is unused; Mono 600 is
used once (`blog/sre-fundamentals.html:89` `.slo-card__example`), so either keep
`wght@400;600` for the mono family or restyle that one rule to 700 (already loaded)
before trimming to `wght@400`.

```bash
grep -rl "Inter:wght@300;400;500;600;700;800;900&family=JetBrains" --include="*.html" --exclude-dir=.claude . \
  | xargs perl -pi -e 's/Inter:wght\@300;400;500;600;700;800;900&family=JetBrains\+Mono:wght\@400;500;600/Inter:wght\@400;500;600;700;800;900&family=JetBrains+Mono:wght\@400/g'

grep -rl "wght@300" --include="*.html" --exclude-dir=.claude . | wc -l   # before 32, after 5 (the Inter-only index pages)
grep -rl "display=swap" --include="*.html" --exclude-dir=.claude . | wc -l   # must still be 32
```

Verify what uses the weights you are about to drop:

```bash
grep -rnE "font-weight: *300" --include="*.html" --include="*.css" --exclude-dir=.claude .
# expect exactly 5 hits, all in style.css (index.html's headings) — none in blog/
grep -rn "slo-card__example" blog/sre-fundamentals.html   # the one Mono-600 use
```

## `.post-series-footer` colour — 22 rules, all still `var(--gray)`

Re-verified 2026-08-10: a block-aware parse finds 22 rules and every one is
`color: var(--gray)`. A line-based grep reports 13 because 9 of them span lines — trust
the parse in a11y-perf R4, not the grep. `blog/claude-code-architecture.html` uses the
class with no rule for it, so the substitution is a no-op there (23 files reference the
class, 22 style it).

```bash
grep -rl "post-series-footer" --include="*.html" --exclude-dir=.claude . \
  | xargs perl -pi -e 's/(\.post-series-footer\s*\{[^}]*?color:\s*)var\(--gray\)/${1}var(--slate-light)/gs'

grep -rnE "\.post-series-footer[^{]*\{[^}]*var\(--gray\)" --include="*.html" --exclude-dir=.claude . | wc -l   # expect 0
```

## `.post-hero__meta` colour — 15 files

```bash
grep -rl "post-hero__meta" --include="*.html" --exclude-dir=.claude . \
  | xargs perl -0pi -e 's/(\.post-hero__meta\s*\{[^}]*?color:\s*)rgba\(255,255,255,0?\.\d+\)/${1}#fff/gs'

grep -rn "rgba(255,255,255,0.6)" --include="*.html" --exclude-dir=.claude . | grep post-hero__meta   # expect nothing
```

Then hand-edit the six files that also need the 0.35 black scrim — see
`references/contrast.md` section C for which and why.

## Heading defects to fix by hand

Two `<h1>` in `blog/deployment-hosting.html` — the `.post-hero__title` and a near
duplicate in the body. Demote the second. `check_site.py` INV-11 prints the current line
numbers; they have moved twice, so do not hardcode them here.

`h2 → h4` skips, count per file (re-measured 2026-08-10 — 12 posts, plus the `h1 → h3`):

```
idle-self-improvement  4      openclaw-101            2
obsidian-ai-jarvis     3      openclaw-memory         2
openclaw-agent-teams   3      openclaw-skills         2
openclaw-migration     3      api-request-lifecycle   1
beyond-plugins         1      devops-security         1
networking-fundamentals 1
openclaw-integrations  1  ← this one is h1 → h3, not h2 → h4
```

Re-detect after editing:

```bash
python3 - <<'EOF'
import re, pathlib
for p in sorted(pathlib.Path('blog').glob('*.html')):
    lv = [int(m.group(1)) for m in re.finditer(r'<h([1-6])[\s>]', p.read_text(encoding='utf8'))]
    skips = [(a,b) for a,b in zip(lv, lv[1:]) if b > a + 1]
    if skips or lv.count(1) != 1:
        print(f"{p}  h1x{lv.count(1)}  skips={skips}")
EOF
```

### `blog/index.html` is already fixed — DO NOT RUN THE OLD RECIPE

This file used to carry a `perl -pi` one-liner that rewrote `<h2 class="card__title">` to
`<h3 class="card__title">`. **Running it today would break a correct ladder.** Task 11
(`635eb94` + `4a31036`) re-cut the page and the card titles are already `<h4>`:

```bash
python3 -c "import re,collections; s=open('blog/index.html').read(); print(collections.Counter(int(m.group(1)) for m in re.finditer(r'<h([1-6])\b[^>]*>', s)))"
# → Counter({4: 37, 2: 3, 3: 2, 1: 1})
#   h1 page title -> h2 x3 .category__title -> h3 x2 .series-title -> h4 x37 .card__title
```

`<h3>` would re-collide the card titles with the `.series-title` headings they sit under.
Leave them at `h4`, and grep for them as `<h[1-6] class="card__title">`.

## Emoji icons — 8 elements

`index.html` already has 3 `aria-hidden="true"`; `blog/index.html` has 0.

```bash
perl -pi -e 's/<div class="research__icon">/<div class="research__icon" aria-hidden="true">/g' index.html
perl -pi -e 's/<span class="series-icon">/<span class="series-icon" aria-hidden="true">/g' blog/index.html
grep -rc 'aria-hidden="true"' index.html blog/index.html   # expect index.html 9, blog/index.html 2
```

## Avatar alt text — 37 identical images in `blog/index.html`

```bash
perl -pi -e 's/alt="Anirach" class="card__avatar"/alt="" class="card__avatar"/g' blog/index.html
grep -c 'alt="" class="card__avatar"' blog/index.html   # expect 37
```

## Counters — already correct; recompute, never hardcode

`b9fb125` fixed the two stale counters and Task 11 added two more sites. All five are
correct today (3 Categories / 2 Series / 37 Articles / `#cat-technology` 37 /
`#series-openclaw` 13 / `#series-devops` 24) and `check_site.py` INV-02a–INV-02e all PASS.

The old `perl -pi -e 's|<strong>33</strong> Articles|...'` recipe is dead — it matches
nothing now, and hardcoding the *next* pair of numbers would just recreate the problem.
Derive them instead:

```bash
grep -c 'class="card"' blog/index.html
python3 -c "
import re
s=open('blog/index.html',encoding='utf-8').read()
for sid,body in re.findall(r'<section class=\"series-section\" id=\"([^\"]+)\">(.*?)</section>',s,re.S):
    print(sid, len(re.findall(r'class=\"card\"',body)))"
python3 .claude/skills/site-check/scripts/check_site.py | grep INV-02
```

## Post-change smoke test

There is no CI and no test suite, so this is the whole safety net:

```bash
python3 -m http.server 8000 &
open http://localhost:8000/blog/index.html
```

Check at 375px and 1440px width, tab through the nav and the first three cards (the 2px
`:focus-visible` ring must be visible on each — it ships on every page now, so its
*absence* is the regression), and confirm the network panel shows the cover images
deferred: all 74 `<img>` tags on `blog/index.html` are `loading="lazy"`, so a first paint
should fetch roughly the first viewport's worth (≈1.7 MB), not all 4.03 MB.

And run the linter, which is the actual test suite:

```bash
python3 .claude/skills/site-check/scripts/check_site.py      # expect exit 0
python3 .claude/skills/blog-post/assets/verify-wiring.py     # expect no FAIL lines
```
