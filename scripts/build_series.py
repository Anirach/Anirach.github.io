#!/usr/bin/env python3
"""Emit a whole numbered blog series from one manifest plus per-post content sheets.

Adding a post to this site is a file plus a card plus two counters plus the
neighbours' nav links, all hand-edited.  That is tolerable once.  For a
twenty-post series launched in one go it is not: the chip strip alone is
twenty near-identical blocks that must agree with each other in twenty files,
and the OpenClaw series already carries a linter constant whose comment exists
because that exact miss happened.

So the mechanical half is code and the editorial half is not:

  manifest   scripts/series/<name>.json — the fixed strings.  Numbers, slugs,
             chip labels, titles, hero subs, tags, descriptions, read times,
             covers and figures.  One place, so the post, the card, the strip,
             the feed and llms.txt cannot disagree.
  sheets     .bilingual/<slug>.{th,en}.html — the prose, in the same delimiter
             grammar bilingualize.py already uses for its answer sheets.  A
             writer writes sections; ids, anchors, figures, tracks, the switch
             and the whole head are none of their business.
  skeleton   blog/hermes-101.html, read at RUN TIME.  The <style> block is
             byte-identical across all ten Hermes posts, so it is a real
             template rather than a copy that will rot; --check diffs what it
             lifted so a future edit to the reference is noticed, not silently
             inherited.

The emitted posts are the committed truth.  Sheets are scratch.  After launch
only --restrip touches a shipped file, and it rewrites nothing but the strip.

    python3 scripts/build_series.py --check
    python3 scripts/build_series.py --all
    python3 scripts/build_series.py --post ai-transformation-layers
    python3 scripts/build_series.py --restrip
    python3 scripts/build_series.py --index-fragment
    python3 scripts/build_series.py --llms-fragment
"""

import argparse
import html as htmlmod
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG = os.path.join(ROOT, "blog")
IMAGES = os.path.join(ROOT, "images")
WORKDIR = os.path.join(ROOT, ".bilingual")
SERIES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "series")

sys.path.insert(0, os.path.join(ROOT, ".claude", "skills", "site-check", "scripts"))
try:
    from check_site import image_pixel_size
except ImportError:                                          # pragma: no cover
    sys.exit("build_series.py: cannot import check_site.py for image_pixel_size")

SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)+$")
RE_DELIM = re.compile(r"<!--(TH|EN)-(TOC|SECTION):([A-Za-z0-9_-]+)-->")
THAI = re.compile(r"[ก-฾เ-๛]")
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

TH_SUMMARY = "ในบทความนี้"
EN_SUMMARY = "In this post"

# Element counts the two tracks must agree on.  The pairs a translator most
# often silently drops are the ones that carry the argument: a table, a code
# sample, a figure.
MIRROR_TAGS = ("<h2", "<h3", "<pre", "<table", "<blockquote", "<ul", "<ol",
               "<li", "key-takeaways", "table-wrapper", "<!--FIGURE:",
               "references__list")


class Bail(Exception):
    pass


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def write(path, text):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def pretty_date(iso):
    y, m, d = iso.split("-")
    return "%d %s %s" % (int(d), MONTHS[int(m) - 1], y)


def roman(n):
    out, table = "", [(10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]
    for v, s in table:
        while n >= v:
            out, n = out + s, n - v
    return out


# ── the skeleton ────────────────────────────────────────────────────────────

def skeleton(man):
    """Lift the shared chrome out of the reference post.

    Three blocks are read verbatim because they are genuinely shared and
    genuinely large: the whole <style>, the top nav and the footer.  Everything
    else in the head is per-post and is generated below, in hermes-101's exact
    line order — --check compares the generated shape against the reference so
    the two cannot drift apart unnoticed."""
    s = read(os.path.join(BLOG, man["skeleton"]))
    out = {}
    i, j = s.index("  <style>"), s.index("  </style>") + len("  </style>")
    out["style"] = s[i:j]
    m = re.search(r'  <nav class="blog-nav">.*?</nav>\n', s, re.S)
    if not m:
        raise Bail("skeleton has no .blog-nav")
    out["nav"] = m.group(0)
    m = re.search(r'  <footer class="blog-footer">.*?</footer>\n', s, re.S)
    if not m:
        raise Bail("skeleton has no .blog-footer")
    out["footer"] = m.group(0)
    m = re.search(r"  <!-- social -->\n(.*?)  <!-- /social -->\n", s, re.S)
    if not m:
        raise Bail("skeleton has no social block")
    out["social_keys"] = re.findall(r'<(?:meta|link)[^>]*?(?:property|name|rel)="([^"]+)"',
                                    m.group(1))
    return out


EXTRA_CSS = """
    /* ── FIGURE — the sanctioned diagram component (page-design §4 Content).
       Diagrams are PNGs; this repo built them out of divs twice and reverted
       twice. The image is wrapped in a link to itself so a phone can pinch a
       1400px drawing without a line of JavaScript. */
    .figure { margin: 2.5rem 0; }
    .figure__img { width: 100%; height: auto; display: block;
                   border-radius: var(--radius); border: 1px solid rgba(0,0,0,0.06); }
    .figure__caption { font-size: 0.85rem; color: var(--slate-light);
                       text-align: center; margin-top: 0.75rem; }

    /* ── REFERENCES — every material number in this series carries its source.
       The tags are the book's own four evidence labels. */
    .references { margin-top: 3rem; padding-top: 2rem; border-top: 1px solid #e2e8f0; }
    .references__note { font-size: 0.85rem; color: var(--slate-light); margin-bottom: 1rem; }
    .references__list { padding-left: 1.4rem; font-size: 0.9rem; line-height: 1.75; }
    .references__list li { margin-bottom: 0.7rem; }
    .ref-tag { display: inline-block; font-size: 0.7rem; font-weight: 700;
               letter-spacing: 0.06em; text-transform: uppercase; padding: 0.1rem 0.5rem;
               border-radius: 50px; margin-right: 0.4rem; vertical-align: 0.05em;
               background: rgba(34,98,153,0.1); color: var(--blue-dark); }
    .ref-tag--law { background: rgba(239,68,68,0.12); color: #991b1b; }
    .ref-tag--synthesis { background: rgba(196,164,108,0.22); color: var(--gold-dark); }
    .ref-supports { display: block; color: var(--slate-light); font-size: 0.85rem; }

    /* ── SERIES STRIP, GROUPED — twenty chips is four rows of noise unless they
       are grouped, so the four parts of the book label their own rows. The
       .series-nav and .series-links wrappers stay byte-literal because INV-08
       recognises the strip by exactly those two, and the chips stay direct
       children of a group because INV-03's item regex cannot see through a
       nested tag. Grouping is a modifier plus two elements of .series-links —
       the flat OpenClaw, Hermes and Life strips are untouched. */
    .series-links--grouped { display: grid; gap: 0.9rem; }
    .series-links__group { position: relative; display: flex; flex-wrap: wrap;
                           gap: 0.5rem; padding-left: 8.25rem; min-height: 2rem; }
    .series-links__label { position: absolute; left: 0; top: 0.45rem; width: 7.5rem;
                           margin: 0; font-size: 0.72rem; font-weight: 700;
                           text-transform: uppercase; letter-spacing: 0.08em;
                           color: var(--slate-light); line-height: 1.3; }
    @media (max-width: 600px) {
      .series-links__group { padding-left: 0; }
      .series-links__label { position: static; width: auto; flex-basis: 100%;
                             margin-bottom: 0.1rem; }
    }
"""


def styled(style, man):
    """Inject the series' own CSS, plus the one token it adds."""
    if "--coral" not in style:
        style = style.replace(
            "--gold: #c4a46c; --gold-dark: #7a5f22;",
            "--gold: #c4a46c; --gold-dark: #7a5f22; --coral: #c2410c;", 1)
    anchor = "    /* ── LANGUAGE SWITCH"
    if anchor not in style:
        raise Bail("skeleton style has no LANGUAGE SWITCH block to anchor on")
    return style.replace(anchor, EXTRA_CSS.strip("\n") + "\n\n" + anchor, 1)


# ── sheets ──────────────────────────────────────────────────────────────────

def parse_sheet(path, lang):
    """(toc, sections) from an answer sheet.  Same delimiter grammar as
    bilingualize.py --fill, with a TH twin, because a writer who has learnt one
    should not have to learn a second."""
    s = read(path)
    hits = list(RE_DELIM.finditer(s))
    if not hits:
        raise Bail("%s has no <!--%s-...--> delimiters" % (os.path.basename(path), lang))
    toc, sections = [], []
    for m, nxt in zip(hits, hits[1:] + [None]):
        got, kind, key = m.group(1), m.group(2), m.group(3)
        if got != lang:
            raise Bail("%s carries a %s delimiter" % (os.path.basename(path), got))
        body = s[m.end():nxt.start() if nxt else len(s)]
        if kind == "TOC":
            toc.append((key, " ".join(body.split())))
        else:
            sections.append((key, body.strip("\n").rstrip()))
    return toc, sections


def figure_markup(fig, lang, pad):
    src = "../images/" + fig["file"]
    size = image_pixel_size(os.path.join(IMAGES, fig["file"]))
    if not size:
        raise Bail("cannot measure images/%s — draw it before building" % fig["file"])
    w, h = size
    return (
        '%s<figure class="figure">\n'
        '%s  <a href="%s">\n'
        '%s    <img class="figure__img" src="%s" alt="%s" width="%d" height="%d" '
        'loading="lazy" decoding="async">\n'
        '%s  </a>\n'
        '%s  <figcaption class="figure__caption">%s</figcaption>\n'
        '%s</figure>' % (pad, pad, src, pad, src, htmlmod.escape(fig["alt"][lang], quote=True),
                         w, h, pad, pad, htmlmod.escape(fig["caption"][lang]), pad))


def namespace(text, prefix, ids):
    """th-/en- the heading ids and the anchors that point at them.  The writer
    writes bare ids; which track a section lands in is the builder's problem."""
    out = text
    for hid in ids:
        out = re.sub(r'(<h[1-6][^>]*\bid=")%s(")' % re.escape(hid),
                     r"\g<1>%s-%s\g<2>" % (prefix, hid), out)
        out = re.sub(r'(<section[^>]*\bid=")%s(")' % re.escape(hid),
                     r"\g<1>%s-%s\g<2>" % (prefix, hid), out)
        out = re.sub(r'(\baria-labelledby=")%s(")' % re.escape(hid),
                     r"\g<1>%s-%s\g<2>" % (prefix, hid), out)
        out = out.replace('href="#%s"' % hid, 'href="#%s-%s"' % (prefix, hid))
    out = re.sub(r'(<li[^>]*\bid=")(ref-\d+)(")', r"\g<1>%s-\g<2>\g<3>" % prefix, out)
    out = re.sub(r'href="#(ref-\d+)"', r'href="#%s-\g<1>"' % prefix, out)
    return out


def track(post, sheet_ids, sections, lang, figs, pad="    "):
    prefix = "th" if lang == "th" else "en"
    body = []
    for key, markup in sections:
        markup = namespace(markup, prefix, sheet_ids)

        def sub(m, _l=lang, _p=pad):
            name = m.group(1)
            if name not in figs:
                raise Bail("unknown figure %r (manifest has %s)"
                           % (name, ", ".join(sorted(figs)) or "none"))
            return figure_markup(figs[name], _l, _p)

        markup = re.sub(r"[ \t]*<!--FIGURE:([A-Za-z0-9_-]+)-->", sub, markup)
        body.append(markup)
    open_tag = ('<div class="l-th">' if lang == "th"
                else '<div class="l-en" lang="en">')
    return "%s%s\n\n%s\n%s</div>\n" % (pad, open_tag, "\n\n".join(body), pad)


def toc_block(toc, lang, pad="    "):
    prefix, summary, cls = (("th", TH_SUMMARY, "l-th") if lang == "th"
                            else ("en", EN_SUMMARY, "l-en"))
    lines = ['%s<details class="post-toc %s" open>' % (pad, cls),
             "%s  <summary>%s</summary>" % (pad, summary),
             "%s  <ol>" % pad]
    for key, text in toc:
        lines.append('%s      <li><a href="#%s-%s">%s</a></li>' % (pad, prefix, key, text))
    lines += ["%s  </ol>" % pad, "%s</details>" % pad]
    return "\n".join(lines) + "\n"


# ── the strip ───────────────────────────────────────────────────────────────

STRIP_OPEN = '    <nav aria-label="%s">'
STRIP_CLOSE = "    </nav>"


def strip_block(man, slug):
    by_group = {g["key"]: [] for g in man["groups"]}
    for p in man["posts"]:
        by_group[p["group"]].append(p)
    lines = [STRIP_OPEN % man["aria_label"],
             '    <div class="series-nav">',
             "      <h3>%s</h3>" % htmlmod.escape(man["h3"]),
             '      <div class="series-links series-links--grouped">']
    for g in man["groups"]:
        lines.append('        <div class="series-links__group">')
        lines.append('          <p class="series-links__label">%s</p>'
                     % htmlmod.escape(g["label"]))
        for p in by_group[g["key"]]:
            label = htmlmod.escape(p["chip"])
            if p["slug"] == slug:
                lines.append('          <span class="current" aria-current="page">%s</span>'
                             % label)
            else:
                lines.append('          <a href="/blog/%s">%s</a>' % (p["slug"], label))
        lines.append("        </div>")
    lines += ["      </div>", "    </div>", STRIP_CLOSE]
    return "\n".join(lines) + "\n"


# ── the page ────────────────────────────────────────────────────────────────

def build(man, post, sk):
    slug = post["slug"]
    figs = {f["name"]: f for f in post["figures"]}
    th_toc, th_sec = parse_sheet(os.path.join(WORKDIR, slug + ".th.html"), "TH")
    en_toc, en_sec = parse_sheet(os.path.join(WORKDIR, slug + ".en.html"), "EN")

    th_ids = [k for k, _ in th_sec if k != "__intro__"]
    en_ids = [k for k, _ in en_sec if k != "__intro__"]
    if th_ids != en_ids:
        raise Bail("track section ids differ: th=%s en=%s" % (th_ids, en_ids))
    if [k for k, _ in th_toc] != th_ids:
        raise Bail("TOC ids %s do not match section ids %s" % ([k for k, _ in th_toc], th_ids))
    if [k for k, _ in en_toc] != en_ids:
        raise Bail("EN TOC ids do not match its section ids")

    th_body = "".join(m for _k, m in th_sec)
    en_body = "".join(m for _k, m in en_sec)
    for tag in MIRROR_TAGS:
        a, b = th_body.count(tag), en_body.count(tag)
        if a != b:
            raise Bail("%s count TH=%d EN=%d — the tracks must mirror" % (tag, a, b))
    if THAI.search(en_body):
        ctx = re.search(r".{0,60}[ก-฾เ-๛].{0,60}", en_body, re.S)
        raise Bail("Thai left in the EN sheet: %r" % ctx.group(0).strip())
    for name in re.findall(r"<!--FIGURE:([A-Za-z0-9_-]+)-->", th_body):
        if name not in figs:
            raise Bail("sheet uses figure %r, not in the manifest" % name)
    for bad in ("<h1", "<script", "<style", "style=", "%%EN-"):
        if bad in th_body or bad in en_body:
            raise Bail("sheet contains %r — the builder owns that" % bad)

    date, title, sub = man["date"], post["title"], post["sub"]
    canon = "https://anirach.com/blog/%s.html" % slug
    og = "https://anirach.com/images/%s-og.jpg" % slug
    og_file = os.path.join(IMAGES, "%s-og.jpg" % slug)
    size = image_pixel_size(og_file)
    if not size:
        raise Bail("cannot measure images/%s-og.jpg — draw the covers first" % slug)
    ogw, ogh = size
    cover = post["cover"]
    csize = image_pixel_size(os.path.join(IMAGES, cover))
    if not csize:
        raise Bail("cannot measure images/%s" % cover)
    cw, ch = csize
    esc = lambda s: htmlmod.escape(s, quote=True)

    head = """<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>%(title_th)s | Anirach Mingkhwan</title>
  <meta name="description" content="%(desc)s">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Sarabun:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
%(style)s
  <!-- social -->
  <link rel="canonical" href="%(canon)s">
  <meta property="og:type" content="article">
  <meta property="og:url" content="%(canon)s">
  <meta property="og:site_name" content="Anirach Mingkhwan">
  <meta property="og:locale" content="th_TH">
  <meta property="og:locale:alternate" content="en_US">
  <meta property="article:published_time" content="%(date)s">
  <meta property="article:author" content="https://anirach.com/">
  <meta property="og:title" content="%(title_th)s">
  <meta property="og:description" content="%(desc)s">
  <meta property="og:image" content="%(og)s">
  <meta property="og:image:width" content="%(ogw)d">
  <meta property="og:image:height" content="%(ogh)d">
  <meta property="og:image:alt" content="%(title_th)s">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="%(og)s">
  <meta name="twitter:image:alt" content="%(title_th)s">
  <meta name="robots" content="max-image-preview:large">
  <meta name="theme-color" content="#11304b">
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <!-- /social -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    "headline": "%(title_json)s",
    "author": {
      "@type": "Person",
      "@id": "https://anirach.com/#person",
      "name": "Anirach Mingkhwan",
      "url": "https://anirach.com/"
    },
    "datePublished": "%(date)s",
    "dateModified": "%(date)s",
    "image": "%(og)s",
    "inLanguage": [
      "th",
      "en"
    ],
    "mainEntityOfPage": "%(canon)s"
  }
  </script>
</head>
""" % {"title_th": esc(title["th"]), "desc": esc(post["description"]),
       "style": styled(sk["style"], man), "canon": canon, "date": date,
       "og": og, "ogw": ogw, "ogh": ogh,
       "title_json": json.dumps(title["th"], ensure_ascii=False)[1:-1]}

    hero = """  <main id="main">

  <header class="post-hero">
    <div class="post-hero__tags">
%(tags)s
    </div>
    <h1 class="post-hero__title"><span class="l-th">%(t_th)s</span><span class="l-en" lang="en">%(t_en)s</span></h1>
    <p class="post-hero__sub"><span class="l-th">%(s_th)s</span><span class="l-en" lang="en">%(s_en)s</span></p>
    <div class="post-hero__meta">
      <span>By <strong>Anirach Mingkhwan</strong></span>
      <span class="post-hero__series">%(series)s</span>
      <span><time datetime="%(date)s">%(pretty)s</time></span>
      <span>%(read)d min read</span>
    </div>
    <label for="langSwitch" class="lang-switch" title="สลับภาษา · Switch language"><span class="lang-th">ไทย</span><span class="lang-sep">·</span><span class="lang-en" lang="en">English</span></label>
    <div class="post-hero__cover">
      <img src="../images/%(cover)s" alt="%(t_th)s" width="%(cw)d" height="%(ch)d" loading="eager" fetchpriority="high" decoding="async">
    </div>
  </header>

""" % {"tags": "\n".join('      <span class="post-hero__tag">%s</span>' % htmlmod.escape(t)
                         for t in post["tags"]),
       "t_th": htmlmod.escape(title["th"]), "t_en": htmlmod.escape(title["en"]),
       "s_th": htmlmod.escape(sub["th"]), "s_en": htmlmod.escape(sub["en"]),
       "series": man["hero_series"] % post["n"], "date": date,
       "pretty": pretty_date(date), "read": post["read_min"],
       "cover": cover, "cw": cw, "ch": ch}

    article = ("  <article class=\"post-body\">\n\n"
               + toc_block(th_toc, "th") + toc_block(en_toc, "en")
               + track(post, th_ids, th_sec, "th", figs)
               + "\n"
               + track(post, en_ids, en_sec, "en", figs)
               + "\n"
               + '    <div class="post-series-footer">\n'
               + '      <span class="l-th">%s</span><span class="l-en" lang="en">%s</span>\n'
                 % (htmlmod.escape(man["footer"]["th"]), htmlmod.escape(man["footer"]["en"]))
               + "    </div>\n\n"
               + strip_block(man, slug)
               + "\n  </article>\n\n  </main>\n\n")

    body = ('<body>\n<a href="#main" class="skip-link">Skip to content</a>\n'
            '<input type="checkbox" id="langSwitch" class="lang-switch-box" '
            'aria-label="Switch language: Thai / English">\n\n'
            + sk["nav"].replace(
                '<div class="blog-nav__title">Hermes 101 · รู้จัก Hermes Agent</div>',
                '<div class="blog-nav__title">%s</div>' % htmlmod.escape(post["nav_title"]))
            + "\n" + hero + article + sk["footer"] + "\n</body>\n</html>\n")

    job = {"slug": slug, "variant": man["hero"],
           "marker": '<div class="post-series-footer">',
           "title": title["th"], "sub": sub["th"], "footer": man["footer"]["th"],
           "toc": [{"id": k, "th": t} for k, t in th_toc],
           "sections": [{"id": k, "th": m} for k, m in th_sec]}
    return head + body, job


# ── commands ────────────────────────────────────────────────────────────────

def visible_chars(path):
    """Thai characters a reader actually reads: markup, comments and code
    samples stripped.  <pre> goes because a reader scans a command block, they
    do not read it at prose speed."""
    s = read(path)
    s = re.sub(r"<pre.*?</pre>", "", s, flags=re.S)
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    return len(re.sub(r"<[^>]+>", "", s))


# hermes-101 measures ~22,000 visible Thai characters against its own "15 min
# read" label.  That is the house rate, and it is the only defensible source
# for one: a number typed by hand drifts the moment a section is added.
CHARS_PER_MIN = 1465


def sync_read_min(man):
    """Rewrite read_min from what the Thai sheets actually contain.

    The label appears twice — the hero and the card — and both come from the
    manifest, so measuring once here keeps them true and identical."""
    path = os.path.join(SERIES_DIR, man["series"] + ".json")
    on_disk = json.load(open(path, encoding="utf-8"))
    changed = 0
    for post, live in zip(on_disk["posts"], man["posts"]):
        sheet = os.path.join(WORKDIR, post["slug"] + ".th.html")
        if not os.path.exists(sheet):
            print("%-38s no sheet yet" % post["slug"])
            continue
        n = visible_chars(sheet)
        want = max(1, round(n / CHARS_PER_MIN))
        if want != post["read_min"]:
            print("%-38s %5d ch  %2d -> %2d min" % (post["slug"], n, post["read_min"], want))
            post["read_min"] = live["read_min"] = want
            changed += 1
        else:
            print("%-38s %5d ch  %2d min" % (post["slug"], n, want))
    if changed:
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(on_disk, fh, ensure_ascii=False, indent=1)
            fh.write("\n")
    print("%d read_min value(s) corrected" % changed)
    return 0


def load(name):
    return json.load(open(os.path.join(SERIES_DIR, name + ".json"), encoding="utf-8"))


def check(man, sk):
    """Everything that can be wrong before a single byte is emitted."""
    bad = []
    posts = man["posts"]
    if [p["n"] for p in posts] != list(range(1, len(posts) + 1)):
        bad.append("post numbers are not 1..%d contiguous" % len(posts))
    sizes = {}
    for p in posts:
        sizes.setdefault(p["group"], []).append(p["n"])
    for g in man["groups"]:
        ns = sizes.get(g["key"], [])
        if len(ns) != len(posts) // len(man["groups"]):
            bad.append("group %s holds %d posts" % (g["key"], len(ns)))
        if ns != sorted(ns):
            bad.append("group %s is out of order: %s" % (g["key"], ns))
    for field, fn in (("slug", lambda p: p["slug"]), ("chip", lambda p: p["chip"]),
                      ("cover", lambda p: p["cover"])):
        seen = [fn(p) for p in posts]
        dupes = {x for x in seen if seen.count(x) > 1}
        if dupes:
            bad.append("duplicate %s: %s" % (field, sorted(dupes)))
    for p in posts:
        if not SLUG_RE.match(p["slug"]):
            bad.append("%s is not a house slug" % p["slug"])
        if "<" in p["chip"]:
            bad.append("%s chip contains markup — INV-03's item regex cannot see through a tag"
                       % p["slug"])
        n = len(p["description"])
        if not 70 <= n <= 160:
            bad.append("%s description is %d chars (want 70-160)" % (p["slug"], n))
        for f in p["figures"]:
            if "-cover." in f["file"] or "-og." in f["file"]:
                bad.append("%s figure %s collides with the cover-detection substring"
                           % (p["slug"], f["file"]))
            if not os.path.exists(os.path.join(IMAGES, f["file"])):
                bad.append("%s figure %s is not drawn yet" % (p["slug"], f["file"]))
            if THAI.search(f["alt"]["en"]) or THAI.search(f["caption"]["en"]):
                bad.append("%s figure %s has Thai in its EN alt/caption" % (p["slug"], f["file"]))
    want = ["canonical", "og:type", "og:url", "og:site_name", "og:locale",
            "og:locale:alternate", "article:published_time", "article:author",
            "og:title", "og:description", "og:image", "og:image:width",
            "og:image:height", "og:image:alt", "twitter:card", "twitter:image",
            "twitter:image:alt", "robots", "theme-color", "icon", "apple-touch-icon"]
    if sk["social_keys"] != want:
        bad.append("the skeleton's social block changed shape: %s" % sk["social_keys"])
    missing = [p["slug"] for p in posts
               if not os.path.exists(os.path.join(WORKDIR, p["slug"] + ".th.html"))
               or not os.path.exists(os.path.join(WORKDIR, p["slug"] + ".en.html"))]
    for line in bad:
        print("  ✗ %s" % line)
    if missing:
        print("  … %d sheet pair(s) not written yet: %s"
              % (len(missing), ", ".join(m.replace("ai-transformation-", "") for m in missing)))
    print("%-22s %s" % (man["series"], "OK" if not bad else "%d problem(s)" % len(bad)))
    return 1 if bad else 0


def emit(man, sk, slugs):
    rc = 0
    if not os.path.isdir(WORKDIR):
        os.makedirs(WORKDIR)
    for p in man["posts"]:
        if slugs and p["slug"] not in slugs:
            continue
        try:
            page, job = build(man, p, sk)
        except Bail as exc:
            print("%-38s BAIL: %s" % (p["slug"], exc), file=sys.stderr)
            rc = 1
            continue
        write(os.path.join(BLOG, p["slug"] + ".html"), page)
        write(os.path.join(WORKDIR, p["slug"] + ".json"),
              json.dumps(job, ensure_ascii=False, indent=1))
        print("%-38s %6d bytes  %d sections  %d figure(s)"
              % (p["slug"], len(page), len(job["sections"]), len(p["figures"])))
    return rc


def restrip(man):
    """Rewrite only the strip, in every member.  The growth path: a 21st post
    means a manifest row, one --post, and this."""
    rc = 0
    for p in man["posts"]:
        path = os.path.join(BLOG, p["slug"] + ".html")
        if not os.path.exists(path):
            print("%-38s missing" % p["slug"], file=sys.stderr)
            rc = 1
            continue
        s = read(path)
        pat = re.compile(re.escape(STRIP_OPEN % man["aria_label"]) + r".*?"
                         + re.escape(STRIP_CLOSE) + r"\n", re.S)
        hits = pat.findall(s)
        if len(hits) != 1:
            print("%-38s %d strip block(s), want 1" % (p["slug"], len(hits)), file=sys.stderr)
            rc = 1
            continue
        new = strip_block(man, p["slug"])
        if hits[0] == new:
            print("%-38s unchanged" % p["slug"])
            continue
        write(path, pat.sub(lambda _m: new, s, count=1))
        print("%-38s strip rewritten" % p["slug"])
    return rc


def index_fragment(man):
    date = man["date"]
    out = ["    <!-- %s Series -->" % man["title"],
           '    <section class="series-section" id="%s">' % man["section_id"],
           '      <div class="series-header">',
           '        <div class="series-header__left">',
           '          <span class="series-icon" aria-hidden="true">%s</span>' % man["icon"],
           '          <h2 class="series-title">%s</h2>' % man["title"],
           "        </div>",
           '        <span class="series-count">%d articles</span>' % len(man["posts"]),
           "      </div>",
           '      <p class="series-description">%s — <span lang="th">%s</span></p>'
           % (htmlmod.escape(man["description"]["en"]), htmlmod.escape(man["description"]["th"])),
           '      <div class="blog-grid">']
    for p in reversed(man["posts"]):
        out += ['        <!-- Card: %s -->' % p["nav_title"],
                '      <a href="%s.html" class="card">' % p["slug"],
                '        <div class="card__image">',
                '          <img src="../images/%s" alt="" width="800" height="800" '
                'loading="lazy" decoding="async">' % p["cover"],
                "        </div>",
                '        <div class="card__body">',
                '          <div class="card__tags">']
        out += ['            <span class="card__tag">%s</span>' % htmlmod.escape(t)
                for t in p["tags"]]
        out += ["          </div>",
                '          <h3 class="card__title"><span lang="th">%s</span></h3>'
                % htmlmod.escape(p["title"]["th"]),
                '          <p class="card__excerpt"><span lang="th">%s</span></p>'
                % htmlmod.escape(p["description"]),
                '          <div class="card__footer">',
                '            <div class="card__author">',
                '              <img src="../images/profile.jpg" alt="" class="card__avatar" '
                'width="800" height="800" loading="lazy" decoding="async">',
                "              <div>",
                '                <div class="card__author-name">Anirach Mingkhwan</div>',
                '                <div class="card__meta"><time datetime="%s">%s</time> '
                '· %d min read</div>' % (date, pretty_date(date), p["read_min"]),
                "              </div>",
                "            </div>",
                '            <span class="card__read">Read →</span>',
                "          </div>", "        </div>", "      </a>"]
    out += ["      </div>", "    </section>"]
    frag = "\n".join(out) + "\n"
    write(os.path.join(WORKDIR, man["series"] + ".index.html"), frag)
    chip = '      <a href="#%s">%s %s · %d</a>' % (
        man["section_id"], man["icon"], htmlmod.escape(man["title"]), len(man["posts"]))
    print(frag)
    print("\n--- jump chip (first in .blog-jump) ---\n" + chip)
    return 0


def llms_fragment(man):
    lines = ["## Blog — %s (bilingual TH/EN)" % man["title"]]
    for p in reversed(man["posts"]):
        lines.append("- [%s](https://anirach.com/blog/%s.html): %s"
                     % (htmlmod.escape(p["title"]["th"]), p["slug"], p["description"]))
    frag = "\n".join(lines) + "\n"
    write(os.path.join(WORKDIR, man["series"] + ".llms.txt"), frag)
    print(frag)
    return 0


def covers_rows(man):
    """The covers.tsv rows this series needs, for cross-checking what was written."""
    for p in man["posts"]:
        ground = "cream" if p["n"] % 2 else "parchment"
        print("%s\t%s\tat_?\t%s\tcoral\tAI TRANSFORMATION · %s\t?\t?\t"
              % (p["slug"], p["cover"], ground, roman(p["n"])))
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--series", default="ai-transformation")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--post", action="append", default=[])
    ap.add_argument("--restrip", action="store_true")
    ap.add_argument("--index-fragment", action="store_true")
    ap.add_argument("--llms-fragment", action="store_true")
    ap.add_argument("--covers-rows", action="store_true")
    ap.add_argument("--sync-read-min", action="store_true")
    ap.add_argument("--date")
    a = ap.parse_args()

    man = load(a.series)
    if a.date:
        man["date"] = a.date
    sk = skeleton(man)

    if a.check:
        return check(man, sk)
    if a.restrip:
        return restrip(man)
    if a.index_fragment:
        return index_fragment(man)
    if a.llms_fragment:
        return llms_fragment(man)
    if a.covers_rows:
        return covers_rows(man)
    if a.sync_read_min:
        return sync_read_min(man)
    if a.all or a.post:
        return emit(man, sk, set(a.post))
    ap.error("nothing to do — pass --check, --all, --post, --restrip, "
             "--sync-read-min, --index-fragment or --llms-fragment")


if __name__ == "__main__":
    sys.exit(main())
