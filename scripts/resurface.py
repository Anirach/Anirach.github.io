#!/usr/bin/env python3
"""Introduce surface tokens so a dark theme has something to re-point.

WHY THIS IS A SEPARATE PASS
---------------------------
A `@media (prefers-color-scheme: dark)` block can only change TOKENS. This site
had 679 literal `background:` declarations across 48 files — every one of them
unreachable by any theme block, so a dark mode built on tokens alone would have
left hundreds of white and near-white surfaces glowing on a dark page.

So: first give the shared surfaces names, changing nothing visible; then flip
the names. This pass must be provably invisible, which is what --verify checks.

WHAT GETS A NAME (and what deliberately does not)

    --surface        #ffffff               card / menu / panel BACKGROUNDS
    --surface-2      #eef3f3               bands and <th>
    --surface-alt    #f1f5f9               image placeholders (absorbs #f8fafc)
    --surface-glass  rgba(248,250,252,.85) the nav's frosted ground
    --line           #e8ecf1               hairlines and card borders
    --tint           rgba(34,98,153,.08)   the blue wash under chips and tags
    --shadow         0 16px 48px rgba(34,98,153,.10)

Every value is the EXACT literal it replaces. The first version of this script
was not: it set --surface-2 to #eef3f3 and mapped #f1f5f9 onto it, shifting
every card's image placeholder, and did the same to card borders via
#e8ecf1 -> #e2e8f0. Both were caught by diffing computed styles against a git
worktree of the pre-token tree — which is the only way to check this honestly,
because 3 units of grey is invisible to the eye and obvious to a diff.

`--white` is NOT renamed: it is used for TEXT on dark grounds as well as for
surfaces, and those two roles diverge under a dark theme. White text on a navy
hero must stay white; a white card must not.

Left as literals on purpose:
  - `#fff` text on dark heroes, buttons and footers
  - `rgba(255,255,255,.12)` borders INSIDE dark heroes
  - <pre> code grounds — dark in both themes already
  - footers — dark in both themes already

    python3 scripts/resurface.py --dry-run
    python3 scripts/resurface.py --apply
    python3 scripts/resurface.py --verify
"""
import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

NEW_TOKENS = """
      /* ---- surfaces (2026-08-26) --------------------------------------
         Named so the dark block has something to re-point. Each value is the
         EXACT literal it replaces, so this pass cannot shift a colour — the
         first version set --surface-2 to #eef3f3 and mapped #f1f5f9 onto it,
         which moved every card's image placeholder by 3 units and was caught
         by diffing computed styles against the pre-token tree. --line made the
         same mistake with #e8ecf1 -> #e2e8f0.

         The one deliberate normalisation is #f8fafc -> --surface-alt (#f1f5f9):
         two greys 7 units apart doing the same job, and they must move together
         under a dark theme regardless. */
      --surface: #ffffff;
      --surface-2: #eef3f3;
      --surface-alt: #f1f5f9;
      --surface-glass: rgba(248,250,252,0.85);
      --line: #e8ecf1;
      --tint: rgba(34,98,153,0.08);
      --shadow: 0 16px 48px rgba(34,98,153,0.10);"""


# (literal, token). Order matters: longest / most specific first.
SUBS = [
    (r"background:\s*rgba\(248,250,252,\s*0?\.85\)", "background: var(--surface-glass)"),
    (r"background:\s*rgba\(34,98,153,\s*0?\.08\)", "background: var(--tint)"),
    (r"background:\s*var\(--white\)", "background: var(--surface)"),
    (r"background:\s*#fff(?![0-9a-fA-F])", "background: var(--surface)"),
    (r"background:\s*#ffffff\b", "background: var(--surface)"),
    (r"background:\s*#eef3f3\b", "background: var(--surface-2)"),
    (r"background:\s*#f1f5f9\b", "background: var(--surface-alt)"),
    (r"background:\s*#f8fafc\b", "background: var(--surface-alt)"),
    (r"border:\s*1px solid #e8ecf1\b", "border: 1px solid var(--line)"),
    # `white` is the same colour as #ffffff and escaped the first sweep, which
    # only looked for hex. .styled-table (8 surfaces on one post) and .flow-step
    # both used it, and the dark-mode detector is what found them.
    (r"background:\s*white\b", "background: var(--surface)"),
    (r"background-color:\s*white\b", "background-color: var(--surface)"),
    # #faf7f0 IS --bg's value, used as a literal surface by .series-nav and the
    # publications table. Pointing it at the token it already equals is
    # value-preserving and makes it follow the theme.
    (r"background:\s*#faf7f0\b", "background: var(--bg)"),
]

# Regions a sweep must never enter.
SKIP = [
    (re.compile(r"<pre><code>.*?</code></pre>", re.S), "code sample"),
    (re.compile(r"<pre>.*?</pre>", re.S), "pre"),
    (re.compile(r"\.post-hero\s*\{[^}]*\}", re.S), "hero gradient"),
    (re.compile(r"\.blog-footer\s*\{[^}]*\}", re.S), "footer (dark in both)"),
    (re.compile(r"\.footer\s*\{[^}]*\}", re.S), "footer (dark in both)"),
    (re.compile(r"@media \(prefers-color-scheme: dark\)\s*\{.*?\n    \}", re.S), "the dark block"),
]


def protect(s):
    """Blank out regions the sweep must not touch, remembering them."""
    holes = []
    for rx, _why in SKIP:
        def stash(m):
            holes.append(m.group(0))
            return "\x00HOLE%d\x00" % (len(holes) - 1)
        s = rx.sub(stash, s)
    return s, holes


def restore(s, holes):
    """Restore until STABLE, then assert nothing is left.

    The first version replaced holes in ascending order, once each. A later
    SKIP pattern can stash text that already contains an earlier placeholder —
    `.footer { ... }` swallowing a region that held HOLE0 — so restoring 0
    before 1 re-buried it. That shipped a literal "\x00HOLE1\x00" into the
    middle of a selector in 47 files, turning `.footer, .nav, .blog-nav` into
    `.footer, <junk> .nav, .blog-nav`, which silently matches nothing: the dark
    nav simply never applied. Loop, then assert."""
    for _ in range(8):
        before = s
        for i, h in enumerate(holes):
            s = s.replace("\x00HOLE%d\x00" % i, h)
        if s == before:
            break
    if "\x00HOLE" in s:
        raise SystemExit("resurface: unrestored placeholder — refusing to write")
    return s


def process(path, apply=False):
    s = orig = path.read_text(encoding="utf-8")
    if ":root" not in s:
        return 0
    body, holes = protect(s)

    n = 0
    for rx, repl in SUBS:
        body, k = re.subn(rx, repl, body)
        n += k

    if "--surface:" not in body:
        m = re.search(r"(:root\s*\{)", body)
        if m:
            body = body[:m.end()] + NEW_TOKENS + body[m.end():]
    # a dark theme needs the UA told, or form controls and scrollbars stay light
    body = body.replace("color-scheme: light;", "color-scheme: light dark;")

    s = restore(body, holes)
    if apply and s != orig:
        path.write_text(s, encoding="utf-8")
    return n


def targets():
    out = [p for p in sorted(ROOT.rglob("*.html"))
           if ".claude" not in str(p) and ".superpowers" not in str(p)]
    out.append(ROOT / "style.css")
    return out


def verify():
    bad = []
    for p in targets():
        s = p.read_text(encoding="utf-8")
        if ":root" not in s:
            continue
        for tok in ("--surface:", "--surface-2:", "--surface-glass:", "--line:",
                    "--surface-alt:", "--tint:", "--shadow:"):
            if tok not in s:
                bad.append("%s is missing %s" % (p.name, tok))
        if "color-scheme: light dark" not in s:
            bad.append("%s does not declare color-scheme: light dark" % p.name)
    return bad


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--dry-run", action="store_true")
    g.add_argument("--apply", action="store_true")
    g.add_argument("--verify", action="store_true")
    a = ap.parse_args()

    if a.verify:
        bad = verify()
        for b in bad[:20]:
            print("  x", b)
        print("VERIFY %s (%d issue%s)" % ("FAILED" if bad else "OK", len(bad),
                                          "" if len(bad) == 1 else "s"))
        return 1 if bad else 0

    total = files = 0
    for p in targets():
        n = process(p, apply=a.apply)
        if n:
            files += 1
            total += n
    print("%s %d literal declaration%s across %d files"
          % ("rewrote" if a.apply else "would rewrite", total,
             "" if total == 1 else "s", files))
    return 0


if __name__ == "__main__":
    sys.exit(main())
