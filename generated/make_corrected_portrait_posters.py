from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parent
POSTER_DIR = ROOT / "playoff_matchup_posters"
FINAL = POSTER_DIR / "final_corrected"
W, H = 1080, 1620

TITLE_FONT = "/System/Library/Fonts/Avenir Next Condensed.ttc"
NAME_FONT = "/System/Library/Fonts/Avenir Next.ttc"
TEAM_FONT = "/System/Library/Fonts/Supplemental/Arial Narrow Bold.ttf"


@dataclass(frozen=True)
class Poster:
    slug: str
    title: str
    left_name: str
    right_name: str
    left_team: str
    right_team: str
    top_label: str
    left_ref: Path
    right_ref: Path
    background: Path
    left_color: tuple[int, int, int]
    right_color: tuple[int, int, int]
    accent: tuple[int, int, int]


POSTERS = [
    Poster(
        slug="franchise_fire_corrected",
        title="FRANCHISE FIRE",
        left_name="BANCHERO",
        right_name="CUNNINGHAM",
        left_team="ORLANDO MAGIC",
        right_team="DETROIT PISTONS",
        top_label="EAST FIRST ROUND  GAME 5",
        left_ref=POSTER_DIR / "refs" / "paolo_banchero.png",
        right_ref=POSTER_DIR / "refs" / "cade_cunningham.png",
        background=ROOT / "banchero_cunningham_1v1_20260429_002202.png",
        left_color=(18, 92, 255),
        right_color=(226, 35, 48),
        accent=(112, 166, 255),
    ),
    Poster(
        slug="northern_pressure_corrected",
        title="NORTHERN PRESSURE",
        left_name="BARNES",
        right_name="MITCHELL",
        left_team="TORONTO RAPTORS",
        right_team="CLEVELAND CAVALIERS",
        top_label="EAST FIRST ROUND  GAME 5",
        left_ref=Path("/Users/masky/Desktop/NBA/Barns.png"),
        right_ref=Path("/Users/masky/Desktop/NBA/donovan michell.png"),
        background=POSTER_DIR / "raw" / "northern_pressure_20260429_003701.png",
        left_color=(206, 17, 65),
        right_color=(111, 38, 61),
        accent=(255, 206, 84),
    ),
    Poster(
        slug="legends_at_war_corrected",
        title="LEGENDS AT WAR",
        left_name="DURANT",
        right_name="LEBRON",
        left_team="HOUSTON ROCKETS",
        right_team="LOS ANGELES LAKERS",
        top_label="WEST FIRST ROUND  GAME 5",
        left_ref=Path("/Users/masky/Desktop/NBA/kevin durent.png"),
        right_ref=POSTER_DIR / "refs" / "lebron_james.png",
        background=POSTER_DIR / "raw" / "legends_at_war_20260429_003728.png",
        left_color=(206, 17, 65),
        right_color=(85, 37, 130),
        accent=(253, 185, 39),
    ),
]


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size=size)


def text_width(draw: ImageDraw.ImageDraw, text: str, face: ImageFont.FreeTypeFont) -> int:
    box = draw.textbbox((0, 0), text, font=face)
    return box[2] - box[0]


def fit_font(draw: ImageDraw.ImageDraw, text: str, path: str, max_width: int, start: int, floor: int) -> ImageFont.FreeTypeFont:
    for size in range(start, floor - 1, -3):
        face = font(path, size)
        if text_width(draw, text, face) <= max_width:
            return face
    return font(path, floor)


def center_text(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    text: str,
    face: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int] | tuple[int, int, int, int],
    stroke_width: int = 0,
    stroke_fill: tuple[int, int, int] = (0, 0, 0),
) -> None:
    box = draw.textbbox((0, 0), text, font=face, stroke_width=stroke_width)
    draw.text((x - (box[2] - box[0]) // 2, y), text, font=face, fill=fill, stroke_width=stroke_width, stroke_fill=stroke_fill)


def cover_resize(src: Image.Image, size: tuple[int, int], x_bias: float = 0.5, y_bias: float = 0.5) -> Image.Image:
    tw, th = size
    scale = max(tw / src.width, th / src.height)
    nw, nh = math.ceil(src.width * scale), math.ceil(src.height * scale)
    resized = src.resize((nw, nh), Image.Resampling.LANCZOS)
    left = int((nw - tw) * x_bias)
    top = int((nh - th) * y_bias)
    return resized.crop((left, top, left + tw, top + th))


def make_background(path: Path, poster: Poster) -> Image.Image:
    src = Image.open(path).convert("RGB")
    base = cover_resize(src, (W, H), 0.5, 0.46)
    base = ImageEnhance.Contrast(base).enhance(1.18)
    base = ImageEnhance.Color(base).enhance(1.15)
    base = base.filter(ImageFilter.GaussianBlur(5)).convert("RGBA")
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    for y in range(H):
        top = int(max(0, 120 * (1 - y / (H * 0.32))))
        bottom = int(max(0, 245 * ((y - H * 0.48) / (H * 0.52)) ** 1.55)) if y > H * 0.48 else 0
        d.line((0, y, W, y), fill=(5, 7, 18, max(top, bottom)))
    for x in range(W):
        la = int(128 * max(0, 1 - x / (W * 0.52)))
        ra = int(128 * max(0, (x - W * 0.48) / (W * 0.52)))
        if la:
            d.line((x, 0, x, H), fill=(*poster.left_color, la))
        if ra:
            d.line((x, 0, x, H), fill=(*poster.right_color, ra))
    for i in range(7):
        y = 210 + i * 88
        d.line((-160, y, W + 160, y + 310), fill=(*poster.left_color, 40), width=9)
        d.line((-180, y + 34, W + 180, y + 344), fill=(*poster.right_color, 35), width=7)
    return Image.alpha_composite(base, overlay.filter(ImageFilter.GaussianBlur(0.35)))


def portrait_layer(path: Path, width: int, color: tuple[int, int, int], mirror: bool = False) -> Image.Image:
    im = Image.open(path).convert("RGBA")
    if mirror:
        im = im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    scale = width / im.width
    im = im.resize((width, int(im.height * scale)), Image.Resampling.LANCZOS)
    alpha = im.getchannel("A")
    glow = Image.new("RGBA", im.size, (*color, 0))
    glow.putalpha(alpha.filter(ImageFilter.GaussianBlur(18)).point(lambda p: int(p * 0.68)))
    shadow = Image.new("RGBA", im.size, (0, 0, 0, 0))
    shadow.putalpha(alpha.filter(ImageFilter.GaussianBlur(10)).point(lambda p: int(p * 0.55)))
    layer = Image.new("RGBA", (im.width + 80, im.height + 80), (0, 0, 0, 0))
    layer.alpha_composite(glow, (40, 28))
    layer.alpha_composite(shadow, (42, 45))
    layer.alpha_composite(im, (40, 40))
    return layer


def compose(poster: Poster) -> Path:
    FINAL.mkdir(parents=True, exist_ok=True)
    canvas = make_background(poster.background, poster)
    d = ImageDraw.Draw(canvas)

    left = portrait_layer(poster.left_ref, 640, poster.left_color)
    right = portrait_layer(poster.right_ref, 640, poster.right_color)
    canvas.alpha_composite(left, (-48, 500))
    canvas.alpha_composite(right, (W - right.width + 48, 500))

    split = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(split)
    sd.rectangle((W // 2 - 36, 0, W // 2 + 36, H), fill=(3, 5, 12, 145))
    canvas = Image.alpha_composite(canvas, split.filter(ImageFilter.GaussianBlur(2)))
    d = ImageDraw.Draw(canvas)

    d.rectangle((54, 58, W - 54, 116), fill=(5, 8, 22, 196), outline=(255, 255, 255, 82), width=2)
    center_text(d, W // 2, 72, poster.top_label, font(TEAM_FONT, 32), (230, 234, 244))

    title_face = fit_font(d, poster.title, TITLE_FONT, 980, 162, 90)
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shd = ImageDraw.Draw(shadow)
    center_text(shd, W // 2 + 8, 1132 + 8, poster.title, title_face, (0, 0, 0, 235), stroke_width=6, stroke_fill=(0, 0, 0))
    canvas = Image.alpha_composite(canvas, shadow.filter(ImageFilter.GaussianBlur(3.6)))
    d = ImageDraw.Draw(canvas)
    center_text(d, W // 2, 1132, poster.title, title_face, (248, 250, 255), stroke_width=4, stroke_fill=(5, 8, 20))
    center_text(d, W // 2, 1127, poster.title, title_face, poster.accent, stroke_width=1, stroke_fill=(5, 8, 20))

    left_face = fit_font(d, poster.left_name, NAME_FONT, 400, 64, 42)
    right_face = fit_font(d, poster.right_name, NAME_FONT, 400, 64, 42)
    slash_face = font(TITLE_FONT, 92)
    d.text((86, 1342), poster.left_name, font=left_face, fill=(246, 248, 255), stroke_width=2, stroke_fill=(5, 8, 18))
    center_text(d, W // 2, 1322, "/", slash_face, (255, 255, 255, 222), stroke_width=2, stroke_fill=(5, 8, 18))
    rw = text_width(d, poster.right_name, right_face)
    d.text((W - 86 - rw, 1342), poster.right_name, font=right_face, fill=(246, 248, 255), stroke_width=2, stroke_fill=(5, 8, 18))

    d.rectangle((86, 1426, 464, 1437), fill=poster.left_color)
    d.rectangle((W - 464, 1426, W - 86, 1437), fill=poster.right_color)
    center_text(d, W // 2, 1480, f"{poster.left_team}  VS  {poster.right_team}", font(TEAM_FONT, 40), (232, 235, 242), stroke_width=1, stroke_fill=(5, 8, 18))

    grain = Image.effect_noise((W, H), 10).convert("L")
    grain_rgba = Image.new("RGBA", (W, H), (255, 255, 255, 0))
    grain_rgba.putalpha(grain.point(lambda p: int(p * 0.08)))
    canvas = Image.alpha_composite(canvas, grain_rgba)

    out = FINAL / f"{poster.slug}.png"
    canvas.convert("RGB").save(out, quality=96)
    return out


def main() -> None:
    for poster in POSTERS:
        print(compose(poster))


if __name__ == "__main__":
    main()
