from pathlib import Path
import textwrap

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parent.parent
SOURCE = Path("/Volumes/Ext-SSd/syyidao.com_20260628/images")
PRODUCT_OUT = ROOT / "public" / "images" / "products"
OG_OUT = ROOT / "public" / "images"

BLUE = (30, 64, 175)
ORANGE = (245, 158, 11)
WHITE = (255, 255, 255)


PRODUCTS = {
    "cold-mix-pothole-repair": {
        "source": SOURCE / "news" / "Upload_news_01393B14697D47C0EB7AEE173F71FC0F.jpg",
        "title": "Cold Mix Asphalt Pothole Repair",
        "subtitle": "Ready-to-use permanent repair material",
    },
    "cold-mix-additive": {
        "source": SOURCE / "news" / "Upload_news_6601C2202FF332B5E4F5DE42C0BF41B3.jpg",
        "title": "Cold Mix Asphalt Additive",
        "subtitle": "100% active formula for cold mix production",
    },
    "cold-mix-production-plant": {
        "source": SOURCE / "news" / "Upload_news_9D8BDEC87897D1EF63DB5F008ECF112C.jpg",
        "title": "Cold Mix Production Plant",
        "subtitle": "Turnkey asphalt material production line",
    },
    "cold-pour-crack-filler": {
        "source": SOURCE / "products" / "userfiles_images_20210329_1617028214573496.jpg",
        "title": "Cold Pour Crack Filler",
        "subtitle": "Ready-to-use crack filling compound",
    },
    "crack-sealing-tape": {
        "source": SOURCE / "products" / "userfiles_images_20210618_1624005544691500.jpg",
        "title": "Bituminous Crack Sealing Tape",
        "subtitle": "Fast self-adhesive pavement sealing",
    },
    "hot-applied-crack-sealer": {
        "source": SOURCE / "products" / "userfiles_images_20210618_1624005543422809.jpg",
        "title": "Hot-Applied Crack Sealer",
        "subtitle": "Commercial-grade asphalt crack sealant",
    },
    "emulsified-asphalt": {
        "source": SOURCE / "news" / "Upload_news_CC5991DA1BEF462C885DE8F7992E876E.jpg",
        "title": "Emulsified Asphalt",
        "subtitle": "Tack coat, chip seal and slurry applications",
    },
    "pavement-sealcoat": {
        "source": SOURCE / "products" / "userfiles_images_20210618_1624005546583936.jpg",
        "title": "Pavement Sealcoat",
        "subtitle": "Surface protection and asphalt beautification",
    },
    "technology-licensing": {
        "source": SOURCE / "products" / "userfiles_images_20210618_1624005543227588.jpg",
        "title": "Technology Licensing",
        "subtitle": "Formula transfer, QC and production support",
    },
    "quick-repair-cement": {
        "source": SOURCE / "products" / "userfiles_images_20210329_1617028431660803.jpg",
        "title": "Quick Repair Cement",
        "subtitle": "Fast-setting mortar for concrete pavement",
    },
    "ultra-thin-anti-skid-pavement": {
        "source": SOURCE / "news" / "Upload_news_8CF736523AD2475F4AA9A2F00653A942.jpg",
        "title": "Ultra-Thin Color Anti-Skid Pavement",
        "subtitle": "Color surfacing, cold patch and granule options",
    },
    "color-sprayed-pavement": {
        "source": SOURCE / "news" / "Upload_news_E4B8B9BD76C3D3BA4BB696A84519CA68.jpg",
        "title": "Color Sprayed Pavement Coating",
        "subtitle": "Fast color restoration for asphalt surfaces",
    },
}


def font(size: int, bold: bool = False):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            try:
                return ImageFont.truetype(str(path), size=size)
            except OSError:
                pass
    return ImageFont.load_default()


def cover_image(src: Path, size: tuple[int, int]) -> Image.Image:
    img = Image.open(src).convert("RGB")
    target_w, target_h = size
    scale = max(target_w / img.width, target_h / img.height)
    resized = img.resize((round(img.width * scale), round(img.height * scale)), Image.Resampling.LANCZOS)
    left = max(0, (resized.width - target_w) // 2)
    top = max(0, (resized.height - target_h) // 2)
    return resized.crop((left, top, left + target_w, top + target_h))


def draw_overlay(img: Image.Image, title: str, subtitle: str, *, og: bool = False) -> Image.Image:
    canvas = img.convert("RGBA")
    draw = ImageDraw.Draw(canvas, "RGBA")
    w, h = canvas.size

    # Darken the photograph slightly and add an industrial text panel.
    dark = ImageEnhance.Brightness(canvas.convert("RGB")).enhance(0.82).convert("RGBA")
    canvas.alpha_composite(dark)

    panel_h = int(h * (0.34 if og else 0.38))
    panel_y = h - panel_h
    panel = Image.new("RGBA", (w, panel_h), (8, 15, 28, 216))
    panel = panel.filter(ImageFilter.GaussianBlur(radius=0.2))
    canvas.alpha_composite(panel, (0, panel_y))

    pad = int(w * 0.07)
    accent_h = max(5, int(h * 0.012))
    draw.rounded_rectangle((pad, panel_y + int(panel_h * 0.17), pad + int(w * 0.16), panel_y + int(panel_h * 0.17) + accent_h), radius=accent_h // 2, fill=ORANGE)
    draw.text((pad, panel_y + int(panel_h * 0.24)), "SHINING ROAD TECHNOLOGY", font=font(18 if og else 16, True), fill=(180, 205, 255, 255))

    title_font = font(48 if og else 34, True)
    subtitle_font = font(25 if og else 20, False)
    max_chars = 32 if og else 25
    lines = textwrap.wrap(title, width=max_chars)
    y = panel_y + int(panel_h * 0.36)
    for line in lines[:2]:
        draw.text((pad, y), line, font=title_font, fill=WHITE)
        y += int((48 if og else 34) * 1.12)
    draw.text((pad, y + int(h * 0.02)), subtitle, font=subtitle_font, fill=(226, 232, 240, 255))

    draw.rounded_rectangle((w - pad - 110, panel_y + panel_h - 64, w - pad, panel_y + panel_h - 24), radius=20, fill=BLUE)
    draw.text((w - pad - 88, panel_y + panel_h - 55), "EXPORT", font=font(16, True), fill=WHITE)
    return canvas.convert("RGB")


def main():
    PRODUCT_OUT.mkdir(parents=True, exist_ok=True)
    OG_OUT.mkdir(parents=True, exist_ok=True)

    for slug, data in PRODUCTS.items():
        hero = draw_overlay(cover_image(data["source"], (800, 400)), data["title"], data["subtitle"])
        hero.save(PRODUCT_OUT / f"{slug}-hero.jpg", quality=88, optimize=True)

        og = draw_overlay(cover_image(data["source"], (1200, 630)), data["title"], data["subtitle"], og=True)
        og.save(OG_OUT / f"{slug}-og.jpg", quality=88, optimize=True)
        print(f"generated {slug}")


if __name__ == "__main__":
    main()
