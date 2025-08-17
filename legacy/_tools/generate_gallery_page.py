import argparse
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Tuple

try:
    from PIL import Image, ImageOps
except Exception as e:  # pragma: no cover
    Image = None  # type: ignore
    ImageOps = None  # type: ignore


# -------------------------
# Data structures
# -------------------------

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif", ".webp", ".heic", ".heif"}


@dataclass
class GalleryImage:
    index: int
    label: str
    src_full: Path
    src_thumb: Path
    href: str
    thumb_src: str
    alt: str


# -------------------------
# Utility helpers
# -------------------------

def ensure_pillow_available():
    if Image is None:
        raise RuntimeError(
            "Pillow is required. Install with: pip install Pillow"
        )


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def natural_key(s: str) -> List:
    import re

    return [int(text) if text.isdigit() else text.lower() for text in re.split(r"(\d+)", s)]


def iter_image_files(folder: Path) -> List[Path]:
    if not folder.exists() or not folder.is_dir():
        raise FileNotFoundError(f"Input folder not found: {folder}")

    files = [p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in ALLOWED_EXTENSIONS]
    files.sort(key=lambda p: natural_key(p.name))
    return files


def zero_padded_labels(count: int) -> List[str]:
    width = max(2, len(str(max(0, count))))
    return [str(i).zfill(width) for i in range(1, count + 1)]


# -------------------------
# Image processing (reusable)
# -------------------------

def convert_to_webp(src: Path, dst: Path, quality: int = 85, max_size: Optional[int] = None) -> None:
    """
    Convert an image to WEBP at `dst`.
    - Respects EXIF orientation.
    - If `max_size` is provided, scales the longest side to <= max_size.
    Idempotent: skips if `dst` exists and is newer than `src`.
    """
    ensure_pillow_available()

    if dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime:
        return

    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im)
        if max_size is not None:
            im.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        # Ensure RGB for formats like PNG with alpha
        if im.mode not in ("RGB", "RGBA"):
            im = im.convert("RGB")
        ensure_dir(dst.parent)
        im.save(dst, format="WEBP", quality=int(quality))


def create_thumbnail(src: Path, dst: Path, thumb_size: int = 480, quality: int = 80) -> None:
    """Create a WEBP thumbnail for `src` at `dst` with the given max side size."""
    convert_to_webp(src, dst, quality=quality, max_size=thumb_size)


# -------------------------
# HTML generation (reusable)
# -------------------------

def generate_gallery_list_items(images: Iterable[GalleryImage]) -> str:
    """
    Return HTML for the list of gallery items (anchors with thumbnails), one per line.
    Each item links to the full-size webp and displays the thumbnail webp.
    """
    lines: List[str] = []
    for img in images:
        lines.append(
            f'    <a class="gallery-item" href="{img.href}" aria-label="{img.alt}">'
            f'<img loading="lazy" decoding="async" src="{img.thumb_src}" alt="{img.alt}" /></a>'
        )
    return "\n".join(lines)


def generate_gallery_html_page(title: str, list_items_html: str) -> str:
    """
    Generate a full HTML page. This loosely matches a simple gallery template
    similar to an "autumn.html"-style gallery: heading + responsive grid.
    """
    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>{title}</title>
  <style>
    :root {{ --gap: 8px; }}
    body {{ margin: 0; font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif; }}
    header {{ padding: 24px 16px 8px; }}
    h1 {{ margin: 0; font-size: 2rem; }}
    .gallery {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
      gap: var(--gap);
      padding: 8px 16px 24px;
    }}
    .gallery-item {{
      display: block;
      border-radius: 6px;
      overflow: hidden;
      background: #f5f5f5;
    }}
    .gallery-item img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }}
  </style>
  <link rel=\"preload\" as=\"style\" href=\"/styles/gallery.css\" onload=\"this.rel='stylesheet'\">
  <noscript><link rel=\"stylesheet\" href=\"/styles/gallery.css\"></noscript>
  <meta name=\"robots\" content=\"noai, noimageai\" />
</head>
<body>
  <header>
    <h1>{title}</h1>
  </header>
  <main>
    <section class=\"gallery\">
{list_items_html}
    </section>
  </main>
  <script>
  // Optional: simple click-to-open in new tab for full image
  document.addEventListener('click', (e) => {{
    const a = e.target.closest('a.gallery-item');
    if (a && (e.metaKey || e.ctrlKey)) {{
      window.open(a.href, '_blank');
      e.preventDefault();
    }}
  }});
  </script>
}</html>
"""


# -------------------------
# Orchestrator (reusable)
# -------------------------

def build_gallery(
    source_dir: Path,
    assets_out_dir: Path,
    count_limit: Optional[int] = None,
    quality: int = 85,
    max_size: Optional[int] = None,
    thumb_size: int = 480,
) -> Tuple[List[GalleryImage], int]:
    """
    Convert images under `source_dir` into webp assets under `assets_out_dir`.
    Returns (images, total_found).
    - images: ordered list of GalleryImage with paths populated (absolute paths)
    - total_found: number of images discovered in `source_dir`
    """
    files = iter_image_files(source_dir)
    total = len(files)
    if count_limit is not None:
        files = files[:count_limit]

    labels = zero_padded_labels(len(files))

    result: List[GalleryImage] = []
    for idx, (src, label) in enumerate(zip(files, labels), start=1):
        full_name = f"{label}.webp"
        thumb_name = f"{label}_thumb.webp"
        full_out = assets_out_dir / full_name
        thumb_out = assets_out_dir / thumb_name

        convert_to_webp(src, full_out, quality=quality, max_size=max_size)
        create_thumbnail(src, thumb_out, thumb_size=thumb_size, quality=max(60, quality - 5))

        result.append(
            GalleryImage(
                index=idx,
                label=label,
                src_full=full_out,
                src_thumb=thumb_out,
                href=full_out.as_posix(),
                thumb_src=thumb_out.as_posix(),
                alt=f"{source_dir.name} {label}",
            )
        )

    return result, total


def relativeize_images(images: List[GalleryImage], html_out_dir: Path, assets_out_dir: Path) -> List[GalleryImage]:
    """Rewrite the href/src to be relative to the HTML file location."""
    rel_images: List[GalleryImage] = []
    for img in images:
        href = os.path.relpath(img.src_full, start=html_out_dir).replace(os.sep, "/")
        thumb = os.path.relpath(img.src_thumb, start=html_out_dir).replace(os.sep, "/")
        rel_images.append(
            GalleryImage(
                index=img.index,
                label=img.label,
                src_full=img.src_full,
                src_thumb=img.src_thumb,
                href=href,
                thumb_src=thumb,
                alt=img.alt,
            )
        )
    return rel_images


# -------------------------
# CLI
# -------------------------

def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate a gallery HTML page from a folder of images.")
    p.add_argument("gallery_page_name", help="Name of folder inside 'toprocess' to build a page for.")
    p.add_argument("--toprocess-dir", default="toprocess", help="Root folder containing galleries to process.")
    p.add_argument(
        "--output-dir",
        default="gallery_pages",
        help="Where to write the HTML page folder (defaults to 'gallery_pages/<name>/index.html').",
    )
    p.add_argument(
        "--assets-dir",
        default=None,
        help="Optional explicit assets output directory. Defaults to '<output-dir>/<name>/assets'.",
    )
    p.add_argument("--quality", type=int, default=85, help="WEBP quality (1-100). Default: 85")
    p.add_argument(
        "--max-size",
        type=int,
        default=2048,
        help="Max long side for full images (pixels). Use 0 to disable.",
    )
    p.add_argument("--thumb-size", type=int, default=480, help="Max long side for thumbnails (pixels).")
    p.add_argument("--limit", type=int, default=None, help="Only process first N images (for testing).")
    p.add_argument("--title", default=None, help="Override page title (defaults to folder name).")
    return p.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)

    gallery_name = args.gallery_page_name
    title = args.title or gallery_name

    toprocess_root = Path(args.toprocess_dir).resolve()
    source_dir = (toprocess_root / gallery_name).resolve()

    output_dir = Path(args.output_dir).resolve() / gallery_name
    html_out_dir = output_dir
    html_out_file = html_out_dir / "index.html"

    assets_out_dir = Path(args.assets_dir).resolve() if args.assets_dir else (output_dir / "assets")

    ensure_dir(html_out_dir)
    ensure_dir(assets_out_dir)

    max_size = int(args.max_size) if args.max_size and int(args.max_size) > 0 else None

    print(f"Building gallery '{gallery_name}' from {source_dir}")
    print(f"Assets -> {assets_out_dir}")
    print(f"HTML   -> {html_out_file}")

    images, total_found = build_gallery(
        source_dir=source_dir,
        assets_out_dir=assets_out_dir,
        count_limit=args.limit,
        quality=args.quality,
        max_size=max_size,
        thumb_size=args.thumb_size,
    )

    if not images:
        print("No images found to process.")
        return 1

    rel_images = relativeize_images(images, html_out_dir=html_out_dir, assets_out_dir=assets_out_dir)

    list_items_html = generate_gallery_list_items(rel_images)
    html = generate_gallery_html_page(title=title, list_items_html=list_items_html)

    html_out_file.write_text(html, encoding="utf-8")

    print(f"Processed {len(images)} images (of {total_found} found).")
    print(f"Wrote HTML page: {html_out_file}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    try:
        raise SystemExit(main())
    except FileNotFoundError as e:
        print(str(e), file=sys.stderr)
        raise SystemExit(1)
