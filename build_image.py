#!/usr/bin/env python3
"""Build the entry image for make.fun bounty news-image-20261121.

Deterministic, offline, code-only: draws a 1024x1024 newspaper-style
front page with PIL using only the DejaVu fonts shipped with the OS and
the news text hard-coded below (see NEWS.md for sources).

Run:  python3 build_image.py            # writes assets/entry.png
      python3 build_image.py out.png    # writes to a custom path
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = Path(__file__).resolve().parent / "assets" / "entry.png"

PAPER = (248, 244, 236)
INK = (22, 19, 14)
MUTED = (90, 84, 72)
RED = (166, 27, 27)
NAVY = (31, 58, 95)
NAVY_DARK = (18, 34, 58)
GOLD = (192, 138, 43)
TEAL = (15, 118, 110)
GREEN = (46, 125, 50)
LIGHT = (238, 232, 220)
WHITE = (255, 255, 255)
ORANGE = (230, 126, 34)
YELLOW = (241, 196, 15)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, color, max_w, leading):
    lines = wrap(draw, text, fnt, max_w)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=color)
        y += leading
    return y


def rule(draw, x0, y, x1, color=INK, width=2):
    draw.line([(x0, y), (x1, y)], fill=color, width=width)


def burst(draw, cx, cy, r, color):
    """Simple starburst: 8 spokes + filled centre."""
    import math
    for k in range(8):
        a = math.pi * k / 4
        draw.line([(cx, cy), (cx + r * math.cos(a), cy + r * math.sin(a))],
                  fill=color, width=3)
    draw.ellipse([cx - r * 0.35, cy - r * 0.35, cx + r * 0.35, cy + r * 0.35],
                 fill=color)


def draw_lead_art(draw, x0, y0, x1, y1):
    """Schematic night-skyline panel for the lead story (no photos)."""
    draw.rectangle([x0, y0, x1, y1], fill=NAVY_DARK)
    # stars
    for sx, sy in [(18, 22), (70, 14), (130, 30), (200, 16), (250, 34),
                   (40, 55), (160, 48), (230, 60), (95, 70), (275, 78)]:
        draw.ellipse([x0 + sx - 2, y0 + sy - 2, x0 + sx + 2, y0 + sy + 2],
                     fill=YELLOW)
    # missile arcs
    draw.arc([x0 + 20, y0 + 10, x0 + 200, y0 + 150], 200, 330, fill=ORANGE, width=3)
    draw.arc([x0 + 90, y0 + 30, x0 + 290, y0 + 170], 210, 320, fill=YELLOW, width=2)
    # skyline
    base = y1
    buildings = [(0, 150, 46), (50, 110, 40), (94, 170, 52), (150, 120, 44),
                 (198, 160, 48), (250, 105, 42)]
    for bx, bh, bw in buildings:
        draw.rectangle([x0 + bx, base - bh, x0 + bx + bw, base], fill=(10, 20, 38))
        for wy in range(base - bh + 12, base - 10, 22):
            for wx in range(x0 + bx + 8, x0 + bx + bw - 6, 14):
                draw.rectangle([wx, wy, wx + 5, wy + 7], fill=(240, 200, 90))
    # explosions over the skyline
    burst(draw, x0 + 70, base - 130, 26, ORANGE)
    burst(draw, x0 + 225, base - 118, 20, YELLOW)
    burst(draw, x0 + 165, base - 185, 16, (255, 120, 60))
    draw.text((x0 + 10, y1 - 24), "KYIV  •  OVERNIGHT", font=font(SANS_B, 15),
              fill=WHITE)


def chip(draw, x, y, big, small):
    """Stat chip: big number over small label. Returns width used."""
    f_big = font(SANS_B, 26)
    f_small = font(SANS, 13)
    w = max(draw.textlength(big, font=f_big), draw.textlength(small, font=f_small)) + 22
    draw.rounded_rectangle([x, y, x + w, y + 56], radius=8,
                           outline=RED, width=2, fill=WHITE)
    draw.text((x + 11, y + 5), big, font=f_big, fill=RED)
    draw.text((x + 11, y + 33), small, font=f_small, fill=MUTED)
    return w


def story_card(draw, x, y, w, h, accent, kicker, headline, body, icon):
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=2, fill=WHITE)
    draw.rectangle([x, y, x + w, y + 6], fill=accent)
    # icon square
    ix, iy, s = x + 14, y + 20, 46
    draw.rectangle([ix, iy, ix + s, iy + s], fill=accent)
    icon(draw, ix, iy, s)
    tx = x + 72
    draw.text((tx, y + 18), kicker, font=font(SANS_B, 14), fill=accent)
    yy = para(draw, tx, y + 40, headline, font(SERIF_B, 23), INK, w - 86, 27)
    para(draw, x + 14, yy + 4, body, font(SANS, 16), (52, 48, 40), w - 28, 20)


def icon_chart(draw, x, y, s):
    bars = [(8, 14), (20, 22), (32, 10)]
    for bx, bh in bars:
        draw.rectangle([x + bx, y + s - 8 - bh, x + bx + 8, y + s - 8], fill=WHITE)
    draw.line([(x + 6, y + s - 14), (x + s - 6, y + 12)], fill=YELLOW, width=3)


def icon_scales(draw, x, y, s):
    cx, cy = x + s // 2, y + 8
    draw.line([(cx, cy), (cx, cy + 26)], fill=WHITE, width=3)
    draw.line([(cx - 13, cy + 4), (cx + 13, cy + 4)], fill=WHITE, width=3)
    for dx in (-13, 13):
        draw.line([(cx + dx, cy + 4), (cx + dx, cy + 14)], fill=WHITE, width=2)
        draw.arc([cx + dx - 7, cy + 10, cx + dx + 7, cy + 22], 0, 180,
                 fill=WHITE, width=2)
    draw.line([(cx - 10, cy + 26), (cx + 10, cy + 26)], fill=WHITE, width=3)


def icon_globe(draw, x, y, s):
    cx, cy = x + s // 2, y + s // 2
    draw.ellipse([cx - 15, cy - 15, cx + 15, cy + 15], outline=WHITE, width=3)
    draw.line([(cx - 15, cy), (cx + 15, cy)], fill=WHITE, width=2)
    draw.ellipse([cx - 7, cy - 15, cx + 7, cy + 15], outline=WHITE, width=2)


def icon_bridge(draw, x, y, s):
    draw.line([(x + 6, y + s - 10), (x + s - 6, y + s - 10)], fill=WHITE, width=3)
    draw.arc([x + 8, y + 10, x + s - 8, y + s - 2], 180, 360, fill=WHITE, width=3)
    draw.line([(x + s // 2, y + 12), (x + s // 2, y + s - 10)], fill=WHITE, width=2)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # outer frame
    d.rectangle([14, 14, W - 14, H - 14], outline=INK, width=3)

    # ---- masthead ----
    d.text((W // 2, 30), "THE WORLD IN ONE IMAGE",
           font=font(SANS_B, 17), fill=RED, anchor="ma")
    d.text((W // 2, 56), "THE WORLD TODAY",
           font=font(SERIF_B, 76), fill=INK, anchor="ma")
    rule(d, 36, 148, W - 36, INK, 3)
    rule(d, 36, 154, W - 36, INK, 1)
    d.text((W // 2, 162), "SATURDAY, 21 NOVEMBER 2026  •  SIX STORIES, ONE PAGE",
           font=font(SANS_B, 19), fill=INK, anchor="ma")

    # ---- lead story ----
    ly = 196
    d.text((36, ly), "LEAD STORY  —  WAR IN EUROPE",
           font=font(SANS_B, 16), fill=RED)
    draw_lead_art(d, 36, ly + 26, 336, ly + 238)
    tx = 356
    yy = para(d, tx, ly + 28,
              "Russia's biggest barrage hits Kyiv — and lands in Poland",
              font(SERIF_B, 33), INK, W - 36 - tx, 40)
    yy = para(d, tx, yy + 8,
              "Overnight, Russia fired 400+ drones and 110+ missiles at "
              "Ukraine, killing at least 8 and hitting three Kyiv bridges. "
              "Two missiles and a drone fell in Poland; PM Tusk called it "
              "a deliberate provocation.",
              font(SANS, 18), (52, 48, 40), W - 36 - tx, 24)
    cx = tx
    for big, small in [("400+", "DRONES"), ("110+", "MISSILES"),
                       ("8+", "KILLED"), ("3", "KYIV BRIDGES HIT")]:
        cx += chip(d, cx, ly + 196, big, small) + 12

    rule(d, 36, 458, W - 36, INK, 2)

    # ---- 2 x 2 story grid ----
    gy, gh, gw, gap = 474, 172, 464, 12
    story_card(d, 36, gy, gw, gh, RED, "MARKETS  •  NEW YORK",
               "AI rout drags Wall Street into correction",
               "S&P 500 fell 3.7% to 6,910 on Friday, 10%+ below its peak; "
               "Nasdaq plunged 5.3% and the Dow 1.9%. Nvidia tumbled 14% "
               "amid reports of an SEC probe.",
               icon_chart)
    story_card(d, 36 + gw + gap, gy, gw, gh, NAVY, "JUSTICE  •  THE HAGUE  (19 NOV)",
               "World court: Myanmar committed genocide",
               "The ICJ ruled 9–6 that Myanmar committed genocide against "
               "the Rohingya in 2017 — a first for any state — and ordered "
               "reparations.",
               icon_scales)
    story_card(d, 36, gy + gh + 12, gw, gh, TEAL, "CLIMATE  •  ANTALYA, TURKEY",
               "COP31 deadlocked as fossil fuels vanish from draft",
               "Nearly 200 nations ran past the deadline into overtime after "
               "a draft deal dropped all mention of coal, oil and gas. "
               "Panama threatened to block a deal.",
               icon_globe)
    story_card(d, 36 + gw + gap, gy + gh + 12, gw, gh, GREEN, "EUROPE  •  BRUSSELS",
               "UK and EU sign biggest post-Brexit deals",
               "Three agreements scrap most food and farm checks, link carbon "
               "markets and open a youth mobility scheme — the closest ties "
               "since Brexit.",
               icon_bridge)

    # ---- wide diplomacy band ----
    by = 844
    d.rectangle([36, by, W - 36, by + 82], outline=INK, width=2, fill=LIGHT)
    d.rectangle([36, by, 44, by + 82], fill=GOLD)
    d.text((60, by + 10), "DIPLOMACY  •  SHENZHEN",
           font=font(SANS_B, 14), fill=(122, 84, 18))
    para(d, 60, by + 30,
         "Trump, Xi and Putin issue joint peace declaration after their "
         "first three-way summit — hours before Russia's barrage on Ukraine.",
         font(SERIF_B, 19), INK, W - 36 - 60 - 14, 24)

    # ---- also strip ----
    ay = 936
    d.text((36, ay), "ALSO:  ", font=font(SANS_B, 15), fill=RED)
    d.text((100, ay),
           "Pancreatic-cancer pill made tumours undetectable in 1 in 12 trial "
           "patients  •  FBI criminal database reportedly hacked",
           font=font(SANS, 15), fill=MUTED)

    # ---- footer ----
    rule(d, 36, 962, W - 36, MUTED, 1)
    d.text((W // 2, 972),
           "Sources: AP, Reuters, The Times, Investopedia, WSJ, Le Monde, "
           "UN / IIMM, HRW, BBC — figures as reported 20–21 Nov 2026.",
           font=font(SANS, 13), fill=MUTED, anchor="ma")
    d.text((W // 2, 990),
           "Illustrated news summary drawn in code — not a photograph.",
           font=font(SANS, 12), fill=MUTED, anchor="ma")

    out = Path(sys.argv[1]) if len(sys.argv) > 1 else OUT
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, format="PNG", optimize=True)
    return out


if __name__ == "__main__":
    p = build()
    print(f"wrote {p} ({p.stat().st_size} bytes, 1024x1024)")
