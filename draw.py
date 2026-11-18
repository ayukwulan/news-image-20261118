#!/usr/bin/env python3
"""Draw the front page for news-image-20261118.

Renders entry.png (1024x1024): a classic broadsheet front page,
masthead + black date band, a lead story on the Gulf strikes with a
drawn map illustration and a fact column, then a 3x2 grid of shorter
stories. Everything is drawn with PIL shapes; no photographs.
Run: python3 draw.py  (writes entry.png next to this file)
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (253, 251, 243)      # warm off-white
INK = (17, 17, 17)           # near-black
RED = (176, 30, 30)          # accent red
GREY = (90, 90, 88)
SEA = (186, 211, 228)        # gulf water
LAND = (232, 220, 192)       # land tan
LAND_LINE = (150, 135, 100)

F_SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
F_SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
F_SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
F_SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
F_SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


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


def draw_text(d, xy, text, fnt, fill=INK, anchor="la"):
    d.text(xy, text, font=fnt, fill=fill, anchor=anchor)


def draw_para(d, x, y, lines, fnt, fill=INK, leading=None):
    """Draw wrapped lines; returns y just below the last line."""
    if leading is None:
        leading = int(fnt.size * 1.28)
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def letterspaced(d, x, y, text, fnt, fill=INK, tracking=3):
    """Draw text with extra space between characters; returns end x."""
    cx = x
    for ch in text:
        d.text((cx, y), ch, font=fnt, fill=fill)
        cx += int(fnt.getlength(ch)) + tracking
    return cx


def burst(d, cx, cy, r, fill=RED):
    """8-point starburst (explosion marker)."""
    import math
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


# ---------------------------------------------------------------- icons
def icon_bridge(d, x, y, s=40):
    """Broken bridge: two pillars, deck with a gap, one half tilted."""
    d.line([(x + 2, y + s - 8), (x + 2, y + 10)], fill=INK, width=3)
    d.line([(x + s - 2, y + s - 8), (x + s - 2, y + 10)], fill=INK, width=3)
    d.line([(x + 2, y + 12), (x + s // 2 - 4, y + 12)], fill=INK, width=4)
    d.line([(x + s // 2 + 4, y + 20), (x + s - 2, y + 14)], fill=INK, width=4)
    d.line([(x + 2, y + s - 6), (x + s - 2, y + s - 6)], fill=INK, width=2)
    burst(d, x + s // 2, y + 18, 6)


def icon_globe(d, x, y, s=40):
    d.ellipse([x + 2, y + 2, x + s - 2, y + s - 2], outline=INK, width=3)
    d.ellipse([x + s // 2 - 7, y + 2, x + s // 2 + 7, y + s - 2],
              outline=INK, width=2)
    d.line([(x + 2, y + s // 2), (x + s - 2, y + s // 2)], fill=INK, width=2)
    d.arc([x + 6, y + 8, x + s - 6, y + s - 8], 200, 340, fill=INK, width=2)


def icon_capitol(d, x, y, s=40):
    d.polygon([(x + s // 2, y + 2), (x + 6, y + 12), (x + s - 6, y + 12)],
              outline=INK, width=2)
    d.arc([x + s // 2 - 7, y + 2, x + s // 2 + 7, y + 14], 180, 360,
          fill=INK, width=2)
    for cx in (x + 8, x + s // 2, x + s - 8):
        d.line([(cx, y + 14), (cx, y + s - 8)], fill=INK, width=3)
    d.line([(x + 2, y + s - 6), (x + s - 2, y + s - 6)], fill=INK, width=3)


def icon_plane(d, x, y, s=40):
    d.polygon([(x + 4, y + s // 2 + 2), (x + s - 6, y + s // 2 - 6),
               (x + s - 2, y + s // 2 - 2), (x + 10, y + s // 2 + 6)],
              fill=INK)
    d.polygon([(x + s // 2 - 2, y + s // 2 - 2), (x + s // 2 + 6, y + 4),
               (x + s // 2 + 10, y + 6), (x + s // 2 + 2, y + s // 2 + 2)],
              fill=INK)
    d.polygon([(x + 8, y + s // 2 + 2), (x + 14, y + s - 6),
               (x + 18, y + s - 4), (x + 16, y + s // 2 + 4)], fill=INK)


def icon_knesset(d, x, y, s=40):
    d.rectangle([x + 4, y + 14, x + s - 4, y + s - 6], outline=INK, width=2)
    d.polygon([(x + 2, y + 14), (x + s // 2, y + 4), (x + s - 2, y + 14)],
              outline=INK, width=2)
    for cx in (x + 10, x + s // 2, x + s - 10):
        d.line([(cx, y + 18), (cx, y + s - 10)], fill=INK, width=3)
    d.line([(x + s - 8, y + 4), (x + s - 8, y + 14)], fill=INK, width=2)
    d.polygon([(x + s - 8, y + 4), (x + s - 2, y + 6), (x + s - 8, y + 8)],
              fill=RED)


def icon_news(d, x, y, s=40):
    d.rectangle([x + 4, y + 6, x + s - 6, y + s - 6], outline=INK, width=2)
    d.line([(x + 8, y + 12), (x + s - 10, y + 12)], fill=INK, width=3)
    for yy in (18, 24, 30):
        d.line([(x + 8, y + yy), (x + s - 10, y + yy)], fill=INK, width=2)


# ---------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 36                      # side margin
    RW = W - 2 * MX              # text width (952)

    # ---- masthead ------------------------------------------------------
    mast = font(F_SERIF_B, 66)
    d.text((W // 2, 14), "THE WORLD TODAY", font=mast, fill=INK,
           anchor="ma")
    d.line([(MX, 88), (W - MX, 88)], fill=INK, width=3)
    d.line([(MX, 93), (W - MX, 93)], fill=INK, width=1)

    # ---- black date band ----------------------------------------------
    d.rectangle([MX, 100, W - MX, 132], fill=INK)
    date_f = font(F_SANS_B, 25)
    d.text((W // 2, 116), "WEDNESDAY 18 NOVEMBER 2026", font=date_f,
           fill=(255, 255, 255), anchor="mm")

    # ---- lead ----------------------------------------------------------
    ly = 146
    kick = font(F_SANS_B, 20)
    letterspaced(d, MX, ly, "THE GULF CRISIS", kick, fill=RED, tracking=4)

    head_f = fit_font("IRAN HITS US BASES IN GULF", F_SERIF_B, 58, RW)
    d.text((MX, ly + 28), "IRAN HITS US BASES IN GULF", font=head_f, fill=INK)

    deck_f = font(F_SERIF_I, 23)
    deck = wrap("Tehran retaliates for the American strike on Qeshm "
                "Island \u2014 missiles and drones hit Kuwait and "
                "Bahrain, and a US MQ-9 is shot down over the strait.",
                deck_f, RW)
    dy = draw_para(d, MX, ly + 28 + head_f.size + 12, deck, deck_f,
                   leading=29)

    # ---- lead illustration (schematic Gulf map) + fact column ----------
    ill_x, ill_y = MX, 300
    ill_w, ill_h = 560, 252
    fac_x, fac_w = 624, 364
    d.rectangle([ill_x, ill_y, ill_x + ill_w, ill_y + ill_h],
                fill=SEA, outline=INK, width=2)
    # Iran landmass (top)
    d.polygon([(ill_x, ill_y), (ill_x + ill_w, ill_y),
               (ill_x + ill_w, ill_y + 62), (ill_x + 470, ill_y + 84),
               (ill_x + 330, ill_y + 66), (ill_x + 170, ill_y + 92),
               (ill_x, ill_y + 74)],
              fill=LAND, outline=LAND_LINE)
    # Arabian Peninsula (bottom left)
    d.polygon([(ill_x, ill_y + ill_h), (ill_x, ill_y + 168),
               (ill_x + 110, ill_y + 150), (ill_x + 190, ill_y + 176),
               (ill_x + 225, ill_y + ill_h)],
              fill=LAND, outline=LAND_LINE)
    # Qatar bump (small peninsula on the right of the gulf)
    d.polygon([(ill_x + 300, ill_y + 150), (ill_x + 330, ill_y + 138),
               (ill_x + 352, ill_y + 158), (ill_x + 330, ill_y + 172)],
              fill=LAND, outline=LAND_LINE)
    # Qeshm Island in the strait
    d.ellipse([ill_x + 428, ill_y + 88, ill_x + 486, ill_y + 104],
              fill=LAND, outline=LAND_LINE)
    # Bahrain island
    d.ellipse([ill_x + 288, ill_y + 128, ill_x + 306, ill_y + 142],
              fill=LAND, outline=LAND_LINE)
    # strike markers
    burst(d, ill_x + 457, ill_y + 96, 15)                    # Qeshm
    burst(d, ill_x + 118, ill_y + 158, 13)                   # Kuwait
    burst(d, ill_x + 297, ill_y + 135, 13)                   # Bahrain
    # drone silhouette over the gulf
    dx, dy2 = ill_x + 420, ill_y + 185
    d.ellipse([dx - 16, dy2 - 4, dx + 16, dy2 + 4], fill=INK)
    d.line([(dx - 22, dy2 - 8), (dx - 8, dy2 - 2)], fill=INK, width=2)
    d.line([(dx + 8, dy2 - 2), (dx + 22, dy2 - 8)], fill=INK, width=2)
    d.line([(dx, dy2 + 4), (dx, dy2 + 12)], fill=INK, width=2)
    # labels with leader lines
    lab_f = font(F_SANS_B, 14)
    label(d, ill_x + 470, ill_y + 66, "QESHM", lab_f)
    d.line([(ill_x + 470, ill_y + 82), (ill_x + 462, ill_y + 88)],
           fill=INK, width=1)
    label(d, ill_x + 12, ill_y + 128, "KUWAIT", lab_f)
    d.line([(ill_x + 66, ill_y + 146), (ill_x + 108, ill_y + 152)],
           fill=INK, width=1)
    label(d, ill_x + 312, ill_y + 122, "BAHRAIN", lab_f)
    d.line([(ill_x + 318, ill_y + 136), (ill_x + 304, ill_y + 136)],
           fill=INK, width=1)
    label(d, ill_x + 398, ill_y + 204, "US MQ-9 DOWN", lab_f)
    d.line([(ill_x + 420, ill_y + 200), (ill_x + 424, ill_y + 192)],
           fill=INK, width=1)
    cap_f = font(F_SERIF_I, 14)
    d.text((ill_x + ill_w // 2, ill_y + ill_h - 26),
           "The Strait of Hormuz \u2014 Qeshm, Kuwait and Bahrain",
           font=cap_f, fill=GREY, anchor="ma")

    # fact column
    fx = fac_x
    fy = ill_y
    fh = font(F_SANS_B, 19)
    letterspaced(d, fx, fy, "THE FACTS", fh, fill=INK, tracking=3)
    d.line([(fx, fy + 28), (fx + fac_w, fy + 28)], fill=INK, width=2)
    facts = [
        "US jets hit an Iranian Guard missile site on Qeshm Island, "
        "in the Strait of Hormuz.",
        "Iran struck Ali Al Salem Air Base in Kuwait, which hosts "
        "US forces.",
        "A US radar site and Patriot batteries in Bahrain were "
        "targeted.",
        "Iran shot down a US MQ-9 drone near the strait.",
    ]
    bf = font(F_SERIF, 19)
    by = fy + 42
    for fact in facts:
        d.rectangle([fx, by + 7, fx + 9, by + 16], fill=RED)
        lines = wrap(fact, bf, fac_w - 20)
        by = draw_para(d, fx + 20, by, lines, bf, leading=24)
        by += 10

    # ---- divider -------------------------------------------------------
    d.line([(MX, 568), (W - MX, 568)], fill=INK, width=2)

    # ---- 3x2 grid ------------------------------------------------------
    grid_y = 584
    row_h = 176
    col_w = 304
    col_xs = [MX, MX + col_w + 20, MX + 2 * (col_w + 20)]

    stories = [
        ("KERCH BRIDGE HIT AGAIN", icon_bridge,
         "Ukraine strikes the Crimean bridge a second day; part of "
         "the road span falls into the strait."),
        ("APEC SHENZHEN", icon_globe,
         "Xi and Putin meet ahead of Thursday\u2019s trilateral with "
         "Trump; Xi vows to resist trade protectionism."),
        ("US SENATE", icon_capitol,
         "Peltola beats Sullivan in Alaska, giving Democrats a "
         "projected 56\u201344 Senate majority."),
        ("SIBERIA CRASH", icon_plane,
         "A Russian An-12 military plane crashes in Kemerovo, "
         "killing all 19 people on board."),
        ("ISRAEL", icon_knesset,
         "Knesset elects Matan Kahana speaker, a win for PM-elect "
         "Eisenkot and a blow to Netanyahu."),
    ]
    hf = font(F_SERIF_B, 24)
    sf = font(F_SERIF, 17)
    for i, (head, icon, summ) in enumerate(stories):
        cx = col_xs[i % 3]
        cy = grid_y + (i // 3) * (row_h + 14)
        icon(d, cx, cy, 40)
        hlines = wrap(head, hf, col_w - 50)
        hy = cy - 2
        for ln in hlines:
            d.text((cx + 50, hy), ln, font=hf, fill=INK)
            hy += 28
        slines = wrap(summ, sf, col_w)
        draw_para(d, cx, cy + 56, slines, sf, leading=21)

    # ALSO IN THE NEWS cell (bottom right)
    cx = col_xs[2]
    cy = grid_y + row_h + 14
    icon_news(d, cx, cy, 40)
    d.text((cx + 50, cy - 2), "ALSO IN THE NEWS", font=hf, fill=INK)
    items = [
        "Ebola in DR Congo: 11,000+ cases, 5,400 dead",
        "Houthis fire 5 drones at Saudi pipeline stations",
        "Cyclone Xavier, Cat 5, hits the Cook Islands",
        "6.0 quake strikes Papua New Guinea",
    ]
    it_f = font(F_SERIF, 15)
    iy = cy + 56
    for it in items:
        d.text((cx, iy), "\u2022", font=it_f, fill=RED)
        d.text((cx + 14, iy), it, font=it_f, fill=INK)
        iy += 19

    # ---- foot ----------------------------------------------------------
    d.line([(MX, 952), (W - MX, 952)], fill=INK, width=1)
    src_f = font(F_SERIF_I, 16)
    d.text((W // 2, 962),
           "Sources: Just Security \u00b7 Open Chronicle \u00b7 Horizon "
           "\u00b7 One Turn \u00b7 Daily Baku",
           font=src_f, fill=GREY, anchor="ma")

    img.save(OUT, "PNG")
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
