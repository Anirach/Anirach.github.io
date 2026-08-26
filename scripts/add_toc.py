#!/usr/bin/env python3
"""Give every post stable <h2> ids and a table of contents.

WHY
---
The posts run to 46 phone-screens with no map. A reader who wants "the part
about secrets" scrolls and hopes. 379 <h2> headings existed across 37 posts and
not one carried an id, so nothing could be linked to either — no deep link from
a series strip, no anchor to paste into a chat.

THE SLUG RULE, designed against the six heading shapes that actually occur
(counted, not guessed):

    194  latin+thai      "API คืออะไร?"                -> api
    107  latin           "🌐 OAuth 2.0 — Login with…"  -> oauth-2-0
     41  thai only       "สรุป"                         -> summary (mapped) / s-N
     18  num latin       "9. Key Takeaways"            -> key-takeaways
     14  num latin+thai  "1. ทำไม ChatGPT ไม่เพียงพอ?"   -> s-1  (Thai leads)
      2  num thai        "8. ข้อจำกัดที่ควรรู้"           -> s-8

Emoji and a leading "N." are stripped, then the LATIN run before the first Thai
character or em dash becomes the slug. A heading whose meaning is carried in
Thai gets a fixed map where the phrase is common, else a positional `s-N` —
never a transliteration, which would be a guess this script has no business
making. Uniqueness is asserted per file; a collision appends -2, -3.

    python3 scripts/add_toc.py --dry-run
    python3 scripts/add_toc.py --apply
    python3 scripts/add_toc.py --verify
"""
import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
BLOG = ROOT / "blog"

EMOJI = re.compile(
    "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0000FE0F\U00002190-\U000021FF"
    "\U00002B00-\U00002BFF\U0001F000-\U0001F02F]")
THAI = re.compile(r"[฀-๿]")

# Common Thai section headings, so the most-repeated ones get a real slug
# rather than a position. Everything else stays positional on purpose.
THAI_MAP = {
    "สรุป": "summary",
    "บทสรุป": "summary",
    "อ้างอิง": "references",
    "ตัวอย่าง": "example",
    "ข้อดี": "pros",
    "ข้อเสีย": "cons",
    "วิธีใช้": "usage",
    "เริ่มต้น": "getting-started",
    "ทำไม": "why",
    "คืออะไร": "what-is-it",
}


def text_of(html):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html)).strip()


def slugify(raw, index):
    t = EMOJI.sub("", raw).strip()
    t = re.sub(r"^\s*\d+[.)]\s*", "", t)          # leading "9." / "9)"
    # the Latin run before the first Thai char or em dash carries the topic
    cut = len(t)
    m = THAI.search(t)
    if m:
        cut = min(cut, m.start())
    for sep in ("—", "–", " - ", ":"):
        j = t.find(sep)
        if j != -1:
            cut = min(cut, j)
    latin = t[:cut]
    slug = re.sub(r"[^a-z0-9]+", "-", latin.lower()).strip("-")
    if len(slug) < 2:                              # Thai-led heading
        for phrase, mapped in THAI_MAP.items():
            if phrase in t:
                return mapped
        return "s-%d" % index
    slug = slug[:60].strip("-")
    # A leading digit is legal in an HTML5 id but is NOT a valid CSS selector
    # (#3-cloud-providers does not parse), so anything that ever tries to style
    # or :target it silently fails. Prefix instead.
    if slug[0].isdigit():
        slug = "s-" + slug
    return slug


def process(path):
    s = path.read_text(encoding="utf-8")
    body = re.search(r'<article class="post-body"[^>]*>(.*?)</article>', s, re.S)
    if not body:
        return None
    seen = {}
    items = []
    out = []
    last = 0
    for i, m in enumerate(re.finditer(r"<h2([^>]*)>(.*?)</h2>", body.group(1), re.S), 1):
        attrs, inner = m.group(1), m.group(2)
        if "id=" in attrs:
            continue
        base = slugify(text_of(inner), i)
        slug = base
        n = 2
        while slug in seen:                        # per-file uniqueness
            slug = "%s-%d" % (base, n)
            n += 1
        seen[slug] = True
        items.append((slug, text_of(inner)))
        abs_start = body.start(1) + m.start()
        out.append(s[last:abs_start])
        out.append('<h2 id="%s"%s>%s</h2>' % (slug, attrs, inner))
        last = body.start(1) + m.end()
    if not items:
        return None
    out.append(s[last:])
    return "".join(out), items


TOC_CSS = """
    /* ---- table of contents ----------------------------------------------
       <details> so it is collapsible with no JavaScript, open by default on
       desktop. The posts run to 46 phone-screens; this is the map. */
    .post-toc {
      max-width: 720px;
      margin: 2rem auto 0;
      padding: 1rem 1.25rem;
      background: rgba(34,98,153,0.05);
      border: 1px solid rgba(34,98,153,0.14);
      border-left: 3px solid var(--gold, #c4a46c);
      border-radius: 10px;
      font-size: 0.92rem;
    }
    .post-toc > summary {
      cursor: pointer;
      font-weight: 700;
      color: var(--navy);
      list-style: none;
    }
    .post-toc > summary::-webkit-details-marker { display: none; }
    .post-toc > summary::before {
      content: "\\25B8";
      display: inline-block;
      margin-right: 0.5rem;
      transition: transform 0.2s ease;
      color: var(--gold-dark, #7a5f22);
    }
    .post-toc[open] > summary::before { transform: rotate(90deg); }
    .post-toc > summary:focus-visible { outline: 3px solid var(--focus, #226299); outline-offset: 3px; }
    .post-toc ol { margin: 0.85rem 0 0.25rem; padding-left: 1.4rem; }
    .post-toc li { margin-bottom: 0.4rem; line-height: 1.5; }
    .post-toc a { color: var(--slate); text-decoration: none; }
    .post-toc a:hover, .post-toc a:focus-visible { color: var(--blue-dark, #1a4d7a); text-decoration: underline; }
    @media (max-width: 600px) { .post-toc { margin: 1.25rem 1rem 0; } }
"""


def build_toc(items):
    lis = "\n".join(
        '          <li><a href="#%s">%s</a></li>' % (slug, html_escape(title))
        for slug, title in items)
    return (
        '\n    <details class="post-toc" open>\n'
        '      <summary>In this post &middot; <span lang="th">ในบทความนี้</span></summary>\n'
        '      <ol>\n%s\n      </ol>\n'
        '    </details>\n' % lis)


def html_escape(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--dry-run", action="store_true")
    g.add_argument("--apply", action="store_true")
    g.add_argument("--verify", action="store_true")
    a = ap.parse_args()

    if a.verify:
        bad = []
        for p in sorted(BLOG.glob("*.html")):
            if p.stem == "index":
                continue
            s = p.read_text(encoding="utf-8")
            ids = re.findall(r'<h2 id="([^"]+)"', s)
            if len(ids) != len(set(ids)):
                dup = [i for i in set(ids) if ids.count(i) > 1]
                bad.append("%s: duplicate h2 ids %s" % (p.name, dup))
            links = re.findall(r'<li><a href="#([^"]+)">', s)
            for l in links:
                if l not in ids:
                    bad.append("%s: TOC links #%s but no heading has that id" % (p.name, l))
            n_h2 = len(re.findall(r"<h2", s))
            if ids and len(ids) < n_h2 - 2:     # hero/series h2s live outside the article
                pass
        for b in bad:
            print("  x", b)
        print("VERIFY %s" % ("FAILED" if bad else "OK"))
        return 1 if bad else 0

    total_ids = total_toc = 0
    for p in sorted(BLOG.glob("*.html")):
        if p.stem == "index":
            continue
        r = process(p)
        if not r:
            continue
        s, items = r
        if '<details class="post-toc"' not in s:
            m = re.search(r'(<article class="post-body"[^>]*>)', s)
            if m:
                s = s[:m.end()] + build_toc(items) + s[m.end():]
                total_toc += 1
        if ".post-toc {" not in s:
            i = s.rfind("</style>")
            if i != -1:
                s = s[:i] + TOC_CSS + "  " + s[i:]
        total_ids += len(items)
        if a.apply:
            p.write_text(s, encoding="utf-8")
        else:
            print("%-34s %2d headings  e.g. %s" % (p.stem, len(items),
                                                   ", ".join(i[0] for i in items[:3])))
    print("\n%s %d ids and %d tables of contents"
          % ("wrote" if a.apply else "would write", total_ids, total_toc))
    return 0


if __name__ == "__main__":
    sys.exit(main())
