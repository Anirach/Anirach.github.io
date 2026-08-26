#!/usr/bin/env python3
"""Verify the cross-file wiring that adding/editing a blog post can break.

Stdlib only, no deps, no build step — matching the repo's design.
Run from anywhere:  python3 .claude/skills/blog-post/assets/verify-wiring.py

Scope is deliberately narrow: only the invariants a post edit touches.
Known pre-existing violations are recorded in BASELINE below, so the script
prints CLEAN on an untouched checkout and any new line is caused by your edit.
"""
import html
import os
import re
import sys
from collections import Counter, defaultdict

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
BLOG = os.path.join(ROOT, "blog")
IMAGES = os.path.join(ROOT, "images")

# --- Deliberate exceptions. Do NOT "fix" these by inventing links. -----------
CHAIN_HEAD = "git-branching.html"          # oldest DevOps post, has no nav at all
OFF_CHAIN = {                              # in #series-openclaw but wear DevOps chrome
    "claude-code-architecture.html",       # post-nav says Related / See also
    "openclaw-memory-architecture.html",   # prev grafted onto deployment-hosting
}
NO_NAV = {"beyond-plugins.html", "git-branching.html", "idle-self-improvement.html",
          "obsidian-ai-jarvis.html", "openclaw-migration.html"}
SERIES7 = ["openclaw-101.html", "openclaw-agent-teams.html", "openclaw-memory.html",
           "openclaw-security.html", "openclaw-integrations.html",
           "openclaw-skills.html", "openclaw-production.html"]
SERIES7_LABELS = ["#1 OpenClaw 101", "#2 Agent Teams", "#3 Memory & Knowledge",
                  "#4 Security & Access", "#5 Integrations", "#6 Skills & Automation",
                  "#7 Production & Scale"]
SERIES7_HREFS = ["/blog/" + f[:-5] for f in SERIES7]

# Violations that already exist on an unmodified checkout.
# Re-verified 2026-08-10 against 7867c00: exactly these two still fire.
# The two counter entries that used to live here ("hero Articles 33 != 37 cards",
# "#series-openclaw declares 12, holds 13") were fixed by b9fb125 and removed —
# a baseline entry that no longer matches a live violation is dead weight that
# hides the next real one. If you fix a baselined violation, delete its line in
# the same commit.
# Empty since 2026-08-26: the two cover-sharing keys died when scripts/make_cover.py
# gave every post its own drawn cover. Add a key only for debt you have inspected
# and can describe; the self-audit below flags any key that stops matching.
BASELINE = set()

# --- Regexes. Every one of these bit somebody during a previous audit. -------
CARD = re.compile(r'<a\s+href="([^"]+)"\s+class="card">')
# `[^>]*>` is load-bearing: 3 posts append style="text-align:right;" to the anchor.
PLINK = re.compile(r'<a\s+href="([^"]+)"\s+class="post-nav__link"[^>]*>\s*'
                   r'<div class="post-nav__dir">([^<]*)</div>\s*'
                   r'<div class="post-nav__title">(.*?)</div>', re.S)
# The container is <div> in 21 posts and <nav> in 4. Match both, and never try
# to bound the block with a non-greedy </div> — it mis-nests on every post-nav.
PNAV = re.compile(r'<(div|nav)\s+class="post-nav">')
SNAV = re.compile(r'<div class="series-nav">(.*?)</div>\s*</div>', re.S)
# href|src|srcset|poster only. Including content= turns every <meta> into a
# "broken path" and buries the real failures under ~76 false positives.
ATTR = re.compile(r'\b(href|src|srcset|poster)\s*=\s*"([^"]+)"')
CODE_SPAN = re.compile(r"<(pre|code)\b[^>]*>.*?</\1>", re.S)
EMOJI = re.compile(r"[\U0001F000-\U0001FAFF☀-➿️]")

fails, warns = [], []


def read(p):
    with open(p, encoding="utf-8") as fh:
        return fh.read()


def norm(s):
    # Inner tags stripped FIRST, matching check_site.norm_title: a card title's
    # <span lang="th"> wrapper is markup, not text. Without this the label check
    # compared bare nav text against tagged card text and warned on ~every link
    # (50 warns), which drowned the 8 real ones.
    s = re.sub(r"<[^>]+>", "", s)
    return EMOJI.sub("", html.unescape(re.sub(r"\s+", " ", s))).strip().rstrip("—").strip()


posts = sorted(f for f in os.listdir(BLOG) if f.endswith(".html") and f != "index.html")
idx = read(os.path.join(BLOG, "index.html"))

# --- card index --------------------------------------------------------------
cards, card_img, card_title = [], {}, {}
chunks = CARD.split(idx)
for i in range(1, len(chunks), 2):
    href, body = chunks[i], chunks[i + 1]
    cards.append(href)
    m = re.search(r'<img src="([^"]+)"', body)
    card_img[href] = os.path.basename(m.group(1)) if m else None
    # Heading-level agnostic ON PURPOSE. Card titles were <h2> until Task 11
    # (635eb94/4a31036) re-cut the heading ladder and made them <h4>; a
    # hardcoded <h2> silently matched 0 of 37 cards and left card_title all
    # None, which turned the title-drift check below into a no-op that always
    # printed CLEAN. Any h1-h6 with that class must keep matching.
    m = re.search(r'<(h[1-6]) class="card__title">(.*?)</\1>', body, re.S)
    card_title[href] = norm(m.group(2)) if m else None
    if m is None:
        fails.append(f"card {href} has no <hN class=\"card__title\"> — "
                     f"title-drift checking is blind for it")
sections = dict(re.findall(r'<section class="series-section" id="([^"]+)">(.*?)</section>',
                           idx, re.S))

# --- 1. link closure ---------------------------------------------------------
for p in posts:
    if p not in cards:
        fails.append(f"{p} exists but has no card in blog/index.html")
for c in cards:
    if not os.path.exists(os.path.join(BLOG, c)):
        fails.append(f"blog/index.html cards {c} but that file does not exist")
for c, n in Counter(cards).items():
    if n > 1:
        fails.append(f"{c} is carded {n} times in blog/index.html")

# --- 2. counters -------------------------------------------------------------
hero = {k.lower(): int(v) for v, k in
        re.findall(r'<span class="blog-hero__stat"><strong>(\d+)</strong>\s*([A-Za-z]+)</span>', idx)}
if hero.get("articles") != len(cards):
    fails.append(f"hero Articles {hero.get('articles')} != {len(cards)} cards")
if hero.get("series") != len(sections):
    fails.append(f"hero Series {hero.get('series')} != {len(sections)} series-section")
for sid, body in sections.items():
    actual = len(re.findall(r'class="card"', body))
    m = re.search(r'<span class="series-count">(\d+)\s*articles?</span>', body)
    declared = int(m.group(1)) if m else None
    if declared != actual:
        fails.append(f"#{sid} declares {declared}, holds {actual}")

# --- 3. nav pattern exclusivity ---------------------------------------------
kind = {}
for p in posts:
    s = read(os.path.join(BLOG, p))
    a, b = bool(SNAV.search(s)), bool(PNAV.search(s))
    if a and b:
        fails.append(f"{p} has BOTH series-nav and post-nav — pick one")
    kind[p] = "series" if a else "post" if b else "none"
    if kind[p] == "none" and p not in NO_NAV:
        fails.append(f"{p} has no nav block and is not in the NO_NAV allowlist")

# --- 4. OpenClaw 7-chip strip ------------------------------------------------
for i, f in enumerate(SERIES7):
    s = read(os.path.join(BLOG, f))
    m = SNAV.search(s)
    if not m:
        fails.append(f"{f} lost its .series-nav block")
        continue
    # Tolerates extra attributes on either tag — byte-identical to check_site.py's
    # RE_SNAV_ITEM. This file kept its own copy of the old regex when that one was
    # widened for aria-current="page" (2026-08-26) and reported 7 false failures.
    items = re.findall(r'<(a href="([^"]+)"[^>]*|span class="current"[^>]*)>([^<]*)<', m.group(1))
    if [l.strip() for _, _, l in items] != SERIES7_LABELS:
        fails.append(f"{f} series-nav labels drifted: {[l.strip() for _, _, l in items]}")
        continue
    if sum(1 for k, _, _ in items if k.startswith("span")) != 1:
        fails.append(f"{f} series-nav must have exactly one <span class=\"current\">")
    if items[i][0].startswith("a"):
        fails.append(f"{f} must be the 'current' entry at position {i + 1}, not a link")
    for j, (k, href, _) in enumerate(items):
        if k.startswith("a") and href != SERIES7_HREFS[j]:
            fails.append(f"{f} series-nav item {j + 1} points at {href}")

# --- 5. DevOps chain == reverse(#series-devops card order) -------------------
nav = {}
for p in posts:
    s = read(os.path.join(BLOG, p))
    if not PNAV.search(s):
        continue
    d = {"prev": None, "next": None, "other": [], "n": 0, "titles": {}}
    for href, dr, title in PLINK.findall(s):
        dr = dr.strip()
        d["n"] += 1
        d["titles"][href] = norm(title)
        if "Previous" in dr:
            d["prev"] = href
        elif "Next" in dr:
            d["next"] = href
        else:
            d["other"].append((dr, href))
    nav[p] = d

for p in sorted(nav):
    if nav[p]["n"] != 2:
        fails.append(f"{p} has {nav[p]['n']} .post-nav__link (expected 2)")
    for dr, href in nav[p]["other"]:
        if p not in OFF_CHAIN:
            warns.append(f"{p} uses non-standard post-nav__dir {dr!r} -> {href}")

expected = list(reversed(CARD.findall(sections.get("series-devops", ""))))
for i, f in enumerate(expected):
    want_prev = expected[i - 1] if i else None
    want_next = expected[i + 1] if i + 1 < len(expected) else "./"
    if f not in nav:
        if f != CHAIN_HEAD:
            fails.append(f"{f} is in #series-devops but has no post-nav")
        continue
    if want_prev and nav[f]["prev"] != want_prev:
        fails.append(f"{f} prev={nav[f]['prev']} but the card below it is {want_prev}")
    if nav[f]["next"] != want_next:
        fails.append(f"{f} next={nav[f]['next']} but the card above it is {want_next}")

for target, n in Counter(nav[f]["prev"] for f in nav if nav[f]["prev"]).items():
    if n > 1 and target != "deployment-hosting.html":
        fails.append(f"{target} is claimed as prev by {n} posts")

for f in sorted(nav):
    for href, t in nav[f]["titles"].items():
        if href in ("./", "."):
            continue
        ct = card_title.get(href)
        if ct and t != ct:
            warns.append(f"{f} labels {href} {t!r}; its card says {ct!r}")

# --- 6. covers ---------------------------------------------------------------
post_cover = {}
for p in posts:
    s = read(os.path.join(BLOG, p))
    found = [x for x in re.findall(r'src="\.\./images/([^"]+)"', s)
             + re.findall(r"url\(\s*['\"]?\.\./images/([^'\"\)]+)", s) if "-cover." in x]
    post_cover[p] = found[0] if found else None
    if not found:
        fails.append(f"{p} embeds no cover image")
    elif post_cover[p] != card_img.get(p):
        fails.append(f"{p} cover={post_cover[p]} but its card shows {card_img.get(p)}")

shared = defaultdict(list)
for p in posts:
    if post_cover[p]:
        shared[post_cover[p]].append(p)
for img, users in sorted(shared.items()):
    if len(users) > 1:
        fails.append(f"cover {img} shared by {', '.join(users)}")

for p in posts:
    for ext in ("png", "jpg", "jpeg", "webp"):
        cand = p[:-5] + "-cover." + ext
        if os.path.exists(os.path.join(IMAGES, cand)) and post_cover[p] != cand:
            fails.append(f"{p} ignores images/{cand} and uses {post_cover[p]}")

# --- 7. link resolution + single h1 -----------------------------------------
pages = ["index.html"] + ["blog/" + f for f in sorted(os.listdir(BLOG)) if f.endswith(".html")]
for rel in pages:
    full = os.path.join(ROOT, rel)
    s = read(full)
    here = os.path.dirname(full)
    skip = [(m.start(), m.end()) for m in CODE_SPAN.finditer(s)]
    for m in ATTR.finditer(s):
        u = m.group(2).strip()
        if u.startswith(("http", "mailto:", "tel:", "data:", "javascript:", "#")):
            continue
        q = u.split("#")[0].split("?")[0]
        if not q:
            continue
        if q.startswith("/"):
            c = os.path.join(ROOT, q.lstrip("/"))
            ok = (os.path.exists(c) or os.path.exists(c + ".html")
                  or os.path.exists(os.path.join(c, "index.html")))
        else:
            c = os.path.normpath(os.path.join(here, q))
            ok = (os.path.exists(os.path.join(c, "index.html"))
                  if q.endswith("/") or q in ("./", ".") else os.path.exists(c))
        if ok or any(a <= m.start() < b for a, b in skip):
            continue
        line = s[:m.start()].count("\n") + 1
        (warns if rel[5:] in SERIES7 else fails).append(
            f'{rel}:{line} broken {m.group(1)}="{u}"')

for p in posts:
    n = len(re.findall(r"<h1[ >]", read(os.path.join(BLOG, p))))
    if n != 1:
        fails.append(f"{p} has {n} <h1> (expected exactly 1)")

# --- report ------------------------------------------------------------------
# Self-audit: a BASELINE entry that matches nothing is a stale suppression. It
# means someone fixed the violation and left the excuse behind, which is exactly
# how this script's <h2 class="card__title"> regex went unnoticed for a sweep.
for b in sorted(BASELINE - set(fails)):
    warns.append(f"BASELINE entry is stale (no longer fires) — delete it: {b!r}")

new_fails = [f for f in fails if f not in BASELINE]
print(f"posts={len(posts)}  cards={len(cards)}  "
      f"series-nav={sum(1 for v in kind.values() if v == 'series')}  "
      f"post-nav={sum(1 for v in kind.values() if v == 'post')}  "
      f"no-nav={sum(1 for v in kind.values() if v == 'none')}")
for f in sorted(set(fails) & BASELINE):
    print("  known :", f)
for w in sorted(set(warns)):
    print("  warn  :", w)
for f in new_fails:
    print("  FAIL  :", f)
nw = len(set(warns))
# "CLEAN" must never overstate: warns do not fail the run, but a run that
# printed 10 warns is not the same as a run that printed 0, and the count is
# what tells you whether YOUR edit added one.
print(f"\nCLEAN — no new wiring breakage ({nw} warn)." if not new_fails
      else f"\n{len(new_fails)} NEW failure(s), {nw} warn. Fix before committing.")
sys.exit(1 if new_fails else 0)
