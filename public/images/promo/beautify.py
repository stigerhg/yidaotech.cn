#!/usr/bin/env python3
"""Beautify product shipping photo for promotional use."""
from PIL import Image, ImageEnhance, ImageDraw, ImageFont
import os

img_path = '/Volumes/Ext-SSd/AI/cache/documents/doc_432f4e6224f2_mmexport1780154135771.jpg'
outdir = '/Volumes/Ext-SSd/yidaotech.xyz/public/images/promo'
os.makedirs(outdir, exist_ok=True)

img = Image.open(img_path)
print(f"Original: {img.size} {img.mode}")

# Sample pixel colors to understand image content
w, h = img.size
regions = [
    ('top_center', w//3, 0, 2*w//3, h//4),
    ('mid_left', 0, h//3, w//2, 2*h//3),
    ('mid_right', w//2, h//3, w, 2*h//3),
    ('bottom', 0, 3*h//4, w, h),
]
for name, x1, y1, x2, y2 in regions:
    region = img.crop((x1, y1, x2, y2))
    pixels = list(region.getdata())
    if not pixels:
        continue
    avg_r = sum(p[0] for p in pixels) // len(pixels)
    avg_g = sum(p[1] for p in pixels) // len(pixels)
    avg_b = sum(p[2] for p in pixels) // len(pixels)
    b = (avg_r + avg_g + avg_b) / 3
    print(f"  {name}: avg RGB({avg_r},{avg_g},{avg_b}) brightness={b:.0f}")

# --- Apply enhancements ---
enhanced = img.copy()
enhanced = ImageEnhance.Brightness(enhanced).enhance(1.12)
enhanced = ImageEnhance.Contrast(enhanced).enhance(1.18)
enhanced = ImageEnhance.Color(enhanced).enhance(1.15)
enhanced = ImageEnhance.Sharpness(enhanced).enhance(1.3)

# Save enhanced
enhanced_path = os.path.join(outdir, 'promo_enhanced.jpg')
enhanced.save(enhanced_path, 'JPEG', quality=92)
print(f"\nEnhanced: {enhanced_path} ({os.path.getsize(enhanced_path)} bytes)")

# --- Hero banner 1200x675 with branding ---
hero = enhanced.copy()
cw, ch = hero.size
target_ratio = 1200/675

if cw/ch > target_ratio:
    new_w = int(ch * target_ratio)
    hero = hero.crop(((cw - new_w)//2, 0, (cw + new_w)//2, ch))
else:
    new_h = int(cw / target_ratio)
    hero = hero.crop((0, (ch - new_h)//2, cw, (ch + new_h)//2))
hero = hero.resize((1200, 675), Image.LANCZOS)

# Branding overlay
hero = hero.convert('RGBA')
bar_h = 90
overlay = Image.new('RGBA', (1200, bar_h), (30, 64, 175, 195))
hero.paste(overlay, (0, 675 - bar_h), overlay)

try:
    font_lg = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 30)
    font_sm = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 18)
except:
    font_lg = font_sm = ImageFont.load_default()

draw = ImageDraw.Draw(hero)
draw.text((30, 675 - bar_h + 10), "Shining Road Technology", fill='white', font=font_lg)
draw.text((30, 675 - bar_h + 48), "yidaotech.xyz  |  Professional Pavement Maintenance", fill='#93C5FD', font=font_sm)

hero_path = os.path.join(outdir, 'promo_hero.jpg')
hero.convert('RGB').save(hero_path, 'JPEG', quality=92)
print(f"Hero: {hero_path} ({os.path.getsize(hero_path)} bytes)")

# --- Square 800x800 ---
sq = enhanced.copy()
size = min(cw, ch)
sq = sq.crop(((cw-size)//2, (ch-size)//2, (cw+size)//2, (ch+size)//2))
sq = sq.resize((800, 800), Image.LANCZOS)
sq_path = os.path.join(outdir, 'promo_square.jpg')
sq.save(sq_path, 'JPEG', quality=92)
print(f"Square: {sq_path} ({os.path.getsize(sq_path)} bytes)")

# --- Web-optimized 800w ---
web = enhanced.copy()
web.thumbnail((800, 800), Image.LANCZOS)
web_path = os.path.join(outdir, 'promo_web.jpg')
web.save(web_path, 'JPEG', quality=85, optimize=True)
print(f"Web: {web_path} ({os.path.getsize(web_path)} bytes)")

print("\n=== ALL DONE ===")
