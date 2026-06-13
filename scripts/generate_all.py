"""
yidaotech.xyz 推广图片生成器 v2 — 竞品风格：工业产品目录风
学习 Crafco / SealMaster / RaynGuard / Asphalt Kingdom
特点：浅色背景 + 产品卡片 + 品牌色点缀 + 专业排版
"""

from pathlib import Path
import math

from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
OUT = Path("/tmp/output_v2")
PUBLIC_IMAGES = OUT / "public" / "images"
PRODUCT_IMAGES = PUBLIC_IMAGES / "products"

# ---- Brand Colors ----
BLUE_DARK = (13, 30, 86)       # #0D1E56
BLUE = (30, 64, 175)            # #1E40AF
BLUE_LIGHT = (147, 197, 253)    # #93C5FD
ORANGE = (245, 158, 11)         # #F59E0B
WHITE = (255, 255, 255)
OFF_WHITE = (248, 250, 252)
LIGHT_GRAY = (226, 232, 240)
MED_GRAY = (148, 163, 184)
DARK_GRAY = (51, 65, 85)
BLACK = (15, 23, 42)

COMPANY = "Shining Road Technology"
COMPANY_CN = "依道科技"
SITE = "yidaotech.xyz"
TAGLINE = "Professional Pavement Maintenance Solutions"

PRODUCTS = [
    ("cold-mix-pothole-repair", "Cold Mix Asphalt\nPothole Repair", "Permanent-grade cold mix · No heating · Wet-application"),
    ("hot-applied-crack-sealer", "Hot-Applied\nCrack Sealer", "ASTM D6690 Type II · Fuel-resistant · Highway-grade"),
    ("emulsified-asphalt", "Emulsified Asphalt", "CSS-1 / SS-1 / CRS-2 · Tack coat · Chip seal · Slurry"),
    ("pavement-sealcoat", "Pavement Sealcoat", "Coal tar & asphalt-based · Sand-filled · 5+ year protection"),
    ("crack-sealing-tape", "Crack Sealing Tape", "Self-adhesive bituminous · Peel & stick · Instant bond"),
    ("cold-pour-crack-filler", "Cold Pour\nCrack Filler", "Ready-to-use · Self-leveling · No equipment needed"),
    ("cold-mix-production-plant", "Cold Mix\nProduction Plant", "5-30 TPH · Turnkey · PLC automated · QC lab included"),
    ("technology-licensing", "Technology\nLicensing", "Formula transfer · Raw material sourcing · 90-day launch"),
]


# ---- Font Helpers ----
def font(size, bold=False):
    candidates = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for c in candidates:
        fp = Path(c)
        if fp.exists():
            try:
                return ImageFont.truetype(str(fp), size=size)
            except OSError:
                pass
    return ImageFont.load_default()


def text_size(draw, text, font_obj):
    bbox = draw.textbbox((0, 0), text, font=font_obj)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def fit_font(draw, text, max_w, start, min_s=18, bold=False):
    size = start
    while size >= min_s:
        f = font(size, bold=bold)
        if text_size(draw, text, f)[0] <= max_w:
            return f
        size -= 2
    return font(min_s, bold=bold)


def draw_centered(draw, text, cx, y, font_obj, fill):
    """Draw text horizontally centered at cx."""
    tw, _ = text_size(draw, text, font_obj)
    draw.text((cx - tw // 2, y), text, font=font_obj, fill=fill)


# ---- Background Generators ----

def gradient_bg(width, height, top_color, bottom_color):
    """Vertical gradient."""
    img = Image.new("RGB", (width, height), top_color)
    px = img.load()
    tr, tg, tb = top_color
    br, bg, bb = bottom_color
    for y in range(height):
        t = y / max(1, height - 1)
        r = int(tr + (br - tr) * t)
        g = int(tg + (bg - tg) * t)
        b = int(tb + (bb - tb) * t)
        for x in range(width):
            px[x, y] = (r, g, b)
    return img


def studio_bg(width, height):
    """Light gray-white studio background like product photos."""
    # Very light gray-to-white gradient
    img = gradient_bg(width, height, (245, 247, 250), (252, 253, 255))
    # Add a subtle warm spot (like one soft studio light)
    px = img.load()
    cx, cy = width * 0.45, height * 0.35
    for y in range(height):
        for x in range(width):
            dist = math.hypot((x - cx) / width, (y - cy) / height)
            glow = max(0, 1 - dist * 2.5) * 18
            r, g_val, b = px[x, y]
            px[x, y] = (
                min(255, int(r + glow)),
                min(255, int(g_val + glow)),
                min(255, int(b + glow)),
            )
    return img


def job_site_bg(width, height):
    """Darker industrial texture reminiscent of job sites."""
    img = gradient_bg(width, height, (30, 35, 45), (15, 18, 28))
    px = img.load()
    # Add subtle noise/texture
    import random
    rng = random.Random(42)
    for y in range(height):
        for x in range(width):
            noise = rng.randint(-6, 6)
            r, g, b = px[x, y]
            px[x, y] = (
                max(0, min(255, r + noise)),
                max(0, min(255, g + noise)),
                max(0, min(255, b + noise)),
            )
    return img


# ---- Card / Elements ----

def draw_card(draw, x, y, w, h, fill=WHITE, radius=16, shadow=True):
    """Draw a card with optional shadow."""
    if shadow:
        # Shadow
        shadow_layer = Image.new("RGBA", (w + 20, h + 20), (0, 0, 0, 0))
        sd = ImageDraw.Draw(shadow_layer, "RGBA")
        sd.rounded_rectangle((4, 8, w + 16, h + 12), radius=radius, fill=(0, 0, 0, 30))
        shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(radius=8))
        draw._image.paste(shadow_layer, (x - 10, y - 10), shadow_layer)
    draw.rounded_rectangle((x, y, x + w, y + h), radius=radius, fill=fill)
    # Subtle border
    draw.rounded_rectangle((x, y, x + w, y + h), radius=radius, outline=(200, 210, 220), width=1)


def product_badge(draw, x, y, category, fill_color=BLUE):
    """Small category badge pill."""
    tw = text_size(draw, category, font(14, bold=True))[0] + 28
    draw.rounded_rectangle((x, y, x + tw, y + 26), radius=13, fill=fill_color)
    draw_centered(draw, category, x + tw // 2, y + 4, font(14, bold=True), WHITE)


def accent_bar(draw, x, y, w, color=ORANGE, height=4):
    """Horizontal accent bar."""
    draw.rounded_rectangle((x, y, x + w, y + height), radius=2, fill=color)


# ---- Layouts ----

def build_header(draw, width, bg_is_dark=True):
    """Draw logo + site in top-left corner."""
    if bg_is_dark:
        logo_fill = WHITE
        sub_fill = BLUE_LIGHT
    else:
        logo_fill = BLUE_DARK
        sub_fill = MED_GRAY

    margin = 44
    # Logo diamond
    draw.polygon(
        [(margin + 15, margin + 36), (margin + 28, margin + 14), (margin + 41, margin + 36)],
        fill=BLUE,
    )
    draw.line((margin + 20, margin + 35, margin + 36, margin + 35), fill=ORANGE, width=3)
    draw.text((margin + 54, margin + 4), COMPANY, font=font(20, bold=True), fill=logo_fill)
    draw.text((margin + 54, margin + 30), SITE, font=font(14), fill=sub_fill)


# =========== OG Image Generator (1200 x 630) ===========

def generate_default_og():
    """Home page default OG image."""
    W, H = 1200, 630
    img = studio_bg(W, H).convert("RGBA")
    draw = ImageDraw.Draw(img, "RGBA")
    build_header(draw, W, bg_is_dark=False)

    # Center content card
    card_x, card_y = 120, 90
    card_w, card_h = 960, 450
    draw_card(draw, card_x, card_y, card_w, card_h, fill=WHITE)

    # Product badge
    product_badge(draw, card_x + 80, card_y + 60, "PAVEMENT SOLUTIONS")

    # Main title
    title = "Asphalt Crack Sealing &\nCold Mix Asphalt Products"
    title_font = font(52, bold=True)
    lines = title.split("\n")
    ty = card_y + 130
    for line in lines:
        draw.text((card_x + 80, ty), line, font=title_font, fill=BLACK)
        ty += text_size(draw, line, title_font)[1] + 12

    # Tagline
    sub_font = font(28)
    draw.text((card_x + 80, ty + 14), TAGLINE, font=sub_font, fill=MED_GRAY)

    # Accent bar
    accent_bar(draw, card_x + 80, ty + 86, 220, ORANGE, 5)

    # Features row
    features = [
        ("✓", "30+ Countries"),
        ("✓", "ASTM Certified"),
        ("✓", "Engineer Support"),
    ]
    fx = card_x + 80
    fy = ty + 130
    for icon, text in features:
        draw.text((fx, fy), icon, font=font(22), fill=BLUE)
        draw.text((fx + 32, fy), text, font=font(22), fill=DARK_GRAY)
        fx += 260

    # Bottom CTA
    cta = "Explore Products →"
    cta_font = font(22, bold=True)
    cta_w = text_size(draw, cta, cta_font)[0]
    draw.text((card_x + 80, card_y + card_h - 70), cta, font=cta_font, fill=BLUE)

    save_jpg(img, PUBLIC_IMAGES / "og-default.jpg")


def generate_product_og(slug, title_lines, subtitle):
    """Product-specific OG image."""
    W, H = 1200, 630
    img = studio_bg(W, H).convert("RGBA")
    draw = ImageDraw.Draw(img, "RGBA")
    build_header(draw, W, bg_is_dark=False)

    # Content card
    card_x, card_y = 100, 80
    card_w, card_h = 1000, 470
    draw_card(draw, card_x, card_y, card_w, card_h, fill=WHITE)

    # Product badge with category color
    category_map = {
        "Pothole": BLUE,
        "Crack": BLUE_DARK,
        "Emulsion": (30, 64, 175),
        "Surface": (13, 30, 86),
        "Plant": (15, 23, 42),
        "Technology": ORANGE,
    }
    cat = subtitle.split(" · ")[0] if " · " in subtitle else "PRODUCT"
    badge_color = BLUE
    for k, v in category_map.items():
        if k in slug or k in subtitle:
            badge_color = v
            break
    product_badge(draw, card_x + 70, card_y + 50, cat.upper(), fill_color=badge_color)

    # Title
    lines = title_lines.split("\n")
    title_font = fit_font(draw, max(lines, key=lambda l: text_size(draw, l, font(56))[0]),
                          card_w - 140, 56, 30, bold=True)
    ty = card_y + 120
    for line in lines:
        tw = text_size(draw, line, title_font)[0]
        draw.text((card_x + (card_w - tw) // 2, ty), line, font=title_font, fill=BLACK)
        ty += text_size(draw, line, title_font)[1] + 8

    # Subtitle
    sub_font = font(26)
    draw.text((card_x + 70, ty + 20), subtitle, font=sub_font, fill=MED_GRAY)

    # Accent bar
    accent_bar(draw, card_x + 70, ty + 66, 280, ORANGE, 5)

    # Bullet features
    bullet_font = font(22)
    bullets = subtitle.split(" · ")
    by = ty + 106
    for bullet in bullets[:4]:
        draw.text((card_x + 70, by), "●", font=font(18), fill=BLUE)  
        draw.text((card_x + 104, by), bullet, font=bullet_font, fill=DARK_GRAY)
        by += 34

    # Bottom
    accent_bar(draw, card_x, card_y + card_h - 4, card_w, BLUE, 4)
    cta = "yidaotech.xyz"
    cta_font = font(18, bold=True)
    draw.text((card_x + 70, card_y + card_h - 56), cta, font=cta_font, fill=MED_GRAY)

    save_jpg(img, PUBLIC_IMAGES / f"{slug}-og.jpg")


# =========== Hero Image Generator (800 x 400) ===========

def generate_product_hero(slug, title_lines, subtitle):
    """Product page Hero image."""
    W, H = 800, 400
    # Industrial dark background
    img = job_site_bg(W, H).convert("RGBA")
    draw = ImageDraw.Draw(img, "RGBA")
    build_header(draw, W, bg_is_dark=True)

    # Content overlay card
    card_x, card_y = 40, 60
    card_w, card_h = 720, 280
    # Semi-transparent dark card
    overlay = Image.new("RGBA", (card_w, card_h), (10, 15, 25, 210))
    img.paste(overlay, (card_x, card_y), overlay)
    draw.rounded_rectangle((card_x, card_y, card_x + card_w, card_y + card_h),
                           radius=12, outline=(255, 255, 255, 40), width=1)
    draw = ImageDraw.Draw(img, "RGBA")

    # Badge
    category_map = {"Pothole": BLUE, "Crack": BLUE_DARK, "Plant": BLUE_LIGHT,
                    "Technology": ORANGE}
    cat = subtitle.split(" · ")[0] if " · " in subtitle else "PRODUCT"
    badge_c = BLUE
    for k, v in category_map.items():
        if k in slug or k in subtitle:
            badge_c = v
            break
    product_badge(draw, card_x + 40, card_y + 30, cat.upper(), fill_color=badge_c)

    # Title
    lines = title_lines.split("\n")
    title_font = fit_font(draw, max(lines, key=lambda l: text_size(draw, l, font(48))[0]),
                          card_w - 80, 48, 26, bold=True)
    ty = card_y + 80
    for line in lines:
        tw = text_size(draw, line, title_font)[0]
        draw.text((card_x + 40 + (card_w - 80 - tw) // 2, ty), line, font=title_font, fill=WHITE)
        ty += text_size(draw, line, title_font)[1] + 6

    # Subtitle
    sub_font = font(20)
    draw.text((card_x + 40, ty + 14), subtitle, font=sub_font, fill=(180, 200, 220))

    # Accent bar
    accent_bar(draw, card_x + 40, ty + 50, 200, ORANGE, 4)

    # Bottom info
    draw.text((card_x + 40, card_y + card_h - 44), SITE, font=font(16, bold=True), fill=MED_GRAY)

    save_jpg(img, PRODUCT_IMAGES / f"{slug}-hero.jpg")


def generate_news_default():
    """News section OG default."""
    W, H = 1200, 630
    img = studio_bg(W, H).convert("RGBA")
    draw = ImageDraw.Draw(img, "RGBA")
    build_header(draw, W, bg_is_dark=False)

    card_x, card_y = 100, 80
    card_w, card_h = 1000, 470
    draw_card(draw, card_x, card_y, card_w, card_h, fill=WHITE)

    product_badge(draw, card_x + 70, card_y + 50, "NEWS & INSIGHTS")

    title_font = font(64, bold=True)
    draw.text((card_x + 70, card_y + 130), "News & Insights", font=title_font, fill=BLACK)

    sub_font = font(28)
    draw.text((card_x + 70, card_y + 240),
              "Industry updates · Product news · Project stories",
              font=sub_font, fill=MED_GRAY)

    accent_bar(draw, card_x + 70, card_y + 300, 280, ORANGE, 5)
    accent_bar(draw, card_x, card_y + card_h - 4, card_w, BLUE, 4)

    save_jpg(img, PUBLIC_IMAGES / "news-og-default.jpg")


# ---- Utils ----

def save_jpg(img, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(path, "JPEG", quality=94, optimize=True, progressive=True)
    print(f"  → {path} ({path.stat().st_size:,} bytes)")


def main():
    PUBLIC_IMAGES.mkdir(parents=True, exist_ok=True)
    PRODUCT_IMAGES.mkdir(parents=True, exist_ok=True)

    print("Generating OG images (1200×630):")
    generate_default_og()
    generate_news_default()

    for slug, title, subtitle in PRODUCTS:
        print(f"  {slug}...")
        generate_product_og(slug, title, subtitle)

    print("\nGenerating Hero images (800×400):")
    for slug, title, subtitle in PRODUCTS:
        print(f"  {slug}...")
        generate_product_hero(slug, title, subtitle)

    generated = sorted(p for p in OUT.rglob("*.jpg") if p.is_file())
    print(f"\nDone! {len(generated)} images generated.")


if __name__ == "__main__":
    main()
