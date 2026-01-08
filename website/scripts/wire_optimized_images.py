#!/usr/bin/env python3
"""
Wire optimized images into HTML pages.

This script looks in `website/images/optimized/` for files named like
`idli-800.webp` and `idli-800.jpg`, then replaces occurrences of
`images/idli.jpg` or `images/idli.png` (and svg fallbacks) in HTML files
with a `<picture>` element that prefers WebP and falls back to JPEG.

Usage:
  python scripts/wire_optimized_images.py

It edits HTML files in-place; keep backups if desired.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
IMG_DIR = ROOT / 'images' / 'optimized'
HTML_DIR = ROOT

if not IMG_DIR.exists():
    print("No optimized images folder found at", IMG_DIR)
    raise SystemExit(1)


def collect_variants():
    # map base -> dict{width: {ext: path}}
    variants = {}
    for p in IMG_DIR.iterdir():
        if not p.is_file():
            continue
        m = re.match(
            r'(?P<name>.+)-(?P<w>\d+)\.(?P<ext>webp|jpe?g|png)$', p.name, re.I)
        if not m:
            continue
        name = m.group('name')
        w = int(m.group('w'))
        ext = m.group('ext').lower()
        variants.setdefault(name, {}).setdefault(w, {})[ext] = p
    return variants


def make_picture_html(name, data):
    # choose largest width available
    widths = sorted(data.keys(), reverse=True)
    chosen = widths[0]
    files = data[chosen]
    webp = files.get('webp')
    jpg = files.get('jpg') or files.get('jpeg')
    png = files.get('png')
    # relative paths from HTML -> images/optimized
    rel_webp = f"images/optimized/{webp.name}" if webp else None
    rel_jpg = f"images/optimized/{jpg.name}" if jpg else None
    rel_png = f"images/optimized/{png.name}" if png else None

    sources = []
    if rel_webp:
        sources.append(f'<source type="image/webp" srcset="{rel_webp}">')
    if rel_jpg:
        sources.append(f'<source type="image/jpeg" srcset="{rel_jpg}">')
    if rel_png:
        sources.append(f'<source type="image/png" srcset="{rel_png}">')

    # fallback img uses jpg or png or webp
    fallback = rel_jpg or rel_png or rel_webp or ''
    pic = '<picture>' + \
        ''.join(
            sources) + f'<img src="{fallback}" loading="lazy" alt="{name}">' + '</picture>'
    return pic


def replace_in_file(path, variants):
    text = path.read_text(encoding='utf-8')
    changed = False
    for name in variants:
        # match images/name.(jpg|png|svg|jpeg) or images/name-*.jpg
        pattern = re.compile(
            rf'(<img[^>]+src=["\'])(?:\.\./)?images/(?:{re.escape(name)}(?:-[0-9]+)?\.[a-zA-Z0-9]+|{re.escape(name)}\.[a-zA-Z0-9]+)(["\'][^>]*>)', re.I)

        def repl(m):
            before = m.group(1)
            after = m.group(2)
            pic = make_picture_html(name, variants[name])
            nonlocal changed
            changed = True
            return pic
        text, n = pattern.subn(repl, text)
    if changed:
        path.write_text(text, encoding='utf-8')
        print('Updated', path)


def main():
    variants = collect_variants()
    if not variants:
        print('No optimized variants found in', IMG_DIR)
        return
    html_files = list(HTML_DIR.glob('*.html'))
    for hf in html_files:
        replace_in_file(hf, variants)


if __name__ == '__main__':
    main()
