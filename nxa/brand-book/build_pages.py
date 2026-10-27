"""Generate NxA brand book pages 15-29 as editable 1920x1080 SVGs.

Pages 01-14 live in the Figma file. Drag these SVGs into the same Figma
file to continue the book: text stays editable and fonts resolve to the
brand's Google Fonts (Syne, Instrument Serif, Manrope).
Also writes large pattern swatches to patterns/.
"""
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).parent
OUT = ROOT / "pages"
W, H = 1920, 1080
TAN35 = 0.7002

INK, BONE, SAND, STONE, ROSE, BLUSH = "#111111", "#F6F2EC", "#E6DCCD", "#8A8279", "#D62271", "#F4D6E2"

ALT_PALETTES = [
    ("Night Majlis", "Restaurants after dark, events, launches",
     [("Ink", INK), ("Aubergine", "#2B1A24"), ("Damask Rose", ROSE), ("Brass", "#B08D57"), ("Smoke", "#3A3633")]),
    ("Saffron & Pistachio", "Persian food, Ava’s kitchen, warm F&B",
     [("Saffron", "#E3A33B"), ("Pistachio", "#A8B96A"), ("Pomegranate", "#9E1F3A"), ("Rosewater", "#F2D7D5"), ("Bone", BONE)]),
    ("Gallery", "Architecture, interiors, Navid’s spaces",
     [("Chalk", "#FAFAF7"), ("Concrete", "#BDB8B0"), ("Shadow Blue", "#A9B7C2"), ("Graphite", "#3B3B3B"), ("Damask Rose", ROSE)]),
    ("Desert Noon", "Hotels, exteriors, golden hour, Dubai light",
     [("Dubai Sand", SAND), ("Terracotta", "#C46A4A"), ("Date", "#5B3A29"), ("Palm", "#4F5D45"), ("Bone", BONE)]),
]

P_N = "M0.000 0.000L0.000 30.215L3.422 30.215L3.422 4.135L40.880 30.215L44.302 30.215L44.302 0.000L40.880 0.000L40.880 26.079L3.422 0.000Z"
P_X = "M63.649 11.851L60.679 13.919L51.102 7.252L57.043 7.252ZM51.102 22.963L73.668 7.252L79.609 7.252L57.043 22.963ZM67.062 18.364L70.033 16.296L79.609 22.963L73.668 22.963Z"
P_A = "M89.831 4.134L127.289 30.215L133.230 30.215L89.831 0.000L86.409 0.000L86.409 26.793L86.409 30.215L89.831 30.215L116.485 30.215L111.621 26.793L89.831 26.793Z"

# Type styles: (family, weight, style, size, letter-spacing, line-height factor)
STYLES = {
    "display": ("Syne", 800, "normal", 96, -2, 1.0),
    "h1": ("Syne", 700, "normal", 56, -1, 1.1),
    "h2": ("Syne", 700, "normal", 32, -0.5, 1.2),
    "serif_l": ("Instrument Serif", 400, "italic", 72, -1, 1.05),
    "serif_m": ("Instrument Serif", 400, "italic", 40, 0, 1.15),
    "body_l": ("Manrope", 400, "normal", 24, 0, 1.5),
    "body_m": ("Manrope", 400, "normal", 18, 0, 1.55),
    "caps": ("Manrope", 700, "normal", 14, 2.5, 1.3),
}


def text(x, y, content, style, fill=INK, opacity=1, anchor="start", size=None, caps=None, family=None, weight=None, fstyle=None):
    """Multi-line text. `y` is the top of the first line; '\n' breaks lines."""
    fam, wt, fs, fsize, ls, lh = STYLES[style]
    family, weight, fstyle, fsize = family or fam, weight or wt, fstyle or fs, size or fsize
    caps = style == "caps" if caps is None else caps
    baseline = y + fsize * 0.8
    spans = []
    for i, line in enumerate(content.split("\n")):
        line = (line.upper() if caps else line) or "\u00a0"  # empty tspans collapse
        dy = 0 if i == 0 else fsize * lh
        spans.append(f'<tspan x="{x}" dy="{dy:.1f}">{escape(line)}</tspan>')
    return (
        f'<text x="{x}" y="{baseline:.1f}" font-family="{family}" font-weight="{weight}" '
        f'font-style="{fstyle}" font-size="{fsize}" letter-spacing="{ls}" fill="{fill}" '
        f'fill-opacity="{opacity}" text-anchor="{anchor}">{"".join(spans)}</text>'
    )


def rect(x, y, w, h, fill, opacity=1, rx=0, stroke=None, dash=None):
    s = f' stroke="{stroke}" stroke-opacity="0.25" stroke-width="2"' if stroke else ""
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" fill-opacity="{opacity}"{s}{d}/>'


def logo(x, y, width, letters=INK, mark=ROSE):
    s = width / 133.6
    return (
        f'<g transform="translate({x} {y}) scale({s:.4f})">'
        f'<path d="{P_N}" fill="{letters}"/><path d="{P_X}" fill="{mark}"/><path d="{P_A}" fill="{letters}"/></g>'
    )


def xmark(x, y, width, fill=ROSE, opacity=1):
    s = width / 28.507
    return f'<g transform="translate({x} {y}) scale({s:.4f}) translate(-51.102 -7.252)" fill-opacity="{opacity}"><path d="{P_X}" fill="{fill}"/></g>'


_clip = [0]


def clipped(x, y, w, h, inner, rx=0):
    _clip[0] += 1
    cid = f"clip{_clip[0]}"
    return f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}"/></clipPath><g clip-path="url(#{cid})">{inner}</g>'


def lines35(x, y, w, h, step, color, width, both=False, opacity=1):
    """Parallel lines at the logo's 35° angle filling a box (clip separately)."""
    out = []
    rise = w * TAN35
    c = -rise
    while c < h + rise:
        out.append(f'<line x1="{x}" y1="{y + c:.1f}" x2="{x + w}" y2="{y + c + rise:.1f}"/>')
        if both:
            out.append(f'<line x1="{x}" y1="{y + c + rise:.1f}" x2="{x + w}" y2="{y + c:.1f}"/>')
        c += step
    return f'<g stroke="{color}" stroke-width="{width}" stroke-opacity="{opacity}">{"".join(out)}</g>'


def xfield(x, y, w, h, size, gap, color, accent, every=7):
    out, k = [], 0
    for row in range(int(h // gap) + 1):
        off = gap / 2 if row % 2 else 0
        for colm in range(int(w // gap) + 2):
            px, py = x + colm * gap + off - size / 2, y + row * gap
            if px > x + w:
                continue
            k += 1
            out.append(xmark(px, py, size, accent if k % every == 0 else color))
    return "".join(out)


def bands(x, y, w, h, step, color):
    """Wide 35° bands: every other strip filled."""
    out = []
    rise = w * TAN35
    c = -rise
    i = 0
    while c < h + rise:
        if i % 2 == 0:
            out.append(f'<polygon points="{x},{y + c:.1f} {x + w},{y + c + rise:.1f} {x + w},{y + c + rise + step:.1f} {x},{y + c + step:.1f}"/>')
        c += step
        i += 1
    return f'<g fill="{color}">{"".join(out)}</g>'


def chrome(num, section, dark=False):
    num = str(num).zfill(2)
    c = BONE if dark else INK
    return text(96, 64, "NxA — Brand Identity Book", "caps", c, 0.55) + text(
        W - 96, 64, f"{num}  ·  {section}", "caps", c, 0.55, anchor="end"
    )


def header(num, section, title, dark=False, size=None):
    fg = BONE if dark else INK
    num = str(num).zfill(2)
    return chrome(num, section, dark) + text(96, 150, f"{num} — {section}", "caps", ROSE) + text(96, 190, title, "display", fg, size=size)


def svg_doc(w, h, bg, body, title=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
        f'<title>{escape(title)}</title>{rect(0, 0, w, h, bg)}{body}</svg>'
    )


def page(section, name, bg, body):
    """Book page number = section + 2 (cover and contents come first)."""
    title = f"{section + 2:02d} — {name}"
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{title}.svg").write_text(svg_doc(W, H, bg, body, title), encoding="utf-8")


def icon(kind, cx, cy, r, color):
    """Minimal line icons for highlight covers."""
    sw = r * 0.08
    g = f'fill="none" stroke="{color}" stroke-width="{sw:.1f}" stroke-linecap="square"'
    s = r * 0.45
    if kind == "Work":
        d = r * 0.18
        return "".join(
            f'<path d="M{cx + sx * s} {cy + sy * s - sy * d} L{cx + sx * s} {cy + sy * s} L{cx + sx * s - sx * d} {cy + sy * s}" {g}/>'
            for sx, sy in [(-1, -1), (1, -1), (-1, 1), (1, 1)]
        )
    if kind == "Before/After":
        c, n = 0.8192 * s, 0.5736 * s  # cos/sin 35°
        return (f'<circle cx="{cx}" cy="{cy}" r="{s}" {g}/>'
                f'<path d="M{cx - c:.1f} {cy - n:.1f} A{s} {s} 0 0 0 {cx + c:.1f} {cy + n:.1f} Z" fill="{color}"/>')
    if kind == "Food":
        return f'<circle cx="{cx}" cy="{cy}" r="{s}" {g}/><circle cx="{cx}" cy="{cy}" r="{s * 0.55}" {g}/>'
    if kind == "Spaces":
        return f'<path d="M{cx - s * 0.7} {cy + s} L{cx - s * 0.7} {cy - s * 0.1} A{s * 0.7} {s * 0.7} 0 0 1 {cx + s * 0.7} {cy - s * 0.1} L{cx + s * 0.7} {cy + s}" {g}/>'
    if kind == "Studio":
        return f'<rect x="{cx - s}" y="{cy - s * 0.6}" width="{2 * s}" height="{1.3 * s}" {g}/><circle cx="{cx}" cy="{cy + s * 0.05}" r="{s * 0.38}" {g}/>'
    return xmark(cx - s * 0.9, cy - s * 0.5, s * 1.8, color)


s = 13  # first section rendered here (13 → page 15)

# 13 — Colour
swatches = [
    ("Ink", INK, "17 17 17", "Letters, text, night frames", BONE, 30),
    ("Bone", BONE, "246 242 236", "Main background, paper", INK, 45),
    ("Dubai Sand", SAND, "230 220 205", "Warm surfaces, cards", INK, 12),
    ("Stone", STONE, "138 130 121", "Secondary text, lines", BONE, 3),
    ("Damask Rose", ROSE, "214 34 113", "The ×, accents, one per frame", BONE, 8),
    ("Blush", BLUSH, "244 214 226", "Soft highlights, Ava’s side", INK, 2),
]
b = header(s, "Colour", "Quiet base. One spark.")
x = 96
for name, hexv, rgb, use, tc, _ in swatches:
    b += rect(x, 340, 272, 420, hexv, stroke=INK if hexv == BONE else None)
    b += text(x + 24, 370, name, "h2", tc)
    b += text(x + 24, 640, f"HEX {hexv}\nRGB {rgb}", "body_m", tc, 0.85)
    b += text(x, 780, use, "body_m", INK, 0.75)
    x += 272 + 20
b += text(96, 860, "Proportion", "caps", ROSE)
x = 96
for name, hexv, _, _, _, pct in [swatches[1], swatches[0]] + swatches[2:]:
    w = (W - 192) * pct / 100
    b += rect(x, 900, w, 56, hexv, stroke=INK if hexv == BONE else None)
    x += w
b += text(96, 980, "Bone 45 · Ink 30 · Sand 12 · Rose 8 · Stone 3 · Blush 2 — Rose is a spark, never a flood.", "body_m", INK, 0.75)
page(s, "Colour", BONE, b)
s += 1

# 14 — Alternative palettes
b = header(s, "Alternative palettes", "Same suit, four fabrics.", size=80)
b += text(96, 300, "Secondary palettes for client work and campaigns. The core palette always owns the NxA page; these dress the content.", "body_l", INK, 0.8)
for i, (name, use, cols) in enumerate(ALT_PALETTES):
    y = 380 + i * 160
    b += text(96, y + 20, name, "h2") + text(96, y + 66, use, "body_m", INK, 0.7)
    for j, (cn, hv) in enumerate(cols):
        x = 700 + j * 230
        b += rect(x, y, 220, 130, hv, stroke=INK if hv in (BONE, "#FAFAF7") else None)
        light = hv in (BONE, "#FAFAF7", SAND, "#F2D7D5", "#BDB8B0", "#A9B7C2", "#E3A33B", "#A8B96A")
        b += text(x + 14, y + 80, f"{cn}\n{hv}", "caps", INK if light else BONE, 0.85, size=12)
b += text(96, 1020, "Rule: the logo’s × stays Damask Rose or Ink in every palette.", "caps", ROSE)
page(s, "Alternative palettes", BONE, b)
s += 1

# 15 — Typography
b = header(s, "Typography", "Shout, whisper, speak.", size=80)
cols = [
    ("Syne ExtraBold", "Display — the shout", "Aa", "display", "Futuristic, artful, wide.\nShort headlines only."),
    ("Instrument Serif Italic", "Accent — the whisper", "Aa", "serif_l", "The suit. One line per layout,\nnext to the shout."),
    ("Manrope", "Body — the speaking voice", "Aa", "body_l", "Clean and legible. Regular\nfor reading, Bold for labels."),
]
for i, (fam, role, sample, st, note) in enumerate(cols):
    x = 96 + i * 600
    b += text(x, 300, sample, st, INK, size=200)
    b += text(x, 540, fam, "h2") + text(x, 590, role, "caps", ROSE) + text(x, 630, note, "body_m", INK, 0.75)
b += rect(96, 740, W - 192, 1, INK, 0.2)
b += text(96, 780, "From t-shirt", "display", size=88) + text(96, 880, "to suit.", "serif_l", ROSE, size=88)
b += text(1100, 790, "Display 96–160 · H1 56 · H2 32\nSerif accent 40–72 · Body 18–24\nLabels 14 caps, +18% tracking\nAll free Google Fonts.", "body_m", INK, 0.75)
page(s, "Typography", BONE, b)
s += 1

# 16 — Type system & alternatives
b = header(s, "Type system", "Rules and alternatives.", size=80)
rules = (
    "Headlines: sentence case, max 6 words, Syne.\n"
    "One serif italic line per layout — never two.\n"
    "Body: Manrope Regular, 45–75 characters a line.\n"
    "Labels: Manrope Bold caps, wide tracking.\n"
    "On Instagram (1080 px): headline 72–96,\n"
    "body 32–40, never below 28.\n"
    "Never stretch, outline or shadow type."
)
b += text(96, 330, "Rules", "caps", ROSE) + text(96, 370, rules, "body_l", INK, 0.85)
b += text(96, 780, "Arabic & Persian companions", "caps", ROSE)
b += text(96, 820, "من التيشيرت إلى البدلة", "h1", INK, family="IBM Plex Sans Arabic", weight=700, size=44)
b += text(96, 900, "از تی‌شرت تا کت‌وشلوار", "h1", INK, family="Vazirmatn", weight=700, size=44)
b += text(96, 980, "IBM Plex Sans Arabic · Vazirmatn — for bilingual posts and Persian food stories.", "body_m", INK, 0.7)
alts = [
    ("More classic", "Fraunces", 600, "normal", "Inter", "Warmer, bookish. For hotels and fine dining."),
    ("More editorial", "Playfair Display", 400, "italic", "Space Grotesk", "Magazine feel. For fashion and styling."),
    ("More futuristic", "Unbounded", 700, "normal", "Manrope", "Louder, techier. For launches and events."),
]
for i, (label, disp, wt, fs, body_font, note) in enumerate(alts):
    y = 330 + i * 230
    b += rect(1000, y, 824, 200, SAND if i != 1 else BLUSH, rx=4)
    b += text(1030, y + 24, label, "caps", ROSE)
    b += text(1030, y + 60, "From t-shirt to suit.", "h1", INK, family=disp, weight=wt, fstyle=fs, size=48)
    b += text(1030, y + 140, f"{disp} + {body_font} — {note}", "body_m", INK, 0.8, family=body_font, weight=400)
page(s, "Type system", BONE, b)
s += 1

# 17 — Pattern
b = header(s, "Pattern", "Four patterns, one angle.", size=80)
tiles = [
    ("The 35° weave", "Rose lines on Ink. Story backgrounds, end cards.", INK, lambda x, y, w, h: lines35(x, y, w, h, 28, ROSE, 3)),
    ("The lattice", "A nod to mashrabiya screens. Packaging, proposals.", SAND, lambda x, y, w, h: lines35(x, y, w, h, 46, INK, 2, both=True, opacity=0.8)),
    ("The × field", "Ink ×s, every seventh in Rose. Stickers, tissue paper.", BONE, lambda x, y, w, h: xfield(x, y, w, h, 26, 58, INK, ROSE)),
    ("The split", "Wide Bone bands on Rose. Announcements, launches.", ROSE, lambda x, y, w, h: bands(x, y, w, h, 60, BONE)),
]
for i, (name, use, bg, fn) in enumerate(tiles):
    x, y, w, h = 96 + i * 440, 330, 410, 470
    b += rect(x, y, w, h, bg, stroke=INK if bg == BONE else None) + clipped(x, y, w, h, fn(x, y, w, h))
    b += text(x, y + h + 24, name, "h2", size=26) + text(x, y + h + 64, use, "body_m", INK, 0.75, size=15)
b += text(96, 960, "Patterns dress our own surfaces — never behind client photos or food. Full-size swatches are in /patterns.", "body_m", INK, 0.75)
page(s, "Pattern", BONE, b)
for name, bg, fn in [(t[0], t[2], t[3]) for t in tiles]:
    (ROOT / "patterns").mkdir(exist_ok=True)
    (ROOT / "patterns" / f"NxA pattern — {name}.svg").write_text(
        svg_doc(2000, 2000, bg, clipped(0, 0, 2000, 2000, fn(0, 0, 2000, 2000)), name), encoding="utf-8")
s += 1

# 18 — Colour moods for covers & stories
MOODS = [
    ("Morning light", "Cafés, breakfast, daylight spaces", BONE, SAND, ROSE, INK),
    ("Golden hour", "Hotels, terraces, exteriors", SAND, "#C46A4A", "#5B3A29", INK),
    ("Night service", "Restaurants at night, events", INK, "#2B1A24", ROSE, BONE),
    ("Studio", "NxA news, launches, offers", ROSE, BLUSH, INK, BONE),
    ("Gallery", "Architecture & interiors", "#FAFAF7", "#BDB8B0", "#3B3B3B", INK),
]
b = header(s, "Colour moods", "A mood for every cover.", size=80)
for i, (name, use, base, second, accent, fg) in enumerate(MOODS):
    x, y = 96 + i * 352, 320
    # story frame 9:16
    b += rect(x, y, 300, 533, base, rx=16, stroke=INK if base in (BONE, "#FAFAF7") else None)
    b += rect(x, y + 330, 300, 203, second, rx=0) + rect(x, y + 330, 300, 6, accent)
    b += text(x + 24, y + 40, name, "h2", fg, size=28) + xmark(x + 240, y + 470, 36, accent if accent != second else fg)
    b += text(x + 24, y + 90, "Same café.\nNew suit.", "serif_m", fg, 0.9, size=30)
    # highlight cover
    b += f'<circle cx="{x + 40}" cy="{y + 600}" r="36" fill="{second}"/>' + icon("Food", x + 40, y + 600, 36, fg if second not in (SAND, BLUSH, "#BDB8B0") else INK)
    b += f'<circle cx="{x + 124}" cy="{y + 600}" r="36" fill="{base}" stroke="{INK}" stroke-opacity="0.2"/>' + icon("Spaces", x + 124, y + 600, 36, fg)
    b += text(x, y + 660, use, "body_m", INK, 0.75, size=15)
b += text(96, 1020, "Pick the mood from the content, not from the calendar. One mood per post; stories may change mood per frame.", "caps", ROSE)
page(s, "Colour moods", BONE, b)
s += 1

# 19 — Photography
b = header(s, "Photography", "Two eyes, one frame.")
tiles = [
    (SAND, "SPACE", "Symmetry, one strong line, natural light"),
    (BLUSH, "HANDS", "The making, not just the made"),
    (SAND, "TABLE", "Steam, texture, a real bite taken"),
    (BLUSH, "PEOPLE", "Staff and owners, candid, never stock"),
]
for i, (c, tag, label) in enumerate(tiles):
    x = 96 + i * 440
    b += rect(x, 340, 410, 470, c) + text(x + 20, 770, tag, "caps", INK, 0.6) + text(x, 830, label, "body_m", INK, 0.8)
b += text(96, 900, "Navid’s frame: light first, lines at 35°, calm symmetry, space to breathe.   Ava’s frame: life, hands, food in motion, warmth.", "body_m", INK, 0.85)
b += text(96, 940, "Grade: true colour, warm neutrals, soft Ink shadows. No heavy filters, no fake HDR, no AI-generated images — ever.", "body_m", INK, 0.85)
page(s, "Photography", BONE, b)
s += 1

# 20 — Film & Reels
b = header(s, "Film & Reels", "She talks.\nHe frames.", dark=True)
rules = [
    ("0–3 s", "Open on the result — the finished plate, the lit room.\nThe words on screen match the words spoken."),
    ("Ava", "On camera, talking to one person.\nWarm, quick, real. Never read off a phone."),
    ("Navid", "Behind the camera. Seen through hands,\nprocess and the final frame."),
    ("Captions", "Always burned in: Manrope Bold, Bone on Ink\nat 70%, lower third, max 2 lines."),
    ("The × wipe", "Our signature transition: a 35° diagonal\nwipe from before to after."),
    ("End card", "The × on Ink, 1 second, no music sting."),
]
for i, (k, v) in enumerate(rules):
    y = 160 + i * 140
    b += text(980, y, k, "serif_m", ROSE) + text(980, y + 54, v, "body_m", BONE, 0.8)
b += rect(96, 470, 320, 570, STONE, rx=24) + text(120, 990, "9:16 reel frame", "caps", BONE, 0.7)
b += rect(116, 880, 280, 70, INK, 0.7, 8) + text(132, 896, "Same café. New suit.", "body_m", BONE)
page(s, "Film & Reels", INK, b)
s += 1

# 21 — Graphic devices
b = header(s, "Graphic devices", "Small tools, used sparingly.", size=80)
b += rect(96, 360, 410, 410, SAND) + f'<line x1="116" y1="740" x2="486" y2="481" stroke="{ROSE}" stroke-width="6"/>'
b += text(96, 790, "The 35° line", "h2") + text(96, 836, "Dividers, wipes, crops.\nAlways at the logo’s angle.", "body_m", INK, 0.75)
b += rect(546, 360, 410, 410, INK) + xmark(631, 490, 240)
b += text(546, 790, "The × stamp", "h2") + text(546, 836, "Sign-off on posts, avatar,\nwatermark at 8% opacity.", "body_m", INK, 0.75)
b += rect(996, 360, 410, 410, SAND)
for cx, cy, dx, dy in [(1036, 400, 1, 1), (1366, 400, -1, 1), (1036, 730, 1, -1), (1366, 730, -1, -1)]:
    b += f'<path d="M{cx} {cy + 50 * dy} L{cx} {cy} L{cx + 50 * dx} {cy}" stroke="{INK}" stroke-width="4" fill="none"/>'
b += text(996, 790, "Frame corners", "h2") + text(996, 836, "Crop marks around a hero shot —\nthe photographer’s view.", "body_m", INK, 0.75)
sx, sy, sw = 1446, 360, 410
cut_l, cut_r = sy + 120, sy + 120 + sw * TAN35
b += rect(sx, sy, sw, sw, SAND)
b += f'<polygon points="{sx},{cut_l} {sx + sw},{cut_r:.1f} {sx + sw},{sy + sw} {sx},{sy + sw}" fill="{STONE}"/>'
b += f'<line x1="{sx}" y1="{cut_l}" x2="{sx + sw}" y2="{cut_r:.1f}" stroke="{ROSE}" stroke-width="6"/>'
b += text(sx + 20, sy + sw - 40, "BEFORE", "caps", BONE) + text(sx + sw - 20, sy + 24, "AFTER", "caps", INK, anchor="end")
b += text(1446, 790, "T-shirt → suit split", "h2") + text(1446, 836, "Before/after on one frame,\ncut on the 35° line.", "body_m", INK, 0.75)
page(s, "Graphic devices", BONE, b)
s += 1

# 22 — Instagram profile
b = header(s, "Instagram profile", "First 3 seconds\non the profile.", size=80)
b += text(96, 420, "Name field (searchable)", "caps", ROSE) + text(96, 456, "NxA · Dubai Content Studio", "h2")
b += text(96, 540, "Bio", "caps", ROSE)
b += text(96, 576, "Two artists. One frame. ×\nPhoto, film & styling for Dubai’s independent places.\nFrom t-shirt to suit ↓", "body_l")
b += text(96, 740, "Avatar: the Rose × on Ink.  Link: one booking link, never a link list.", "body_m", INK, 0.75)
b += text(96, 776, "Handle: @nxa.studio (to confirm — check it is free first).", "body_m", INK, 0.75)
px, py = 1180, 120
b += rect(px, py, 520, 900, INK, rx=48) + rect(px + 16, py + 16, 488, 868, BONE, rx=36)
b += f'<circle cx="{px + 100}" cy="{py + 150}" r="56" fill="{INK}"/>' + xmark(px + 66, py + 131, 68)
b += text(px + 190, py + 115, "12      340      180", "h2", size=22) + text(px + 190, py + 150, "posts   followers   following", "body_m", INK, 0.6, size=14)
b += text(px + 44, py + 230, "NxA · Dubai Content Studio", "body_m", size=16)
b += text(px + 44, py + 258, "Two artists. One frame. ×\nPhoto, film & styling for Dubai’s\nindependent places.\nFrom t-shirt to suit ↓", "body_m", INK, 0.85, size=15)
for i, h in enumerate(["Work", "Before/After", "Food", "Spaces", "Studio"]):
    cx = px + 80 + i * 92
    b += f'<circle cx="{cx}" cy="{py + 440}" r="34" fill="{[INK, SAND, BLUSH, SAND, ROSE][i]}"/>' + icon(h, cx, py + 440, 34, BONE if i in (0, 4) else INK)
    b += text(cx, py + 486, h, "body_m", INK, 0.8, anchor="middle", size=12)
for i in range(6):
    gx, gy = px + 16 + (i % 3) * 164, py + 530 + (i // 3) * 176
    b += rect(gx + 1, gy, 162, 174, [SAND, INK, BLUSH, STONE, SAND, ROSE][i])
page(s, "Instagram profile", BONE, b)
s += 1

# 23 — Instagram grid
b = header(s, "Instagram grid", "A rhythm,\nnot a puzzle.", dark=True, size=80)
b += text(96, 440, "Every 3 posts:\n1 · Before → after (the proof)\n2 · Reel with Ava (the voice)\n3 · Calm frame by Navid (the eye)\n\nRose appears in one tile per row, max.\nNo puzzle grids — each post stands alone.", "body_l", BONE, 0.85)
grid = [(SAND, "Before → after"), (STONE, "Reel · Ava"), (BONE, "Navid · space"), (BLUSH, "Reel · Ava"), (SAND, "Navid · table"), (ROSE, "Before → after"), (BONE, "Navid · light"), (SAND, "Before → after"), (STONE, "Reel · Ava")]
for i, (c, label) in enumerate(grid):
    gx, gy = 1000 + (i % 3) * 276, 140 + (i // 3) * 300
    b += rect(gx, gy, 270, 294, c) + text(gx + 16, gy + 260, label, "caps", BONE if c in (STONE, ROSE) else INK, 0.8)
page(s, "Instagram grid", INK, b)
s += 1

# 24 — Post templates
b = chrome(s, "Post templates") + text(96, 150, f"{s} — Post templates", "caps", ROSE)
tw, th = 380, 475
tx = [96, 536, 976, 1416]
b += rect(tx[0], 220, tw, th, SAND) + f'<polygon points="{tx[0]},{220 + th * 0.62} {tx[0] + tw},{220 + th * 0.62 - tw * TAN35:.1f} {tx[0] + tw},{220 + th} {tx[0]},{220 + th}" fill="{STONE}"/>'
b += f'<line x1="{tx[0]}" y1="{220 + th * 0.62}" x2="{tx[0] + tw}" y2="{220 + th * 0.62 - tw * TAN35:.1f}" stroke="{ROSE}" stroke-width="5"/>'
b += text(tx[0] + 20, 240, "AFTER", "caps") + text(tx[0] + 20, 220 + th - 40, "BEFORE", "caps", BONE)
b += rect(tx[1], 220, tw, th, INK) + text(tx[1] + 28, 260, "3 things\nthat make\na café look\nexpensive", "h1", BONE, size=44)
b += text(tx[1] + 28, 560, "(none of them cost money)", "serif_m", ROSE, size=26) + xmark(tx[1] + tw - 70, 220 + th - 50, 44)
b += rect(tx[2], 220, tw, th, BONE, stroke=INK) + text(tx[2] + 28, 300, "“Looking\nexpensive is\na decision,\nnot a budget.”", "serif_l", INK, size=48)
b += text(tx[2] + 28, 220 + th - 60, "— NxA", "caps", ROSE)
b += rect(tx[3], 220, tw, th, STONE) + rect(tx[3] + 24, 220 + th - 150, tw - 48, 110, INK, 0.75, 8)
b += text(tx[3] + 44, 220 + th - 132, "Same café.\nNew suit.", "h2", BONE, size=30)
for i, l in enumerate(["Before → after\n1080×1350", "Carousel cover\n1080×1350", "Quote / point of view\n1080×1350", "Reel cover\n1080×1920 (safe 4:5)"]):
    b += text(tx[i], 720, l, "caps", INK, 0.7)
b += text(96, 860, "Rules: one message per post · the × sign-off only, never the full logo on content · one Rose element per post.", "body_m", INK, 0.8)
page(s, "Post templates", BONE, b)
s += 1

# 25 — Story & highlight covers
b = header(s, "Story & highlight covers", "Stories that feel\nlike the studio.", size=80)
hl = [("Work", INK, BONE), ("Before/After", SAND, INK), ("Food", BLUSH, INK), ("Spaces", "#BDB8B0", INK), ("Studio", ROSE, BONE), ("Book", BONE, ROSE)]
for i, (name, bg, fg) in enumerate(hl):
    cx = 150 + i * 140
    b += f'<circle cx="{cx}" cy="{470}" r="56" fill="{bg}" stroke="{INK}" stroke-opacity="0.15"/>' + icon(name, cx, 470, 56, fg)
    b += text(cx, 545, name, "body_m", INK, 0.8, anchor="middle", size=14)
b += text(96, 610, "Highlight covers: one line icon, mood colours, no text inside the circle.", "body_m", INK, 0.75)
stories = [
    ("Question box", BLUSH, INK, "Ask Ava anything\nabout food styling ↓"),
    ("Behind the scenes", INK, BONE, "6:40 am.\nThe light is ready.\nAre you?"),
    ("Book a shoot", ROSE, BONE, "Your place deserves\na better suit.\nDM “SUIT”."),
]
for i, (name, bg, fg, line) in enumerate(stories):
    x, y = 1000 + i * 290, 280
    b += rect(x, y, 270, 480, bg, rx=14)
    b += text(x + 22, y + 32, name, "caps", fg, 0.7) + text(x + 22, y + 90, line, "serif_m", fg, size=28)
    b += rect(x + 22, y + 340, 226, 64, BONE if bg != BONE else SAND, 0.95, 32) + text(x + 135, y + 360, "Tap to reply", "body_m", INK, 0.6, anchor="middle", size=15)
    b += xmark(x + 220, y + 440, 30, fg)
b += text(1000, 800, "Stories: text in the top 60%, stickers in the safe middle,\nthe × in the corner. Change mood per frame, keep fonts fixed.", "body_m", INK, 0.75)
page(s, "Story & highlight covers", BONE, b)
s += 1

# 26 — Stationery
b = header(s, "Stationery", "Small touches, same suit.", size=80)
b += rect(96, 360, 510, 330, INK, rx=8) + logo(171, 490, 360, BONE, ROSE)
b += rect(646, 360, 510, 330, BONE, rx=8, stroke=INK) + text(686, 400, "Ava Izadpanah", "h2", size=28) + text(686, 440, "Filmmaker · Storyteller", "caps", ROSE)
b += text(686, 560, "+971 — — —\nhello@nxa.studio\n@nxa.studio · Dubai", "body_m", INK, 0.85) + xmark(1090, 400, 40)
b += text(96, 710, "Business card — 85 × 55 mm, front & back", "caps", INK, 0.7)
b += rect(1220, 360, 604, 330, SAND, rx=8)
b += text(1250, 400, "Navid Atrvash", "h2", size=26) + text(1250, 440, "Photographer & Art Director", "caps", ROSE)
b += text(1250, 480, "NxA — Navid × Ava · Dubai\nnxa.studio · @nxa.studio", "body_m", INK, 0.8) + logo(1250, 600, 180)
b += text(1220, 710, "Email signature", "caps", INK, 0.7)
b += rect(96, 780, 1728, 220, INK, rx=8) + clipped(1100, 780, 724, 220, lines35(1100, 780, 724, 220, 28, ROSE, 2, opacity=0.5), rx=8)
b += logo(140, 860, 300, BONE, ROSE)
b += text(1040, 840, "Proposal — The Lana Café", "h2", BONE, anchor="end") + text(1040, 890, "From t-shirt to suit.", "serif_m", ROSE, anchor="end")
page(s, "Stationery", BONE, b)
s += 1

# 27 — Rules & AI policy
b = header(s, "Rules & AI policy", "Real hands.\nReal cameras.")
dos = "Show the process — hands, set-ups, light\nName the people behind every shoot\nGet client approval before posting their work\nBurn captions into every video\nWrite alt text for every image\nRespect UAE content rules and guests’ privacy"
donts = "No AI faces, AI voices or cloned voices\nNo AI-generated food, spaces or people as our work\nNo fake numbers, fake urgency or fake reviews\nNo naming or mocking other agencies\nNo posting client work before they publish\nNo stock photos — ever"
b += text(96, 460, "Always", "caps", ROSE) + text(96, 500, dos, "body_l", INK, 0.85)
b += text(1000, 460, "Never", "caps", ROSE) + text(1000, 500, donts, "body_l", INK, 0.85)
b += rect(96, 860, W - 192, 1, INK, 0.2)
b += text(96, 900, "AI may help us plan, draft captions and edit. It never replaces the camera. Every portfolio image is a real shoot.", "serif_m", INK, size=32)
page(s, "Rules & AI policy", BONE, b)
s += 1

# Back cover
b = xmark((W - 300) / 2, 420, 300) + text(W / 2, 640, "hello@nxa.studio  ·  @nxa.studio  ·  Dubai", "caps", BONE, 0.7, anchor="middle")
b += text(96, H - 100, "NxA Brand Identity Book — v1.0 · 2026", "caps", BONE, 0.5)
page(s, "Back cover", INK, b)

print(sorted(p.name for p in OUT.glob("*.svg")))
