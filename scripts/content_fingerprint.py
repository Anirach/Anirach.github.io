#!/usr/bin/env python3
"""Prove a page's CONTENT survived a chrome conversion.

Phase 3 converts 11 island posts to house chrome. The chrome must change;
the writing must not. This extracts what a reader actually sees — visible
text and code, in order, with markup and CSS stripped — so a before/after
comparison catches a single dropped paragraph in a 66 KB file.

    python3 scripts/content_fingerprint.py save blog/openclaw-101.html
    ...convert the file...
    python3 scripts/content_fingerprint.py check blog/openclaw-101.html

`check` exits 0 only when the visible text is identical. It reports the
first differing line and the counts on each side. Fingerprints live in
.fingerprints/ (git-ignored, dot-dir so Jekyll never publishes it).
"""
import html
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
STORE = ROOT / ".fingerprints"

# Everything that is chrome, styling or metadata rather than content.
DROP_BLOCKS = re.compile(
    r"<(script|style|nav|footer|head)\b.*?</\1>|<!--.*?-->", re.S | re.I)
TAG = re.compile(r"<[^>]+>")
WS = re.compile(r"[ \t ]+")


def visible_text(path: pathlib.Path) -> list[str]:
    s = path.read_text(encoding="utf-8")
    s = DROP_BLOCKS.sub("\n", s)
    # a block-level close should not glue two sentences together
    s = re.sub(r"</(p|div|h[1-6]|li|pre|blockquote|td|tr|section|article|header)>",
               "\n", s, flags=re.I)
    s = re.sub(r"<br\s*/?>", "\n", s, flags=re.I)
    s = TAG.sub("", s)
    s = html.unescape(s)
    out = []
    for line in s.splitlines():
        line = WS.sub(" ", line).strip()
        if line:
            out.append(line)
    return out


def path_for(target: pathlib.Path) -> pathlib.Path:
    return STORE / (str(target).replace("/", "__") + ".txt")


def main() -> int:
    if len(sys.argv) != 3 or sys.argv[1] not in ("save", "check"):
        print(__doc__)
        return 2
    mode, target = sys.argv[1], pathlib.Path(sys.argv[2])
    if not target.exists():
        print(f"no such file: {target}")
        return 2
    lines = visible_text(target)
    store = path_for(target)
    if mode == "save":
        STORE.mkdir(exist_ok=True)
        store.write_text("\n".join(lines), encoding="utf-8")
        print(f"saved {len(lines)} content lines for {target}")
        return 0

    if not store.exists():
        print(f"NO BASELINE for {target} — run `save` before converting")
        return 2
    before = store.read_text(encoding="utf-8").splitlines()
    if before == lines:
        print(f"OK {target}: {len(lines)} content lines identical")
        return 0
    print(f"CONTENT CHANGED {target}: {len(before)} lines before, {len(lines)} after")
    bset, aset = set(before), set(lines)
    lost = [l for l in before if l not in aset]
    added = [l for l in lines if l not in bset]
    for l in lost[:5]:
        print(f"  LOST  : {l[:110]}")
    for l in added[:5]:
        print(f"  ADDED : {l[:110]}")
    if len(lost) > 5 or len(added) > 5:
        print(f"  ... {len(lost)} lost, {len(added)} added in total")
    return 1


if __name__ == "__main__":
    sys.exit(main())
