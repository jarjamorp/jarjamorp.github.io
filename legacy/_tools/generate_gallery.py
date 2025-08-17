#!/usr/bin/env python3
import argparse, datetime, os, sys, pathlib, html
from typing import List

# Optional HEIC support if pillow-heif is installed
try:
    import pillow_heif  # type: ignore
    pillow_heif.register_heif_opener()
except Exception:
    pass

from PIL import Image, ImageOps  # type: ignore

SUPPORTED_EXTS = (".jpg", ".jpeg", ".png", ".heic", ".heif", ".webp")

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{{TITLE}}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  :root{--bg:#fafafa;--fg:#111;--card:#fff;--muted:#666;}
  @media (prefers-color-scheme: dark){
    :root{--bg:#0b0b0b;--fg:#f0f0f0;--card:#111;--muted:#999;}
  }
  body{font-family:system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;margin:0;padding:24px;background:var(--bg);color:var(--fg)}
  header{margin-bottom:16px}
  h1{margin:0 0 4px;font-size:28px;line-height:1.2}
  .date{color:var(--muted);font-size:14px}
  .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:10px}
  .grid a{display:block;border-radius:10px;overflow:hidden;background:var(--card);box-shadow:0 1px 3px rgba(0,0,0,.08)}
  .grid img{width:100%;height:100%;object-fit:cover;display:block}
  a{text-decoration:none;color:inherit}
</style>
</head>
<body>
  <header>
    <h1>{{TITLE}}</h1>
    <div class="date">{{DATE}}</div>
  </header>
  <main class="grid">
{{ITEMS}}
  </main>
</body>
</html>
"""

def slugify(s: str) -> str:
    return "".join(c.lower() if c.isalnum() else "-" for c in s).strip("-").replace("--","-")

def find_images(folder: pathlib.Path) -> List[pathlib.Path]:
    files = []
    for p in sorted(folder.iterdir()):
        if p.is_file() and p.suffix.lower() in SUPPORTED_EXTS:
            files.append(p)
    return files

def to_webp(src: pathlib.Path, dst: pathlib.Path, max_side: int, quality: int) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im)
        w, h = im.size
        if max(w, h) > max_side:
            if w >= h:
                nh = int(h * (max_side / float(w)))
                im = im.resize((max_side, nh), Image.LANCZOS)
            else:
                nw = int(w * (max_side / float(h)))
                im = im.resize((nw, max_side), Image.LANCZOS)
        im.save(dst, format="WEBP", quality=quality, method=6)

def build_html(title: str, date_str: str, webps: List[pathlib.Path], rel_from: pathlib.Path) -> str:
    items = []
    for p in webps:
        rel = p.relative_to(rel_from).as_posix()
        items.append(f'    <a href="{rel}"><img loading="lazy" src="{rel}" alt=""></a>')
    return TEMPLATE.replace("{{TITLE}}", html.escape(title)) \
                   .replace("{{DATE}}", html.escape(date_str)) \
                   .replace("{{ITEMS}}", "\n".join(items))

def main():
    ap = argparse.ArgumentParser(description="Convert images to WebP and generate index.html in a folder (no date prefix).")
    ap.add_argument("--input", "-i", default=".", help="Folder with source images (default: .)")
    ap.add_argument("--outdir", "-o", default=None, help="Output folder. Default: same as --input (in-place).")
    ap.add_argument("--title", "-t", required=True, help="Gallery title (used in <title>/<h1>, NOT in folder name).")
    ap.add_argument("--date", "-d", default=None, help="Date string to display (default: today UTC YYYY-MM-DD).")
    ap.add_argument("--max-size", type=int, default=2048, help="Max longer side for WebP resize (default: 2048)")
    ap.add_argument("--quality", type=int, default=86, help="WebP quality (default: 86)")
    args = ap.parse_args()

    in_dir = pathlib.Path(args.input).resolve()
    out_dir = pathlib.Path(args.outdir).resolve() if args.outdir else in_dir  # in-place by default
    date_str = args.date or datetime.datetime.utcnow().strftime("%Y-%m-%d")

    if not in_dir.exists() or not in_dir.is_dir():
        print(f"ERROR: input folder not found: {in_dir}", file=sys.stderr)
        sys.exit(2)

    imgs = find_images(in_dir)
    if not imgs:
        print(f"ERROR: no images found in {in_dir}", file=sys.stderr)
        sys.exit(3)

    # Convert every supported image in input to WebP in out_dir (same folder by default)
    webps: List[pathlib.Path] = []
    for src in imgs:
        # Keep basename, change extension to .webp
        dst = (out_dir / src.with_suffix(".webp").name)
        to_webp(src, dst, args.max_size, args.quality)
        webps.append(dst)

    # Generate index.html into out_dir
    html_out = build_html(args.title, date_str, webps, out_dir)
    (out_dir / "index.html").write_text(html_out, encoding="utf-8")

    print(f"Generated {out_dir}/index.html with {len(webps)} images")

if __name__ == "__main__":
    main()
