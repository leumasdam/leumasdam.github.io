"""Generate the 1200x630 social-share card (og:image) for the portfolio.

Run once to produce og-image.png in the repo root. Committed to the repo so
GitHub Pages can serve it; LinkedIn / Slack / Twitter render it on link share.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "og-image.png"

W, H = 1200, 630
BG = (15, 23, 42)        # slate-900
CARD = (30, 41, 59)      # slate-800
ACCENT = (237, 63, 34)   # brand orange #ED3F22
WHITE = (248, 250, 252)
MUTED = (148, 163, 184)  # slate-400

FONTS = "C:/Windows/Fonts"


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(f"{FONTS}/{name}", size)


def rounded(draw, box, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def main() -> None:
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Subtle dot grid
    for y in range(0, H, 32):
        for x in range(0, W, 32):
            d.ellipse([x, y, x + 2, y + 2], fill=(30, 41, 59))

    # Accent glow corner
    glow = Image.new("RGB", (W, H), BG)
    gd = ImageDraw.Draw(glow)
    gd.ellipse([W - 360, -200, W + 200, 360], fill=(74, 32, 22))
    img = Image.blend(img, glow, 0.5)
    d = ImageDraw.Draw(img)

    margin = 72

    # Status pill
    pill = "OPEN TO AI AUTOMATION ROLES — INSURANCE & CONSULTING"
    pf = font("segoeui.ttf", 20)
    pw = d.textlength(pill, font=pf)
    rounded(d, [margin, margin, margin + pw + 70, margin + 46], 23,
            outline=(51, 65, 85), width=2)
    d.ellipse([margin + 22, margin + 17, margin + 34, margin + 29], fill=ACCENT)
    d.text((margin + 48, margin + 11), pill, font=pf, fill=MUTED)

    # Headline (serif, two lines)
    hf = font("georgiab.ttf", 68)
    d.text((margin, margin + 96), "AI-assisted tools for the", font=hf, fill=WHITE)
    d.text((margin, margin + 178), "back office of ", font=hf, fill=WHITE)
    insurance_x = margin + d.textlength("back office of ", font=hf)
    d.text((insurance_x, margin + 178), "insurance.", font=hf, fill=ACCENT)

    # Subline
    sf = font("segoeui.ttf", 28)
    d.text((margin, margin + 288),
           "Three live demos: document extraction, case routing, summarization.",
           font=sf, fill=MUTED)

    # Tool chips
    chips = ["Extract", "Classify", "Summarize"]
    cf = font("segoeuib.ttf", 24)
    cx = margin
    cy = margin + 348
    for chip in chips:
        cw = d.textlength(chip, font=cf)
        rounded(d, [cx, cy, cx + cw + 48, cy + 52], 26, fill=CARD)
        d.text((cx + 24, cy + 11), chip, font=cf, fill=WHITE)
        cx += cw + 48 + 16

    # Footer: brand logo + stack
    logo_path = ROOT / "assets" / "logo.png"
    if logo_path.exists():
        logo = Image.open(logo_path).convert("RGBA")
        target_h = 46
        target_w = int(logo.width * target_h / logo.height)
        logo = logo.resize((target_w, target_h), Image.LANCZOS)
        img.paste(logo, (margin, H - margin - target_h), logo)
    else:
        d.text((margin, H - margin - 30), "Samuel", font=font("segoeuib.ttf", 26), fill=WHITE)
    stf = font("segoeui.ttf", 22)
    stack = "FastAPI · Claude Opus 4.7 · pdfplumber · Docker"
    sw = d.textlength(stack, font=stf)
    d.text((W - margin - sw, H - margin - 28), stack, font=stf, fill=MUTED)

    # Accent baseline
    d.rectangle([0, H - 8, W, H], fill=ACCENT)

    img.save(OUT, "PNG")
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes, {W}x{H})")


if __name__ == "__main__":
    main()
