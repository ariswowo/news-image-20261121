#!/usr/bin/env python3
"""make.fun bounty news-image-20261121 — entry program (Python 3.13).

Writes one image to /output/entry.png.

The image itself is generated offline, deterministically, by
build_image.py (PIL, system DejaVu fonts, no network) and shipped in
this repository as assets/entry.png. This program — standard library
only, no network, no randomness — copies those exact bytes to
/output/entry.png, so two runs always write identical bytes.

This is the approach the bounty itself names: "the simplest program
copies an image the repository holds".

To regenerate the bundled image locally:
    python3 build_image.py

To run this entry locally (OUTPUT_DIR overrides the /output default):
    OUTPUT_DIR=/tmp/out python3 main.py
"""
import hashlib
import os
import shutil
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent / "assets" / "entry.png"


def main() -> int:
    out_dir = Path(os.environ.get("OUTPUT_DIR", "/output"))
    out = out_dir / "entry.png"
    if not SRC.is_file():
        print(f"missing bundled image: {SRC}", file=sys.stderr)
        return 1
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SRC, out)
    data = out.read_bytes()
    print(f"wrote {out} ({len(data)} bytes, "
          f"sha256={hashlib.sha256(data).hexdigest()})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
