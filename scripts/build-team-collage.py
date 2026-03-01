#!/usr/bin/env python3
"""Build a team photo collage from resources/team-photos/.

Reads presentation/team.yaml for author order and names.
Outputs resources/team-collage.png.

Layout: COLS columns, rows as needed. Each cell has a circular photo
above the author's (shortened) name.
"""

from pathlib import Path

import yaml
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).parent.parent
TEAM_YAML = ROOT / "presentation" / "team.yaml"
PHOTOS_DIR = ROOT / "resources" / "team-photos"
OUT_PATH = ROOT / "resources" / "team-collage.png"

# ── layout constants ──────────────────────────────────────────────────────────
COLS = 7
PHOTO_SIZE = 120          # px — diameter of circular photo
NAME_HEIGHT = 32          # px — space below photo for name
CELL_PAD_X = 18           # px — horizontal padding between cells
CELL_PAD_Y = 24           # px — vertical padding between rows
BG_COLOR = (255, 255, 255, 0)   # transparent background
TEXT_COLOR = (40, 40, 40)
FONT_SIZE = 13


def circular_crop(img: Image.Image, size: int) -> Image.Image:
    img = ImageOps.fit(img, (size, size), method=Image.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size, size), fill=255)
    result = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    result.paste(img.convert("RGBA"), mask=mask)
    return result


def short_name(full: str) -> str:
    parts = full.split()
    if len(parts) <= 2:
        return full
    # First name + last name only
    return f"{parts[0]} {parts[-1]}"


def main() -> None:
    with open(TEAM_YAML) as f:
        config = yaml.safe_load(f)
    authors = config["authors"]

    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", FONT_SIZE)
    except OSError:
        font = ImageFont.load_default()

    cell_w = PHOTO_SIZE + CELL_PAD_X
    cell_h = PHOTO_SIZE + NAME_HEIGHT + CELL_PAD_Y

    n = len(authors)
    rows = (n + COLS - 1) // COLS
    img_w = COLS * cell_w - CELL_PAD_X
    img_h = rows * cell_h - CELL_PAD_Y

    canvas = Image.new("RGBA", (img_w, img_h), BG_COLOR)
    draw = ImageDraw.Draw(canvas)

    for i, author in enumerate(authors):
        row, col = divmod(i, COLS)

        # Centre the last (possibly short) row
        row_count = n - row * COLS if row == rows - 1 else COLS
        row_offset = (COLS - row_count) * cell_w // 2

        x = col * cell_w + row_offset
        y = row * cell_h

        slug = author["name"].lower().replace(" ", "-")
        photo_path = PHOTOS_DIR / f"{slug}.png"

        if photo_path.exists():
            photo = circular_crop(Image.open(photo_path), PHOTO_SIZE)
            canvas.paste(photo, (x, y), photo)
        else:
            # Grey placeholder circle
            placeholder = Image.new("RGBA", (PHOTO_SIZE, PHOTO_SIZE), (0, 0, 0, 0))
            ImageDraw.Draw(placeholder).ellipse(
                (0, 0, PHOTO_SIZE, PHOTO_SIZE), fill=(180, 180, 180, 255)
            )
            canvas.paste(placeholder, (x, y), placeholder)
            print(f"  warn  no photo for {author['name']}")

        label = short_name(author["name"])
        bbox = draw.textbbox((0, 0), label, font=font)
        text_w = bbox[2] - bbox[0]
        text_x = x + (PHOTO_SIZE - text_w) // 2
        text_y = y + PHOTO_SIZE + 4
        draw.text((text_x, text_y), label, fill=TEXT_COLOR, font=font)

    canvas.save(OUT_PATH, "PNG")
    print(f"  saved {OUT_PATH.relative_to(ROOT)}  ({img_w}×{img_h}px)")


if __name__ == "__main__":
    main()
