import argparse
from tools.config import load_config
from tools.pages import build_index, build_index_with_galleries
from tools.models import Gallery, ImageAsset, VideoAsset
from tools.galleries import scan_galleries, build_gallery_pages, process_gallery_media

def main():
    parser = argparse.ArgumentParser(prog="site-tools")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("build-index")
    p = sub.add_parser("build-galleries")
    p.add_argument("--process-media", action="store_true", help="Convert images to WebP + thumbnails before rendering")
    args = parser.parse_args()

    cfg = load_config()
    if args.cmd == "build-index":
        galleries = scan_galleries(cfg)
        build_index_with_galleries(cfg, galleries)
        print(f"Wrote site/index.html with {len(galleries)} galleries")
    elif args.cmd == "build-galleries":
        galleries = scan_galleries(cfg)
        if args.process_media:
            total_changed = 0
            for g in galleries:
                total_changed += process_gallery_media(cfg, g)
            print(f"Processed images (updated {total_changed} item(s))")
        build_gallery_pages(cfg, galleries)
        print(f"Wrote {len(galleries)} gallery page(s)")

if __name__ == "__main__":
    main()
