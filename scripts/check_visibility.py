#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_visibility — search-visibility (SEO + GEO + AEO) scanner for anirach.com

The companion to check_site.py: that script polices cross-file *consistency*
(nav chains, counters, covers); this one grades how visible the site is to
search engines and AI answer engines — robots.txt AI-crawler policy, llms.txt,
JSON-LD structured data, title/description hygiene, heading hierarchy, link
health.  It IMPORTS check_site.py and reuses its Site model and helpers; it
never modifies anything.  Python 3 standard library only.

Check design is learned from claude-rank (MIT, github.com/Houseofmvps/claude-rank
— a Node CLI with 170+ SEO/GEO/AEO checks).  Each rule id below maps to one or
more of its checks, re-derived for this hand-written, zero-JavaScript, bilingual
(Thai/English) static site.  Full mapping: the 2026-09-02 planning notes.

Deliberately NOT adopted from claude-rank, and why (one line each):
  * English-NLP content heuristics (word counts, readability, passive voice,
    front-loading) — whitespace tokenization is structurally broken on Thai.
  * script/analytics checks — INV-38 forbids executable <script>; dead rules.
  * robots/sitemap/llms *generators* — they would clobber hand-maintained
    files with verified semantics; this site hand-merges instead.
  * noindex check — the one noindex is 404.html, deliberate and documented.
  * canonical/OG presence checks — check_site's INV-27 recomputes values from
    file location and real image pixels; strictly stronger.
  * hreflang rules — single-URL bilingual design has none on purpose; the
    signal is JSON-LD inLanguage ["th","en"] instead.
  * PWA manifest — adds nothing to a content site.
  * composite Rank Score as a CI gate — the score here is report-only
    (--min-score is an opt-in convention); check_site's per-violation
    empty-baseline model stays the real gate.

Scoring model (per the 2026-09-02 plan):
  * Six sections: [AI Access] [llms.txt] [Structured Data]
    [Titles & Descriptions] [Headings] [Hygiene].
  * Section score = 100 minus one deduction per UNIQUE rule id with findings
    (never per instance): CRITICAL -20, HIGH -10, MEDIUM -5, LOW -2.
    FAIL-severity checks are HIGH (R2 and M3 are CRITICAL); WARN checks are
    MEDIUM; advisories (T2) are LOW; INFO findings (M7, dirty-tree M6)
    deduct nothing.  A rule with mixed-severity findings deducts once at the
    highest class present.  Per-rule instance counts are printed so volume
    stays visible even though it does not multiply deductions.
  * Overall = round(mean of the six section scores)).
    Grade line: AI-READY >= 90 / GOOD >= 75 / NEEDS WORK < 75.

Usage
    python3 scripts/check_visibility.py                 # human report
    python3 scripts/check_visibility.py --json          # machine dump
    python3 scripts/check_visibility.py --strict        # every violation,
                                                        # exit 1 on any FAIL
    python3 scripts/check_visibility.py --min-score 90  # exit 1 below 90
    python3 scripts/check_visibility.py --strict --min-score 90   # composable

Exit status
    0  clean under the requested gates (default mode always exits 0)
    1  --strict saw a FAIL-severity finding, or overall < --min-score
    2  usage / environment error
"""

import argparse
import html as htmlmod
import json
import os
import re
import subprocess
import sys
from collections import defaultdict

# ---------------------------------------------------------------------------
# Repo root + the check_site import (reuse, never copy)
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
CHECK_SITE_DIR = os.path.join(
    REPO_ROOT, ".claude", "skills", "site-check", "scripts")

sys.path.insert(0, CHECK_SITE_DIR)
try:
    import check_site
except ImportError:
    sys.stderr.write(
        "check_visibility.py: cannot import check_site.py — expected it at\n"
        "  %s\n"
        "This scanner reuses check_site's Site model and helpers (it does not\n"
        "copy them). Restore .claude/skills/site-check/scripts/check_site.py\n"
        "or pass --root pointing at a checkout that has it.\n"
        % os.path.join(CHECK_SITE_DIR, "check_site.py"))
    sys.exit(2)

SITE_ORIGIN = check_site.SITE_ORIGIN


# ---------------------------------------------------------------------------
# Severity model
# ---------------------------------------------------------------------------
FAIL, WARN, INFO = "FAIL", "WARN", "INFO"
CRITICAL, HIGH, MEDIUM, LOW, NONE = "critical", "high", "medium", "low", "none"
DEDUCTION = {CRITICAL: 20, HIGH: 10, MEDIUM: 5, LOW: 2, NONE: 0}


class Finding(object):
    __slots__ = ("rule", "severity", "klass", "page", "detail")

    def __init__(self, rule, severity, klass, page, detail):
        self.rule = rule          # "R1", "S5", ...
        self.severity = severity  # FAIL / WARN / INFO  (strict-mode gate)
        self.klass = klass        # scoring class: critical/high/medium/low/none
        self.page = page          # repo-relative path or "" for site-level
        self.detail = detail


class Rule(object):
    __slots__ = ("rid", "title", "severity", "klass", "fn")

    def __init__(self, rid, title, severity, klass, fn):
        self.rid, self.title = rid, title
        self.severity, self.klass, self.fn = severity, klass, fn


RULES = {}


def rule(rid, title, severity, klass):
    """Register a check.  severity/klass are the rule's DEFAULT finding tags;
    a check may emit findings at other tags (T1's description duplicates are
    WARN/medium beside its FAIL/high title duplicates; M6 drops to INFO/none
    on a dirty file)."""
    def deco(fn):
        RULES[rid] = Rule(rid, title, severity, klass, fn)
        return fn
    return deco


SECTIONS = [
    ("AI Access", ["R1", "R2", "R3"]),
    ("llms.txt", ["L1", "L2"]),
    ("Structured Data", ["S1", "S2", "S3", "S4", "S5"]),
    ("Titles & Descriptions", ["T1", "T2", "T3"]),
    ("Headings", ["H1", "H2"]),
    ("Hygiene", ["M1", "M2", "M3", "M4", "M5", "M6", "M7"]),
]

# The AI crawlers robots.txt must welcome by name (R1).  Wildcard `*` does not
# count: the point is an EXPLICIT per-bot policy signal.
AI_BOTS = [
    "GPTBot", "OAI-SearchBot", "ChatGPT-User",
    "PerplexityBot", "Perplexity-User",
    "ClaudeBot", "Claude-SearchBot", "Claude-User",
    "Google-Extended", "CCBot", "Applebot-Extended",
    "Meta-ExternalAgent", "Amazonbot",
]

# Required JSON-LD fields per @type (S2).  Types not listed are validated for
# JSON well-formedness only — claude-rank's engine has no Book type at all,
# so extending validation to Book is this site's own addition.
LD_REQUIRED_FIELDS = {
    "BlogPosting": ["headline", "author", "datePublished"],
    "Article": ["headline", "author", "datePublished"],
    "NewsArticle": ["headline", "author", "datePublished"],
    "Book": ["name", "author", "inLanguage"],
    "Person": ["name"],
    "WebSite": ["name", "url"],
}

PERSON_ID = SITE_ORIGIN + "/#person"

RE_LDJSON = re.compile(
    r'<script type="application/ld\+json">(.*?)</script>', re.S)
RE_TITLE = re.compile(r"<title>(.*?)</title>", re.S)
RE_PUBTIME = re.compile(
    r'<meta\s+property="article:published_time"\s+content="([^"]*)"')
RE_TIME_DT = re.compile(r'<time\b[^>]*\bdatetime="([^"]*)"')
RE_LINK_ATTR = re.compile(r'\b(href|src|poster)\s*=\s*"([^"]*)"')
RE_SRCSET_ATTR = re.compile(r'\bsrcset\s*=\s*"([^"]*)"')
RE_IMG_TAG = re.compile(r"<img\b[^>]*>")
RE_H1_TAG = re.compile(r"<h1[\s>]")
RE_HEADING = re.compile(r"<h([234])[\s>]")
RE_TRACK_MARK = re.compile(
    r'<(?:div|details|section)\b[^>]*class="[^"]*\bl-(th|en)\b')
RE_FEED_LINK = re.compile(
    r'<link\b[^>]*rel="alternate"[^>]*type="application/rss\+xml"[^>]*>'
    r'|<link\b[^>]*type="application/rss\+xml"[^>]*rel="alternate"[^>]*>')
RE_LLMS_LINK = re.compile(r"^- \[(.+?)\]\((\S+?)\)(: .+)?$")
RE_SITEMAP_URL = re.compile(r"<url>(.*?)</url>", re.S)


# ---------------------------------------------------------------------------
# Context — the parsed site, plus visibility-specific caches
# ---------------------------------------------------------------------------
class Ctx(object):
    def __init__(self, root):
        self.root = root
        self.site = check_site.Site(root)       # 66 pages, text preloaded
        self.pages = self.site.pages
        self.posts = ["blog/" + f for f in self.site.posts]
        self._inert = {}
        self._ld = {}
        self._resolved_links = None
        self._git_dirty = None
        self._git_dates = {}

    def text(self, rel):
        return self.site.text[rel]

    def inert(self, rel):
        """Page text with HTML comments AND <style>/<script>/<pre>/<code>
        bodies blanked to same-length spaces (newlines kept, offsets stable),
        so neither a code sample nor a comment that merely *mentions* markup
        can look like markup.  Comments are blanked FIRST — index.html has a
        comment that says "<h1>" in prose, and a comment could equally open a
        phantom <pre> span (check_site's trap #4, generalised)."""
        if rel not in self._inert:
            no_comments = check_site.RE_HTML_COMMENT.sub(
                lambda m: re.sub(r"[^\n]", " ", m.group(0)),
                self.site.text[rel])
            self._inert[rel] = check_site.blank_inert(no_comments)
        return self._inert[rel]

    def ld_blocks(self, rel):
        """[(raw, parsed_or_None), ...] for every ld+json block on the page.
        Extracted from RAW text (blank_inert would blank them)."""
        if rel not in self._ld:
            out = []
            for m in RE_LDJSON.finditer(self.site.text[rel]):
                raw = m.group(1)
                try:
                    out.append((raw, json.loads(raw)))
                except ValueError:
                    out.append((raw, None))
            self._ld[rel] = out
        return self._ld[rel]

    def is_bilingual(self, rel):
        return 'class="l-en"' in self.site.text[rel]

    # -- git (M6) ---------------------------------------------------------
    def git_dirty_files(self):
        if self._git_dirty is None:
            self._git_dirty = set()
            try:
                out = subprocess.run(
                    ["git", "-C", self.root, "status", "--porcelain"],
                    capture_output=True, text=True, timeout=30)
                for line in out.stdout.splitlines():
                    if len(line) > 3:
                        self._git_dirty.add(line[3:].strip().strip('"'))
            except (OSError, subprocess.SubprocessError):
                pass  # no git -> M6 silently degrades to lastmod-format only
        return self._git_dirty

    def git_last_date(self, rel):
        if rel not in self._git_dates:
            date = None
            try:
                out = subprocess.run(
                    ["git", "-C", self.root, "log", "-1", "--format=%ad",
                     "--date=short", "--", rel],
                    capture_output=True, text=True, timeout=30)
                date = out.stdout.strip() or None
            except (OSError, subprocess.SubprocessError):
                pass
            self._git_dates[rel] = date
        return self._git_dates[rel]

    # -- internal-link resolution (M1/M2) ---------------------------------
    def resolved_links(self):
        """{source_rel: (broken, internal_targets)} where broken is
        [(raw_href, tried_path)] and internal_targets is a set of site-page
        rel paths the source links to (post-resolution, extensionless and
        directory forms included)."""
        if self._resolved_links is not None:
            return self._resolved_links
        page_set = set(self.pages)
        result = {}
        for rel in self.pages:
            text = self.inert(rel)
            base = os.path.dirname(rel)
            broken, targets = [], set()
            raws = [v for _a, v in RE_LINK_ATTR.findall(text)]
            for ss in RE_SRCSET_ATTR.findall(text):
                raws.extend(p.strip().split()[0]
                            for p in ss.split(",") if p.strip())
            for raw in raws:
                t = raw.strip()
                if (not t or t.startswith("#") or "://" in t
                        or t.startswith(("mailto:", "tel:", "data:",
                                         "javascript:", "//"))):
                    continue
                t = t.split("#", 1)[0].split("?", 1)[0]
                if not t:
                    continue
                if t.startswith("/"):
                    cand = os.path.normpath(t.lstrip("/")) or "."
                else:
                    cand = os.path.normpath(os.path.join(base, t))
                hit = None
                if cand != "." and os.path.isfile(os.path.join(self.root, cand)):
                    hit = cand
                elif os.path.isfile(os.path.join(self.root, cand + ".html")):
                    hit = cand + ".html"          # extensionless chip fallback
                elif os.path.isfile(os.path.join(
                        self.root, cand, "index.html")):
                    hit = os.path.join(cand, "index.html")
                if hit is None:
                    broken.append((raw, cand))
                else:
                    hit = hit.replace(os.sep, "/")
                    if hit in page_set and hit != rel:
                        targets.add(hit)
            result[rel] = (broken, targets)
        self._resolved_links = result
        return result


def clean_text(s):
    return htmlmod.unescape(re.sub(r"\s+", " ", s)).strip()


# ---------------------------------------------------------------------------
# [AI Access] R1-R3 — robots.txt
# ---------------------------------------------------------------------------
def parse_robots(text):
    """Records of (agents, directives) with comments stripped.  A record is
    one or more consecutive User-agent lines plus the directives that follow,
    per the robots.txt grouping rules."""
    records, agents, directives, collecting = [], [], [], True
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        if ":" not in line:
            continue
        field, _sep, value = line.partition(":")
        field, value = field.strip().lower(), value.strip()
        if field == "user-agent":
            if not collecting and agents:
                records.append((agents, directives))
                agents, directives = [], []
            agents.append(value)
            collecting = True
        elif field == "sitemap":
            records.append((["__sitemap__"], [(field, value)]))
        else:
            if agents:
                directives.append((field, value))
                collecting = False
    if agents:
        records.append((agents, directives))
    return records


def robots_records(ctx):
    path = os.path.join(ctx.root, "robots.txt")
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8") as fh:
        return parse_robots(fh.read())


@rule("R1", "robots.txt welcomes each AI crawler by name (User-agent + Allow)",
      FAIL, HIGH)
def _(ctx):
    recs = robots_records(ctx)
    if recs is None:
        return [Finding("R1", FAIL, HIGH, "robots.txt",
                        "robots.txt does not exist — no crawler policy at all")]
    covered = {}
    for agents, directives in recs:
        for a in agents:
            covered[a.lower()] = directives
    out = []
    for bot in AI_BOTS:
        d = covered.get(bot.lower())
        if d is None:
            out.append(Finding("R1", FAIL, HIGH, "robots.txt",
                               "no explicit User-agent stanza for %s "
                               "(wildcard * does not count as a policy signal)"
                               % bot))
        elif not any(f == "allow" for f, _v in d):
            out.append(Finding("R1", FAIL, HIGH, "robots.txt",
                               "stanza for %s has no Allow directive" % bot))
    return out


@rule("R2", "no robots.txt stanza blocks by accident (Disallow without Allow)",
      FAIL, CRITICAL)
def _(ctx):
    recs = robots_records(ctx)
    if recs is None:
        return []          # R1 already reported the missing file
    out = []
    for agents, directives in recs:
        if agents == ["__sitemap__"]:
            continue
        disallows = [v for f, v in directives if f == "disallow" and v]
        has_allow = any(f == "allow" for f, _v in directives)
        if disallows and not has_allow:
            out.append(Finding(
                "R2", FAIL, CRITICAL, "robots.txt",
                "User-agent %s has Disallow (%s) with no Allow — if this is "
                "deliberate, add an explicit Allow for what remains open"
                % (", ".join(agents), ", ".join(disallows))))
    return out


@rule("R3", "robots.txt Sitemap: line points at the real sitemap URL",
      FAIL, HIGH)
def _(ctx):
    recs = robots_records(ctx)
    if recs is None:
        return []          # R1 already reported the missing file
    want = SITE_ORIGIN + "/sitemap.xml"
    maps = [v for agents, ds in recs if agents == ["__sitemap__"]
            for _f, v in ds]
    if not maps:
        return [Finding("R3", FAIL, HIGH, "robots.txt",
                        "no Sitemap: line (want %s)" % want)]
    return [Finding("R3", FAIL, HIGH, "robots.txt",
                    "Sitemap: %s (want %s)" % (m, want))
            for m in maps if m != want]


# ---------------------------------------------------------------------------
# [llms.txt] L1-L2
# ---------------------------------------------------------------------------
def llms_path(ctx):
    return os.path.join(ctx.root, "llms.txt")


@rule("L1", "llms.txt exists in the expected format (# title, > blurb, "
            "## sections, - [title](abs url): desc)", FAIL, HIGH)
def _(ctx):
    p = llms_path(ctx)
    if not os.path.isfile(p):
        return [Finding("L1", FAIL, HIGH, "llms.txt",
                        "llms.txt does not exist at the repo root — AI "
                        "answer engines have no site inventory to read")]
    with open(p, encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    out = []
    nonblank = [(i + 1, l) for i, l in enumerate(lines) if l.strip()]
    if not nonblank or not nonblank[0][1].startswith("# "):
        out.append(Finding("L1", FAIL, HIGH, "llms.txt",
                           "first non-blank line must be an H1 title "
                           "('# ...')"))
    first_h2 = next((n for n, l in nonblank if l.startswith("## ")),
                    len(lines) + 1)
    if not any(l.startswith("> ") for n, l in nonblank if n < first_h2):
        out.append(Finding("L1", FAIL, HIGH, "llms.txt",
                           "no '> ' blockquote blurb before the first "
                           "'## ' section"))
    if not any(l.startswith("## ") for _n, l in nonblank):
        out.append(Finding("L1", FAIL, HIGH, "llms.txt",
                           "no '## Section' headings at all"))
    for n, l in nonblank:
        if l.startswith("- "):
            m = RE_LLMS_LINK.match(l)
            if not m:
                out.append(Finding(
                    "L1", FAIL, HIGH, "llms.txt",
                    "line %d: link line does not match "
                    "'- [Title](url): description' — %r" % (n, l[:80])))
            elif not m.group(2).startswith(("http://", "https://")):
                out.append(Finding(
                    "L1", FAIL, HIGH, "llms.txt",
                    "line %d: link URL %r is not absolute" % (n, m.group(2))))
            elif not m.group(3):
                out.append(Finding(
                    "L1", FAIL, HIGH, "llms.txt",
                    "line %d: link line has no ': description' suffix"
                    % n))
    return out


@rule("L2", "llms.txt drift: every link resolves on disk and every blog "
            "series is represented", FAIL, HIGH)
def _(ctx):
    p = llms_path(ctx)
    if not os.path.isfile(p):
        # The file's absence is L1's finding; L2 adds the drift consequence
        # once (not per series) so the section reflects both gaps.
        return [Finding("L2", FAIL, HIGH, "llms.txt",
                        "no llms.txt to cross-check — series coverage and "
                        "link resolution unverifiable until L1's fix lands")]
    with open(p, encoding="utf-8") as fh:
        content = fh.read()
    out = []
    for i, line in enumerate(content.splitlines(), 1):
        m = RE_LLMS_LINK.match(line.strip())
        if not m:
            continue
        url = m.group(2)
        if not url.startswith(SITE_ORIGIN):
            continue          # off-origin links are not on-disk resolvable
        path = url[len(SITE_ORIGIN):].split("#")[0].split("?")[0]
        rel = path.lstrip("/")
        if path.endswith("/") or rel == "":
            rel = rel + "index.html"
        full = os.path.join(ctx.root, rel)
        if not (os.path.isfile(full)
                or os.path.isfile(full + ".html")
                or os.path.isfile(os.path.join(full, "index.html"))):
            out.append(Finding("L2", FAIL, HIGH, "llms.txt",
                               "line %d: %s resolves to no file on disk (%s)"
                               % (i, url, rel)))
    # Series representation: the four series-title h2s on blog/index.html.
    text = htmlmod.unescape(content)
    for m in re.finditer(r'<h2 class="series-title">(.*?)</h2>',
                         ctx.text("blog/index.html")):
        series = clean_text(m.group(1))
        if series.lower() not in text.lower():
            out.append(Finding("L2", FAIL, HIGH, "llms.txt",
                               "series %r (blog/index.html) appears nowhere "
                               "in llms.txt" % series))
    return out


# ---------------------------------------------------------------------------
# [Structured Data] S1-S5
# ---------------------------------------------------------------------------
def typed_nodes(node):
    """Every dict in a parsed JSON-LD tree that carries an @type."""
    if isinstance(node, dict):
        if "@type" in node:
            yield node
        for v in node.values():
            for n in typed_nodes(v):
                yield n
    elif isinstance(node, list):
        for v in node:
            for n in typed_nodes(v):
                yield n


def node_types(node):
    t = node.get("@type")
    return t if isinstance(t, list) else [t]


@rule("S1", "every post carries one BlogPosting JSON-LD block with the "
            "required fields", FAIL, HIGH)
def _(ctx):
    out = []
    for rel in ctx.posts:
        blocks = [(raw, d) for raw, d in ctx.ld_blocks(rel) if d is not None]
        bps = [d for _raw, d in blocks
               if any("BlogPosting" in node_types(n) for n in typed_nodes(d))]
        if len(bps) != 1:
            out.append(Finding(
                "S1", FAIL, HIGH, rel,
                "has %d BlogPosting ld+json blocks (want exactly 1)"
                % len(bps)))
            continue
        bp = next(n for n in typed_nodes(bps[0])
                  if "BlogPosting" in node_types(n))
        problems = []
        for f in ("headline", "datePublished", "dateModified", "image",
                  "inLanguage"):
            if not bp.get(f):
                problems.append("missing %s" % f)
        author = bp.get("author")
        if not isinstance(author, dict):
            problems.append("author is not an inline Person object")
        else:
            if "Person" not in node_types(author):
                problems.append("author @type is not Person")
            if not author.get("name"):
                problems.append("author has no name")
            if author.get("@id") != PERSON_ID:
                problems.append("author @id %r (want %r so each page parses "
                                "standalone)" % (author.get("@id"), PERSON_ID))
        want_canonical = check_site.canonical_url_for(rel)
        meop = bp.get("mainEntityOfPage")
        if isinstance(meop, dict):
            meop = meop.get("@id")
        if meop != want_canonical:
            problems.append("mainEntityOfPage %r != canonical %r"
                            % (meop, want_canonical))
        if ctx.is_bilingual(rel):
            lang = bp.get("inLanguage")
            if lang and sorted(lang if isinstance(lang, list) else [lang]) \
                    != ["en", "th"]:
                problems.append('bilingual post: inLanguage %r (want '
                                '["th","en"])' % (lang,))
        if problems:
            out.append(Finding("S1", FAIL, HIGH, rel,
                               "BlogPosting: " + "; ".join(problems)))
    return out


@rule("S2", "every ld+json block sitewide parses and carries the required "
            "fields for its @type", FAIL, HIGH)
def _(ctx):
    out = []
    for rel in ctx.pages:
        for i, (raw, parsed) in enumerate(ctx.ld_blocks(rel), 1):
            if parsed is None:
                out.append(Finding("S2", FAIL, HIGH, rel,
                                   "ld+json block %d does not parse as JSON"
                                   % i))
                continue
            for node in typed_nodes(parsed):
                for t in node_types(node):
                    for f in LD_REQUIRED_FIELDS.get(t, ()):
                        if not node.get(f):
                            out.append(Finding(
                                "S2", FAIL, HIGH, rel,
                                "block %d: %s is missing required field %s"
                                % (i, t, f)))
    return out


@rule("S3", "post dates agree: JSON-LD datePublished == "
            "article:published_time == <time datetime>", FAIL, HIGH)
def _(ctx):
    out = []
    for rel in ctx.posts:
        vals = {}
        for _raw, d in ctx.ld_blocks(rel):
            if d is None:
                continue
            for node in typed_nodes(d):
                if "BlogPosting" in node_types(node) \
                        and node.get("datePublished"):
                    vals["JSON-LD datePublished"] = \
                        str(node["datePublished"])[:10]
        inert = ctx.inert(rel)
        m = RE_PUBTIME.search(inert)
        if m:
            vals["article:published_time"] = m.group(1)[:10]
        m = RE_TIME_DT.search(inert)
        if m:
            vals["<time datetime>"] = m.group(1)[:10]
        if len(set(vals.values())) > 1:
            out.append(Finding(
                "S3", FAIL, HIGH, rel,
                "dates disagree: " + ", ".join(
                    "%s=%s" % (k, v) for k, v in sorted(vals.items()))))
    return out


@rule("S4", "root page carries the WebSite + Person entity graph "
            "(and no SearchAction)", WARN, MEDIUM)
def _(ctx):
    types = set()
    for _raw, d in ctx.ld_blocks("index.html"):
        if d is None:
            continue
        for node in typed_nodes(d):
            types.update(t for t in node_types(node) if t)
    out = []
    for want in ("WebSite", "Person"):
        if want not in types:
            out.append(Finding("S4", WARN, MEDIUM, "index.html",
                               "no %s node in the root ld+json graph" % want))
    if any("SearchAction" in t for t in types):
        out.append(Finding("S4", WARN, MEDIUM, "index.html",
                           "root graph declares a SearchAction but the site "
                           "has no search"))
    return out


@rule("S5", "no orphan itemprop outside an itemscope", FAIL, HIGH)
def _(ctx):
    """APPROXIMATION, kept simple and honest: microdata scoping is a tree
    property, but this scanner (stdlib, no DOM) flags a page when its FIRST
    itemprop-carrying tag appears BEFORE its first itemscope tag — exactly
    the found bug shape (head/hero itemprops emitted above the article's
    itemscope, which parses to a BlogPosting item holding only an author).
    An orphan itemprop *after* a closed itemscope would not be caught; none
    exists in this corpus and INV-38 keeps the markup hand-auditable."""
    out = []
    for rel in ctx.pages:
        text = ctx.inert(rel)
        prop = text.find("itemprop=")
        if prop == -1:
            continue
        scope = text.find("itemscope")
        if scope == -1:
            out.append(Finding("S5", FAIL, HIGH, rel,
                               "carries itemprop= but no itemscope at all"))
        elif prop < scope:
            out.append(Finding(
                "S5", FAIL, HIGH, rel,
                "first itemprop (offset %d) precedes the first itemscope "
                "(offset %d) — those itemprops bind to no item" % (prop, scope)))
    return out


# ---------------------------------------------------------------------------
# [Titles & Descriptions] T1-T3
# ---------------------------------------------------------------------------
def page_title(ctx, rel):
    m = RE_TITLE.search(ctx.text(rel))
    return clean_text(m.group(1)) if m else None


@rule("T1", "titles unique sitewide (FAIL); descriptions unique (WARN)",
      FAIL, HIGH)
def _(ctx):
    titles, descs = defaultdict(list), defaultdict(list)
    for rel in ctx.pages:
        t = page_title(ctx, rel)
        if t:
            titles[t.lower()].append(rel)
        _canon, tags = check_site.social_head(ctx.text(rel))
        d = clean_text(tags.get("description", ""))
        if d:
            descs[d.lower()].append(rel)
    out = []
    for t, pages in sorted(titles.items()):
        if len(pages) > 1:
            out.append(Finding("T1", FAIL, HIGH, pages[0],
                               "duplicate <title> on %s: %r"
                               % (", ".join(pages), t[:60])))
    for d, pages in sorted(descs.items()):
        if len(pages) > 1:
            out.append(Finding("T1", WARN, MEDIUM, pages[0],
                               "duplicate meta description on %s: %r"
                               % (", ".join(pages), d[:60])))
    return out


@rule("T2", "length bands (advisory, char-based/Thai-safe): title 20-60, "
            "description 70-160", WARN, LOW)
def _(ctx):
    out = []
    for rel in ctx.pages:
        t = page_title(ctx, rel)
        if t is not None and not (20 <= len(t) <= 60):
            out.append(Finding("T2", WARN, LOW, rel,
                               "title is %d chars (band 20-60): %r"
                               % (len(t), t[:70])))
        _canon, tags = check_site.social_head(ctx.text(rel))
        d = clean_text(tags.get("description", ""))
        if d and not (70 <= len(d) <= 160):
            out.append(Finding("T2", WARN, LOW, rel,
                               "description is %d chars (band 70-160)"
                               % len(d)))
    return out


@rule("T3", "post image alts mirror og:title (og:image:alt and "
            "twitter:image:alt)", WARN, MEDIUM)
def _(ctx):
    out = []
    for rel in ctx.posts:
        _canon, tags = check_site.social_head(ctx.text(rel))
        ogt = clean_text(tags.get("og:title", ""))
        if not ogt:
            continue          # INV-27's domain
        for key in ("og:image:alt", "twitter:image:alt"):
            if key in tags and clean_text(tags[key]) != ogt:
                out.append(Finding("T3", WARN, MEDIUM, rel,
                                   "%s %r != og:title %r"
                                   % (key, clean_text(tags[key])[:40],
                                      ogt[:40])))
    return out


# ---------------------------------------------------------------------------
# [Headings] H1-H2
# ---------------------------------------------------------------------------
@rule("H1", "exactly one <h1> per page", FAIL, HIGH)
def _(ctx):
    out = []
    for rel in ctx.pages:
        n = len(RE_H1_TAG.findall(ctx.inert(rel)))
        if n != 1:
            out.append(Finding("H1", FAIL, HIGH, rel,
                               "has %d <h1> (want exactly 1)" % n))
    return out


@rule("H2", "no skipped heading level (h2 -> h4) within a post, "
            "per language track", WARN, MEDIUM)
def _(ctx):
    """Language tracks: a bilingual post interleaves .l-th and .l-en blocks,
    so the raw document order legitimately reads h2(th) h2(en) h3(th) h3(en).
    Headings are assigned to the track opened by the nearest preceding
    l-th/l-en block marker (headings before any marker are shared by both
    tracks); each track's h2/h3/h4 sequence is then checked independently.
    This is a linear approximation of block nesting — good enough because
    the corpus alternates sibling track blocks rather than nesting them.
    A page flags at most once."""
    out = []
    for rel in ctx.posts:
        text = ctx.inert(rel)
        events = [(m.start(), "track", m.group(1))
                  for m in RE_TRACK_MARK.finditer(text)]
        events += [(m.start(), "h", int(m.group(1)))
                   for m in RE_HEADING.finditer(text)]
        events.sort()
        has_tracks = any(kind == "track" for _p, kind, _v in events)
        seqs = {"th": [], "en": []} if has_tracks else {"whole body": []}
        current = None
        for _pos, kind, val in events:
            if kind == "track":
                current = val
            elif current is None:
                for seq in seqs.values():
                    seq.append(val)
            else:
                seqs[current].append(val)
        for track, seq in sorted(seqs.items()):
            for a, b in zip(seq, seq[1:]):
                if b > a + 1:
                    out.append(Finding(
                        "H2", WARN, MEDIUM, rel,
                        "heading level skip h%d -> h%d (%s)"
                        % (a, b, track if track == "whole body"
                           else "track " + track)))
                    break
            else:
                continue
            break              # flag once per page
    return out


# ---------------------------------------------------------------------------
# [Hygiene] M1-M7
# ---------------------------------------------------------------------------
@rule("M1", "every internal href/src resolves on disk (extensionless and "
            "directory fallbacks included)", FAIL, HIGH)
def _(ctx):
    out = []
    for rel in ctx.pages:
        broken, _targets = ctx.resolved_links()[rel]
        for raw, tried in broken:
            out.append(Finding("M1", FAIL, HIGH, rel,
                               "link %r resolves to nothing (tried %s, "
                               "%s.html, %s/index.html)"
                               % (raw, tried, tried, tried)))
    return out


@rule("M2", "no orphan pages (zero incoming internal links)", WARN, MEDIUM)
def _(ctx):
    incoming = defaultdict(set)
    for src in ctx.pages:
        _broken, targets = ctx.resolved_links()[src]
        for t in targets:
            incoming[t].add(src)
    out = []
    for rel in ctx.pages:
        if rel == "index.html":
            continue          # the root is the entry point, not a link target
                              # requirement — though in practice every nav
                              # links it anyway
        if not incoming[rel]:
            out.append(Finding("M2", WARN, MEDIUM, rel,
                               "no other page links this one (feed/sitemap "
                               "reachability does not count)"))
    return out


@rule("M3", "no http:// resource or internal link (mixed content / "
            "insecure origin)", FAIL, CRITICAL)
def _(ctx):
    out = []
    for rel in ctx.pages:
        text = ctx.inert(rel)
        for attr, val in RE_LINK_ATTR.findall(text):
            if val.startswith("http://"):
                out.append(Finding("M3", FAIL, CRITICAL, rel,
                                   '%s="%s" is plain http' % (attr, val[:80])))
        for ss in RE_SRCSET_ATTR.findall(text):
            if "http://" in ss:
                out.append(Finding("M3", FAIL, CRITICAL, rel,
                                   "srcset carries a plain-http URL"))
    return out


@rule("M4", "every <img> declares width and height (CLS)", WARN, MEDIUM)
def _(ctx):
    out = []
    for rel in ctx.pages:
        missing, first = 0, None
        for m in RE_IMG_TAG.finditer(ctx.inert(rel)):
            attrs = {k.lower() for k, _v
                     in check_site.RE_ATTR_ANY.findall(m.group(0))}
            if "width" not in attrs or "height" not in attrs:
                missing += 1
                if first is None:
                    src = dict(check_site.RE_ATTR_ANY.findall(m.group(0))
                               ).get("src", "?")
                    first = src
        if missing:
            out.append(Finding("M4", WARN, MEDIUM, rel,
                               "%d <img> without width/height (first: %s)"
                               % (missing, first)))
    return out


@rule("M5", "feed rel=alternate link on the home page and every section "
            "index", FAIL, HIGH)
def _(ctx):
    out = []
    for rel in ctx.site.nav_pages:
        if not RE_FEED_LINK.search(ctx.inert(rel)):
            out.append(Finding(
                "M5", FAIL, HIGH, rel,
                'no <link rel="alternate" type="application/rss+xml"> — '
                "feed.xml is undiscoverable from here"))
    return out


@rule("M6", "sitemap lastmod is not older than the file's last git commit "
            "(INFO, not WARN, for dirty files)", WARN, MEDIUM)
def _(ctx):
    path = os.path.join(ctx.root, "sitemap.xml")
    if not os.path.isfile(path):
        return [Finding("M6", WARN, MEDIUM, "sitemap.xml",
                        "sitemap.xml does not exist")]
    with open(path, encoding="utf-8") as fh:
        sm = fh.read()
    dirty = ctx.git_dirty_files()
    out = []
    for m in RE_SITEMAP_URL.finditer(sm):
        entry = m.group(1)
        loc = re.search(r"<loc>(.*?)</loc>", entry)
        lastmod = re.search(r"<lastmod>(.*?)</lastmod>", entry)
        if not loc or not loc.group(1).startswith(SITE_ORIGIN):
            continue
        p = loc.group(1)[len(SITE_ORIGIN):]
        rel = p.lstrip("/")
        if p.endswith("/") or rel == "":
            rel += "index.html"
        if not os.path.isfile(os.path.join(ctx.root, rel)):
            continue          # sitemap<->disk drift is INV-32's domain
        if not lastmod:
            out.append(Finding("M6", WARN, MEDIUM, "sitemap.xml",
                               "%s has no <lastmod>" % loc.group(1)))
            continue
        git_date = ctx.git_last_date(rel)
        if git_date and lastmod.group(1)[:10] < git_date:
            if rel in dirty:
                out.append(Finding(
                    "M6", INFO, NONE, "sitemap.xml",
                    "%s lastmod %s < last commit %s (file is dirty in the "
                    "working tree — regenerate after committing)"
                    % (rel, lastmod.group(1)[:10], git_date)))
            else:
                out.append(Finding(
                    "M6", WARN, MEDIUM, "sitemap.xml",
                    "%s lastmod %s < last commit %s"
                    % (rel, lastmod.group(1)[:10], git_date)))
    return out


@rule("M7", "standing report-only items (no deduction)", INFO, NONE)
def _(ctx):
    return [
        Finding("M7", INFO, NONE, "",
                "Search Console property for anirach.com is still unverified "
                "— owner action outside the repo (CLAUDE.md)"),
        Finding("M7", INFO, NONE, "robots.txt",
                "this repo file REPLACES Cloudflare's Content Signals block "
                "outright (verified 2026-08-26) — it is the site's only "
                "AI-access policy surface; re-verify with "
                "curl https://anirach.com/robots.txt after edge changes"),
    ]


# ---------------------------------------------------------------------------
# Runner + scoring
# ---------------------------------------------------------------------------
GRADE_LINE = "AI-READY >= 90 / GOOD >= 75 / NEEDS WORK < 75"


def grade_for(score):
    if score >= 90:
        return "AI-READY"
    if score >= 75:
        return "GOOD"
    return "NEEDS WORK"


def run_all(ctx):
    """-> (findings_by_rule, section_results, overall)
    section_results: [(name, score, [(rule, findings, deduction)])]"""
    by_rule = {}
    for rid in RULES:
        by_rule[rid] = RULES[rid].fn(ctx) or []
    sections = []
    for name, rids in SECTIONS:
        score, rows = 100, []
        for rid in rids:
            fs = by_rule[rid]
            deductible = [f for f in fs if f.klass != NONE]
            ded = max((DEDUCTION[f.klass] for f in deductible), default=0)
            score -= ded
            rows.append((RULES[rid], fs, ded))
        sections.append((name, max(score, 0), rows))
    overall = int(round(sum(s for _n, s, _r in sections) / len(sections)))
    return by_rule, sections, overall


def print_report(ctx, sections, overall, strict, max_details):
    C = check_site.C
    n_pages = len(ctx.pages)
    print(C.bold("check_visibility") + "  " + ctx.root)
    print(C.grey("%d HTML pages  |  %d posts  |  search & AI-answer-engine "
                 "visibility scan (learned from claude-rank)"
                 % (n_pages, len(ctx.posts))))
    print()

    counts = {FAIL: 0, WARN: 0, INFO: 0}
    for name, score, rows in sections:
        colour = C.green if score >= 90 else (
            C.yellow if score >= 75 else C.red)
        print("%s  %s" % (C.bold("[%s]" % name),
                          colour("score %d/100" % score)))
        for r, fs, ded in rows:
            for f in fs:
                counts[f.severity] += 1
            if not fs:
                status, col = "PASS", C.green
            elif all(f.severity == INFO for f in fs):
                status, col = "INFO", C.grey
            elif any(f.severity == FAIL for f in fs):
                status, col = "FAIL", C.red
            else:
                status, col = "WARN", C.yellow
            tail = ("  (-%d)" % ded) if ded else ""
            print("  %s %-4s %-3d %s%s"
                  % (col("[%-5s]" % status), r.rid, len(fs), r.title,
                     C.grey(tail)))
            shown = fs if strict else fs[:max_details]
            for f in shown:
                mark = C.red("✗") if f.severity == FAIL else (
                    C.yellow("!") if f.severity == WARN else C.grey("·"))
                where = (f.page + ": ") if f.page else ""
                print("          %s %s%s" % (mark, where, f.detail))
            if len(fs) > len(shown):
                print("          %s" % C.grey(
                    "... and %d more (run with --strict to list every one)"
                    % (len(fs) - len(shown))))
        print()

    print(C.bold("SUMMARY"))
    for name, score, _rows in sections:
        colour = C.green if score >= 90 else (
            C.yellow if score >= 75 else C.red)
        print("  %-24s %s" % (name, colour("%3d" % score)))
    g = grade_for(overall)
    gcol = C.green if g == "AI-READY" else (
        C.yellow if g == "GOOD" else C.red)
    print("  %-24s %s   %s" % (C.bold("OVERALL"),
                               gcol("%3d" % overall), gcol(g)))
    print("  " + check_site.C.grey(GRADE_LINE))
    print("  findings: %d fail, %d warn, %d info"
          % (counts[FAIL], counts[WARN], counts[INFO]))
    return counts


def json_dump(ctx, by_rule, sections, overall):
    doc = {
        "root": ctx.root,
        "overall": overall,
        "grade": grade_for(overall),
        "sections": [
            {
                "name": name,
                "score": score,
                "rules": [
                    {
                        "id": r.rid,
                        "title": r.title,
                        "severity": r.severity,
                        "class": r.klass,
                        "findings": len(fs),
                        "deduction": ded,
                    }
                    for r, fs, ded in rows
                ],
            }
            for name, score, rows in sections
        ],
        "findings": [
            {
                "rule": f.rule,
                "severity": f.severity,
                "class": f.klass,
                "page": f.page,
                "detail": f.detail,
            }
            for rid in sorted(by_rule)
            for f in by_rule[rid]
        ],
    }
    print(json.dumps(doc, ensure_ascii=False, indent=2))


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="check_visibility.py",
        description="Search-visibility (SEO/GEO/AEO) scanner for the "
                    "anirach.com static site. Companion to check_site.py.")
    ap.add_argument("--root", help="repository root (default: the parent of "
                                   "this script's directory)")
    ap.add_argument("--json", action="store_true",
                    help="machine-readable dump: {sections, findings, overall}")
    ap.add_argument("--strict", action="store_true",
                    help="list every violation; exit 1 if any FAIL-severity "
                         "finding exists")
    ap.add_argument("--min-score", type=int, metavar="N",
                    help="exit 1 if the overall score is below N")
    ap.add_argument("--max-details", type=int, default=8, metavar="N",
                    help="detail lines shown per rule in the default report "
                         "(default 8; --strict always shows all)")
    ap.add_argument("--color", choices=("auto", "always", "never"),
                    default="auto")
    args = ap.parse_args(argv)

    check_site.C.init(None if args.color == "auto"
                      else (args.color == "always"))

    root = os.path.abspath(os.path.expanduser(args.root)) if args.root \
        else REPO_ROOT
    try:
        ctx = Ctx(root)
    except SystemExit as e:
        print(str(e), file=sys.stderr)
        return 2

    by_rule, sections, overall = run_all(ctx)

    if args.json:
        json_dump(ctx, by_rule, sections, overall)
        n_fail = sum(1 for fs in by_rule.values()
                     for f in fs if f.severity == FAIL)
    else:
        counts = print_report(ctx, sections, overall,
                              strict=args.strict,
                              max_details=max(args.max_details, 0))
        n_fail = counts[FAIL]

    rc = 0
    if args.strict and n_fail:
        rc = 1
    if args.min_score is not None and overall < args.min_score:
        rc = 1
    return rc


if __name__ == "__main__":
    sys.exit(main())
