#!/usr/bin/env python3
"""Draw the 19 November 2026 one-day news image (1024x1024).

Pillow + stdlib only, no network, fully deterministic: same input bytes
produce the same output bytes on every run (fixed layout, fixed fonts,
no timestamps, no randomness).
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 28

NAVY = (16, 30, 51)
NAVY2 = (30, 58, 95)
GOLD = (201, 162, 39)
RED = (178, 34, 34)
PAPER = (247, 243, 234)
CARD = (255, 255, 255)
INK = (24, 24, 24)
GREY = (92, 92, 92)
GREEN = (18, 128, 60)
SKY = (214, 228, 240)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    path = os.path.join(FONT_DIR, name)
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


F_TITLE = lambda: font("DejaVuSans-Bold.ttf", 40)
F_DATE = lambda: font("DejaVuSans-Bold.ttf", 22)
F_HERO = lambda: font("DejaVuSans-Bold.ttf", 42)
F_HERO_SUB = lambda: font("DejaVuSans.ttf", 22)
F_KICK = lambda: font("DejaVuSans-Bold.ttf", 16)
F_HEAD = lambda: font("DejaVuSans-Bold.ttf", 23)
F_BODY = lambda: font("DejaVuSans.ttf", 18)
F_STRIP_H = lambda: font("DejaVuSans-Bold.ttf", 26)
F_STRIP_B = lambda: font("DejaVuSans.ttf", 20)
F_TICK_LBL = lambda: font("DejaVuSans-Bold.ttf", 21)
F_TICK_NAME = lambda: font("DejaVuSans-Bold.ttf", 16)
F_TICK_VAL = lambda: font("DejaVuSans-Bold.ttf", 21)
F_TICK_PCT = lambda: font("DejaVuSans-Bold.ttf", 18)
F_TICK_NOTE = lambda: font("DejaVuSans.ttf", 13)
F_FOOT = lambda: font("DejaVuSans.ttf", 13)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for word in words[1:]:
            trial = cur + " " + word
            if draw.textlength(trial, font=fnt) <= max_w:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
    return lines


def star_points(cx, cy, r_out, r_in, points=5, rot=-90):
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        ang = math.radians(rot + i * 180.0 / points)
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return pts


def draw_us_flag(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(255, 255, 255))
    stripe_h = (y1 - y0) / 13.0
    for i in range(13):
        if i % 2 == 0:
            draw.rectangle([x0, y0 + i * stripe_h, x1, y0 + (i + 1) * stripe_h],
                           fill=(178, 34, 34))
    canton_w = (x1 - x0) * 0.4
    canton_h = stripe_h * 7
    draw.rectangle([x0, y0, x0 + canton_w, y0 + canton_h], fill=(30, 58, 95))
    for row in range(4):
        for col in range(5):
            cx = x0 + canton_w * (col + 0.5) / 5
            cy = y0 + canton_h * (row + 0.5) / 4
            draw.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=(255, 255, 255))


def draw_cn_flag(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(222, 41, 16))
    w, h = x1 - x0, y1 - y0
    draw.polygon(star_points(x0 + w * 0.22, y0 + h * 0.30, 16, 6.5),
                 fill=(255, 222, 0))
    for sx, sy in [(0.52, 0.16), (0.64, 0.30), (0.60, 0.52), (0.44, 0.60)]:
        draw.polygon(star_points(x0 + w * sx, y0 + h * sy, 7, 3),
                     fill=(255, 222, 0))


def draw_ru_flag(draw, x0, y0, x1, y1):
    h = (y1 - y0) / 3.0
    draw.rectangle([x0, y0, x1, y0 + h], fill=(255, 255, 255))
    draw.rectangle([x0, y0 + h, x1, y0 + 2 * h], fill=(0, 57, 166))
    draw.rectangle([x0, y0 + 2 * h, x1, y1], fill=(213, 0, 50))


def skyline(draw, x0, x1, base_y, top_y, color):
    """Deterministic city silhouette: fixed heights, no randomness."""
    heights = [26, 40, 18, 52, 34, 62, 24, 44, 30, 58, 20, 38, 48, 28,
               66, 36, 22, 46, 32, 56, 26, 42, 18, 50, 30, 60, 24, 40]
    bw = (x1 - x0) / len(heights)
    for i, hh in enumerate(heights):
        bx = x0 + i * bw
        draw.rectangle([bx + 1, base_y - hh, bx + bw - 1, base_y],
                       fill=color)
        if i % 5 == 2:  # antenna on every fifth tower
            draw.line([bx + bw / 2, base_y - hh, bx + bw / 2,
                       base_y - hh - 10], fill=color, width=2)


def card(draw, x0, y0, x1, y1, accent, kicker, headline, body):
    draw.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=CARD,
                           outline=(210, 205, 190), width=1)
    draw.rectangle([x0 + 10, y0, x1 - 10, y0 + 6], fill=accent)
    tx = x0 + 18
    ty = y0 + 18
    draw.text((tx, ty), kicker, font=F_KICK(), fill=accent)
    ty += 26
    for line in wrap(draw, headline, F_HEAD(), x1 - x0 - 36):
        draw.text((tx, ty), line, font=F_HEAD(), fill=INK)
        ty += 28
    ty += 4
    for line in wrap(draw, body, F_BODY(), x1 - x0 - 36):
        draw.text((tx, ty), line, font=F_BODY(), fill=(52, 52, 52))
        ty += 24


def build_image(path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------
    d.rectangle([0, 0, W, 100], fill=NAVY)
    d.text((MARGIN, 18), "THE WORLD IN ONE DAY", font=F_TITLE(),
           fill=(255, 255, 255))
    d.text((MARGIN, 64), "THURSDAY, 19 NOVEMBER 2026", font=F_DATE(),
           fill=GOLD)
    right_txt = "WORLD NEWS"
    rw = d.textlength(right_txt, font=F_DATE())
    d.text((W - MARGIN - rw, 64), right_txt,
           font=F_DATE(), fill=(180, 195, 215))
    d.rectangle([0, 100, W, 106], fill=RED)

    # ---- Hero: three flags + headline band ------------------------
    hero_y0, hero_y1 = 106, 396
    flag_y0, flag_y1 = hero_y0, 252
    third = W / 3.0
    draw_us_flag(d, 0, flag_y0, third, flag_y1)
    draw_cn_flag(d, third, flag_y0, 2 * third, flag_y1)
    draw_ru_flag(d, 2 * third, flag_y0, W, flag_y1)
    d.line([third, flag_y0, third, flag_y1], fill=(255, 255, 255), width=3)
    d.line([2 * third, flag_y0, 2 * third, flag_y1], fill=(255, 255, 255),
           width=3)
    d.rectangle([0, flag_y1, W, hero_y1], fill=NAVY)
    skyline(d, 0, W, hero_y1, hero_y1, NAVY2)
    d.text((MARGIN, 264), "TRUMP, XI & PUTIN MEET IN SHENZHEN",
           font=F_HERO(), fill=(255, 255, 255))
    d.text((MARGIN, 316),
           "First three-way summit of the three leaders, on the",
           font=F_HERO_SUB(), fill=(220, 228, 238))
    d.text((MARGIN, 344),
           "APEC sidelines — a first for the three powers.",
           font=F_HERO_SUB(), fill=(220, 228, 238))

    # ---- Grid: four stories ---------------------------------------
    gx0, gy0 = MARGIN, 410
    gap = 14
    cw = (W - 2 * MARGIN - gap) // 2
    ch = 184
    stories = [
        (RED, "THE HAGUE  •  10:00 AM",
         "ICJ rules on Rohingya genocide case",
         "The court delivers its verdict on Myanmar — "
         "Gambia v. Myanmar, filed 2019. 740,000+ Rohingya "
         "fled in the 2017 crackdown."),
        (NAVY2, "CRIMEA",
         "Crimean Bridge hit a third time this week",
         "Ukraine's strike closes the bridge again; Crimea's "
         "Russian-appointed head, Aksyonov, orders traffic "
         "halted on 19 Nov."),
        (RED, "WASHINGTON",
         "Jeffries picked as Speaker nominee",
         "House Democrats choose Hakeem Jeffries — in line "
         "to become the first Black Speaker when the new "
         "Congress convenes in January."),
        (NAVY2, "THE GULF",
         "Iran widens attacks after US strikes",
         "The US hit a missile site on Qeshm Island on 17 Nov; "
         "Iran struck a US radar site in Bahrain and a US base "
         "in Kuwait on 18 Nov."),
    ]
    for i, (accent, kicker, head, body) in enumerate(stories):
        cx = gx0 + (i % 2) * (cw + gap)
        cy = gy0 + (i // 2) * (ch + gap)
        card(d, cx, cy, cx + cw, cy + ch, accent, kicker, head, body)

    # ---- Strip: Voyager 1 ------------------------------------------
    sy0, sy1 = 806, 884
    d.rounded_rectangle([MARGIN, sy0, W - MARGIN, sy1], radius=10,
                        fill=NAVY)
    for sx, sy in [(900, 818), (950, 830), (985, 862), (860, 872)]:
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 255, 255))
    d.text((MARGIN + 18, sy0 + 12), "VOYAGER 1 NEARS ONE LIGHT-DAY",
           font=F_STRIP_H(), fill=GOLD)
    d.text((MARGIN + 18, sy0 + 48),
           "NASA's probe becomes the first human-made object to reach "
           "one light-day from Earth.",
           font=F_STRIP_B(), fill=(220, 228, 238))

    # ---- Ticker: US markets, closes 18 Nov -------------------------
    ty0, ty1 = 896, 996
    d.rounded_rectangle([MARGIN, ty0, W - MARGIN, ty1], radius=10,
                        fill=CARD, outline=(210, 205, 190), width=1)
    d.text((MARGIN + 18, ty0 + 10), "US MARKETS — CLOSES 18 NOV",
           font=F_TICK_LBL(), fill=NAVY)
    d.text((W - MARGIN - 18 - 210, ty0 + 12), "FINAL CLOSES, WED 18 NOV",
           font=F_TICK_NOTE(), fill=GREY)
    marks = [
        ("DOW", "50,198.17", "\u22121.11%", RED),
        ("S&P 500", "7,323.63", "\u22120.23%", RED),
        ("NASDAQ", "24,429.89", "+0.42%", GREEN),
        ("GOLD · DEC", "$3,741.90", "\u22123.16%", RED),
        ("BRENT · JAN", "$91.95", "\u22121.28%", RED),
    ]
    col_w = (W - 2 * MARGIN - 36) // 5
    for i, (name, val, pct, color) in enumerate(marks):
        cx = MARGIN + 18 + i * col_w
        d.text((cx, ty0 + 34), name, font=F_TICK_NAME(), fill=GREY)
        d.text((cx, ty0 + 54), val, font=F_TICK_VAL(), fill=INK)
        d.text((cx, ty0 + 76), pct, font=F_TICK_PCT(), fill=color)

    # ---- Footer ----------------------------------------------------
    d.text((MARGIN, 1004), "Sources: AP, BBC, Reuters — reported 19 Nov 2026",
           font=F_FOOT(), fill=GREY)

    img.save(path, format="PNG")
    return path


if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    build_image(target)
    print("wrote", target)
