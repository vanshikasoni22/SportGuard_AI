"""
generate_dataset.py — Programmatically create simulated sports media images
                      (originals + modified variants) for the demo dataset.

Run once:  python generate_dataset.py
Output:    backend/dataset_media/*.png
"""
import os
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

OUTPUT_DIR = Path("dataset_media")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Colour palettes per "team / event"
TEAMS = [
    {"name": "FC_Blaze",       "bg": (220, 38,  38),  "fg": (255, 255, 255)},
    {"name": "Ocean_United",   "bg": (37,  99,  235),  "fg": (255, 255, 255)},
    {"name": "GreenStorm_FC",  "bg": (22,  163, 74),   "fg": (255, 255, 0)},
    {"name": "Thunder_Hawks",  "bg": (124, 58,  237),  "fg": (255, 200, 0)},
    {"name": "Iron_Wolves",    "bg": (15,  23,  42),   "fg": (250, 204, 21)},
]

SIZE = (512, 512)


def draw_original(team: dict) -> Image.Image:
    img = Image.new("RGB", SIZE, team["bg"])
    draw = ImageDraw.Draw(img)

    # Outer border
    draw.rectangle([10, 10, SIZE[0]-10, SIZE[1]-10], outline=team["fg"], width=6)

    # Circle emblem
    cx, cy, r = SIZE[0]//2, SIZE[1]//2 - 30, 120
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=team["fg"], outline=team["bg"], width=4)

    # Team name
    try:
        font_big = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 44)
        font_sm  = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 28)
    except Exception:
        font_big = ImageFont.load_default()
        font_sm  = font_big

    name = team["name"].replace("_", " ")
    draw.text((SIZE[0]//2, SIZE[1]//2 + 100), name, fill=team["fg"],
              font=font_big, anchor="mm")
    draw.text((SIZE[0]//2, SIZE[1]//2 + 155), "Official Media", fill=team["fg"],
              font=font_sm, anchor="mm")

    # Decorative lines
    for y in [60, SIZE[1]-60]:
        draw.line([(40, y), (SIZE[0]-40, y)], fill=team["fg"], width=3)

    return img


def make_cropped(img: Image.Image) -> Image.Image:
    """Simulate crop — remove 10% from each edge."""
    w, h = img.size
    margin = int(w * 0.10)
    cropped = img.crop((margin, margin, w-margin, h-margin))
    return cropped.resize(SIZE)


def make_resized(img: Image.Image) -> Image.Image:
    """Downsample then upsample — simulates re-upload at lower resolution."""
    small = img.resize((128, 128))
    return small.resize(SIZE)


def make_filtered(img: Image.Image) -> Image.Image:
    """Apply slight blur + brightness shift — simulates filter / watermark."""
    blurred = img.filter(ImageFilter.GaussianBlur(radius=2))
    enhanced = ImageEnhance.Brightness(blurred).enhance(0.80)
    return enhanced


def make_tinted(img: Image.Image) -> Image.Image:
    """Overlay a semi-transparent colour tint — platform repost simulation."""
    tint = Image.new("RGB", SIZE, (255, 120, 0))
    return Image.blend(img, tint, alpha=0.15)


VARIANTS = [
    ("crop",    make_cropped),
    ("resize",  make_resized),
    ("filter",  make_filtered),
    ("tint",    make_tinted),
]


def generate():
    generated = []
    for team in TEAMS:
        # Original
        orig = draw_original(team)
        orig_path = OUTPUT_DIR / f"{team['name']}_original.png"
        orig.save(orig_path)
        generated.append({"name": f"{team['name']} Original", "path": str(orig_path),
                           "is_original": True, "team": team["name"]})

        # Variants
        for var_name, fn in VARIANTS:
            variant = fn(orig)
            var_path = OUTPUT_DIR / f"{team['name']}_{var_name}.png"
            variant.save(var_path)
            generated.append({"name": f"{team['name']} ({var_name})",
                               "path": str(var_path),
                               "is_original": False, "team": team["name"]})

    print(f"✅  Generated {len(generated)} dataset images in '{OUTPUT_DIR}/'")
    return generated


if __name__ == "__main__":
    generate()
