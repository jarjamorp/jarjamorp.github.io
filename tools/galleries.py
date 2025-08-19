from __future__ import annotations
from pathlib import Path
from datetime import datetime
import yaml
from yaml import YAMLError

from tools.models import Gallery, ImageAsset
from tools.pages import make_env, render_to_file
from tools.images import build_variants
from tools.cache import file_digest, key_for
import re

PIPELINE_VERSION = "img-v1"  # bump this if you change encoder logic in a breaking way
REQUIRED_KEYS = {"title", "date"}
SUPPORTED_IMAGE_EXTS = {'.jpg','.jpeg','.png','.heic','.heif','.tif','.tiff','.webp'}

def _load_meta(meta_p: Path) -> dict:
    """Load and validate gallery.yml; give clear errors if it's empty/invalid."""
    try:
        raw = meta_p.read_text(encoding="utf-8")
        data = yaml.safe_load(raw)
    except YAMLError as e:
        raise SystemExit(f"[YAML ERROR] {meta_p}: {e}") from e

    if not data:
        raise SystemExit(f"[YAML ERROR] {meta_p}: file is empty (needs: {', '.join(sorted(REQUIRED_KEYS))})")
    if not isinstance(data, dict):
        raise SystemExit(f"[YAML ERROR] {meta_p}: expected a mapping/object at top level")
    missing = REQUIRED_KEYS - data.keys()
    if missing:
        raise SystemExit(f"[YAML ERROR] {meta_p}: missing required keys: {', '.join(sorted(missing))}")
    return data

def _natural_key(name: str):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r'(\d+)', name)]

def _autoscan_image_filenames(images_dir: Path) -> list[str]:
    if not images_dir.exists():
        return []
    files = [
        p.name for p in images_dir.iterdir()
        if p.is_file()
        and p.suffix.lower() in SUPPORTED_IMAGE_EXTS
        and not p.stem.endswith('_thumb')
    ]
    files.sort(key=_natural_key)
    return files

def _output_stem(fname: str, idx: int, cfg: dict) -> str:
    mode = (cfg["images"].get("naming") or "preserve").lower()
    if mode == "index":
        width = int(cfg["images"].get("index_pad", 3))
        return f"{idx+1:0{width}d}"  # 1-based: 001, 002, ...
    # default: keep original base name
    return Path(fname).stem

def scan_galleries(cfg: dict) -> list[Gallery]:
    root = Path(cfg["paths"]["content"]) / "galleries"
    galleries: list[Gallery] = []

    for gdir in sorted(root.glob("*/"), key=lambda p: p.name):
        meta_p = gdir / "gallery.yml"
        if not meta_p.exists():
            continue
        meta = _load_meta(meta_p)

        slug = gdir.name
        asset_base = (cfg.get("asset_base_url") or "").rstrip("/")
        out_dirname = cfg["images"].get("output_dir_name", "img")
        base_url = f"{asset_base}/galleries/{slug}" if asset_base else f"/galleries/{slug}"

        # originals folder on disk
        originals_dir = cfg["images"].get("originals_dir_name", "images")
        images_dir = gdir / originals_dir

        # allow auto cover and auto images
        cover_cfg = meta.get("cover", "auto")
        raw_images = meta.get("images", "auto")

        if raw_images in ("auto", "*", None) or (isinstance(raw_images, dict) and raw_images.get("auto")):
            files = _autoscan_image_filenames(images_dir)
            meta_images = [{"file": f, "alt": ""} for f in files]
        elif isinstance(raw_images, list):
            meta_images = raw_images
        else:
            raise SystemExit(f"[YAML ERROR] {meta_p}: 'images' must be a list, 'auto', or '*'")

        # default cover to first image if requested/unspecified
        if cover_cfg in (None, "auto") and meta_images:
            cover = meta_images[0]["file"]
        else:
            cover = cover_cfg

        cover_url = f"{base_url}/{out_dirname}/{Path(cover).stem}.webp" if cover else None

        # map to ImageAsset (use naming strategy)
        image_items: list[ImageAsset] = []
        for idx, item in enumerate(meta_images):
            fname = str(item["file"])
            stem = _output_stem(fname, idx, cfg)
            image_items.append(
                ImageAsset(
                    webp_url=f"{base_url}/{out_dirname}/{stem}.webp",
                    thumb_url=f"{base_url}/{out_dirname}/{stem}_thumb.webp",
                    alt=item.get("alt", ""),
                    source_file=fname,
                )
            )

        # ensure cover gets processed even if it wasn't in the list
        if cover and all(Path(i.source_file).stem != Path(cover).stem for i in image_items if i.source_file):
            try:
                ci = next(i for i, it in enumerate(meta_images) if it["file"] == cover)
            except StopIteration:
                ci = 0
            cstem = _output_stem(cover, ci, cfg)
            image_items.insert(0, ImageAsset(
                webp_url=f"{base_url}/{out_dirname}/{cstem}.webp",
                thumb_url=f"{base_url}/{out_dirname}/{cstem}_thumb.webp",
                alt="",
                source_file=cover,
            ))

        # >>> append the gallery unconditionally (not inside the cover-if) <<<
        galleries.append(Gallery(
            slug=slug,
            title=str(meta["title"]),
            date=str(meta["date"]),
            cover_image_url=cover_url,
            images=image_items,
            videos=[],
        ))

    galleries.sort(key=lambda g: g.date, reverse=True)
    return galleries


def build_gallery_pages(cfg: dict, galleries: list[Gallery]) -> None:
    env = make_env(Path(cfg["paths"]["templates"]))
    out_root = Path(cfg["paths"]["output"]) / "galleries"
    for g in galleries:
        out = out_root / g.slug / "index.html"
        ctx = {
            "site_title": cfg.get("site_title", "My Site"),
            "build_time": datetime.now().isoformat(timespec="seconds"),
            "gallery": g,
        }
        render_to_file(env, "gallery.html", ctx, out)
        
def process_gallery_media(cfg: dict, g: Gallery, *, manifest: dict, project_root: Path, force: bool = False) -> int:
    """
    Convert originals → webp + thumb using a manifest cache for idempotence.
    Returns count of (re)built images.
    """
    originals_dir = cfg["images"].get("originals_dir_name", "images")
    out_dirname = cfg["images"].get("output_dir_name", "img")

    content_root = Path(cfg["paths"]["content"]) / "galleries" / g.slug / originals_dir
    output_root  = Path(cfg["paths"]["output"]) / "galleries" / g.slug / out_dirname

    thumb_size = (
        int(cfg["images"]["thumb"]["width"]),
        int(cfg["images"]["thumb"]["height"]),
    )
    quality = int(cfg["images"].get("webp_quality", 82))

    # What we consider part of the processing "options"
    options = {
        "pipeline": PIPELINE_VERSION,
        "webp_quality": quality,
        "thumb_w": thumb_size[0],
        "thumb_h": thumb_size[1],
    }


    changed = 0
    entries = manifest.setdefault("entries", {})
    for idx, img in enumerate(g.images):
        if not img.source_file: continue
        src = content_root / img.source_file
        if not src.exists():
            print(f"[WARN] {g.slug}: missing source {src}")
            continue
        stem = _output_stem(img.source_file, idx, cfg)
        webp_out  = output_root / f"{stem}.webp"
        thumb_out = output_root / f"{stem}_thumb.webp"

        key = key_for(src, project_root)
        prev = entries.get(key)

        # compute digest of (file bytes + options)
        try:
            digest = file_digest(src, options)
        except Exception as e:
            print(f"[ERROR] {g.slug}: cannot hash {src}: {e}")
            continue

        # Skip if unchanged and outputs exist (unless --force)
        outputs_exist = webp_out.exists() and thumb_out.exists()
        if (not force) and prev and prev.get("digest") == digest and outputs_exist:
            continue

        # Rebuild
        try:
            build_variants(src, webp_out, thumb_out, thumb_size=thumb_size, quality=quality, only_if_newer=False)
            changed += 1
        except Exception as e:
            print(f"[ERROR] {g.slug}: failed to process {src}: {e}")
            continue

        # Update manifest entry
        entries[key] = {
            "digest": digest,
            "outputs": [webp_out.as_posix(), thumb_out.as_posix()],
            "gallery": g.slug,
        }

    return changed
