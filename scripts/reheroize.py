#!/usr/bin/env python3
"""Collapse the 5 post-hero gradient families to 2, and fix the ink to match.

WHY
---
The palette was re-keyed to the book jackets on 2026-08-26 — navy, cream, blue,
gold. Violet and teal are not in it, yet 16 posts wore them. Five families also
meant a cover could never be designed against a known ground: the drawn cover
system (scripts/make_cover.py) needs to know what a post's hero looks like so
the cover never vanishes into it.

    DevOps & Vibe Coding  (24 posts) -> Sunrise    (light)
    OpenClaw band         (13 posts) -> Deep Blue  (dark)

Emerald survives as books/'s identity and Deep Blue as publications/'s; neither
is a post family any more.

THE PART THAT IS NOT A FIND-AND-REPLACE
---------------------------------------
A post moving from a dark family to Sunrise inverts from white ink on dark to
navy ink on light. Miss that and the title is white-on-cream — invisible. The
ink values below are not invented: they were read off the 9 posts already on
Sunrise, where all 5 declarations are unanimous 9/9.

Worse, the 28 dark posts are not uniform. 11 declare `color:#fff` on
`.post-hero` and let it cascade; 17 set colour per element instead. So this
works element by element rather than trusting the parent.

    python3 scripts/reheroize.py --dry-run     # what would change, per file
    python3 scripts/reheroize.py --apply
    python3 scripts/reheroize.py --verify      # every post is in its target family
"""
import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
BLOG = ROOT / "blog"

SUNRISE = "linear-gradient(135deg, #eef3f3 0%, #dee7e6 50%, #e9e1c4 100%)"
DEEPBLUE = "linear-gradient(135deg, #11304b 0%, #1a4d7a 45%, #226299 100%)"

OPENCLAW = [
    "openclaw-101", "openclaw-agent-teams", "openclaw-memory", "openclaw-security",
    "openclaw-integrations", "openclaw-skills", "openclaw-production",
    "openclaw-memory-architecture", "openclaw-migration", "idle-self-improvement",
    "obsidian-ai-jarvis", "beyond-plugins", "claude-code-architecture",
]

# Read off the 9 posts already on Sunrise — unanimous, so these are the house
# values rather than a fresh opinion.
SUNRISE_INK = {
    "post-hero__title":  {"color": "var(--navy)"},
    "post-hero__meta":   {"color": "var(--slate-light)"},
    "post-hero__tag":    {"color": "var(--blue)", "background": "rgba(34,98,153,0.1)"},
    "post-hero__series": {"color": "var(--blue)"},
    "post-hero__sub":    {"color": "var(--slate)"},
}
# Deep Blue is dark, and every source family was dark too, so the ink that is
# already there stays correct. Only posts that had NO explicit colour need one.
DEEPBLUE_INK = {
    "post-hero__title":  {"color": "#fff"},
    "post-hero__meta":   {"color": "#fff"},
}

RE_HERO = re.compile(r"(\.post-hero\s*\{)([^}]*)(\})", re.S)


def family(css_body):
    return "sunrise" if "#eef3f3" in css_body else "dark"


def set_decl(block, prop, value):
    """Set one declaration inside a rule body, preserving the file's own
    indentation. Adds it if absent."""
    pat = re.compile(r"(^|;)(\s*)" + re.escape(prop) + r":\s*[^;]+;", re.M)
    if pat.search(block):
        return pat.sub(lambda m: "%s%s%s: %s;" % (m.group(1), m.group(2), prop, value),
                       block, count=1)
    indent = re.search(r"\n(\s+)\S", block)
    pad = indent.group(1) if indent else "      "
    return block.rstrip().rstrip(";") + ";\n%s%s: %s;\n%s" % (pad, prop, value, pad[:-2])


def edit_rule(s, sel, prop, value):
    m = re.search(r"(\." + re.escape(sel) + r"\s*\{)([^}]*)(\})", s, re.S)
    if not m:
        return s, False
    new = set_decl(m.group(2), prop, value)
    if new == m.group(2):
        return s, False
    return s[:m.start()] + m.group(1) + new + m.group(3) + s[m.end():], True


def process(path, apply=False):
    slug = path.stem
    s = orig = path.read_text(encoding="utf-8")
    m = RE_HERO.search(s)
    if not m:
        return slug, ["no .post-hero rule"], False

    target = "deepblue" if slug in OPENCLAW else "sunrise"
    grad = DEEPBLUE if target == "deepblue" else SUNRISE
    was = family(m.group(2))
    notes = []

    # 1. the gradient itself
    body = re.sub(r"background:\s*[^;]+;", "background: %s;" % grad, m.group(2), count=1)
    if body != m.group(2):
        notes.append("hero %s -> %s" % (was, target))
    s = s[:m.start()] + m.group(1) + body + m.group(3) + s[m.end():]

    if target == "sunrise":
        # a cascading `color:#fff` on the hero would make every child white on cream
        m2 = RE_HERO.search(s)
        body2 = re.sub(r"\s*color:\s*#fff[^;]*;", "", m2.group(2))
        if body2 != m2.group(2):
            notes.append("dropped cascading color:#fff")
        s = s[:m2.start()] + m2.group(1) + body2 + m2.group(3) + s[m2.end():]
        ink = SUNRISE_INK
    else:
        ink = DEEPBLUE_INK if was == "sunrise" else {}

    for sel, props in ink.items():
        for prop, val in props.items():
            s, changed = edit_rule(s, sel, prop, val)
            if changed:
                notes.append("%s %s -> %s" % (sel, prop, val))

    if apply and s != orig:
        path.write_text(s, encoding="utf-8")
    return slug, notes, s != orig


def verify():
    bad = []
    for p in sorted(BLOG.glob("*.html")):
        if p.stem == "index":
            continue
        m = RE_HERO.search(p.read_text(encoding="utf-8"))
        if not m:
            continue
        want = "deepblue" if p.stem in OPENCLAW else "sunrise"
        got = "sunrise" if "#eef3f3" in m.group(2) else (
            "deepblue" if "#11304b 0%" in m.group(2) else "OTHER")
        if got != want:
            bad.append("%s is %s, want %s" % (p.stem, got, want))
        if want == "sunrise" and re.search(r"color:\s*#fff", m.group(2)):
            bad.append("%s is Sunrise but still cascades color:#fff" % p.stem)
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
        for b in bad:
            print("  x", b)
        print("VERIFY %s — 37 posts, 2 families" % ("FAILED" if bad else "OK"))
        return 1 if bad else 0

    n = 0
    for p in sorted(BLOG.glob("*.html")):
        if p.stem == "index":
            continue
        slug, notes, changed = process(p, apply=a.apply)
        if changed:
            n += 1
            print("%-34s %s" % (slug, "; ".join(notes)))
    print("\n%s %d file(s)" % ("changed" if a.apply else "would change", n))
    return 0


if __name__ == "__main__":
    sys.exit(main())
