#!/usr/bin/env python3
"""Draw a post cover in the house visual language.

Two posts wore another post's cover (INV-07a's long-standing pair). The
a11y-perf skill is explicit that the fix is a dedicated cover, not a reworded
alt — so these are drawn rather than borrowed.

The language is deliberately the BOOK JACKETS', not the AI clip-art the rest of
the corpus wears: a deep gradient ground in the post's own hero family, flat
geometric forms, one gold accent, and real typography. Flat art, so PNG-then-JPEG
at the house budget (<=200 KB, 800x800 to match every other cover).

    python3 scripts/make_cover.py memory-architecture
    python3 scripts/make_cover.py vibe-coding
"""
import pathlib
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = pathlib.Path(__file__).resolve().parents[1]
FONTS = pathlib.Path("/private/tmp/claude-501/-Users-anirach-Documents-Anirach-github-io/"
                     "bed2c623-bbc4-4ff7-92b6-a51793171070/scratchpad/fonts")
GOLD = (196, 164, 108)
CREAM = (250, 247, 240)
S = 1600  # drawn at 2x then downsampled, so edges and type stay crisp


def font(px, weight="Bold"):
    for name in (f"Inter-{weight}.ttf", "Inter-var.ttf", "Inter-Regular.ttf"):
        p = FONTS / name
        if p.exists():
            try:
                f = ImageFont.truetype(str(p), px)
                if name == "Inter-var.ttf":
                    try:
                        f.set_variation_by_name("Bold" if weight == "Bold" else "Regular")
                    except Exception:
                        pass
                return f
            except Exception:
                continue
    return ImageFont.load_default()


def gradient(stops):
    """Diagonal gradient from a list of (position, rgb)."""
    g = Image.new("RGB", (S, S))
    px = g.load()
    for y in range(S):
        for x in range(0, S, 8):
            t = (x / S * 0.55 + y / S * 0.45)
            for i in range(len(stops) - 1):
                p0, c0 = stops[i]
                p1, c1 = stops[i + 1]
                if p0 <= t <= p1:
                    k = (t - p0) / (p1 - p0) if p1 > p0 else 0
                    col = tuple(int(c0[j] + (c1[j] - c0[j]) * k) for j in range(3))
                    break
            else:
                col = stops[-1][1]
            for dx in range(8):
                if x + dx < S:
                    px[x + dx, y] = col
    return g


def rounded(d, box, r, outline=None, fill=None, width=4):
    d.rounded_rectangle(box, radius=r, outline=outline, fill=fill, width=width)


def memory_architecture():
    """Three memory tiers as stacked, offset planes — short-term feeding
    long-term. The motif is the post's actual subject, not decoration."""
    img = gradient([(0.0, (0x13, 0x4e, 0x4a)), (0.45, (0x11, 0x5e, 0x59)),
                    (1.0, (0x0f, 0x76, 0x6e))])
    d = ImageDraw.Draw(img, "RGBA")
    # faint grid, the "structure" note
    for i in range(0, S, 100):
        d.line([(i, 0), (i, S)], fill=(255, 255, 255, 12), width=2)
        d.line([(0, i), (S, i)], fill=(255, 255, 255, 12), width=2)

    # positions chosen so the boxes never overlap and each arrow has clear air:
    # box height .105, pitch .155 -> a .05 gap the arrow lives in.
    tiers = [(0.355, 0.26, "SESSION"), (0.510, 0.20, "WORKING"), (0.665, 0.14, "LONG-TERM")]
    for idx, (ty, alpha, label) in enumerate(tiers):
        w, h = int(S * 0.56), int(S * 0.105)
        x = int(S * 0.20) + idx * int(S * 0.030)
        y = int(S * ty)
        d.rounded_rectangle([x, y, x + w, y + h], radius=26,
                            fill=(255, 255, 255, int(alpha * 90)),
                            outline=(*GOLD, 200) if idx == 2 else (255, 255, 255, 110),
                            width=5)
        d.text((x + 40, y + h // 2 - 20), label, font=font(34), fill=(255, 255, 255, 235))
        if idx < 2:                                   # the flow between tiers
            cx = x + w // 2
            d.line([(cx, y + h + 10), (cx, y + h + 48)], fill=(*GOLD, 220), width=6)
            d.polygon([(cx - 14, y + h + 46), (cx + 14, y + h + 46), (cx, y + h + 72)],
                      fill=(*GOLD, 230))

    d.text((int(S * 0.20), int(S * 0.135)), "OPENCLAW", font=font(40), fill=(*GOLD, 255))
    d.text((int(S * 0.20), int(S * 0.175)), "Memory", font=font(112), fill=(255, 255, 255))
    d.text((int(S * 0.20), int(S * 0.235)), "Architecture", font=font(112), fill=(255, 255, 255))
    d.line([(int(S * 0.20), int(S * 0.825)), (int(S * 0.34), int(S * 0.825))],
           fill=(*GOLD, 255), width=8)
    d.text((int(S * 0.20), int(S * 0.850)), "ออกแบบความจำให้ Agent ทำงานต่อเนื่อง",
           font=ImageFont.truetype(str(FONTS / "Sarabun-Regular.ttf"), 42)
           if (FONTS / "Sarabun-Regular.ttf").exists() else font(42, "Regular"),
           fill=(255, 255, 255, 190))
    return img


def vibe_coding():
    """A four-stage pipeline with one stage lit — 'ship fast without breaking
    the system' is a process picture, so the cover is the process."""
    img = gradient([(0.0, (0x2e, 0x10, 0x65)), (0.45, (0x4c, 0x1d, 0x95)),
                    (1.0, (0x6d, 0x28, 0xd9))])
    d = ImageDraw.Draw(img, "RGBA")
    for i in range(0, S, 100):
        d.line([(i, 0), (i, S)], fill=(255, 255, 255, 12), width=2)
        d.line([(0, i), (S, i)], fill=(255, 255, 255, 12), width=2)

    labels = ["PROMPT", "REVIEW", "TEST", "SHIP"]
    n = len(labels)
    box = int(S * 0.155)
    gap = int(S * 0.045)
    total = n * box + (n - 1) * gap
    x0 = (S - total) // 2
    y = int(S * 0.44)
    for i, lab in enumerate(labels):
        x = x0 + i * (box + gap)
        lit = i == n - 1
        d.rounded_rectangle([x, y, x + box, y + box], radius=26,
                            fill=(*GOLD, 45) if lit else (255, 255, 255, 26),
                            outline=(*GOLD, 235) if lit else (255, 255, 255, 120), width=5)
        tw = d.textlength(lab, font=font(30))
        d.text((x + box // 2 - tw // 2, y + box // 2 - 16), lab, font=font(30),
               fill=(255, 255, 255, 240))
        if i < n - 1:
            cx = x + box + gap // 2
            d.line([(x + box + 10, y + box // 2), (cx + 12, y + box // 2)],
                   fill=(255, 255, 255, 170), width=6)
            d.polygon([(cx + 8, y + box // 2 - 12), (cx + 8, y + box // 2 + 12),
                       (cx + 30, y + box // 2)], fill=(255, 255, 255, 190))

    d.text((int(S * 0.16), int(S * 0.175)), "DEVOPS PROCESS", font=font(40), fill=(*GOLD, 255))
    d.text((int(S * 0.16), int(S * 0.215)), "Vibe Coding", font=font(120), fill=(255, 255, 255))
    d.line([(int(S * 0.16), int(S * 0.70)), (int(S * 0.30), int(S * 0.70))],
           fill=(*GOLD, 255), width=8)
    d.text((int(S * 0.16), int(S * 0.725)), "ใช้ AI ให้เร็วขึ้นแบบไม่พังระบบ",
           font=ImageFont.truetype(str(FONTS / "Sarabun-Regular.ttf"), 46)
           if (FONTS / "Sarabun-Regular.ttf").exists() else font(46, "Regular"),
           fill=(255, 255, 255, 195))
    return img


COVERS = {
    "memory-architecture": (memory_architecture, "openclaw-memory-architecture-cover.jpg"),
    "vibe-coding": (vibe_coding, "vibe-coding-devops-process-cover.jpg"),
}


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] not in COVERS:
        print(__doc__)
        return 2
    fn, out = COVERS[sys.argv[1]]
    img = fn().resize((800, 800), Image.LANCZOS)
    img = img.filter(ImageFilter.UnsharpMask(radius=1.2, percent=55, threshold=3))
    path = ROOT / "images" / out
    img.save(path, "JPEG", quality=86, optimize=True, progressive=True)
    kb = path.stat().st_size / 1024
    print(f"{out}: 800x800, {kb:.0f} KB {'OK' if kb <= 200 else 'OVER BUDGET'}")
    return 0 if kb <= 200 else 1


if __name__ == "__main__":
    sys.exit(main())
