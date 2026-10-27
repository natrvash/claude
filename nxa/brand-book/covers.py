"""Write the 4 Instagram highlight covers (1080x1920) as SVGs for rendering."""
from pathlib import Path
from build_pages import BONE, INK, ROSE, SAND, icon, svg_doc

OUT = Path(__file__).parent.parent / "instagram" / "highlight-covers"
COVERS = [
    ("1-Mise-en-scene", SAND, "Before/After", INK),
    ("2-Behind", INK, "Studio", BONE),
    ("3-Us", INK, "×", ROSE),
    ("4-Book", ROSE, "Work", BONE),
]
for name, bg, kind, fg in COVERS:
    body = icon(kind, 540, 960, 300, fg)
    (OUT / f"{name}.svg").write_text(svg_doc(1080, 1920, bg, body, name), encoding="utf-8")
print("ok")
