"""Generate NxA brand book pages 01-14 as SVGs (same content as the Figma file).

Run build_pages.py first; this reuses its helpers and writes into pages/.
"""
from build_pages import (
    BLUSH, BONE, H, INK, ROSE, SAND, STONE, TAN35, W, chrome, header, logo, page, rect, text, xmark, P_N, P_X, P_A,
)

# 01 — Cover
b = logo((W - 1100) / 2, 330, 1100, BONE, ROSE)
b += text(W / 2, 640, "the look of a suit, made by hand.", "serif_m", BONE, 0.8, anchor="middle")
b += text(96, H - 100, "Brand Identity Book — v1.0", "caps", BONE, 0.6)
b += text(W - 96, H - 100, "Navid × Ava  ·  Dubai  ·  2026", "caps", BONE, 0.6, anchor="end")
page(-1, "Cover", INK, b)

# 02 — Contents
sections = [
    "Our story", "The big idea", "Mission, vision, values", "Positioning", "Audience", "Personality",
    "Voice & tone", "The logo", "Construction — the 35° line", "Logo variations", "Clear space & size",
    "Logo misuse", "Colour", "Alternative palettes", "Typography", "Type system", "Pattern", "Colour moods",
    "Photography", "Film & Reels", "Graphic devices", "Instagram profile", "Instagram grid", "Post templates",
    "Story & highlight covers", "Stationery", "Rules & AI policy",
]
b = chrome("00", "Contents") + text(96, 160, "Contents", "display")
half = (len(sections) + 1) // 2
for i, name in enumerate(sections):
    x = 96 + (i // half) * 880
    y = 340 + (i % half) * 50
    b += text(x, y, f"{i + 1:02d}", "caps", ROSE) + text(x + 60, y - 6, name, "body_l") + rect(x, y + 38, 780, 1, INK, 0.15)
page(0, "Contents", BONE, b)

# 03 — Our story
b = header(1, "Our story", "Navid × Ava.", size=80)
b += text(96, 310, "Partners in life. Partners in frame.", "serif_m")
b += text(96, 390, (
    "NxA is a creative studio in Dubai run by two artists.\n"
    "Navid is a photographer and art director who sees\n"
    "in light, lines and space. Ava is a filmmaker,\n"
    "storyteller, cook and stylist who sees in people,\n"
    "flavour and feeling.\n\n"
    "Together we make places, products and brands look\n"
    "the way they deserve to look — on camera, by hand,\n"
    "with no shortcuts."), "body_l", INK, 0.85)
b += rect(980, 180, 400, 560, SAND) + rect(1424, 180, 400, 560, BLUSH)
b += text(1004, 690, "Portrait — Navid\n(behind the camera)", "caps", INK, 0.5)
b += text(1448, 690, "Portrait — Ava\n(in front of it)", "caps", INK, 0.5)
b += xmark(1354, 432, 96)
b += text(980, 780, "Navid — the eye", "h2") + text(980, 830, "Photographer & art director. Space,\narchitecture, light. Calm, precise,\nbehind the camera.", "body_m", INK, 0.75)
b += text(1424, 780, "Ava — the voice", "h2") + text(1424, 830, "Filmmaker, storyteller, cook & stylist.\nFood, people, story. Energetic, warm,\nin front of the camera.", "body_m", INK, 0.75)
page(1, "Our story", BONE, b)

# 04 — The big idea
b = chrome(2, "The big idea", True) + text(96, 200, "02 — The big idea", "caps", ROSE)
b += text(96, 260, "From t-shirt", "display", BONE, size=160)
b += text(96, 430, "to suit.", "serif_l", ROSE, size=150)
b += text(96, 680, (
    "Most small businesses show up online in a t-shirt and a hoodie. The big brands hire agencies a small\n"
    "business can’t afford. NxA puts every client in a well-cut suit: tailored content, made by hand and\n"
    "camera, at a price a small business can pay."), "body_l", BONE, 0.85)
b += text(96, 830, "Everything in this book serves that one idea.", "serif_m", BONE, 0.6)
page(2, "The big idea", INK, b)

# 05 — Mission, vision, values
b = chrome(3, "Mission, vision, values")
b += text(96, 180, "Mission", "caps", ROSE) + text(96, 220, "Make Dubai’s independent\nplaces look as good as\nthey really are.", "h1")
b += text(1000, 180, "Vision", "caps", ROSE) + text(1000, 220, "The studio Dubai’s best small\nbrands name when someone\nasks: “who shot this?”", "h1")
b += rect(96, 520, W - 192, 1, INK, 0.2) + text(96, 570, "Values", "caps", ROSE)
vals = [
    ("Made by hand", "Real people, real cameras, real\nlight. No AI faces, no AI voices."),
    ("Tailored, not templated", "Every client gets their own cut.\nNo copy-paste looks."),
    ("Affordable luxury", "Omega — not Patek Philippe, not\nSwatch. Premium a small business\ncan own."),
    ("Two eyes, one frame", "Space and story, always shot\ntogether. Navid’s frame, Ava’s\nfeeling."),
]
for k, (t, d) in enumerate(vals):
    x = 96 + k * 444
    b += text(x, 630, f"0{k + 1}", "serif_m", ROSE) + text(x, 690, t, "h2", size=28) + text(x, 740, d, "body_m", INK, 0.75)
page(3, "Mission, vision, values", BONE, b)

# 06 — Positioning
b = header(4, "Positioning", "Where\nwe stand.")
b += text(96, 420, (
    "For independent restaurants, cafés, boutique\n"
    "hotels and design brands in Dubai that want to\n"
    "look world-class, NxA is the two-artist studio\n"
    "that tailors space, food and story into one look —\n"
    "at a price a small business can pay.\n\n"
    "Unlike volume agencies, you always know who\n"
    "is behind the camera."), "body_l", INK, 0.85)
b += text(96, 820, "Not Patek. Not Swatch. Omega.", "serif_m", ROSE)
mx, my, ms = 1000, 170, 800
b += rect(mx, my, ms, ms, BONE, rx=4) + rect(mx + ms / 2, my + 40, 1, ms - 80, INK, 0.25) + rect(mx + 40, my + ms / 2, ms - 80, 1, INK, 0.25)
b += text(mx + ms - 50, my + ms / 2 + 14, "Craft-led →", "caps", INK, 0.55, anchor="end") + text(mx + 50, my + ms / 2 + 14, "← Volume-led", "caps", INK, 0.55)
b += text(mx + ms / 2 + 14, my + 50, "↑ Named artists", "caps", INK, 0.55) + text(mx + ms / 2 + 14, my + ms - 70, "↓ Faceless", "caps", INK, 0.55)
for x, y, label, big in [(170, 600, "Big F&B agencies", False), (130, 180, "DIY / freelancers", False), (560, 500, "Solo specialists", False), (620, 180, "NxA", True)]:
    r = 22 if big else 12
    b += f'<circle cx="{mx + x}" cy="{my + y}" r="{r}" fill="{ROSE if big else STONE}"/>'
    b += text(mx + x + r + 14, my + y - (20 if big else 14), label, "h2" if big else "body_m")
page(4, "Positioning", SAND, b)

# 07 — Audience
b = header(5, "Audience", "Who we dress.")
cards = [
    (96, SAND, "Lead segment · months 1–3", "Hospitality owners", (
        "Independent restaurants, cafés, boutique hotels and\nconcept stores in Dubai, under 50 staff.\n\n"
        "They want to look as good as the big names and win\nbookings — without a big-agency bill.\n\n"
        "They decide fast, by look and by trust. Instagram first.\n\n"
        "Before → after: t-shirt content → a tailored look that\nmatches the real quality of the place.")),
    (1004, BLUSH, "Secondary segment", "Design & lifestyle brands", (
        "Interior studios, furniture and design brands, developer\nshow units, fashion and lifestyle labels.\n\n"
        "They care about space, material and craft — Navid’s\nhome ground.\n\n"
        "Followers include creatives; buyers are owners.\nImpress the first, convert the second.")),
]
for x, bg, tag, title, body in cards:
    b += rect(x, 360, 820, 480, bg, rx=4) + text(x + 40, 400, tag, "caps", ROSE) + text(x + 40, 436, title, "h2") + text(x + 40, 500, body, "body_m", INK, 0.8)
b += text(96, 880, "The bar we aim for (not the price list)", "caps", INK, 0.55)
b += text(96, 920, "Atlantis The Royal  ·  Ariana’s Persian Kitchen  ·  Studio Nada Debs  ·  Omniyat  ·  The Lana", "serif_m")
page(5, "Audience", BONE, b)

# 08 — Personality
b = header(6, "Personality", "Calm ×\nenergetic.", dark=True)
b += text(96, 420, (
    "Navid is the calm. Ava is the energy. NxA lives\n"
    "in the tension between them: futuristic and\n"
    "minimal on the surface, warm and playful\n"
    "underneath. Serious in the meeting, playful\n"
    "in the studio."), "body_l", BONE, 0.85)
b += text(96, 720, "If NxA were…", "caps", BONE, 0.55)
b += text(96, 760, "a painter — David Hockney\na couple — David & Victoria Beckham\na voice — Adele", "serif_m", BONE)
for k, (a, z, v) in enumerate([("Luxury", "Affordable", 0.5), ("Serious", "Playful", 0.5), ("Minimal", "Bold", 0.3), ("Expert", "Friend", 0.8), ("Traditional", "Futuristic", 0.95), ("Calm", "Energetic", 0.5)]):
    y, x, w = 230 + k * 130, 1000, 820
    b += text(x, y, a, "caps", BONE, 0.7) + text(x + w, y, z, "caps", BONE, 0.7, anchor="end") + rect(x, y + 44, w, 2, BONE, 0.25)
    b += f'<circle cx="{x + v * w}" cy="{y + 45}" r="14" fill="{ROSE}"/>'
page(6, "Personality", INK, b)

# 09 — Voice & tone
b = header(7, "Voice & tone", "How we\nsound.")
b += text(96, 420, "Ava speaks. Navid frames. We write like a friend with\nimpeccable taste: short lines, real process, no hype.", "body_l", INK, 0.85)
for k, (a, z) in enumerate([("a friend with taste", "a sales deck"), ("confident — we show the work", "boastful"), ("futuristic & minimal", "cold"), ("playful in the studio", "careless with clients")]):
    y = 600 + k * 76
    b += text(96, y, f"We sound like {a}", "body_l") + text(856, y + 2, f"never {z}", "serif_m", ROSE, anchor="end", size=28) + rect(96, y + 56, 760, 1, INK, 0.15)
b += text(1000, 170, "Words we use", "caps", ROSE) + text(1000, 206, "tailored · frame · light · texture · table ·\nspace · story · hand-made · the suit", "h2", size=30)
b += text(1000, 330, "Words we ban", "caps", ROSE) + text(1000, 366, "elevate · next level · game-changer · unlock ·\npremium quality content · in today’s fast-paced\nworld · fake urgency", "body_l", INK, 0.6)
b += text(1000, 520, "Sample caption", "caps", ROSE) + rect(1000, 556, 824, 230, SAND)
b += text(1032, 588, "Same café. Same table. Same coffee.\nWe just changed the light, the angle and the story.\nThis is what a suit looks like on a small business. ×", "body_l")
b += text(1032, 730, "Emoji: one, max. Hashtags: 3–5 topic tags, never a block.", "body_m", INK, 0.6)
page(7, "Voice & tone", BONE, b)

# 10 — The logo
b = chrome(8, "The logo") + logo((W - 1300) / 2, 300, 1300)
b += text(96, 760, "08 — The logo", "caps", ROSE)
b += text(96, 800, "N for Navid. A for Ava. × for what happens when they work together.", "h2")
b += text(96, 860, "One wordmark, drawn from a single stroke family. The letters stay quiet in Ink; the × carries the colour.\nNever redraw, retype or rearrange it — always use the master files.", "body_m", INK, 0.75)
page(8, "The logo", BONE, b)

# 11 — Construction
sc, lx, ly = 1400 / 133.6, 260, 380
b = chrome(9, "Construction — the 35° line") + text(96, 170, "09 — Construction", "caps", ROSE) + text(96, 206, "Every stroke runs at 35°.", "h1")
b += logo(lx, ly, 1400, INK, INK)
b += (
    f'<g transform="translate({lx} {ly}) scale({sc:.4f})">'
    f'<g stroke="{ROSE}" stroke-width="0.16" fill="none"><line x1="-10" y1="-5.21" x2="55" y2="40.05"/>'
    f'<line x1="80" y1="-2.71" x2="145" y2="42.55"/><line x1="45" y1="27.21" x2="85" y2="-0.64"/></g>'
    f'<g stroke="{INK}" stroke-opacity="0.35" stroke-width="0.08" stroke-dasharray="0.8 0.8" fill="none">'
    f'<line x1="-18" y1="0" x2="152" y2="0"/><line x1="-18" y1="30.215" x2="152" y2="30.215"/>'
    f'<line x1="-18" y1="7.252" x2="152" y2="7.252"/><line x1="-18" y1="22.963" x2="152" y2="22.963"/></g></g>'
)
for k, (big, note) in enumerate([("35°", "One angle for every diagonal — N, ×, A.\nIt is the brand’s signature line."), ("1 unit", "Cap height of N and A."), ("½ unit", "Height of the ×. It sits on the optical\ncentre, between the letters.")]):
    b += text(96 + k * 600, 800, big, "serif_l", ROSE) + text(96 + k * 600, 890, note, "body_m", INK, 0.8)
page(9, "Construction", SAND, b)

# 12 — Logo variations
tw, th = 560, 340
b = chrome(10, "Logo variations") + text(96, 150, "10 — Logo variations", "caps", ROSE)
tiles = [
    ("Primary — on Bone or Sand", BONE, INK, ROSE, False), ("Reversed — on Ink", INK, BONE, ROSE, False),
    ("On Rose — for statements", ROSE, BONE, INK, False), ("Mono Ink — print, stamps, emboss", SAND, INK, INK, False),
    ("Mono Bone — over dark photos", STONE, BONE, BONE, False), ("The × — avatar, favicon, sign-off", INK, None, ROSE, True),
]
for k, (label, bg, letters, mark, only_x) in enumerate(tiles):
    x, y = 96 + (k % 3) * (tw + 24), 200 + (k // 3) * (th + 80)
    b += rect(x, y, tw, th, bg, stroke=INK if bg == BONE else None)
    b += xmark(x + (tw - 200) / 2, y + (th - 110) / 2, 200, mark) if only_x else logo(x + 80, y + (th - 90.7) / 2, 400, letters, mark)
    b += text(x, y + th + 18, label, "caps", INK, 0.7)
page(10, "Logo variations", BONE, b)

# 13 — Clear space & size
s2 = 900 / 133.6
u = 15.711 * s2
bx, by = 170, 300
bh = 30.215 * s2 + 2 * u
b = chrome(11, "Clear space & size")
b += rect(bx, by, 900 + 2 * u, bh, BLUSH, 0.6) + f'<rect x="{bx}" y="{by}" width="{900 + 2 * u:.1f}" height="{bh:.1f}" fill="none" stroke="{ROSE}" stroke-width="2" stroke-dasharray="8 8"/>'
b += logo(bx + u, by + u, 900)
for cx, cy in [(bx, by), (bx + 900 + u, by), (bx, by + bh - u), (bx + 900 + u, by + bh - u)]:
    b += xmark(cx, cy + u * 0.225, u)
b += text(170, 770, "11 — Clear space & size", "caps", ROSE) + text(170, 810, "Give it room: clear space on every side = the height of the ×.", "h2")
b += text(170, 870, "Nothing — text, edges, other logos — enters the pink zone.", "body_m", INK, 0.75)
b += text(1400, 300, "Minimum size", "caps", ROSE) + text(1400, 340, "Wordmark\n120 px digital · 30 mm print", "body_l")
b += text(1400, 440, "Below that, or in a circle,\nuse the × alone.", "body_m", INK, 0.75)
b += f'<circle cx="1510" cy="670" r="110" fill="{INK}"/>' + xmark(1435, 628, 150) + text(1400, 800, "Instagram avatar ✓", "caps", INK, 0.7)
b += f'<circle cx="1755" cy="670" r="55" fill="{INK}"/>' + logo(1710, 660, 90, BONE, ROSE) + text(1660, 800, "Wordmark in a circle ✕", "caps", ROSE)
page(11, "Clear space & size", BONE, b)

# 14 — Logo misuse
b = chrome(12, "Logo misuse") + text(96, 150, "12 — Never do this", "caps", ROSE)
mis = ["Don’t stretch or squash", "Don’t recolour the ×", "Don’t add shadows or effects", "Don’t rotate", "Don’t use Primary on Rose", "Don’t retype it in a font"]
for k, label in enumerate(mis):
    x, y = 96 + (k % 3) * (tw + 24), 200 + (k // 3) * (th + 80)
    b += rect(x, y, tw, th, ROSE if k == 4 else SAND)
    if k == 0:
        b += f'<g transform="translate({x + 50} {y + 140}) scale({460 / 133.6:.3f} {60 / 30.215:.3f})"><path d="{P_N}" fill="{INK}"/><path d="{P_X}" fill="{ROSE}"/><path d="{P_A}" fill="{INK}"/></g>'
    elif k == 1:
        b += logo(x + 80, y + 125, 400, INK, "#1A66F2")
    elif k == 2:
        b += logo(x + 90, y + 137, 400, "#000000", "#000000").replace("<g ", '<g fill-opacity="0.3" ', 1) + logo(x + 80, y + 125, 400)
    elif k == 3:
        b += f'<g transform="rotate(14 {x + tw / 2} {y + th / 2})">{logo(x + 80, y + 125, 400)}</g>'
    elif k == 4:
        b += logo(x + 80, y + 125, 400)
    else:
        b += text(x + tw / 2, y + 120, "NXA", "display", anchor="middle", caps=False)
    b += text(x, y + th + 18, "✕  " + label, "caps", ROSE)
page(12, "Logo misuse", BONE, b)

print("front pages written")
