import argparse
from tools.config import load_config
from tools.pages import build_index

def main():
    parser = argparse.ArgumentParser(prog="site-tools")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("build-index")
    args = parser.parse_args()

    cfg = load_config()
    if args.cmd == "build-index":
        out = build_index(cfg)
        print(f"Wrote {out}")

if __name__ == "__main__":
    main()
