#!/usr/bin/env python3
"""Regenerate blog/index.html — the 2026-09-07 redesign, and its repair tool.

Reads the CURRENT blog/index.html (source of truth for cards, hrefs, covers,
dates, read times, excerpts, titles), the two series manifests, the three
chip-strip host posts and the DevOps .post-nav chain, then re-emits the page:
numbered row cards in reading order, the sticky series bar, the Start-here
spotlight. IDEMPOTENT — safe to re-run on its own output (running it is how
card ordering is repaired after posts are added by hand).

Every string a repo linter or generator reads is kept in its exact shape:
  <a href="slug.html" class="card">                (RE_CARD ×5, single space)
  first <img src=...> in a card = the cover          (INV-07b)
  <h3 class="card__title">...</h3>                   (level-agnostic, no attrs)
  <p class="card__excerpt">...</p>                   (gen_feed, bare <p>)
  <time datetime="YYYY-MM-DD">                       (INV-36)
  <section class="series-section" id="...">          (RE_SECTION)
  <h2 class="series-title">...</h2>                  (check_visibility L2)
  <span class="series-count">N articles</span>       (RE_SERIES_COUNT)
  <span class="blog-hero__stat"><strong>N</strong> Label</span>   (RE_HERO_STAT)
  <nav class="blog-jump" ...> with <a href="#id">text · N</a>      (INV-02f)
  class="feature" for the spotlight (never class="card")

Usage: reindex_blog.py --repo . --out blog/index.html [--order reading|newest]
"""
import argparse, html as htmlmod, json, os, re, sys

RE_CARD = re.compile(r'<a href="([a-z0-9-]+\.html)" class="card">(.*?)</a>', re.S)
RE_SECTION = re.compile(r'<section class="series-section" id="([^"]+)">(.*?)</section>', re.S)
RE_EMOJI_TAIL = re.compile(r'\s*[\U0001F000-\U0001FAFF\u2300-\u23FF☀-➿⬀-⯿️]+\s*$')

# ---------------------------------------------------------------- copy deck
SERIES = {
    # id: (chip label WITHOUT the "· N" suffix, EN description, TH description)
    "series-ai-core": (
        "AI-Core Systems",
        "A zero-to-hero engineering course from the author&#x27;s own paper — classify, design, contract, guard and prove a system whose core is a language model.",
        "คอร์สวิศวกรรมจากศูนย์ถึงมือโปร อิงเปเปอร์ของผู้เขียนเอง — จำแนก ออกแบบ ทำสัญญา วางการ์ด และพิสูจน์ระบบที่มีโมเดลภาษาเป็นแกน ตอนละ 7 ขั้นลงมือจริง"),
    "series-hermes-desktop": (
        "Hermes Desktop",
        "Install and run Nous Research&#x27;s Hermes Desktop on your own machine, screen by screen.",
        "ติดตั้งและใช้ Hermes Desktop บนเครื่องของเราเองทีละหน้าจอ — โมเดลบนเครื่อง โปรไฟล์ สภาตรวจคำตอบ และงานอัตโนมัติ"),
    "series-ai-transformation": (
        "AI Transformation",
        "Making AI an organizational core rather than a pilot — reframe, redesign, engineer, lead.",
        "ทำให้ AI เป็นแกนกลางขององค์กร ไม่ใช่โครงการนำร่อง — เปลี่ยนกรอบคิด ออกแบบใหม่ วิศวกรรม และนำการเปลี่ยนผ่าน"),
    "series-hermes": (
        "Hermes Agent",
        "Adopting Nous Research&#x27;s open-source agent harness in a real organization, from first install to production.",
        "คู่มือ Hermes Agent ฉบับลงมือจริง — ตั้งแต่ติดตั้ง ทีม agent ความจำ ความปลอดภัย จนถึง production"),
    "series-openclaw": (
        "OpenClaw",
        "Building AI systems that think, remember and act — a seven-part course plus standalone deep dives.",
        "สร้างระบบ AI ที่คิด จำ และลงมือทำเองได้ — คอร์ส 7 ตอน พร้อมบทความเดี่ยวเจาะลึก"),
    "series-devops": (
        "DevOps",
        "Modern DevOps from Git fundamentals to Kubernetes, CI/CD and production-ready infrastructure — in 24 steps.",
        "DevOps ยุคใหม่ตั้งแต่ Git พื้นฐานถึง Kubernetes, CI/CD และ infrastructure พร้อมใช้จริง — 24 ตอนตามลำดับ"),
    # "series-life" left this page on 2026-09-08: the nine Life essays are
    # catalogued on thoughts/index.html (hand-written; the series is complete).
}
NUM_WORD = {4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine"}
ICON_FIX = {"series-devops": "🚀"}   # chip said ⚙️, header says 🚀 — one glyph per series

HERO_LABEL = 'Anirach Mingkhwan · KMUTNB · <span lang="th">ไทย</span> ⇄ English'
HERO_TITLE = 'Tutorials'
HERO_SUB = ('{nseries} series on DevOps, AI agents, AI transformation and AI-core engineering — '
            'every post in Thai, with English one tap away. Essays on living well are in '
            '<a href="../thoughts/">Thoughts</a>.')
META_DESC = ('{total} bilingual Thai/English tutorials by Anirach Mingkhwan in {nseries} series — AI-Core '
             'Systems, Hermes Desktop, AI Transformation, Hermes Agent, OpenClaw and DevOps.')
PAGE_TITLE = 'Tutorials — Anirach Mingkhwan'


def read_label(mins):
    """80 -> '1 h 20 min', 60 -> '1 h', 45 -> '45 min'. check_site.py INV-02g
    parses exactly this shape back out of the tile."""
    h, m = divmod(mins, 60)
    if h and m:
        return "%d h %d min" % (h, m)
    return "%d h" % h if h else "%d min" % m

# ---------------------------------------------------------------- helpers
def read(p):
    return open(p, encoding="utf-8").read()

def strip_tags(s):
    return htmlmod.unescape(re.sub(r"<[^>]+>", "", s)).strip()

def split_title(raw):
    """'<span lang="th">EN — TH 🚚</span>' -> (EN, sep, TH) as escaped HTML fragments.
    The separator text is kept so the concatenated title stays byte-identical for
    gen_feed / INV-10; it renders display:none. ' = ' covers the Obsidian title."""
    inner = re.sub(r"</?span[^>]*>", "", raw).strip()
    inner = RE_EMOJI_TAIL.sub("", inner)
    for sep in (" — ", " = "):
        if sep in inner:
            en, th = inner.split(sep, 1)
            if re.search(r"[\u0E00-\u0E7F]", th) and not re.search(r"[\u0E00-\u0E7F]", en):
                return en.strip(), sep, th.strip()
    return inner, "", ""

def rewrap_excerpt(ex):
    """Six OpenClaw excerpts open on an English list before the em dash; move the
    lang="th" span to the Thai half so the English is not voiced in Thai. The
    concatenated text (what gen_feed emits) is unchanged."""
    m = re.match(r'^<span lang="th">(.*)</span>$', ex.strip(), re.S)
    if not m or ' — ' not in m.group(1):
        return ex
    head, tail = m.group(1).split(' — ', 1)
    thai = len(re.findall(r'[\u0E00-\u0E7F]', head))
    latin = len(re.findall(r'[A-Za-z]', head))
    if latin >= 8 and thai <= max(2, latin // 10) and re.search(r'[\u0E00-\u0E7F]', tail):
        return '%s — <span lang="th">%s</span>' % (head, tail)
    return ex

def ordinal_map(repo):
    """slug -> (n, group_key) from manifests, chip strips and the DevOps chain."""
    out = {}
    for name in ("hermes-desktop", "ai-transformation", "ai-core"):
        man = json.load(open(os.path.join(repo, "scripts", "series", name + ".json")))
        for p in man["posts"]:
            out[p["slug"]] = (p["n"], p.get("group"))
    for host in ("hermes-101", "morning-waking", "openclaw-101"):
        s = read(os.path.join(repo, "blog", host + ".html"))
        body = re.search(r'<div class="series-links">(.*?)</div>', s, re.S).group(1)
        n = 0
        for m in re.finditer(r'<(?:a href="/blog/([a-z0-9-]+)"|span class="current"[^>]*)>', body):
            n += 1
            slug = m.group(1) or host
            out[slug] = (n, None)
    return out

def devops_chain(repo):
    """Follow .post-nav 'Next' links from the chain head; independent of card order."""
    chain, cur = [], "git-branching"
    seen = set()
    while cur and cur not in seen:
        seen.add(cur); chain.append(cur)
        s = read(os.path.join(repo, "blog", cur + ".html"))
        m = re.search(r'<a href="([^"]+)" class="post-nav__link"[^>]*>\s*<div class="post-nav__dir">Next', s)
        nxt = m.group(1) if m else None
        cur = None if (not nxt or nxt == "./") else nxt[:-5]
    return chain

def parse_index(repo):
    s = read(os.path.join(repo, "blog", "index.html"))
    feature = re.search(r'<a href="([a-z0-9-]+\.html)" class="feature">(.*?)</a>', s, re.S)
    f_href, f_block = feature.group(1), feature.group(2)
    f_img = re.search(r'<img src="([^"]+)"[^>]*>', f_block).group(0)
    f_title = re.search(r'<h([23]) class="feature__title">(.*?)</h\1>', f_block, re.S).group(2)
    f_ex = re.search(r'<p class="feature__excerpt"[^>]*>(.*?)</p>', f_block, re.S).group(1)
    sections = []
    for sid, body in RE_SECTION.findall(s):
        icon = re.search(r'<span class="series-icon" aria-hidden="true">([^<]*)</span>', body).group(1)
        title = re.search(r'<h2 class="series-title">(.*?)</h2>', body).group(1)
        cards = []
        for href, block in RE_CARD.findall(body):
            cover = re.search(r'<img src="([^"]+)"', block).group(1)
            t = re.search(r'<h3 class="card__title">(.*?)</h3>', block, re.S).group(1)
            ex = re.search(r'<p class="card__excerpt">(.*?)</p>', block, re.S).group(1)
            tm = re.search(r'<time datetime="([^"]+)">([^<]*)</time>\s*·\s*(\d+) min', block)
            en, sep, th = split_title(t)
            cards.append(dict(href=href, slug=href[:-5], cover=cover, en=en, sep=sep, th=th,
                              excerpt=rewrap_excerpt(ex.strip()), date=tm.group(1),
                              date_text=tm.group(2), mins=int(tm.group(3))))
        sections.append(dict(id=sid, icon=ICON_FIX.get(sid, icon), title=title, cards=cards))
    # keep everything between </style> and </head> that is the social block (rewritten below)
    style = re.search(r'<style>(.*?)</style>', s, re.S).group(1)
    return dict(feature=dict(href=f_href, img=f_img, title=f_title, excerpt=f_ex),
                sections=sections, style=style, raw=s)

def block(style, start_pat, end_pat):
    """Extract a rule group, normalised to end with exactly one newline so that
    re-running this script on its own output is byte-stable."""
    a = style.index(start_pat)
    b = style.index(end_pat, a)
    return style[a:b].rstrip() + "\n"

# ---------------------------------------------------------------- CSS
CSS_HERO = r"""
    /* ── HERO ── compact: identity line, title, one sentence, two counted stats.
       The stats keep the exact <span class="blog-hero__stat"><strong>N</strong> Label>
       shape check_site.py RE_HERO_STAT rewrites with --fix; only the pill chrome
       is gone, so a number is stated once here, once per chip, once per section. */
    .blog-hero {
      padding: 6rem 2.5rem 1.6rem;
      background: linear-gradient(135deg, #eef3f3 0%, #dee7e6 50%, #e9e1c4 100%);
      text-align: center;
    }
    .blog-hero__label {
      font-size: 0.78rem; font-weight: 600; letter-spacing: 0.12em;
      color: var(--blue-dark); text-transform: uppercase; margin-bottom: 0.9rem;
    }
    .blog-hero__label [lang="th"] { text-transform: none; letter-spacing: 0.04em; }
    .blog-hero__title {
      font-size: clamp(2rem, 4vw, 2.8rem); font-weight: 900;
      color: var(--navy); line-height: 1.1; margin-bottom: 0.75rem;
    }
    .blog-hero__sub {
      font-size: 1.02rem; color: var(--slate-light); max-width: 600px;
      margin: 0 auto 1rem; line-height: 1.6;
    }
    .blog-hero__sub a { color: var(--blue-dark); font-weight: 700; }
    .blog-hero__sub a:hover { text-decoration: underline; }
    .blog-hero__stats { display: flex; justify-content: center; gap: 0.6rem; font-size: 0.85rem;
                        color: var(--slate-light); font-variant-numeric: tabular-nums; }
    .blog-hero__stat strong { color: var(--blue-dark); font-weight: 700; }
    .blog-hero__stat + .blog-hero__stat::before { content: "·"; margin-right: 0.6rem; opacity: 0.6; }

    /* ── SERIES BAR ── the .blog-jump strip, now the site's first sticky element.
       One row of short chips (no emoji — INV-02f reads chip text with [^<]* so an
       aria-hidden span is illegal, and a bare pictograph is announced by name).
       Opaque ground, no backdrop-filter: it is repainted on every scroll frame.
       scroll-padding-top / scroll-margin-top below are raised to clear it. */
    .blog-jump {
      position: sticky; top: 64px; z-index: 90;
      background: var(--bg); border-bottom: 1px solid rgba(17,48,75,0.08);
      display: flex; justify-content: center; gap: 0.5rem;
      padding: 0.6rem 2.5rem; flex-wrap: wrap;
    }
    .blog-jump a {
      display: inline-flex; align-items: center; min-height: 36px;
      font-size: 0.8rem; font-weight: 600; color: var(--blue-dark);
      background: var(--white); border: 1px solid var(--blue-light);   /* borders-only token: 3.2:1 edge */
      padding: 0.35rem 0.85rem; border-radius: 50px; white-space: nowrap;
      text-decoration: none; transition: background-color var(--transition), color var(--transition);
    }
    .blog-jump a:hover { background: var(--blue-dark); border-color: var(--blue-dark); color: #fff; }
    .blog-jump a[href="/feed.xml"] { color: var(--gold-dark); border-color: var(--gold-dark); }  /* --gold is 2.21:1 on cream — fails the 3:1 edge */
    .blog-jump a[href="/feed.xml"]:hover { background: var(--gold-dark); border-color: var(--gold-dark); color: #fff; }
    /* After a chip jump the destination is :target — light the chip that got you
       there. Pure enhancement: nothing depends on :has(). */
    body:has(#series-ai-core:target)          .blog-jump a[href="#series-ai-core"],
    body:has(#series-hermes-desktop:target)   .blog-jump a[href="#series-hermes-desktop"],
    body:has(#series-ai-transformation:target) .blog-jump a[href="#series-ai-transformation"],
    body:has(#series-hermes:target)           .blog-jump a[href="#series-hermes"],
    body:has(#series-openclaw:target)         .blog-jump a[href="#series-openclaw"],
    body:has(#series-devops:target)           .blog-jump a[href="#series-devops"] {
      background: var(--blue-dark); border-color: var(--blue-dark); color: #fff;
    }

    /* ── LIST ── */
    .blog-list { max-width: 1200px; margin: 0 auto; padding: 2rem 2.5rem 5rem; }
    .section-kicker {
      font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.12em;
      color: var(--gold-dark); margin-bottom: 0.75rem;
    }
    .section-kicker [lang="th"] { text-transform: none; letter-spacing: 0.02em; font-weight: 600; }

    /* ── SPOTLIGHT ── the one promoted post, and the page's only lifted object.
       class="feature", never "card" (three regexes count class="card"). */
    .spotlight { margin-bottom: 2.5rem; padding-bottom: 2.5rem; border-bottom: 1px solid #e8ecf1; }
    .feature {
      display: grid; grid-template-columns: minmax(0, 0.9fr) minmax(0, 1.1fr);
      background: var(--white); border: 1px solid #e8ecf1;
      border-radius: var(--radius-lg); overflow: hidden; text-decoration: none;
      box-shadow: 0 10px 30px rgba(17,48,75,0.07);              /* the one lifted object on the page */
      transition: box-shadow 0.25s ease, border-color 0.25s ease;
    }
    .feature:hover, .feature:focus-within { box-shadow: 0 16px 48px rgba(34,98,153,0.14); border-color: rgba(34,98,153,0.25); }
    .feature__media { overflow: hidden; background: #f1f5f9; }
    .feature__media img { width: 100%; height: 100%; object-fit: cover; display: block; }
    .feature__body { padding: 1.5rem 1.75rem; display: flex; flex-direction: column; justify-content: center; }
    .feature__eyebrow {
      font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em;
      color: var(--gold-dark); margin-bottom: 0.6rem; font-variant-numeric: tabular-nums;
    }
    .feature__eyebrow [lang="th"] { text-transform: none; letter-spacing: 0.02em; }
    .feature__title { font-size: 1.35rem; font-weight: 800; color: var(--navy); line-height: 1.3; margin-bottom: 0.6rem; }
    .feature__title .card__sep { display: none; }
    .feature__title .card__th { display: block; font-size: 0.85em; font-weight: 600; color: var(--slate); line-height: 1.55; margin-top: 0.15rem; }
    .feature__excerpt { font-size: 0.9rem; color: var(--slate-light); line-height: 1.7; margin-bottom: 1rem;
                        display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }
    .feature__read { font-size: 0.85rem; font-weight: 700; color: var(--blue); }

    /* ── CATALOG ── the six series side by side, each with a description and a
       summed reading time, so a reader picks a series before scrolling into
       80-odd rows. Tiles are <a>s with their own class — never class="card" —
       and check_site.py INV-02g keeps their counts and reading times honest. */
    .catalog { margin-bottom: 2.5rem; padding-bottom: 2.5rem; border-bottom: 1px solid #e8ecf1; }
    .catalog__grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 0.9rem; }
    .series-tile {
      display: grid; grid-template-columns: 40px minmax(0, 1fr); gap: 0.85rem; align-items: start;
      background: var(--white); border: 1px solid #e8ecf1; border-radius: var(--radius);
      padding: 0.95rem 1rem; transition: border-color var(--transition), box-shadow var(--transition);
    }
    .series-tile:hover, .series-tile:focus-within { border-color: rgba(34,98,153,0.35); box-shadow: 0 8px 24px rgba(34,98,153,0.08); }
    .series-tile:hover .series-tile__name { color: var(--blue); }
    .series-tile__icon { font-size: 1.25rem; width: 40px; height: 40px; display: flex; align-items: center;
                         justify-content: center; background: rgba(34,98,153,0.08); border-radius: 10px; }
    .series-tile__body { display: block; min-width: 0; }
    .series-tile__name { display: block; font-size: 1rem; font-weight: 800; color: var(--navy); line-height: 1.3; }
    .series-tile__meta { display: block; font-size: 0.74rem; font-weight: 600; color: var(--gold-dark);
                         margin: 0.2rem 0 0.35rem; font-variant-numeric: tabular-nums; }
    .series-tile__desc { font-size: 0.82rem; color: var(--slate-light); line-height: 1.55;
                         display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }

    /* ── SERIES SECTIONS ── */
    .series-section { margin-bottom: 2.5rem; }
    .series-section + .series-section { padding-top: 2rem; border-top: 1px solid #e8ecf1; }
    .series-header { display: flex; align-items: center; justify-content: space-between;
                     gap: 0.75rem; flex-wrap: wrap; margin-bottom: 0.5rem; }
    .series-header__left { display: flex; align-items: center; gap: 0.75rem; }
    .series-icon { font-size: 1.35rem; width: 40px; height: 40px; display: flex;
                   align-items: center; justify-content: center;
                   background: rgba(34,98,153,0.08); border-radius: 10px; }
    .series-title { font-size: 1.35rem; font-weight: 800; color: var(--navy); letter-spacing: -0.01em; }
    .series-count { font-size: 0.8rem; font-weight: 600; color: var(--blue-dark);
                    background: rgba(34,98,153,0.08); padding: 0.35rem 0.9rem; border-radius: 50px;
                    white-space: nowrap; }
    .series-description { font-size: 0.92rem; color: var(--slate-light); line-height: 1.6;
                          max-width: 860px; margin-bottom: 1rem; }
    /* A :target section gets a quiet marker so a chip jump visibly "lands". */
    .series-section:target .series-title { text-decoration: underline; text-decoration-color: var(--gold-dark);
                                           text-decoration-thickness: 3px; text-underline-offset: 6px; }

    /* ── ROW CARDS ── the phone row-card of 2026-08-26, promoted to every width.
       Two columns of numbered rows: ordinal · 72px square thumb (covers are
       800x800, so the crop is zero) · EN title / TH title / one-line excerpt /
       date + read time. No byline (one author), no "Read →" (the row IS the
       link), no tag row (the section header already names the topic).
       The anchor keeps the exact href-then-class shape every regex parser reads —
       every variant lives on the container, never on the card's class list. */
    .blog-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(460px, 1fr)); gap: 0.6rem 1.25rem; }
    .blog-grid__label {
      grid-column: 1 / -1; margin: 0.6rem 0 0; padding-left: 0.25rem;
      font-size: 0.7rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: var(--slate-light);
    }
    .blog-grid__label [lang="th"] { text-transform: none; letter-spacing: 0.02em; }
    .card {
      display: grid; grid-template-columns: 2rem 72px minmax(0, 1fr); gap: 0 0.85rem; align-items: start;
      background: var(--white); border: 1px solid #e8ecf1; border-radius: var(--radius);
      padding: 0.7rem 0.9rem 0.7rem 0.65rem;
      transition: border-color var(--transition), box-shadow var(--transition);
    }
    .card:visited .card__en { color: var(--slate-light); }   /* read = quieter title, no JS;
                                                declared BEFORE the interactive states so
                                                hover/focus still light a visited title */
    .card:hover { border-color: rgba(34,98,153,0.35); box-shadow: 0 8px 24px rgba(34,98,153,0.08); }
    .card:hover .card__en, .card:focus-within .card__en { color: var(--blue); }
    .card__num {
      font-size: 0.78rem; font-weight: 800; color: var(--gold-dark); text-align: right;
      padding-top: 0.28rem; font-variant-numeric: tabular-nums; letter-spacing: 0.02em;
    }
    .card__image { width: 72px; aspect-ratio: 1 / 1; overflow: hidden; border-radius: var(--radius-sm); background: #f1f5f9; }
    .card__image img { width: 100%; height: 100%; object-fit: cover; }
    .card__body { min-width: 0; }
    .card__title { font-size: 0.98rem; line-height: 1.35; margin: 0 0 0.15rem; font-weight: 700; color: var(--navy); }
    .card__sep { display: none; }
    .card__th { display: block; font-size: 0.86rem; font-weight: 500; color: var(--slate); line-height: 1.6; }
    .card__excerpt {
      font-size: 0.8rem; color: var(--slate-light); line-height: 1.6; margin: 0.1rem 0 0;
      display: -webkit-box; -webkit-line-clamp: 1; -webkit-box-orient: vertical; overflow: hidden;
      padding-bottom: 0.08em;                       /* keeps a clamped Thai line's lower vowels */
    }
    .card__meta { font-size: 0.72rem; color: var(--slate-light); margin-top: 0.3rem; font-variant-numeric: tabular-nums; }

    /* ── FOOTER ── */
    .footer { background: var(--navy); padding: 2rem 0; text-align: center; }
    .footer a { color: var(--gold); font-weight: 600; font-size: 0.9rem;
                display: inline-block; padding: 0.4rem 0.5rem; }
    .footer a + a { margin-left: 1.5rem; }
    .footer span { color: var(--gray); font-size: 0.8rem; display: block; margin-top: 0.4rem; }
"""

CSS_RESPONSIVE = r"""
    /* ── ≤1024px: one centred chip row no longer fits (measured wrap at ~990px),
       so the bar becomes a left-aligned scroller. 1024 is the house wide
       breakpoint. The scrollbar is hidden; the right-edge fade + end padding
       are the overflow affordance, and proximity snap lands whole chips. */
    @media (max-width: 1024px) {
      .blog-jump { justify-content: flex-start; flex-wrap: nowrap; overflow-x: auto;
                   scrollbar-width: none; padding-inline-end: 2.25rem;
                   scroll-snap-type: x proximity;
                   -webkit-mask-image: linear-gradient(to right, #000 calc(100% - 28px), transparent);
                   mask-image: linear-gradient(to right, #000 calc(100% - 28px), transparent); }
      .blog-jump::-webkit-scrollbar { display: none; }
      .blog-jump a { scroll-snap-align: start; }
      .catalog__grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    }
    @media (max-width: 768px) {
      /* In-page jumps use instant scroll here: a smooth 13,000px scroll drags
         every row through the lazy-load margin and pulls ~3 MB of covers on 4G. */
      html { scroll-behavior: auto; }
      .blog-hero { padding: 5rem 1.25rem 1.4rem; }
      .blog-hero__sub { font-size: 0.95rem; }
      .blog-jump { padding: 0.5rem 2.25rem 0.5rem 1.25rem; gap: 0.45rem; }
      .blog-jump a { min-height: 44px; padding: 0.5rem 0.9rem; }
      .blog-list { padding: 1.5rem 1.25rem 4rem; }
      .spotlight { margin-bottom: 2rem; }
      .feature { grid-template-columns: 1fr; }
      .feature__media { aspect-ratio: 1200 / 630; }
      .feature__body { padding: 0.9rem 1.1rem 1.1rem; }
      /* On a phone the spotlight is image + eyebrow + title; the first row of
         the series it opens is one flick away and carries the excerpt. */
      .feature__excerpt, .feature__read { display: none; }
      .feature__title { font-size: 1.15rem; }
      .series-section { margin-bottom: 2rem; }
      .series-title { font-size: 1.15rem; }
      .series-description { font-size: 0.88rem; margin-bottom: 1rem; }
      .blog-grid { grid-template-columns: 1fr; gap: 0.5rem; }
      .card { grid-template-columns: 1.7rem 64px minmax(0, 1fr); gap: 0 0.7rem; padding: 0.6rem 0.75rem 0.6rem 0.55rem; }
      .card__image { width: 64px; }
      .card__title { font-size: 0.95rem; }
      .card__th { font-size: 0.84rem; }
      .card__excerpt { font-size: 0.84rem; }
    }
    @media (max-width: 600px) {
      .blog-hero__title { font-size: 1.9rem; }
      .blog-hero__label { font-size: 0.7rem; letter-spacing: 0.08em; }
      /* The truncated one-line excerpt mostly restates the Thai title at this
         width; the row keeps EN title / TH title / date · read time. */
      .card__excerpt { display: none; }
      /* The count is already on the sticky chip ("DevOps · 24") and on the last
         row's ordinal; hiding the pill stops it wrapping under every title.
         The span stays in the markup — RE_SERIES_COUNT reads the source. */
      .series-count { display: none; }
      .catalog__grid { grid-template-columns: 1fr; gap: 0.6rem; }
      .series-tile { padding: 0.75rem 0.85rem; }
      .series-tile__desc { display: none; }     /* the section header below carries it */
    }
"""

# ---------------------------------------------------------------- markup
def card_html(c, num, indent="      "):
    en = c["en"]; th = c["th"]
    if th:
        title = ('<span class="card__en">%s</span><span class="card__sep">%s</span>'
                 '<span class="card__th" lang="th">%s</span>') % (en, c.get("sep") or " — ", th)
    else:
        title = '<span class="card__en">%s</span>' % en
    if num:
        num_span = '<span class="card__num">%02d</span>' % num
    else:
        num_span = '<span class="card__num" aria-hidden="true"></span>'
    return "\n".join([
        indent + '<!-- Card: %s -->' % strip_tags(en),
        indent + '<a href="%s" class="card">' % c["href"],
        indent + '  %s' % num_span,
        indent + '  <div class="card__image">',
        indent + '    <img src="%s" alt="" width="800" height="800" loading="lazy" decoding="async">' % c["cover"],
        indent + '  </div>',
        indent + '  <div class="card__body">',
        indent + '    <h3 class="card__title">%s</h3>' % title,
        indent + '    <p class="card__excerpt">%s</p>' % c["excerpt"],
        indent + '    <p class="card__meta"><time datetime="%s">%s</time> · %d min read</p>' % (c["date"], c["date_text"], c["mins"]),
        indent + '  </div>',
        indent + '</a>',
    ])

def order_cards(sec, ords, chain, order):
    """Return [(card, ordinal, group_key)] in the chosen reading order."""
    cards = sec["cards"]
    if sec["id"] == "series-devops":
        pos = {slug: i + 1 for i, slug in enumerate(chain)}
        rows = [(c, pos.get(c["slug"]), None) for c in cards]
    else:
        rows = [(c,) + (ords.get(c["slug"]) or (None, None)) for c in cards]
    if order == "reading":
        numbered = sorted([r for r in rows if r[1]], key=lambda r: r[1])
        unnumbered = [r for r in rows if not r[1]]
        return numbered, unnumbered
    return [r for r in rows if r[1]], [r for r in rows if not r[1]]

def section_html(sec, ords, chain, order, groups):
    chip_label, desc_en, desc_th = SERIES[sec["id"]]
    numbered, unnumbered = order_cards(sec, ords, chain, order)
    n = len(sec["cards"])
    out = [
        '    <!-- %s -->' % strip_tags(sec["title"]),
        '    <section class="series-section" id="%s">' % sec["id"],
        '      <div class="series-header">',
        '        <div class="series-header__left">',
        '          <span class="series-icon" aria-hidden="true">%s</span>' % sec["icon"],
        '          <h2 class="series-title">%s</h2>' % sec["title"],
        '        </div>',
        '        <span class="series-count">%d articles</span>' % n,
        '      </div>',
        '      <p class="series-description">%s <span lang="th">%s</span></p>' % (desc_en, desc_th),
        '      <div class="blog-grid">',
    ]
    if sec["id"] == "series-ai-transformation":
        for g in groups:
            en_l, th_l = g["label"].split(" · ", 1)
            out.append('      <p class="blog-grid__label">%s · <span lang="th">%s</span></p>' % (en_l, th_l))
            for c, num, gk in numbered:
                if gk == g["key"]:
                    out.append(card_html(c, num))
    else:
        for c, num, _ in numbered:
            out.append(card_html(c, num))
    if unnumbered:
        if numbered:
            out.append('      <p class="blog-grid__label">Standalone posts · <span lang="th">บทความเดี่ยว</span></p>')
        for c, num, _ in unnumbered:
            out.append(card_html(c, None))
    out += ['      </div>', '    </section>', '']
    return "\n".join(out)

def build(repo, order):
    idx = parse_index(repo)
    ords = ordinal_map(repo)
    chain = devops_chain(repo)
    groups = json.load(open(os.path.join(repo, "scripts", "series", "ai-transformation.json")))["groups"]
    style = idx["style"]
    raw = idx["raw"]

    # ---- verbatim house blocks
    root_block = block(style, "    :root {", "    html { scroll-behavior")
    nav_block = block(style, "    /* ── NAV ── */", "    /* ── HERO ──")   # matches both the live "*/" and this script's own longer HERO comment
    nav_block = nav_block.replace(
        "    .nav__toggle { position: absolute; opacity: 0; width: 1px; height: 1px; }",
        "    /* Hidden entirely at desktop — the burger label is display:none there too,\n"
        "       so a focusable-but-invisible checkbox would be a purposeless tab stop\n"
        "       between the logo and the first nav link. Restored, visually-hidden but\n"
        "       focusable, only inside the max-width:950px block below. */\n"
        "    .nav__toggle { display: none; }")
    try:
        takeover = block(style, "    /* ── RESPONSIVE ── */", "    /* ── PHONE: row cards ──")
    except ValueError:   # re-run on our own output: the PHONE block is gone
        takeover = block(style, "    /* ── RESPONSIVE ── */", "    /* ── ≤1024px:")
    tail = style[style.index("    :focus-visible {"):].rstrip() + "\n"
    tail = tail.replace("html { scroll-padding-top: 5rem; }", "html { scroll-padding-top: 8.5rem; }   /* fixed nav (64) + sticky series bar (56) + 16 */")
    tail = tail.replace("[id] { scroll-margin-top: 5rem; }",
                        "/* no [id] scroll-margin-top here: it ADDS to scroll-padding-top, and the pair landed every chip jump 272px down */")
    tail = re.sub(r"    /\* Hover/focus parity:.*?\.card:focus-within \.card__read \{[^\n]*\n",
                  "    /* Hover/focus parity: keyboard focus gets the same edge, shadow and title\n"
                  "       colour a mouse hover gets. No lift and no image zoom on a dense row. */\n"
                  "    .card:focus-within { border-color: rgba(34,98,153,0.35); box-shadow: 0 8px 24px rgba(34,98,153,0.08); }\n"
                  "    .blog-jump a:focus-visible, .feature:focus-visible { outline: 2px solid var(--focus); outline-offset: 3px; }\n",
                  tail, flags=re.S)
    tail = tail.replace("        transition-duration: .01ms !important; scroll-behavior: auto !important;\n      }\n    }",
                        "        transition-duration: .01ms !important; scroll-behavior: auto !important;\n      }\n"
                        "      .feature:hover, .feature:focus-within, .card:hover, .card:focus-within { transform: none; }\n    }")

    # ---- head
    nav_markup = re.search(r'  <!-- NAV -->\n(.*?)  </nav>\n', raw, re.S).group(1) + "  </nav>\n"
    nav_markup = nav_markup.replace('<nav class="nav">', '<nav class="nav" aria-label="Site">')
    nav_markup = nav_markup.replace('<a href="../blog/" class="active">Tutorials</a>', '<a href="../blog/" class="active" aria-current="page">Tutorials</a>')
    social = re.search(r'  <!-- social -->.*?<!-- /social -->\n', raw, re.S).group(0)
    total = sum(len(s["cards"]) for s in idx["sections"])
    nseries = NUM_WORD.get(len(idx["sections"]), str(len(idx["sections"])))
    meta_desc = META_DESC.format(total=total, nseries=nseries)
    hero_sub = HERO_SUB.format(nseries=nseries.capitalize())
    social = re.sub(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="%s">' % PAGE_TITLE, social)
    social = re.sub(r'<meta property="og:description" content="[^"]*">', '<meta property="og:description" content="%s">' % meta_desc, social)
    social = re.sub(r'<meta property="og:image:alt" content="[^"]*">', '<meta property="og:image:alt" content="%s">' % PAGE_TITLE, social)
    jsonld = ('  <script type="application/ld+json">\n'
              '  {"@context":"https://schema.org","@type":"Blog","name":"Anirach Mingkhwan — Tutorials",'
              '"url":"https://anirach.com/blog/","inLanguage":["th","en"],'
              '"author":{"@type":"Person","@id":"https://anirach.com/#person","name":"Anirach Mingkhwan"}}\n'
              '  </script>\n')
    fonts = re.search(r'  <link rel="preconnect".*?rel="stylesheet">\n', raw, re.S).group(0)

    # ---- body
    f = idx["feature"]
    fen, fsep, fth = split_title(f["title"])
    f_slug = f["href"][:-5]
    f_ord = ords.get(f_slug, (None, None))[0]
    f_sec = next(s for s in idx["sections"] if any(c["slug"] == f_slug for c in s["cards"]))
    f_card = next(c for c in f_sec["cards"] if c["slug"] == f_slug)
    eyebrow = 'New series · <span lang="th">ซีรีส์ใหม่</span> · %s · %s' % (f_card["date_text"], strip_tags(f_sec["title"]))
    if f_ord:
        eyebrow += ' · Post %d of %d' % (f_ord, len(f_sec["cards"]))
    feature = "\n".join([
        '    <!-- SPOTLIGHT: the promoted post. class="feature", NOT "card" — three',
        '         separate regexes count class="card" and an 84th match would inflate',
        '         the counters and duplicate a feed item. -->',
        '    <section class="spotlight" aria-labelledby="spotlight-title">',
        '      <h2 class="section-kicker" id="spotlight-title">Start here · <span lang="th">เริ่มอ่านที่นี่</span></h2>',
        '      <a href="%s" class="feature">' % f["href"],
        '        <div class="feature__media">',
        '          %s' % f["img"],
        '        </div>',
        '        <div class="feature__body">',
        '          <p class="feature__eyebrow">%s</p>' % eyebrow,
        '          <h3 class="feature__title"><span class="card__en">%s</span><span class="card__sep">%s</span><span class="card__th" lang="th">%s</span></h3>' % (fen, fsep or ' — ', fth),
        '          <p class="feature__excerpt" lang="th">%s</p>' % f["excerpt"],
        '          <span class="feature__read">Read <span lang="th">อ่านต่อ</span> &rarr;</span>',
        '        </div>',
        '      </a>',
        '    </section>',
        '',
    ])
    chips = "\n".join('      <a href="#%s">%s · %d</a>' % (s["id"], SERIES[s["id"]][0], len(s["cards"])) for s in idx["sections"])
    tiles = []
    for s in idx["sections"]:
        mins = sum(c["mins"] for c in s["cards"])
        tiles.append("\n".join([
            '        <a href="#%s" class="series-tile">' % s["id"],
            '          <span class="series-tile__icon" aria-hidden="true">%s</span>' % s["icon"],
            '          <span class="series-tile__body">',
            '            <span class="series-tile__name">%s</span>' % s["title"],
            '            <span class="series-tile__meta">%d articles · ≈ %s</span>' % (len(s["cards"]), read_label(mins)),
            '            <span class="series-tile__desc">%s</span>' % SERIES[s["id"]][1],
            '          </span>',
            '        </a>',
        ]))
    catalog = "\n".join([
        '    <!-- CATALOG: one tile per series. class="series-tile", never "card";',
        '         INV-02g checks each tile\'s count and reading time against its section. -->',
        '    <section class="catalog" aria-labelledby="catalog-title">',
        '      <h2 class="section-kicker" id="catalog-title">Choose a series · <span lang="th">เลือกซีรีส์</span></h2>',
        '      <div class="catalog__grid">',
        "\n".join(tiles),
        '      </div>',
        '    </section>',
        '',
    ])
    sections = "\n".join(section_html(s, ords, chain, order, groups) for s in idx["sections"])

    page = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{PAGE_TITLE}</title>
  <meta name="description" content="{meta_desc}">
{fonts}  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
{root_block}    html {{ scroll-behavior: smooth; }}
    body {{
      font-family: var(--font); font-size: 16px; line-height: 1.7;
      color: var(--slate); background: var(--bg); -webkit-font-smoothing: antialiased;
    }}
    a {{ text-decoration: none; color: inherit; }}
    img {{ max-width: 100%; display: block; }}

{nav_block}{CSS_HERO}
{takeover}{CSS_RESPONSIVE}
{tail}  </style>
{social}{jsonld}</head>
<body>
<a href="#main" class="skip-link">Skip to content</a>

  <!-- NAV -->
{nav_markup}
  <!-- HERO -->
  <header class="blog-hero">
    <p class="blog-hero__label">{HERO_LABEL}</p>
    <h1 class="blog-hero__title">{HERO_TITLE}</h1>
    <p class="blog-hero__sub">{hero_sub}</p>
    <p class="blog-hero__stats">
      <span class="blog-hero__stat"><strong>{len(idx["sections"])}</strong> Series</span>
      <span class="blog-hero__stat"><strong>{total}</strong> Articles</span>
    </p>
  </header>

  <!-- SERIES BAR — sticky, between the hero and <main> so the skip link lands
       on content rather than on a second navigation. One chip per section;
       INV-02f checks each chip's "· N" against its section's card count. The
       RSS link is not a section chip and is ignored by that check. The site
       <nav> above must stay the FIRST nav in the document (INV-23). -->
  <nav class="blog-jump" id="series-index" aria-label="Jump to a series">
{chips}
      <a href="/feed.xml">RSS</a>
    </nav>

  <main id="main">
    <div class="blog-list">

{feature}
{catalog}
{sections}    </div>
  </main>

  <!-- FOOTER -->
  <footer class="footer">
    <a href="../index.html">← Back to Home</a>
    <a href="#main">↑ Top</a>
    <span>© 2026 Anirach Mingkhwan — Associate Professor, KMUTNB</span>
  </footer>

</body>
</html>
'''
    return page

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--order", choices=["reading", "newest"], default="reading")
    a = ap.parse_args()
    html_out = build(a.repo, a.order)
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    open(a.out, "w", encoding="utf-8").write(html_out)
    n_cards = len(RE_CARD.findall(html_out))
    print("wrote", a.out, len(html_out), "bytes,", n_cards, "cards")
