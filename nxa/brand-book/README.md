# NxA Brand Identity Book

All 30 pages, ready to use:

| File | What it is |
|---|---|
| `exports/NxA-Brand-Identity-Book.pdf` | Full 30-page book, for sharing and printing |
| `exports/NxA-Brand-Identity-Book.ai` | The same book for Adobe Illustrator (PDF-compatible .ai) |
| `exports/jpg/` | Every page as a 3840×2160 JPG |
| `exports/logo-pack/` | Logo, × mark and Instagram avatar in SVG, PNG (transparent, 3000 px), JPG and PDF |
| `exports/NxA-Brand-Kit.zip` | Everything above plus SVG pages and patterns, in one download |
| `pages/` | Every page as an editable SVG (live text) — drag into Figma or open in Illustrator |
| `patterns/` | Four 2000×2000 pattern swatches |

Figma: pages 01–14 with colour variables, text styles and logo components are in
https://www.figma.com/design/kGzpC4tkbXu0qLiKvfCqBm

Rebuild after editing the content:

```bash
python3 build_front.py && python3 logos.py && node export.js
```
