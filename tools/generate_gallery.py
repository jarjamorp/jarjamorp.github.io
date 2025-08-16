#!/usr/bin/env python3
"""Generate a static photo gallery from a directory of images."""

from __future__ import annotations

import argparse
import datetime as _dt
import re
import sys
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageOps


def slugify(text: str) -> str:
    """Return a filesystem-friendly slug for *text*."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text


def convert_image(src: Path, dest: Path, max_size: int, quality: int) -> bool:
    """Convert *src* image to WebP at *dest*.

    Returns True if conversion succeeded, False otherwise.
    """
    try:
        with Image.open(src) as im:
            im = ImageOps.exif_transpose(im)
            im.thumbnail((max_size, max_size), Image.LANCZOS)
            im.save(dest, "webp", quality=quality, method=6)
        return True
    except OSError as exc:
        print(f"Warning: skipping {src.name}: {exc}", file=sys.stderr)
        return False


def build_html(title: str, date: str, images: Iterable[str]) -> str:
    """Return gallery HTML string."""
    img_tags = "\n".join(
        f'        <a href="{img}"><img src="{img}" loading="lazy" alt=""></a>'
        for img in images
    )
    return f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
<meta charset=\"utf-8\">
<title>{title}</title>
<style>
:root {{
  color-scheme: light dark;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}}
body {{
  margin: 1rem;
}}
.gallery {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 0.5rem;
}}
.gallery img {{
  width: 100%;
  height: auto;
  border-radius: 4px;
  display: block;
}}
</style>
</head>
<body>
<header>
  <h1>{title}</h1>
  <p>{date}</p>
</header>
<section class=\"gallery\">
{img_tags}
</section>
</body>
</html>
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate a static photo gallery")
    parser.add_argument("--input", default="incoming", help="directory of source images")
    parser.add_argument("--outdir", default="photos", help="base output directory")
    parser.add_argument("--title", required=True, help="gallery title")
    parser.add_argument("--date", help="date string YYYY-MM-DD")
    parser.add_argument("--max-size", type=int, default=2048, help="max image dimension")
    parser.add_argument("--quality", type=int, default=86, help="WebP quality")
    args = parser.parse_args(argv)

    date = args.date or _dt.datetime.now(tz=_dt.timezone.utc).strftime("%Y-%m-%d")
    slug = slugify(args.title)
    out_dir = Path(args.outdir) / f"{date}-{slug}"
    out_dir.mkdir(parents=True, exist_ok=True)

    input_dir = Path(args.input)
    if not input_dir.is_dir():
        print(f"Error: input directory '{input_dir}' does not exist", file=sys.stderr)
        return 1

    exts = {".jpg", ".jpeg", ".png", ".heic"}
    images: list[str] = []
    for path in sorted(input_dir.iterdir()):
        if path.suffix.lower() not in exts or not path.is_file():
            continue
        dest = out_dir / (path.stem + ".webp")
        if convert_image(path, dest, args.max_size, args.quality):
            images.append(dest.name)

    if not images:
        print("Error: no images found for conversion", file=sys.stderr)
        return 1

    (out_dir / "index.html").write_text(
        build_html(args.title, date, images), encoding="utf-8"
    )
    print(f"Generated {out_dir}/index.html with {len(images)} images")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Acceptance test:

If I place 2–3 JPGs into `incoming/` and run:

    python tools/generate_gallery.py --title "Ocean Walk" --date 2025-08-16

…the script creates `photos/2025-08-16-ocean-walk/` containing `.webp` files and an `index.html` that displays them in a grid. Opening `index.html` in a browser shows the gallery.
"""
