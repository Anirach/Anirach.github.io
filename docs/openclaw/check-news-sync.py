#!/usr/bin/env python3
"""Gate for news updates on anirach.com. Run from anywhere; resolves the repo itself.

Two things nothing else in this repo checks:

1. SYNC — index.html's "Latest updates" strip must list the 3 newest items from
   news/index.html, in order. This shipped wrong once: the homepage showed
   Jul 2026 / Dec 2025 / Nov 2024 while the news page's third-newest was Oct 2025,
   so an entire update was invisible from the front page.

2. PROVENANCE — every news item must carry an HTML comment naming the source it was
   verified against. This is the anti-fabrication gate. A structural checker cannot
   tell a true item from an invented one, so instead it refuses to let an item exist
   without a stated source. Omitting a source now fails the build; fabricating one
   requires writing a deliberate falsehood into the file, which is auditable.

Exit 0 = both pass.  1 = a real problem.  2 = the checker itself could not run
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


def fail(msg: str) -> None:
    print(f"  ✗ {msg}")


def main() -> int:
    try:
        home = (ROOT / "index.html").read_text(encoding="utf-8")
        news = (ROOT / "news" / "index.html").read_text(encoding="utf-8")
    except OSError as exc:
        print(f"cannot read site files: {exc}", file=sys.stderr)
        return 2

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

    print("PASS" if problems == 0 else f"FAIL — {problems} problem(s)")
    return 0 if problems == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
