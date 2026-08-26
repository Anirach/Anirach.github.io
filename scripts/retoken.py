#!/usr/bin/env python3
"""One-shot palette re-key for anirach.com (spec 2026-08-26 §3, as corrected).

Substitutes VALUES in place — never rewrites a :root block — so each file keeps
its own indentation and the two semi-minified blocks
(blog/openclaw-memory-architecture.html, blog/vibe-coding-devops-process.html,
which write `--navy:#0f172a` with no space) stay minified.

Order matters and is enforced by the rule lists below:
  1. WHOLE_STRINGS  — two gradients whose stops would otherwise collapse into a
                      dead flat band once the hue map ran (verified by a
                      collision scan, 2026-08-26).
  2. HUE_MAP        — every retired hue, mapped once, everywhere outside :root.
  3. SELECTORS      — role fixes the hue map cannot express (footer link ink,
                      the focus ring), each of which is a real WCAG regression
                      if left to the value substitution alone.
  4. TOKENS         — the :root declarations themselves.

Usage:
    python3 scripts/retoken.py --dry-run
    python3 scripts/retoken.py --apply
    python3 scripts/retoken.py --verify     # census: must print "clean"
"""
import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

# 404.html and the two skill assets are included deliberately: 404.html shipped
# after the spec was drafted and carries its own :root, and the skill assets are
# the templates every future page is copied from — leaving them on the old
# palette would reintroduce it on the next new page.
TARGETS = ["index.html", "404.html", "style.css", "blog/*.html", "books/*.html",
           "publications/index.html", "projects/index.html", "news/index.html",
           ".claude/skills/page-design/assets/post-template.html",
           ".claude/skills/a11y-perf/assets/a11y-block.css"]

# --- 1. :root token values: name -> (old, new) ------------------------------
TOKENS = {
    "--navy":        ("#0f172a", "#11304b"),
    "--slate-light": ("#64748b", "#526174"),
    "--bg":          ("#f8fafc", "#faf7f0"),
    "--blue":        ("#6366f1", "#226299"),
    "--blue-dark":   ("#4f46e5", "#1a4d7a"),
    "--blue-light":  ("#818cf8", "#4992b9"),
}
# --- 2. tokens ADDED after --blue-light's declaration ------------------------
NEW_TOKENS = [("--gold", "#c4a46c"), ("--gold-dark", "#7a5f22"),
              ("--cloud", "#dee7e6"), ("--parchment", "#e9e1c4"),
              ("--focus", "#226299")]

# --- 3. gradients that must be replaced whole (collision fix) ---------------
WHOLE_STRINGS = [
    # #0f172a and #1e1b4b both map to #11304b -> stops 0% and 50% identical
    ("linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #312e81 100%)",
     "linear-gradient(135deg, #11304b 0%, #1a4d7a 45%, #226299 100%)"),
    # #312e81 and #4338ca both map to #1a4d7a -> stops 40% and 100% identical
    ("linear-gradient(135deg, #1e1b4b 0%, #312e81 40%, #4338ca 100%)",
     "linear-gradient(135deg, #11304b 0%, #1a4d7a 45%, #226299 100%)"),
]

# --- 4. every retired hue, mapped once --------------------------------------
HUE_MAP = {
    # periwinkle family -> the sunrise (cool light -> warm parchment)
    "#eff3ff": "#f4f7f6", "#e8f0fe": "#eef3f3", "#dde6fb": "#e4ecea",
    "#d0d9f7": "#dee7e6", "#ddd6fe": "#dee7e6", "#c7d2fe": "#e9e1c4",
    # indigo-deep family -> deep blue
    "#1e1b4b": "#11304b", "#312e81": "#1a4d7a", "#3730a3": "#226299",
    # flat inks, grounds and accents
    "#0f172a": "#11304b", "#f8fafc": "#faf7f0", "#64748b": "#526174",
    "#6366f1": "#226299", "#4f46e5": "#1a4d7a", "#818cf8": "#4992b9",
    "#4338ca": "#1a4d7a",
}
RGBA_MAP = {
    "rgba(99,102,241,": "rgba(34,98,153,", "rgba(99, 102, 241,": "rgba(34, 98, 153,",
    "rgba(79,70,229,": "rgba(26,77,122,", "rgba(79, 70, 229,": "rgba(26, 77, 122,",
    "rgba(129,140,248,": "rgba(73,146,185,", "rgba(129, 140, 248,": "rgba(73, 146, 185,",
    "rgba(15,23,42,": "rgba(17,48,75,", "rgba(15, 23, 42,": "rgba(17, 48, 75,",
}

# --- 5. role fixes the value map cannot express -----------------------------
# C1: every one of the 32 var(--blue-light) uses is footer LINK TEXT on the navy
#     ground, not a border. On the new navy it would read 3.94:1 (FAIL AA);
#     --gold is 5.73:1 there.
# C2: the focus ring carries outline-offset:3px, so it lands on the page ground;
#     inside a navy footer var(--blue) collapses to 2.12:1 (FAIL SC 1.4.11).
SELECTORS = [
    (".blog-footer a { color: var(--blue-light);", ".blog-footer a { color: var(--gold);"),
    (".footer a { color: var(--blue-light);", ".footer a { color: var(--gold);"),
    (":focus-visible { outline: 2px solid var(--blue); outline-offset: 3px; border-radius: 2px; }",
     ":focus-visible { outline: 2px solid var(--focus); outline-offset: 3px; border-radius: 2px; }\n"
     "    /* the ring sits on the page ground (3px offset). Inside the navy footers\n"
     "       and code blocks var(--blue) collapses to 2.12:1, so those scopes\n"
     "       re-point --focus to gold (5.73:1 on navy). */\n"
     "    .footer, .blog-footer, pre { --focus: var(--gold); }"),
]

STALE = ("#6366f1", "rgba(99,102,241", "rgba(99, 102, 241", "#4f46e5",
         "rgba(79,70,229", "rgba(79, 70, 229", "#818cf8", "rgba(129,140,248",
         "#4338ca", "#0f172a", "#f8fafc", "#64748b", "rgba(15,23,42",
         "rgba(15, 23, 42", "#e8f0fe", "#ddd6fe", "#c7d2fe", "#dde6fb",
         "#d0d9f7", "#eff3ff", "#1e1b4b", "#312e81", "#3730a3")

ROOT_RE = re.compile(r":root\s*\{.*?\}", re.S)


def files():
    out = []
    for pat in TARGETS:
        out.extend(sorted(ROOT.glob(pat)))
    return out


def retoken_root(block: str) -> tuple[str, int]:
    n = 0
    for name, (old, new) in TOKENS.items():
        pat = re.compile(r"(" + re.escape(name) + r"\s*:\s*)" + re.escape(old) + r"\b")
        block, k = pat.subn(lambda m: m.group(1) + new, block)
        n += k
    if "--gold" not in block:
        anchor = re.search(r"(--blue-light\s*:\s*#[0-9a-fA-F]{6};)", block)
        if anchor:
            body = block.split("{", 1)[1]
            minified = "\n" not in body.strip()[:120]
            if minified:
                add = "".join(f"{k}:{v};" for k, v in NEW_TOKENS)
            else:
                indent = re.match(r"\s*", block.splitlines()[-1]).group(0) + "  "
                add = ("\n" + indent + "/* brand — sampled from the book covers. --gold is "
                       "decorative on light grounds (2.2:1); --gold-dark is its text form. */"
                       + "\n" + indent + " ".join(f"{k}: {v};" for k, v in NEW_TOKENS))
            block = block[:anchor.end()] + add + block[anchor.end():]
            n += len(NEW_TOKENS)
    return block, n


def process(text: str) -> tuple[str, int, int]:
    root_hits = 0
    m = ROOT_RE.search(text)
    if m:
        new_block, root_hits = retoken_root(m.group(0))
        text = text[:m.start()] + new_block + text[m.end():]

    m = ROOT_RE.search(text)
    if m:
        head, block, tail = text[:m.start()], m.group(0), text[m.end():]
    else:
        head, block, tail = text, "", ""

    hits = 0
    for rules in (WHOLE_STRINGS, list(HUE_MAP.items()), list(RGBA_MAP.items()), SELECTORS):
        for old, new in rules:
            hits += head.count(old) + tail.count(old)
            head = head.replace(old, new)
            tail = tail.replace(old, new)
    return head + block + tail, root_hits, hits


def verify() -> int:
    stale = {}
    for f in files():
        t = f.read_text(encoding="utf-8")
        for pat in STALE:
            c = t.count(pat)
            if c:
                stale.setdefault(pat, []).append(f"{f.relative_to(ROOT)}:{c}")
    for pat, where in sorted(stale.items()):
        print(f"STALE {pat}: {', '.join(where[:6])}{' …' if len(where) > 6 else ''}")
    # bespoke tokens that must survive the sweep untouched
    refs = 0
    for f in files():
        refs += len(re.findall(r"var\(--(?:emerald|emerald-dark|purple-light|teal|teal2|orange|sky)\b",
                               f.read_text(encoding="utf-8")))
    print(f"bespoke var() refs still resolvable: {refs} (expected 18)")
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
    if not (a.dry_run or a.apply):
        ap.error("pass --dry-run, --apply or --verify")
    tot_r = tot_l = 0
    for f in files():
        t = f.read_text(encoding="utf-8")
        new, r, l = process(t)
        tot_r, tot_l = tot_r + r, tot_l + l
        if r or l:
            print(f"{f.relative_to(ROOT)}: {r} token value(s), {l} substitution(s)")
            if a.apply:
                f.write_text(new, encoding="utf-8")
    print(f"TOTAL: {tot_r} token values, {tot_l} substitutions across {len(files())} files")
    if not a.apply:
        print("(dry run — nothing written)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
