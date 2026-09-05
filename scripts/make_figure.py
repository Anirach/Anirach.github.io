#!/usr/bin/env python3
"""Draw the diagram figures for the AI Transformation series, from one
registry of named drawing functions.

    python3 scripts/make_figure.py 10-five-rails   # one figure (a unique prefix works: "10")
    python3 scripts/make_figure.py --all           # every implemented figure; stubs print SKIP
    python3 scripts/make_figure.py --check         # registry, fonts, text bboxes, fits, contrast
    python3 scripts/make_figure.py --contact       # 3-up 420-px review sheet -> .covers/figures-contact.jpg
    python3 scripts/make_figure.py --phone         # every figure at 335 px    -> .covers/figures-phone.jpg

THE SYSTEM (plan: make-the-openclaw-and-glimmering-tome, section 3 + Appendix B)
--------------------------------------------------------------------------------
Every figure is an opaque white card, 1400 wide, one of four heights (STRIP 560,
WIDE 700, STD 840, TALL 1000), drawn at 2x and LANCZOS-downsampled so type stays
crisp, then written as a 128-colour palette PNG (96 if that is over budget).
Coordinates in every figure function are FINAL pixels -- the helpers multiply
by K -- so the geometry in Appendix B can be typed in verbatim. Margin 60; the
checker demands every text bbox stay 20 px inside the edge.

Palette roles (house :root tokens, never invented colours):
  ink NAVY, ink-2 SLATE (slate-light), flow BLUE, flow-2 BLUE_LIGHT, CORAL for
  the envelope / red line / AI-core / Model tile / BLOCK (text only on white),
  GOLD + GOLD_DARK, GREEN, RED (Contain ring only), tints blue -> green -> gold
  -> coral -> gray. A tile's outline is its own token at 3 px.

Type: L1 Inter Bold 32 caps navy (36 in tiles >= 300 wide), Thai gloss Sarabun
26 navy @85 %, L2 Inter Medium 24 slate-light; core-bar line 1 Bold 32-36 white;
badge Black 28 white; axis Bold 26 + Sarabun 22; chip Bold 26 + Sarabun 22.
fit() shrinks to floor 26 (L1) / 22 (everything else) and PRINTS when it does.
Inter has no Thai glyphs and there is no bold Sarabun: any string containing a
Thai character is set in Sarabun Regular, whole.

HELPERS -- the vocabulary other figure functions are written against
(all coordinates final px; `d` is the Fig canvas handed to every figure fn):

  tile(d, box, key, l1=None, th=None, l2=None, l1px=None, thpx=26, l2px=24,
       rows=None, solid=False, outline=None, ow=3, pad=12, gap=6)
  bar(d, box, rows, px=34, l2px=26, thpx=26, pad=30, gap=8)      dark core bar
  disc(d, c, r, rows, px=36, thpx=28, gap=6)                     dark core disc
  node(d, c, key, l1, th=None, rx=100, ry=55, px=28, thpx=24)    white ellipse
  node_geom(d, l1, px=28, rx=100, ry=55, th=True) -> (rx, px)    pre-compute for chords
  ring_points(c, rx, ry, n, start=-90) -> [(x, y)]
  ring_chords(d, pts, rxs, ry, col, w=4, gap=12)                 arrows node -> next node
  badge(d, c, n, r=26, px=28)
  chip(d, xy, key, l1, th=None, w=220, h=90, px=26, thpx=22)
  arrow(d, p0, p1, col, w=4, head=None)                          make_cover geometry
  envelope(d, box, col=CORAL, w=6, r=24)
  wedge(d, apex, b0, b1, label, px=22, col=CORAL)
  axes(d, frame, mx=None, my=None, w=4, mid_w=4, mid_col=NAVY)
  text(d, xy, s, px, weight="Bold", col=NAVY, anchor="mm", kind="L1", maxw=None, floor=None) -> bbox
  mixed(d, xy, en, th, px=26, thpx=22, col=NAVY, anchor="mm", kind="AXIS", gap=14) -> bbox
  rtext(d, c, en, th=None, px=26, thpx=22, col=NAVY, angle=90, kind="AXIS") -> bbox
  stack(d, cx, cy, rows, maxw=None, gap=6, align="m") -> [bbox]  centred lines
  L1(s, px=32, col=NAVY) / TH(s, px=26, col=NAVY_85) / L2(s, px=24, col=SLATE) / row(...)
  fit(d, s, px, weight, maxw, floor=26) -> (font, px)
  row_px(d, labels, px, weight="Bold", maxw=..., floor=26) -> px  one size for a row
  wrap(d, s, f, maxw) -> [lines]
  tint(rgb, a) -> rgb            rr / ellipse / line / polygon   raw shapes

Rows for stack()/tile(rows=)/bar()/disc() are (text, px, weight, colour, kind)
tuples; weight "thai" (or any Thai character) selects Sarabun. Kinds drive the
checker: "L1" boxes may not overlap each other; every box must clear the inner
margin. Sentence-length footers and panel titles are NOT drawn -- they belong
to the per-track <figcaption>.
"""
import argparse
import math
import pathlib
import re
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parents[1]
FONTS = pathlib.Path(__file__).resolve().parent / "fonts"
OUT = ROOT / "images"
SHEETS = ROOT / ".covers"                    # gitignored, like make_cover's contact sheet
PREFIX = "ai-transformation-fig-"

K = 2                                         # draw at 2x, LANCZOS down to final
SIZES = {"STRIP": (1400, 560), "WIDE": (1400, 700), "STD": (1400, 840), "TALL": (1400, 1000)}
MARGIN = 60
INNER = 20                                    # --check: text may not come closer to an edge
KB_WARN = 60
KB_FAIL = 80
COLORS = 128
COLORS_FALLBACK = 96                          # tried before anyone touches geometry
FLOOR_L1 = 26
FLOOR_L2 = 22

# --------------------------------------------------------------------------
# palette
# --------------------------------------------------------------------------
NAVY = (17, 48, 75)          # --navy        #11304b
SLATE = (82, 97, 116)        # --slate-light #526174
GRAY = (148, 163, 184)       # --gray
BLUE = (34, 98, 153)         # --blue        #226299
BLUE_LIGHT = (73, 146, 185)  # --blue-light  #4992b9
CORAL = (194, 65, 12)        # --coral       #c2410c
GOLD = (196, 164, 108)       # --gold        #c4a46c
GOLD_DARK = (122, 95, 34)    # --gold-dark   #7a5f22
GREEN = (34, 197, 94)        # --green
RED = (239, 68, 68)          # --red
WHITE = (255, 255, 255)
CREAM = (250, 247, 240)      # --bg, the review sheets' ground only

TOKENS = {
    "navy": NAVY, "slate": SLATE, "gray": GRAY, "blue": BLUE, "blue-light": BLUE_LIGHT,
    "coral": CORAL, "gold": GOLD, "gold-dark": GOLD_DARK, "green": GREEN, "red": RED,
    "white": WHITE,
}
TINT_A = {"blue": 0.12, "green": 0.15, "gold": 0.30, "coral": 0.14, "gray": 0.25}


def tint(rgb, a):
    """`a` of `rgb` over white."""
    return tuple(int(round(255 + (c - 255) * a)) for c in rgb)


TINTS = {k: tint(TOKENS[k], a) for k, a in TINT_A.items()}


def alpha(rgb, a):
    return (rgb[0], rgb[1], rgb[2], int(round(255 * a)))


NAVY_85 = alpha(NAVY, 0.85)   # Thai gloss
NAVY_45 = alpha(NAVY, 0.45)   # faint midlines (Fig 3), stems (A1)
NAVY_40 = alpha(NAVY, 0.40)   # white tiles' outline (Fig 4)

# stroke weights + radii (Appendix B idioms)
W_HAIR, W_CONN, W_EMPH, W_FRAME, W_RING = 3, 4, 6, 4, 5
R_TILE, R_BAR, R_CHIP, R_ENV = 14, 16, 14, 24

THAI = re.compile("[฀-๿]")


# --------------------------------------------------------------------------
# type
# --------------------------------------------------------------------------
_font_cache = {}


def font(px, weight="Bold"):
    """Inter at `px` FINAL pixels (the face is loaded at K x px)."""
    key = (px, weight)
    if key not in _font_cache:
        f = ImageFont.truetype(str(FONTS / "Inter-var.ttf"), int(round(px * K)))
        f.set_variation_by_name(weight)
        _font_cache[key] = f
    return _font_cache[key]


def thai_font(px):
    key = (px, "thai")
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(str(FONTS / "Sarabun-Regular.ttf"),
                                              int(round(px * K)))
    return _font_cache[key]


def face(px, weight="Bold", s=None):
    """Sarabun for anything Thai (Inter has no Thai glyphs), Inter otherwise."""
    if weight == "thai" or (s is not None and THAI.search(s)):
        return thai_font(px)
    return font(px, weight)


def line_h(px, weight, s):
    """The line box a row occupies: Sarabun carries marks above and below."""
    return px * 1.2 if (weight == "thai" or THAI.search(s)) else px


# --------------------------------------------------------------------------
# the canvas
# --------------------------------------------------------------------------
class Fig:
    def __init__(self, name, size_key):
        self.name = name
        self.size_key = size_key
        self.W, self.H = SIZES[size_key]
        self.img = Image.new("RGB", (self.W * K, self.H * K), WHITE)
        self.d = ImageDraw.Draw(self.img, "RGBA")
        self.boxes = []      # (kind, text, (x0, y0, x1, y1)) in final px
        self.fits = []       # (text, asked, got, fits)
        self.notes = []      # geometry the helpers changed (node rx widened, ...)
        self._geom = {}

    def width(self, s, f):
        return self.d.textlength(s, font=f) / K

    def note(self, msg):
        self.notes.append(msg)
        print("  note: " + msg)


def _sc(box):
    return [v * K for v in box]


def rr(d, box, r, fill=None, outline=None, w=0):
    d.d.rounded_rectangle(_sc(box), radius=r * K, fill=fill, outline=outline,
                          width=int(round(w * K)))


def ellipse(d, cx, cy, rx, ry, fill=None, outline=None, w=0):
    d.d.ellipse([(cx - rx) * K, (cy - ry) * K, (cx + rx) * K, (cy + ry) * K],
                fill=fill, outline=outline, width=int(round(w * K)))


def line(d, pts, col, w):
    d.d.line([(x * K, y * K) for x, y in pts], fill=col, width=int(round(w * K)),
             joint="curve")


def polygon(d, pts, fill=None, outline=None, w=0):
    d.d.polygon([(x * K, y * K) for x, y in pts], fill=fill, outline=outline,
                width=int(round(w * K)))


# --------------------------------------------------------------------------
# text
# --------------------------------------------------------------------------
def fit(d, s, px, weight, maxw, floor=FLOOR_L1):
    """Shrink 1 px at a time until `s` fits `maxw`; never below `floor`. Every
    shrink is recorded on the canvas and printed, so no size drops silently."""
    asked = px
    f = face(px, weight, s)
    while d.width(s, f) > maxw and px - 1 >= floor:
        px -= 1
        f = face(px, weight, s)
    ok = d.width(s, f) <= maxw
    if px != asked or not ok:
        _record_fit(d, s, asked, px, ok, floor)
    return f, px


def _record_fit(d, s, asked, got, ok, floor=FLOOR_L1):
    """One warning per (label, size) even if two passes fit the same label."""
    if (s, asked, got, ok) in d.fits:
        return
    d.fits.append((s, asked, got, ok))
    print("  fit: %r %d -> %d%s" % (s, asked, got,
                                     "" if ok else "  DOES NOT FIT at floor %d" % floor))


def row_px(d, labels, px, weight="Bold", maxw=0, floor=FLOOR_L1):
    """The largest size <= px at which EVERY label fits, so one row of tiles
    shares one L1 size instead of one tile shrinking alone."""
    p = px
    while p > floor and any(d.width(s, face(p, weight, s)) > maxw for s in labels):
        p -= 1
    if p != px:
        print("  row_px: %d -> %d so %r fits %d px" %
              (px, p, max(labels, key=lambda s: d.width(s, face(px, weight, s))), maxw))
    return p


def wrap(d, s, f, maxw):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if d.width(trial, f) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def text(d, xy, s, px, weight="Bold", col=NAVY, anchor="mm", kind="L1", maxw=None,
         floor=None):
    """One line. Records its ink bbox (final px) under `kind` for --check.
    With `maxw` the line is fit() to it first."""
    if maxw is not None:
        f, px = fit(d, s, px, weight, maxw,
                    floor if floor is not None else (FLOOR_L1 if kind == "L1" else FLOOR_L2))
    else:
        f = face(px, weight, s)
    x, y = xy
    d.d.text((x * K, y * K), s, font=f, fill=col, anchor=anchor)
    bb = tuple(v / K for v in d.d.textbbox((x * K, y * K), s, font=f, anchor=anchor))
    d.boxes.append((kind, s, bb))
    return bb


def mixed(d, xy, en, th, px=26, thpx=22, col=NAVY, anchor="mm", kind="AXIS", gap=14,
          weight="Bold"):
    """`EN LABEL  Thai gloss` on one line, two faces, placed as one unit."""
    we = d.width(en, font(px, weight))
    wt = d.width(th, thai_font(thpx))
    x, y = xy
    total = we + gap + wt
    x0 = {"m": x - total / 2, "l": x, "r": x - total}[anchor[0]]
    va = anchor[1]
    b1 = text(d, (x0, y), en, px, weight, col, "l" + va, kind)
    b2 = text(d, (x0 + we + gap, y), th, thpx, "thai", col, "l" + va, kind)
    return (min(b1[0], b2[0]), min(b1[1], b2[1]), max(b1[2], b2[2]), max(b1[3], b2[3]))


def rtext(d, c, en, th=None, px=26, thpx=22, col=NAVY, angle=90, kind="AXIS",
          weight="Bold", gap=14):
    """Rotated label (y-axis names, the wedge caption): drawn on a temporary
    RGBA strip, rotated, pasted centred on `c`."""
    fe = font(px, weight)
    ft = thai_font(thpx) if th else None
    we = d.width(en, fe)
    wt = d.width(th, ft) if th else 0
    tw = we + (gap + wt if th else 0)
    hh = max(px, thpx if th else 0) * 1.4
    tmp = Image.new("RGBA", (int(tw * K) + 8, int(hh * K) + 8), (0, 0, 0, 0))
    td = ImageDraw.Draw(tmp)
    td.text((4, tmp.height / 2), en, font=fe, fill=(*col[:3], 255), anchor="lm")
    if th:
        td.text((4 + (we + gap) * K, tmp.height / 2), th, font=ft, fill=(*col[:3], 255),
                anchor="lm")
    rot = tmp.rotate(angle, expand=True, resample=Image.BICUBIC)
    cx, cy = c
    px0 = int(round(cx * K - rot.width / 2))
    py0 = int(round(cy * K - rot.height / 2))
    d.img.paste(rot, (px0, py0), rot)
    bb = (px0 / K, py0 / K, (px0 + rot.width) / K, (py0 + rot.height) / K)
    d.boxes.append((kind, en + ((" " + th) if th else ""), bb))
    return bb


def L1(s, px=32, col=NAVY):
    return (s, px, "Bold", col, "L1")


def TH(s, px=26, col=NAVY_85):
    return (s, px, "thai", col, "TH")


def L2(s, px=24, col=SLATE):
    return (s, px, "Medium", col, "L2")


def row(s, px, weight="Bold", col=NAVY, kind="L1"):
    return (s, px, weight, col, kind)


def stack(d, cx, cy, rows, maxw=None, gap=6, align="m"):
    """Centred block of lines at (cx, cy). A multi-word row that does not fit
    `maxw` at its size WRAPS (L1 to 2 lines, L2 to 3) before it shrinks, so one
    long label in a row of tiles does not end up smaller than its neighbours.
    align "l" left-aligns every line at cx."""
    resolved = []
    for s, px, weight, col, kind in rows:
        f = face(px, weight, s)
        lines = [s]
        if maxw is not None and d.width(s, f) > maxw:
            limit = 3 if kind == "L2" else 2
            cand = wrap(d, s, f, maxw)
            if 1 < len(cand) <= limit and all(d.width(ln, f) <= maxw for ln in cand):
                lines = cand
            else:
                f, px = fit(d, s, px, weight, maxw,
                            FLOOR_L1 if kind in ("L1", "BAR", "DISC") else FLOOR_L2)
        lh = line_h(px, weight, s)
        resolved.append((lines, f, px, col, kind, lh))
    total = sum(len(ls) * lh + (len(ls) - 1) * lh * 0.12 for ls, _, _, _, _, lh in resolved)
    total += gap * (len(resolved) - 1)
    y = cy - total / 2
    out = []
    for lines, f, px, col, kind, lh in resolved:
        for i, ln in enumerate(lines):
            yc = y + lh / 2
            anchor = "lm" if align == "l" else "mm"
            d.d.text((cx * K, yc * K), ln, font=f, fill=col, anchor=anchor)
            bb = tuple(v / K for v in d.d.textbbox((cx * K, yc * K), ln, font=f, anchor=anchor))
            d.boxes.append((kind, ln, bb))
            out.append(bb)
            y += lh + (lh * 0.12 if i < len(lines) - 1 else 0)
        y += gap
    return out


# --------------------------------------------------------------------------
# components
# --------------------------------------------------------------------------
def tile(d, box, key, l1=None, th=None, l2=None, l1px=None, thpx=26, l2px=24,
         rows=None, solid=False, outline=None, ow=W_HAIR, pad=12, gap=6, r=R_TILE):
    """Tinted rounded rect, 3 px parent-token outline, L1 + Thai gloss (+ L2)
    centred. key "white" = white tile with a navy @40 % outline (or `outline`);
    solid=True fills with the token and sets the text white (Fig 9's MODEL).
    rows=[...] replaces the automatic L1/TH/L2 rows; l1=None draws just the box."""
    x0, y0, x1, y1 = box
    w = x1 - x0
    if solid:
        fill, oc, tc, thc, l2c = TOKENS[key], TOKENS[key], WHITE, WHITE, WHITE
    elif key == "white":
        fill, oc, tc, thc, l2c = WHITE, (outline or NAVY_40), NAVY, NAVY_85, SLATE
    else:
        fill, oc, tc, thc, l2c = TINTS[key], (outline or TOKENS[key]), NAVY, NAVY_85, SLATE
    rr(d, box, r, fill=fill, outline=oc, w=ow)
    if rows is None:
        rows = []
        if l1:
            rows.append(L1(l1, l1px or (36 if w >= 300 else 32), tc))
        if th:
            rows.append(TH(th, thpx, thc))
        if l2:
            rows.append(L2(l2, l2px, l2c))
    if rows:
        stack(d, (x0 + x1) / 2, (y0 + y1) / 2, rows, maxw=w - 2 * pad, gap=gap)
    return box


def bar(d, box, rows, px=34, l2px=26, thpx=26, pad=30, gap=8):
    """Dark core bar: navy r 16, white lines. Strings: line 1 Bold `px` caps,
    later lines Medium `l2px`, Thai lines Sarabun `thpx`. Tuples pass through."""
    x0, y0, x1, y1 = box
    rr(d, box, R_BAR, fill=NAVY)
    rs = []
    for i, s in enumerate(rows):
        if isinstance(s, tuple):
            rs.append(s)
        elif THAI.search(s):
            rs.append((s, thpx, "thai", WHITE, "BAR"))
        elif i == 0:
            rs.append((s, px, "Bold", WHITE, "BAR"))
        else:
            rs.append((s, l2px, "Medium", WHITE, "BAR"))
    return stack(d, (x0 + x1) / 2, (y0 + y1) / 2, rs, maxw=(x1 - x0) - 2 * pad, gap=gap)


def disc(d, c, r, rows, px=36, thpx=28, gap=6):
    """Dark core disc: navy circle, 2-4 centred white lines (Bold `px` /
    Sarabun `thpx`; L2-ish strings in Medium via a tuple row)."""
    cx, cy = c
    ellipse(d, cx, cy, r, r, fill=NAVY)
    rs = []
    for s in rows:
        if isinstance(s, tuple):
            rs.append(s)
        elif THAI.search(s):
            rs.append((s, thpx, "thai", WHITE, "DISC"))
        else:
            rs.append((s, px, "Bold", WHITE, "DISC"))
    return stack(d, cx, cy, rs, maxw=2 * r * 0.82, gap=gap)


NODE_GAP = 3


def _node_avail(rx, ry, px, th):
    """Inner width an L1 line may use inside an rx/ry ellipse: the chord at
    the caps' TOP corners (the line sits above the Thai gloss), less the ring."""
    top = (px / 2 + NODE_GAP / 2 + 0.36 * px) if th else 0.36 * px
    return 2 * (rx * math.sqrt(max(1 - (top / ry) ** 2, 0.01)) - W_RING - 3)


def node_geom(d, l1, px=28, rx=100, ry=55, th=True):
    """(rx, px) a node needs for `l1`: fit() down to the floor first, then widen
    rx if the word still does not clear the ring. Cached so node() and the
    chord pass agree and print once."""
    key = (l1, px, rx, ry, th)
    if key in d._geom:
        return d._geom[key]
    asked, p = px, px
    w = d.width(l1, font(p))
    while w > _node_avail(rx, ry, p, th) and p - 1 >= FLOOR_L1:
        p -= 1
        w = d.width(l1, font(p))
    if p != asked:
        _record_fit(d, l1, asked, p, True)
    if w > _node_avail(rx, ry, p, th):
        top = (p / 2 + NODE_GAP / 2 + 0.36 * p) if th else 0.36 * p
        need = math.ceil((w / 2 + W_RING + 3) / math.sqrt(max(1 - (top / ry) ** 2, 0.01)))
        d.note("node %r: rx %d -> %d (%d px at %d does not clear an rx-%d ring)"
               % (l1, rx, need, w, p, rx))
        rx = need
    d._geom[key] = (rx, p)
    return rx, p


def node(d, c, key, l1, th=None, rx=100, ry=55, px=28, thpx=24, ow=W_RING):
    """White ellipse rx 100 ry 55, 5 px token outline, L1 28 + Sarabun 24."""
    cx, cy = c
    rx, px = node_geom(d, l1, px, rx, ry, bool(th))
    ellipse(d, cx, cy, rx, ry, fill=WHITE, outline=TOKENS[key], w=ow)
    rows = [L1(l1, px)] + ([TH(th, thpx)] if th else [])
    stack(d, cx, cy, rows, maxw=_node_avail(rx, ry, px, bool(th)), gap=NODE_GAP)
    return rx


def ring_points(c, rx, ry, n, start=-90):
    cx, cy = c
    return [(cx + rx * math.cos(math.radians(start + i * 360 / n)),
             cy + ry * math.sin(math.radians(start + i * 360 / n))) for i in range(n)]


def _ellipse_hit(centre, rx, ry, ux, uy):
    """Distance from an ellipse's centre to its boundary along unit (ux, uy)."""
    return 1 / math.sqrt((ux / rx) ** 2 + (uy / ry) ** 2)


def ring_chords(d, pts, rxs, ry, col, w=W_CONN, gap=12):
    """Straight arrows from each node to the next (closing the loop), starting
    `gap` px after the source ring and ending `gap` px before the target ring.
    Draw BEFORE the nodes."""
    n = len(pts)
    for i in range(n):
        (x0, y0), (x1, y1) = pts[i], pts[(i + 1) % n]
        dx, dy = x1 - x0, y1 - y0
        L = math.hypot(dx, dy)
        ux, uy = dx / L, dy / L
        t0 = _ellipse_hit(pts[i], rxs[i], ry, ux, uy) + gap
        t1 = _ellipse_hit(pts[(i + 1) % n], rxs[(i + 1) % n], ry, ux, uy) + gap
        arrow(d, (x0 + ux * t0, y0 + uy * t0), (x1 - ux * t1, y1 - uy * t1), col, w)


def badge(d, c, n, r=26, px=28):
    """Navy disc, white numeral Black 28."""
    cx, cy = c
    ellipse(d, cx, cy, r, r, fill=NAVY)
    return text(d, (cx, cy), str(n), px, "Black", WHITE, kind="BADGE")


def chip(d, xy, key, l1, th=None, w=220, h=90, px=26, thpx=22):
    """220x90 white, 4 px status outline, status dot r 10 at x+26, navy label."""
    x, y = xy
    rr(d, (x, y, x + w, y + h), R_CHIP, fill=WHITE, outline=TOKENS[key], w=4)
    ellipse(d, x + 26, y + h / 2, 10, 10, fill=TOKENS[key])
    rows = [row(l1, px, "Bold", NAVY, "CHIP")]
    if th:
        rows.append((th, thpx, "thai", NAVY_85, "CHIP"))
    stack(d, x + 46, y + h / 2, rows, maxw=w - 46 - 12, gap=2, align="l")
    return (x, y, x + w, y + h)


def arrow(d, p0, p1, col, w=W_CONN, head=None):
    """Straight arrow, solid isosceles head at p1 -- make_cover.arrow's
    construction: head 5.5 x w long, 2.5 x w half-width; a short arrow (a tile
    gap) caps its head at 60 % of its own length so a shaft survives."""
    x0, y0 = p0
    x1, y1 = p1
    L = math.hypot(x1 - x0, y1 - y0)
    if head is None:
        head = min(5.5 * w, 0.6 * L)
    s = head * (2.5 / 5.5)
    ang = math.atan2(y1 - y0, x1 - x0)
    bx, by = x1 - head * math.cos(ang), y1 - head * math.sin(ang)
    line(d, [(x0, y0), (bx, by)], col, w)
    polygon(d, [(x1, y1),
                (bx - s * math.sin(ang), by + s * math.cos(ang)),
                (bx + s * math.sin(ang), by - s * math.cos(ang))], fill=col)


def envelope(d, box, col=CORAL, w=W_EMPH, r=R_ENV):
    """The assurance envelope: coral 6 px rounded rect r 24, no fill."""
    rr(d, box, r, fill=None, outline=col, w=w)


def wedge(d, apex, b0, b1, label, px=22, col=CORAL):
    """Coral filled triangle with a rotated white caps label along its axis."""
    polygon(d, [apex, b0, b1], fill=col)
    mx, my = (b0[0] + b1[0]) / 2, (b0[1] + b1[1]) / 2
    ang = math.degrees(math.atan2(-(apex[1] - my), apex[0] - mx))
    cx, cy = (apex[0] + 2 * mx) / 3, (apex[1] + 2 * my) / 3
    return rtext(d, (cx, cy), label, px=px, col=WHITE, angle=ang, kind="WEDGE")


def axes(d, frame, mx=None, my=None, w=W_FRAME, mid_w=W_FRAME, mid_col=NAVY):
    """4 px navy frame with optional midlines (Fig 3: 2 px NAVY_45; Fig 8: 4 px navy)."""
    x0, y0, x1, y1 = frame
    d.d.rectangle(_sc(frame), outline=NAVY, width=int(round(w * K)))
    if mx is not None:
        line(d, [(mx, y0), (mx, y1)], mid_col, mid_w)
    if my is not None:
        line(d, [(x0, my), (x1, my)], mid_col, mid_w)


# --------------------------------------------------------------------------
# figures -- geometry from Appendix B, labels verbatim
# --------------------------------------------------------------------------
def fig01(d):
    """TALL -- The organizational learning engine: a navy core disc inside a
    ring of seven nodes, chords running clockwise from DATA."""
    C = (700, 500)
    nodes = [("DATA", "ข้อมูล", "blue"), ("CONTEXT", "บริบท", "gold"),
             ("INTELLIGENCE", "ปัญญา", "coral"), ("JUDGMENT", "ดุลพินิจ", "navy"),
             ("ACTION", "การกระทำ", "blue"), ("OUTCOME", "ผลลัพธ์", "gold"),
             ("LEARNING", "การเรียนรู้", "coral")]
    pts = ring_points(C, 470, 330, 7)
    rxs = [node_geom(d, l1)[0] for l1, _, _ in nodes]
    ring_chords(d, pts, rxs, 55, BLUE_LIGHT, W_CONN)
    disc(d, C, 200, ["LEARNING", "VELOCITY", "ความเร็วในการเรียนรู้"], px=36, thpx=28)
    for (l1, th, key), p, rx in zip(nodes, pts, rxs):
        node(d, p, key, l1, th, rx=rx)


def fig02(d):
    """STD -- Five maturity levels (rising blocks, badges 1-5, coral risers).

    The blocks are 220 wide, so the caps labels wrap (level 5 to three lines)
    and the level-1 block, only 200 tall, cannot carry the badge plus a
    two-line L2 note on the +95/+125/+170 ladder: the ladder is tightened to
    +90 / last L1 +30 / Thai +32, which every block shares."""
    base, W, PAD = 760, 220, 8          # 740 in the spec, +20 to balance the card
    maxw = W - 2 * PAD
    xs = [90, 340, 590, 840, 1090]
    tops = [base - h for h in (200, 320, 440, 560, 680)]
    keys = ["gray", "blue", "green", "gold", "coral"]
    l1s = ["AI AS TOOL", "AI IN DECISIONS", "AI IN WORKFLOWS", "AI OPERATING MODEL",
           "AI-FIRST LEARNING SYSTEM"]
    ths = ["AI เป็นเครื่องมือ",
           "AI ในการตัดสินใจ",
           "AI ในกระบวนงาน",
           "รูปแบบดำเนินงานด้วย AI",
           "ระบบเรียนรู้ที่ใช้ AI เป็นแกน"]
    l2s = ["Personal productivity", "Evidence and estimates", "End-to-end redesign",
           "Shared capability", "Compounding adaptation"]
    for i, x in enumerate(xs):
        top, cx = tops[i], x + W / 2
        tile(d, (x, top, x + W, base), keys[i])
        badge(d, (x + 40, top + 40), i + 1)
        y = top + 90
        for ln in wrap(d, l1s[i], font(28), maxw):
            text(d, (cx, y), ln, 28, "Bold", NAVY, kind="L1")
            y += 32
        thpx, lines = 24, None
        for thpx in (24, 23, FLOOR_L2):     # level 4's gloss only wraps inside below 24
            f = thai_font(thpx)
            lines = wrap(d, ths[i], f, maxw)
            if all(d.width(ln, f) <= maxw for ln in lines):
                break
        if thpx != 24:
            d.note("level %d gloss %r set at %d to wrap inside the block" % (i + 1, ths[i], thpx))
        y += 30 - 32                        # Thai gloss 30 under the last caps line
        for ln in lines:
            text(d, (cx, y), ln, thpx, "thai", NAVY_85, kind="TH")
            y += 34                         # Sarabun carries marks: 30 collides
        y += 32 - 34
        for ln in wrap(d, l2s[i], font(22, "Medium"), maxw):
            text(d, (cx, y), ln, 22, "Medium", SLATE, kind="L2")
            y += 24
    for i in range(4):                              # coral risers between block tops
        arrow(d, (xs[i] + W + 6, tops[i] - 10), (xs[i + 1] - 12, tops[i + 1] + 14),
              CORAL, W_CONN)


def fig03(d):
    """TALL -- Decision portfolio: a 2x2 on VALUE x LEARNABILITY with faint
    midlines, four quadrant blocks and five consequence bubbles.

    The three notes the plan could not read were taken off a 300-dpi render of
    PDF page 16: the TRANSFORM blue bubble is `Case routing`, DEFER's is
    `Rare report`, AUTOMATE's is `FAQ draft`.

    `Refund eligibility` is the one note that wraps. Its coral r-48 bubble sits
    at x 1150, so only 128 px separate the bubble's right edge from the frame,
    and the line is 177 px at 22 -- already the floor. It wraps between its two
    words rather than cross the frame it belongs inside."""
    F = (220, 60, 1340, 860)
    axes(d, F, mx=780, my=460, mid_w=2, mid_col=NAVY_45)
    rtext(d, (130, 460), "VALUE", 'คุณค่า')
    mixed(d, (780, 930), "LEARNABILITY", 'ความพร้อมในการเรียนรู้จากผลลัพธ์')
    cells = [(500, 60, "RESEARCH", "High value Low learnability", 'วิจัยและจัดการข้อจำกัด'),
             (1060, 60, "TRANSFORM", "High value High learnability", 'ลงมือแบบเต็มระบบ'),
             (500, 460, "DEFER", "Low value Low learnability", 'ชะลอ'),
             (1060, 460, "AUTOMATE", "Low value High learnability", 'ทำเมื่อใช้ความสามารถช่วยได้')]
    for cx, top, l1, l2, th in cells:
        stack(d, cx, top + 98, [L1(l1, 30), L2(l2), TH(th, 24)], maxw=500)
    bubbles = [(450, 340, 34, "gold", "Executive acquisition"),
               (1150, 300, 48, "coral", "Refund eligibility"),
               (930, 380, 34, "blue", "Case routing"),
               (450, 720, 22, "gray", "Rare report"),
               (1100, 700, 34, "navy", "FAQ draft")]
    for cx, cy, r, key, note in bubbles:
        ellipse(d, cx, cy, r, r, fill=TOKENS[key])
        x = cx + r + 14
        stack(d, x, cy, [row(note, 22, "Medium", SLATE, "L2")], maxw=1328 - x, align="l")
    text(d, (1320, 815), "Bubble size  annual consequence", 22, "Medium", SLATE,
         anchor="rm", kind="L2")


def fig04(d):
    """STD -- Redesign the flow not one task (BEFORE / AFTER lanes).

    The caption sentence the book puts under the AFTER row is not drawn, which
    leaves the spec geometry (y 76-640) high on an 840 canvas: the BEFORE lane
    moves down 92 and the AFTER lane 32, closing the lane gap to 240 and
    centring the card."""
    DY = 92
    text(d, (60, 90 + DY), "BEFORE", 28, "Bold", CORAL, anchor="lm", kind="L1")
    before = [("Intake", "รับเรื่อง", "white"),
              ("Draft", "ร่าง", "white"),
              ("Queue", "รอ", "coral"),
              ("Review", "ตรวจ", "white"),
              ("Queue", "รอ", "coral"),
              ("Approve", "อนุมัติ", "white")]
    for i, (l1, th, key) in enumerate(before):
        x = 100 + 200 * i
        tile(d, (x, 130 + DY, x + 170, 220 + DY), key, l1, th, l1px=32)
        if i < 5:
            arrow(d, (x + 176, 175 + DY), (x + 196, 175 + DY), BLUE_LIGHT, W_CONN)
    text(d, (100, 262 + DY), "Touch time 18 min", 24, "Medium", SLATE, anchor="lm", kind="L2")
    text(d, (340, 262 + DY), "Waiting time 46 h", 24, "Medium", SLATE, anchor="lm", kind="L2")
    DY = 32
    text(d, (60, 470 + DY), "AFTER", 28, "Bold", BLUE, anchor="lm", kind="L1")
    after = [("Digital intake", "รับเรื่องดิจิทัล", "blue"),
             ("Bounded AI assessment", "AI ประเมินในขอบเขต", "green"),
             ("Normal case action", "ดำเนินการกรณีปกติ", "white"),
             ("Exception desk", "โต๊ะจัดการข้อยกเว้น", "gold"),
             ("Outcome evidence", "หลักฐานผลลัพธ์", "coral")]
    for i, (l1, th, key) in enumerate(after):
        x = 100 + 250 * i
        tile(d, (x, 520 + DY, x + 210, 640 + DY), key, l1, th, l1px=30, pad=8, gap=4)
        if i < 4:
            arrow(d, (x + 216, 580 + DY), (x + 244, 580 + DY), BLUE, W_EMPH)


def fig05(d):
    """STD -- Authority must follow consequence (four rows + coral wedge).

    row_px puts the whole left column on one L1 size that keeps every label on
    one line; the wedge caption is set at 20 rather than 22 because at 22 the
    line is 420 px long and its first letter falls below the triangle's base."""
    ys = [150, 310, 470, 630]
    left = [("Suggest", "เสนอแนะ", "green"),
            ("Draft", "ร่าง", "blue"),
            ("Act with approval", "กระทำเมื่ออนุมัติ", "gold"),
            ("Bounded autonomy", "อัตโนมัติในขอบเขต", "coral")]
    right = ["Observe and compare", "Human releases", "Authenticated approval",
             "Hard limits and rollback"]
    px = row_px(d, [l1 for l1, _, _ in left], 30, "Bold", maxw=260)
    for (l1, th, key), r, cy in zip(left, right, ys):
        tile(d, (80, cy - 55, 360, cy + 55), key, l1, th, l1px=px, pad=10)
        arrow(d, (380, cy), (700, cy), BLUE_LIGHT, W_CONN)
        tile(d, (720, cy - 55, 1130, cy + 55), "white", r, l1px=26, outline=BLUE)
    wedge(d, (1250, 80), (1200, 700), (1300, 700),
          "INCREASING EVIDENCE AND CONTROL", px=20)
    text(d, (80, 760), "Default red line  no autonomous irreversible external effects",
         24, "Bold", CORAL, anchor="lm", kind="L2")


def fig06(d):
    """WIDE -- The AI and data factory: two rows of three tiles over the
    shared-assurance core bar. L1 is 32 (not the 36 a >= 300-wide tile would
    default to) because the spec fixes it there and 'CONTEXT SERVICES' at 36
    is 364 px in a 356-px inner width."""
    tiles = [("DATA PRODUCTS", "ผลิตภัณฑ์ข้อมูล", "blue"),
             ("CONTEXT SERVICES", "บริการบริบท", "green"),
             ("MODEL SERVICES", "บริการโมเดล", "gold"),
             ("EVALUATION", "การประเมิน", "coral"),
             ("TOOL REGISTRY", "ทะเบียนเครื่องมือ", "blue"),
             ("OBSERVABILITY", "การสังเกตการณ์", "green")]
    xs = [80, 510, 940]
    for i, (l1, th, key) in enumerate(tiles):
        x, top = xs[i % 3], (70 if i < 3 else 260)
        tile(d, (x, top, x + 380, top + 150), key, l1, th, l1px=32)
    bar(d, (80, 470, 1320, 610),
        ["SHARED ASSURANCE • SECURITY • PRIVACY • FINOPS • GREENOPS",
         "การประกันความเชื่อมั่น ความมั่นคง ความเป็นส่วนตัว ต้นทุน และพลังงาน"],
        px=34)


def fig07(d):
    """STD -- A federated operating model: the platform disc between two
    value-stream tiles feeding in from the left and two obligation tiles
    pushing in from the right.

    L1 is 30, not the 36 a 300-wide tile defaults to: at 36 three of the four
    labels overflow the 276-px inner width and wrap mid-phrase. At 30 only
    'PEOPLE AND CHANGE' wraps, and it wraps between its words."""
    C = (700, 400)
    left = [("VALUE STREAM A", "สายคุณค่า A", "blue", 230),
            ("VALUE STREAM B", "สายคุณค่า B", "green", 570)]
    right = [("RISK AND LEGAL", "ความเสี่ยงและกฎหมาย", "coral", 230),
             ("PEOPLE AND CHANGE", "คนและการเปลี่ยนแปลง", "gold", 570)]
    disc(d, C, 210, ["AI PLATFORM", "AND ASSURANCE", "แพลตฟอร์มและ", "การประกันร่วม"],
         px=34, thpx=28)
    for l1, th, key, cy in left:
        tile(d, (100, cy - 60, 400, cy + 60), key, l1, th, l1px=30, gap=4)
        arrow(d, (420, cy), (560, cy), BLUE, W_EMPH)
    for l1, th, key, cy in right:
        tile(d, (1000, cy - 60, 1300, cy + 60), key, l1, th, l1px=30, gap=4)
        arrow(d, (980, cy), (840, cy), CORAL, W_EMPH)


def fig08(d):
    """TALL -- What is AI-core: a 2x2 on INDISPENSABILITY x DECISION AUTHORITY,
    no cell fills, the AI-core cell framed by the coral envelope."""
    F = (220, 60, 1340, 860)
    axes(d, F, mx=780, my=460)
    rtext(d, (130, 460), "INDISPENSABILITY", "ความจำเป็น")
    mixed(d, (780, 930), "DECISION AUTHORITY", "อำนาจในการตัดสินใจ")
    cw = 560 - 40
    stack(d, 500, 260, [L1("INDISPENSABLE ADVISOR"), TH("ผู้ช่วยที่จำเป็น"),
                        L2("Text release is the effect boundary")], maxw=cw)
    envelope(d, (792, 72, 1328, 448))
    stack(d, 1060, 260, [L1("AI-CORE"), TH("AI เป็นแกนกลาง"),
                         row("Full assurance envelope", 26, "Bold", CORAL, "L2")],
          maxw=cw - 40)
    stack(d, 500, 660, [L1("AI FEATURE"), TH("คุณลักษณะ AI"),
                        L2("Proportionate controls")], maxw=cw)
    stack(d, 1060, 660, [L1("BOUNDED AGENT"), TH("เอเจนต์ในขอบเขต"),
                         L2("Hard effect mediation", col=BLUE)], maxw=cw)


def fig09(d):
    """TALL -- Context is part of the program: the BEHAVIOR disc with eight
    runtime components on spokes, MODEL solid coral because it is one
    component among eight and not the seat of the behaviour.

    ring_points(rx 470, ry 360, 8) reproduces the spec's angle list exactly
    (-90 stepping 45). L1 is 28 with pad 8: 'ORCHESTRATION' is one word 278 px
    wide at 32 and cannot wrap, so it alone shrinks to the 26 floor (a 2-px
    step nobody reads), and 'SYSTEM CONTEXT' wraps between its two words.
    Spokes are drawn first so the disc and the tiles cover their ends."""
    C, R = (700, 500), 190
    tiles = [("MODEL", "โมเดล", "coral", True),
             ("DECODING", "การสุ่ม", "gold", False),
             ("SYSTEM CONTEXT", "บริบทระบบ", "blue", False),
             ("RETRIEVAL", "การค้นคืน", "green", False),
             ("TOOLS", "เครื่องมือ", "coral", False),
             ("MEMORY", "หน่วยความจำ", "blue", False),
             ("ORCHESTRATION", "การประสานงาน", "gold", False),
             ("ENVIRONMENT", "สภาพแวดล้อม", "green", False)]
    pts = ring_points(C, 470, 360, 8)
    for cx, cy in pts:
        ux, uy = cx - C[0], cy - C[1]
        L = math.hypot(ux, uy)
        line(d, [(cx, cy), (C[0] + R * ux / L, C[1] + R * uy / L)], BLUE_LIGHT, W_CONN)
    disc(d, C, R, [])                     # the circle; its rows are two pairs
    for cy, en, th in ((458, "BEHAVIOR", "พฤติกรรม"),
                       (552, "One manifest", "หนึ่งบัญชีรายการ")):
        stack(d, C[0], cy, [row(en, 36, "Bold", WHITE, "DISC"),
                            (th, 28, "thai", WHITE, "DISC")], maxw=2 * R * 0.82)
    for (l1, th, key, solid), (cx, cy) in zip(tiles, pts):
        tile(d, (cx - 120, cy - 55, cx + 120, cy + 55), key, l1, th,
             l1px=28, solid=solid, pad=8, gap=4)


def fig10(d):
    """WIDE -- The five rails inside the assurance envelope, over the trace bar.
    The rail numeral is its own line: '4 EXECUTION' inline does not fit a
    200-px tile at 32, and the row shares one L1 size (row_px)."""
    envelope(d, (60, 60, 1340, 300))
    rails = [("1", "INPUT", "อินพุต", "blue"), ("2", "DIALOG", "บทสนทนา", "green"),
             ("3", "RETRIEVAL", "การค้นคืน", "gold"), ("4", "EXECUTION", "การปฏิบัติการ", "coral"),
             ("5", "OUTPUT", "ผลลัพธ์", "blue")]
    xs = [110, 355, 600, 845, 1090]
    px = row_px(d, [r[1] for r in rails], 32, "Bold", maxw=200 - 24)
    for (n, l1, th, key), x in zip(rails, xs):
        tile(d, (x, 100, x + 200, 260), key,
             rows=[row(n, 28, "Black", NAVY, "NUM"), L1(l1, px), TH(th)], gap=4)
    for x in xs[:-1]:
        arrow(d, (x + 206, 180), (x + 239, 180), BLUE, W_EMPH)
    mixed(d, (700, 345), "ASSURANCE ENVELOPE", "กรอบการประกันความเชื่อมั่น",
          px=28, thpx=26, col=CORAL, kind="L1")
    bar(d, (120, 430, 1280, 580),
        ["RECONSTRUCTABLE TRACE ACROSS EVERY REACHED STAGE",
         "ร่องรอยที่สร้างเหตุการณ์ย้อนหลังได้ในทุกขั้นที่ระบบเดินผ่าน"], px=32)


def fig11(d):
    """STD -- A proposal is not an effect: the MODEL PROPOSAL tile, the navy
    EFFECT GUARD panel carrying its seven checks, the coral BLOCK AND ESCALATE
    tile.

    The panel is a plain navy r-20 rect and not bar(): its rows are pinned to
    the spec's y ladder against a dot column at x 550, not centred as a block.
    The spec fixes the title's y and not its x; the book figure (PDF p36) sets
    it flush with the dot column, so it is left-aligned there rather than
    centred over a left-aligned list."""
    DOT_X, DOT_R = 550, 9
    tile(d, (80, 300, 360, 540), "blue",
         rows=[L1("MODEL", 28), L1("PROPOSAL", 28),
               row("issue_refund", 28, "SemiBold", NAVY, "L1"), L1("THB 2,500", 28)],
         gap=8)
    arrow(d, (380, 420), (480, 420), BLUE, W_EMPH)
    rr(d, (500, 120, 900, 720), 20, fill=NAVY)
    text(d, (DOT_X - DOT_R, 170), "EFFECT GUARD", 30, "Bold", WHITE, anchor="lm",
         kind="L1")
    checks = [("Identity", "ตัวตน"),
              ("Authority", "อำนาจ"),
              ("Schema", "โครงสร้าง"),
              ("Parameters", "ขอบเขต"),
              ("Risk", "ความเสี่ยง"),
              ("Approval", "การอนุมัติ"),
              ("Idempotency", "ไม่ทำซ้ำ")]
    for i, (en, th) in enumerate(checks):
        y = 240 + 70 * i
        ellipse(d, DOT_X, y, DOT_R, DOT_R, fill=BLUE_LIGHT)
        mixed(d, (580, y), en, th, px=26, thpx=24, col=WHITE, anchor="lm",
              kind="ROW", weight="Medium")
    arrow(d, (920, 420), (1020, 420), CORAL, W_EMPH)
    tile(d, (1040, 300, 1320, 540), "coral", ow=4,
         rows=[L1("BLOCK", 28), L1("AND", 28), L1("ESCALATE", 28),
               TH("ระงับและส่งต่อ", 24)],
         gap=8)


def fig12(d):
    """STD -- Evaluation tracks and release gate: five track tiles feeding the
    RELEASE GATE bar, four verdict chips beneath."""
    tracks = [("FIXED", "ชุดตรึง", "blue"), ("HIDDEN", "ชุดซ่อน", "green"),
              ("ADAPTIVE", "ปรับตามระบบ", "coral"), ("STATE FAULT", "ความผิดสถานะ", "gold"),
              ("LIVE", "การใช้งานจริง", "gray")]
    for i, (l1, th, key) in enumerate(tracks):
        x = 100 + 250 * i
        tile(d, (x, 60, x + 210, 210), key, l1, th)
        arrow(d, (x + 105, 230), (x + 105, 330), BLUE_LIGHT, W_CONN)
    bar(d, (100, 350, 1300, 490),
        ["RELEASE GATE", "Utility  Security  Effects  Trace  Operations  Economics  Recovery"],
        px=34)
    verdicts = [("PROMOTE", "ปล่อย", "green"), ("CANARY", "ทดลองจำกัด", "blue"),
                ("HOLD", "ระงับ", "gold"), ("REJECT", "ปฏิเสธ", "coral")]
    for i, (l1, th, key) in enumerate(verdicts):
        chip(d, (170 + 280 * i, 560), key, l1, th)


def fig13(d):
    """TALL -- Incident to improvement: Fig 1's ring with eight nodes, 45 deg
    apart from -90, around the EVIDENCE BEFORE CHANGE core disc. CONTAIN is the
    only --red ring in the series -- the palette reserves the token for it."""
    C = (700, 500)
    nodes = [("DETECT", "ตรวจพบ", "coral"),
             ("CONTAIN", "จำกัดผล", "red"),
             ("PRESERVE", "รักษาหลักฐาน", "gold"),
             ("DIAGNOSE", "วินิจฉัย", "navy"),
             ("REMEDIATE", "แก้ไข", "blue"),
             ("RE-EVALUATE", "ประเมินใหม่", "green"),
             ("RECOVER", "กู้คืน", "blue"),
             ("LEARN", "เรียนรู้", "coral")]
    pts = ring_points(C, 470, 330, 8)
    rxs = [node_geom(d, l1)[0] for l1, _, _ in nodes]
    ring_chords(d, pts, rxs, 55, BLUE_LIGHT, W_CONN)
    disc(d, C, 200, ["EVIDENCE", "BEFORE CHANGE", "เก็บหลักฐาน", "ก่อนแก้ระบบ"],
         px=36, thpx=28)
    for (l1, th, key), p, rx in zip(nodes, pts, rxs):
        node(d, p, key, l1, th, rx=rx)


def fig14(d):
    """STD -- One operating system many obligations: five obligation tiles whose
    lines converge on the organizational evidence bar.

    Fig 12's 210-wide tile cannot hold these labels: 'MEASURE MANAGE' is 233 px
    at Bold 24 against a 186-px inner width, and no five-across row of 210s can
    take it at any size at or above the 22 floor. The tiles are therefore 240
    wide on a 260 pitch (60..1340, gap 20, pad 8) and row_px picks the one size
    at which all fifteen lines fit -- the row stays a row rather than one tile
    shrinking alone. Lines are drawn first so the tiles and the bar cap them.

    Neither the book's panel title nor its footer sentence is drawn, which
    leaves the spec's y ladder (60-640) 200 px short of the 840 canvas' foot
    against 60 at its head: every y moves down DY so the card is centred, the
    same correction Fig 4 makes for the same reason."""
    DY = 70
    tiles = [(["NIST", "GOVERN MAP", "MEASURE MANAGE"], "blue"),
             (["ISO 42001", "MANAGEMENT", "SYSTEM"], "green"),
             (["OECD", "VALUES AND", "ACCOUNTABILITY"], "gold"),
             (["ASEAN ETDA", "REGIONAL AND", "THAI GUIDANCE"], "coral"),
             (["LAW", "JURISDICTION AND", "SECTOR"], "gray")]
    W, PAD = 240, 8
    xs = [60 + 260 * i for i in range(5)]
    px = row_px(d, [ln for lines, _ in tiles for ln in lines], 24, "Bold",
                maxw=W - 2 * PAD, floor=FLOOR_L2)
    for x in xs:
        line(d, [(x + W / 2, 210 + DY), (700, 430 + DY)], BLUE_LIGHT, W_HAIR)
    for (lines, key), x in zip(tiles, xs):
        tile(d, (x, 60 + DY, x + W, 210 + DY), key,
             rows=[L1(ln, px) for ln in lines],
             pad=PAD, gap=6)
    bar(d, (260, 430 + DY, 1140, 640 + DY),
        ["ORGANIZATIONAL EVIDENCE SYSTEM",
         "Inventory  Impact  Contract  Manifest  Evaluation  Trace  Incident",
         "ระบบหลักฐานขององค์กร"],
        px=34)


def fig15(d):
    """STD -- Redesign work at task level: three tall tiles, each an L1 + Thai
    head over a rule, then the scope line and the owner / evidence / escalation
    rows.

    L1 is 34, not the spec's 36: 'HUMAN AUTHORITY' is 367 px at 36 against a
    348-px inner width, and the +60 / +100 ladder leaves no room for it to wrap
    over its Thai gloss, so row_px puts all three heads on one smaller size
    rather than shrinking that tile alone.

    Neither the book's panel title nor its footer sentence is drawn, which
    leaves the spec's y ladder (80-700) 140 px short of the 840 canvas' foot
    against 80 at its head: every y moves down DY, the correction Figs 4 and 14
    make for the same reason.

    The three owner/evidence/escalation rows sit at +390/+460/+530 rather than
    the spec's +330/+400/+470. The spec's ladder leaves 150 px -- a quarter of
    the tile -- empty under the last row, where the book figure (PDF p48) puts
    its rows in the bottom third with a ninth of the tile beneath them; the
    70-px pitch and every other stop on the ladder are unchanged."""
    DY = 30
    cols = [("AUTOMATE", "ทำอัตโนมัติ", "green",
             "Routine measurable bounded"),
            ("AUGMENT", "เสริมมนุษย์", "blue",
             "Creation synthesis preparation"),
            ("HUMAN AUTHORITY",
             "มนุษย์เป็นเจ้าของ", "coral",
             "Ambiguity relationship consequence")]
    rows = [("Owner", "เจ้าของ"),
            ("Evidence", "หลักฐาน"),
            ("Escalation", "การส่งต่อ")]
    W, top = 380, 80 + DY
    px = row_px(d, [l1 for l1, _, _, _ in cols], 36, "Bold", maxw=W - 32)
    for i, (l1, th, key, scope) in enumerate(cols):
        x = 80 + 430 * i
        cx = x + W / 2
        tile(d, (x, top, x + W, top + 620), key)
        text(d, (cx, top + 60), l1, px, "Bold", NAVY, kind="L1")
        text(d, (cx, top + 100), th, 28, "thai", NAVY_85, kind="TH")
        line(d, [(x + 50, top + 150), (x + 330, top + 150)], NAVY, W_HAIR)
        stack(d, cx, top + 210, [L2(scope)], maxw=W - 48)
        for j, (en, tha) in enumerate(rows):
            y = top + 390 + 70 * j
            text(d, (x + 50, y), en, 24, "Bold", NAVY, anchor="lm", kind="ROW")
            text(d, (x + 50 + d.width(en, font(24)) + 14, y), tha, 22, "thai", SLATE,
                 anchor="lm", kind="ROW")


def fig16(d):
    """STD -- The first 180 days: six phase cards, day-range pills, arrows in
    the gaps, the artifact/owner/threshold/stop bar beneath."""
    keys = ["blue", "green", "gold", "coral", "gray", "blue"]
    days = ["0–30", "31–60", "61–90", "91–120", "121–150", "151–180"]
    l1s = ["ALIGN", "DESIGN", "BUILD", "PROVE", "PREPARE", "DECIDE"]
    ths = ["กำหนดทิศ", "ออกแบบ", "สร้าง", "พิสูจน์", "เตรียมขยาย", "ตัดสิน"]
    l2s = ["Outcome and decision", "Workflow and contract", "Minimum safe system",
           "Hidden and adaptive tests", "Operations and adoption", "Scale hold or stop"]
    top = 60
    for i in range(6):
        x = 60 + 220 * i
        cx = x + 90
        tile(d, (x, top, x + 180, top + 500), keys[i])
        rr(d, (cx - 60, top + 30, cx + 60, top + 74), 22, fill=WHITE)
        text(d, (cx, top + 52), days[i], 26, "Bold", CORAL, kind="PILL")
        text(d, (cx, top + 190), l1s[i], 30, "Bold", NAVY, kind="L1", maxw=152)
        text(d, (cx, top + 232), ths[i], 26, "thai", NAVY_85, kind="TH", maxw=152)
        for j, ln in enumerate(wrap(d, l2s[i], font(20, "Medium"), 152)):
            text(d, (cx, top + 330 + j * 26), ln, 20, "Medium", SLATE, kind="L2")
        if i < 5:
            arrow(d, (x + 185, 310), (x + 215, 310), BLUE, 5)
    bar(d, (100, 620, 1300, 760),
        ["Every phase produces an artifact owner threshold and stop condition",
         "ทุกช่วงต้องมีหลักฐาน เจ้าของ เกณฑ์ และเงื่อนไขหยุด"], px=28)


def figa1(d):
    """STRIP -- Masterclass companion map: the 52-minute timeline, eleven marks
    (coral at 00, 24 and 50), minute numerals under the line, labels alternating
    above and below on faint stems.

    A label is wrapped when it does not fit its own slot -- half the distance to
    its neighbour on the same side, or the room left to the inner margin, which
    is what wraps 'Old organization' at x 100. A wrapped label grows AWAY from
    the timeline (the line nearest the axis keeps the spec's y), so its stem
    clears the type by the same 8 px whether it is one line or two."""
    Y, X0, SPAN, LPX = 300, 100, 1200, 24
    above = [(0, "Old organization"), (10, "Decision loop"), (20, "Workflow"),
             (26, "AI factory"), (42, "Work and governance"), (50, "Learning system")]
    below = [(2, "Maturity"), (14, "Decision inventory"), (24, "Oversight"),
             (32, "Operating model"), (47, "Six layers")]
    ts = sorted(t for t, _ in above + below)
    xs = {t: X0 + SPAN * t / 52 for t in ts}

    def slot(t, group):
        """The width this label may take: to its neighbour on its own side, and
        to the inner margin."""
        ks = [k for k, _ in group]
        i = ks.index(t)
        gaps = [abs(xs[ks[j]] - xs[t]) for j in (i - 1, i + 1) if 0 <= j < len(ks)]
        return min(min(gaps) - 16, 2 * (xs[t] - 26), 2 * (d.W - 26 - xs[t]))

    def label(t, s, group, up):
        f = font(LPX, "Medium")
        maxw = slot(t, group)
        lines = wrap(d, s, f, maxw) if d.width(s, f) > maxw else [s]
        shift = (len(lines) - 1) * (LPX + 6) / 2
        x = xs[t]
        line(d, [(x, 288 if up else 312), (x, 160 if up else 410)], NAVY_45, 2)
        stack(d, x, (140 - shift) if up else (430 + shift),
              [row(ln, LPX, "Medium", NAVY, "L2") for ln in lines])

    line(d, [(X0, Y), (1300, Y)], NAVY, W_FRAME)
    for t, s in above:
        label(t, s, above, True)
    for t, s in below:
        label(t, s, below, False)
    for t in ts:
        ellipse(d, xs[t], Y, 12, 12, fill=(CORAL if t in (0, 24, 50) else BLUE))
        text(d, (xs[t], 336), "%02d" % t, 22, "Medium", NAVY, kind="NUM")


def figs1(d):
    """STD -- Six layers and one spine (the pp3-4 table redrawn): six tinted
    bars with the layer name and its Thai gloss on one left-aligned line, and
    the coral assurance spine piercing all six under its navy cap.

    The table's other two columns -- the leadership question and the minimum
    evidence -- stay in the HTML table, so the bar carries only the name. The
    spine is drawn last: over the bars is what 'piercing' looks like."""
    SPINE, layers = 1180, [
        ("Strategy", "กลยุทธ์", "blue"),
        ("Decisions", "การตัดสินใจ", "green"),
        ("Workflows", "กระบวนงาน", "gold"),
        ("AI and data factory",
         "โรงงาน AI และข้อมูล", "coral"),
        ("Operating model",
         "รูปแบบการดำเนินงาน", "gray"),
        ("Learning loop",
         "วงจรการเรียนรู้", "blue")]
    bar(d, (SPINE - 160, 60, SPINE + 160, 170),
        [row("AI-AS-A-CORE", 30, "Bold", WHITE, "L1"),
         row("ASSURANCE SPINE", 30, "Bold", WHITE, "L1")], pad=14, gap=4)
    for i, (l1, th, key) in enumerate(layers):
        y0 = 200 + 100 * i
        rr(d, (60, y0, 1340, y0 + 80), R_TILE, fill=TINTS[key], outline=TOKENS[key],
           w=W_HAIR)
        text(d, (100, y0 + 40), l1, 32, "Bold", NAVY, anchor="lm", kind="L1")
        text(d, (100 + d.width(l1, font(32)) + 16, y0 + 40), th, 26, "thai", NAVY_85,
             anchor="lm", kind="TH")
    rr(d, (SPINE - 8, 170, SPINE + 8, 792), 8, fill=CORAL)


def figs2(d):
    """STD -- The board scorecard (the p4 table redrawn): the six dimensions as
    upright header tiles over the read-together bar.

    The tiles carry the English name alone. The book gives no Thai gloss for
    these six -- its Thai track names them in English ('Value เทียบ Baseline,
    Quality แยกตามกลุ่มกรณี ...') -- and inventing six is not this
    script's job, so the Thai the spec does supply is in the core bar. The
    indicators under each heading stay in the HTML table.

    The row shares one L1 size (row_px): 'ECONOMICS' is 200 px at 32 against a
    180-px inner width, so all six are set at 28.

    Each tile drops a 4 px --blue-light arrow into the bar, Fig 12's connector
    at Fig 12's length (100 px, here 440 -> 510). Without them the tiles and the
    bar are two unrelated groups floating on the card; with them the figure says
    what the table says -- the six are read into one view."""
    cols = [("VALUE", "blue"), ("QUALITY", "green"), ("RISK", "gold"),
            ("PEOPLE", "coral"), ("LEARNING", "gray"), ("ECONOMICS", "blue")]
    W, PAD = 200, 10
    px = row_px(d, [l1 for l1, _ in cols], 32, "Bold", maxw=W - 2 * PAD)
    for i, (l1, key) in enumerate(cols):
        x = 60 + 216 * i
        tile(d, (x, 180, x + W, 420), key, l1, l1px=px, pad=PAD)
        arrow(d, (x + W / 2, 440), (x + W / 2, 510), BLUE_LIGHT, W_CONN)
    bar(d, (60, 530, 1340, 670),
        ["Read together • No single composite score",
         "อ่านร่วมกัน ห้ามยุบเป็นคะแนนเดียว"], px=34)


FIGS = {
    "01-learning-engine": ("TALL", fig01),
    "02-maturity-levels": ("STD", fig02),
    "03-decision-portfolio": ("TALL", fig03),
    "04-redesign-the-flow": ("STD", fig04),
    "05-authority-ladder": ("STD", fig05),
    "06-ai-data-factory": ("WIDE", fig06),
    "07-federated-model": ("STD", fig07),
    "08-ai-core-matrix": ("TALL", fig08),
    "09-context-as-program": ("TALL", fig09),
    "10-five-rails": ("WIDE", fig10),
    "11-proposal-not-effect": ("STD", fig11),
    "12-release-gate": ("STD", fig12),
    "13-incident-loop": ("TALL", fig13),
    "14-one-evidence-system": ("STD", fig14),
    "15-task-level-redesign": ("STD", fig15),
    "16-first-180-days": ("STD", fig16),
    "a1-masterclass-map": ("STRIP", figa1),
    "s1-six-layers": ("STD", figs1),
    "s2-board-scorecard": ("STD", figs2),
}


def out_path(name):
    return OUT / (PREFIX + name + ".png")


# --------------------------------------------------------------------------
# render + save + validate
# --------------------------------------------------------------------------
def render(name):
    """Draw one figure in memory. Raises NotImplementedError for a stub."""
    size_key, fn = FIGS[name]
    d = Fig(name, size_key)
    fn(d)
    return d


def finish(d):
    return d.img.resize((d.W, d.H), Image.LANCZOS)


def save(d, path):
    """RGB at 2x -> LANCZOS -> palette PNG (128 colours; 96 if over KB_FAIL)."""
    im = finish(d)
    kb, colors = 0.0, COLORS
    for colors in (COLORS, COLORS_FALLBACK):
        q = im.quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
        q.save(path, "PNG", optimize=True)
        kb = path.stat().st_size / 1024
        if kb <= KB_FAIL:
            break
    return kb, colors


def _overlap(a, b):
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def validate(d):
    """(fails, warns) for one rendered canvas: every text bbox inside the
    inner margin, no two L1 boxes overlapping (any other overlap warns), no
    fit that failed at its floor."""
    fails, warns = [], []
    lim = (INNER, INNER, d.W - INNER, d.H - INNER)
    for kind, s, bb in d.boxes:
        if bb[0] < lim[0] or bb[1] < lim[1] or bb[2] > lim[2] or bb[3] > lim[3]:
            fails.append("%s %r bbox (%.0f,%.0f,%.0f,%.0f) crosses the %d-px inner margin"
                         % (kind, s, *bb, INNER))
    for i in range(len(d.boxes)):
        for j in range(i + 1, len(d.boxes)):
            ka, sa, ba = d.boxes[i]
            kb_, sb, bb = d.boxes[j]
            if _overlap(ba, bb):
                msg = "%s %r overlaps %s %r" % (ka, sa, kb_, sb)
                (fails if ka == "L1" and kb_ == "L1" else warns).append(msg)
    for s, asked, got, ok in d.fits:
        if not ok:
            fails.append("fit: %r could not fit at floor (%d -> %d)" % (s, asked, got))
        else:
            warns.append("fit: %r %d -> %d" % (s, asked, got))
    return fails, warns


# --------------------------------------------------------------------------
# --check: registry, fonts, contrast
# --------------------------------------------------------------------------
def _lum(rgb):
    def ch(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgb[:3]
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def contrast(fg, bg):
    a, b = _lum(fg), _lum(bg)
    return (max(a, b) + 0.05) / (min(a, b) + 0.05)


def composite(rgba, bg):
    if len(rgba) == 3:
        return rgba
    a = rgba[3] / 255
    return tuple(int(round(rgba[i] * a + bg[i] * (1 - a))) for i in range(3))


def contrast_table():
    grounds = [("white", WHITE)] + [("%s tint" % k, TINTS[k]) for k in TINT_A]
    inks = [("navy", NAVY), ("navy @85%", NAVY_85), ("slate-light", SLATE),
            ("blue", BLUE), ("coral", CORAL)]
    print("\ncontrast (WCAG; text needs >= 4.5, PASS/large/FAIL):")
    print("  %-12s" % "" + "".join("%12s" % g for g, _ in grounds))
    for iname, ink in inks:
        cells = []
        for _, g in grounds:
            c = contrast(composite(ink, g), g)
            cells.append("%5.1f %-6s" % (c, "PASS" if c >= 4.5 else ("large" if c >= 3 else "FAIL")))
        print("  %-12s" % iname + "".join("%12s" % c for c in cells))
    c = contrast(WHITE, NAVY)
    print("  %-12s%12s   (core bar / disc / badge)" % ("white/navy", "%5.1f %-6s" % (c, "PASS" if c >= 4.5 else "FAIL")))


def check_registry():
    bad = []
    for name, (size_key, fn) in FIGS.items():
        if size_key not in SIZES:
            bad.append("%s: unknown size %r" % (name, size_key))
        if not callable(fn):
            bad.append("%s: drawing function is not callable" % name)
    outs = [out_path(n).name for n in FIGS]
    if len(set(outs)) != len(outs):
        bad.append("two figures write the same file")
    if len(FIGS) != 19:
        bad.append("registry has %d figures, the series needs 19" % len(FIGS))
    for f in ("Inter-var.ttf", "Sarabun-Regular.ttf"):
        if not (FONTS / f).exists():
            bad.append("missing font scripts/fonts/%s" % f)
    if (FONTS / "Inter-var.ttf").exists():
        names = {n.decode() if isinstance(n, bytes) else n
                 for n in ImageFont.truetype(str(FONTS / "Inter-var.ttf"), 20).get_variation_names()}
        for w in ("Medium", "SemiBold", "Bold", "Black"):
            if w not in names:
                bad.append("Inter-var.ttf has no named instance %r" % w)
    return bad


# --------------------------------------------------------------------------
# review sheets
# --------------------------------------------------------------------------
def _thumbs(width):
    out = []
    for name in FIGS:
        p = out_path(name)
        if not p.exists():
            continue
        im = Image.open(p).convert("RGB")
        out.append((name, im.resize((width, int(round(im.height * width / im.width))),
                                    Image.LANCZOS)))
    return out


def contact_sheet(cols=3, cell_w=420, pad=16):
    thumbs = _thumbs(cell_w)
    rows = [thumbs[i:i + cols] for i in range(0, len(thumbs), cols)]
    heights = [max(t.height for _, t in r) for r in rows]
    sheet = Image.new("RGB", (cols * (cell_w + pad) + pad, sum(heights) + pad * (len(rows) + 1)),
                      CREAM)
    y = pad
    for r, h in zip(rows, heights):
        for i, (_, t) in enumerate(r):
            sheet.paste(t, (pad + i * (cell_w + pad), y))
        y += h + pad
    SHEETS.mkdir(exist_ok=True)
    out = SHEETS / "figures-contact.jpg"
    sheet.save(out, "JPEG", quality=88, optimize=True)
    print("contact sheet: %s (%d figures, %.0f KB)"
          % (out.relative_to(ROOT), len(thumbs), out.stat().st_size / 1024))
    return out


def phone_sheet(width=335, pad=12):
    thumbs = _thumbs(width)
    sheet = Image.new("RGB", (width + 2 * pad, sum(t.height for _, t in thumbs) + pad * (len(thumbs) + 1)),
                      CREAM)
    y = pad
    for _, t in thumbs:
        sheet.paste(t, (pad, y))
        y += t.height + pad
    SHEETS.mkdir(exist_ok=True)
    out = SHEETS / "figures-phone.jpg"
    sheet.save(out, "JPEG", quality=88, optimize=True)
    print("phone sheet: %s (%d figures at %d px, %.0f KB)"
          % (out.relative_to(ROOT), len(thumbs), width, out.stat().st_size / 1024))
    return out


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------
def resolve(name):
    if name in FIGS:
        return name
    hits = [n for n in FIGS if n.startswith(name)]
    return hits[0] if len(hits) == 1 else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name", nargs="?")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--contact", action="store_true")
    ap.add_argument("--phone", action="store_true")
    a = ap.parse_args()

    bad = check_registry()
    if bad:
        print("FIGS FAILED %d check(s):" % len(bad))
        for b in bad:
            print("  x", b)
        return 1

    if a.check:
        print("FIGS OK -- %d figures, %d sizes, fonts present" % (len(FIGS), len(SIZES)))
        nfail = 0
        for name in FIGS:
            print("\n" + name)
            try:
                d = render(name)
            except NotImplementedError:
                print("  SKIP (stub)")
                continue
            fails, warns = validate(d)
            for w in warns:
                print("  !", w)
            for f in fails:
                print("  x", f)
            print("  %s -- %d text boxes, %d fit warning(s), %d note(s)"
                  % ("FAIL" if fails else "OK", len(d.boxes),
                     sum(1 for w in warns if w.startswith("fit")), len(d.notes)))
            nfail += bool(fails)
        contrast_table()
        return 1 if nfail else 0
    if a.contact:
        contact_sheet()
        return 0
    if a.phone:
        phone_sheet()
        return 0

    if a.all:
        todo = list(FIGS)
    else:
        n = resolve(a.name or "")
        if not n:
            print("no such figure: %r (use --all; ids: %s)" % (a.name, ", ".join(FIGS)))
            return 2
        todo = [n]

    OUT.mkdir(exist_ok=True)
    worst, total, fails, drawn = 0.0, 0.0, 0, 0
    for name in todo:
        try:
            d = render(name)
        except NotImplementedError:
            print("%-46s SKIP (stub)" % out_path(name).name)
            continue
        kb, colors = save(d, out_path(name))
        line_ = "%-46s %dx%d %5.0f KB" % (out_path(name).name, d.W, d.H, kb)
        if colors != COLORS:
            line_ += "  (%d colours)" % colors
        if kb > KB_FAIL:
            line_ += "  OVER BUDGET"
            fails += 1
        elif kb > KB_WARN:
            line_ += "  (warn)"
        vf, _ = validate(d)
        if vf:
            line_ += "  CHECK FAILED"
            fails += 1
        print(line_)
        for f in vf:
            print("  x", f)
        worst = max(worst, kb)
        total += kb
        drawn += 1
    print("\n%d figures drawn, %d stubs skipped  |  worst %.0f KB (warn >%d, fail >%d)  |  %.0f KB total"
          % (drawn, len(todo) - drawn, worst, KB_WARN, KB_FAIL, total))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
