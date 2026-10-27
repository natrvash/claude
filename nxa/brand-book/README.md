# NxA Brand Identity Book

- **Pages 01–14** are in Figma: https://www.figma.com/design/kGzpC4tkbXu0qLiKvfCqBm
  (cover, contents, story, big idea, values, positioning, audience, personality, voice, logo pages).
  The file also holds the colour variables, text styles and logo components (Library page).
- **Pages 15–30** are in `pages/` as editable SVGs. Drag them into the Figma file.
  Previews are in `previews/` and `contact-sheet-pages-15-30.png`.
- **Patterns**: full-size 2000×2000 swatches are in `patterns/`.

Regenerate pages after editing `build_pages.py`:

```bash
python3 build_pages.py && node render.js
```
