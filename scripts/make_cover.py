#!/usr/bin/env python3
"""Draw every blog cover in the house visual language, from one spec table.

WHY THIS EXISTS
---------------
Round 1 (2026-08-26) replaced 35 AI clip-art covers with one drawn system. It
fixed the weight (4.1 MB -> 1.5 MB) and the sameness of the clip art, but it
introduced a sameness of its own: five generic motifs, four grounds, and every
shape drawn in the SAME faint grey -- fill at alpha 16-26, outline at 90-120.
The only saturated ink on any cover was the gold eyebrow. Six covers side by
side read as one cover. The owner said so, with screenshots.

Round 2 -- this file -- keeps the spec-table architecture and throws away the
generic vocabulary. Two changes:

  1. ONE MOTIF PER POST. 37 named drawings, not 5 shapes with parameters. The
     picture IS the subject: Kubernetes is a helm wheel steering hex pods, the
     testing pyramid is a pyramid, Docker-vs-VMs is the only split frame on the
     page. Where two posts share territory (3 memory posts, 3 testing posts,
     2 Docker posts, 4 pipeline posts) the shapes are deliberately different --
     see the `vs` note on each function.

  2. REAL COLOUR. Each series gets its own world, and DevOps additionally gets
     a per-cluster accent so 24 blueprints do not blur:

     OpenClaw (13) -- violet poster on light paper. Filled violet pictograms,
     navy line, gold detail. Grid drops to near-nothing.
     DevOps (24)   -- cyanotype blueprint on navy. White line-work, grid kept
     as the blueprint texture, one CLUSTER ACCENT as the lit ink.

WHY THAT LIGHT/DARK SPLIT AND NOT THE OTHER WAY ROUND
-----------------------------------------------------
It is forced, not chosen. A cover sits inside its post's hero, so it may not
share the hero's tone or it vanishes (this site shipped a teal cover on a teal
hero once). Posts have exactly two hero families: OpenClaw = Deep Blue (dark),
DevOps = Sunrise (light). So OpenClaw covers must be LIGHT and DevOps covers
must be DARK. FORBIDDEN below is that rule; check() enforces it against the
post's real HTML, not a second table that could drift.

    python3 scripts/make_cover.py --all          # redraw all 37 + share cards
    python3 scripts/make_cover.py openclaw-101   # one, by slug
    python3 scripts/make_cover.py --check        # validate the table, draw nothing
    python3 scripts/make_cover.py --contact      # 37-up contact sheet for review

THE SPEC TABLE
--------------
`scripts/covers.tsv` is the single source of truth: one row per post,
`slug | out | motif | ground | accent | eyebrow | title | thai | opts`.
Adding a post means adding a row and one motif function.

TWO RULES THE CHECKER ENFORCES
------------------------------
1. A cover's ground may never be its post's own hero family.
2. Everything that carries meaning stays inside the SAFE BAND, y in
   [0.20, 0.80] and x in [0.12, 0.88]. blog/index.html crops covers to 16:10
   and to a 96px square on phones.

MOTIF GEOMETRY
--------------
Every motif is handed a box and must fill it at BOTH aspect ratios it is asked
for: ~2.6:1 on the square cover, ~2.0:1 on the share card. So motifs size their
figures from the box HEIGHT and place them across the WIDTH -- never assume a
square. The helpers below all take explicit centres and radii for that reason.
"""
import argparse
import csv
import math
import pathlib
import re
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = pathlib.Path(__file__).resolve().parents[1]
FONTS = pathlib.Path(__file__).resolve().parent / "fonts"
TABLE = pathlib.Path(__file__).resolve().parent / "covers.tsv"
OUT = ROOT / "images"

S = 1600                      # drawn at 2x, downsampled -- keeps type crisp
FINAL = 800                   # every existing cover is 800x800; do not churn 74 <img> tags
OG = (1200, 630)              # share card, re-laid rather than cropped
KB_FAIL = 90
KB_WARN = 60

BAND_Y = (0.20, 0.80)
BAND_X = (0.12, 0.88)

GOLD = (196, 164, 108)        # --gold
GOLD_DARK = (122, 95, 34)     # --gold-dark
NAVY = (17, 48, 75)           # --navy
SLATE = (82, 97, 116)         # --slate-light
WHITE = (255, 255, 255)
VIOLET = (139, 92, 246)       # --purple
VIOLET_DEEP = (124, 58, 237)  # --purple-dark

GROUNDS = {
    "navy":      ("flat", (0x11, 0x30, 0x4b)),
    "deep":      ("grad", [(0.0, (0x11, 0x30, 0x4b)), (0.45, (0x1a, 0x4d, 0x7a)),
                           (1.0, (0x22, 0x62, 0x99))]),
    "cloud":     ("flat", (0xde, 0xe7, 0xe6)),
    "parchment": ("flat", (0xe9, 0xe1, 0xc4)),
    "cream":     ("flat", (0xfa, 0xf7, 0xf0)),
}
DARK_GROUNDS = {"navy", "deep"}
FORBIDDEN = {"sunrise": {"cloud", "parchment", "cream"}, "deepblue": {"navy", "deep"}}

# DevOps cluster accents. Every value is a :root token -- no seventh status
# colour is invented. The cluster, not the post, picks the colour: readers learn
# "green means testing" across three covers without being told.
ACCENTS = {
    "violet": VIOLET,             # OpenClaw (all 13)
    "gray":   (148, 163, 184),    # fundamentals   --gray
    "cyan":   (6, 182, 212),      # containers     --cyan
    "amber":  (245, 158, 11),     # ci/cd          --amber
    "green":  (34, 197, 94),      # testing        --green
    "blue":   (73, 146, 185),     # infra/cloud    --blue-light
    "teal":   (20, 184, 166),     # reliability
    "red":    (239, 68, 68),      # security       --red
    "gold":   GOLD,               # vibe coding
}


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
# grounds + ink
# --------------------------------------------------------------------------
def ground(name, size):
    kind, spec = GROUNDS[name]
    w, h = size
    if kind == "flat":
        return Image.new("RGB", size, spec)
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


def ink(g, accent):
    """Colour follows from ground + accent, so a row cannot pick an unreadable
    combination by hand.

    Semantic keys, so one motif function draws correctly in both series:
      ln   structural stroke        hi   the highlight -- "this is the point"
      fill faint body fill          hif  highlight fill (semi-transparent)
      gold detail accent           dimf  inactive/background body
    """
    dark = g in DARK_GROUNDS
    acc = ACCENTS.get(accent, VIOLET)
    kind, spec = GROUNDS[g]
    bg = spec if kind == "flat" else spec[len(spec) // 2][1]
    if dark:
        # blueprint: white line-work, the cluster accent as the lit ink
        return {
            "title": WHITE, "eyebrow": GOLD, "thai": (255, 255, 255, 190),
            "rule": GOLD, "grid": (255, 255, 255, 22),
            "ln": (255, 255, 255, 215), "ln2": (255, 255, 255, 120),
            "fill": (255, 255, 255, 24), "dimf": (255, 255, 255, 14),
            "hi": acc, "hif": (*acc, 80), "gold": GOLD, "chip": (*acc, 235),
            "chiptx": (13, 27, 42), "bg": bg,
        }
    # poster: filled violet pictograms, navy line, gold detail
    return {
        "title": NAVY, "eyebrow": GOLD_DARK, "thai": (*SLATE, 255),
        "rule": GOLD_DARK, "grid": (*NAVY, 10),
        "ln": (*NAVY, 210), "ln2": (*NAVY, 110),
        "fill": (*NAVY, 20), "dimf": (*NAVY, 12),
        "hi": acc, "hif": (*acc, 90), "gold": GOLD_DARK, "chip": (*acc, 255),
        "chiptx": WHITE, "bg": bg,
    }


# --------------------------------------------------------------------------
# drawing helpers -- shared by the 37 motifs
# --------------------------------------------------------------------------
def rr(d, box, r, fill=None, outline=None, w=6):
    d.rounded_rectangle([box[0], box[1], box[2], box[3]], radius=int(r),
                        fill=fill, outline=outline, width=int(w))


def arrow(d, p0, p1, col, w=7, head=24):
    """Straight arrow with a solid head at p1."""
    x0, y0 = p0
    x1, y1 = p1
    ang = math.atan2(y1 - y0, x1 - x0)
    bx, by = x1 - head * math.cos(ang), y1 - head * math.sin(ang)
    d.line([(x0, y0), (bx, by)], fill=col, width=int(w))
    s = head * 0.55
    d.polygon([(x1, y1),
               (bx - s * math.sin(ang), by + s * math.cos(ang)),
               (bx + s * math.sin(ang), by - s * math.cos(ang))], fill=col)


def poly(cx, cy, r, n, rot=0.0, squash=1.0):
    return [(cx + r * math.cos(rot + i * 2 * math.pi / n),
             cy + r * squash * math.sin(rot + i * 2 * math.pi / n)) for i in range(n)]


def hexa(d, cx, cy, r, fill=None, outline=None, w=6):
    d.polygon(poly(cx, cy, r, 6, math.pi / 6), fill=fill, outline=outline, width=int(w))


def circ(d, cx, cy, r, fill=None, outline=None, w=6):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill, outline=outline, width=int(w))


def cyl(d, cx, cy, rw, h, c, lit=False):
    """Database cylinder: two ellipses and a body."""
    er = rw * 0.34
    body = c["hif"] if lit else c["fill"]
    d.rectangle([cx - rw, cy - h / 2, cx + rw, cy + h / 2], fill=body)
    d.ellipse([cx - rw, cy + h / 2 - er, cx + rw, cy + h / 2 + er],
              fill=body, outline=c["hi"] if lit else c["ln"], width=6)
    d.line([(cx - rw, cy - h / 2), (cx - rw, cy + h / 2)], fill=c["hi"] if lit else c["ln"], width=6)
    d.line([(cx + rw, cy - h / 2), (cx + rw, cy + h / 2)], fill=c["hi"] if lit else c["ln"], width=6)
    d.ellipse([cx - rw, cy - h / 2 - er, cx + rw, cy - h / 2 + er],
              fill=body, outline=c["hi"] if lit else c["ln"], width=6)


def gear(d, cx, cy, r, col, teeth=8, w=7):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=int(w))
    d.ellipse([cx - r * 0.42, cy - r * 0.42, cx + r * 0.42, cy + r * 0.42],
              outline=col, width=int(w * 0.8))
    for i in range(teeth):
        a = i * 2 * math.pi / teeth
        d.line([(cx + r * math.cos(a), cy + r * math.sin(a)),
                (cx + r * 1.3 * math.cos(a), cy + r * 1.3 * math.sin(a))],
               fill=col, width=int(w))


def label(d, cx, cy, text, col, px, weight="Black"):
    d.text((cx, cy), text, font=font(int(px), weight), fill=col, anchor="mm")


def server(d, cx, cy, w_, h_, c, lit=False):
    """A little rack: three slots."""
    col = c["hi"] if lit else c["ln"]
    rr(d, (cx - w_ / 2, cy - h_ / 2, cx + w_ / 2, cy + h_ / 2), h_ * 0.12,
       fill=c["hif"] if lit else c["fill"], outline=col, w=6)
    for i in range(3):
        y = cy - h_ / 2 + h_ * (0.28 + i * 0.22)
        d.line([(cx - w_ * 0.3, y), (cx + w_ * 0.22, y)], fill=col, width=5)


# --------------------------------------------------------------------------
# OpenClaw motifs -- violet posters, light ground
# --------------------------------------------------------------------------
def oc_os(d, b, c, o):
    """Chatbot becomes an operating system: small bubble -> arrow -> big hex core
    with orbiting tool glyphs.  vs oc_team's org chart."""
    x0, y0, x1, y1 = b
    h = y1 - y0
    cy = (y0 + y1) / 2
    bw, bh = h * 0.55, h * 0.42
    bx = x0 + bw * 0.55
    rr(d, (bx - bw / 2, cy - bh / 2, bx + bw / 2, cy + bh / 2), bh * 0.3,
       fill=c["fill"], outline=c["ln"], w=6)
    d.polygon([(bx - bw * 0.18, cy + bh / 2), (bx + bw * 0.02, cy + bh / 2),
               (bx - bw * 0.22, cy + bh * 0.85)], fill=c["ln"])
    r = h * 0.42
    hx = x1 - r * 1.5
    arrow(d, (bx + bw * 0.62, cy), (hx - r * 1.25, cy), c["gold"], 8, 28)
    for i in range(6):
        a = i * math.pi / 3 + math.pi / 12
        circ(d, hx + r * 1.42 * math.cos(a), cy + r * 1.42 * math.sin(a),
             h * 0.075, fill=c["hif"], outline=c["hi"], w=4)
    hexa(d, hx, cy, r, fill=c["hi"], outline=None)
    hexa(d, hx, cy, r * 0.52, fill=None, outline=(255, 255, 255, 220), w=7)


def oc_team(d, b, c, o):
    """Org chart: one lead over three specialists.  vs oc_integrations' radial hub."""
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    cx = (x0 + x1) / 2
    lw, lh = min(w * 0.26, h * 1.05), h * 0.3
    rr(d, (cx - lw / 2, y0, cx + lw / 2, y0 + lh), lh * 0.32, fill=c["hi"], outline=None)
    label(d, cx, y0 + lh / 2, "AI", WHITE, lh * 0.5)
    kw = min(w * 0.2, h * 0.72)
    ky = y1 - h * 0.3
    xs = [cx - w * 0.3, cx, cx + w * 0.3]
    for kx in xs:
        d.line([(cx, y0 + lh + 6), (kx, ky - 8)], fill=c["ln2"], width=6)
    for kx in xs:
        rr(d, (kx - kw / 2, ky, kx + kw / 2, ky + h * 0.3), h * 0.09,
           fill=c["hif"], outline=c["hi"], w=6)


def oc_memory(d, b, c, o):
    """Three solid layers with a magnifier ON them -- semantic search over
    layered memory.  vs oc_memarch's labelled cross-section, oc_jarvis' brain."""
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    pw = w * 0.6
    ph = h * 0.24
    for i in range(3):
        x = x0 + i * w * 0.05
        y = y0 + i * (h - ph) / 2
        rr(d, (x, y, x + pw, y + ph), ph * 0.34,
           fill=c["hi"] if i == 2 else c["hif"], outline=None)
    r = h * 0.32
    mx, my = x1 - r * 1.35, y0 + h * 0.42
    circ(d, mx, my, r, fill=None, outline=c["ln"], w=9)
    d.line([(mx + r * 0.72, my + r * 0.72), (mx + r * 1.5, my + r * 1.5)],
           fill=c["ln"], width=12)


def oc_security(d, b, c, o):
    """Shield with keyhole inside sandbox brackets.  vs dv_secpipe's padlock and
    dv_auth's door."""
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    cx = (x0 + x1) / 2
    sw = min(w * 0.3, h * 0.86)
    top, bot = y0 + h * 0.04, y1 - h * 0.04
    d.polygon([(cx - sw / 2, top + h * 0.06), (cx, top),
               (cx + sw / 2, top + h * 0.06), (cx + sw / 2, top + h * 0.46),
               (cx, bot), (cx - sw / 2, top + h * 0.46)], fill=c["hi"])
    kr = sw * 0.15
    circ(d, cx, top + h * 0.38, kr, fill=WHITE)
    d.polygon([(cx - kr * 0.62, top + h * 0.42), (cx + kr * 0.62, top + h * 0.42),
               (cx + kr * 0.34, top + h * 0.6), (cx - kr * 0.34, top + h * 0.6)], fill=WHITE)
    for s in (-1, 1):
        bx = cx + s * w * 0.28
        d.line([(bx - s * h * 0.14, top), (bx, top), (bx, bot), (bx - s * h * 0.14, bot)],
               fill=c["gold"], width=9, joint="curve")


def oc_integrations(d, b, c, o):
    """One hub, six named services on spokes.  vs oc_team's top-down chart."""
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    R = min(w * 0.32, h * 0.52)
    for i in range(6):
        a = i * math.pi / 3 + math.pi / 6
        ex, ey = cx + R * 1.55 * math.cos(a), cy + R * math.sin(a)
        d.line([(cx, cy), (ex, ey)], fill=c["ln2"], width=6)
        rr(d, (ex - h * 0.13, ey - h * 0.13, ex + h * 0.13, ey + h * 0.13),
           h * 0.05, fill=c["hif"], outline=c["hi"], w=5)
    circ(d, cx, cy, h * 0.24, fill=c["hi"], outline=None)
    circ(d, cx, cy, h * 0.11, fill=WHITE)


def oc_skills(d, b, c, o):
    """A new tile being placed into the grid -- teaching = adding a capability.
    vs any plain grid: one tile is OUTSIDE, mid-flight, with an arrow."""
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    cols, rows = 4, 2
    gx, gy = w * 0.028, h * 0.1
    tw = (w * 0.66 - gx * (cols - 1)) / cols
    th = (h - gy) / rows
    for r in range(rows):
        for cc in range(cols):
            x, y = x0 + cc * (tw + gx), y0 + r * (th + gy)
            rr(d, (x, y, x + tw, y + th), th * 0.24,
               fill=c["hif"] if (r + cc) % 3 == 0 else c["fill"],
               outline=c["hi"] if (r + cc) % 3 == 0 else c["ln2"], w=5)
    nx = x1 - tw * 0.62
    ny = y0 + h * 0.5 - th / 2
    arrow(d, (nx - tw * 0.5, y0 + h * 0.5), (x0 + w * 0.7, y0 + h * 0.5), c["gold"], 8, 26)
    rr(d, (nx, ny, nx + tw, ny + th), th * 0.24, fill=c["hi"], outline=None)
    label(d, nx + tw / 2, ny + th / 2, "+", WHITE, th * 0.8)


def oc_production(d, b, c, o):
    """Rocket on a rack platform, gauges beside.  vs dv_deploy, which FORKS to
    three pads; this one LAUNCHES from one."""
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    cx = x0 + w * 0.26
    rw = min(w * 0.075, h * 0.19)
    top = y0 + h * 0.02
    nose = top + h * 0.34
    body_b = y1 - h * 0.26
    d.polygon([(cx, top), (cx + rw, nose), (cx - rw, nose)], fill=c["hi"])
    d.rectangle([cx - rw, nose, cx + rw, body_b], fill=c["hi"])
    d.polygon([(cx - rw, body_b - h * 0.2), (cx - rw * 2.3, body_b),
               (cx - rw, body_b)], fill=c["hif"])
    d.polygon([(cx + rw, body_b - h * 0.2), (cx + rw * 2.3, body_b),
               (cx + rw, body_b)], fill=c["hif"])
    circ(d, cx, nose + h * 0.14, rw * 0.5, fill=WHITE)
    d.polygon([(cx - rw * 0.55, body_b), (cx + rw * 0.55, body_b),
               (cx, body_b + h * 0.16)], fill=c["gold"])
    rr(d, (cx - rw * 2.8, body_b + h * 0.18, cx + rw * 2.8, y1), h * 0.05,
       fill=c["fill"], outline=c["ln"], w=6)
    for i in range(3):
        gx_ = x0 + w * 0.66 + i * w * 0.14
        circ(d, gx_, (y0 + y1) / 2, h * 0.16, fill=None, outline=c["ln"], w=6)
        a = -2.3 + i * 0.75
        d.line([(gx_, (y0 + y1) / 2),
                (gx_ + h * 0.12 * math.cos(a), (y0 + y1) / 2 + h * 0.12 * math.sin(a))],
               fill=c["gold"], width=6)


def oc_migration(d, b, c, o):
    """Two machines and an ARC of carried boxes -- the only arc on the page."""
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    sw, sh = min(w * 0.15, h * 0.6), h * 0.62
    ly, ry = y1 - sh, y1 - sh
    lx, rx = x0 + sw * 0.7, x1 - sw * 0.7
    server(d, lx, ly + sh / 2, sw, sh, c)
    server(d, rx, ry + sh / 2, sw, sh, c, lit=True)
    steps = 5
    for i in range(steps):
        t = (i + 0.5) / steps
        px = lx + (rx - lx) * t
        py = y1 - sh - h * 0.16 - math.sin(t * math.pi) * h * 0.3
        s_ = h * 0.075
        rr(d, (px - s_, py - s_, px + s_, py + s_), s_ * 0.4,
           fill=c["hi"] if i >= steps - 2 else c["hif"], outline=None)
    arrow(d, (lx + sw * 0.7, y1 - sh * 0.2), (rx - sw * 0.7, y1 - sh * 0.2), c["gold"], 7, 24)


def oc_idle(d, b, c, o):
    """Crescent moon over meshed gears -- it maintains itself while you sleep.
    vs dv_gitops' sync loop, which has a commit dot and no moon."""
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    cy = (y0 + y1) / 2
    mx = x0 + w * 0.1
    mr = h * 0.37
    # A crescent is a disc minus a disc, and PIL has no subtract -- so the
    # ground colour rides in the palette purely so this punch is exact.
    circ(d, mx, cy, mr, fill=c["hi"])
    circ(d, mx + mr * 0.52, cy - mr * 0.24, mr * 0.88, fill=c["bg"])
    for i in range(3):
        a = -1.15 + i * 0.62
        circ(d, mx + mr * 1.75 * math.cos(a), cy + mr * 1.75 * math.sin(a),
             h * 0.036, fill=c["gold"])
    gx_ = x0 + w * 0.55
    gear(d, gx_, cy - h * 0.04, h * 0.28, c["ln"], teeth=9, w=8)
    gear(d, gx_ + h * 0.54, cy + h * 0.26, h * 0.16, c["hi"], teeth=7, w=7)
    d.arc([x1 - w * 0.26, cy - h * 0.46, x1 - w * 0.01, cy + h * 0.46],
          -70, 180, fill=c["gold"], width=8)
    arrow(d, (x1 - w * 0.135, cy - h * 0.46), (x1 - w * 0.055, cy - h * 0.4),
          c["gold"], 7, 20)


def oc_jarvis(d, b, c, o):
    """Obsidian crystal wired to a brain -- the vault becomes a second brain.
    vs the two memory posts: only this one has the crystal."""
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    cy = (y0 + y1) / 2
    cx = x0 + w * 0.13
    r = h * 0.42
    d.polygon([(cx, cy - r), (cx + r * 0.74, cy - r * 0.26),
               (cx + r * 0.44, cy + r * 0.82), (cx - r * 0.44, cy + r * 0.82),
               (cx - r * 0.74, cy - r * 0.26)], fill=c["hi"])
    d.line([(cx, cy - r), (cx, cy + r * 0.82)], fill=(255, 255, 255, 160), width=5)
    d.line([(cx - r * 0.74, cy - r * 0.26), (cx, cy - r * 0.06)],
           fill=(255, 255, 255, 120), width=4)
    d.line([(cx + r * 0.74, cy - r * 0.26), (cx, cy - r * 0.06)],
           fill=(255, 255, 255, 120), width=4)
    bx = x1 - w * 0.19
    br = h * 0.42
    for s_ in (-1, 1):
        d.ellipse([bx + s_ * br * 0.3 - br * 0.62, cy - br * 0.9,
                   bx + s_ * br * 0.3 + br * 0.62, cy + br * 0.9],
                  fill=c["hif"], outline=c["ln"], width=7)
    d.line([(bx, cy - br * 0.86), (bx, cy + br * 0.86)], fill=c["ln"], width=6)
    for s_ in (-1, 1):
        for k in (-1, 1):
            d.arc([bx + s_ * br * 0.3 - br * 0.42, cy + k * br * 0.34 - br * 0.26,
                   bx + s_ * br * 0.3 + br * 0.42, cy + k * br * 0.34 + br * 0.26],
                  190, 350, fill=c["ln"], width=5)
    for k in (-1, 0, 1):
        d.line([(cx + r * 0.8, cy + k * h * 0.18),
                (bx - br * 0.95, cy + k * h * 0.26)], fill=c["gold"], width=5)


def oc_beyond(d, b, c, o):
    """Puzzle piece -> arrow -> columned building: past plugins, into
    architecture.  vs dv_cloud's pillars (that roof is a CLOUD)."""
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    cy = (y0 + y1) / 2
    pw = min(w * 0.18, h * 0.62)
    px = x0 + pw * 0.7
    rr(d, (px - pw / 2, cy - pw / 2, px + pw / 2, cy + pw / 2), pw * 0.14,
       fill=c["fill"], outline=c["ln2"], w=6)
    circ(d, px + pw / 2, cy, pw * 0.18, fill=c["fill"], outline=c["ln2"], w=6)
    arrow(d, (px + pw * 0.95, cy), (x0 + w * 0.5, cy), c["gold"], 8, 26)
    bx = x1 - w * 0.22
    bw = min(w * 0.34, h * 1.1)
    d.polygon([(bx - bw / 2, cy - h * 0.16), (bx, cy - h * 0.46),
               (bx + bw / 2, cy - h * 0.16)], fill=c["hi"])
    for i in range(4):
        cxx = bx - bw * 0.34 + i * bw * 0.227
        rr(d, (cxx - bw * 0.05, cy - h * 0.1, cxx + bw * 0.05, cy + h * 0.36),
           bw * 0.02, fill=c["hi"], outline=None)
    d.rectangle([bx - bw / 2, cy + h * 0.36, bx + bw / 2, cy + h * 0.46], fill=c["hi"])


def oc_claude(d, b, c, o):
    """Terminal window opened as a cutaway, with the agent loop turning beside
    it.  vs oc_memarch's strata: this one is a WINDOW with a title bar."""
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    tw = min(w * 0.6, h * 2.1)
    tx = x0 + w * 0.01
    rr(d, (tx, y0, tx + tw, y1), h * 0.1, fill=c["fill"], outline=c["ln"], w=7)
    d.line([(tx, y0 + h * 0.2), (tx + tw, y0 + h * 0.2)], fill=c["ln"], width=6)
    for i in range(3):
        circ(d, tx + h * 0.12 + i * h * 0.14, y0 + h * 0.1, h * 0.045, fill=c["ln2"])
    label(d, tx + h * 0.18, y0 + h * 0.44, ">", c["hi"], h * 0.32)
    for i in range(2):
        yy = y0 + h * 0.38 + i * h * 0.26
        d.line([(tx + h * 0.36, yy), (tx + tw * (0.7 if i else 0.86), yy)],
               fill=c["ln2"], width=7)
    cx, cy = x1 - w * 0.14, (y0 + y1) / 2
    r = h * 0.36
    d.arc([cx - r, cy - r, cx + r, cy + r], 40, 330, fill=c["hi"], width=11)
    a = math.radians(330)
    arrow(d, (cx + r * math.cos(a - 0.3), cy + r * math.sin(a - 0.3)),
          (cx + r * math.cos(a + 0.25), cy + r * math.sin(a + 0.25)), c["hi"], 9, 26)
    circ(d, cx, cy, r * 0.34, fill=c["gold"])


def oc_memarch(d, b, c, o):
    """Cross-section: four labelled strata with a governance line drawn through
    them, like a foundation section.  vs oc_memory's glowing stack + magnifier."""
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    n = 4
    sh = h / n
    names = ["IDENTITY", "CONFIG", "DAILY", "LONG-TERM"]
    for i in range(n):
        y = y0 + i * sh
        inset = w * 0.03 * i
        rr(d, (x0 + inset, y + sh * 0.08, x0 + w * 0.66, y + sh * 0.92), sh * 0.2,
           fill=c["hif"] if i == n - 1 else c["fill"],
           outline=c["hi"] if i == n - 1 else c["ln2"], w=5)
        label(d, x0 + inset + w * 0.02, y + sh / 2, names[i], c["ln"], sh * 0.34, "Bold")
    gx_ = x0 + w * 0.74
    d.line([(gx_, y0), (gx_, y1)], fill=c["gold"], width=8)
    for i in range(n):
        circ(d, gx_, y0 + sh * (i + 0.5), h * 0.045, fill=c["gold"])


# --------------------------------------------------------------------------
# DevOps motifs -- blueprints, dark ground
# --------------------------------------------------------------------------
def dv_git(d, b, c, o):
    """Commit-graph rail: a branch leaving the trunk and merging back.
    vs dv_gitops (which is a LOOP into a cluster)."""
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    my = y0 + h * 0.72
    by = y0 + h * 0.2
    d.line([(x0, my), (x1, my)], fill=c["ln"], width=8)
    d.line([(x0 + w * 0.24, by), (x0 + w * 0.72, by)], fill=c["hi"], width=8)
    d.arc([x0 + w * 0.08, by, x0 + w * 0.4, my], 180, 270, fill=c["hi"], width=8)
    d.arc([x0 + w * 0.6, by, x0 + w * 0.92, my], 270, 360, fill=c["hi"], width=8)
    for t in (0.06, 0.34, 0.62, 0.94):
        circ(d, x0 + w * t, my, h * 0.085, fill=c["ln"])
    for t in (0.3, 0.5, 0.7):
        circ(d, x0 + w * t, by, h * 0.075, fill=c["hi"])


def dv_api(d, b, c, o):
    """Client and server volleying, with status stamps.  vs dv_net's packet path
    (that one crosses a firewall and a fork)."""
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    lx, rx = x0 + w * 0.1, x1 - w * 0.1
    cy = (y0 + y1) / 2
    circ(d, lx, cy, h * 0.24, fill=c["fill"], outline=c["ln"], w=7)
    server(d, rx, cy, min(w * 0.15, h * 0.6), h * 0.72, c)
    arrow(d, (lx + h * 0.3, cy - h * 0.2), (rx - h * 0.42, cy - h * 0.2), c["ln"], 7, 24)
    arrow(d, (rx - h * 0.42, cy + h * 0.24), (lx + h * 0.3, cy + h * 0.24), c["hi"], 7, 24)
    label(d, (lx + rx) / 2, cy - h * 0.42, "GET", c["ln2"], h * 0.24, "Bold")
    label(d, (lx + rx) / 2, cy + h * 0.46, "200", c["hi"], h * 0.26, "Black")


def dv_linux(d, b, c, o):
    """A shell prompt with a real pipeline of piped commands."""
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    cy = (y0 + y1) / 2
    label(d, x0 + w * 0.05, cy, "$", c["hi"], h * 0.78)
    n = 3
    bw = w * 0.2
    for i in range(n):
        bx = x0 + w * 0.14 + i * (bw + w * 0.07)
        rr(d, (bx, cy - h * 0.24, bx + bw, cy + h * 0.24), h * 0.1,
           fill=c["fill"], outline=c["ln"], w=6)
        for k in range(2):
            d.line([(bx + bw * 0.14, cy - h * 0.08 + k * h * 0.16),
                    (bx + bw * (0.78 if k == 0 else 0.5), cy - h * 0.08 + k * h * 0.16)],
                   fill=c["ln2"], width=5)
        if i < n - 1:
            px = bx + bw + w * 0.035
            d.line([(px, cy - h * 0.2), (px, cy + h * 0.2)], fill=c["hi"], width=7)


def dv_net(d, b, c, o):
    """Packet path: globe -> firewall -> load-balancer fork -> servers.
    vs dv_api's two-party volley."""
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    cy = (y0 + y1) / 2
    gx_ = x0 + w * 0.08
    circ(d, gx_, cy, h * 0.26, fill=None, outline=c["ln"], w=7)
    d.line([(gx_ - h * 0.26, cy), (gx_ + h * 0.26, cy)], fill=c["ln"], width=5)
    d.arc([gx_ - h * 0.13, cy - h * 0.26, gx_ + h * 0.13, cy + h * 0.26], 0, 360,
          fill=c["ln"], width=5)
    fx = x0 + w * 0.36
    for r_ in range(3):
        for k in range(3):
            bw2, bh2 = w * 0.045, h * 0.16
            off = (bw2 / 2) if r_ % 2 else 0
            d.rectangle([fx - bw2 + off + (k - 1) * bw2, cy - h * 0.24 + r_ * bh2,
                         fx + off + (k - 1) * bw2, cy - h * 0.24 + (r_ + 1) * bh2],
                        outline=c["hi"], width=4)
    arrow(d, (gx_ + h * 0.32, cy), (fx - w * 0.09, cy), c["ln2"], 6, 20)
    lx = x0 + w * 0.62
    circ(d, lx, cy, h * 0.15, fill=c["hif"], outline=c["hi"], w=6)
    arrow(d, (fx + w * 0.09, cy), (lx - h * 0.2, cy), c["ln2"], 6, 20)
    for k in (-1, 0, 1):
        sy = cy + k * h * 0.34
        d.line([(lx + h * 0.18, cy), (x1 - w * 0.12, sy)], fill=c["ln2"], width=5)
        server(d, x1 - w * 0.06, sy, w * 0.08, h * 0.24, c)


def dv_db(d, b, c, o):
    """Cylinder stack plus a JOIN venn -- design AND query in one picture."""
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    cy = (y0 + y1) / 2
    cx = x0 + w * 0.16
    cyl(d, cx, cy, min(w * 0.11, h * 0.32), h * 0.44, c, lit=True)
    r = h * 0.3
    vx = x1 - w * 0.26
    circ(d, vx - r * 0.55, cy, r, fill=c["fill"], outline=c["ln"], w=7)
    circ(d, vx + r * 0.55, cy, r, fill=c["fill"], outline=c["ln"], w=7)
    d.chord([vx - r * 0.55 - r, cy - r, vx - r * 0.55 + r, cy + r], -60, 60, fill=c["hif"])
    d.chord([vx + r * 0.55 - r, cy - r, vx + r * 0.55 + r, cy + r], 120, 240, fill=c["hif"])
    label(d, vx, cy, "JOIN", c["hi"], h * 0.2, "Black")


def dv_dockervm(d, b, c, o):
    """The page's ONLY split frame: a heavy VM with OS floors vs light
    containers.  vs dv_compose (one file fanning out)."""
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    mid = (x0 + x1) / 2
    d.line([(mid, y0 - h * 0.06), (mid, y1 + h * 0.06)], fill=c["ln2"], width=5)
    lw = w * 0.34
    lx = x0 + w * 0.06
    for i in range(3):
        yy = y1 - (i + 1) * h * 0.3
        rr(d, (lx, yy, lx + lw, yy + h * 0.26), h * 0.05,
           fill=c["dimf"], outline=c["ln2"], w=6)
        d.line([(lx + lw * 0.1, yy + h * 0.13), (lx + lw * 0.5, yy + h * 0.13)],
               fill=c["ln2"], width=5)
    label(d, lx + lw / 2, y0 - h * 0.02, "VM", c["ln2"], h * 0.22, "Bold")
    bw = w * 0.12
    for i in range(3):
        bx = mid + w * 0.08 + i * (bw + w * 0.03)
        rr(d, (bx, y1 - h * 0.42, bx + bw, y1 - h * 0.02), h * 0.07,
           fill=c["hif"], outline=c["hi"], w=6)
    label(d, mid + w * 0.28, y0 + h * 0.14, "CONTAINERS", c["hi"], h * 0.2, "Bold")


def dv_compose(d, b, c, o):
    """One YAML sheet fanning into three linked containers.
    vs dv_dockervm's comparison."""
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    fw, fh = min(w * 0.17, h * 0.62), h * 0.86
    fx, fy = x0 + w * 0.03, (y0 + y1) / 2 - fh / 2
    rr(d, (fx, fy, fx + fw, fy + fh), fh * 0.08, fill=c["fill"], outline=c["ln"], w=7)
    for i in range(4):
        yy = fy + fh * (0.2 + i * 0.19)
        d.line([(fx + fw * 0.16 + (i % 2) * fw * 0.14, yy),
                (fx + fw * 0.82, yy)], fill=c["ln2"], width=5)
    bw = min(w * 0.19, h * 0.62)
    bx = x1 - bw * 1.15
    ys = [(y0 + y1) / 2 - h * 0.34, (y0 + y1) / 2, (y0 + y1) / 2 + h * 0.34]
    for yy in ys:
        rr(d, (bx, yy - h * 0.14, bx + bw, yy + h * 0.14), h * 0.06,
           fill=c["hif"], outline=c["hi"], w=6)
        d.line([(fx + fw + w * 0.02, (y0 + y1) / 2), (bx - w * 0.02, yy)],
               fill=c["ln2"], width=5)
    d.line([(bx - w * 0.035, ys[0]), (bx - w * 0.035, ys[2])], fill=c["hi"], width=5)


def dv_k8s(d, b, c, o):
    """Helm wheel steering a ring of hex pods.  vs dv_gitops (commit-driven)."""
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    cy = (y0 + y1) / 2
    hx = x0 + w * 0.15
    r = h * 0.4
    circ(d, hx, cy, r, fill=None, outline=c["hi"], w=9)
    circ(d, hx, cy, r * 0.3, fill=c["hi"])
    for i in range(8):
        a = i * math.pi / 4
        d.line([(hx + r * 0.3 * math.cos(a), cy + r * 0.3 * math.sin(a)),
                (hx + r * 1.28 * math.cos(a), cy + r * 1.28 * math.sin(a))],
               fill=c["hi"], width=7)
    ring_x = x1 - w * 0.28
    for i in range(6):
        a = i * math.pi / 3 + math.pi / 6
        px = ring_x + h * 0.46 * math.cos(a)
        py = cy + h * 0.4 * math.sin(a)
        hexa(d, px, py, h * 0.16, fill=c["fill"], outline=c["ln"], w=5)
    arrow(d, (hx + r * 1.4, cy), (ring_x - h * 0.66, cy), c["ln2"], 6, 22)


def dv_gitops(d, b, c, o):
    """A commit driving a sync loop into a cluster.  vs dv_k8s (helm) and
    dv_cicd (a straight conveyor)."""
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    cy = (y0 + y1) / 2
    gx_ = x0 + w * 0.08
    circ(d, gx_, cy, h * 0.16, fill=c["hi"])
    d.line([(gx_, cy + h * 0.18), (gx_, y1)], fill=c["ln2"], width=6)
    label(d, gx_, y1 + h * 0.12, "git", c["ln2"], h * 0.2, "Bold")
    lx, rx = x0 + w * 0.28, x1 - w * 0.3
    d.arc([lx, cy - h * 0.42, rx, cy + h * 0.42], 180, 360, fill=c["hi"], width=8)
    d.arc([lx, cy - h * 0.42, rx, cy + h * 0.42], 0, 180, fill=c["ln2"], width=8)
    arrow(d, ((lx + rx) / 2 - w * 0.02, cy - h * 0.42),
          ((lx + rx) / 2 + w * 0.06, cy - h * 0.42), c["hi"], 7, 22)
    arrow(d, ((lx + rx) / 2 + w * 0.02, cy + h * 0.42),
          ((lx + rx) / 2 - w * 0.06, cy + h * 0.42), c["ln2"], 7, 22)
    hexa(d, x1 - w * 0.1, cy, h * 0.34, fill=c["hif"], outline=c["hi"], w=7)
    hexa(d, x1 - w * 0.1, cy, h * 0.16, fill=c["hi"])


def dv_cicd(d, b, c, o):
    """A conveyor of four stations, each a different tool.  vs dv_gha's matrix."""
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    cy = (y0 + y1) / 2 - h * 0.06
    n = 4
    gap = w * 0.045
    side = (w - gap * (n - 1)) / n
    side = min(side, h * 0.62)
    total = side * n + gap * (n - 1)
    sx = x0 + (w - total) / 2
    for i in range(n):
        x = sx + i * (side + gap)
        lit = i == n - 1
        rr(d, (x, cy - side / 2, x + side, cy + side / 2), side * 0.22,
           fill=c["hif"] if lit else c["fill"],
           outline=c["hi"] if lit else c["ln"], w=6)
        col = c["hi"] if lit else c["ln"]
        mx, my = x + side / 2, cy
        if i == 0:      # hammer
            d.line([(mx - side * 0.16, my + side * 0.16),
                    (mx + side * 0.1, my - side * 0.1)], fill=col, width=8)
            d.line([(mx + side * 0.02, my - side * 0.22),
                    (mx + side * 0.22, my - side * 0.02)], fill=col, width=12)
        elif i == 1:    # flask
            d.polygon([(mx - side * 0.07, my - side * 0.2), (mx + side * 0.07, my - side * 0.2),
                       (mx + side * 0.2, my + side * 0.2), (mx - side * 0.2, my + side * 0.2)],
                      outline=col, width=7)
        elif i == 2:    # box
            rr(d, (mx - side * 0.19, my - side * 0.16, mx + side * 0.19, my + side * 0.18),
               side * 0.05, outline=col, w=7)
            d.line([(mx - side * 0.19, my - side * 0.02), (mx + side * 0.19, my - side * 0.02)],
                   fill=col, width=6)
        else:           # rocket
            d.polygon([(mx, my - side * 0.24), (mx + side * 0.12, my + side * 0.06),
                       (mx - side * 0.12, my + side * 0.06)], fill=col)
            d.polygon([(mx - side * 0.06, my + side * 0.08), (mx + side * 0.06, my + side * 0.08),
                       (mx, my + side * 0.24)], fill=col)
        if i < n - 1:
            arrow(d, (x + side + gap * 0.12, cy), (x + side + gap * 0.88, cy), c["ln2"], 6, 16)
    d.line([(sx, cy + side * 0.72), (sx + total, cy + side * 0.72)], fill=c["ln2"], width=6)


def dv_gha(d, b, c, o):
    """A play button firing a cascading job matrix.  vs dv_cicd's linear belt."""
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    cy = (y0 + y1) / 2
    px = x0 + w * 0.1
    circ(d, px, cy, h * 0.3, fill=None, outline=c["hi"], w=8)
    d.polygon([(px - h * 0.09, cy - h * 0.15), (px - h * 0.09, cy + h * 0.15),
               (px + h * 0.16, cy)], fill=c["hi"])
    cols, rows = 4, 3
    gw = w * 0.5
    cw = gw / cols * 0.78
    ch = h / rows * 0.72
    gx0 = x0 + w * 0.32
    for r in range(rows):
        for cc in range(cols):
            x = gx0 + cc * (gw / cols)
            y = y0 + r * (h / rows)
            on = cc <= r
            rr(d, (x, y, x + cw, y + ch), ch * 0.26,
               fill=c["hif"] if on else c["dimf"],
               outline=c["hi"] if on else c["ln2"], w=5)
    arrow(d, (px + h * 0.36, cy), (gx0 - w * 0.03, cy), c["ln2"], 6, 20)


def dv_autotest(d, b, c, o):
    """A push running a GAUNTLET of gates, each stamped with a check.
    vs dv_pyramid (a pyramid) and dv_quality (a magnifier)."""
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    cy = (y0 + y1) / 2
    circ(d, x0 + w * 0.05, cy, h * 0.13, fill=c["ln"])
    d.line([(x0 + w * 0.05, cy), (x1 - w * 0.02, cy)], fill=c["ln2"], width=6)
    n = 4
    for i in range(n):
        gx_ = x0 + w * (0.18 + i * 0.2)
        d.line([(gx_, cy - h * 0.42), (gx_, cy + h * 0.42)], fill=c["ln"], width=7)
        d.line([(gx_ + w * 0.055, cy - h * 0.42), (gx_ + w * 0.055, cy + h * 0.42)],
               fill=c["ln"], width=7)
        mx = gx_ + w * 0.0275
        d.line([(mx - h * 0.09, cy), (mx - h * 0.02, cy + h * 0.09),
                (mx + h * 0.11, cy - h * 0.12)], fill=c["hi"], width=8, joint="curve")
    arrow(d, (x1 - w * 0.1, cy), (x1, cy), c["hi"], 7, 22)


def dv_pyramid(d, b, c, o):
    """The testing pyramid -- the page's only pyramid.  vs dv_autotest's gates."""
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    cx = x0 + w * 0.32
    base = min(w * 0.46, h * 1.6)
    tiers = [("E2E", 0.34), ("INTEGRATION", 0.67), ("UNIT", 1.0)]
    th = h / 3
    for i, (name, k) in enumerate(tiers):
        yy = y0 + i * th
        top_w = base * (k - 0.33) if i else 0
        bot_w = base * k
        d.polygon([(cx - top_w / 2, yy), (cx + top_w / 2, yy),
                   (cx + bot_w / 2, yy + th * 0.9), (cx - bot_w / 2, yy + th * 0.9)],
                  fill=c["hif"] if i == 2 else c["fill"],
                  outline=c["hi"] if i == 2 else c["ln"], width=6)
        d.text((x1, yy + th * 0.45), name, font=font(int(h * 0.16), "Bold"),
               fill=c["hi"] if i == 2 else c["ln2"], anchor="rm")


def dv_quality(d, b, c, o):
    """Magnifier over code lines, revealing a cut gem.  vs the two test posts."""
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    for i in range(4):
        yy = y0 + h * (0.12 + i * 0.25)
        d.line([(x0 + w * 0.03 + (i % 2) * w * 0.06, yy),
                (x0 + w * (0.42 if i % 2 else 0.5), yy)], fill=c["ln2"], width=7)
    cx, cy = x0 + w * 0.62, (y0 + y1) / 2
    r = h * 0.42
    circ(d, cx, cy, r, fill=c["dimf"], outline=c["ln"], w=9)
    d.line([(cx + r * 0.72, cy + r * 0.72), (cx + r * 1.5, cy + r * 1.5)],
           fill=c["ln"], width=13)
    gr = r * 0.5
    d.polygon([(cx, cy - gr), (cx + gr * 0.86, cy - gr * 0.2),
               (cx, cy + gr), (cx - gr * 0.86, cy - gr * 0.2)], fill=c["hi"])
    d.line([(cx - gr * 0.86, cy - gr * 0.2), (cx + gr * 0.86, cy - gr * 0.2)],
           fill=(255, 255, 255, 160), width=4)


def dv_secpipe(d, b, c, o):
    """A padlock built INTO a pipe segment -- security inside the pipeline.
    vs dv_auth's door and oc_security's shield."""
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    cy = (y0 + y1) / 2
    d.line([(x0, cy - h * 0.2), (x1, cy - h * 0.2)], fill=c["ln"], width=7)
    d.line([(x0, cy + h * 0.2), (x1, cy + h * 0.2)], fill=c["ln"], width=7)
    for t in (0.14, 0.86):
        d.line([(x0 + w * t, cy - h * 0.28), (x0 + w * t, cy + h * 0.28)],
               fill=c["ln2"], width=6)
    cx = (x0 + x1) / 2
    bw, bh = min(w * 0.2, h * 0.66), h * 0.46
    rr(d, (cx - bw / 2, cy - bh * 0.1, cx + bw / 2, cy + bh * 0.9), bh * 0.18,
       fill=c["hi"], outline=None)
    d.arc([cx - bw * 0.3, cy - bh * 0.72, cx + bw * 0.3, cy + bh * 0.16],
          180, 360, fill=c["hi"], width=11)
    circ(d, cx, cy + bh * 0.36, bh * 0.12, fill=(13, 27, 42))


def dv_auth(d, b, c, o):
    """A door with a key (authN) and a badge list (authZ) -- two ideas, two
    glyphs.  vs dv_secpipe's padlock."""
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    dw, dh = min(w * 0.24, h * 0.72), h * 0.96
    dx, dy = x0 + w * 0.06, y0 + h * 0.02
    rr(d, (dx, dy, dx + dw, dy + dh), dw * 0.1, fill=c["fill"], outline=c["ln"], w=7)
    circ(d, dx + dw * 0.78, dy + dh * 0.52, h * 0.055, fill=c["hi"])
    kx, ky = x0 + w * 0.42, (y0 + y1) / 2
    circ(d, kx, ky, h * 0.15, fill=None, outline=c["hi"], w=9)
    d.line([(kx + h * 0.14, ky), (kx + h * 0.5, ky)], fill=c["hi"], width=9)
    d.line([(kx + h * 0.42, ky), (kx + h * 0.42, ky + h * 0.14)], fill=c["hi"], width=9)
    d.line([(kx + h * 0.5, ky), (kx + h * 0.5, ky + h * 0.1)], fill=c["hi"], width=9)
    bx = x1 - w * 0.26
    for i in range(3):
        yy = y0 + h * (0.14 + i * 0.32)
        rr(d, (bx, yy, bx + w * 0.22, yy + h * 0.2), h * 0.06,
           fill=c["dimf"], outline=c["ln2"], w=5)
        col = c["hi"] if i < 2 else c["ln2"]
        d.line([(bx + w * 0.03, yy + h * 0.1), (bx + w * 0.055, yy + h * 0.15),
                (bx + w * 0.095, yy + h * 0.05)], fill=col, width=6, joint="curve")


def dv_obs(d, b, c, o):
    """Three signals -- metric line, log bars, trace spans -- converging into an
    eye.  vs dv_sre's dial."""
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    sw = w * 0.3
    pts = [(x0 + sw * i / 6, y0 + h * (0.16 + 0.1 * math.sin(i * 1.3))) for i in range(7)]
    d.line(pts, fill=c["ln"], width=6, joint="curve")
    for i in range(6):
        bh2 = h * (0.06 + 0.04 * ((i * 5) % 3))
        d.rectangle([x0 + sw * i / 6, y0 + h * 0.56 - bh2, x0 + sw * i / 6 + sw * 0.1,
                     y0 + h * 0.56], fill=c["ln2"])
    for i in range(3):
        d.line([(x0 + sw * (0.05 + i * 0.12), y0 + h * (0.76 + i * 0.08)),
                (x0 + sw * (0.55 + i * 0.14), y0 + h * (0.76 + i * 0.08))],
               fill=c["ln2"], width=7)
    ex, ey = x1 - w * 0.2, (y0 + y1) / 2
    er = h * 0.44
    d.chord([ex - er, ey - er * 0.72, ex + er, ey + er * 0.72], 0, 180, fill=None,
            outline=c["hi"], width=8)
    d.chord([ex - er, ey - er * 0.72, ex + er, ey + er * 0.72], 180, 360, fill=None,
            outline=c["hi"], width=8)
    circ(d, ex, ey, er * 0.3, fill=c["hi"])
    for i, yy in enumerate((y0 + h * 0.2, y0 + h * 0.5, y0 + h * 0.85)):
        d.line([(x0 + sw * 1.05, yy), (ex - er * 1.1, ey)], fill=c["ln2"], width=4)


def dv_sre(d, b, c, o):
    """A reliability dial at 99.9% beside an error-budget burn-down.
    vs dv_obs' eye and dv_frontend's dial-inside-a-browser."""
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    cx, cy = x0 + w * 0.16, (y0 + y1) / 2 + h * 0.1
    r = h * 0.44
    d.arc([cx - r, cy - r, cx + r, cy + r], 180, 360, fill=c["ln2"], width=13)
    d.arc([cx - r, cy - r, cx + r, cy + r], 180, 342, fill=c["hi"], width=13)
    a = math.radians(342)
    d.line([(cx, cy), (cx + r * 0.8 * math.cos(a), cy + r * 0.8 * math.sin(a))],
           fill=c["ln"], width=8)
    circ(d, cx, cy, h * 0.06, fill=c["ln"])
    label(d, cx, cy + h * 0.26, "99.9%", c["hi"], h * 0.26, "Black")
    bx0, bx1 = x0 + w * 0.44, x1 - w * 0.02
    by = y0 + h * 0.28
    d.line([(bx0, by), (bx1, y0 + h * 0.86)], fill=c["hi"], width=8)
    d.line([(bx0, by), (bx0, y0 + h * 0.95)], fill=c["ln2"], width=5)
    d.line([(bx0, y0 + h * 0.95), (bx1, y0 + h * 0.95)], fill=c["ln2"], width=5)
    for i in range(4):
        xx = bx0 + (bx1 - bx0) * (0.2 + i * 0.25)
        d.line([(xx, y0 + h * 0.95), (xx, y0 + h * 0.9)], fill=c["ln2"], width=4)


def dv_iac(d, b, c, o):
    """Curly braces projecting isometric servers upward -- code becomes real
    machines.  vs dv_cloud's pillars holding a roof up."""
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    cy = (y0 + y1) / 2
    bf = font(int(h * 1.15), "Black")
    d.text((x0 + w * 0.01, cy), "{", font=bf, fill=c["ln"], anchor="lm")
    d.text((x0 + w * 0.27, cy), "}", font=bf, fill=c["ln"], anchor="lm")
    for i in range(3):
        yy = cy - h * 0.16 + i * h * 0.16
        d.line([(x0 + w * 0.11, yy), (x0 + w * (0.24 if i % 2 else 0.2), yy)],
               fill=c["ln2"], width=5)
    arrow(d, (x0 + w * 0.40, cy), (x0 + w * 0.53, cy), c["gold"], 8, 24)
    for i in range(3):
        sx = x1 - w * 0.36 + i * w * 0.11
        sy = cy + h * 0.28 - i * h * 0.28
        d.polygon([(sx, sy), (sx + w * 0.11, sy - h * 0.16), (sx + w * 0.22, sy),
                   (sx + w * 0.11, sy + h * 0.16)],
                  fill=c["hif"], outline=c["hi"], width=5)


def dv_cloud(d, b, c, o):
    """A cloud roof resting on pillars -- the Well-Architected picture.
    vs oc_beyond's temple (that roof is a TRIANGLE)."""
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    cx = (x0 + x1) / 2
    cw = min(w * 0.62, h * 2.4)
    cy = y0 + h * 0.22
    circ(d, cx - cw * 0.24, cy, h * 0.2, fill=c["hif"])
    circ(d, cx, cy - h * 0.06, h * 0.26, fill=c["hif"])
    circ(d, cx + cw * 0.24, cy, h * 0.2, fill=c["hif"])
    d.rectangle([cx - cw * 0.36, cy, cx + cw * 0.36, cy + h * 0.2], fill=c["hif"])
    d.line([(cx - cw * 0.44, cy + h * 0.2), (cx + cw * 0.44, cy + h * 0.2)],
           fill=c["hi"], width=8)
    for i in range(4):
        px = cx - cw * 0.33 + i * cw * 0.22
        d.line([(px, cy + h * 0.24), (px, y1)], fill=c["ln"], width=10)
    d.line([(cx - cw * 0.44, y1), (cx + cw * 0.44, y1)], fill=c["ln"], width=8)


def dv_deploy(d, b, c, o):
    """One package FORKING to three landing pads -- the hosting choice.
    vs oc_production's single launch."""
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    px, py = x0 + w * 0.09, (y0 + y1) / 2
    s_ = h * 0.24
    rr(d, (px - s_, py - s_, px + s_, py + s_), s_ * 0.24, fill=c["hi"], outline=None)
    d.line([(px - s_, py - s_ * 0.2), (px + s_, py - s_ * 0.2)], fill=(255, 255, 255, 170), width=5)
    ys = [y0 + h * 0.12, (y0 + y1) / 2, y1 - h * 0.12]
    for i, yy in enumerate(ys):
        arrow(d, (px + s_ * 1.3, py), (x1 - w * 0.2, yy), c["ln2"], 6, 20)
        pw = w * 0.14
        d.ellipse([x1 - w * 0.17, yy - h * 0.09, x1 - w * 0.17 + pw, yy + h * 0.09],
                  fill=c["dimf"], outline=c["ln"], width=6)
        circ(d, x1 - w * 0.17 + pw / 2, yy, h * 0.03, fill=c["hi"])


def dv_webarch(d, b, c, o):
    """An exploded floor plan: MVC rooms plus a queue corridor.
    vs dv_cloud and oc_beyond."""
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    names = ["M", "V", "C"]
    rw = w * 0.17
    for i in range(3):
        rx = x0 + w * 0.03 + i * (rw + w * 0.035)
        rr(d, (rx, y0 + h * 0.06, rx + rw, y1 - h * 0.28), h * 0.07,
           fill=c["fill"], outline=c["ln"], w=6)
        label(d, rx + rw / 2, (y0 + y1) / 2 - h * 0.1, names[i], c["ln"], h * 0.3)
    cy = y1 - h * 0.13
    d.line([(x0 + w * 0.03, cy), (x1 - w * 0.28, cy)], fill=c["ln2"], width=6)
    d.line([(x0 + w * 0.03, cy + h * 0.14), (x1 - w * 0.28, cy + h * 0.14)],
           fill=c["ln2"], width=6)
    for i in range(4):
        qx = x0 + w * 0.09 + i * w * 0.12
        rr(d, (qx, cy + h * 0.02, qx + w * 0.06, cy + h * 0.12), h * 0.03,
           fill=c["hif"], outline=c["hi"], w=4)
    for i in range(3):
        yy = y0 + h * (0.16 + i * 0.3)
        rr(d, (x1 - w * 0.2, yy, x1 - w * 0.02, yy + h * 0.2), h * 0.06,
           fill=c["dimf"], outline=c["ln2"], w=5)


def dv_frontend(d, b, c, o):
    """A speedometer INSIDE a browser frame -- the frame is what separates it
    from dv_sre's bare dial."""
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    bw = min(w * 0.56, h * 2.0)
    bx = x0 + w * 0.02
    rr(d, (bx, y0, bx + bw, y1), h * 0.08, fill=c["fill"], outline=c["ln"], w=7)
    d.line([(bx, y0 + h * 0.2), (bx + bw, y0 + h * 0.2)], fill=c["ln"], width=6)
    for i in range(3):
        circ(d, bx + h * 0.12 + i * h * 0.13, y0 + h * 0.1, h * 0.04, fill=c["ln2"])
    cx, cy = bx + bw / 2, y0 + h * 0.72
    r = h * 0.36
    d.arc([cx - r, cy - r, cx + r, cy + r], 180, 360, fill=c["ln2"], width=12)
    d.arc([cx - r, cy - r, cx + r, cy + r], 180, 300, fill=c["hi"], width=12)
    a = math.radians(300)
    d.line([(cx, cy), (cx + r * 0.78 * math.cos(a), cy + r * 0.78 * math.sin(a))],
           fill=c["ln"], width=8)
    for i in range(3):
        fx = x1 - w * 0.28 + i * w * 0.1
        rr(d, (fx, (y0 + y1) / 2 - h * 0.16, fx + w * 0.07, (y0 + y1) / 2 + h * 0.16),
           h * 0.05, fill=c["hif"] if i == 0 else c["dimf"],
           outline=c["hi"] if i == 0 else c["ln2"], w=5)


def dv_vibe(d, b, c, o):
    """A flowing gold wave threading four nodes -- plan, build, verify, release.
    vs dv_cicd's rigid conveyor: this one is a CURVE."""
    x0, y0, x1, y1 = b
    w, h = x1 - x0, y1 - y0
    cy = (y0 + y1) / 2
    pts = []
    for i in range(41):
        t = i / 40
        pts.append((x0 + w * t, cy + math.sin(t * math.pi * 2.1) * h * 0.3))
    d.line(pts, fill=c["hi"], width=11, joint="curve")
    for i, t in enumerate((0.06, 0.36, 0.66, 0.95)):
        px = x0 + w * t
        py = cy + math.sin(t * math.pi * 2.1) * h * 0.3
        circ(d, px, py, h * 0.15, fill=c["ln"] if i < 3 else c["hi"],
             outline=None)
        circ(d, px, py, h * 0.07, fill=(13, 27, 42) if i < 3 else WHITE)


MOTIFS = {
    "oc_os": oc_os, "oc_team": oc_team, "oc_memory": oc_memory,
    "oc_security": oc_security, "oc_integrations": oc_integrations,
    "oc_skills": oc_skills, "oc_production": oc_production,
    "oc_migration": oc_migration, "oc_idle": oc_idle, "oc_jarvis": oc_jarvis,
    "oc_beyond": oc_beyond, "oc_claude": oc_claude, "oc_memarch": oc_memarch,
    "dv_git": dv_git, "dv_api": dv_api, "dv_linux": dv_linux, "dv_net": dv_net,
    "dv_db": dv_db, "dv_dockervm": dv_dockervm, "dv_compose": dv_compose,
    "dv_k8s": dv_k8s, "dv_gitops": dv_gitops, "dv_cicd": dv_cicd, "dv_gha": dv_gha,
    "dv_autotest": dv_autotest, "dv_pyramid": dv_pyramid, "dv_quality": dv_quality,
    "dv_secpipe": dv_secpipe, "dv_auth": dv_auth, "dv_obs": dv_obs, "dv_sre": dv_sre,
    "dv_iac": dv_iac, "dv_cloud": dv_cloud, "dv_deploy": dv_deploy,
    "dv_webarch": dv_webarch, "dv_frontend": dv_frontend, "dv_vibe": dv_vibe,
}


# --------------------------------------------------------------------------
# the one renderer
# --------------------------------------------------------------------------
PART_RE = re.compile(r"PART (\d+)$")   # chip is OpenClaw-only; see render()


def part_chip(d, x, y, n, c, px):
    """N/7 chip for the seven numbered OpenClaw posts, so the sequence reads at
    card size where the eyebrow is only a few pixels tall."""
    txt = "%s/7" % n
    f = font(int(px * 0.62), "Black")
    tw = d.textlength(txt, font=f)
    pad = px * 0.34
    rr(d, (x, y, x + tw + pad * 2, y + px * 1.05), px * 0.52, fill=c["chip"], outline=None)
    d.text((x + pad, y + px * 0.52), txt, font=f, fill=c["chiptx"], anchor="lm")
    return tw + pad * 2


def render(row, size=(S, S), og=False):
    W, H = size
    img = ground(row["ground"], size).convert("RGB")
    d = ImageDraw.Draw(img, "RGBA")
    c = ink(row["ground"], row.get("accent") or "violet")
    opts = dict(kv.split("=", 1) for kv in row["opts"].split(";") if kv)
    motif = MOTIFS[row["motif"]]

    # Blueprint grid: real texture on the dark DevOps covers, near-invisible on
    # the light OpenClaw posters (a poster is not graph paper).
    pitch = int(min(W, H) * 0.0625)
    for i in range(0, max(W, H), pitch):
        d.line([(i, 0), (i, H)], fill=c["grid"], width=2)
        d.line([(0, i), (W, i)], fill=c["grid"], width=2)

    # OpenClaw only: the chip says "N of 7". DevOps runs to PART 24, where a
    # "/7" denominator would be a lie (and "24/7" reads as the phrase).
    m = PART_RE.search(row["eyebrow"]) if row["eyebrow"].startswith("OPENCLAW") else None

    if og:
        lx = int(W * 0.07)
        maxw = int(W * 0.44)
        ey = int(H * 0.20)
        ex = lx
        if m:
            ex += part_chip(d, lx, ey - int(H * 0.012), m.group(1), c, H * 0.05) + W * 0.012
        d.text((ex, ey), row["eyebrow"], font=font(28, "Bold"), fill=c["eyebrow"])
        f = fit(d, row["title"], 76, "Black", maxw, floor=40)
        lines = wrap(d, row["title"], f, maxw)
        y = int(H * 0.30)
        for ln in lines[:3]:
            d.text((lx, y), ln, font=f, fill=c["title"])
            y += int(f.size * 1.12)
        d.line([(lx, y + 18), (lx + int(W * 0.09), y + 18)], fill=c["rule"], width=6)
        if row["thai"]:
            tf = thai_font(30)
            for ln in wrap(d, row["thai"], tf, maxw)[:2]:
                y += 46
                d.text((lx, y + 24), ln, font=tf, fill=c["thai"])
        motif(d, (int(W * 0.52), int(H * 0.30), int(W * 0.965), int(H * 0.72)), c, opts)
        return img

    lx = int(W * BAND_X[0] + W * 0.02)
    maxw = int(W * (BAND_X[1] - BAND_X[0]) - W * 0.04)

    ey = int(H * 0.215)
    ex = lx
    if m:
        ex += part_chip(d, lx, ey - int(H * 0.011), m.group(1), c, H * 0.042) + W * 0.014
    d.text((ex, ey), row["eyebrow"], font=font(40, "Bold"), fill=c["eyebrow"])

    f = fit(d, row["title"], 116, "Black", maxw)
    lines = wrap(d, row["title"], f, maxw)
    if len(lines) > 1:
        f = fit(d, max(lines, key=len), 104, "Black", maxw)
        lines = wrap(d, row["title"], f, maxw)
    y = int(H * 0.255)
    for ln in lines[:2]:
        d.text((lx, y), ln, font=f, fill=c["title"])
        y += int(f.size * 1.06)

    motif_top = max(int(H * 0.415), y + int(H * 0.015))
    motif(d, (lx, motif_top, int(W * BAND_X[1]), int(H * 0.675)), c, opts)

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
        r["accent"] = r.get("accent") or "violet"
    return rows


def hero_family(slug):
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
    seen, motifs_used = set(), set()
    for r in rows:
        if r["motif"] not in MOTIFS:
            bad.append("%s: unknown motif %r" % (r["slug"], r["motif"]))
        if r["motif"] in motifs_used:
            bad.append("%s: motif %r is already used by another post -- one "
                       "drawing per post is the whole point" % (r["slug"], r["motif"]))
        motifs_used.add(r["motif"])
        if r["ground"] not in GROUNDS:
            bad.append("%s: unknown ground %r" % (r["slug"], r["ground"]))
        if r["accent"] not in ACCENTS:
            bad.append("%s: unknown accent %r" % (r["slug"], r["accent"]))
        if r["out"] in seen:
            bad.append("%s: two posts write %s" % (r["slug"], r["out"]))
        seen.add(r["out"])
        if not (ROOT / "blog" / (r["slug"] + ".html")).exists():
            bad.append("%s: no such post" % r["slug"])
        fam = hero_family(r["slug"])
        if fam and r["ground"] in FORBIDDEN.get(fam, set()):
            bad.append("%s: ground %r is its own hero family (%s) -- the cover "
                       "will vanish into the hero" % (r["slug"], r["ground"], fam))
    posts = {p.stem for p in (ROOT / "blog").glob("*.html") if p.stem != "index"}
    for missing in sorted(posts - {r["slug"] for r in rows}):
        bad.append("%s has no row in covers.tsv" % missing)
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
    out = ROOT / ".covers" / "contact-sheet.jpg"
    out.parent.mkdir(exist_ok=True)
    sheet.save(out, "JPEG", quality=88, optimize=True)
    print("contact sheet: %s (%d covers, %.0f KB)"
          % (out.relative_to(ROOT), n, out.stat().st_size / 1024))
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
        print("covers.tsv OK -- %d rows, %d motifs, %d grounds, %d accents"
              % (len(rows), len({r["motif"] for r in rows}),
                 len({r["ground"] for r in rows}), len({r["accent"] for r in rows})))
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
