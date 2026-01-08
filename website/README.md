# Renuka Gruh Udyog — Static Website

Open `index.html` in a browser to view the site locally. This is a lightweight static product showcase with WhatsApp ordering links.

Quick start (Windows):

```powershell
start "" "index.html"
```

Next steps:
- Add real product images into `website/images/` and update the `img` placeholders
	- Recommended filenames:
		- `idli.jpg` (Idli photo you uploaded)
		- `amla.jpg` or `amla.png` (Amla Candy)
		- `step1.jpg` ... `step5.jpg` (preparation step photos)
  
Image optimization (optional):

1. Install Pillow:

```powershell
python -m pip install pillow
```

2. Run the optimizer (creates `website/images/optimized/`):

```powershell
python scripts/optimize_images.py
```

The script generates resized JPEG and WebP variants (e.g. `idli-800.jpg`, `idli-800.webp`). Use these in pages for faster loading.

Automatically wire optimized files into pages:

1. After running `scripts/optimize_images.py`, run:

```powershell
python scripts/wire_optimized_images.py
```

2. The script will update `*.html` files in the `website/` folder, replacing matching `<img src="images/<name>...">` tags with a `<picture>` element that prefers WebP and falls back to JPEG.

Notes:
- The optimizer writes to `website/images/optimized/`.
- Keep backups if you want to review HTML changes before committing.
- Localize Marathi text where needed
- Optionally host on GitHub Pages or Netlify
