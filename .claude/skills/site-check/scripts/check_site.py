#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
site-check — cross-file consistency linter for anirach.com

A hand-written static site with no build system, no package manager and no
shared partials.  Every file in blog/ carries its own <style>, its own copy of
the nav markup and its own footer, so a "global" change means editing N files
and nothing but a linter can tell you when one of them drifted.

This script is Python 3 standard library ONLY (argparse, html, os, re, sys,
collections).  No pip, no BeautifulSoup, no lxml — matching the
repository's deliberate zero-dependency design.

Usage
    python3 .claude/skills/site-check/scripts/check_site.py
    python3 .claude/skills/site-check/scripts/check_site.py --root /path/to/repo
    python3 .claude/skills/site-check/scripts/check_site.py --quiet
    python3 .claude/skills/site-check/scripts/check_site.py --check INV-05
    python3 .claude/skills/site-check/scripts/check_site.py --list
    python3 .claude/skills/site-check/scripts/check_site.py --fix

Exit status
    0  no FAIL-severity violations outside the documented baseline
    1  at least one FAIL-severity violation outside the documented baseline
    2  usage / environment error

--fix repairs ONE thing and one thing only: the article-counter values in
blog/index.html (the .blog-hero__stats "N Articles" total, the "N Series"
stat, and every .series-count).  It rewrites nothing else, ever.

=============================================================================
FOUR REGEX TRAPS.  Every one of these produced a wrong answer during the
verification pass that produced this script.  Do not "simplify" them.
=============================================================================
1.  The post-nav anchor is NOT always `<a href="..." class="post-nav__link">`.
    Three files (cicd-pipeline, frontend-performance, web-architecture) append
    `style="text-align:right;"` to the Next anchor.  A pattern ending in
    `class="post-nav__link">` silently drops those links and fabricates three
    phantom dead-ends.  `[^>]*>` is load-bearing.
2.  The post-nav container is `<div class="post-nav">` in 21 posts but
    `<nav class="post-nav">` in 4 (claude-code-architecture,
    deployment-hosting, openclaw-memory-architecture,
    vibe-coding-devops-process).  Match `<(div|nav)`.
3.  Never bound a post-nav block with a non-greedy `</div>` — the block
    contains nested divs and the match mis-nests, returning zero links.
    Anchor on the link pattern instead of on the container's closing tag.
4.  The link checker must skip <pre>/<code> spans and must NEVER read
    `content=` attributes.  Scanning content= turns every <meta name=
    "description"> and every viewport tag into a "broken path" (~76 false
    positives) and buries the 14 real ones.
=============================================================================
"""

import argparse
import html as htmlmod
import os
import re
import struct
import sys
from collections import Counter, defaultdict

# ---------------------------------------------------------------------------
# Load-bearing regexes (see the four traps above)
# ---------------------------------------------------------------------------
RE_CARD = re.compile(r'<a\s+href="([^"]+)"\s+class="card">')
RE_SECTION = re.compile(
    r'<section class="series-section" id="([^"]+)">(.*?)</section>', re.S)
RE_SERIES_COUNT = re.compile(r'(<span class="series-count">)(\d+)(\s*articles?</span>)')
RE_HERO_STAT = re.compile(
    r'(<span class="blog-hero__stat"><strong>)(\d+)(</strong>\s*([A-Za-z]+)</span>)')
# A .category block's header is a small fixed shape (icon/title/count, no
# nested divs) so it is safe to bound non-greedily on its own </div> — unlike
# a post-nav block (trap #3), there is nothing inside the header to mis-nest
# on. The category's *body* (its child series-sections or its coming-soon
# note) is NOT bounded by this regex; Site._parse_index() slices that
# positionally, from the end of one category's header to the start of the
# next (see Task 11, 2026-08-10).
RE_CATEGORY_HEAD = re.compile(
    r'<div class="category" id="([^"]+)">\s*'
    r'<div class="category__header">\s*'
    r'<span class="category__icon">[^<]*</span>\s*'
    r'<h2 class="category__title">(.*?)</h2>\s*'
    r'<span class="category__count">([^<]*)</span>\s*'
    r'</div>', re.S)
RE_SNAV = re.compile(r'<div class="series-nav">(.*?)</div>\s*</div>', re.S)
RE_SNAV_ITEM = re.compile(r'<(a href="([^"]+)"|span class="current")>([^<]*)<')
RE_PNAV_OPEN = re.compile(r'<(div|nav)\s+class="post-nav">')
RE_PLINK = re.compile(                       # trap #1: [^>]*> is load-bearing
    r'<a\s+href="([^"]+)"\s+class="post-nav__link"[^>]*>\s*'
    r'<div class="post-nav__dir">([^<]*)</div>\s*'
    r'<div class="post-nav__title">(.*?)</div>', re.S)
RE_ATTR = re.compile(r'\b(href|src|srcset|poster)\s*=\s*"([^"]+)"')  # never content=
RE_CODE_SPAN = re.compile(r'<(pre|code)\b[^>]*>.*?</\1>', re.S)      # trap #4
RE_IMG_REF = re.compile(r'(?:src|href)="([^"]*images/[^"]+)"')
# og:image / twitter:image live in content=, which RE_IMG_REF cannot see and
# RE_ATTR must never learn to read (trap #4 — the link resolver would then try
# to resolve absolute share URLs as on-disk links).  Without this, every share
# image added by the INV-27 sweep reports as an unreferenced orphan in INV-06a.
RE_META_IMG_REF = re.compile(r'content="[^"]*?/images/([^"]+)"')
RE_URL_REF = re.compile(r"url\(\s*['\"]?([^'\"\)]*images/[^'\"\)]+)")
RE_POST_COVER_SRC = re.compile(r'src="\.\./images/([^"]+)"')
RE_POST_COVER_URL = re.compile(r"url\(\s*['\"]?\.\./images/([^'\"\)]+)")
RE_LANG = re.compile(r'<html[^>]*\slang="([^"]+)"')
RE_H1 = re.compile(r'<h1[ >]')
RE_FOOTER = re.compile(r'<footer[^>]*>')
RE_COPYRIGHT = re.compile(r'©\s*(\d{4})')
RE_EXTLESS = re.compile(r'href="(/blog/[^"#?]+)"')
RE_JS_SEL = re.compile(r"querySelector(?:All)?\('([^']+)'\)|getElementById\('([^']+)'\)")
RE_EMOJI = re.compile('[\U0001F000-\U0001FAFF☀-➿️]')
RE_NAV_BLOCK = re.compile(r'<nav\b[^>]*>(.*?)</nav>', re.S)
RE_NAV_HREF = re.compile(r'href="([^"]+)"')
# INV-26: a same-directory .html link (no path segment — the first character
# class excludes "." and "/" so "../index.html" and absolute URLs never
# match).  Fragment/query tolerated, filename captured bare.
RE_SAME_DIR_HTML_HREF = re.compile(
    r'href="([A-Za-z0-9][A-Za-z0-9._-]*\.html)(?:[#?][^"]*)?"')
# INV-26 orphan direction only: an href quoted inside an HTML comment is not
# a link a visitor can follow, so it must not count as "linked".
RE_HTML_COMMENT = re.compile(r'<!--.*?-->', re.S)

# -- menu-toggle controls (INV-12) -----------------------------------------
# Task 9 replaced the JS <button class="nav__hamburger"> with a pure-CSS
# checkbox toggle on 4 of the 5 nav-bearing pages, which left the literal
# string "hamburger" alive in index.html and nowhere else — so a grep for it
# policed 1 page out of 42.  Match the CONTROL, not one page's class name.
RE_INERT_SPAN = re.compile(r'<(style|script|pre|code)\b[^>]*>.*?</\1>', re.S)
RE_ANY_TAG = re.compile(r'<([a-zA-Z][a-zA-Z0-9]*)\b([^>]*)>')
RE_MENU_TOKEN = re.compile(
    r'hamburger|burger|nav__toggle|nav-toggle|navtoggle|menu-toggle|menu__toggle',
    re.I)
RE_ATTR_ANY = re.compile(r'([A-Za-z_:][-A-Za-z0-9_:.]*)\s*=\s*"([^"]*)"')


def blank_inert(s):
    """Blank the bodies of <style>/<script>/<pre>/<code>, preserving byte
    offsets and newlines so line numbers stay accurate.  A markup-shape check
    must never fire on a CSS rule that merely *names* a class, nor on example
    markup inside a code sample (trap #4, generalised)."""
    out, last = [], 0
    for m in RE_INERT_SPAN.finditer(s):
        out.append(s[last:m.start()])
        out.append(re.sub(r"[^\n]", " ", m.group(0)))
        last = m.end()
    out.append(s[last:])
    return "".join(out)


def menu_controls(s):
    """Every menu-toggle control actually RENDERED by this page.

    Returns (js_driven, labels, checkboxes) where
      js_driven  = [(tag, attrs, pos)]   button/a/div/span carrying a menu
                   token — inert without JavaScript
      labels     = [(for_id, pos)]       <label> carrying a menu token
      checkboxes = {id: pos}             <input type="checkbox"> carrying one
    """
    js_driven, labels, checkboxes = [], [], {}
    for m in RE_ANY_TAG.finditer(blank_inert(s)):
        tag, attrs = m.group(1).lower(), m.group(2)
        if not RE_MENU_TOKEN.search(attrs):
            continue
        a = {k.lower(): v for k, v in RE_ATTR_ANY.findall(attrs)}
        if tag == "input":
            if a.get("type", "").lower() == "checkbox" and a.get("id"):
                checkboxes[a["id"]] = m.start()
        elif tag == "label":
            labels.append((a.get("for"), m.start()))
        elif tag in ("button", "a", "div", "span"):
            js_driven.append((tag, a, m.start()))
    return js_driven, labels, checkboxes


# ---------------------------------------------------------------------------
# Canonical, hand-verified constants
# ---------------------------------------------------------------------------

# The 7 numbered OpenClaw posts, in series order.
SERIES7 = [
    "openclaw-101.html",
    "openclaw-agent-teams.html",
    "openclaw-memory.html",
    "openclaw-security.html",
    "openclaw-integrations.html",
    "openclaw-skills.html",
    "openclaw-production.html",
]

# The fixed 7-entry .series-nav chip strip.  Adding an OpenClaw post means
# editing all 7 existing files, not just the new one.
SERIES_NAV_ENTRIES = [
    ("#1 OpenClaw 101", "/blog/openclaw-101"),
    ("#2 Agent Teams", "/blog/openclaw-agent-teams"),
    ("#3 Memory & Knowledge", "/blog/openclaw-memory"),
    ("#4 Security & Access", "/blog/openclaw-security"),
    ("#5 Integrations", "/blog/openclaw-integrations"),
    ("#6 Skills & Automation", "/blog/openclaw-skills"),
    ("#7 Production & Scale", "/blog/openclaw-production"),
]
SERIES_NAV_H3 = "\U0001F4DA OpenClaw for Organizations 2026"

# The 5 posts that legitimately carry no in-post navigation at all.
NO_NAV_POSTS = {
    "beyond-plugins.html",
    "git-branching.html",
    "idle-self-improvement.html",
    "obsidian-ai-jarvis.html",
    "openclaw-migration.html",
}

# git-branching.html is the head of the DevOps chain.  It has no nav block at
# all, so it cannot reciprocate cicd-pipeline's prev pointer.  This is by
# design — do NOT "fix" it by inventing a post-nav.
CHAIN_HEAD = "git-branching.html"
CHAIN_TERMINAL_NEXT = "./"

EXPECTED_COPYRIGHT_YEAR = "2026"

# The sibling landing pages that joined index.html and blog/index.html as
# full-site destinations (Task 9, 2026-08-10): books/, projects/, news/ today.
# DISCOVERED, never hardcoded — a hardcoded list meant a future talks/ or
# teaching/ directory would be invisible to every check that walks the site
# (link scan, image-orphan scan, lang, nav consistency), which is precisely
# when a linter is supposed to speak up.  The rule is deliberately narrow:
# a *top-level*, non-hidden directory that ships its own index.html is a
# section of the site.  blog/ is excluded because it is handled explicitly
# everywhere; images/ and docs/ carry no index.html and so are skipped for
# free.
DISCOVERY_EXCLUDE_DIRS = {"blog", "images", "node_modules"}


def discover_nav_sibling_dirs(root):
    """Top-level directories that publish an index.html, sorted for stable
    report ordering.  Returns e.g. ['books', 'news', 'projects']."""
    out = []
    try:
        names = os.listdir(root)
    except OSError:
        return out
    for name in sorted(names):
        if name.startswith(".") or name in DISCOVERY_EXCLUDE_DIRS:
            continue
        d = os.path.join(root, name)
        if os.path.isdir(d) and os.path.isfile(os.path.join(d, "index.html")):
            out.append(name)
    return out


def nav_pages_for(root):
    """The nav-bearing pages INV-23/INV-24 police, relative to the site root:
    home, the blog index, and every discovered section index."""
    return ["index.html", "blog/index.html"] + \
           [d + "/index.html" for d in discover_nav_sibling_dirs(root)]


def nav_dest_dirs_for(root):
    """The off-page nav destinations every nav-bearing page must link to. The
    brief's five-destination list is "home, blog, books, projects, news";
    home is checked separately (any page's own index.html target, tracked as
    found_home in INV-23) since it isn't a subdirectory like the others, and
    Contact is checked separately again since it's index.html's #contact
    anchor, not a destination page at all.  Derived from the same discovery
    as the page list, so adding a section directory adds it to the contract
    every nav must satisfy."""
    return ["blog"] + discover_nav_sibling_dirs(root)


# ---------------------------------------------------------------------------
# BASELINE — pre-existing violations verified by hand against the current
# checkout.  These are NOT suppressed: every one is still printed, tagged
# [known].  They just do not flip the exit code, so that any *new* violation
# introduced by an edit stands out instead of drowning in known debt.
#
# Each entry maps a check id to its stable violation keys — either a set
# (each key expected at most once) or a dict of key -> expected occurrence
# count, for checks where one key legitimately fires at several sites.  If a
# known violation changes shape at all, its key stops matching and it is
# re-reported as NEW; if a key re-offends MORE times than baselined, the
# extra occurrences are reported as NEW too.
#
# Deliberately NOT baselined: INV-02a and INV-02c (the stale article
# counters).  They are the thing --fix repairs, so they must fail.
# ---------------------------------------------------------------------------
BASELINE = {
    # The .series-nav <h3> drifts in exactly one of seven files.
    "INV-03b": {"openclaw-integrations.html"},

    # Two genuine chain asymmetries, both understood:
    #  - cicd-pipeline points back at the chain head, which has no nav.
    #  - openclaw-memory-architecture is grafted onto deployment-hosting.
    "INV-04a": {
        "cicd-pipeline.html|prev|git-branching.html",
        "openclaw-memory-architecture.html|prev|deployment-hosting.html",
    },
    "INV-04c": {
        "claude-code-architecture.html",
        "deployment-hosting.html",
        "openclaw-memory-architecture.html",
        "vibe-coding-devops-process.html",
    },
    "INV-04d": {
        "claude-code-architecture.html|Related",
        "claude-code-architecture.html|See also",
    },
    "INV-04f": {"deployment-hosting.html"},

    # The same 2 posts are the only nodes not reachable by walking next from
    # the chain head.  Consequence of INV-17, not an independent defect.
    "INV-04h": {"claude-code-architecture.html", "openclaw-memory-architecture.html"},

    # INV-05 (14 dead /about|/projects|/research|/contact|/teaching links in 6
    # of the 7 OpenClaw posts) was fixed in the counters/gradient/dead-links
    # cleanup — every one now points at /#about|/#projects|/#research|/#contact
    # on index.html. No baseline entry remains; a future recurrence must fail.

    # Illustrative paths inside code samples — never a real defect.
    # /css/app.css appears twice (lines 1199 and 1201, two <link> examples).
    "INV-05b": {
        "blog/frontend-performance.html|hero.jpg": 1,
        "blog/frontend-performance.html|/css/app.css": 2,
        "blog/frontend-performance.html|/fonts/inter-var.woff2": 1,
    },

    # Leftovers from a prior HTML template.  Safe to delete, nothing links them.
    "INV-06a": {
        "Opic02.jpg", "bg.jpg", "overlay.png", "pic01.jpg", "pic02.jpg",
        "pic03.jpg", "pictop.png", "xpic01.jpg", "xpic03.jpg",
    },

    # The only 2 posts with no dedicated cover asset.  The fix is to generate
    # the missing PNGs, NOT to silently re-point a card.
    "INV-07a": {"github-actions-cover.jpg", "monitoring-cover.jpg"},

    # 8 stale prev/next labels.  All but the first two are the nav label
    # dropping the target's Thai subtitle; devops-security is the worst — it
    # calls linux-command-line "Linux & Shell Essentials".
    "INV-10": {
        "claude-code-architecture.html|openclaw-101.html",
        "claude-code-architecture.html|web-architecture.html",
        "cloud-architecture.html|gitops-argocd.html",
        "deployment-hosting.html|frontend-performance.html",
        "devops-security.html|linux-command-line.html",
        "docker-compose.html|gitops-argocd.html",
        "openclaw-memory-architecture.html|deployment-hosting.html",
        "vibe-coding-devops-process.html|deployment-hosting.html",
    },

    # INV-11 (deployment-hosting.html carried two <h1>) was fixed by the
    # 2026-08-26 metadata sweep, which deleted the duplicate heading and
    # the orphaned import line beside it. No baseline entry remains; a
    # future regression must fail.

    # INV-12 (blog/index.html rendered a hamburger button but loaded no JS)
    # was fixed by Task 9: the dead button was replaced with the checkbox-
    # toggle pattern from projects/index.html. No baseline entry remains; a
    # future regression must fail.

    # INV-14 (6 posts with no <meta name="description">) was cleared by the
    # 2026-08-26 metadata sweep — all 47 pages now carry one, and INV-27
    # promotes it from warn to FAIL. No baseline entry remains.
    "INV-15": {"2025", "NONE"},
    "INV-16": {
        '<footer class="blog-footer">', '<footer class="footer">',
        '<footer class="post-footer">', '<footer>',
    },

    # Two posts sit in #series-openclaw but carry DevOps post-nav chrome.
    # They are also the only 2 nodes unreachable from the chain walk.
    "INV-17": {"claude-code-architecture.html", "openclaw-memory-architecture.html"},

    # The ordinal number is correct in all 7 posts; only the markup varies.
    "INV-20b": {".series-badge", ".series-info", "<p>", "<strong>"},
    "INV-20c": {"openclaw-memory.html"},

    # INV-22 (10 island posts with no :root block of their own) and INV-22b
    # (style.css carrying zero custom properties) were both retired by the
    # canonical :root sweep in 6670480 — every post now declares the 24-token
    # block and style.css declares it too.  The two entries then sat here dead
    # for 19 commits and were actively LAUNDERING new regressions: stripping
    # :root from openclaw-101.html and from docker-compose.html produced two
    # identical fresh violations, and only the non-baselined one was reported.
    # No baseline entry remains; a future recurrence must be reported as new.
    # INV-25 now audits the whole table for exactly this failure mode.
}

FAIL, WARN, INFO = "fail", "warn", "info"


# ---------------------------------------------------------------------------
# Plumbing
# ---------------------------------------------------------------------------
class C:
    """ANSI colours, active only when stdout is a tty."""
    on = False

    @classmethod
    def init(cls, force=None):
        cls.on = sys.stdout.isatty() if force is None else force

    @classmethod
    def _w(cls, code, s):
        return "\033[%sm%s\033[0m" % (code, s) if cls.on else s

    @classmethod
    def red(cls, s):
        return cls._w("1;31", s)

    @classmethod
    def green(cls, s):
        return cls._w("1;32", s)

    @classmethod
    def yellow(cls, s):
        return cls._w("1;33", s)

    @classmethod
    def blue(cls, s):
        return cls._w("1;34", s)

    @classmethod
    def grey(cls, s):
        return cls._w("2", s)

    @classmethod
    def bold(cls, s):
        return cls._w("1", s)


class Violation(object):
    """key is the stable identity used for baseline matching (never contains a
    line number).  detail is the human-readable message."""
    __slots__ = ("key", "detail", "known")

    def __init__(self, key, detail=None):
        self.key = key
        self.detail = detail if detail is not None else key
        self.known = False


class Check(object):
    __slots__ = ("cid", "title", "severity", "fn")

    def __init__(self, cid, title, severity, fn):
        self.cid, self.title, self.severity, self.fn = cid, title, severity, fn


CHECKS = []


def check(cid, title, severity=FAIL):
    def deco(fn):
        CHECKS.append(Check(cid, title, severity, fn))
        return fn
    return deco


def lineno(text, pos):
    return text.count("\n", 0, pos) + 1


def norm_title(s):
    """Titles must be unescaped, whitespace-collapsed and emoji-stripped before
    comparison, or `&amp;` vs `&` alone yields ~14 false positives."""
    s = htmlmod.unescape(re.sub(r"\s+", " ", s)).strip()
    s = RE_EMOJI.sub("", s)
    return s.strip().strip("—-").strip()


# ---------------------------------------------------------------------------
# Site model — everything is parsed once
# ---------------------------------------------------------------------------
class Site(object):
    def __init__(self, root):
        self.root = root
        self.blog = os.path.join(root, "blog")
        self.images = os.path.join(root, "images")
        for p in (self.blog, self.images, os.path.join(root, "index.html")):
            if not os.path.exists(p):
                raise SystemExit("not a site root (missing %s): %s" % (p, root))

        self.posts = sorted(f for f in os.listdir(self.blog)
                            if f.endswith(".html") and f != "index.html")
        self.pages = ["index.html"] + \
                     ["blog/" + f for f in sorted(os.listdir(self.blog))
                      if f.endswith(".html")]
        # The sibling landing pages (books/, projects/, news/ today, whatever
        # ships an index.html tomorrow) carry the same 5-destination nav as
        # index.html and blog/index.html and must be in every link/image/lang
        # scan too, or e.g. an image referenced only from books/index.html
        # reports as a false-positive orphan (INV-06a).
        #
        # EVERY *.html in a sibling dir is swept, not just its index.html:
        # books/ grew per-book detail pages (2026-08-23) and an index-only
        # sweep gave them zero coverage — no INV-05 link resolution, no
        # INV-06 image scan, no INV-12 nav-toggle wiring, no INV-13 lang.
        # site.nav_pages stays index-only on purpose: INV-23/INV-24 police
        # the five hand-copied section navs, and a detail page is not one.
        self.nav_sibling_dirs = discover_nav_sibling_dirs(root)
        self.nav_pages = nav_pages_for(root)
        self.nav_dest_dirs = nav_dest_dirs_for(root)
        for d in self.nav_sibling_dirs:
            self.pages.extend(
                d + "/" + f for f in sorted(os.listdir(os.path.join(root, d)))
                if f.endswith(".html"))
        self.text = {}
        for rel in self.pages:
            with open(os.path.join(root, rel), encoding="utf-8") as fh:
                self.text[rel] = fh.read()
        self.idx = self.text["blog/index.html"]
        self.images_on_disk = sorted(
            f for f in os.listdir(self.images)
            if os.path.isfile(os.path.join(self.images, f)) and not f.startswith("."))

        js = os.path.join(root, "script.js")
        self.script_js = open(js, encoding="utf-8").read() if os.path.exists(js) else ""
        css = os.path.join(root, "style.css")
        self.style_css = open(css, encoding="utf-8").read() if os.path.exists(css) else ""

        self._parse_index()
        self._parse_navs()

    def post(self, f):
        return self.text["blog/" + f]

    # -- blog/index.html --------------------------------------------------
    def _parse_index(self):
        idx = self.idx
        self.cards = []          # card hrefs, document order
        self.card_img = {}
        self.card_title = {}
        self.card_pos = {}       # href -> byte offset of the <a>
        parts = re.split(r'(<a\s+href="[^"]+"\s+class="card">)', idx)
        offset = 0
        cur = None
        for p in parts:
            m = RE_CARD.match(p)
            if m:
                cur = m.group(1)
                self.cards.append(cur)
                self.card_pos.setdefault(cur, offset)
            elif cur is not None:
                im = re.search(r'<img src="([^"]+)"', p)
                # The heading LEVEL .card__title uses is not stable — it was <h2>
                # until Task 11's fix round (2026-08-10) demoted it to <h4> to
                # repair the heading ladder (h1 -> h2 category -> h3 series ->
                # h4 card). Match any level via a backreference instead of
                # hardcoding one, so a future ladder change can't silently zero
                # out site.card_title and turn INV-10 into a check that always
                # passes because it has nothing left to compare.
                t = re.search(r'<(h[1-6]) class="card__title">(.*?)</\1>', p, re.S)
                self.card_img[cur] = os.path.basename(im.group(1)) if im else None
                self.card_title[cur] = norm_title(t.group(2)) if t else None
                cur = None
            offset += len(p)

        # (sid, body, body_offset) — body_offset is m.start(2), NOT m.start():
        # the opening <section ...> tag is ~52 bytes long and shifting the
        # window by that much lands a later match on a different line.
        self.sections = []
        for m in RE_SECTION.finditer(idx):
            self.sections.append((m.group(1), m.group(2), m.start(2)))
        self.section_cards = {}
        self.card_section = {}
        for sid, body, _off in self.sections:
            hrefs = RE_CARD.findall(body)
            self.section_cards[sid] = hrefs
            for h in hrefs:
                self.card_section[h] = sid

        self.hero_stats = {}     # label.lower() -> (value, offset)
        for m in RE_HERO_STAT.finditer(idx):
            self.hero_stats[m.group(4).lower()] = (int(m.group(2)), m.start())

        # -- category bands (Task 11, 2026-08-10) -------------------------
        # Each category's card count is derived positionally: everything
        # between the end of its own header and the start of the next
        # category's opening <div> (or end of file for the last one). That
        # correctly sums cards across a category's *multiple* child
        # series-sections (Technology has 2) without needing to balance
        # nested </div> tags.
        self.categories = []
        heads = list(RE_CATEGORY_HEAD.finditer(idx))
        for i, m in enumerate(heads):
            body_start = m.end()
            body_end = heads[i + 1].start() if i + 1 < len(heads) else len(idx)
            body = idx[body_start:body_end]
            self.categories.append({
                "id": m.group(1),
                "title": norm_title(m.group(2)),
                "count_text": htmlmod.unescape(m.group(3)).strip(),
                "count_off": m.start(3),
                "cards": len(RE_CARD.findall(body)),
            })

    # -- in-post navigation ----------------------------------------------
    def _parse_navs(self):
        self.nav = {}            # post -> dict(prev,next,other,n,tag,titles)
        for f in self.posts:
            s = self.post(f)
            m = RE_PNAV_OPEN.search(s)
            if not m:
                continue
            d = {"prev": None, "next": None, "other": [], "n": 0,
                 "tag": m.group(1), "titles": {}}
            for href, dr, title in RE_PLINK.findall(s):
                dr = dr.strip()
                d["n"] += 1
                d["titles"][href] = norm_title(title)
                if "Previous" in dr:
                    d["prev"] = href
                elif "Next" in dr:
                    d["next"] = href
                else:
                    d["other"].append((dr, href))
            self.nav[f] = d

        self.snav = {}           # post -> (h3_text, [(kind, href, label)])
        for f in self.posts:
            s = self.post(f)
            m = RE_SNAV.search(s)
            if not m:
                continue
            body = m.group(1)
            h3 = re.search(r"<h3[^>]*>(.*?)</h3>", body, re.S)
            items = [(k, h, l.strip()) for k, h, l in RE_SNAV_ITEM.findall(body)]
            self.snav[f] = (htmlmod.unescape(h3.group(1)).strip() if h3 else None,
                            items)

    # -- helpers -----------------------------------------------------------
    def code_spans(self, s):
        return [(m.start(), m.end()) for m in RE_CODE_SPAN.finditer(s)]

    def devops_chain(self):
        """The canonical DevOps reading order IS reversed(#series-devops card
        order) — verified byte-identical over 24 nodes.  blog/index.html is the
        single source of truth for the chain; never hand-author it."""
        return list(reversed(self.section_cards.get("series-devops", [])))


# ---------------------------------------------------------------------------
# INV-01 — link closure
# ---------------------------------------------------------------------------
@check("INV-01a", "every blog/*.html post is linked from blog/index.html")
def _(site):
    return [Violation(p, "blog/%s is not carded in blog/index.html" % p)
            for p in site.posts if p not in site.cards]


@check("INV-01b", "every card href in blog/index.html resolves to a real file")
def _(site):
    out = []
    for c in site.cards:
        if not os.path.exists(os.path.join(site.blog, c)):
            out.append(Violation(c, "blog/index.html:%d card -> %s (no such file)"
                                 % (lineno(site.idx, site.card_pos[c]), c)))
    return out


@check("INV-01c", "no post is carded twice")
def _(site):
    return [Violation(c, "%s appears in %d cards" % (c, n))
            for c, n in sorted(Counter(site.cards).items()) if n > 1]


# ---------------------------------------------------------------------------
# INV-02 — article counters (the thing --fix repairs)
# ---------------------------------------------------------------------------
@check("INV-02a", 'blog-hero "N Articles" == total card count')
def _(site):
    stat = site.hero_stats.get("articles")
    want = len(site.cards)
    if stat is None:
        return [Violation("missing", 'blog/index.html has no "N Articles" hero stat')]
    got, off = stat
    if got != want:
        ln = lineno(site.idx, off)
        return [Violation("articles", "blog/index.html:%d declared %d, actual %d"
                          % (ln, got, want))]
    return []


@check("INV-02b", 'blog-hero "N Series" == number of <section class="series-section">')
def _(site):
    stat = site.hero_stats.get("series")
    want = len(site.sections)
    if stat is None:
        return [Violation("missing", 'blog/index.html has no "N Series" hero stat')]
    got, off = stat
    if got != want:
        ln = lineno(site.idx, off)
        return [Violation("series", "blog/index.html:%d declared %d, actual %d"
                          % (ln, got, want))]
    return []


@check("INV-02c", ".series-count == cards inside its own series-section")
def _(site):
    out = []
    for sid, body, body_off in site.sections:
        actual = len(RE_CARD.findall(body))
        m = RE_SERIES_COUNT.search(body)
        if not m:
            out.append(Violation(sid, "#%s has no .series-count span" % sid))
            continue
        declared = int(m.group(2))
        if declared != actual:
            ln = lineno(site.idx, body_off + m.start())
            out.append(Violation(sid, "blog/index.html:%d #%s declared %d, actual %d"
                                 % (ln, sid, declared, actual)))
    return out


# The exact label an empty category (0 cards) must show instead of a number
# — "0 articles" reads like a bug, so it is a distinct, deliberate string
# rather than a numeric label of zero.
CATEGORY_COMING_SOON = "First posts coming soon"

# The two categories that intentionally carry 0 cards today (Task 11,
# 2026-08-10). Not used to *skip* them — INV-02d checks every category,
# empty or not — only referenced by fault-injection notes / commit history.
EMPTY_CATEGORIES = {"cat-academic", "cat-lifestyle"}


@check("INV-02d", ".category__count == cards inside that category "
                   "(sum of its child series), or the coming-soon label if empty")
def _(site):
    out = []
    for c in site.categories:
        ln = lineno(site.idx, c["count_off"])
        if c["cards"] == 0:
            # An empty category must show the quiet coming-soon label, never
            # a numeric "0 articles" — and never a stale positive number
            # left over from before its cards were removed.
            if c["count_text"] != CATEGORY_COMING_SOON:
                out.append(Violation(c["id"],
                    'blog/index.html:%d #%s has 0 cards but .category__count '
                    'reads %r (want %r)'
                    % (ln, c["id"], c["count_text"], CATEGORY_COMING_SOON)))
            continue
        m = re.match(r'^(\d+)\s+articles?$', c["count_text"])
        if not m:
            out.append(Violation(c["id"],
                'blog/index.html:%d #%s has %d card(s) but .category__count '
                'reads %r (want "%d articles")'
                % (ln, c["id"], c["cards"], c["count_text"], c["cards"])))
            continue
        declared = int(m.group(1))
        if declared != c["cards"]:
            out.append(Violation(c["id"],
                "blog/index.html:%d #%s declared %d, actual %d"
                % (ln, c["id"], declared, c["cards"])))
    return out


@check("INV-02e", 'blog-hero "N Categories" == number of <div class="category">')
def _(site):
    stat = site.hero_stats.get("categories")
    want = len(site.categories)
    if stat is None:
        return [Violation("missing", 'blog/index.html has no "N Categories" hero stat')]
    got, off = stat
    if got != want:
        ln = lineno(site.idx, off)
        return [Violation("categories", "blog/index.html:%d declared %d, actual %d"
                          % (ln, got, want))]
    return []


# ---------------------------------------------------------------------------
# INV-03 — the 7-entry OpenClaw series-nav chip strip
# ---------------------------------------------------------------------------
@check("INV-03", "each of the 7 OpenClaw posts has one 7-entry .series-nav, current == self")
def _(site):
    out = []
    want_labels = [e[0] for e in SERIES_NAV_ENTRIES]
    for i, f in enumerate(SERIES7):
        if f not in site.snav:
            out.append(Violation(f + "|missing", "%s has no .series-nav block" % f))
            continue
        _h3, items = site.snav[f]
        labels = [htmlmod.unescape(l) for _k, _h, l in items]
        if labels != want_labels:
            out.append(Violation(f + "|order",
                                 "%s label order %r" % (f, labels)))
            continue
        cur = [j for j, (k, _h, _l) in enumerate(items) if k.startswith("span")]
        if len(cur) != 1:
            out.append(Violation(f + "|current",
                                 "%s has %d <span class=\"current\"> (want 1)" % (f, len(cur))))
        elif cur[0] != i:
            out.append(Violation(f + "|self",
                                 "%s marks entry #%d current, should be #%d"
                                 % (f, cur[0] + 1, i + 1)))
        for j, (k, h, _l) in enumerate(items):
            if k.startswith("a") and h != SERIES_NAV_ENTRIES[j][1]:
                out.append(Violation("%s|href%d" % (f, j),
                                     "%s entry %d href=%s (want %s)"
                                     % (f, j + 1, h, SERIES_NAV_ENTRIES[j][1])))
    return out


@check("INV-03b", ".series-nav <h3> heading text identical across all 7", WARN)
def _(site):
    out = []
    for f in SERIES7:
        if f not in site.snav:
            continue
        h3 = site.snav[f][0]
        if h3 != SERIES_NAV_H3:
            out.append(Violation(f, "%s h3=%r (others: %r)" % (f, h3, SERIES_NAV_H3)))
    return out


# ---------------------------------------------------------------------------
# INV-04 — the DevOps prev/next chain
# ---------------------------------------------------------------------------
@check("INV-04a", "post-nav edges are symmetric (A.next == B  <=>  B.prev == A)")
def _(site):
    out = []
    nav = site.nav
    for f in sorted(nav):
        n, p = nav[f]["next"], nav[f]["prev"]
        if n and n != CHAIN_TERMINAL_NEXT:
            if n not in nav:
                out.append(Violation("%s|next|%s" % (f, n),
                                     "%s next->%s but %s has no post-nav" % (f, n, n)))
            elif nav[n]["prev"] != f:
                out.append(Violation("%s|next|%s" % (f, n),
                                     "%s next->%s but %s.prev=%s" % (f, n, n, nav[n]["prev"])))
        if p:
            if p not in nav:
                out.append(Violation("%s|prev|%s" % (f, p),
                                     "%s prev->%s but %s has no post-nav%s"
                                     % (f, p, p,
                                        " (chain head, by design)" if p == CHAIN_HEAD else "")))
            elif nav[p]["next"] != f:
                out.append(Violation("%s|prev|%s" % (f, p),
                                     "%s prev->%s but %s.next=%s" % (f, p, p, nav[p]["next"])))
    return out


@check("INV-04b", "every .post-nav block has exactly 2 .post-nav__link anchors")
def _(site):
    return [Violation(f, "%s has %d .post-nav__link (want 2)" % (f, site.nav[f]["n"]))
            for f in sorted(site.nav) if site.nav[f]["n"] != 2]


@check("INV-04c", ".post-nav container element is always <div>", WARN)
def _(site):
    return [Violation(f, '%s uses <%s class="post-nav">' % (f, site.nav[f]["tag"]))
            for f in sorted(site.nav) if site.nav[f]["tag"] != "div"]


@check("INV-04d", ".post-nav__dir text is '← Previous' or 'Next →'", WARN)
def _(site):
    out = []
    for f in sorted(site.nav):
        for dr, href in site.nav[f]["other"]:
            out.append(Violation("%s|%s" % (f, dr),
                                 "%s dir=%r -> %s" % (f, dr, href)))
    return out


@check("INV-04e", "prev/next chain == reversed(#series-devops card order)")
def _(site):
    expect = site.devops_chain()
    nav = site.nav
    out = []
    for i, f in enumerate(expect):
        ep = expect[i - 1] if i > 0 else None
        en = expect[i + 1] if i + 1 < len(expect) else None
        if f not in nav:
            if f != CHAIN_HEAD:
                out.append(Violation(f + "|nonav",
                                     "%s is in the chain but has no post-nav" % f))
            continue
        if ep is not None and nav[f]["prev"] != ep:
            out.append(Violation(f + "|prev",
                                 "%s prev=%s expected %s" % (f, nav[f]["prev"], ep)))
        if en is not None and nav[f]["next"] != en:
            out.append(Violation(f + "|next",
                                 "%s next=%s expected %s" % (f, nav[f]["next"], en)))
        if en is None and nav[f]["next"] != CHAIN_TERMINAL_NEXT:
            out.append(Violation(f + "|tail",
                                 "%s is the chain tail; next=%s expected %r"
                                 % (f, nav[f]["next"], CHAIN_TERMINAL_NEXT)))
    return out


@check("INV-04f", "no post is the prev of more than one other post")
def _(site):
    c = Counter(site.nav[f]["prev"] for f in site.nav if site.nav[f]["prev"])
    out = []
    for target, n in sorted(c.items()):
        if n > 1:
            claimers = sorted(f for f in site.nav if site.nav[f]["prev"] == target)
            out.append(Violation(target, "%s is claimed as prev by %d posts: %s"
                                 % (target, n, ", ".join(claimers))))
    return out


@check("INV-04g", "linter self-check: post-nav regexes tolerate the known variants", FAIL)
def _(site):
    out = []
    probe = ('<a href="x.html" class="post-nav__link" style="text-align:right;">'
             '<div class="post-nav__dir">Next →</div>'
             '<div class="post-nav__title">T</div>')
    if not RE_PLINK.search(probe):
        out.append(Violation("plink-attrs",
                             "RE_PLINK does not tolerate a trailing attribute on "
                             "the anchor (trap #1) — the linter would fabricate "
                             "phantom dead-ends"))
    if not RE_PNAV_OPEN.search('<nav class="post-nav">'):
        out.append(Violation("pnav-tag",
                             'RE_PNAV_OPEN does not match <nav class="post-nav"> (trap #2)'))
    return out


@check("INV-04h", "chain reachability: every chain node is reachable by walking next", INFO)
def _(site):
    expect = site.devops_chain()
    nav = site.nav
    # Skip the head only when it actually is the documented no-nav head.
    start = (expect[1] if (len(expect) > 1 and expect[0] == CHAIN_HEAD)
             else (expect[0] if expect else None))
    seen, cur, guard = [], start, 0
    while cur and cur in nav and cur not in seen and guard < 200:
        seen.append(cur)
        cur = nav[cur]["next"]
        if cur == CHAIN_TERMINAL_NEXT:
            break
        guard += 1
    unreached = sorted(set(nav) - set(seen))
    return [Violation(f, "%s is not reachable from the chain walk" % f)
            for f in unreached]


# ---------------------------------------------------------------------------
# INV-05 — link resolution
# ---------------------------------------------------------------------------
def _scan_links(site):
    """Returns (real_markup_violations, code_span_violations)."""
    real, incode = [], []
    for rel in site.pages:
        s = site.text[rel]
        d = os.path.dirname(os.path.join(site.root, rel))
        spans = site.code_spans(s)
        for m in RE_ATTR.finditer(s):
            u = m.group(2).strip()
            if u.startswith(("http://", "https://", "//", "mailto:", "tel:",
                             "data:", "javascript:", "#")):
                continue
            q = u.split("#")[0].split("?")[0]
            if not q:
                continue
            if q.startswith("/"):
                cand = os.path.join(site.root, q.lstrip("/"))
                ok = (os.path.exists(cand) or os.path.exists(cand + ".html")
                      or (os.path.isdir(cand) and os.path.exists(cand + "/index.html")))
            else:
                cand = os.path.normpath(os.path.join(d, q))
                if q.endswith("/") or q in ("./", "."):
                    ok = os.path.exists(os.path.join(cand, "index.html"))
                else:
                    ok = os.path.exists(cand)
            if ok:
                continue
            v = Violation("%s|%s" % (rel, u),
                          '%s:%d %s="%s"' % (rel, lineno(s, m.start()), m.group(1), u))
            (incode if any(a <= m.start() < b for a, b in spans) else real).append(v)
    return real, incode


@check("INV-05", "every relative/site-absolute href|src|srcset|poster resolves on disk")
def _(site):
    return _scan_links(site)[0]


@check("INV-05b", "refs inside <pre>/<code> that do not resolve (illustrative)", INFO)
def _(site):
    return _scan_links(site)[1]


@check("INV-09", "every extensionless /blog/<slug> link resolves")
def _(site):
    out = []
    for rel in site.pages:
        s = site.text[rel]
        for h in sorted(set(RE_EXTLESS.findall(s))):
            p = os.path.join(site.root, h.lstrip("/"))
            if not (os.path.exists(p) or os.path.exists(p + ".html")):
                out.append(Violation("%s|%s" % (rel, h), "%s -> %s" % (rel, h)))
    return out


# ---------------------------------------------------------------------------
# INV-06 — images
# ---------------------------------------------------------------------------
def _images_used(site):
    used = set()
    for rel in site.pages:
        s = site.text[rel]
        for u in (RE_IMG_REF.findall(s) + RE_URL_REF.findall(s)
                  + RE_META_IMG_REF.findall(s)):
            used.add(os.path.basename(u))
    return used


@check("INV-06a", "every file in images/ is referenced at least once", WARN)
def _(site):
    used = _images_used(site)
    return [Violation(i, "images/%s is never referenced" % i)
            for i in site.images_on_disk if i not in used]


@check("INV-06b", "every referenced image exists on disk")
def _(site):
    used = _images_used(site)
    return [Violation(u, "images/%s referenced but missing on disk" % u)
            for u in sorted(used) if not os.path.exists(os.path.join(site.images, u))]


# ---------------------------------------------------------------------------
# INV-07 — cover images
#
# Do NOT enforce <slug>-cover.*: 14 of 37 posts deliberately use short names
# (iac-cover.jpg, auth-cover.jpg, sre-cover.jpg ...).  The enforceable rules
# are 07a/07b/07c/07d below.
# ---------------------------------------------------------------------------
def _post_covers(site):
    cov = {}
    for f in site.posts:
        s = site.post(f)
        names = [x for x in RE_POST_COVER_SRC.findall(s) + RE_POST_COVER_URL.findall(s)
                 if "-cover." in x]
        cov[f] = names[0] if names else None
    return cov


@check("INV-07a", "no cover image is shared by two posts")
def _(site):
    cov = _post_covers(site)
    dd = defaultdict(list)
    for f in site.posts:
        if cov[f]:
            dd[cov[f]].append(f)
    return [Violation(k, "%s is used by %d posts: %s" % (k, len(v), ", ".join(v)))
            for k, v in sorted(dd.items()) if len(v) > 1]


@check("INV-07b", "a post's own cover == the cover on its card in blog/index.html")
def _(site):
    cov = _post_covers(site)
    return [Violation(f, "%s post=%s card=%s" % (f, cov[f], site.card_img.get(f)))
            for f in site.posts if cov[f] != site.card_img.get(f)]


@check("INV-07c", "every post embeds a cover image")
def _(site):
    cov = _post_covers(site)
    return [Violation(f, "%s has no *-cover.* image" % f)
            for f in site.posts if not cov[f]]


@check("INV-07d", "if images/<slug>-cover.* exists, the post uses it")
def _(site):
    cov = _post_covers(site)
    out = []
    for f in site.posts:
        slug = f[:-5]
        for ext in ("png", "jpg", "jpeg", "webp"):
            name = "%s-cover.%s" % (slug, ext)
            if os.path.exists(os.path.join(site.images, name)) and cov[f] != name:
                out.append(Violation(f, "%s uses %s but images/%s exists"
                                     % (f, cov[f], name)))
    return out


# ---------------------------------------------------------------------------
# INV-08 — nav pattern exclusivity
# ---------------------------------------------------------------------------
@check("INV-08", "nav patterns partition cleanly: series-nav | post-nav | none")
def _(site):
    out = []
    for f in site.posts:
        a, b = f in site.snav, f in site.nav
        if a and b:
            out.append(Violation(f + "|both", "%s has BOTH series-nav and post-nav" % f))
        if not a and not b and f not in NO_NAV_POSTS:
            out.append(Violation(f + "|neither",
                                 "%s has no nav and is not in the allowlist" % f))
        if (a or b) and f in NO_NAV_POSTS:
            out.append(Violation(f + "|unexpected",
                                 "%s is allowlisted as no-nav but now has one" % f))
    return out


# ---------------------------------------------------------------------------
# INV-10 — post-nav labels vs card titles
# ---------------------------------------------------------------------------
@check("INV-10", ".post-nav__title matches the target post's card title", WARN)
def _(site):
    out = []
    for f in sorted(site.nav):
        for href, title in sorted(site.nav[f]["titles"].items()):
            if href in ("./", "."):
                continue
            ct = site.card_title.get(href)
            if ct and norm_title(title) != norm_title(ct):
                out.append(Violation("%s|%s" % (f, href),
                                     "%s -> %s\n        nav  = %r\n        card = %r"
                                     % (f, href, title, ct)))
    return out


# ---------------------------------------------------------------------------
# INV-11 .. INV-16 — per-page hygiene
# ---------------------------------------------------------------------------
@check("INV-11", "exactly one <h1> per post")
def _(site):
    out = []
    for f in site.posts:
        s = site.post(f)
        hits = [m.start() for m in RE_H1.finditer(s)]
        if len(hits) != 1:
            out.append(Violation(f, "%s has %d <h1> (lines %s)"
                                 % (f, len(hits),
                                    ", ".join(str(lineno(s, p)) for p in hits) or "-")))
    return out


# The original INV-12 grepped the literal string "hamburger".  After Task 9
# that string survives in index.html alone (the other four nav-bearing pages
# were converted to `.nav__toggle` + `.nav__burger`), so the check policed 1
# page out of 42 and could not see the very pages most likely to regress.
# It now recognises the CONTROL in either of the two shapes this site uses,
# and asks the question that actually matters for each: a JS-driven toggle
# needs JavaScript on the page, and a CSS checkbox toggle needs both halves
# of the label/checkbox pair present or nothing happens on tap.
@check("INV-12", "every menu-toggle control is wired: JS toggles need <script>, "
                 "CSS toggles need their label+checkbox pair")
def _(site):
    out = []
    for rel in site.pages:
        s = site.text[rel]
        has_js = "<script" in s
        js_driven, labels, checkboxes = menu_controls(s)
        for tag, a, pos in js_driven:
            if not has_js:
                ident = a.get("id") or a.get("class") or tag
                out.append(Violation("%s|nojs|%s" % (rel, ident),
                                     "%s:%d renders a JS-driven menu toggle "
                                     "<%s %s> but the page has 0 <script> "
                                     "— the mobile menu is dead"
                                     % (rel, lineno(s, pos), tag, ident)))
        for for_id, pos in labels:
            if for_id is None:
                out.append(Violation("%s|label-nofor" % rel,
                                     "%s:%d menu <label> has no for= attribute "
                                     "— it toggles nothing"
                                     % (rel, lineno(s, pos))))
            elif for_id not in checkboxes and not has_js:
                out.append(Violation("%s|orphan-label|%s" % (rel, for_id),
                                     '%s:%d menu <label for="%s"> has no '
                                     '<input type="checkbox" id="%s"> and the '
                                     "page loads no JS — the mobile menu is dead"
                                     % (rel, lineno(s, pos), for_id, for_id)))
        labelled = {f for f, _p in labels}
        for cb_id, pos in sorted(checkboxes.items(), key=lambda kv: kv[1]):
            if cb_id not in labelled and not has_js:
                out.append(Violation("%s|orphan-checkbox|%s" % (rel, cb_id),
                                     '%s:%d menu checkbox id="%s" has no '
                                     "<label for> pointing at it and the page "
                                     "loads no JS — nothing can toggle it"
                                     % (rel, lineno(s, pos), cb_id)))
    return out


@check("INV-13", 'blog posts are lang="th", every other page lang="en"', WARN)
def _(site):
    out = []
    for rel in site.pages:
        m = RE_LANG.search(site.text[rel])
        # Post-detection keys on the blog/ prefix, NOT on "non-index": the
        # sibling dirs now carry non-index detail pages (books/*.html) and
        # those are section pages — lang="en" with inline <span lang="th">
        # runs, exactly like the five index pages.
        want = "th" if rel.startswith("blog/") and rel != "blog/index.html" else "en"
        if not m:
            out.append(Violation(rel, "%s has no lang attribute" % rel))
        elif m.group(1) != want:
            out.append(Violation(rel, '%s lang="%s" (want "%s")' % (rel, m.group(1), want)))
    return out


@check("INV-14", 'every post has <meta name="description">', WARN)
def _(site):
    return [Violation(f, "%s has no meta description" % f)
            for f in site.posts if '<meta name="description"' not in site.post(f)]


@check("INV-15", "footer copyright year is uniform", WARN)
def _(site):
    groups = defaultdict(list)
    for f in site.posts:
        years = sorted(set(RE_COPYRIGHT.findall(site.post(f))))
        key = "+".join(years) if years else "NONE"
        groups[key].append(f)
    out = []
    for key in sorted(groups):
        if key == EXPECTED_COPYRIGHT_YEAR:
            continue
        files = groups[key]
        label = "no © line" if key == "NONE" else "© %s" % key
        out.append(Violation(key, "%-10s %2d posts (want © %s): %s"
                             % (label, len(files), EXPECTED_COPYRIGHT_YEAR,
                                ", ".join(files[:4]) + (" ..." if len(files) > 4 else ""))))
    return out


@check("INV-16", "footer container class is uniform", WARN)
def _(site):
    c = Counter(x for f in site.posts for x in RE_FOOTER.findall(site.post(f)))
    if len(c) <= 1:
        return []
    return [Violation(tag, "%-34s %2d posts" % (tag, n))
            for tag, n in sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))]


# ---------------------------------------------------------------------------
# INV-17 .. INV-19 — series membership vs nav family
# ---------------------------------------------------------------------------
@check("INV-17", "a card's series section matches its in-post nav family", WARN)
def _(site):
    out = []
    for f in site.section_cards.get("series-openclaw", []):
        if f in site.nav:
            n = site.nav[f]
            out.append(Violation(f, "%s is carded in #series-openclaw but carries a "
                                    "DevOps .post-nav (prev=%s next=%s)"
                                 % (f, n["prev"], n["next"])))
    return out


@check("INV-18", "no #series-devops card uses the OpenClaw series-nav chip strip", WARN)
def _(site):
    return [Violation(f, "%s is in #series-devops but has a .series-nav chip strip" % f)
            for f in site.section_cards.get("series-devops", []) if f in site.snav]


@check("INV-19", "the 7 numbered OpenClaw posts all live in #series-openclaw")
def _(site):
    return [Violation(f, "%s is carded in #%s (want #series-openclaw)"
                      % (f, site.card_section.get(f)))
            for f in SERIES7 if site.card_section.get(f) != "series-openclaw"]


# ---------------------------------------------------------------------------
# INV-20 — OpenClaw ordinal badge
# ---------------------------------------------------------------------------
def _ordinal_badges(site):
    """post -> (number, markup_signature, line, raw_line)"""
    res = {}
    for f in SERIES7:
        for i, raw in enumerate(site.post(f).split("\n"), 1):
            if "OpenClaw for Organizations 2026" not in raw:
                continue
            m = re.search(r"Post #(\d+)|บทที่\s*(\d+)", raw)
            if not m:
                continue
            num = int(m.group(1) or m.group(2))
            tag = re.search(r"<(\w+)([^>]*)>", raw.strip())
            sig = "?"
            if tag:
                cls = re.search(r'class="([^"]+)"', tag.group(2) or "")
                sig = "." + cls.group(1).split()[0] if cls else "<%s>" % tag.group(1)
            res[f] = (num, sig, i, raw.strip(), bool(m.group(2)))
            break
    return res


@check("INV-20a", "the OpenClaw ordinal badge number matches series-nav position")
def _(site):
    badges = _ordinal_badges(site)
    out = []
    for i, f in enumerate(SERIES7):
        if f not in badges:
            out.append(Violation(f + "|missing", "%s has no ordinal badge" % f))
            continue
        num = badges[f][0]
        if num != i + 1:
            out.append(Violation(f + "|num", "%s says #%d, series position is #%d"
                                 % (f, num, i + 1)))
    return out


@check("INV-20b", "the OpenClaw ordinal badge uses one consistent markup form", WARN)
def _(site):
    badges = _ordinal_badges(site)
    if not badges:
        return []
    groups = defaultdict(list)
    for f in SERIES7:
        if f in badges:
            groups[badges[f][1]].append(f)
    if len(groups) <= 1:
        return []
    out = []
    for sig, files in sorted(groups.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        out.append(Violation(sig, "%-15s %d post%s: %s"
                             % (sig, len(files), "" if len(files) == 1 else "s",
                                ", ".join(files))))
    return out


@check("INV-20c", 'the OpenClaw ordinal badge is worded "Post #N"', WARN)
def _(site):
    badges = _ordinal_badges(site)
    return [Violation(f, '%s:%d writes "บทที่ %d" instead of "Post #%d"'
                      % (f, badges[f][2], badges[f][0], badges[f][0]))
            for f in SERIES7 if f in badges and badges[f][4]]


# ---------------------------------------------------------------------------
# INV-21 — script.js DOM contract
# ---------------------------------------------------------------------------
def _selector_present(sel, s):
    """Enough of a CSS-selector evaluator for the handful of hooks script.js
    actually uses: #id, .class, [attr], tag, tag[attr^="v"]."""
    sel = sel.strip()
    if sel.startswith("#"):
        return ('id="%s"' % sel[1:]) in s
    if sel.startswith("."):
        return re.search(r'class="[^"]*\b%s\b' % re.escape(sel[1:]), s) is not None
    if sel.startswith("["):
        attr = re.match(r"\[([A-Za-z0-9_-]+)", sel)
        return bool(attr) and (attr.group(1) in s)
    tag = re.match(r"^([a-zA-Z]+)", sel)
    if not tag:
        return True
    if ("<" + tag.group(1)) not in s:
        return False
    inner = re.search(r"\[([A-Za-z0-9_-]+)", sel)
    return (inner.group(1) in s) if inner else True


@check("INV-21", "every DOM hook script.js uses exists in index.html")
def _(site):
    if not site.script_js:
        return []
    home = site.text["index.html"]
    out = []
    for qsel, gid in RE_JS_SEL.findall(site.script_js):
        sel = ("#" + gid) if gid else qsel
        if not _selector_present(sel, home):
            out.append(Violation(sel, "script.js targets %s — not present in index.html" % sel))
    return out


# This check used to skip index.html — which is the only file in the repo
# that contains data-reveal, so its domain was guaranteed empty and it could
# never fire.  The exclusion is gone: the invariant is about the HOOK, not
# about one page.  style.css ships `[data-reveal] { opacity: 0 }`, so a page
# that carries the hook and never loads the script that adds `.revealed`
# doesn't just lose an animation, it renders that content invisible — which
# is exactly what the detail line now distinguishes.  Severity stays INFO
# (unchanged); the domain is now every page, so index.html losing its
# <script> tag, or a blog post inheriting a data-reveal by copy-paste, both
# report.
@check("INV-21b", "every data-reveal hook is on a page that loads JavaScript", INFO)
def _(site):
    out = []
    for rel in site.pages:
        s = site.text[rel]
        n = s.count("data-reveal")
        if n and "<script" not in s:
            hidden = ('href="../style.css"' in s or 'href="style.css"' in s
                      or "[data-reveal]" in s)
            out.append(Violation(rel, "%s has %d data-reveal hook%s but loads no JS "
                                      "— the reveal animation never fires%s"
                                 % (rel, n, "" if n == 1 else "s",
                                    " and the opacity:0 rule leaves that content "
                                    "invisible" if hidden else "")))
    return out


# ---------------------------------------------------------------------------
# INV-22 — per-post :root
# ---------------------------------------------------------------------------
@check("INV-22", "every post defines its own :root custom-property block", WARN)
def _(site):
    return [Violation(f, "%s defines no :root block" % f)
            for f in site.posts if ":root" not in site.post(f)]


@check("INV-22b", "style.css custom properties (CLAUDE.md claims they exist)", INFO)
def _(site):
    if not site.style_css:
        return []
    roots = site.style_css.count(":root")
    uses = site.style_css.count("var(")
    if roots == 0 and uses == 0:
        return [Violation("style.css",
                          "style.css has 0 :root blocks and 0 var() uses — it is hex "
                          "literals only, so CLAUDE.md's \"use --navy/--blue from "
                          "style.css\" guidance cannot be followed there")]
    return []


# ---------------------------------------------------------------------------
# INV-23 — 5-page nav consistency (Task 9, 2026-08-10; home check added in
# fix round 1 after review Finding 1 — see below)
#
# The page list and the destination list are DISCOVERED (see
# discover_nav_sibling_dirs) rather than hardcoded, so a new top-level
# section directory is policed the day it appears instead of the day someone
# remembers to edit this file.
#
# index.html, blog/index.html, books/index.html, projects/index.html and
# news/index.html each carry their own hand-copied <nav>. Every one of them
# must link to all 5 destinations the brief names — home, blog, books,
# projects, news — plus index.html's #contact section is checked separately
# (index.html itself trivially satisfies "home" via its own logo link; the
# real target of the home check is the 4 sibling pages). Every relative href
# inside that <nav> must resolve to something real on disk — a page that
# looks fine but 404s on click is worse than a page that never linked there
# at all.
#
# Home and Contact are tracked as two INDEPENDENT booleans on purpose: a
# fault-injection test proved that folding "home" into the Contact check
# lets a page silently lose its way back to home as long as
# "../index.html#contact" is still present elsewhere in the nav (that
# href resolves to index.html too, but it is not what a reader would call
# a "way back home" link). So a link only counts toward found_home if its
# fragment is anything OTHER than "contact"; the bare logo link
# (`../index.html`, no fragment) is the one expected to satisfy it.
# ---------------------------------------------------------------------------
@check("INV-23", "every nav-bearing page links to all 5 destinations, every nav href resolves")
def _(site):
    out = []
    root_index = os.path.normpath(os.path.join(site.root, "index.html"))
    for rel in site.nav_pages:
        s = site.text.get(rel)
        if s is None:
            out.append(Violation(rel + "|missing-page", "%s does not exist" % rel))
            continue
        m = RE_NAV_BLOCK.search(s)
        if not m:
            out.append(Violation(rel + "|missing-nav", "%s has no <nav>...</nav> element" % rel))
            continue
        page_dir = os.path.dirname(os.path.join(site.root, rel))
        found_dirs, found_contact, found_home = set(), False, False
        for href in RE_NAV_HREF.findall(m.group(1)):
            if href.startswith(("http://", "https://", "mailto:", "tel:", "javascript:")):
                continue
            path_part, _, frag = href.partition("#")
            path_part = path_part.split("?")[0]
            if path_part == "":
                cand = os.path.join(site.root, rel)              # anchor-only: same page
            elif path_part.startswith("/"):
                cand = os.path.join(site.root, path_part.lstrip("/"))
            else:
                cand = os.path.normpath(os.path.join(page_dir, path_part))
            exists = (os.path.exists(cand) or os.path.exists(cand + ".html")
                      or (os.path.isdir(cand) and os.path.exists(os.path.join(cand, "index.html"))))
            if not exists:
                out.append(Violation("%s|badhref|%s" % (rel, href),
                                     '%s: nav href "%s" does not resolve on disk' % (rel, href)))
                continue
            norm = os.path.normpath(cand)
            if norm == root_index:
                if frag == "contact":
                    found_contact = True
                else:
                    found_home = True
            elif os.path.isdir(norm):
                base = os.path.basename(norm)
                if base in site.nav_dest_dirs:
                    found_dirs.add(base)
            elif os.path.basename(norm) == "index.html":
                parent = os.path.basename(os.path.dirname(norm))
                if parent in site.nav_dest_dirs:
                    found_dirs.add(parent)
        missing_dirs = [d for d in site.nav_dest_dirs if d not in found_dirs]
        if missing_dirs:
            out.append(Violation(rel + "|missing-dest|" + ",".join(missing_dirs),
                                 "%s nav has no link resolving to: %s"
                                 % (rel, ", ".join(missing_dirs))))
        if not found_home:
            out.append(Violation(rel + "|missing-home",
                                 "%s nav has no link resolving to index.html (home)" % rel))
        if not found_contact:
            out.append(Violation(rel + "|missing-contact",
                                 "%s nav has no link resolving to index.html#contact" % rel))
    return out


# ---------------------------------------------------------------------------
# INV-24 — page-chrome uniformity across the NAV-BEARING pages
#
# INV-14 (meta description), INV-15 (footer year) and INV-16 (footer class)
# all iterate site.posts, so blog/index.html and the landing pages sit
# outside their loop entirely.  Nothing policed them — which is how a
# "© 2025" footer survived on blog/index.html while the other four landing
# pages read 2026.  This check closes that hole for the two properties a
# reader actually notices.
#
# The year is checked for CONSISTENCY, not against a constant: the whole
# point is that these five hand-copied footers must agree with each other,
# and pinning a literal year here just means the linter goes red every 1
# January for a reason that isn't drift.  The modal year wins; every page
# that disagrees (or shows no © line at all) is named.  Severity is WARN, to
# match its three siblings INV-14/15/16 which police the same two properties
# over posts.
# ---------------------------------------------------------------------------
@check("INV-24", "nav-bearing pages agree on the footer © year and all carry "
                 "a meta description", WARN)
def _(site):
    out = []
    years, missing_desc = {}, []
    for rel in site.nav_pages:
        s = site.text.get(rel)
        if s is None:
            out.append(Violation(rel + "|missing-page", "%s does not exist" % rel))
            continue
        found = sorted(set(RE_COPYRIGHT.findall(s)))
        years[rel] = "+".join(found) if found else "NONE"
        if '<meta name="description"' not in s:
            missing_desc.append(rel)

    if years:
        groups = defaultdict(list)
        for rel, key in years.items():
            groups[key].append(rel)
        # modal year wins; ties break on the key so the report is stable
        majority = sorted(groups, key=lambda k: (-len(groups[k]), k))[0]
        for rel in sorted(years):
            if years[rel] == majority:
                continue
            shown = "no © line" if years[rel] == "NONE" else "© " + years[rel]
            out.append(Violation(rel + "|year",
                                 "%s footer shows %s but %d of the %d nav-bearing "
                                 "pages show © %s"
                                 % (rel, shown, len(groups[majority]),
                                    len(years), majority)))
    for rel in sorted(missing_desc):
        out.append(Violation(rel + "|desc",
                             '%s has no <meta name="description">' % rel))
    return out


# ---------------------------------------------------------------------------
# INV-25 — the linter audits its own BASELINE
#
# A baseline entry is a promise: "this violation exists today, we understand
# it, do not fail the build for it".  When the underlying debt is repaired
# and nobody deletes the entry, that promise silently becomes a suppression
# rule for a violation that no longer exists — and the next time the same
# defect is reintroduced it is absorbed as [known] and the build stays
# green.  That is not hypothetical: INV-22's 10 keys and INV-22b's 1 key
# outlived their debt by 19 commits and four linter-editing tasks, and a
# fresh :root regression injected into openclaw-101.html was laundered by
# them while the identical regression in docker-compose.html was reported.
#
# So: every baselined key must still match at least one live violation, and
# a key baselined for N occurrences must still fire N times.  A baseline
# that has gone stale is now a FAIL, on the same footing as the regressions
# it would otherwise hide.  Re-running each baselined check costs ~17 extra
# check invocations against an already-parsed Site (~40 ms total).
# ---------------------------------------------------------------------------
@check("INV-25", "linter self-audit: no BASELINE entry is stale "
                 "(every baselined key still matches a live violation)")
def _(site):
    out = []
    by_id = {c.cid: c for c in CHECKS}
    for cid in sorted(BASELINE, key=cid_sort_key):
        base = BASELINE[cid]
        allowed = dict(base) if isinstance(base, dict) else {k: 1 for k in base}
        chk = by_id.get(cid)
        if chk is None:
            out.append(Violation(cid + "|no-such-check",
                                 "BASELINE has an entry for %s but no such check "
                                 "is registered — it suppresses nothing and "
                                 "hides a renamed check" % cid))
            continue
        live = Counter()
        for v in chk.fn(site) or []:
            live[v.key if isinstance(v, Violation) else str(v)] += 1
        for key in sorted(allowed):
            n_live, n_allowed = live.get(key, 0), allowed[key]
            if n_live == 0:
                out.append(Violation("%s|%s|dead" % (cid, key),
                                     "BASELINE[%s] key %r matches 0 live "
                                     "violations — the debt it documented is "
                                     "gone; delete the entry, or it will "
                                     "silently absorb the next regression that "
                                     "reuses this key"
                                     % (cid, key)))
            elif n_live < n_allowed:
                out.append(Violation("%s|%s|overcount" % (cid, key),
                                     "BASELINE[%s] key %r allows %d occurrences "
                                     "but only %d fire — lower it to %d, the "
                                     "spare slot suppresses a future regression"
                                     % (cid, key, n_allowed, n_live, n_live)))
    return out


# ---------------------------------------------------------------------------
# INV-26 — section-dir detail pages: the mirror of INV-01a/b for the sibling
# dirs.  books/ grew per-book detail pages (2026-08-23); Site.pages now
# sweeps every *.html in a sibling dir (INV-05/06/12/13 coverage), but none
# of the above ties a detail page to its own section index — an orphan
# detail page is unreachable from the site, and a card href to a file that
# does not exist 404s on the section that advertises it.  The two directions
# read different texts, deliberately:
#   orphan — comment-STRIPPED index text.  An href quoted inside an HTML
#     comment is not a link a visitor can follow, so a detail page whose only
#     mention is commented out is still an orphan.  Scanning raw text here
#     let a commented-out card mark its target "linked" and mute the check.
#   dead — RAW text, matching INV-05's deliberate policy that comments in
#     this repo never quote an unresolvable href (books/index.html spelled
#     its wrap-pending attributes in prose for exactly this reason).
# ---------------------------------------------------------------------------
@check("INV-26", "every sibling-dir detail page is linked from its dir's "
                 "index.html, and every same-dir .html link there resolves")
def _(site):
    out = []
    for d in site.nav_sibling_dirs:
        idx_rel = d + "/index.html"
        idx = site.text.get(idx_rel, "")
        ddir = os.path.join(site.root, d)
        details = sorted(f for f in os.listdir(ddir)
                         if f.endswith(".html") and f != "index.html")
        hrefs = set(RE_SAME_DIR_HTML_HREF.findall(idx))
        linked = set(RE_SAME_DIR_HTML_HREF.findall(RE_HTML_COMMENT.sub("", idx)))
        for f in details:
            if f not in linked:
                out.append(Violation("%s|orphan|%s" % (d, f),
                                     "%s/%s exists but %s never links it"
                                     % (d, f, idx_rel)))
        for h in sorted(hrefs):
            if h != "index.html" and not os.path.isfile(os.path.join(ddir, h)):
                out.append(Violation("%s|dead|%s" % (d, h),
                                     '%s links href="%s" but %s/%s does not exist'
                                     % (idx_rel, h, d, h)))
    return out




# ---------------------------------------------------------------------------
# INV-27 — the social / canonical head block
#
# Nothing in this repo generates a <head>.  Every one of the 47 pages carries
# a hand-copied one, which is exactly the shape of drift the other 26 checks
# exist for — except that a wrong canonical or a stale og:url is invisible in
# a browser.  It only shows up in a search result, a Slack unfurl or a Line
# preview, i.e. somewhere nobody on this project ever looks.
#
# So every value this check can DERIVE, it derives, and compares the file's
# text against the derivation — never one hand-typed tag against another:
#   canonical/og:url  <- the file's own path on disk (canonical_path_for)
#   og:locale         <- the same blog/-prefix rule INV-13 uses for lang=
#   og:image w/h      <- the actual pixel dimensions of the actual file,
#                        parsed out of the PNG IHDR chunk / the JPEG SOF
#                        marker with struct (image_pixel_size).  Pillow is
#                        not a dependency and must never become one.
# The only value compared against a constant is og:site_name, which is a
# constant by definition.
#
# NOTE ON TRAP #4: this is the one check in the file that deliberately reads
# content=".  Trap #4 forbids that to the LINK scanner (RE_ATTR), because a
# viewport or description string is not a path — it does not forbid it to a
# metadata checker, which has nothing else to read.  RE_ATTR is untouched;
# the two regexes below are INV-27's own.  Both are applied to blank_inert()
# text so that a <code> sample showing an og: tag can never satisfy — or
# break — a real page's head block.
#
# A page with no social head AT ALL reports ONE violation, not eight: the
# fix is a single block, and eight lines per page would bury the pages that
# have a block with something wrong inside it.  Facet (h), the meta
# description, is scored separately — it is ordinary <head> hygiene, not
# part of the social block, and it is the one facet that already exists on
# most pages.
# ---------------------------------------------------------------------------
SITE_ORIGIN = "https://anirach.com"
SITE_IMAGE_PREFIX = SITE_ORIGIN + "/images/"
OG_SITE_NAME = "Anirach Mingkhwan"
OG_LOCALE_TH = "th_TH"
OG_LOCALE_EN = "en_US"

# Presence-and-non-empty only; their VALUES are checked individually below
# where a value is derivable (og:url, og:image, og:site_name, og:locale).
REQUIRED_SOCIAL_TAGS = (
    "og:title", "og:description", "og:image", "og:type",
    "og:site_name", "og:locale", "twitter:card",
)

RE_LINK_TAG = re.compile(r"<link\b[^>]*>", re.I)
RE_META_TAG = re.compile(r"<meta\b[^>]*>", re.I)

# JPEG start-of-frame markers.  0xC4 (DHT), 0xC8 (JPG) and 0xCC (DAC) live in
# the same 0xC0-0xCF range and are NOT frame headers — reading dimensions out
# of a Huffman table returns confident garbage.
JPEG_SOF_MARKERS = frozenset(
    set(range(0xC0, 0xD0)) - {0xC4, 0xC8, 0xCC})


def image_pixel_size(path):
    """(width, height) of a PNG or JPEG on disk, or None if it is neither /
    is truncated / is a format this stdlib-only reader cannot measure.

    PNG:  the IHDR chunk is mandatory and mandatory-first — width and height
          are two big-endian uint32 at a fixed offset of 16.
    JPEG: walk the marker segments until a SOF; its payload is
          precision(1) height(2) width(2), height FIRST.  Walking is
          required, not optional: a cover with an EXIF/ICC block in front of
          the frame header puts the SOF hundreds of bytes in."""
    try:
        with open(path, "rb") as fh:
            head = fh.read(24)
            if head[:8] == b"\x89PNG\r\n\x1a\n" and head[12:16] == b"IHDR":
                if len(head) < 24:
                    return None
                w, h = struct.unpack(">II", head[16:24])
                return (int(w), int(h))
            if head[:2] != b"\xff\xd8":
                return None
            fh.seek(2)
            for _ in range(256):                 # guard: no unbounded walk
                b = fh.read(1)
                while b and b != b"\xff":        # resync on the marker byte
                    b = fh.read(1)
                if not b:
                    return None
                m = fh.read(1)
                while m == b"\xff":              # 0xFF fill bytes
                    m = fh.read(1)
                if not m:
                    return None
                mk = m[0]
                if mk in (0x01, 0xD8) or 0xD0 <= mk <= 0xD7:
                    continue                     # standalone, no payload
                if mk in (0xD9, 0xDA):
                    return None                  # end of header, no SOF seen
                raw = fh.read(2)
                if len(raw) < 2:
                    return None
                (seglen,) = struct.unpack(">H", raw)
                if mk in JPEG_SOF_MARKERS:
                    seg = fh.read(5)
                    if len(seg) < 5:
                        return None
                    h, w = struct.unpack(">HH", seg[1:5])
                    return (int(w), int(h))
                if seglen < 2:
                    return None
                fh.seek(seglen - 2, 1)
    except (OSError, struct.error):
        return None
    return None


def canonical_path_for(rel):
    """The ONE canonical path a page at `rel` may claim, derived from where
    the file sits.  index.html anywhere is its directory, with the trailing
    slash and without the filename (GitHub Pages serves /books/ and
    /books/index.html as the same document; only one of them may be
    advertised).  Everything else keeps its .html, matching the URL form the
    site's own cards and post-navs already link."""
    rel = rel.replace(os.sep, "/")
    d, base = os.path.split(rel)
    if base == "index.html":
        return "/" + (d + "/" if d else "")
    return "/" + rel


def canonical_url_for(rel):
    return SITE_ORIGIN + canonical_path_for(rel)


def og_locale_for(rel):
    """Same domain rule as INV-13's lang= check, and for the same reason: a
    blog post is Thai prose, every index and every section detail page is
    English chrome."""
    return (OG_LOCALE_TH
            if rel.startswith("blog/") and rel != "blog/index.html"
            else OG_LOCALE_EN)


def social_head(s):
    """(canonical_hrefs, tags) for one page.

    canonical_hrefs  [href, ...] in document order, one per
                     <link rel="canonical"> — a LIST, because "exactly one"
                     is the invariant and a count of 2 must be reportable.
    tags             {key: content} for every <meta> carrying a property= or
                     name= of og:*/twitter:*/description, first occurrence
                     wins.  Both attribute spellings are accepted: og: is
                     property= per the OGP spec, twitter: and description are
                     name=, and enough of the world emits the other spelling
                     that policing WHICH attribute carries the key would fail
                     pages whose preview actually works."""
    s = blank_inert(s)
    canon = []
    for m in RE_LINK_TAG.finditer(s):
        a = {k.lower(): v for k, v in RE_ATTR_ANY.findall(m.group(0))}
        if a.get("rel", "").strip().lower() == "canonical":
            canon.append(a.get("href", ""))
    tags = {}
    for m in RE_META_TAG.finditer(s):
        a = {k.lower(): v for k, v in RE_ATTR_ANY.findall(m.group(0))}
        key = (a.get("property") or a.get("name") or "").strip().lower()
        if not key:
            continue
        if key == "description" or key.startswith(("og:", "twitter:")):
            tags.setdefault(key, a.get("content", ""))
    return canon, tags


@check("INV-27", "every page carries a self-consistent social/canonical head block")
def _(site):
    out = []
    for rel in site.pages:
        s = site.text[rel]
        canon, tags = social_head(s)
        want_url = canonical_url_for(rel)

        def bad(facet, detail):
            out.append(Violation("%s|%s" % (rel, facet), "%s %s" % (rel, detail)))

        # (h) — scored for EVERY page, block or no block.  INV-14 asks the
        # same question of posts only, and only warns.
        desc = htmlmod.unescape(tags.get("description", "")).strip()
        if "description" not in tags:
            bad("meta-description", 'has no <meta name="description">')
        elif not desc:
            bad("meta-description", 'has an empty <meta name="description" content="">')

        # A page with no social block: ONE violation, not eight.  This fires on
        # "no og:/twitter: tags at all" regardless of the canonical, because a
        # page that has a stray canonical but no og: block is the same missing
        # block — and reporting its eight absent tags individually is exactly
        # the bury-the-signal case this short-circuit exists to prevent.
        if not any(k.startswith(("og:", "twitter:")) for k in tags):
            bad("no-social-head",
                "carries no og:/twitter: meta at all%s — wants the whole block "
                "(canonical %s)"
                % ("" if not canon else ", though it does declare a canonical",
                   want_url))
            continue

        # (a) canonical: exactly one, right origin, path derived from the
        # file's own location, never .../index.html.
        href, canon_bad = None, False
        if not canon:
            bad("canonical-missing",
                'has og:/twitter: meta but no <link rel="canonical"> '
                '(want href="%s")' % want_url)
            canon_bad = True
        else:
            if len(canon) > 1:
                bad("canonical-dup",
                    'declares %d <link rel="canonical"> (want exactly 1): %s'
                    % (len(canon), ", ".join(repr(h) for h in canon)))
                canon_bad = True
                href = None          # the duplicate IS the finding; do not also
                                     # grade whichever href happened to come first
            else:
                href = canon[0]
            if href is None:
                pass
            elif not href.startswith(SITE_ORIGIN):
                bad("canonical-origin",
                    'canonical %r does not start with "%s"' % (href, SITE_ORIGIN))
                canon_bad = True
            elif href.endswith("/index.html"):
                bad("canonical-index",
                    "canonical %r ends in /index.html — the directory form %r "
                    "is the one URL this page may advertise" % (href, want_url))
                canon_bad = True
            elif href != want_url:
                bad("canonical-path",
                    "canonical %r does not match the path this file sits at "
                    "(want %r)" % (href, want_url))
                canon_bad = True

        # (b) og:url == want_url.  The separate "og:url must equal the canonical
        # href" comparison that used to live here was DEAD CODE: reaching it
        # required href == want_url and ogurl == want_url, so the two were
        # already equal by construction.  Both values are graded against the
        # same derivation instead, which is the stronger check anyway — and one
        # typo still produces one violation, not two.
        if "og:url" not in tags:
            bad("og:url", "has no og:url (want %r)" % want_url)
        else:
            ogurl = tags["og:url"]
            if ogurl != want_url:
                bad("og:url",
                    "og:url %r does not match the path this file sits at "
                    "(want %r)" % (ogurl, want_url))

        # (c) the seven presence-only tags.
        for key in REQUIRED_SOCIAL_TAGS:
            if key not in tags:
                bad(key, "has no %s" % key)
            elif not tags[key].strip():
                bad(key, 'has %s with an empty content=""' % key)

        # (d) og:image absolute, under /images/, and on disk.
        img = tags.get("og:image", "").strip()
        img_path = None
        if img:
            if not img.startswith(SITE_IMAGE_PREFIX):
                bad("og:image-url",
                    'og:image %r is not an absolute "%s..." URL — a relative '
                    "or off-origin og:image does not unfurl"
                    % (img, SITE_IMAGE_PREFIX))
            else:
                name = img[len(SITE_ORIGIN):].split("#")[0].split("?")[0]
                name = name.lstrip("/")
                # normpath + the images/ containment test: a ".." in the URL
                # must report as missing, never resolve to a file elsewhere
                # in the checkout and quietly pass.
                cand = os.path.normpath(os.path.join(site.root, name))
                if (cand.startswith(site.images + os.sep)
                        and os.path.isfile(cand)):
                    img_path = cand
                else:
                    bad("og:image-file",
                        "og:image %r has no file on disk at %s" % (img, name))

        # (e) declared dimensions vs the file's real pixels.  Absent is
        # allowed (they are optional tags); wrong is not — a lying width is
        # worse than none, it reserves the wrong box in the unfurl.
        declared = [(k, tags[k]) for k in ("og:image:width", "og:image:height")
                    if k in tags]
        if declared and img_path:
            size = image_pixel_size(img_path)
            if size is None:
                bad("og:image-unreadable",
                    "declares %s but %s is not a PNG/JPEG this checker can "
                    "measure — the numbers cannot be verified"
                    % ("/".join(k for k, _v in declared),
                       os.path.relpath(img_path, site.root)))
            else:
                for k, v in declared:
                    real = size[0] if k.endswith("width") else size[1]
                    v = v.strip()
                    if not v.isdigit():
                        bad(k, "%s=%r is not a number (real %s is %d)"
                            % (k, tags[k], k.rsplit(":", 1)[1], real))
                    elif int(v) != real:
                        bad(k, "%s=%s but %s is %dx%d — real %s is %d"
                            % (k, v, os.path.relpath(img_path, site.root),
                               size[0], size[1], k.rsplit(":", 1)[1], real))

        # (f) og:site_name is a constant on every page.
        if "og:site_name" in tags:
            got = htmlmod.unescape(tags["og:site_name"]).strip()
            if got != OG_SITE_NAME:
                bad("og:site_name-value",
                    "og:site_name %r (want %r on every page)" % (got, OG_SITE_NAME))

        # (g) og:locale follows the file's location, not the author's mood.
        if "og:locale" in tags:
            want_loc = og_locale_for(rel)
            got = tags["og:locale"].strip()
            if got != want_loc:
                bad("og:locale-value",
                    "og:locale %r (want %r — %s)"
                    % (got, want_loc,
                       "blog posts are Thai prose" if want_loc == OG_LOCALE_TH
                       else 'this is one of the lang="en" chrome pages'))
    return out


# ---------------------------------------------------------------------------
# --fix : article counters in blog/index.html, and NOTHING else
# ---------------------------------------------------------------------------
def do_fix(site, quiet=False):
    path = os.path.join(site.blog, "index.html")
    with open(path, encoding="utf-8", newline="") as fh:
        raw = fh.read()

    edits = []       # (start, end, old, new, line, label)
    unchanged = []   # (line, label, value)

    total_cards = len(RE_CARD.findall(raw))
    n_sections = len(RE_SECTION.findall(raw))

    # 1 + 2: the two .blog-hero__stat values
    for m in RE_HERO_STAT.finditer(raw):
        label = m.group(4).lower()
        if label == "articles":
            want = total_cards
        elif label == "series":
            want = n_sections
        else:
            continue
        got = int(m.group(2))
        ln = lineno(raw, m.start())
        if got == want:
            unchanged.append((ln, 'blog-hero__stat "%s"' % m.group(4), got))
        else:
            edits.append((m.start(2), m.end(2), str(got), str(want), ln,
                          'blog-hero__stat "%s"' % m.group(4)))

    # 3: every .series-count, measured against its own section
    for sm in RE_SECTION.finditer(raw):
        sid, body, base = sm.group(1), sm.group(2), sm.start(2)
        want = len(RE_CARD.findall(body))
        cm = RE_SERIES_COUNT.search(body)
        if not cm:
            continue
        got = int(cm.group(2))
        ln = lineno(raw, base + cm.start())
        if got == want:
            unchanged.append((ln, "series-count #%s" % sid, got))
        else:
            edits.append((base + cm.start(2), base + cm.end(2), str(got), str(want),
                          ln, "series-count #%s" % sid))

    if not quiet:
        print(C.bold("--fix  blog/index.html  (article counters only)"))
        print("  computed truth: %d cards, %d series-sections" % (total_cards, n_sections))
        for ln, label, val in sorted(unchanged):
            print("  %s line %-4d %-28s %s" % (C.grey("  ok"), ln, label,
                                               C.grey("%s (already correct)" % val)))
    if not edits:
        if not quiet:
            print("  " + C.green("nothing to change — all counters already correct"))
        return 0

    out = raw
    for start, end, old, new, _ln, _label in sorted(edits, key=lambda e: -e[0]):
        out = out[:start] + new + out[end:]

    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(out)

    if not quiet:
        for _s, _e, old, new, ln, label in sorted(edits, key=lambda e: e[4]):
            print("  %s line %-4d %-28s %s" % (C.yellow("edit"), ln, label,
                                               C.red("-" + old) + "  " + C.green("+" + new)))
        print("  %s %d counter%s rewritten in blog/index.html"
              % (C.green("wrote"), len(edits), "" if len(edits) == 1 else "s"))
    return len(edits)


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------
def find_root(explicit):
    if explicit:
        return os.path.abspath(os.path.expanduser(explicit))
    # walk up from cwd, then from this script's location
    for start in (os.getcwd(), os.path.dirname(os.path.abspath(__file__))):
        d = start
        while True:
            if (os.path.isfile(os.path.join(d, "index.html"))
                    and os.path.isdir(os.path.join(d, "blog"))
                    and os.path.isdir(os.path.join(d, "images"))):
                return d
            parent = os.path.dirname(d)
            if parent == d:
                break
            d = parent
    return os.getcwd()


def cid_sort_key(cid):
    """INV-2 < INV-10, and INV-04a < INV-04b < INV-04h."""
    m = re.match(r"INV-(\d+)([a-z]*)$", cid)
    return (int(m.group(1)), m.group(2)) if m else (999, cid)


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="check_site.py",
        description="Cross-file consistency linter for the anirach.com static site.")
    ap.add_argument("--root", help="repository root (default: auto-detect)")
    ap.add_argument("--check", metavar="ID", action="append",
                    help="run only this check id (repeatable), e.g. --check INV-05")
    ap.add_argument("--quiet", action="store_true",
                    help="status line per check plus the summary; no violation detail")
    ap.add_argument("--fix", action="store_true",
                    help="repair ONLY the article counters in blog/index.html")
    ap.add_argument("--list", action="store_true", help="list check ids and exit")
    ap.add_argument("--color", choices=("auto", "always", "never"), default="auto")
    args = ap.parse_args(argv)

    C.init(None if args.color == "auto" else (args.color == "always"))

    CHECKS.sort(key=lambda c: cid_sort_key(c.cid))

    if args.list:
        for c in CHECKS:
            print("%-9s %-5s %s" % (c.cid, c.severity, c.title))
        return 0

    root = find_root(args.root)
    try:
        site = Site(root)
    except SystemExit as e:
        print(str(e), file=sys.stderr)
        return 2

    if args.fix:
        do_fix(site, quiet=args.quiet)
        site = Site(root)          # reload so the report reflects the repair
        if not args.quiet:
            print()

    selected = CHECKS
    if args.check:
        want = {c.upper() for c in args.check}
        selected = [c for c in CHECKS if c.cid.upper() in want]
        missing = want - {c.cid.upper() for c in selected}
        if missing:
            print("unknown check id(s): %s" % ", ".join(sorted(missing)), file=sys.stderr)
            print("run --list to see all ids", file=sys.stderr)
            return 2

    if not args.quiet:
        print(C.bold("site-check") + "  " + root)
        print(C.grey("%d HTML files  |  %d posts  |  %d files in images/  |  %d cards in blog/index.html"
                     % (len(site.pages), len(site.posts),
                        len(site.images_on_disk), len(site.cards))))
        print()

    n_pass = n_known = n_warn = n_fail = n_info = 0
    failed_ids, warned_ids = [], []
    total_new = total_known = 0

    for c in selected:
        viols = c.fn(site) or []
        viols = [v if isinstance(v, Violation) else Violation(str(v)) for v in viols]
        base = BASELINE.get(c.cid, set())
        allowed = dict(base) if isinstance(base, dict) else {k: 1 for k in base}
        occurrences = Counter()
        for v in viols:
            occurrences[v.key] += 1
            v.known = occurrences[v.key] <= allowed.get(v.key, 0)
        new = [v for v in viols if not v.known]
        known = [v for v in viols if v.known]
        total_new += len(new)
        total_known += len(known)

        if not viols:
            status, colour, n_pass = "PASS", C.green, n_pass + 1
        elif not new:
            status, colour, n_known = "KNOWN", C.blue, n_known + 1
        elif c.severity == FAIL:
            status, colour, n_fail = "FAIL", C.red, n_fail + 1
            failed_ids.append(c.cid)
        elif c.severity == WARN:
            status, colour, n_warn = "WARN", C.yellow, n_warn + 1
            warned_ids.append(c.cid)
        else:
            status, colour, n_info = "INFO", C.grey, n_info + 1

        counts = []
        if new:
            counts.append("%d new" % len(new))
        if known:
            counts.append("%d known" % len(known))
        tail = ("  (%s)" % ", ".join(counts)) if counts else ""
        print("%s %-9s %-3d %s%s" % (colour("[%-5s]" % status), c.cid,
                                     len(viols), c.title, C.grey(tail)))

        if viols and not args.quiet:
            for v in new:
                print("        %s %s" % (C.red("✗"), v.detail))
            for v in known:
                print("        %s %s %s" % (C.grey("·"), v.detail, C.grey("[known]")))
            print()

    print()
    print(C.bold("SUMMARY"))
    print("  checks run       %3d" % len(selected))
    print("  %s  %3d" % (C.green("clean         "), n_pass))
    print("  %s  %3d   %s" % (C.blue("known baseline"), n_known,
                              C.grey("pre-existing debt; does not fail the build")))
    print("  %s  %3d" % (C.yellow("warn          "), n_warn))
    print("  %s  %3d" % (C.grey("info          "), n_info))
    print("  %s  %3d" % (C.red("FAIL          "), n_fail))
    print("  violations       %3d new, %d known" % (total_new, total_known))

    if failed_ids:
        print()
        print("  " + C.red("FAILING: " + ", ".join(failed_ids)))
        if any(i.startswith("INV-02") for i in failed_ids):
            print("  " + C.grey("hint: --fix recomputes the blog/index.html article "
                                "counters from the card count"))
    if warned_ids:
        print("  " + C.yellow("WARN:    " + ", ".join(warned_ids)))
    if not failed_ids:
        print()
        print("  " + C.green("PASS — no new FAIL-severity violations"))

    return 1 if failed_ids else 0


if __name__ == "__main__":
    sys.exit(main())
