import argparse
from tools.config import load_config
from tools.pages import build_index, build_index_with_galleries
from tools.models import Gallery, ImageAsset, VideoAsset
from tools.galleries import scan_galleries

def main():
    parser = argparse.ArgumentParser(prog="site-tools")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("build-index")
    args = parser.parse_args()

    cfg = load_config()
    if args.cmd == "build-index":
        galleries = scan_galleries(cfg)
        build_index_with_galleries(cfg, galleries)
        print(f"Wrote site/index.html with {len(galleries)} galleries")

if __name__ == "__main__":
    main()
