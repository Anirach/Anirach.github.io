#!/usr/bin/env python3
"""Gate for news updates on anirach.com. Run from anywhere; resolves the repo itself.

Three things nothing else in this repo checks:

1. SYNC — index.html's "Latest updates" strip must list the 3 newest items from
   news/index.html, in order. This shipped wrong once: the homepage showed
   Jul 2026 / Dec 2025 / Nov 2024 while the news page's third-newest was Oct 2025,
   so an entire update was invisible from the front page.

2. PROVENANCE — every news item must carry an HTML comment naming the source it was
   verified against. This is the anti-fabrication gate. A structural checker cannot
   tell a true item from an invented one, so instead it refuses to let an item exist
   without a stated source. Omitting a source now fails the build; fabricating one
   requires writing a deliberate falsehood into the file, which is auditable.

3. COUNTERS — four hand-maintained counters that nothing else verifies: news/index.html's
   "N updates" (the .series-count label over the timeline), publications/index.html's
   "N chapters" (the .series-count label over the Chapters section), and books/index.html's
   "N novel" and "N complete" (the .series-count labels over the Published and
   Manuscripts sections). All four drift silently whenever an item is added or
   removed without also touching the label. This recomputes each from the actual
   item count and fails if any of them disagrees.

Exit 0 = all four pass.  1 = a real problem.  2 = the checker itself could not run
(missing file, or the markup changed and its patterns no longer match — treat exit 2
as "the checker is broken", never as "the site is fine").
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

STRIP_DATE = re.compile(r'<span class="latest__date">([^<]+)</span>')
NEWS_DATE = re.compile(r'card__tag card__tag--date">([^<]+)<')
# An optional provenance comment immediately preceding each news <article>.
#
# The article tag is anchored to the start of a line (^\s*) on purpose. Without that
# anchor the pattern also matches the literal string "<article class="card card--row">"
# written *inside* the maintenance comment at the top of the timeline, inventing a
# phantom item with no source and failing the run. Documentation that quotes markup is
# normal; a scanner that cannot tell quoted markup from real markup is the bug.
NEWS_ITEM = re.compile(
    r'(?:<!--\s*source:\s*(\S+)\s*\|\s*verified\s*([0-9]{4}-[0-9]{2}-[0-9]{2})\s*-->\s*)?'
    r'^[ \t]*<article class="card card--row">(.*?)</article>',
    re.S | re.M,
)
# The ^[ \t]* anchors above and below only guard INLINE quoted markup — markup
# quoted inside a comment but sitting on its own indented line still starts a
# line and would be counted. So every body is stripped of comments before any
# findall; the anchors stay as defense in depth. strip_comments can keep the
# provenance comments, which NEWS_ITEM must still see.
COMMENT = re.compile(r'<!--.*?-->', re.S)
PROVENANCE_COMMENT = re.compile(r'<!--\s*source:')


def strip_comments(html: str, keep_provenance: bool = False) -> str:
    if keep_provenance:
        return COMMENT.sub(
            lambda m: m.group(0) if PROVENANCE_COMMENT.match(m.group(0)) else "", html)
    return COMMENT.sub("", html)


def fail(msg: str) -> None:
    print(f"  ✗ {msg}")


def main() -> int:
    try:
        home = (ROOT / "index.html").read_text(encoding="utf-8")
        news = (ROOT / "news" / "index.html").read_text(encoding="utf-8")
    except OSError as exc:
        print(f"cannot read site files: {exc}", file=sys.stderr)
        return 2

    # Comments out of the way first: quoted markup inside them must never reach
    # a findall. The provenance comments are the one kind NEWS_ITEM parses.
    news = strip_comments(news, keep_provenance=True)

    strip = STRIP_DATE.findall(home)
    dates = NEWS_DATE.findall(news)

    if not strip or not dates:
        print("found no dates — the markup changed; update the patterns in this script.",
              file=sys.stderr)
        print(f"  strip matches: {len(strip)}   news matches: {len(dates)}", file=sys.stderr)
        return 2

    problems = 0

    # ---- 1. sync -------------------------------------------------------------
    newest3 = dates[:3]
    print("SYNC")
    print(f"  homepage strip : {strip}")
    print(f"  news 3 newest  : {newest3}")
    if len(strip) != 3:
        fail(f"the strip has {len(strip)} rows; it must have exactly 3")
        problems += 1
    elif strip != newest3:
        fail("fix the .latest__list rows in index.html to match, in order")
        problems += 1
    else:
        print("  ok")

    # ---- 2. provenance -------------------------------------------------------
    print("PROVENANCE")
    checked = 0
    for src, verified, body in NEWS_ITEM.findall(news):
        date = NEWS_DATE.search(body)
        if not date:            # career-timeline rows carry no date chip; not news
            continue
        checked += 1
        if not src:
            fail(f'{date.group(1)} has no source comment. Add, directly above the '
                 f'<article>:  <!-- source: <url-or-repo-path> | verified YYYY-MM-DD -->')
            problems += 1
        elif src.startswith(("http://", "https://")):
            pass                                  # external source, cannot check offline
        elif (ROOT / src).is_file():
            pass                                  # artifact stored in the repo (e.g. a poster)
        else:
            fail(f"{date.group(1)} source is neither a URL nor a file in this repo: {src}")
            problems += 1
    if checked == 0:
        print("  found 0 news items — the markup changed; update the patterns.",
              file=sys.stderr)
        return 2
    if problems == 0 or checked:
        print(f"  {checked} news items checked")

    # ---- 3. counters ----------------------------------------------------------
    print("COUNTERS")
    try:
        pubs = (ROOT / "publications" / "index.html").read_text(encoding="utf-8")
        books = (ROOT / "books" / "index.html").read_text(encoding="utf-8")
    except OSError as exc:
        print(f"cannot read publications/index.html or books/index.html: {exc}",
              file=sys.stderr)
        return 2

    news_label = re.search(r'<span class="series-count">(\d+) updates</span>', news)
    news_actual = checked  # articles carrying a date chip in news/index.html's timeline

    chapters_section = re.search(r'id="chapters".*?</section>', pubs, re.S)
    chapters_body = strip_comments(chapters_section.group(0)) if chapters_section else ""
    chapters_label = re.search(r'<span class="series-count">(\d+) chapters</span>', chapters_body)
    chapters_actual = len(re.findall(r'<article class="card card--row">', chapters_body))

    published_section = re.search(r'id="published".*?</section>', books, re.S)
    published_body = strip_comments(published_section.group(0)) if published_section else ""
    novels_label = re.search(r'<span class="series-count">(\d+) novels?</span>', published_body)
    # The card is a whole-card link since the detail pages landed (2026-08-23):
    # <a class="card card--feature" href="..."> — class attribute FIRST, then
    # href, so this pattern keys on the class prefix and tolerates any href.
    # ^[ \t]* anchored for the same reason NEWS_ITEM is: books/index.html writes the
    # markup contract as an HTML comment directly beside the label, and an unanchored
    # pattern would count that quoted <a> tag as a real card (strip_comments already
    # removes it; the anchor stays as defense in depth).
    novels_actual = len(re.findall(r'^[ \t]*<a class="card card--feature"',
                                   published_body, re.M))

    manuscripts_section = re.search(r'id="manuscripts".*?</section>', books, re.S)
    manuscripts_body = strip_comments(manuscripts_section.group(0)) if manuscripts_section else ""
    manuscripts_label = re.search(r'<span class="series-count">(\d+) complete</span>',
                                  manuscripts_body)
    # ^[ \t]* anchored like the two patterns above: the manuscript cards are the
    # bare .card primitive — whole-card links, <a class="card" href="..."> — and
    # an unanchored pattern would also count any <a class="card"> quoted inside
    # a maintenance comment.  The closing quote after "card" keeps the feature
    # card (class="card card--feature") out of this count.
    manuscripts_actual = len(re.findall(r'^[ \t]*<a class="card"',
                                        manuscripts_body, re.M))

    if not news_label:
        fail('news/index.html: no "N updates" series-count label found — '
             'the markup changed; update the pattern in this script')
        problems += 1
    elif int(news_label.group(1)) != news_actual:
        fail(f'news/index.html says "{news_label.group(1)} updates" but the '
             f'timeline actually has {news_actual} item(s)')
        problems += 1
    else:
        print(f'  news/index.html          "{news_label.group(1)} updates" '
              f'== {news_actual} actual — ok')

    if not chapters_section or not chapters_label:
        fail('publications/index.html: no "N chapters" series-count label found in the '
             '#chapters section — the markup changed; update the pattern in this script')
        problems += 1
    elif int(chapters_label.group(1)) != chapters_actual:
        fail(f'publications/index.html says "{chapters_label.group(1)} chapters" but the '
             f'#chapters section actually has {chapters_actual} row(s)')
        problems += 1
    else:
        print(f'  publications/index.html  "{chapters_label.group(1)} chapters" '
              f'== {chapters_actual} actual — ok')

    if not published_section or not novels_label:
        fail('books/index.html: no "N novel" series-count label found in the '
             '#published section — the markup changed; update the pattern in this script')
        problems += 1
    elif int(novels_label.group(1)) != novels_actual:
        fail(f'books/index.html says "{novels_label.group(1)} novel" but the '
             f'#published section actually has {novels_actual} card(s)')
        problems += 1
    else:
        print(f'  books/index.html         "{novels_label.group(1)} novel" '
              f'== {novels_actual} actual — ok')

    if not manuscripts_section or not manuscripts_label:
        fail('books/index.html: no "N complete" series-count label found in the '
             '#manuscripts section — the markup changed; update the pattern in this script')
        problems += 1
    elif int(manuscripts_label.group(1)) != manuscripts_actual:
        fail(f'books/index.html says "{manuscripts_label.group(1)} complete" but the '
             f'#manuscripts section actually has {manuscripts_actual} card(s)')
        problems += 1
    else:
        print(f'  books/index.html         "{manuscripts_label.group(1)} complete" '
              f'== {manuscripts_actual} actual — ok')

    print("PASS" if problems == 0 else f"FAIL — {problems} problem(s)")
    return 0 if problems == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
