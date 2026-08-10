# Sitewide edits — file lists, scripts, verification

No partials exist, so every "global" change is an N-file edit. Run these from the repo
root, `/Users/anirach/Documents/Anirach.github.io`. macOS `sed` needs the empty
`-i ''` argument.

Always: work on a branch, run the verification grep afterwards, and eyeball
`git diff --stat` before committing.

## Baseline counters — re-run these, don't trust a stale number

Always exclude `.claude/` — the skill directories carry HTML templates and CSS
assets that match most of these patterns and inflate every count.

```bash
find . -name "*.html" -not -path "./.git/*" -not -path "./.claude/*" | wc -l          # 39
grep -roh "<img[^>]*>" --include="*.html" --exclude-dir=.claude . | wc -l             # 118
grep -roh "<img[^>]*>" --include="*.html" --exclude-dir=.claude . | grep -c "loading="  # 0
grep -roh "<img[^>]*>" --include="*.html" --exclude-dir=.claude . | grep -c "width="    # 0
grep -rIo ":hover"  --include="*.html" --include="*.css" --include="*.js" --exclude-dir=.claude . | wc -l   # 91
grep -rIo ":focus"  --include="*.html" --include="*.css" --include="*.js" --exclude-dir=.claude . | wc -l   #  0
grep -rIoE "outline *:" --include="*.html" --include="*.css" --exclude-dir=.claude . | wc -l     # 0  (UA ring intact)
grep -rl "prefers-reduced-motion" --include="*.html" --include="*.css" --exclude-dir=.claude . | wc -l      # 0
grep -rl "<script" --include="*.html" --exclude-dir=.claude .                         # index.html only
grep -rl "<main"   --include="*.html" --exclude-dir=.claude . | wc -l                 #  8 / 39
grep -roh 'target="_blank"' --include="*.html" --exclude-dir=.claude . | wc -l        # 21
grep -ro  'rel="noopener' --include="*.html" --exclude-dir=.claude . | wc -l          #  0
grep -rhoE '<html lang="[^"]*"' --include="*.html" --exclude-dir=.claude . | sort | uniq -c   # 37 th, 2 en
grep -c 'class="card"' blog/index.html                                                # 37
du -sh images/                                                                        # 20M
```

## The 11 files with no `:root`

A `sed` on `:root` skips these 11. The **10 blog posts** among them also load no
webfont and set their own `font-family`, so the Inter design system never reaches
them; `index.html` is different — it has no `:root` but does load Inter and does
use `style.css`.

```
index.html
blog/beyond-plugins.html          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif   (:11)
blog/idle-self-improvement.html
blog/openclaw-101.html
blog/openclaw-agent-teams.html
blog/openclaw-integrations.html
blog/openclaw-memory.html         font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif                     (:15)
blog/openclaw-migration.html
blog/openclaw-production.html
blog/openclaw-security.html
blog/openclaw-skills.html
```

Regenerate the list at any time:

```bash
for f in $(find . -name "*.html" -not -path "./.git/*" -not -path "./.claude/*"); do grep -q ":root" "$f" || echo "$f"; done
```

## Insert a CSS block into every embedded `<style>`

`assets/a11y-block.css` has no `:root` dependency beyond `--blue-dark` / `--navy`,
which is why it falls back with `var(--blue-dark, #4f46e5)` — safe in all 39 files.

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

grep -rl "prefers-reduced-motion" --include="*.html" --exclude-dir=.claude . | wc -l   # expect 39
grep -rl "focus-visible"          --include="*.html" --exclude-dir=.claude . | wc -l   # expect 39
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
grep -rl "skip-link" --include="*.html" . | wc -l   # expect 39
```

The link is useless without a target. The 31 files lacking `<main>` must get
`<main id="main">` wrapped around the article body — that one is not safely
scriptable because the wrap point differs per file. Do it a handful at a time and
diff each. The 8 that already have `<main>` just need `id="main"` added:

```
blog/index.html  blog/beyond-plugins.html  blog/idle-self-improvement.html
blog/openclaw-101.html  blog/openclaw-agent-teams.html  blog/openclaw-integrations.html
blog/openclaw-migration.html  blog/openclaw-security.html
```

## `rel="noopener noreferrer"` on all 21 external links

```bash
grep -rl 'target="_blank"' --include="*.html" --exclude-dir=.claude . \
  | xargs sed -i '' -E 's/target="_blank"(?![^>]*rel=)/target="_blank" rel="noopener noreferrer"/g' 2>/dev/null \
  || grep -rl 'target="_blank"' --include="*.html" --exclude-dir=.claude . \
     | xargs perl -pi -e 's/target="_blank"(?![^>]*rel=)/target="_blank" rel="noopener noreferrer"/g'

grep -roh '<a[^>]*target="_blank"[^>]*>' --include="*.html" . | grep -vc 'rel='   # expect 0
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

grep -rl "wght@300" --include="*.html" --exclude-dir=.claude .        # expect only index.html + blog/index.html (Inter-only URLs)
grep -rl "display=swap" --include="*.html" --exclude-dir=.claude . | wc -l    # must still be 29
```

Verify what uses the weights you are about to drop:

```bash
grep -rnE "font-weight: *300" --include="*.html" --include="*.css" --exclude-dir=.claude .
# expect exactly 5 hits, all in style.css (index.html's headings) — none in blog/
grep -rn "slo-card__example" blog/sre-fundamentals.html   # the one Mono-600 use
```

## `.post-series-footer` colour — 22 rules across 23 referencing files

`blog/claude-code-architecture.html` uses the class with no rule for it (line 598
renders with the inherited body colour); the substitution is a no-op there.

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

Two `<h1>` — `blog/deployment-hosting.html:164` (`.post-hero__title`) and `:176`.
Demote 176.

`h2 → h4` skips, count per file:

```
idle-self-improvement  4      openclaw-101          2
obsidian-ai-jarvis     3      openclaw-memory       2
openclaw-agent-teams   3      openclaw-skills       2
openclaw-migration     3      api-request-lifecycle 1
beyond-plugins         1      devops-security       1
networking-fundamentals 1
openclaw-integrations  1  ← this one is h1 (line 272) → h3 (line 282)
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

`blog/index.html` separately: 39 `<h2>`, 0 `<h3>`. The 37 `.card__title` headings
should be `<h3>` so they nest under the 2 `.series-title` `<h2>`s at lines 233 and 571.

```bash
perl -pi -e 's/<(\/?)h2 class="card__title"/<${1}h3 class="card__title"/g' blog/index.html
grep -c '<h3 class="card__title"' blog/index.html   # expect 37
grep -c '<h2' blog/index.html                       # expect 2
```

## Emoji icons — 8 elements

```bash
perl -pi -e 's/<div class="research__icon">/<div class="research__icon" aria-hidden="true">/g' index.html
perl -pi -e 's/<span class="series-icon">/<span class="series-icon" aria-hidden="true">/g' blog/index.html
grep -rc 'aria-hidden="true"' index.html blog/index.html   # index.html 8, blog/index.html 2
```

## Avatar alt text — 37 identical images in `blog/index.html`

```bash
perl -pi -e 's/alt="Anirach" class="card__avatar"/alt="" class="card__avatar"/g' blog/index.html
grep -c 'alt="" class="card__avatar"' blog/index.html   # expect 37
```

## Counters

```bash
perl -pi -e 's|<strong>33</strong> Articles|<strong>37</strong> Articles|'          blog/index.html
perl -pi -e 's|<span class="series-count">12 articles</span>|<span class="series-count">13 articles</span>|' blog/index.html
grep -n "Articles</\|series-count\">" blog/index.html
```

## Post-change smoke test

There is no CI and no test suite, so this is the whole safety net:

```bash
python3 -m http.server 8000 &
open http://localhost:8000/blog/index.html
```

Check at 375px and 1440px width, tab through the nav and the first three cards
(the focus ring must be visible on each), and confirm the network panel shows the
cover images deferred rather than all 74 firing at once.
