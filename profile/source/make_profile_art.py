"""Draws the images of the digiface-ir GitHub profile page (profile/README.md).

GitHub strips fonts and styles from a README, so the Persian text is drawn here
with Estedad (headings) and Vazirmatn (body), both SIL Open Font License.
Every image is a rounded card with its own light background, so it reads the
same in GitHub's light and dark themes. Run: python3 make_profile_art.py <out dir>
"""
import math
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT = sys.argv[1]
ROSE = (172, 23, 84)
ROSE_SOFT = (232, 160, 184)
BLUSH = (249, 225, 233)
CREAM = (255, 248, 245)
INK = (43, 29, 34)
MUTED = (122, 102, 112)
WHITE = (255, 255, 255)


def font(name, size, weight):
    f = ImageFont.truetype(f"{name}-wght-normal.woff2", size)
    f.set_variation_by_axes([weight])
    return f


def fa(size, weight, family="estedad"):
    return font(f"{family}-arabic", size, weight)


def en(size, weight, family="vazirmatn"):
    return font(f"{family}-latin", size, weight)


def rounded_card(w, h, radius, top, bottom):
    """A vertical gradient from `top` to `bottom`, clipped to a rounded rectangle."""
    grad = Image.new("RGBA", (w, h))
    px = grad.load()
    for y in range(h):
        t = y / (h - 1)
        c = tuple(round(top[i] + (bottom[i] - top[i]) * t) for i in range(3)) + (255,)
        for x in range(w):
            px[x, y] = c
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, w - 1, h - 1), radius, fill=255)
    card = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    card.paste(grad, (0, 0), mask)
    return card


def sparkle(draw, cx, cy, r, color):
    """The four-point star of the logo."""
    pts = []
    for i in range(8):
        ang = math.pi / 2 + i * math.pi / 4
        rr = r if i % 2 == 0 else r * 0.22
        pts.append((cx + rr * math.cos(ang), cy - rr * math.sin(ang)))
    draw.polygon(pts, fill=color)


def rtl(draw, x_right, y, text, f, fill):
    """Persian text, its right edge at x_right, top at y."""
    draw.text((x_right, y), text, font=f, fill=fill, anchor="ra", direction="rtl")


def wrap_rtl(text, f, width):
    lines, line = [], ""
    for word in text.split(" "):
        trial = f"{line} {word}".strip()
        if f.getlength(trial, direction="rtl") <= width:
            line = trial
        else:
            lines.append(line)
            line = word
    lines.append(line)
    return lines


def soft_shadow(base, box, radius, color, blur, offset):
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    x0, y0, x1, y1 = box
    ImageDraw.Draw(layer).rounded_rectangle((x0, y0 + offset, x1, y1 + offset), radius, fill=color)
    base.alpha_composite(layer.filter(ImageFilter.GaussianBlur(blur)))


# 1. Hero banner ---------------------------------------------------------------
W, H = 1800, 660
hero = rounded_card(W, H, 56, CREAM, BLUSH)
d = ImageDraw.Draw(hero)
for cx, cy, r, a in [(160, 120, 300, 70), (1650, 600, 260, 60), (980, -40, 180, 45)]:
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse((cx - r, cy - r, cx + r, cy + r), fill=ROSE_SOFT + (a,))
    hero.alpha_composite(glow.filter(ImageFilter.GaussianBlur(60)))
d = ImageDraw.Draw(hero)
for cx, cy, r, c in [(640, 120, 26, ROSE_SOFT), (720, 520, 18, ROSE_SOFT), (1120, 560, 22, WHITE), (90, 560, 16, ROSE_SOFT)]:
    sparkle(d, cx, cy, r, c)

logo = Image.open("digiface-card.png").convert("RGBA")
logo = logo.resize((520, 520), Image.LANCZOS)
hero.alpha_composite(logo, (70, (H - 520) // 2))

right = W - 110
rtl(d, right, 70, "دیجی‌فیس", fa(176, 900), ROSE)
rtl(d, right, 300, "لوازم آرایشی و بهداشتی،", fa(64, 700), INK)
rtl(d, right, 380, "از فروشگاه‌های شهرت تا درِ خانه‌ات", fa(64, 700), INK)
eng = "Beauty & personal care, from the shops in your city to your door"
ef = en(31, 500)
d.text((right, 482), eng, font=ef, fill=MUTED, anchor="ra")
pill_f = en(34, 700)
label = "digi-face.ir"
pw = int(pill_f.getlength(label)) + 76
px0 = right - pw
d.rounded_rectangle((px0, 548, right, 612), 32, fill=ROSE)
d.text((px0 + pw / 2, 580), label, font=pill_f, fill=WHITE, anchor="mm")
hero.save(f"{OUT}/hero.png", optimize=True)

# 2. What DigiFace is, and four cards ------------------------------------------
W = 1800
cards = [
    ("۰۱", "برای مشتری", "کالا را از فروشگاه‌های شهرِ خودت پیدا کن، آنلاین بخر و سفارشت را قدم‌به‌قدم دنبال کن"),
    ("۰۲", "برای فروشگاه", "کالا و قیمت، موجودی، سفارش‌ها و کیف‌پول؛ همه در پنلِ فروشگاه"),
    ("۰۳", "برای پیک", "سفارشِ آماده را از فروشگاه تحویل بگیر و به مشتری برسان؛ هر قدم در اپِ پیک ثبت می‌شود"),
    ("۰۴", "جشنواره‌ها و باکس‌ها", "جشنواره‌های تخفیفِ فروشگاه‌ها و باکس‌های دیجی‌فیس"),
]
intro = (
    "دیجی‌فیس بازار آنلاینِ لوازم آرایشی و بهداشتی است؛ فروشگاه‌ها کالاهایشان را عرضه می‌کنند، "
    "مشتری از فروشگاه‌های شهرِ خودش می‌خرد و پیکِ دیجی‌فیس سفارش را به دستش می‌رساند"
)
pad = 110
body_f = fa(42, 500, "vazirmatn")
intro_lines = wrap_rtl(intro, body_f, W - 2 * pad)
card_w = (W - 2 * pad - 50) // 2
card_text_f = fa(36, 450, "vazirmatn")
card_lines = [wrap_rtl(text, card_text_f, card_w - 120) for _, _, text in cards]
card_h = 150 + 70 + max(len(l) for l in card_lines) * 58 + 70
H = 305 + len(intro_lines) * 74 + 80 + 2 * card_h + 50 + 110
about = rounded_card(W, H, 56, WHITE, CREAM)
d = ImageDraw.Draw(about)
right = W - pad
rtl(d, right, 110, "دیجی‌فیس چیست؟", fa(78, 900), ROSE)
d.rounded_rectangle((right - 150, 252, right, 262), 5, fill=ROSE_SOFT)
y = 305
for line in intro_lines:
    rtl(d, right, y, line, body_f, INK)
    y += 74
y += 80
for i, (num, title, _) in enumerate(cards):
    row, col = divmod(i, 2)
    x1 = W - pad - col * (card_w + 50)
    x0 = x1 - card_w
    y0 = y + row * (card_h + 50)
    soft_shadow(about, (x0, y0, x1, y0 + card_h), 40, ROSE_SOFT + (90,), 22, 12)
    d = ImageDraw.Draw(about)
    d.rounded_rectangle((x0, y0, x1, y0 + card_h), 40, fill=WHITE, outline=BLUSH, width=3)
    d.rounded_rectangle((x1 - 14, y0 + 60, x1 - 4, y0 + card_h - 60), 5, fill=ROSE)
    rtl(d, x1 - 60, y0 + 50, num, fa(70, 900), ROSE_SOFT)
    rtl(d, x1 - 60, y0 + 150, title, fa(52, 800), INK)
    ty = y0 + 150 + 85
    for line in card_lines[i]:
        rtl(d, x1 - 60, ty, line, card_text_f, MUTED)
        ty += 58
about.save(f"{OUT}/about.png", optimize=True)

# 3. One order, from start to finish --------------------------------------------
W, H = 1800, 680
flow = rounded_card(W, H, 56, BLUSH, CREAM)
d = ImageDraw.Draw(flow)
right = W - 110
rtl(d, right, 90, "یک سفارش، از اول تا آخر", fa(70, 900), ROSE)
d.rounded_rectangle((right - 150, 222, right, 232), 5, fill=ROSE_SOFT)
steps = [
    ("۱", "عرضه", "فروشگاه کالا را", "عرضه می‌کند"),
    ("۲", "خرید", "مشتری سفارش می‌دهد", "و پرداخت می‌کند"),
    ("۳", "آماده‌سازی", "فروشگاه سفارش را", "آماده می‌کند"),
    ("۴", "تحویل", "پیک سفارش را", "به مشتری می‌رساند"),
]
cy = 360
slot = (W - 220) / 4
centers = [W - 110 - slot * (i + 0.5) for i in range(4)]
for a, b in zip(centers, centers[1:]):
    for x in range(int(b + 80), int(a - 80), 28):
        d.rounded_rectangle((x, cy - 4, x + 14, cy + 4), 4, fill=ROSE_SOFT)
for (num, title, l1, l2), cx in zip(steps, centers):
    soft_shadow(flow, (cx - 72, cy - 72, cx + 72, cy + 72), 72, ROSE + (60,), 16, 10)
    d = ImageDraw.Draw(flow)
    d.ellipse((cx - 72, cy - 72, cx + 72, cy + 72), fill=ROSE)
    d.text((cx, cy + 6), num, font=fa(84, 800), fill=WHITE, anchor="mm", direction="rtl")
    d.text((cx, cy + 130), title, font=fa(50, 800), fill=INK, anchor="mm", direction="rtl")
    d.text((cx, cy + 200), l1, font=fa(34, 450, "vazirmatn"), fill=MUTED, anchor="mm", direction="rtl")
    d.text((cx, cy + 248), l2, font=fa(34, 450, "vazirmatn"), fill=MUTED, anchor="mm", direction="rtl")
flow.save(f"{OUT}/flow.png", optimize=True)
print("ok")
