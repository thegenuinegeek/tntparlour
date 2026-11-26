#!/usr/bin/env python3
"""
Process visual assets for Tooth & Nail Tattoo Parlour:
1. Extract clean outer transparency on images/logo.png and save images/logo.webp.
2. Convert hero-bg.jpg (if present) to responsive WebP (max width 1600px).
3. Regenerate a crisp 1200x630 images/og.jpg with the transparent logo.
4. Convert portfolio JPEGs to WebP alongside existing JPEGs.
"""

from collections import deque
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
IMAGES = ROOT / "images"
FONTS = ROOT / "fonts"

MATTE_RGB = (28, 27, 23)
PORTFOLIO_STEMS = [
    "work-kidbuu",
    "work-vault",
    "work-armor",
    "work-dagger",
    "work-joy",
    "work-koi",
    "work-mandala",
    "work-rose",
    "work-hibiscus",
]


def is_matte(rgb, tol=20):
    r, g, b = rgb[:3]
    mr, mg, mb = MATTE_RGB
    # Match dark neutral matte around (28, 27, 23); avoid touching warm golds or bright whites
    return (
        abs(r - mr) <= tol
        and abs(g - mg) <= tol
        and abs(b - mb) <= tol
        and max(r, g, b) < 58
    )


def make_logo_transparent():
    logo_path = IMAGES / "logo.png"
    im = Image.open(logo_path).convert("RGBA")
    w, h = im.size
    px = im.load()

    # Only run flood-fill if corners are still opaque matte
    if px[0, 0][3] == 255 and is_matte(px[0, 0], tol=24):
        visited = [[False] * h for _ in range(w)]
        bg_mask = [[False] * h for _ in range(w)]
        q = deque()

        for x in range(w):
            for y in (0, h - 1):
                if is_matte(px[x, y], tol=22):
                    visited[x][y] = True
                    bg_mask[x][y] = True
                    q.append((x, y))
        for y in range(h):
            for x in (0, w - 1):
                if not visited[x][y] and is_matte(px[x, y], tol=22):
                    visited[x][y] = True
                    bg_mask[x][y] = True
                    q.append((x, y))

        while q:
            cx, cy = q.popleft()
            for nx, ny in ((cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)):
                if 0 <= nx < w and 0 <= ny < h and not visited[nx][ny]:
                    visited[nx][ny] = True
                    if is_matte(px[nx, ny], tol=19):
                        bg_mask[nx][ny] = True
                        q.append((nx, ny))

        # Apply transparency to flood-filled exterior, plus gentle anti-aliased edge cleanup
        for x in range(w):
            for y in range(h):
                if bg_mask[x][y]:
                    px[x, y] = (0, 0, 0, 0)

        # Feather 1px fringe pixels touching transparent background if they are still near-matte dark
        for x in range(w):
            for y in range(h):
                if bg_mask[x][y]:
                    continue
                r, g, b, a = px[x, y]
                touches_bg = any(
                    0 <= nx < w and 0 <= ny < h and bg_mask[nx][ny]
                    for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1))
                )
                if touches_bg:
                    # Bright white/cream outline or gold stays solid; dark fringe blends out
                    lum = 0.299 * r + 0.587 * g + 0.114 * b
                    if lum < 55:
                        px[x, y] = (r, g, b, 0)
                    elif lum < 120:
                        new_a = int(max(0, min(255, (lum - 45) * 3.4)))
                        px[x, y] = (r, g, b, new_a)

        im.save(logo_path, "PNG", optimize=True)
        print(f"Updated transparent {logo_path.name} ({w}x{h})")
    else:
        print(f"{logo_path.name} already transparent; keeping as-is.")

    im.save(IMAGES / "logo.webp", "WEBP", quality=92, method=6)
    # Create a crisp 2.4x high-DPI hero version (960x439) for the large homepage hero lockup
    hero_w, hero_h = 960, int(round(im.height * (960 / im.width)))
    hero_logo = im.resize((hero_w, hero_h), Image.Resampling.LANCZOS)
    hero_logo = hero_logo.filter(ImageFilter.UnsharpMask(radius=1.1, percent=115, threshold=3))
    hero_logo.save(IMAGES / "logo-hero.png", "PNG", optimize=True)
    hero_logo.save(IMAGES / "logo-hero.webp", "WEBP", quality=94, method=6)
    print(f"Saved logo.webp and crisp logo-hero ({hero_w}x{hero_h})")
    return im


def load_font(candidates, size):
    for path in candidates:
        p = Path(path)
        if p.exists():
            return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()


def generate_og_image(logo_im):
    W, H = 1200, 630
    base = Image.new("RGB", (W, H), (11, 10, 9))

    # Subtle warm radial ambient glow behind center
    glow = Image.new("RGB", (W, H), (0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    for step in range(42, 0, -1):
        frac = step / 42.0
        rx = int(460 * frac)
        ry = int(230 * frac)
        intensity = (1.0 - frac) ** 2.1
        col = (int(42 * intensity), int(26 * intensity), int(8 * intensity))
        gdraw.ellipse((W // 2 - rx, 245 - ry, W // 2 + rx, 245 + ry), fill=col)
    glow = glow.filter(ImageFilter.GaussianBlur(24))
    base = Image.composite(glow, base, Image.new("L", (W, H), 255))
    # Add glow onto base cleanly
    from PIL import ImageChops
    base = ImageChops.add(Image.new("RGB", (W, H), (11, 10, 9)), glow)

    draw = ImageDraw.Draw(base)
    gold = (230, 147, 20)
    gold_dim = (130, 84, 16)
    paper = (244, 237, 224)
    muted = (184, 173, 156)

    # Outer & inner heritage rules
    draw.rectangle((28, 28, W - 29, H - 29), outline=gold_dim, width=2)
    draw.rectangle((40, 40, W - 41, H - 41), outline=(72, 52, 24), width=1)

    # Corner diamond accents
    for cx, cy in ((28, 28), (W - 29, 28), (28, H - 29), (W - 29, H - 29)):
        pts = [(cx, cy - 8), (cx + 8, cy), (cx, cy + 8), (cx - 8, cy)]
        draw.polygon(pts, fill=gold)

    # Place transparent logo cleanly
    logo_target_w = 580
    scale = logo_target_w / logo_im.width
    logo_target_h = int(logo_im.height * scale)
    resized_logo = logo_im.resize((logo_target_w, logo_target_h), Image.Resampling.LANCZOS)
    logo_x = (W - logo_target_w) // 2
    logo_y = 98
    base.paste(resized_logo, (logo_x, logo_y), resized_logo)

    # Horizontal divider rule with center diamond
    rule_y = logo_y + logo_target_h + 36
    draw.line((220, rule_y, W // 2 - 22, rule_y), fill=gold_dim, width=2)
    draw.line((W // 2 + 22, rule_y, W - 220, rule_y), fill=gold_dim, width=2)
    draw.polygon(
        [(W // 2, rule_y - 7), (W // 2 + 7, rule_y), (W // 2, rule_y + 7), (W // 2 - 7, rule_y)],
        fill=gold,
    )

    font_title = load_font(
        [
            FONTS / "source-sans-3-700.ttf",
            "/usr/share/fonts/google-noto/NotoSans-Bold.ttf",
        ],
        28,
    )
    font_sub = load_font(
        [
            FONTS / "source-sans-3-600.ttf",
            "/usr/share/fonts/google-noto/NotoSans-SemiBold.ttf",
        ],
        23,
    )

    line1 = "CUSTOM TATTOOS & BODY PIERCING  \u00b7  DOWNTOWN MACON, GA"
    line2 = "484 CHERRY ST  \u00b7  (478) 259-1829  \u00b7  WALK-INS WELCOME"

    b1 = draw.textbbox((0, 0), line1, font=font_title)
    w1 = b1[2] - b1[0]
    draw.text(((W - w1) // 2, rule_y + 26), line1, font=font_title, fill=paper)

    b2 = draw.textbbox((0, 0), line2, font=font_sub)
    w2 = b2[2] - b2[0]
    draw.text(((W - w2) // 2, rule_y + 72), line2, font=font_sub, fill=gold)

    out_path = IMAGES / "og.jpg"
    base.save(out_path, "JPEG", quality=90, optimize=True, progressive=True)
    print(f"Generated {out_path.name} ({W}x{H})")


def optimize_editorial_photos():
    targets = [
        ("hero-bg.jpg", 1600, 82),
        ("hero-editorial.jpg", 1600, 84),
        ("strip-flash.jpg", 1000, 84),
        ("strip-piercing.jpg", 1000, 84),
    ]
    for filename, max_w, webp_q in targets:
        src = IMAGES / filename
        if not src.exists():
            print(f"{filename} not found; skipping.")
            continue
        im = Image.open(src).convert("RGB")
        if im.width > max_w:
            new_h = int(im.height * (max_w / im.width))
            im = im.resize((max_w, new_h), Image.Resampling.LANCZOS)
            im.save(src, "JPEG", quality=85, optimize=True, progressive=True)
        webp_path = IMAGES / f"{src.stem}.webp"
        im.save(webp_path, "WEBP", quality=webp_q, method=6)
        print(f"Saved optimized {filename} & {webp_path.name} ({im.size[0]}x{im.size[1]})")


def convert_portfolio_webp():
    for stem in PORTFOLIO_STEMS:
        src = IMAGES / f"{stem}.jpg"
        if not src.exists():
            print(f"Warning: {src.name} missing")
            continue
        im = Image.open(src).convert("RGB")
        # Save responsive WebP at native size (or max 1200px for 1400px sources)
        if im.width > 1200:
            new_h = int(im.height * (1200 / im.width))
            im_webp = im.resize((1200, new_h), Image.Resampling.LANCZOS)
        else:
            im_webp = im
        im_webp.save(IMAGES / f"{stem}.webp", "WEBP", quality=84, method=6)
    print("Converted portfolio images to WebP.")


def main():
    logo_im = make_logo_transparent()
    generate_og_image(logo_im)
    optimize_editorial_photos()
    convert_portfolio_webp()


if __name__ == "__main__":
    main()
