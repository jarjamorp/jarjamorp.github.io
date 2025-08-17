import argparse
from tools.config import load_config
from tools.pages import build_index,build_index_with_galleries
from tools.models import Gallery, ImageAsset, VideoAsset

def main():
    parser = argparse.ArgumentParser(prog="site-tools")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("build-index")
    args = parser.parse_args()

    cfg = load_config()
    if args.cmd == "build-index":
        fake = Gallery(
            slug="beach-day-2025",
            title="Beach Day (2025)",
            date="2025-08-12",
            cover_image_url=None,
            images=[],
            videos=[],
        )
        build_index_with_galleries(cfg, [fake])
        print("Wrote site/index.html with 1 fake gallery")

if __name__ == "__main__":
    main()
