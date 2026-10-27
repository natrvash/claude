"""Compare alternative light neutrals to replace Bone + Dubai Sand."""
from pathlib import Path
from build_pages import INK, ROSE, STONE, BLUSH, svg_doc, logo, rect, text, xmark

OPTIONS = [
    ("Current", "Bone + Dubai Sand", "#F6F2EC", "#E6DCCD", "#8A8279", "Warm cream. Reads close to Claude’s own colours."),
    ("A · Porcelain", "Porcelain + Concrete", "#F4F4F2", "#D6D6D1", "#85857F", "Neutral gallery white. Most futuristic; Rose pops hardest."),
    ("B · Pearl", "Pearl + Mauve Stone", "#F5EFF1", "#DCCBD1", "#8A7F84", "White with a breath of rose. Own-able, ties to the ×."),
    ("C · Pistachio Cream", "Mist + Sage", "#F0F2EC", "#CDD3C3", "#858A7C", "Green is magenta’s opposite: fresh, Persian, food-friendly."),
    ("D · Chrome", "Cloud + Titanium", "#EEF0F3", "#C9CDD4", "#7D838D", "Cool silver-blue. Tech, night, architecture."),
]
W, H = 2028, 110 + 3 * 540
cw, ch = 900, 500
b = text(96, 40, "Light neutrals — options to replace Bone + Dubai Sand", "h2")
for i, (tag, name, light, mid, stone, note) in enumerate(OPTIONS):
    x, y = 96 + (i % 2) * (cw + 32), 110 + (i // 2) * (ch + 40)
    b += rect(x, y, cw, ch, light, stroke=INK)
    b += rect(x + 520, y + 40, 340, ch - 80, mid)
    b += logo(x + 40, y + 60, 420)
    b += text(x + 40, y + 190, tag, "caps", ROSE) + text(x + 40, y + 222, name, "h2", size=28)
    b += text(x + 40, y + 270, note, "body_m", INK, 0.8, size=15)
    for k, c in enumerate([light, mid, INK, ROSE, stone, BLUSH]):
        b += rect(x + 40 + k * 70, y + 330, 60, 60, c, stroke=INK)
    b += text(x + 40, y + 400, f"{light} · {mid} · grey {stone}", "caps", INK, 0.6, size=12)
    b += rect(x + 40, y + 430, 200, 40, INK, rx=20) + text(x + 140, y + 441, "Book a shoot", "caps", light, anchor="middle", size=12)
    b += text(x + 550, y + 70, "Same place.\nNew scene.", "serif_m", INK, size=40)
    b += xmark(x + 790, y + ch - 90, 44)
out = Path(__file__).parent / "exports" / "NxA-neutral-options.svg"
out.write_text(svg_doc(W, H, "#FFFFFF", b), encoding="utf-8")
print(out, W, H)
