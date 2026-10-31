# NxA brand intro videos

Vertical 1080×1920 loops, 30 fps. Main graphics stay inside the centred 4:5 zone (y 285–1635) so they read in the feed.

| # | Title | Background | Status |
|---|---|---|---|
| 01 | FRAME | Porcelain | v1 rendered |
| 02 | SPACE | Titanium | — |
| 03 | TABLE | Blush | — |
| 04 | LIGHT | Ink | — |
| 05 | FILM | Slate | — |
| 06 | N × A | Damask Rose | — |

## Rebuild 01
```
cd src && node rec.js && python3 sfx.py
ffmpeg -framerate 30 -i frames/f%04d.png -i sfx.wav -af loudnorm=I=-16:TP=-1.5 -c:v libx264 -crf 16 -pix_fmt yuv420p -c:a aac -b:a 256k -shortest NxA_01_FRAME.mp4
```
`anim.html` holds the timeline (`render(t)`); `rec.js` captures it with Playwright; `sfx.py` synthesises the sound.
