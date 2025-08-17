# tools/images.py
from pathlib import Path
from typing import Tuple, Optional

from PIL import Image, ImageOps

def _ensure_dir(p: Path) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)

def _atomic_save_webp(img: Image.Image, path: Path, **save_kwargs) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    img.save(tmp, "WEBP", **save_kwargs)
    tmp.replace(path)

def to_webp(src: Path, dst: Path, quality: int = 82) -> None:
    _ensure_dir(dst)
    with Image.open(src) as im:
        # Respect camera rotation
        im = ImageOps.exif_transpose(im)
        _atomic_save_webp(im, dst, quality=quality, method=6)

def make_thumbnail(src: Path, dst: Path, size: Tuple[int, int] = (75, 75), quality: int = 82) -> None:
    _ensure_dir(dst)
    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im)
        im.thumbnail(size)  # keeps aspect ratio
        _atomic_save_webp(im, dst, quality=quality, method=6)

def build_variants(
    src: Path,
    webp_out: Path,
    thumb_out: Path,
    thumb_size: Tuple[int, int] = (75, 75),
    quality: int = 82,
    only_if_newer: bool = True,
) -> bool:
    """
    Returns True if we wrote/updated files, False if skipped.
    """
    if only_if_newer and webp_out.exists() and thumb_out.exists():
        src_m = src.stat().st_mtime
        if webp_out.stat().st_mtime >= src_m and thumb_out.stat().st_mtime >= src_m:
            return False

    to_webp(src, webp_out, quality=quality)
    make_thumbnail(src, thumb_out, size=thumb_size, quality=quality)
    return True
