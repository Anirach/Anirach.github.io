#!/usr/bin/env python3
"""Draw every blog cover in the house visual language, from one spec table.

WHY THIS EXISTS
---------------
35 of the 37 covers were AI clip-art: glowing blue circuit-brains, neon
hexagons, robots at keyboards. They were indistinguishable from one another at
card size, carried no information, and cost 4.1 MB. The two exceptions were
drawn by an earlier version of this script and were the only covers that looked
like they belonged to this site.

The language is deliberately the BOOK JACKETS' — the same navy/cream/blue/gold
the palette was re-keyed to in 2026-08-26 — not the AI clip-art house style:
a flat ground, one geometric motif built from the post's own subject, one gold
accent, and real typography. Flat art, so JPEG at a fraction of the old weight.

    python3 scripts/make_cover.py --all          # redraw all 37 + share cards
    python3 scripts/make_cover.py openclaw-101   # one, by slug
    python3 scripts/make_cover.py --check        # validate the table, draw nothing
    python3 scripts/make_cover.py --contact      # 37-up contact sheet for review

THE SPEC TABLE
--------------
`scripts/covers.tsv` is the single source of truth: one row per post,
`slug | out | motif | ground | eyebrow | title | thai | opts`. Adding a post
means adding a row, not editing this file. The renderer is deliberately dumb;
all the judgement lives in the table.

TWO RULES THE CHECKER ENFORCES
------------------------------
1. A cover's ground may never be its post's own hero family. A teal cover on a
   teal hero vanishes — that is a defect this site actually shipped.
2. Everything that carries meaning stays inside the SAFE BAND, y in
   [0.20, 0.80] and x in [0.12, 0.88]. blog/index.html crops covers to 16:10
   and was already cutting the Thai line off the two drawn covers.
"""
import argparse
import csv
import pathlib
import re
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = pathlib.Path(__file__).resolve().parents[1]
FONTS = pathlib.Path(__file__).resolve().parent / "fonts"
TABLE = pathlib.Path(__file__).resolve().parent / "covers.tsv"
OUT = ROOT / "images"

S = 1600                      # drawn at 2x, downsampled — keeps type crisp
FINAL = 800                   # every existing cover is 800x800; do not churn 74 <img> tags
OG = (1200, 630)              # share card, re-laid rather than cropped
KB_FAIL = 90
KB_WARN = 60

# Safe band: the 16:10 card crop and the 1.91:1 share crop both eat the edges.
BAND_Y = (0.20, 0.80)
BAND_X = (0.12, 0.88)

GOLD = (196, 164, 108)        # --gold
GOLD_DARK = (122, 95, 34)     # --gold-dark
NAVY = (17, 48, 75)           # --navy
SLATE = (82, 97, 116)         # --slate-light

# The five grounds, all from the book-jacket palette. `deep` is the Deep Blue
# hero gradient; the rest are flat, because a flat ground is what makes the
# motif read at 96px on a phone.
GROUNDS = {
    "navy":      ("flat", (0x11, 0x30, 0x4b)),
    "deep":      ("grad", [(0.0, (0x11, 0x30, 0x4b)), (0.45, (0x1a, 0x4d, 0x7a)),
                           (1.0, (0x22, 0x62, 0x99))]),
    "cloud":     ("flat", (0xde, 0xe7, 0xe6)),
    "parchment": ("flat", (0xe9, 0xe1, 0xc4)),
    "cream":     ("flat", (0xfa, 0xf7, 0xf0)),
}
DARK_GROUNDS = {"navy", "deep"}

# A cover must CONTRAST with the hero it sits under, so the forbidden set is
# the SAME-TONE grounds: a pale jacket on the pale Sunrise hero washes out, and
# a navy jacket on the navy Deep Blue hero disappears entirely. The site shipped
# the second failure once already (a teal cover on a teal hero).
#
#   Sunrise hero  (light) -> navy | deep         cover
#   Deep Blue hero (dark) -> cloud | parchment | cream
FORBIDDEN = {"sunrise": {"cloud", "parchment", "cream"}, "deepblue": {"navy", "deep"}}


# --------------------------------------------------------------------------
# type
# --------------------------------------------------------------------------
_font_cache = {}


def font(px, weight="Bold"):
    key = (px, weight)
    if key not in _font_cache:
        f = ImageFont.truetype(str(FONTS / "Inter-var.ttf"), px)
        try:
            f.set_variation_by_name(weight)
        except Exception:
            pass
        _font_cache[key] = f
    return _font_cache[key]


def thai_font(px):
    key = (px, "thai")
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(str(FONTS / "Sarabun-Regular.ttf"), px)
    return _font_cache[key]


def fit(draw, text, px, weight, max_w, floor=64):
    """Shrink until the line fits the safe band. Titles vary from 'SRE' to
    'Infrastructure as Code' and a fixed size would either overflow or waste
    half the canvas."""
    while px > floor:
        f = font(px, weight)
        if draw.textlength(text, font=f) <= max_w:
            return f
        px -= 4
    return font(floor, weight)


def wrap(draw, text, f, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=f) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# --------------------------------------------------------------------------
# grounds
# --------------------------------------------------------------------------
def ground(name, size):
    kind, spec = GROUNDS[name]
    w, h = size
    if kind == "flat":
        return Image.new("RGB", size, spec)
    # diagonal gradient, vectorised — the per-pixel version took ~10s a cover
    ys, xs = np.mgrid[0:h, 0:w]
    t = (xs / w) * 0.55 + (ys / h) * 0.45
    pos = np.array([p for p, _ in spec])
    cols = np.array([c for _, c in spec], dtype=float)
    out = np.zeros((h, w, 3))
    for i in range(len(spec) - 1):
        m = (t >= pos[i]) & (t <= pos[i + 1])
        k = np.clip((t - pos[i]) / max(pos[i + 1] - pos[i], 1e-9), 0, 1)
        for c in range(3):
            out[..., c] = np.where(m, cols[i][c] + (cols[i + 1][c] - cols[i][c]) * k,
                                   out[..., c])
    out[t > pos[-1]] = cols[-1]
    out[t < pos[0]] = cols[0]
    return Image.fromarray(out.astype("uint8"), "RGB")


def ink(g):
    """Every colour decision follows from the ground, so a row cannot pick an
    unreadable combination by hand."""
    dark = g in DARK_GROUNDS
    return {
        "title": (255, 255, 255) if dark else NAVY,
        "eyebrow": GOLD if dark else GOLD_DARK,      # 5.73:1 on navy, >=4.6:1 on the light three
        "thai": (255, 255, 255, 190) if dark else (*SLATE, 255),
        "rule": GOLD if dark else GOLD_DARK,
        "line": (255, 255, 255, 120) if dark else (*NAVY, 90),
        "fill": (255, 255, 255, 26) if dark else (*NAVY, 16),
        "grid": (255, 255, 255, 12) if dark else (*NAVY, 12),
    }


# --------------------------------------------------------------------------
# motifs — each is the post's subject, not decoration
# --------------------------------------------------------------------------
def m_planes(d, box, c, opts):
    """Stacked, offset planes: layers feeding layers. Memory tiers, request
    lifecycle, architecture strata."""
    x0, y0, x1, y1 = box
    n = 3
    w, h = int((x1 - x0) * 0.74), int((y1 - y0) * 0.20)
    step = ((y1 - y0) - h) / (n - 1)
    for i in range(n):
        x = int(x0 + i * (x1 - x0) * 0.055)
        y = int(y0 + i * step)
        last = i == n - 1
        d.rounded_rectangle([x, y, x + w, y + h], radius=26,
                            fill=c["fill"], outline=c["rule"] if last else c["line"], width=5)
        if i < n - 1:
            cx = x + w // 2
            gap_top, gap_bot = y + h + 8, int(y0 + (i + 1) * step) - 8
            if gap_bot - gap_top > 24:
                d.line([(cx, gap_top), (cx, gap_bot - 18)], fill=c["rule"], width=6)
                d.polygon([(cx - 13, gap_bot - 20), (cx + 13, gap_bot - 20), (cx, gap_bot)],
                          fill=c["rule"])


def m_chain(d, box, c, opts):
    """A pipeline: n stages, the last one lit. CI/CD, git flow, a build."""
    x0, y0, x1, y1 = box
    n = int(opts.get("n", 4))
    loop = opts.get("loop")
    gap = (x1 - x0) * 0.055
    side = ((x1 - x0) - gap * (n - 1)) / n
    y = y0 + ((y1 - y0) - side) / 2
    for i in range(n):
        x = x0 + i * (side + gap)
        lit = (i == n - 1) and not loop
        d.rounded_rectangle([x, y, x + side, y + side], radius=24,
                            fill=(*c["rule"], 45) if lit else c["fill"],
                            outline=c["rule"] if lit else c["line"], width=5)
        if i < n - 1:
            cx = x + side + gap / 2
            d.line([(x + side + 8, y + side / 2), (cx + 8, y + side / 2)],
                   fill=c["line"], width=6)
            d.polygon([(cx + 4, y + side / 2 - 11), (cx + 4, y + side / 2 + 11),
                       (cx + 24, y + side / 2)], fill=c["line"])
    if loop:
        # the return arc — GitOps and idle self-improvement are cycles, not lines
        by = y + side + (y1 - y0) * 0.10
        d.line([(x0 + side / 2, y + side + 8), (x0 + side / 2, by),
                (x1 - side / 2, by), (x1 - side / 2, y + side + 22)],
               fill=c["rule"], width=6, joint="curve")
        d.polygon([(x1 - side / 2 - 12, y + side + 24), (x1 - side / 2 + 12, y + side + 24),
                   (x1 - side / 2, y + side + 4)], fill=c["rule"])


def m_nest(d, box, c, opts):
    """Concentric containment: a boundary inside a boundary. Security layers,
    sandboxes, isolation, a container inside an orchestrator.

    The first version drew SQUARES centred in the band. Two things broke. The
    band is wide and short, so a square was constrained by the short side and
    came out tiny — a stamp floating in space. And centring put it off the left
    axis that the eyebrow, title, rule and Thai line all share, so it was the
    one motif that did not line up with anything. Nesting rectangles that
    follow the band's own proportions fixes both, and reads more like a
    boundary inside a boundary than a square inside a square did."""
    x0, y0, x1, y1 = box
    n = int(opts.get("rings", 3))
    for i in range(n):
        k = i / n * 0.34                     # inset each ring by a share of the band
        ix = (x1 - x0) * k
        iy = (y1 - y0) * k
        inner = i == n - 1
        d.rounded_rectangle([x0 + ix, y0 + iy, x1 - ix, y1 - iy],
                            radius=int(30 - i * 5),
                            fill=(*c["rule"], 40) if inner else c["fill"] if i else None,
                            outline=c["rule"] if inner else c["line"], width=5)


def m_tree(d, box, c, opts):
    """A root branching into children — and, with hub, edges between them.
    Branching, orchestration, an agent delegating."""
    x0, y0, x1, y1 = box
    n = int(opts.get("n", 3))
    hub = opts.get("hub")
    rw, rh = (x1 - x0) * 0.34, (y1 - y0) * 0.17
    rx, ry = (x0 + x1) / 2 - rw / 2, y0
    d.rounded_rectangle([rx, ry, rx + rw, ry + rh], radius=22,
                        fill=(*c["rule"], 40), outline=c["rule"], width=5)
    cw = (x1 - x0 - (x1 - x0) * 0.05 * (n - 1)) / n
    ch = (y1 - y0) * 0.17
    cy = y1 - ch
    kids = []
    for i in range(n):
        cx = x0 + i * (cw + (x1 - x0) * 0.05)
        d.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=22,
                            fill=c["fill"], outline=c["line"], width=5)
        kids.append(cx + cw / 2)
        d.line([((rx + rx + rw) / 2, ry + rh + 6), (cx + cw / 2, cy - 6)],
               fill=c["line"], width=5)
    if hub:
        for a, b in zip(kids, kids[1:]):
            d.line([(a, cy + ch + 14), (b, cy + ch + 14)], fill=c["rule"], width=5)


def m_grid(d, box, c, opts):
    """A field of uniform cells with a few lit: coverage, observability,
    a matrix of jobs, a marketplace of skills."""
    x0, y0, x1, y1 = box
    cols, rows = 4, 3
    gx, gy = (x1 - x0) * 0.045, (y1 - y0) * 0.07
    w = ((x1 - x0) - gx * (cols - 1)) / cols
    h = ((y1 - y0) - gy * (rows - 1)) / rows
    lit = set(opts.get("lit", "1,6,10").split(","))
    for r in range(rows):
        for cc in range(cols):
            i = r * cols + cc
            x, y = x0 + cc * (w + gx), y0 + r * (h + gy)
            on = str(i) in lit
            d.rounded_rectangle([x, y, x + w, y + h], radius=18,
                                fill=(*c["rule"], 45) if on else c["fill"],
                                outline=c["rule"] if on else c["line"], width=4)


MOTIFS = {"planes": m_planes, "chain": m_chain, "nest": m_nest,
          "tree": m_tree, "grid": m_grid}


# --------------------------------------------------------------------------
# the one renderer
# --------------------------------------------------------------------------
def render(row, size=(S, S), og=False):
    W, H = size
    img = ground(row["ground"], size).convert("RGB")
    d = ImageDraw.Draw(img, "RGBA")
    c = ink(row["ground"])
    opts = dict(kv.split("=", 1) for kv in row["opts"].split(";") if kv)

    # faint structural grid, full-bleed (it is texture, not meaning, so it may
    # leave the safe band)
    pitch = int(min(W, H) * 0.0625)
    for i in range(0, max(W, H), pitch):
        d.line([(i, 0), (i, H)], fill=c["grid"], width=2)
        d.line([(0, i), (W, i)], fill=c["grid"], width=2)

    if og:
        # share card: type left, motif right — re-laid, never cropped
        lx = int(W * 0.07)
        maxw = int(W * 0.46)
        d.text((lx, int(H * 0.20)), row["eyebrow"], font=font(28, "Bold"), fill=c["eyebrow"])
        f = fit(d, row["title"], 76, "Black", maxw, floor=40)
        lines = wrap(d, row["title"], f, maxw)
        y = int(H * 0.28)
        for ln in lines[:3]:
            d.text((lx, y), ln, font=f, fill=c["title"])
            y += int(f.size * 1.12)
        d.line([(lx, y + 18), (lx + int(W * 0.09), y + 18)], fill=c["rule"], width=6)
        if row["thai"]:
            tf = thai_font(30)
            for ln in wrap(d, row["thai"], tf, maxw)[:2]:
                y += 46
                d.text((lx, y + 24), ln, font=tf, fill=c["thai"])
        box = (int(W * 0.58), int(H * 0.22), int(W * 0.94), int(H * 0.80))
        MOTIFS[row["motif"]](d, box, c, opts)
        return img

    # square cover: everything meaningful inside the safe band
    lx = int(W * BAND_X[0] + W * 0.02)
    maxw = int(W * (BAND_X[1] - BAND_X[0]) - W * 0.04)

    d.text((lx, int(H * 0.215)), row["eyebrow"], font=font(40, "Bold"), fill=c["eyebrow"])

    f = fit(d, row["title"], 116, "Black", maxw)
    lines = wrap(d, row["title"], f, maxw)
    if len(lines) > 1:
        f = fit(d, max(lines, key=len), 104, "Black", maxw)
        lines = wrap(d, row["title"], f, maxw)
    y = int(H * 0.255)
    for ln in lines[:2]:
        d.text((lx, y), ln, font=f, fill=c["title"])
        y += int(f.size * 1.06)

    motif_top = max(int(H * 0.42), y + int(H * 0.02))
    box = (lx, motif_top, int(W * BAND_X[1]), int(H * 0.66))
    MOTIFS[row["motif"]](d, box, c, opts)

    d.line([(lx, int(H * 0.705)), (lx + int(W * 0.14), int(H * 0.705))],
           fill=c["rule"], width=8)
    if row["thai"]:
        tf = thai_font(44)
        ty = int(H * 0.728)
        for ln in wrap(d, row["thai"], tf, maxw)[:2]:
            d.text((lx, ty), ln, font=tf, fill=c["thai"])
            ty += 56
    return img


def save(img, path, size, quality=82):
    img = img.resize(size, Image.LANCZOS)
    img = img.filter(ImageFilter.UnsharpMask(radius=1.2, percent=55, threshold=3))
    img.save(path, "JPEG", quality=quality, optimize=True, progressive=True)
    return path.stat().st_size / 1024


# --------------------------------------------------------------------------
# table + checks
# --------------------------------------------------------------------------
def load():
    with open(TABLE, encoding="utf-8") as fh:
        rows = [r for r in csv.DictReader(fh, delimiter="\t")
                if r["slug"] and not r["slug"].startswith("#")]
    for r in rows:
        r["opts"] = r.get("opts") or ""
        r["thai"] = r.get("thai") or ""
    return rows


def hero_family(slug):
    """Read the post's actual hero gradient so rule 1 is checked against
    reality, not against a second table that could drift out of step."""
    p = ROOT / "blog" / (slug + ".html")
    if not p.exists():
        return None
    s = p.read_text(encoding="utf-8")
    if "#eef3f3" in s and ".post-hero" in s:
        return "sunrise"
    if "#11304b 0%" in s:
        return "deepblue"
    return None


def check(rows):
    bad = []
    seen = set()
    for r in rows:
        if r["motif"] not in MOTIFS:
            bad.append("%s: unknown motif %r" % (r["slug"], r["motif"]))
        if r["ground"] not in GROUNDS:
            bad.append("%s: unknown ground %r" % (r["slug"], r["ground"]))
        if r["out"] in seen:
            bad.append("%s: two posts write %s" % (r["slug"], r["out"]))
        seen.add(r["out"])
        if not (ROOT / "blog" / (r["slug"] + ".html")).exists():
            bad.append("%s: no such post" % r["slug"])
        fam = hero_family(r["slug"])
        if fam and r["ground"] in FORBIDDEN.get(fam, set()):
            bad.append("%s: ground %r is its own hero family (%s) — the cover "
                       "will vanish into the hero" % (r["slug"], r["ground"], fam))
    posts = {p.stem for p in (ROOT / "blog").glob("*.html") if p.stem != "index"}
    for missing in sorted(posts - {r["slug"] for r in rows}):
        bad.append("%s has no row in covers.tsv" % missing)

    # "37 covers that all look like one cover" is the real risk of a system
    # this regular, and it shows up worst between NEIGHBOURS — two cards side
    # by side on the index with the same ground and the same motif read as a
    # duplicate image. Checked in the order a reader actually meets them, not
    # the order of this table.
    idx = (ROOT / "blog" / "index.html").read_text(encoding="utf-8")
    idx = re.sub(r"<!--.*?-->", "", idx, flags=re.S)
    order = [m.group(1) for m in
             re.finditer(r'<a href="([a-z0-9-]+)\.html" class="card"', idx)]
    by = {r["slug"]: r for r in rows}
    for a, b in zip(order, order[1:]):
        if a in by and b in by and by[a]["ground"] == by[b]["ground"] \
                and by[a]["motif"] == by[b]["motif"]:
            bad.append("%s and %s are adjacent on the index and share both "
                       "ground (%s) and motif (%s)" % (a, b, by[a]["ground"], by[a]["motif"]))
    return bad


def contact_sheet(rows):
    cols, cell, pad = 6, 260, 10
    n = len(rows)
    rowsn = (n + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (cell + pad) + pad, rowsn * (cell + pad) + pad),
                      (250, 247, 240))
    for i, r in enumerate(rows):
        p = OUT / r["out"]
        if not p.exists():
            continue
        im = Image.open(p).resize((cell, cell), Image.LANCZOS)
        sheet.paste(im, (pad + (i % cols) * (cell + pad), pad + (i // cols) * (cell + pad)))
    # A dot-dir, like .fingerprints/: Jekyll never publishes a path starting
    # with "." and INV-06a would otherwise report the sheet as an unreferenced
    # published image — which it correctly did the first time this ran.
    out = ROOT / ".covers" / "contact-sheet.jpg"
    out.parent.mkdir(exist_ok=True)
    sheet.save(out, "JPEG", quality=88, optimize=True)
    print("contact sheet: %s (%d covers, %.0f KB)" % (out.relative_to(ROOT), n, out.stat().st_size / 1024))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug", nargs="?")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--contact", action="store_true")
    ap.add_argument("--no-og", action="store_true")
    a = ap.parse_args()

    rows = load()
    bad = check(rows)
    if bad:
        print("covers.tsv FAILED %d check(s):" % len(bad))
        for b in bad:
            print("  x", b)
        return 1
    if a.check:
        print("covers.tsv OK — %d rows, %d motifs, %d grounds"
              % (len(rows), len({r["motif"] for r in rows}), len({r["ground"] for r in rows})))
        return 0
    if a.contact:
        contact_sheet(rows)
        return 0

    todo = rows if a.all else [r for r in rows if r["slug"] == a.slug]
    if not todo:
        print("no such slug: %s (use --all)" % a.slug)
        return 2

    worst, total, fails = 0.0, 0.0, 0
    for r in todo:
        kb = save(render(r), OUT / r["out"], (FINAL, FINAL))
        line = "%-42s %5.0f KB" % (r["out"], kb)
        if kb > KB_FAIL:
            line += "  OVER BUDGET"
            fails += 1
        elif kb > KB_WARN:
            line += "  (warn)"
        if not a.no_og:
            ogk = save(render(r, OG, og=True), OUT / (r["slug"] + "-og.jpg"), OG, quality=80)
            line += "   og %4.0f KB" % ogk
            total += ogk
        print(line)
        worst = max(worst, kb)
        total += kb
    print("\n%d covers  |  worst %.0f KB (fail >%d)  |  %.1f MB total"
          % (len(todo), worst, KB_FAIL, total / 1024))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
