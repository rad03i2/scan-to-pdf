from __future__ import annotations
import argparse, json, sys
from .core import Options, ScanError, convert


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="scan-to-pdf", description="Turn scanned images into a multi-page PDF locally.")
    p.add_argument("inputs", nargs="+", help="Image files and/or directories")
    p.add_argument("-o", "--output", required=True, help="Destination .pdf")
    p.add_argument("--recursive", action="store_true", help="Scan directories recursively")
    p.add_argument("--grayscale", action="store_true", help="Convert pages to grayscale")
    p.add_argument("--auto-contrast", action="store_true", help="Normalize page contrast")
    p.add_argument("--rotate", type=int, choices=(0,90,180,270), default=0, help="Clockwise page rotation")
    p.add_argument("--brightness", type=float, default=1.0, help="Brightness multiplier (default: 1.0)")
    p.add_argument("--quality", type=int, default=90, help="PDF image quality 1..100")
    p.add_argument("--dpi", type=int, default=150, help="PDF resolution 72..600")
    p.add_argument("--overwrite", action="store_true", help="Explicitly replace an existing output")
    p.add_argument("--json", action="store_true", help="Print machine-readable result")
    p.add_argument("--version", action="version", version="scan-to-pdf 1.0.0 — Radwan Abdulhadi Ahmed / @rad03i2")
    return p


def main(argv=None) -> int:
    args = parser().parse_args(argv)
    try:
        result = convert(args.inputs, args.output, Options(args.grayscale, args.auto_contrast, args.rotate, args.brightness, args.quality, args.dpi), args.recursive, args.overwrite)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"Created {result['output']} — {result['pages']} page(s), {result['bytes']} bytes")
        return 0
    except ScanError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
