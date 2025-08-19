import argparse
from tools.config import load_config
from tools.pages import build_index, build_index_with_galleries
from tools.models import Gallery, ImageAsset, VideoAsset
from tools.galleries import scan_galleries, build_gallery_pages, process_gallery_media, init_gallery
from pathlib import Path
from tools.cache import load_manifest, save_manifest

def main():
    parser = argparse.ArgumentParser(prog="site-tools")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("build-index")
    p = sub.add_parser("build-galleries")
    p.add_argument("--process-media", action="store_true", help="Convert images to WebP + thumbnails before rendering")
    p.add_argument("--force", action="store_true", help="Ignore cache and rebuild media even if unchanged")
    p_all = sub.add_parser("build-all")
    p_all.add_argument("--force", action="store_true", help="Ignore cache and rebuild media even if unchanged")
    p_new = sub.add_parser("init-gallery")
    p_new.add_argument("slug", help="Folder name under content/galleries")
    p_new.add_argument("--title", help="Display title (defaults from slug)")
    p_new.add_argument("--date", help="YYYY-MM-DD (defaults to today)")

    args = parser.parse_args()

    cfg = load_config()
    if args.cmd == "build-index":
        galleries = scan_galleries(cfg)
        build_index_with_galleries(cfg, galleries)
        print(f"Wrote site/index.html with {len(galleries)} galleries")
    elif args.cmd == "build-galleries":
        cfg = load_config()
        galleries = scan_galleries(cfg)

        manifest_path = Path(".cache/manifest.json")
        manifest = load_manifest(manifest_path)
        project_root = Path(".").resolve()

        total_changed = 0
        if args.process_media:
            for g in galleries:
                total_changed += process_gallery_media(
                    cfg, g, manifest=manifest, project_root=project_root, force=args.force
                )
            save_manifest(manifest_path, manifest)
            print(f"Processed images (updated {total_changed} item(s))  {'[FORCED]' if args.force else ''}")

        build_gallery_pages(cfg, galleries)
        print(f"Wrote {len(galleries)} gallery page(s)")
    elif args.cmd == "build-all":
        galleries = scan_galleries(cfg)
        manifest_path = Path(".cache/manifest.json")
        manifest = load_manifest(manifest_path)
        project_root = Path(".").resolve()

        total_changed = 0
        for g in galleries:
            total_changed += process_gallery_media(cfg, g, manifest=manifest, project_root=project_root, force=args.force)
        save_manifest(manifest_path, manifest)
        print(f"Processed images (updated {total_changed} item(s))  {'[FORCED]' if args.force else ''}")

        build_gallery_pages(cfg, galleries)
        from tools.pages import build_index_with_galleries
        build_index_with_galleries(cfg, galleries)
        print(f"Wrote {len(galleries)} gallery page(s) and index")
    elif args.cmd == "init-gallery":
        init_gallery(cfg, args.slug, args.title, args.date)


if __name__ == "__main__":
    main()
