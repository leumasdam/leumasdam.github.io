"""Turn the white-on-orange brand logo into a clean transparent PNG.

Source: assets/logo-orange.png  (white logo on solid orange #ED3F22)
Output: assets/logo.png         (white logo, transparent background, trimmed)

The logo is pure white on a solid orange field, so per-pixel alpha can be
derived from how far each pixel sits from orange toward white. The green
channel is the cleanest discriminator (orange G≈63, white G≈255).
"""
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "logo-orange.png"
OUT = ROOT / "assets" / "logo.png"

ORANGE_G = 63
WHITE_G = 255


def main() -> None:
    src = Image.open(SRC).convert("RGB")
    w, h = src.size
    out = Image.new("RGBA", (w, h), (255, 255, 255, 0))
    src_px = src.load()
    out_px = out.load()

    span = WHITE_G - ORANGE_G
    for y in range(h):
        for x in range(w):
            _, g, _ = src_px[x, y]
            alpha = (g - ORANGE_G) / span
            alpha = 0.0 if alpha < 0 else 1.0 if alpha > 1 else alpha
            # Floor near-orange noise to fully transparent so getbbox() trims.
            if alpha < 0.12:
                alpha = 0.0
            out_px[x, y] = (255, 255, 255, int(alpha * 255))

    # Trim to the logo's bounding box.
    bbox = out.getbbox()
    if bbox:
        pad = 12
        x0, y0, x1, y1 = bbox
        x0 = max(0, x0 - pad); y0 = max(0, y0 - pad)
        x1 = min(w, x1 + pad); y1 = min(h, y1 + pad)
        out = out.crop((x0, y0, x1, y1))

    out.save(OUT, "PNG")
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes, {out.size[0]}x{out.size[1]})")


if __name__ == "__main__":
    main()
