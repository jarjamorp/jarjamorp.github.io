from pathlib import Path
import yaml
from tools.models import Gallery

def scan_galleries(cfg: dict) -> list[Gallery]:
    root = Path(cfg["paths"]["content"]) / "galleries"
    galleries: list[Gallery] = []
    for gdir in sorted(root.glob("*/"), key=lambda p: p.name):
        meta_p = gdir / "gallery.yml"
        if not meta_p.exists():
            continue
        meta = yaml.safe_load(meta_p.read_text(encoding="utf-8"))
        slug = gdir.name
        base_url = f"/galleries/{slug}"
        cover = meta.get("cover")
        cover_url = f"{base_url}/img/{Path(cover).stem}.webp" if cover else None
        galleries.append(Gallery(
            slug=slug,
            title=str(meta["title"]),
            date=str(meta["date"]),
            cover_image_url=cover_url,
            images=[],
            videos=[],
        ))
    # newest first
    galleries.sort(key=lambda g: g.date, reverse=True)
    return galleries
