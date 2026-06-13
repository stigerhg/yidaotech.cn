from pathlib import Path
import math
import re
import textwrap

from PIL import Image, ImageDraw, ImageFont, ImageFilter


ROOT = Path(__file__).resolve().parent
OUT = Path("/tmp/output")
PUBLIC_IMAGES = OUT / "public" / "images"
PRODUCT_IMAGES = PUBLIC_IMAGES / "products"
NEWS_IMAGES = PUBLIC_IMAGES / "news"

BRAND_BLUE = (30, 64, 175)
BRAND_BLUE_DARK = (13, 30, 86)
BRAND_BLUE_DEEP = (8, 19, 57)
LIGHT_BLUE = (147, 197, 253)
ORANGE = (245, 158, 11)
WHITE = (255, 255, 255)
MUTED = (202, 222, 255)

COMPANY = "Shining Road Technology"
COMPANY_CN = "依道科技"
SITE = "yidaotech.xyz"
TAGLINE = "Professional Pavement Maintenance Solutions"
PRODUCT_SUBTITLE = "Professional Pavement Maintenance"

PRODUCTS = [
    ("cold-mix-pothole-repair", "冷拌沥青坑槽修补料"),
    ("hot-applied-crack-sealer", "热灌缝胶"),
    ("emulsified-asphalt", "乳化沥青"),
    ("pavement-sealcoat", "路面封层"),
    ("crack-sealing-tape", "贴缝带"),
    ("cold-pour-crack-filler", "冷灌缝胶"),
    ("cold-mix-production-plant", "冷拌生产设备"),
    ("technology-licensing", "技术授权"),
]


def ensure_dirs():
    for path in (PUBLIC_IMAGES, PRODUCT_IMAGES, NEWS_IMAGES):
        path.mkdir(parents=True, exist_ok=True)


def font(size, bold=False):
    candidates = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "/Library/Fonts/Arial Unicode.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            try:
                return ImageFont.truetype(candidate, size=size)
            except OSError:
                pass
    return ImageFont.load_default()


def parse_frontmatter(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    data = {}
    for line in parts[1].splitlines():
        if ":" not in line or line.startswith(" "):
            continue
        key, value = line.split(":", 1)
        value = value.strip().strip("\"'")
        data[key.strip()] = value
    return data


def gradient_background(width, height):
    img = Image.new("RGB", (width, height), BRAND_BLUE_DARK)
    px = img.load()
    for y in range(height):
        for x in range(width):
            tx = x / max(1, width - 1)
            ty = y / max(1, height - 1)
            glow = max(0.0, 1.0 - math.hypot(tx - 0.22, ty - 0.25) * 1.55)
            edge = (tx * 0.35 + ty * 0.65)
            r = int(BRAND_BLUE_DEEP[0] * edge + BRAND_BLUE[0] * (1 - edge) + 24 * glow)
            g = int(BRAND_BLUE_DEEP[1] * edge + BRAND_BLUE[1] * (1 - edge) + 44 * glow)
            b = int(BRAND_BLUE_DEEP[2] * edge + BRAND_BLUE[2] * (1 - edge) + 72 * glow)
            px[x, y] = (min(255, r), min(255, g), min(255, b))
    return img


def add_decor(img, seed=0):
    w, h = img.size
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer, "RGBA")

    draw.polygon(
        [(w * 0.62, 0), (w, 0), (w, h * 0.72), (w * 0.78, h * 0.56)],
        fill=(147, 197, 253, 26),
    )
    draw.polygon(
        [(0, h * 0.74), (w * 0.34, h), (0, h)],
        fill=(245, 158, 11, 34),
    )
    draw.rounded_rectangle(
        (w * 0.70, h * 0.17, w * 1.08, h * 0.29),
        radius=18,
        fill=(255, 255, 255, 20),
        outline=(147, 197, 253, 45),
        width=2,
    )
    draw.rounded_rectangle(
        (-w * 0.05, h * 0.12, w * 0.32, h * 0.20),
        radius=14,
        fill=(255, 255, 255, 13),
        outline=(255, 255, 255, 25),
        width=2,
    )

    for i in range(9):
        offset = (seed * 31 + i * 79) % int(w)
        y = h * (0.18 + (i % 5) * 0.14)
        draw.line(
            [(offset - w * 0.16, y), (offset + w * 0.12, y + h * 0.10)],
            fill=(147, 197, 253, 30),
            width=2,
        )

    lane_y = int(h * 0.77)
    draw.line([(0, lane_y), (w, int(h * 0.60))], fill=(255, 255, 255, 42), width=max(3, w // 220))
    draw.line([(0, lane_y + 34), (w, int(h * 0.60) + 34)], fill=(147, 197, 253, 34), width=max(2, w // 320))
    for i in range(7):
        x0 = int(w * (0.12 + i * 0.14))
        y0 = int(lane_y - i * h * 0.024)
        draw.line([(x0, y0), (x0 + int(w * 0.045), y0 - int(h * 0.008))], fill=(245, 158, 11, 135), width=max(4, w // 180))

    gdraw = ImageDraw.Draw(layer, "RGBA")
    gdraw.ellipse((w * 0.58, h * 0.46, w * 1.14, h * 1.20), fill=(147, 197, 253, 38))
    layer = layer.filter(ImageFilter.GaussianBlur(radius=max(20, w // 35)))
    sharp = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(sharp, "RGBA")
    sdraw.polygon(
        [(w * 0.62, 0), (w, 0), (w, h * 0.72), (w * 0.78, h * 0.56)],
        fill=(147, 197, 253, 26),
    )
    sdraw.polygon(
        [(0, h * 0.74), (w * 0.34, h), (0, h)],
        fill=(245, 158, 11, 34),
    )
    sdraw.rounded_rectangle(
        (w * 0.70, h * 0.17, w * 1.08, h * 0.29),
        radius=18,
        fill=(255, 255, 255, 20),
        outline=(147, 197, 253, 45),
        width=2,
    )
    sdraw.rounded_rectangle(
        (-w * 0.05, h * 0.12, w * 0.32, h * 0.20),
        radius=14,
        fill=(255, 255, 255, 13),
        outline=(255, 255, 255, 25),
        width=2,
    )
    for i in range(9):
        offset = (seed * 31 + i * 79) % int(w)
        y = h * (0.18 + (i % 5) * 0.14)
        sdraw.line(
            [(offset - w * 0.16, y), (offset + w * 0.12, y + h * 0.10)],
            fill=(147, 197, 253, 30),
            width=2,
        )
    lane_y = int(h * 0.77)
    sdraw.line([(0, lane_y), (w, int(h * 0.60))], fill=(255, 255, 255, 42), width=max(3, w // 220))
    sdraw.line([(0, lane_y + 34), (w, int(h * 0.60) + 34)], fill=(147, 197, 253, 34), width=max(2, w // 320))
    for i in range(7):
        x0 = int(w * (0.12 + i * 0.14))
        y0 = int(lane_y - i * h * 0.024)
        sdraw.line([(x0, y0), (x0 + int(w * 0.045), y0 - int(h * 0.008))], fill=(245, 158, 11, 135), width=max(4, w // 180))
    layer.alpha_composite(sharp)
    img.alpha_composite(layer)


def text_bbox(draw, xy, text, font_obj):
    return draw.textbbox(xy, text, font=font_obj)


def fit_font(draw, text, max_width, start_size, min_size=24, bold=False):
    size = start_size
    while size >= min_size:
        fnt = font(size, bold=bold)
        if text_bbox(draw, (0, 0), text, fnt)[2] <= max_width:
            return fnt
        size -= 2
    return font(min_size, bold=bold)


def wrap_by_pixels(draw, text, font_obj, max_width):
    words = text.split()
    if len(words) == 1:
        return textwrap.wrap(text, width=max(4, int(max_width / max(12, font_obj.size * 0.58)))) or [text]
    lines = []
    current = ""
    for word in words:
        test = word if not current else f"{current} {word}"
        if text_bbox(draw, (0, 0), test, font_obj)[2] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_brand_mark(draw, width, height):
    mark_x, mark_y = int(width * 0.07), int(height * 0.10)
    draw.rounded_rectangle((mark_x, mark_y, mark_x + 58, mark_y + 58), radius=12, fill=WHITE)
    draw.polygon(
        [(mark_x + 15, mark_y + 39), (mark_x + 30, mark_y + 15), (mark_x + 43, mark_y + 39)],
        fill=BRAND_BLUE,
    )
    draw.line((mark_x + 21, mark_y + 38, mark_x + 37, mark_y + 38), fill=ORANGE, width=4)
    draw.text((mark_x + 76, mark_y + 2), COMPANY, font=font(28, bold=True), fill=WHITE)
    draw.text((mark_x + 76, mark_y + 34), SITE, font=font(18), fill=LIGHT_BLUE)


def save_jpg(img, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(path, "JPEG", quality=92, optimize=True, progressive=True)


def create_canvas(width, height, seed=0):
    img = gradient_background(width, height).convert("RGBA")
    add_decor(img, seed=seed)
    return img


def draw_centered_multiline(draw, lines, center_x, top, font_obj, fill, spacing):
    y = top
    for line in lines:
        bbox = text_bbox(draw, (0, 0), line, font_obj)
        draw.text((center_x - (bbox[2] - bbox[0]) / 2, y), line, font=font_obj, fill=fill)
        y += (bbox[3] - bbox[1]) + spacing
    return y


def generate_default_og():
    img = create_canvas(1200, 630, seed=3)
    draw = ImageDraw.Draw(img, "RGBA")
    draw_brand_mark(draw, 1200, 630)

    title_font = font(68, bold=True)
    cn_font = font(46, bold=True)
    tag_font = font(34)
    y = 220
    y = draw_centered_multiline(draw, [COMPANY], 600, y, title_font, WHITE, 18)
    y = draw_centered_multiline(draw, [COMPANY_CN], 600, y + 4, cn_font, LIGHT_BLUE, 22)
    draw_centered_multiline(draw, [TAGLINE], 600, y + 16, tag_font, MUTED, 10)

    draw.rounded_rectangle((330, 500, 870, 508), radius=4, fill=ORANGE)
    save_jpg(img, PUBLIC_IMAGES / "og-default.jpg")


def generate_product_og(slug, name, seed):
    img = create_canvas(1200, 630, seed=seed)
    draw = ImageDraw.Draw(img, "RGBA")
    draw_brand_mark(draw, 1200, 630)

    title_font = fit_font(draw, name, 900, 86, 50, bold=True)
    subtitle_font = font(34)
    title_bbox = text_bbox(draw, (0, 0), name, title_font)
    x = 90
    y = 255
    draw.text((x + 3, y + 5), name, font=title_font, fill=(0, 0, 0, 70))
    draw.text((x, y), name, font=title_font, fill=WHITE)
    draw.text((x, y + (title_bbox[3] - title_bbox[1]) + 32), PRODUCT_SUBTITLE, font=subtitle_font, fill=LIGHT_BLUE)

    draw.rounded_rectangle((90, 492, 360, 500), radius=4, fill=ORANGE)
    site_font = font(24, bold=True)
    site_bbox = text_bbox(draw, (0, 0), SITE, site_font)
    draw.text((1120 - site_bbox[2], 548), SITE, font=site_font, fill=(230, 240, 255))
    save_jpg(img, PUBLIC_IMAGES / f"{slug}-og.jpg")


def generate_product_hero(slug, name, seed):
    img = create_canvas(800, 400, seed=seed + 19)
    draw = ImageDraw.Draw(img, "RGBA")
    draw_brand_mark(draw, 800, 400)

    title_font = fit_font(draw, name, 620, 56, 34, bold=True)
    sub_font = font(23)
    draw.text((58, 176), name, font=title_font, fill=WHITE)
    title_h = text_bbox(draw, (0, 0), name, title_font)[3]
    draw.text((60, 176 + title_h + 24), PRODUCT_SUBTITLE, font=sub_font, fill=LIGHT_BLUE)
    draw.rounded_rectangle((60, 318, 252, 325), radius=4, fill=ORANGE)
    draw.text((610, 336), SITE, font=font(17, bold=True), fill=(232, 242, 255))
    save_jpg(img, PRODUCT_IMAGES / f"{slug}-hero.jpg")


def discover_news():
    candidates = []
    for folder_name in ("news", "blog", "posts", "content/news", "content/blog", "src/content/news", "src/content/blog"):
        folder = ROOT / folder_name
        if folder.exists():
            candidates.extend(folder.rglob("*.md"))
            candidates.extend(folder.rglob("*.mdx"))
    return sorted(set(candidates))


def generate_news_default():
    img = create_canvas(1200, 630, seed=71)
    draw = ImageDraw.Draw(img, "RGBA")
    draw_brand_mark(draw, 1200, 630)
    draw.text((92, 256), "News & Insights", font=font(76, bold=True), fill=WHITE)
    draw.text((96, 350), TAGLINE, font=font(34), fill=LIGHT_BLUE)
    draw.rounded_rectangle((94, 490, 430, 498), radius=4, fill=ORANGE)
    save_jpg(img, PUBLIC_IMAGES / "news-og-default.jpg")


def generate_news_item(path, seed):
    meta = parse_frontmatter(path)
    title = meta.get("title") or path.stem.replace("-", " ").title()
    slug = meta.get("slug") or path.stem

    img = create_canvas(1200, 630, seed=seed)
    draw = ImageDraw.Draw(img, "RGBA")
    draw_brand_mark(draw, 1200, 630)
    title_font = fit_font(draw, title, 940, 62, 36, bold=True)
    lines = wrap_by_pixels(draw, title, title_font, 930)[:3]
    draw.text((92, 224), "News", font=font(28, bold=True), fill=ORANGE)
    y = 272
    for line in lines:
        draw.text((92, y), line, font=title_font, fill=WHITE)
        y += text_bbox(draw, (0, 0), line, title_font)[3] + 18
    draw.text((96, 520), SITE, font=font(24, bold=True), fill=LIGHT_BLUE)
    save_jpg(img, NEWS_IMAGES / f"{slug}-og.jpg")


def main():
    ensure_dirs()
    generate_default_og()

    for idx, (slug, fallback_name) in enumerate(PRODUCTS, start=1):
        md_path = ROOT / f"{slug}.md"
        meta = parse_frontmatter(md_path) if md_path.exists() else {}
        name = fallback_name or meta.get("title") or slug.replace("-", " ").title()
        generate_product_og(slug, name, seed=idx * 11)
        generate_product_hero(slug, name, seed=idx * 11)

    generate_news_default()
    for idx, news_path in enumerate(discover_news(), start=1):
        generate_news_item(news_path, seed=100 + idx * 13)

    generated = sorted(p for p in OUT.rglob("*") if p.is_file())
    print("生成完成：")
    for path in generated:
        print(f"{path} - {path.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
