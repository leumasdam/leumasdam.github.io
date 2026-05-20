"""Turn the orange-on-white brand logo into a clean transparent PNG.

Source: assets/logo-orange-src.png  (orange logo on a solid white background)
Output: assets/logo.png             (orange logo, transparent background, trimmed)

The logo is a solid brand orange on white, so per-pixel alpha is derived from
how far each pixel sits from white toward orange. The green channel is the
cleanest discriminator (white G≈255, orange G≈63).
"""
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "logo-orange-src.png"
OUT = ROOT / "assets" / "logo.png"

BRAND = (237, 63, 34)  # #ED3F22
WHITE_G = 255
ORANGE_G = 63


def main() -> None:
    src = Image.open(SRC).convert("RGB")
    w, h = src.size
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    src_px = src.load()
    out_px = out.load()

    span = WHITE_G - ORANGE_G
    for y in range(h):
        for x in range(w):
            _, g, _ = src_px[x, y]
            alpha = (WHITE_G - g) / span
            alpha = 0.0 if alpha < 0 else 1.0 if alpha > 1 else alpha
            if alpha < 0.12:  # floor near-white noise so getbbox() trims
                alpha = 0.0
            out_px[x, y] = (*BRAND, int(alpha * 255))

    bbox = out.getbbox()
    if bbox:
        pad = 14
        x0, y0, x1, y1 = bbox
        out = out.crop((
            max(0, x0 - pad), max(0, y0 - pad),
            min(w, x1 + pad), min(h, y1 + pad),
        ))

    out.save(OUT, "PNG")
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes, {out.size[0]}x{out.size[1]})")


if __name__ == "__main__":
    main()
