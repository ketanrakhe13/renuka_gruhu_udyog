#!/usr/bin/env python3
"""
Optimize images in website/images:
- resize to max widths (800, 400)
- generate WebP versions
- write outputs to website/images/optimized/

Usage:
  python -m pip install pillow
  python scripts/optimize_images.py

This script is intentionally simple and safe — it doesn't overwrite originals.
"""
from pathlib import Path
from PIL import Image

BASE = Path(__file__).resolve().parents[1] / 'images'
OUT = BASE / 'optimized'
OUT.mkdir(exist_ok=True)

SIZES = [800, 400]
EXTS = ('.jpg', '.jpeg', '.png')


def optimize(path: Path):
    name = path.stem
    try:
        img = Image.open(path)
    except Exception as e:
        print(f"skip {path}: {e}")
        return

    for w in SIZES:
        img2 = img.copy()
        # skip upscaling
        if img2.width > w:
            h = int(img2.height * (w / img2.width))
            img2 = img2.resize((w, h), Image.LANCZOS)
        out_name = OUT / f"{name}-{w}.jpg"
        img2.convert('RGB').save(
            out_name, format='JPEG', quality=85, optimize=True)
        webp_name = OUT / f"{name}-{w}.webp"
        img2.save(webp_name, format='WEBP', quality=80, method=6)
        print(f"wrote {out_name.name}, {webp_name.name}")


def main():
    paths = [p for p in BASE.iterdir() if p.suffix.lower() in EXTS]
    if not paths:
        print("No JPG/PNG images found in", BASE)
        return
    for p in paths:
        optimize(p)


if __name__ == '__main__':
    main()
