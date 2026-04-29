from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "banchero_cunningham_1v1_20260429_002202.png"
OUTPUT = ROOT / "banchero_cunningham_east_side_duel_poster.png"

W, H = 1080, 1620
BLUE = (25, 84, 255)
RED = (224, 35, 54)
WHITE = (245, 247, 255)


def font(path: str, size: int, index: int = 0) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size=size, index=index)


def fit(draw: ImageDraw.ImageDraw, text: str, path: str, max_width: int, start: int, floor: int) -> ImageFont.FreeTypeFont:
    for size in range(start, floor - 1, -3):
        face = font(path, size)
        if draw.textbbox((0, 0), text, font=face)[2] <= max_width:
            return face
    return font(path, floor)


def cover_resize(src: Image.Image, size: tuple[int, int], x_bias: float = 0.5, y_bias: float = 0.5) -> Image.Image:
    tw, th = size
    scale = max(tw / src.width, th / src.height)
    nw, nh = math.ceil(src.width * scale), math.ceil(src.height * scale)
    resized = src.resize((nw, nh), Image.Resampling.LANCZOS)
    left = int((nw - tw) * x_bias)
    top = int((nh - th) * y_bias)
    return resized.crop((left, top, left + tw, top + th))


def add_gradient(image: Image.Image) -> Image.Image:
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    for y in range(H):
        top_alpha = int(max(0, 150 * (1 - y / (H * 0.36))))
        bottom_alpha = int(max(0, 235 * ((y - H * 0.50) / (H * 0.50)) ** 1.6)) if y > H * 0.50 else 0
        draw.line((0, y, W, y), fill=(4, 6, 14, max(top_alpha, bottom_alpha)))

    for x in range(W):
        left_alpha = int(95 * max(0, 1 - x / (W * 0.45)))
        right_alpha = int(95 * max(0, (x - W * 0.55) / (W * 0.45)))
        if left_alpha:
            draw.line((x, 0, x, H), fill=(*BLUE, left_alpha))
        if right_alpha:
            draw.line((x, 0, x, H), fill=(*RED, right_alpha))

    return Image.alpha_composite(image, overlay)


def diagonal_streaks(image: Image.Image) -> Image.Image:
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for i, color in enumerate((BLUE, RED, WHITE)):
        offset = 170 + i * 86
        draw.line((-160, offset, W + 160, offset + 310), fill=(*color, 52), width=8)
        draw.line((-180, offset + 24, W + 180, offset + 334), fill=(*color, 22), width=22)
    for i in range(6):
        y = 980 + i * 62
        draw.line((-80, y, W + 80, y + 180), fill=(255, 255, 255, 18), width=3)
    return Image.alpha_composite(image, overlay.filter(ImageFilter.GaussianBlur(0.35)))


def draw_centered(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, face: ImageFont.FreeTypeFont, fill, **kwargs) -> None:
    x, y = xy
    box = draw.textbbox((0, 0), text, font=face, stroke_width=kwargs.get("stroke_width", 0))
    draw.text((x - (box[2] - box[0]) // 2, y), text, font=face, fill=fill, **kwargs)


def main() -> None:
    src = Image.open(SOURCE).convert("RGB")
    backdrop = cover_resize(src.filter(ImageFilter.GaussianBlur(18)), (W, H), 0.5, 0.5).convert("RGBA")
    sharp = cover_resize(src, (W, 900), 0.50, 0.40).convert("RGBA")

    canvas = ImageEnhance.Contrast(backdrop).enhance(1.18)
    canvas = ImageEnhance.Color(canvas).enhance(1.18)
    canvas.alpha_composite(sharp, (0, 235))
    canvas = add_gradient(canvas)
    canvas = diagonal_streaks(canvas)

    d = ImageDraw.Draw(canvas)
    title_font = "/System/Library/Fonts/Avenir Next Condensed.ttc"
    name_font = "/System/Library/Fonts/Avenir Next.ttc"
    narrow_font = "/System/Library/Fonts/Supplemental/Arial Narrow Bold.ttf"

    d.rounded_rectangle((54, 56, W - 54, 112), radius=0, fill=(5, 8, 22, 178), outline=(255, 255, 255, 74), width=2)
    draw_centered(d, (W // 2, 68), "ORLANDO MAGIC  VS  DETROIT PISTONS", font(narrow_font, 33), (226, 232, 244))

    title = "EAST SIDE DUEL"
    title_face = fit(d, title, title_font, 980, 172, 110)
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    draw_centered(sd, (W // 2 + 8, 1162 + 8), title, title_face, (0, 0, 0, 230), stroke_width=5, stroke_fill=(0, 0, 0, 230))
    canvas = Image.alpha_composite(canvas, shadow.filter(ImageFilter.GaussianBlur(3.5)))
    d = ImageDraw.Draw(canvas)
    draw_centered(d, (W // 2, 1162), title, title_face, (248, 250, 255), stroke_width=4, stroke_fill=(6, 9, 24))
    draw_centered(d, (W // 2, 1156), title, title_face, (120, 166, 255), stroke_width=1, stroke_fill=(6, 9, 24))

    slash_face = font(title_font, 88)
    name_face = fit(d, "BANCHERO", name_font, 390, 64, 46)
    name2_face = fit(d, "CUNNINGHAM", name_font, 410, 64, 44)
    d.text((85, 1355), "BANCHERO", font=name_face, fill=WHITE, stroke_width=2, stroke_fill=(5, 8, 18))
    draw_centered(d, (W // 2, 1337), "/", slash_face, (255, 255, 255, 210), stroke_width=2, stroke_fill=(5, 8, 18))
    box = d.textbbox((0, 0), "CUNNINGHAM", font=name2_face, stroke_width=2)
    d.text((W - 85 - (box[2] - box[0]), 1355), "CUNNINGHAM", font=name2_face, fill=WHITE, stroke_width=2, stroke_fill=(5, 8, 18))

    d.rectangle((85, 1438, 466, 1447), fill=BLUE)
    d.rectangle((W - 466, 1438, W - 85, 1447), fill=RED)
    draw_centered(d, (W // 2, 1474), "ONE-ON-ONE ISOLATION", font(narrow_font, 52), (232, 235, 242), stroke_width=1, stroke_fill=(5, 8, 18))

    grain = Image.effect_noise((W, H), 12).convert("L")
    grain_rgba = Image.new("RGBA", (W, H), (255, 255, 255, 0))
    grain_rgba.putalpha(grain.point(lambda p: int(p * 0.11)))
    canvas = Image.alpha_composite(canvas, grain_rgba)

    canvas.convert("RGB").save(OUTPUT, quality=96)
    print(OUTPUT)


if __name__ == "__main__":
    main()
