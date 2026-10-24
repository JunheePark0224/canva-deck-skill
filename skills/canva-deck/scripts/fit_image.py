"""Crop an image to a Canva frame's aspect ratio, then scale it to the frame size (references/pitfalls.md 21:
Canva's crop_media zoomed the wrong way, so crop locally and insert_fill at the frame's exact box).

Usage: python fit_image.py <in.png> <WIDTHxHEIGHT> <out.png> [--top]
  --top keeps the top of a tall screenshot (phone screens); the default keeps the centre.
Needs Pillow: pip install pillow
"""
import argparse
import sys

from PIL import Image


def fit(src: Image.Image, width: int, height: int, top: bool) -> Image.Image:
    target = width / height
    w, h = src.size
    if w / h > target:            # too wide: trim the sides
        new_w = round(h * target)
        left = (w - new_w) // 2
        box = (left, 0, left + new_w, h)
    else:                         # too tall: trim top/bottom (or only the bottom with --top)
        new_h = round(w / target)
        upper = 0 if top else (h - new_h) // 2
        box = (0, upper, w, upper + new_h)
    return src.crop(box).resize((width * 2, height * 2), Image.LANCZOS)   # 2x for a sharp slide


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("src")
    ap.add_argument("size", help="frame size in slide px, e.g. 330x560")
    ap.add_argument("out")
    ap.add_argument("--top", action="store_true")
    a = ap.parse_args(argv)
    try:
        width, height = (int(x) for x in a.size.lower().split("x"))
    except ValueError:
        ap.error("size must look like 330x560")
    fit(Image.open(a.src).convert("RGB"), width, height, a.top).save(a.out)
    print(f"{a.out}: {a.size} (saved at 2x)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
