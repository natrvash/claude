"""Write the NxA logo pack as SVGs into exports/logo-pack/svg."""
from pathlib import Path
from build_pages import BONE, INK, ROSE, P_N, P_X, P_A

OUT = Path(__file__).parent / "exports" / "logo-pack" / "svg"
OUT.mkdir(parents=True, exist_ok=True)

def wordmark(letters, mark, bg=None, pad=0):
    w, h = 133.6 + 2 * pad, 30.3 + 2 * pad
    back = f'<rect x="{-pad}" y="{-pad}" width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w * 20:.0f}" height="{h * 20:.0f}" viewBox="{-pad} {-pad} {w} {h}">'
            f'{back}<path d="{P_N}" fill="{letters}"/><path d="{P_X}" fill="{mark}"/><path d="{P_A}" fill="{letters}"/></svg>')

def mark_only(fill, bg=None, circle=False):
    # 600x600 canvas, × centred
    s = 360 / 28.507
    back = ""
    if bg:
        back = f'<circle cx="300" cy="300" r="300" fill="{bg}"/>' if circle else f'<rect width="600" height="600" fill="{bg}"/>'
    y = 300 - 15.711 * s / 2
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="600" height="600" viewBox="0 0 600 600">{back}'
            f'<g transform="translate(120 {y:.2f}) scale({s:.4f}) translate(-51.102 -7.252)"><path d="{P_X}" fill="{fill}"/></g></svg>')

files = {
    "NxA-logo-primary": wordmark(INK, ROSE),
    "NxA-logo-reversed": wordmark(BONE, ROSE),
    "NxA-logo-on-rose": wordmark(BONE, INK),
    "NxA-logo-mono-ink": wordmark(INK, INK),
    "NxA-logo-mono-porcelain": wordmark(BONE, BONE),
    "NxA-logo-primary-on-porcelain": wordmark(INK, ROSE, BONE, 16),
    "NxA-logo-reversed-on-ink": wordmark(BONE, ROSE, INK, 16),
    "NxA-logo-on-rose-background": wordmark(BONE, INK, ROSE, 16),
    "NxA-mark-rose": mark_only(ROSE),
    "NxA-mark-ink": mark_only(INK),
    "NxA-mark-porcelain": mark_only(BONE),
    "NxA-instagram-avatar": mark_only(ROSE, INK, circle=False),
}
for name, svg in files.items():
    (OUT / f"{name}.svg").write_text(svg, encoding="utf-8")
print(len(files))
