#!/usr/bin/env python3
"""Give a monolingual Thai post the house TH/EN language switch.

The switch itself is pure CSS (INV-38): one visually hidden checkbox before
<main>, two content tracks .l-th / .l-en, a pill label in the hero.  Shipped
first on the Life series, copied unchanged by Hermes; this script is the
third copy, so it reads its CSS from a live post rather than a literal here.

Two phases, because only one of them needs a human (or a model):

  scaffold  every mechanical edit — head tags, CSS, checkbox, label, hero
            spans, the th-/en- id split, both TOCs, and an .l-en track whose
            sections are %%EN-SECTION:id%% placeholders.  The Thai source of
            every placeholder is dumped to a work file.
  fill      splice translations back in from that work file's answer sheet,
            forcing en- ids and #en- anchors so a translator never has to
            think about them.

Scaffolding is idempotent: a post that already has class="l-en" is skipped.

  python3 scripts/bilingualize.py --all
  python3 scripts/bilingualize.py --post docker-vs-vms
  python3 scripts/bilingualize.py --fill docker-vs-vms
  python3 scripts/bilingualize.py --status
"""

import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG = os.path.join(ROOT, "blog")

# The two reference posts. Every literal this script inserts is read out of
# one of them at run time, so a future edit to the pattern lands here for free.
REF_DEEPBLUE = "hermes-101.html"      # dark hero — the OpenClaw family
REF_SUNRISE = "morning-waking.html"   # light hero — the DevOps family

HERO_DEEPBLUE = "linear-gradient(135deg, #11304b 0%, #1a4d7a 45%, #226299 100%)"
HERO_SUNRISE = "linear-gradient(135deg, #eef3f3 0%, #dee7e6 50%, #e9e1c4 100%)"

CHECKBOX = ('<input type="checkbox" id="langSwitch" class="lang-switch-box" '
            'aria-label="Switch language: Thai / English">')
LABEL = ('<label for="langSwitch" class="lang-switch" title="สลับภาษา · Switch language">'
         '<span class="lang-th">ไทย</span><span class="lang-sep">·</span>'
         '<span class="lang-en" lang="en">English</span></label>')
ALTERNATE = '<meta property="og:locale:alternate" content="en_US">'

TH_SUMMARY = "ในบทความนี้"
EN_SUMMARY = "In this post"

# Thai letters, marks and digits — but NOT ฿ (U+0E3F), which is a currency sign
# and stays in English prose the same way £ or ¥ would.
THAI = re.compile(r"[ก-฾เ-๛]")

WORKDIR = os.path.join(ROOT, ".bilingual")   # dot-dir: unpublished, INV-06a-safe


class Bail(Exception):
    pass


# ── reading the reference implementation ────────────────────────────────────

def ref_css(variant):
    """The LANGUAGE SWITCH block, lifted from whichever reference post shares
    this post's hero family. The two variants differ only in the pill's
    background/border and its hover — the mechanism is identical."""
    ref = REF_DEEPBLUE if variant == "deepblue" else REF_SUNRISE
    s = read(os.path.join(BLOG, ref))
    start = s.index("    /* ── LANGUAGE SWITCH")
    end = s.index("#langSwitch:focus-visible ~ main .lang-switch {", start)
    end = s.index("}", s.index("outline-offset", end)) + 1
    return s[start:end]


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def write(path, text):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def indent_of(line):
    return line[: len(line) - len(line.lstrip())]


# ── scaffold ────────────────────────────────────────────────────────────────

def hero_variant(s):
    m = re.search(r"\.post-hero\s*\{[^}]*?background:\s*([^;]+);", s, re.S)
    if not m:
        raise Bail("no .post-hero background rule")
    bg = " ".join(m.group(1).split())
    if bg == HERO_DEEPBLUE:
        return "deepblue"
    if bg == HERO_SUNRISE:
        return "sunrise"
    raise Bail("hero gradient is neither approved family: %r" % bg)


def split_sections(body):
    """Cut the article body at its <h2> boundaries.

    Returns [(id, html)], the first chunk keyed __intro__ when the body opens
    with prose. <h2> written inside a <pre> sample is not a section break.
    """
    lines = body.split("\n")
    depth = 0
    cuts = []
    for i, line in enumerate(lines):
        opens = len(re.findall(r"<pre\b", line))
        closes = len(re.findall(r"</pre>", line))
        if depth == 0 and opens == 0 and re.match(r"\s*<h2[\s>]", line):
            cuts.append(i)
        depth += opens - closes
    if not cuts:
        raise Bail("body has no <h2> section breaks")
    out = []
    if lines[: cuts[0]] and "".join(lines[: cuts[0]]).strip():
        out.append(("__intro__", "\n".join(lines[: cuts[0]])))
    bounds = cuts + [len(lines)]
    for a, b in zip(bounds, bounds[1:]):
        chunk = "\n".join(lines[a:b])
        m = re.search(r'<h2[^>]*\bid="([^"]+)"', chunk)
        out.append((m.group(1) if m else "s-%d" % a, chunk))
    return out


def scaffold(slug, force=False):
    path = os.path.join(BLOG, slug + ".html")
    s = read(path)
    if 'class="l-en"' in s and not force:
        return "skip (already bilingual)"

    variant = hero_variant(s)

    # 1. head — the alternate locale and the inLanguage array must land with
    #    the .l-en markup, or check_visibility S1 fails on the intermediate.
    m = re.search(r'( *)<meta property="og:locale" content="[^"]*">\n', s)
    if not m:
        raise Bail("no og:locale tag")
    if "og:locale:alternate" not in s:
        s = s[: m.end()] + m.group(1) + ALTERNATE + "\n" + s[m.end():]

    m = re.search(r'( *)"inLanguage": "th",\n', s)
    if m:
        pad = m.group(1)
        s = (s[: m.start()] + pad + '"inLanguage": [\n' + pad + '  "th",\n'
             + pad + '  "en"\n' + pad + "],\n" + s[m.end():])
    elif '"inLanguage": [' not in s:
        raise Bail("no JSON-LD inLanguage field")

    # 2. the switch CSS, last rule before </style>
    i = s.rindex("  </style>")
    s = s[:i] + "\n" + ref_css(variant) + "\n" + s[i:]

    # 3. three posts open <main> after the hero, which would leave the pill and
    #    the hero title outside `#langSwitch:checked ~ main`. Move the landmark
    #    up to wrap the hero, as the other 34 posts already do.
    hero_open = re.search(r'( *)<(header|section) class="post-hero">', s)
    if not hero_open:
        raise Bail("no .post-hero element")
    main_open = re.search(r' *<main id="main">\n?', s)
    if not main_open:
        raise Bail("no <main id=\"main\">")
    if main_open.start() > hero_open.start():
        pad = hero_open.group(1)
        s = s[: main_open.start()] + s[main_open.end():]      # drop it...
        hero_open = re.search(r' *<(header|section) class="post-hero">', s)
        s = (s[: hero_open.start()] + pad + '<main id="main">\n\n'
             + s[hero_open.start():])                          # ...and re-open it above the hero

    # 4. the checkbox: a direct child of <body>, before <main>
    m = re.search(r'<a href="#main" class="skip-link">[^<]*</a>\n', s)
    if not m:
        raise Bail("no skip link")
    s = s[: m.end()] + CHECKBOX + "\n" + s[m.end():]

    # 5. hero title + optional sub become one element with two spans — never a
    #    second <h1> (INV-11).
    def pair(tag, cls, token):
        nonlocal s
        m = re.search(r'(<%s class="%s"[^>]*>)(.*?)(</%s>)' % (tag, cls, tag), s, re.S)
        if not m:
            return None
        inner = m.group(2)
        new = ('%s<span class="l-th">%s</span><span class="l-en" lang="en">%s</span>%s'
               % (m.group(1), inner, token, m.group(3)))
        s = s[: m.start()] + new + s[m.end():]
        return inner.strip()

    th_title = pair("h1", "post-hero__title", "%%EN-TITLE%%")
    if th_title is None:
        raise Bail("no .post-hero__title")
    th_sub = pair("p", "post-hero__sub", "%%EN-SUB%%")

    # 6. the pill, immediately before the hero cover
    m = re.search(r'( *)<div class="post-hero__(cover|image)">', s)
    if not m:
        raise Bail("no hero cover block")
    s = s[: m.start()] + m.group(1) + LABEL + "\n" + s[m.start():]

    # 7. body: split the article, namespace the ids, build both tracks
    art = re.search(r'<article class="post-body">\n', s)
    if not art:
        raise Bail("no <article class=\"post-body\">")
    toc = re.search(r'( *)<details class="post-toc" open>\n(.*?)\n( *)</details>\n',
                    s[art.end():], re.S)
    if not toc:
        raise Bail("no .post-toc")
    toc_start = art.end() + toc.start()
    toc_end = art.end() + toc.end()

    # openclaw-integrations puts its 7-chip strip at the TOP of the article,
    # where the other six put it at the bottom. Either way the strip belongs to
    # neither track — a copy in each would give INV-03 two current chips.
    snav = re.compile(r'(<nav[^>]*>\s*)?<div class="series-nav">.*?</div>\s*</div>\s*'
                      r'(</nav>\s*)?', re.S)
    lead = snav.search(s, toc_end)
    if lead and not s[toc_end:lead.start()].strip():
        toc_end = lead.end()

    marker = None
    for cand in ('<div class="series-nav">', '<div class="post-series-footer">',
                 '<p class="post-series-footer">', '<div class="post-nav">',
                 "</article>"):
        j = s.find(cand, toc_end)
        if j != -1 and (marker is None or j < marker[0]):
            marker = (j, cand)
    if marker is None:
        raise Bail("no body-closing marker")
    body_end, marker_text = marker

    # Six OpenClaw posts wrap the chip strip in <nav aria-label=…>. Cutting at
    # the <div> would strand that opening tag inside the Thai track while its
    # </nav> stayed outside — malformed nesting, and the landmark would wrap
    # nothing. Take the whole landmark, not just the div.
    wrapper = re.search(r"<nav\b[^>]*>\s*$", s[:body_end])
    if wrapper:
        body_end = wrapper.start()
    body = s[toc_end:body_end].rstrip("\n")

    ids = re.findall(r'<h[1-6][^>]*\bid="([^"]+)"', body)
    if not ids:
        raise Bail("body has no heading ids")

    def namespace(text, prefix):
        out = text
        for hid in ids:
            out = re.sub(r'(<h[1-6][^>]*\bid=")%s(")' % re.escape(hid),
                         r"\g<1>%s-%s\g<2>" % (prefix, hid), out)
            out = out.replace('href="#%s"' % hid, 'href="#%s-%s"' % (prefix, hid))
        return out

    th_body = namespace(body, "th")
    sections = split_sections(body)

    pad = toc.group(1)
    th_toc = s[toc_start:toc_end]
    th_toc = th_toc.replace('<details class="post-toc" open>',
                            '<details class="post-toc l-th" open>')
    th_toc = re.sub(r"<summary>.*?</summary>", "<summary>%s</summary>" % TH_SUMMARY,
                    th_toc, flags=re.S)
    th_toc = namespace(th_toc, "th")

    toc_items = re.findall(r'<li><a href="#([^"]+)">(.*?)</a></li>',
                           s[toc_start:toc_end], re.S)
    en_lines = [pad + '<details class="post-toc l-en" open>',
                pad + "  <summary>%s</summary>" % EN_SUMMARY,
                pad + "  <ol>"]
    for hid, _ in toc_items:
        en_lines.append(pad + '      <li><a href="#en-%s">%%%%EN-TOC:%s%%%%</a></li>'
                        % (hid, hid))
    en_lines += [pad + "  </ol>", pad + "</details>"]
    en_toc = "\n".join(en_lines) + "\n"

    track = [pad + '<div class="l-th">', th_body, pad + "</div>",
             pad + '<div class="l-en" lang="en">', ""]
    for hid, _ in sections:
        track.append(pad + "%%%%EN-SECTION:%s%%%%" % hid)
        track.append("")
    track += [pad + "</div>", ""]

    s = s[:toc_start] + th_toc + en_toc + "\n".join(track) + "\n" + s[body_end:]

    # 8. the series footer, where it is Thai (claude-code-architecture's is
    #    already English prose and needs no second track)
    m = re.search(r'(<(?:div|p) class="post-series-footer">)(.*?)(</(?:div|p)>)', s, re.S)
    th_footer = None
    if m and THAI.search(m.group(2)):
        th_footer = m.group(2).strip()
        s = (s[: m.start()] + '%s<span class="l-th">%s</span>'
             '<span class="l-en" lang="en">%%%%EN-FOOTER%%%%</span>%s'
             % (m.group(1), th_footer, m.group(3)) + s[m.end():])

    write(path, s)

    job = {
        "slug": slug, "variant": variant, "marker": marker_text,
        "title": th_title, "sub": th_sub, "footer": th_footer,
        "toc": [{"id": hid, "th": " ".join(t.split())} for hid, t in toc_items],
        "sections": [{"id": hid, "th": html} for hid, html in sections],
    }
    if not os.path.isdir(WORKDIR):
        os.makedirs(WORKDIR)
    write(os.path.join(WORKDIR, slug + ".json"),
          json.dumps(job, ensure_ascii=False, indent=1))
    return "scaffolded (%s, %d sections, marker %s)" % (
        variant, len(sections), marker_text)


# ── fill ────────────────────────────────────────────────────────────────────

def fill(slug, src=None):
    """Splice an answer sheet into the placeholders.

    The sheet is HTML, not JSON — an EN track is markup, and quoting markup
    into JSON is where translators lose <code> blocks. Delimiters:

        <!--EN-TITLE-->            one line of text
        <!--EN-SUB-->              one line of text
        <!--EN-TOC:the-id-->       one line of text
        <!--EN-SECTION:the-id-->   the section's markup, h2 first
        <!--EN-FOOTER-->           one line of text
    """
    path = os.path.join(BLOG, slug + ".html")
    src = src or os.path.join(WORKDIR, slug + ".en.html")
    s = read(path)
    sheet = read(src)

    parts = re.split(r"<!--EN-(TITLE|SUB|FOOTER|TOC:[^>]+?|SECTION:[^>]+?)-->", sheet)
    if len(parts) < 3:
        raise Bail("answer sheet has no <!--EN-...--> delimiters")
    filled = 0
    for key, val in zip(parts[1::2], parts[2::2]):
        if key.startswith("SECTION:"):
            hid = key.split(":", 1)[1]
            token = "%%EN-SECTION:" + hid + "%%"   # never %-format a %% token
            body = val.strip("\n").rstrip()
            # ids and in-section anchors are the script's business, not the
            # translator's: force them rather than trusting the sheet.
            body = re.sub(r'(<h[1-6][^>]*\bid=")(?:th-|en-)?([^"]+)(")',
                          r"\g<1>en-\g<2>\g<3>", body)
            body = re.sub(r'href="#(?:th-|en-)?([^"]+)"', r'href="#en-\g<1>"', body)
            repl = body
        else:
            token = {"TITLE": "%%EN-TITLE%%", "SUB": "%%EN-SUB%%",
                     "FOOTER": "%%EN-FOOTER%%"}.get(key)
            if token is None:
                token = "%%EN-TOC:" + key.split(":", 1)[1] + "%%"
            repl = " ".join(val.split())
        if token not in s:
            print("  ! no placeholder for %s" % key, file=sys.stderr)
            continue
        s = s.replace(token, repl, 1)
        filled += 1
    write(path, s)
    left = len(re.findall(r"%%EN-[A-Z]+", s))
    return "filled %d, %d placeholder(s) left" % (filled, left)


# ── verify ──────────────────────────────────────────────────────────────────

def verify(slug):
    """Per-file checks the sitewide linters cannot make.

    check_site and check_visibility both read the whole tree, so neither can be
    run while a fleet is mid-conversion. These are file-scoped and safe to run
    on one post at any time.
    """
    path = os.path.join(BLOG, slug + ".html")
    s = read(path)
    job = json.load(open(os.path.join(WORKDIR, slug + ".json"), encoding="utf-8"))
    bad = []

    def want(n, needle, what):
        got = s.count(needle)
        if got != n:
            bad.append("%s: %d, want %d" % (what, got, n))

    want(1, 'id="langSwitch"', "checkbox")
    want(1, 'for="langSwitch"', "label")
    want(1, '<div class="l-th">', "l-th track")
    want(1, '<div class="l-en" lang="en">', "l-en track")
    want(1, '<details class="post-toc l-th" open>', "TH toc")
    want(1, '<details class="post-toc l-en" open>', "EN toc")
    want(1, "og:locale:alternate", "og:locale:alternate")
    want(1, "<h1", "h1")
    want(1, '<main id="main"', "main landmark")
    if '"inLanguage": [' not in s:
        bad.append("inLanguage is not an array")

    # Any surviving marker fragment means a partial splice — including the
    # bare-% wreckage a %-formatted token used to leave behind.
    left = re.findall(r"EN-(?:TITLE|SUB|FOOTER|TOC:[^%\s<]*|SECTION:[^%\s<]*)", s)
    if left:
        bad.append("%d placeholder fragment(s) left: %s" % (len(left), left[:4]))

    # the pill must match the hero family, or it disappears into its own hero
    fingerprint = ("rgba(255,255,255,0.85)" if job["variant"] == "deepblue"
                   else "rgba(34,98,153,0.25)")
    if fingerprint not in s:
        bad.append("wrong .lang-switch variant for a %s hero" % job["variant"])

    # ids: one th- and one en- per section, and every anchor resolves
    ids = re.findall(r'id="([^"]+)"', s)
    th = {i[3:] for i in ids if i.startswith("th-")}
    en = {i[3:] for i in ids if i.startswith("en-")}
    if th != en:
        bad.append("th/en heading ids differ: only-th=%s only-en=%s"
                   % (sorted(th - en)[:4], sorted(en - th)[:4]))
    dead = [a for a in set(re.findall(r'href="#((?:th|en)-[^"]+)"', s)) if a not in ids]
    if dead:
        bad.append("dead anchors: %s" % sorted(dead)[:4])

    # navigation belongs to neither track — a copy in each breaks INV-03/INV-04b
    if s.count('class="current"') > 1:
        bad.append("%d current chips (series-nav duplicated into a track)"
                   % s.count('class="current"'))
    n_pnav = s.count('class="post-nav__link"')
    if n_pnav not in (0, 2):
        bad.append("%d post-nav links (want 0 or 2)" % n_pnav)

    # the two tracks must mirror each other element for element
    i_th = s.find('<div class="l-th">')
    i_en = s.find('<div class="l-en" lang="en">')
    i_end = s.find(job["marker"], i_en)
    if min(i_th, i_en, i_end) < 0:
        bad.append("cannot locate both tracks")
    else:
        a, b = s[i_th:i_en], s[i_en:i_end]
        for tag in ("<h2", "<h3", "<pre", "<table", "<blockquote"):
            if a.count(tag) != b.count(tag):
                bad.append("%s count TH=%d EN=%d" % (tag, a.count(tag), b.count(tag)))
        thai = THAI.findall(b)
        if thai:
            ctx = re.search(r".{0,60}[฀-๿].{0,60}", b, re.S)
            bad.append("%d Thai character(s) left in the EN track, e.g. %r"
                       % (len(thai), ctx.group(0).strip() if ctx else ""))

    for line in bad:
        print("  ✗ %s" % line)
    print("%-34s %s" % (slug, "OK" if not bad else "%d problem(s)" % len(bad)))
    return 1 if bad else 0


def status():
    rows = []
    for name in sorted(os.listdir(BLOG)):
        if not name.endswith(".html") or name == "index.html":
            continue
        s = read(os.path.join(BLOG, name))
        left = len(re.findall(r"%%EN-[A-Z]+", s))
        if 'class="l-en"' in s or left:
            rows.append((name[:-5], "bilingual" if not left else "%d TODO" % left))
    done = sum(1 for _, v in rows if v == "bilingual")
    for slug, state in rows:
        if state != "bilingual":
            print("  %-34s %s" % (slug, state))
    print("%d bilingual, %d with placeholders remaining" % (done, len(rows) - done))
    return 0 if done == len(rows) else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--post", action="append", default=[])
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--fill")
    ap.add_argument("--from", dest="src")
    ap.add_argument("--verify", action="append", default=[])
    ap.add_argument("--verify-all", action="store_true")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()

    if a.status:
        return status()
    if a.verify or a.verify_all:
        slugs = a.verify or sorted(f[:-5] for f in os.listdir(WORKDIR)
                                   if f.endswith(".json"))
        return max(verify(slug) for slug in slugs)
    if a.fill:
        print("%-34s %s" % (a.fill, fill(a.fill, a.src)))
        return 0

    targets = a.post
    if a.all:
        idx = read(os.path.join(BLOG, "index.html"))
        for sid in ("series-openclaw", "series-devops"):
            m = re.search(r'<section class="series-section" id="%s">(.*?)</section>' % sid,
                          idx, re.S)
            targets += re.findall(r'<a href="([a-z0-9-]+)\.html" class="card">', m.group(1))
    if not targets:
        ap.error("nothing to do — pass --post, --all, --fill or --status")

    rc = 0
    for slug in targets:
        try:
            print("%-34s %s" % (slug, scaffold(slug, a.force)))
        except Bail as exc:
            print("%-34s BAIL: %s" % (slug, exc), file=sys.stderr)
            rc = 1
    return rc


if __name__ == "__main__":
    sys.exit(main())
