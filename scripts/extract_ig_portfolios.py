#!/usr/bin/env python3
"""
Auto-detect exact non-white photo bounds in captured Instagram screenshots,
apply clean UI-free insets (removing carousel dots, > arrows, and tag icons),
and export crisp .jpg + .webp portfolio images to images/artists/.
"""

from pathlib import Path
from PIL import Image, ImageFilter

RAW = Path("/home/thegenuinegeek/.gemini/antigravity/brain/cd43f4a5-4166-4126-ab98-f0c300a2bf80/scratch/ig_raw")
OUT = Path(__file__).resolve().parent.parent / "images" / "artists"
OUT.mkdir(parents=True, exist_ok=True)


def auto_main_box(im, trim_ui=True, keep_bottom=False):
    px = im.load()
    w, h = im.size
    cx, cy = 210, 260

    # Walk up from cy to first white row
    y0 = cy
    while y0 > 50 and any(min(px[x, y0 - 1]) < 248 for x in range(120, 310, 8)):
        y0 -= 1

    # Walk down from cy to first white row
    y1 = cy
    while y1 < 620 and any(min(px[x, y1 + 1]) < 248 for x in range(120, 310, 8)):
        y1 += 1

    mid_y = (y0 + y1) // 2
    # Walk left from cx to first white col
    x0 = cx
    while x0 > 5 and any(min(px[x0 - 1, y]) < 248 for y in range(y0 + 30, y1 - 30, 12)):
        x0 -= 1

    # Walk right from cx until comment pane (vertical border followed by white sidebar)
    x1 = cx
    while x1 < 460:
        # Stop if next 12px horizontally are almost pure white across vertical samples
        samples = range(y0 + 50, y1 - 50, 16)
        is_sidebar = all(
            sum(1 for y in samples if min(px[x1 + dx, y]) >= 250) > len(samples) * 0.85
            for dx in (3, 8, 14)
        )
        if is_sidebar:
            break
        x1 += 1

    if trim_ui:
        # Trim carousel '>' on right, '...' dots at bottom, and tag/mute icon at bottom-left
        x0 += 28
        x1 -= 32
        y0 += 4
        y1 -= 8 if keep_bottom else 24
    else:
        x0 += 2
        x1 -= 2
        y0 += 2
        y1 -= 2

    return (x0, y0, x1, y1)


# (out_stem, src_name, mode, custom_or_flags)
ITEMS = [
    ("work-kevin-moth", "step_26_shot_1_kevin-dtattoos-1.png", "main_ui", False),

    ("storm-1", "step_30_shot_1_baza-stormtattoos-1.png", "main_ui", False),
    ("storm-2", "step_30_shot_2_baza-stormtattoos-2.png", "main_clean", False),
    ("storm-3", "step_30_shot_3_baza-stormtattoos-3.png", "main_clean", False),
    ("storm-4", "step_30_shot_4_baza-stormtattoos-4.png", "main_clean", False),

    ("amber-1", "step_61_shot_1_c-lo-qween-1.png", "main_ui", False),
    ("amber-2", "step_52_shot_2_c-lo-qween-2.png", "main_ui", False),
    ("amber-3", "step_52_shot_3_c-lo-qween-3.png", "main_ui", False),
    ("amber-4", "step_61_shot_1_c-lo-qween-1.png", "custom", (18, 648, 222, 912)),

    ("lee-1", "step_64_shot_1_inkyleetattoos-1.png", "custom", (68, 90, 364, 526)),
    ("lee-2", "step_79_shot_1_inkyleetattoos-2.png", "main_ui", False),
    ("lee-3", "step_56_shot_4_inkyleetattoos-4.png", "main_ui", False),
    ("lee-4", "step_56_shot_4_inkyleetattoos-4.png", "custom", (464, 684, 650, 956)),

    ("jordyn-1", "step_110_shot_1_jordyn-tatts-1.png", "main_ui", False),
    ("jordyn-2", "step_113_shot_1_jordyn-tatts-2.png", "main_ui", False),
    ("jordyn-3", "step_113_shot_2_jordyn-tatts-3.png", "main_clean", False),
    ("jordyn-4", "step_73.png", "main_ui", False),

    ("tyler-1", "step_117_shot_1_hol3-punch3r-2.png", "main_clean", False),
    ("tyler-2", "step_113.png", "main_ui", False),
    ("tyler-3", "step_117_shot_2_hol3-punch3r-3.png", "main_clean", False),
    ("tyler-4", "step_82.png", "main_clean", False),

    ("sky-1", "step_121_shot_1_lilskythetatguy-2.png", "main_ui", False),
    ("sky-2", "step_117.png", "main_ui", False),
    ("sky-3", "step_121_shot_2_lilskythetatguy-3.png", "main_ui", False),
    ("sky-4", "step_121_shot_3_lilskythetatguy-4.png", "main_ui", False),
]


def main():
    for out_stem, src_name, mode, extra in ITEMS:
        im = Image.open(RAW / src_name).convert("RGB")
        if mode == "custom":
            box = extra
        elif mode == "main_clean":
            box = auto_main_box(im, trim_ui=False)
        else:
            box = auto_main_box(im, trim_ui=True, keep_bottom=bool(extra))

        cropped = im.crop(box)
        target_w = 640
        if cropped.width < target_w:
            scale = target_w / cropped.width
            target_h = int(round(cropped.height * scale))
            cropped = cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)
            cropped = cropped.filter(ImageFilter.UnsharpMask(radius=0.9, percent=95, threshold=3))

        cropped.save(OUT / f"{out_stem}.jpg", "JPEG", quality=88, optimize=True, progressive=True)
        cropped.save(OUT / f"{out_stem}.webp", "WEBP", quality=85, method=6)
        print(f"{out_stem:18s} box={box} -> {cropped.size[0]}x{cropped.size[1]}")


if __name__ == "__main__":
    main()
