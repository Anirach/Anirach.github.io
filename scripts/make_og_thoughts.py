#!/usr/bin/env python3
"""Draw images/og-thoughts.jpg — the 1200x630 share card for /thoughts/.

The Thoughts catalog (2026-09-08) is the one section page whose share card is
neither the generic site card nor a post's own: it is the sunrise of *One Day of
Light* — the Sunrise ground every Life essay's hero uses, a gold sun on the
horizon, and the section's name. Same visual language as scripts/make_cover.py
(house tokens only, Inter + Sarabun from scripts/fonts), written as its own
script because it is one card, not a spec table.

    python3 scripts/make_og_thoughts.py          # writes images/og-thoughts.jpg
"""
import pathlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = pathlib.Path(__file__).resolve().parents[1]
FONTS = ROOT / "scripts" / "fonts"
OUT = ROOT / "images" / "og-thoughts.jpg"
W, H = 1200, 630

NAVY = (17, 48, 75)          # --navy
SLATE = (51, 65, 85)         # --slate
GOLD = (196, 164, 108)       # --gold
GOLD_DARK = (122, 95, 34)    # --gold-dark
SUNRISE = [(0.0, (0xee, 0xf3, 0xf3)), (0.5, (0xde, 0xe7, 0xe6)), (1.0, (0xe9, 0xe1, 0xc4))]


def font(px, weight="Bold"):
    f = ImageFont.truetype(str(FONTS / "Inter-var.ttf"), px)
    try:
        f.set_variation_by_name(weight)
    except Exception:
        pass
    return f


def thai(px):
    return ImageFont.truetype(str(FONTS / "Sarabun-Regular.ttf"), px)


def ground():
    """The Sunrise gradient at 135deg — the same three stops as the CSS."""
    ys, xs = np.mgrid[0:H, 0:W]
    t = (xs / W) * 0.55 + (ys / H) * 0.45
    out = np.zeros((H, W, 3))
    for i in range(len(SUNRISE) - 1):
        p0, c0 = SUNRISE[i]
        p1, c1 = SUNRISE[i + 1]
        m = (t >= p0) & (t <= p1)
        k = np.clip((t - p0) / (p1 - p0), 0, 1)
        for c in range(3):
            out[..., c] = np.where(m, c0[c] + (c1[c] - c0[c]) * k, out[..., c])
    return Image.fromarray(out.astype("uint8"), "RGB")


def main():
    img = ground().convert("RGBA")

    # --- the sun: a soft halo, then a gold disc rising through the horizon
    horizon = 452
    cx, r = 1010, 140
    halo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(halo)
    for i in range(14):                       # 14 faint rings, then one wide blur
        k = 2.4 - i * 0.1
        hd.ellipse((cx - r * k, horizon - r * k, cx + r * k, horizon + r * k),
                   fill=GOLD + (7,))
    halo = halo.filter(ImageFilter.GaussianBlur(40))
    img = Image.alpha_composite(img, halo)

    d = ImageDraw.Draw(img)
    # ground band below the horizon, slightly deeper parchment
    d.rectangle((0, horizon, W, H), fill=(0xe4, 0xdb, 0xbb, 255))
    # the disc, clipped by the horizon
    disc = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dd = ImageDraw.Draw(disc)
    dd.ellipse((cx - r, horizon - r, cx + r, horizon + r), fill=GOLD + (255,))
    dd.rectangle((0, horizon, W, H), fill=(0, 0, 0, 0))
    img = Image.alpha_composite(img, disc)
    d = ImageDraw.Draw(img)
    # horizon line
    d.line((0, horizon, W, horizon), fill=NAVY + (255,), width=3)
    # a walking figure with a lamp, as on the book cover — stick figure, navy
    fx, fy = 836, horizon
    d.line((fx, fy - 46, fx, fy - 18), fill=NAVY, width=4)            # body
    d.ellipse((fx - 7, fy - 62, fx + 7, fy - 48), fill=NAVY)           # head
    d.line((fx, fy - 18, fx - 10, fy), fill=NAVY, width=4)             # legs
    d.line((fx, fy - 18, fx + 12, fy), fill=NAVY, width=4)
    d.line((fx, fy - 40, fx + 22, fy - 30), fill=NAVY, width=4)        # arm
    d.ellipse((fx + 17, fy - 34, fx + 29, fy - 22), fill=GOLD, outline=NAVY, width=2)  # lamp

    # --- type, left column
    x = 84
    eyebrow = "THOUGHTS · LIFE & PHILOSOPHY"
    d.text((x, 118), eyebrow, font=font(26, "SemiBold"), fill=GOLD_DARK)
    d.line((x, 162, x + 96, 162), fill=GOLD, width=4)
    title_f = font(92, "Black")
    d.text((x, 190), "One Day", font=title_f, fill=NAVY)
    d.text((x, 290), "of Light", font=title_f, fill=NAVY)
    d.text((x, 410), "Nine essays on living, working, and what remains",
           font=font(30, "Regular"), fill=SLATE)
    d.text((x, 478), "แสงของวันหนึ่ง — ความเรียงเก้าบท ว่าด้วยชีวิต การงาน และสิ่งที่ตกผลึกภายใน",
           font=thai(30), fill=SLATE)
    d.text((x, 548), "Anirach Mingkhwan · anirach.com/thoughts", font=font(24, "Medium"), fill=NAVY)

    img.convert("RGB").save(OUT, "JPEG", quality=86, optimize=True, progressive=True)
    print("wrote", OUT.relative_to(ROOT), OUT.stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main()
