#!/usr/bin/env python3
"""Draw the v2 front page for news-image-20261118.

Renders entry.png (1024x1024): a dense broadsheet front page copying
the winning formula of the top-5 entries — masthead with a story count,
3 big leads, a numbered 6-story grid with REGION x BEAT tags, a
BY THE NUMBERS strip, a dotted world map with numbered pins, and
16 one-line briefs continuing the numbering (25 stories in total).
Everything is drawn with PIL shapes; no photographs, no network.
Run: python3 draw.py  (writes entry.png next to this file)
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (253, 251, 243)      # warm off-white
INK = (17, 17, 17)           # near-black
RED = (176, 30, 30)          # middle east
BLUE = (31, 80, 150)         # europe
GREEN = (27, 120, 70)        # asia
ORANGE = (198, 102, 18)      # americas
BROWN = (120, 72, 40)        # africa
TEAL = (14, 120, 120)        # oceania
PURPLE = (110, 60, 150)      # global
GREY = (90, 90, 88)
SEA = (186, 211, 228)
LAND = (232, 220, 192)
LAND_LINE = (150, 135, 100)
BOX = (242, 238, 228)        # number-strip box fill

F_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
F_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

MX = 32                      # side margin
RW = W - 2 * MX              # content width (960)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, fnt, max_w):
    """Greedy word wrap to a pixel width; returns a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if fnt.getlength(t) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_font(text, path, start, max_w):
    """Largest font size (<= start) at which text fits max_w."""
    size = start
    while size > 8:
        fnt = ImageFont.truetype(path, size)
        if fnt.getlength(text) <= max_w:
            return fnt
        size -= 1
    return ImageFont.truetype(path, 8)


def draw_para(d, x, y, lines, fnt, fill=INK, leading=None):
    """Draw wrapped lines; returns y just below the last line."""
    if leading is None:
        leading = int(fnt.size * 1.28)
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def fit_lines(text, path, start, max_w, max_lines):
    """Largest font size (<= start) at which text wraps to <= max_lines."""
    size = start
    while size > 8:
        fnt = ImageFont.truetype(path, size)
        if len(wrap(text, fnt, max_w)) <= max_lines:
            return fnt
        size -= 1
    return ImageFont.truetype(path, 8)


def burst(d, cx, cy, r, fill=RED):
    """8-point starburst (explosion marker)."""
    pts = []
    for i in range(16):
        ang = math.pi * i / 8
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=fill, outline=INK)


def label(d, x, y, text, fnt, fill=INK, halo=(255, 255, 255)):
    """Small label with a white halo so it stays legible over art."""
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        d.text((x + dx, y + dy), text, font=fnt, fill=halo)
    d.text((x, y), text, font=fnt, fill=fill)


# ------------------------------------------------------------------ icons
def icon_capitol(d, x, y, s=28):
    d.polygon([(x + s // 2, y + 1), (x + 4, y + 8), (x + s - 4, y + 8)],
              outline=INK, width=2)
    d.arc([x + s // 2 - 5, y + 1, x + s // 2 + 5, y + 10], 180, 360,
          fill=INK, width=2)
    for cx in (x + 6, x + s // 2, x + s - 6):
        d.line([(cx, y + 10), (cx, y + s - 6)], fill=INK, width=2)
    d.line([(x + 1, y + s - 4), (x + s - 1, y + s - 4)], fill=INK, width=2)


def icon_euro(d, x, y, s=28):
    d.ellipse([x + 1, y + 1, x + s - 1, y + s - 1], fill=BLUE, outline=INK,
              width=2)
    d.text((x + s // 2, y + s // 2), "\u20ac", font=font(F_SANS_B, 16),
           fill=(255, 255, 255), anchor="mm")


def icon_cyclone(d, x, y, s=28):
    d.arc([x + 2, y + 2, x + s - 2, y + s - 2], 0, 300, fill=INK, width=2)
    d.arc([x + 7, y + 7, x + s - 7, y + s - 7], 120, 420, fill=INK, width=2)
    d.ellipse([x + s // 2 - 3, y + s // 2 - 3, x + s // 2 + 3,
               y + s // 2 + 3], fill=RED)


def icon_satellite(d, x, y, s=28):
    d.rectangle([x + 10, y + 10, x + 18, y + 18], fill=INK)
    d.rectangle([x + 1, y + 8, x + 9, y + 20], outline=INK, width=2)
    d.rectangle([x + 19, y + 8, x + 27, y + 20], outline=INK, width=2)
    d.line([(x + 14, y + 18), (x + 20, y + 26)], fill=INK, width=2)
    d.line([(x + 20, y + 26), (x + 26, y + 22)], fill=INK, width=2)


def icon_chip(d, x, y, s=28):
    d.rectangle([x + 6, y + 6, x + s - 6, y + s - 6], fill=INK)
    d.rectangle([x + 11, y + 11, x + s - 11, y + s - 11], fill=GREEN)
    for i in range(3):
        yy = y + 9 + i * 6
        d.line([(x + 1, yy), (x + 6, yy)], fill=INK, width=2)
        d.line([(x + s - 6, yy), (x + s - 1, yy)], fill=INK, width=2)
        xx = x + 9 + i * 6
        d.line([(xx, y + 1), (xx, y + 6)], fill=INK, width=2)
        d.line([(xx, y + s - 6), (xx, y + s - 1)], fill=INK, width=2)


def icon_controller(d, x, y, s=28):
    d.rounded_rectangle([x + 1, y + 6, x + s - 1, y + s - 6], radius=6,
                        outline=INK, width=2)
    d.line([(x + 7, y + 13), (x + 11, y + 13)], fill=INK, width=2)
    d.line([(x + 9, y + 11), (x + 9, y + 15)], fill=INK, width=2)
    d.ellipse([x + 17, y + 11, x + 20, y + 14], fill=RED)
    d.ellipse([x + 21, y + 15, x + 24, y + 18], fill=INK)


# ------------------------------------------------------- lead illustrations
def ill_gulf(d, x, y, w, h):
    """Schematic Strait of Hormuz."""
    d.rectangle([x, y, x + w, y + h], fill=SEA, outline=INK, width=2)
    d.polygon([(x, y), (x + w, y), (x + w, y + 26), (x + 250, y + 36),
               (x + 170, y + 28), (x + 80, y + 40), (x, y + 32)],
              fill=LAND, outline=LAND_LINE)
    d.polygon([(x, y + h), (x, y + 62), (x + 55, y + 54), (x + 100, y + 66),
               (x + 118, y + h)],
              fill=LAND, outline=LAND_LINE)
    d.ellipse([x + 228, y + 38, x + 262, y + 48], fill=LAND,
              outline=LAND_LINE)
    d.ellipse([x + 148, y + 52, x + 160, y + 62], fill=LAND,
              outline=LAND_LINE)
    burst(d, x + 245, y + 43, 8)
    burst(d, x + 62, y + 60, 7)
    burst(d, x + 154, y + 57, 7)
    lab = font(F_SANS_B, 10)
    label(d, x + 252, y + 26, "QESHM", lab)
    label(d, x + 6, y + 46, "KUWAIT", lab)
    label(d, x + 162, y + 44, "BAHRAIN", lab)


def ill_bridge(d, x, y, w, h):
    """Broken Kerch bridge over the strait."""
    d.rectangle([x, y, x + w, y + h], fill=PAPER, outline=INK, width=2)
    d.rectangle([x, y + 48, x + w, y + h], fill=SEA)
    d.line([(x + 30, y + 48), (x + 30, y + 10)], fill=INK, width=3)
    d.line([(x + w - 30, y + 48), (x + w - 30, y + 10)], fill=INK, width=3)
    d.line([(x + 30, y + 14), (x + w // 2 - 8, y + 14)], fill=INK, width=4)
    d.line([(x + w // 2 + 8, y + 22), (x + w - 30, y + 16)], fill=INK,
           width=4)
    d.line([(x + 30, y + 48), (x + w - 30, y + 48)], fill=INK, width=2)
    burst(d, x + w // 2, y + 20, 9)
    lab = font(F_SANS_B, 9)
    label(d, x + 8, y + 56, "KERCH STRAIT", lab)
    label(d, x + w - 78, y + 56, "ROAD SPAN DOWN", lab)


def ill_summit(d, x, y, w, h):
    """Two leaders at a summit table."""
    d.rectangle([x, y, x + w, y + h], fill=PAPER, outline=INK, width=2)
    # figures
    d.ellipse([x + 62, y + 8, x + 92, y + 38], fill=(222, 190, 160),
              outline=INK, width=2)
    d.pieslice([x + 48, y + 36, x + 106, y + 66], 180, 360,
               fill=(40, 60, 90), outline=INK, width=2)
    d.ellipse([x + w - 92, y + 8, x + w - 62, y + 38],
              fill=(222, 190, 160), outline=INK, width=2)
    d.pieslice([x + w - 106, y + 36, x + w - 48, y + 66], 180, 360,
               fill=(90, 40, 40), outline=INK, width=2)
    # table
    d.rectangle([x + 20, y + 52, x + w - 20, y + 62], fill=(150, 110, 70),
                outline=INK, width=2)
    # flags on the table: China (red) and Russia (white/blue/red)
    fx = x + w // 2 - 34
    d.rectangle([fx, y + 26, fx + 26, y + 42], fill=(222, 30, 30),
                outline=INK, width=1)
    d.text((fx + 5, y + 29), "\u2605", font=font(F_SANS, 9),
           fill=(255, 220, 0))
    fx = x + w // 2 + 8
    d.rectangle([fx, y + 26, fx + 26, y + 42], outline=INK, width=1)
    d.rectangle([fx, y + 26, fx + 26, y + 31], fill=(255, 255, 255))
    d.rectangle([fx, y + 31, fx + 26, y + 36], fill=(0, 60, 180))
    d.rectangle([fx, y + 36, fx + 26, y + 42], fill=(220, 30, 30))
    lab = font(F_SANS_B, 10)
    label(d, x + 8, y + 64, "SHENZHEN", lab)


# ------------------------------------------------------------- world map
def point_in_poly(px, py, poly):
    """Ray-casting point-in-polygon test."""
    inside = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if ((yi > py) != (yj > py)) and (
                px < (xj - xi) * (py - yi) / (yj - yi) + xi):
            inside = not inside
        j = i
    return inside


# Simplified continent outlines in a 608 x 124 map box.
CONTINENTS = [
    # North America
    [(18, 18), (95, 8), (150, 14), (168, 34), (150, 62), (118, 74),
     (80, 72), (38, 52), (14, 34)],
    # Greenland
    [(150, 6), (172, 4), (178, 12), (160, 16)],
    # South America
    [(168, 78), (205, 72), (228, 92), (216, 118), (190, 122), (172, 100)],
    # Europe
    [(300, 14), (338, 8), (356, 22), (344, 44), (312, 48), (294, 30)],
    # Africa
    [(300, 52), (348, 46), (372, 68), (356, 104), (322, 112), (298, 84)],
    # Asia
    [(360, 8), (540, 4), (590, 18), (586, 44), (540, 60), (492, 66),
     (448, 58), (404, 44), (366, 30)],
    # SE Asia islands
    [(470, 66), (490, 62), (500, 74), (480, 78)],
    # Australia
    [(492, 88), (556, 84), (572, 100), (540, 116), (498, 112)],
]


def draw_world_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 244, 248), outline=INK,
                width=2)
    step = 7
    for gx in range(4, w - 2, step):
        for gy in range(4, h - 2, step):
            if any(point_in_poly(gx, gy, poly) for poly in CONTINENTS):
                d.ellipse([x + gx - 2, y + gy - 2, x + gx + 2, y + gy + 2],
                          fill=(70, 70, 70))
    # pins: (number, local x, local y, colour)
    pins = [
        (1, 470, 42, RED),      # Gulf
        (2, 352, 32, BLUE),     # Kerch
        (3, 522, 54, GREEN),    # Shenzhen
        (4, 55, 24, ORANGE),    # Alaska
        (5, 308, 28, BLUE),     # Brussels
        (6, 478, 64, GREEN),    # Odisha / Bay of Bengal
        (8, 78, 50, ORANGE),    # Silicon Valley
    ]
    nf = font(F_SANS_B, 11)
    for num, px, py, col in pins:
        d.ellipse([x + px - 9, y + py - 9, x + px + 9, y + py + 9],
                  fill=col, outline=INK, width=1)
        d.text((x + px, y + py), str(num), font=nf, fill=(255, 255, 255),
               anchor="mm")


# ------------------------------------------------------------------ page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ------------------------------------------------------
    d.text((W // 2, 8), "THE WORLD TODAY", font=font(F_SERIF_B, 54),
           fill=INK, anchor="ma")
    d.text((W // 2, 66), "25 STORIES \u00b7 6 CONTINENTS \u00b7 ONE PAGE",
           font=font(F_SANS_B, 20), fill=RED, anchor="ma")
    d.text((W // 2, 90),
           "Everything on this page happened, or was first reported, on "
           "Wednesday 18 November 2026.",
           font=font(F_SERIF, 15), fill=GREY, anchor="ma")
    d.line([(MX, 110), (W - MX, 110)], fill=INK, width=3)
    d.line([(MX, 115), (W - MX, 115)], fill=INK, width=1)

    # ---- black date band ----------------------------------------------
    d.rectangle([MX, 122, W - MX, 148], fill=INK)
    d.text((W // 2, 135), "WEDNESDAY 18 NOVEMBER 2026",
           font=font(F_SANS_B, 21), fill=(255, 255, 255), anchor="mm")

    # ---- 3 leads -------------------------------------------------------
    lead_xs = [MX, MX + 304 + 24, MX + 2 * (304 + 24)]
    leads = [
        ("MIDDLE EAST \u00b7 IRAN WAR", RED, "IRAN HITS US BASES IN GULF",
         ill_gulf,
         "US jets hit an IRGC missile site on Qeshm Island; Iran struck "
         "Ali Al Salem Air Base in Kuwait and a US radar site in "
         "Bahrain, and downed a US MQ-9."),
        ("EUROPE \u00b7 UKRAINE WAR", BLUE, "KERCH BRIDGE HIT AGAIN",
         ill_bridge,
         "Ukrainian strikes hit the bridge a second day; part of the "
         "road span fell into the strait and one arch collapsed."),
        ("ASIA \u00b7 DIPLOMACY", GREEN, "XI AND PUTIN MEET IN SHENZHEN",
         ill_summit,
         "Xi and Putin met in Shenzhen ahead of Thursday\u2019s "
         "trilateral with Trump; Xi pledged against trade "
         "protectionism, Putin criticised Western sanctions."),
    ]
    for i, (tag, col, head, ill, summ) in enumerate(leads):
        lx = lead_xs[i]
        d.text((lx, 156), tag, font=font(F_SANS_B, 13), fill=col)
        hf = fit_lines(head, F_SERIF_B, 26, 304, 2)
        hlines = wrap(head, hf, 304)
        hy = 176
        for ln in hlines:
            d.text((lx, hy), ln, font=hf, fill=INK)
            hy += 28
        ill(d, lx, 232, 304, 76)
        slines = wrap(summ, font(F_SERIF, 13), 304)
        draw_para(d, lx, 314, slines, font(F_SERIF, 13), leading=15)

    d.line([(MX, 376), (W - MX, 376)], fill=INK, width=2)

    # ---- numbered grid, stories 4-9 -----------------------------------
    stories = [
        (4, "NORTH AMERICA \u00b7 POLITICS", ORANGE, "PELTOLA WINS ALASKA",
         icon_capitol,
         "Peltola beat Sen. Dan Sullivan; Democrats projected to a "
         "56\u201344 majority."),
        (5, "EUROPE \u00b7 UKRAINE WAR", BLUE, "EU\u2019S \u20ac45BN UKRAINE LOAN",
         icon_euro,
         "\u20ac45bn for 2027 \u2014 \u20ac25bn military, \u20ac20bn budget "
         "\u2014 repaid only after Russia pays reparations."),
        (6, "ASIA \u00b7 WEATHER", GREEN, "CYCLONE AKVAN NEARS INDIA",
         icon_cyclone,
         "Severe storm in the Bay of Bengal; landfall 20 Nov, gusts "
         "145 km/h; Odisha evacuates 200,000."),
        (7, "GLOBAL \u00b7 SCIENCE", PURPLE, "VOYAGER 1, ONE LIGHT-DAY OUT",
         icon_satellite,
         "First object one light-day from Earth \u2014 25.9bn km; a radio "
         "signal now takes 24 hours one way."),
        (8, "GLOBAL \u00b7 TECH", PURPLE, "NVIDIA REVENUE DOUBLES",
         icon_chip,
         "$115.8bn revenue, up 103%, beating its $108bn guide; first "
         "results since CEO Huang resigned."),
        (9, "GLOBAL \u00b7 CULTURE", PURPLE, "GTA VI LANDS TOMORROW",
         icon_controller,
         "Launches 19 Nov; about 14.9m pre-orders worth $1.45bn "
         "(Sensor Tower); Metacritic 99."),
    ]
    cell_w, cell_h = 304, 97
    for i, (num, tag, col, head, icon, summ) in enumerate(stories):
        cx = lead_xs[i % 3]
        cy = 384 + (i // 3) * (cell_h + 8)
        # number badge
        d.ellipse([cx, cy, cx + 24, cy + 24], fill=col, outline=INK,
                  width=1)
        d.text((cx + 12, cy + 12), str(num), font=font(F_SANS_B, 13),
               fill=(255, 255, 255), anchor="mm")
        d.text((cx + 30, cy + 4), tag, font=font(F_SANS_B, 11), fill=col)
        # headline, fitted to the space left of the icon
        hf = fit_font(head, F_SERIF_B, 17, 264)
        d.text((cx, cy + 28), head, font=hf, fill=INK)
        icon(d, cx + 272, cy + 26, 28)
        slines = wrap(summ, font(F_SERIF, 12), 304)
        draw_para(d, cx, cy + 52, slines[:2], font(F_SERIF, 12),
                  leading=15)

    d.line([(MX, 590), (W - MX, 590)], fill=INK, width=1)

    # ---- BY THE NUMBERS strip -----------------------------------------
    box_w, box_h = 228, 60
    numbers = [
        ("56\u201344", "US SENATE SEATS, DEMOCRATS"),
        ("$115.8bn", "NVIDIA REVENUE, UP 103%"),
        ("200,000", "ODISHA EVACUATIONS"),
        ("25.9bn km", "VOYAGER 1 FROM EARTH"),
    ]
    for i, (big, small) in enumerate(numbers):
        bx = MX + i * (228 + 16)
        d.rectangle([bx, 598, bx + box_w, 598 + box_h], fill=BOX,
                    outline=INK, width=2)
        bf = fit_font(big, F_SERIF_B, 28, box_w - 16)
        d.text((bx + box_w // 2, 606), big, font=bf, fill=INK, anchor="ma")
        d.text((bx + box_w // 2, 636), small, font=font(F_SANS_B, 11),
               fill=GREY, anchor="ma")

    # ---- WHERE IT HAPPENED map + legend --------------------------------
    d.text((MX, 664), "WHERE IT HAPPENED", font=font(F_SANS_B, 16),
           fill=INK)
    d.text((W - MX, 664), "PINS MARK STORIES 1\u20139",
           font=font(F_SANS_B, 11), fill=GREY, anchor="ra")
    draw_world_map(d, MX, 686, 608, 122)
    # legend
    lx = 656
    d.text((lx, 686), "REGIONS", font=font(F_SANS_B, 13), fill=INK)
    legend = [
        (RED, "MIDDLE EAST \u2014 1"),
        (BLUE, "EUROPE \u2014 2, 5"),
        (GREEN, "ASIA \u2014 3, 6"),
        (ORANGE, "AMERICAS \u2014 4, 8"),
        (BROWN, "AFRICA \u2014 briefs 12, 17"),
        (TEAL, "OCEANIA \u2014 brief 14"),
        (PURPLE, "GLOBAL \u2014 7, 9 (no pin)"),
    ]
    ly = 702
    for col, txt in legend:
        d.rectangle([lx, ly + 1, lx + 12, ly + 13], fill=col, outline=INK,
                    width=1)
        d.text((lx + 18, ly), txt, font=font(F_SANS_B, 12), fill=INK)
        ly += 16

    d.line([(MX, 818), (W - MX, 818)], fill=INK, width=1)

    # ---- briefs 10-25 ---------------------------------------------------
    d.text((MX, 824), "ALSO ON WEDNESDAY 18 NOVEMBER \u2014 16 MORE STORIES",
           font=font(F_SANS_B, 15), fill=INK)
    briefs = [
        (10, "RUSSIA", "An-12 military plane crashes in Kemerovo; 19 dead."),
        (11, "ISRAEL", "Knesset elects Matan Kahana speaker; blow to Netanyahu."),
        (12, "DR CONGO", "Ebola more than doubles: 11,000+ cases, 5,400 dead."),
        (13, "SAUDI ARABIA", "Houthis fire 5 drones at pipeline pumping stations."),
        (14, "COOK ISLANDS", "Category 5 Cyclone Xavier hits the north."),
        (15, "PAPUA NEW GUINEA", "Magnitude 6.0 earthquake."),
        (16, "USA", "Measles elimination status lost: 5,400+ cases, 10 dead."),
        (17, "SUDAN", "9 RSF drone strikes near El Obeid kill 37 civilians."),
        (18, "MONGOLIA", "President resigns amid a corruption scandal."),
        (19, "FRANCE", "Depardieu drops appeal, admits sexual assault charge."),
        (20, "JAPAN", "Jets scrambled over two suspected Russian violations."),
        (21, "YEMEN", "Government forces retreat before Houthi push on Aden."),
        (22, "GAZA", "UK, Australia, Canada, Italy urge Israel to open crossings."),
        (23, "UKRAINE", "Zelenskyy at Ramstein seeks air defence, 40 F-16s. (17 Nov)"),
        (24, "KYIV", "Russia\u2019s overnight attack: 306 drones; two bridges hit. (17 Nov)"),
        (25, "WEST BANK", "72-year-old Palestinian woman shot dead by settlers."),
    ]
    bf_num = font(F_SANS_B, 12)
    bf_place = font(F_SERIF_B, 12)
    bf_txt = font(F_SERIF, 12)
    by = 846
    for j, (num, place, txt) in enumerate(briefs):
        bx = MX if j < 8 else MX + 492
        row = j % 8
        yy = by + row * 19
        d.text((bx, yy), "%d." % num, font=bf_num, fill=RED)
        d.text((bx + 26, yy), place + " \u2014 ", font=bf_place, fill=INK)
        pw = bf_place.getlength(place + " \u2014 ")
        d.text((bx + 26 + pw, yy), txt, font=bf_txt, fill=INK)

    # ---- foot ----------------------------------------------------------
    d.line([(MX, 994), (W - MX, 994)], fill=INK, width=1)
    d.text((W // 2, 1002),
           "Sources: Just Security \u00b7 Open Chronicle \u00b7 Horizon "
           "\u00b7 One Turn \u00b7 Daily Baku \u00b7 Reuters \u00b7 AP "
           "\u00b7 AFP \u00b7 BBC \u00b7 Al Jazeera",
           font=font(F_SERIF, 13), fill=GREY, anchor="ma")

    img.save(OUT, "PNG")
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
