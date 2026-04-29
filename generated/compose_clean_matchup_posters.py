from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parent
POSTER_DIR = ROOT / "playoff_matchup_posters"
OUTDIR = POSTER_DIR / "final_clean"
W, H = 1080, 1620

TITLE_FONT = "/System/Library/Fonts/Avenir Next Condensed.ttc"
NAME_FONT = "/System/Library/Fonts/Avenir Next.ttc"
TEAM_FONT = "/System/Library/Fonts/Supplemental/Arial Narrow Bold.ttf"


@dataclass(frozen=True)
class Poster:
    slug: str
    raw: Path
    title: str
    left_name: str
    right_name: str
    left_team: str
    right_team: str
    top_label: str
    left_color: tuple[int, int, int]
    right_color: tuple[int, int, int]
    accent: tuple[int, int, int]


def latest(folder: str, pattern: str) -> Path:
    paths = sorted((POSTER_DIR / folder).glob(pattern))
    if not paths:
        raise FileNotFoundError(f"{folder}/{pattern}")
    return paths[-1]


POSTERS = [
    Poster("paint_warfare_clean", latest("raw_clean", "paint_warfare_airborne_clean_*.png"), "PAINT WARFARE", "CARTER JR", "DUREN", "ORLANDO MAGIC", "DETROIT PISTONS", "CENTER MATCHUP  DUNK VS BLOCK", (18, 92, 255), (226, 35, 48), (112, 166, 255)),
    Poster("low_post_collision_clean", latest("raw_clean", "low_post_collision_airborne_clean_*.png"), "LOW POST COLLISION", "SENGUN", "AYTON", "HOUSTON ROCKETS", "LOS ANGELES LAKERS", "CENTER MATCHUP  DUNK VS BLOCK", (206, 17, 65), (85, 37, 130), (253, 185, 39)),
    Poster("rim_lockdown_clean", latest("raw_clean", "rim_lockdown_airborne_clean_*.png"), "RIM LOCKDOWN", "POELTL", "ALLEN", "TORONTO RAPTORS", "CLEVELAND CAVALIERS", "CENTER MATCHUP  DUNK VS BLOCK", (206, 17, 65), (111, 38, 61), (255, 206, 84)),
    Poster("second_unit_smoke_clean", latest("raw_identity_next", "second_unit_smoke_identity_action_*.png"), "SECOND UNIT SMOKE", "ISAAC", "STEWART", "ORLANDO MAGIC", "DETROIT PISTONS", "BENCH MOB  HARDCORE PLAY", (18, 92, 255), (226, 35, 48), (235, 237, 244)),
    Poster("spark_plug_showdown_clean", latest("raw_identity_next", "spark_plug_showdown_identity_action_*.png"), "SPARK PLUG SHOWDOWN", "SHEPPARD", "REAVES", "HOUSTON ROCKETS", "LOS ANGELES LAKERS", "BENCH MOB  HARDCORE PLAY", (206, 17, 65), (85, 37, 130), (253, 185, 39)),
    Poster("bench_heat_check_clean", latest("raw_identity_next", "bench_heat_check_identity_action_*.png"), "BENCH HEAT CHECK", "DICK", "MERRILL", "TORONTO RAPTORS", "CLEVELAND CAVALIERS", "BENCH MOB  HARDCORE PLAY", (206, 17, 65), (111, 38, 61), (255, 206, 84)),
    Poster("deuce_under_fire_clean", latest("raw_bench_three", "deuce_under_fire_identity_action_*.png"), "DEUCE UNDER FIRE", "MCBRIDE", "DANIELS", "NEW YORK KNICKS", "ATLANTA HAWKS", "BENCH SHOOTER  THREE-POINT CONTEST", (0, 107, 182), (225, 68, 52), (245, 132, 38)),
    Poster("green_light_contest_clean", latest("raw_bench_three", "green_light_contest_identity_action_*.png"), "GREEN LIGHT CONTEST", "PRITCHARD", "GRIMES", "BOSTON CELTICS", "PHILADELPHIA 76ERS", "BENCH SHOOTER  THREE-POINT CONTEST", (0, 122, 51), (0, 107, 182), (139, 111, 78)),
    Poster("mile_high_release_clean", latest("raw_bench_three", "mile_high_release_identity_action_*.png"), "MILE HIGH RELEASE", "STRAWTHER", "DOSUNMU", "DENVER NUGGETS", "MINNESOTA TIMBERWOLVES", "BENCH SHOOTER  THREE-POINT CONTEST", (13, 34, 64), (12, 35, 64), (255, 198, 39)),
]


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size=size)


def text_w(draw: ImageDraw.ImageDraw, text: str, face: ImageFont.FreeTypeFont) -> int:
    box = draw.textbbox((0, 0), text, font=face)
    return box[2] - box[0]


def fit_font(draw: ImageDraw.ImageDraw, text: str, path: str, max_width: int, start: int, floor: int) -> ImageFont.FreeTypeFont:
    for size in range(start, floor - 1, -3):
        face = font(path, size)
        if text_w(draw, text, face) <= max_width:
            return face
    return font(path, floor)


def center_text(draw: ImageDraw.ImageDraw, x: int, y: int, text: str, face: ImageFont.FreeTypeFont, fill, stroke_width: int = 0, stroke_fill=(0, 0, 0)) -> None:
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


def grade(image: Image.Image, poster: Poster) -> Image.Image:
    image = ImageEnhance.Contrast(image).enhance(1.08)
    image = ImageEnhance.Color(image).enhance(1.04).convert("RGBA")
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    for y in range(H):
        top_alpha = int(max(0, 72 * (1 - y / (H * 0.32))))
        bottom_alpha = int(max(0, 210 * ((y - H * 0.58) / (H * 0.42)) ** 1.45)) if y > H * 0.58 else 0
        d.line((0, y, W, y), fill=(4, 6, 14, max(top_alpha, bottom_alpha)))
    for x in range(W):
        left_alpha = int(42 * max(0, 1 - x / (W * 0.46)))
        right_alpha = int(42 * max(0, (x - W * 0.54) / (W * 0.46)))
        if left_alpha:
            d.line((x, 0, x, H), fill=(*poster.left_color, left_alpha))
        if right_alpha:
            d.line((x, 0, x, H), fill=(*poster.right_color, right_alpha))
    d.rectangle((W // 2 - 24, 0, W // 2 + 24, H), fill=(0, 0, 0, 34))
    return Image.alpha_composite(image, overlay)


def compose(poster: Poster) -> Path:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    src = Image.open(poster.raw).convert("RGB")
    canvas = cover_resize(src, (W, H), 0.5, 0.45)
    canvas = grade(canvas, poster)
    draw = ImageDraw.Draw(canvas)

    draw.rectangle((54, 58, W - 54, 116), fill=(5, 8, 22, 185), outline=(255, 255, 255, 90), width=2)
    center_text(draw, W // 2, 72, poster.top_label, font(TEAM_FONT, 32), (232, 236, 246))

    title_face = fit_font(draw, poster.title, TITLE_FONT, 980, 150, 84)
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    center_text(sd, W // 2 + 7, 1182 + 7, poster.title, title_face, (0, 0, 0, 230), stroke_width=5, stroke_fill=(0, 0, 0))
    canvas = Image.alpha_composite(canvas, shadow.filter(ImageFilter.GaussianBlur(2.8)))
    draw = ImageDraw.Draw(canvas)
    center_text(draw, W // 2, 1182, poster.title, title_face, poster.accent, stroke_width=4, stroke_fill=(5, 8, 20))
    center_text(draw, W // 2, 1178, poster.title, title_face, (252, 253, 255), stroke_width=1, stroke_fill=(5, 8, 20))

    left_face = fit_font(draw, poster.left_name, NAME_FONT, 410, 60, 40)
    right_face = fit_font(draw, poster.right_name, NAME_FONT, 410, 60, 40)
    slash_face = font(TITLE_FONT, 86)
    draw.text((86, 1360), poster.left_name, font=left_face, fill=(248, 250, 255), stroke_width=2, stroke_fill=(5, 8, 18))
    center_text(draw, W // 2, 1344, "/", slash_face, (255, 255, 255, 225), stroke_width=2, stroke_fill=(5, 8, 18))
    rw = text_w(draw, poster.right_name, right_face)
    draw.text((W - 86 - rw, 1360), poster.right_name, font=right_face, fill=(248, 250, 255), stroke_width=2, stroke_fill=(5, 8, 18))

    draw.rectangle((86, 1442, 464, 1452), fill=poster.left_color)
    draw.rectangle((W - 464, 1442, W - 86, 1452), fill=poster.right_color)
    center_text(draw, W // 2, 1490, f"{poster.left_team}  VS  {poster.right_team}", font(TEAM_FONT, 39), (235, 238, 246), stroke_width=1, stroke_fill=(5, 8, 18))

    out = OUTDIR / f"{poster.slug}.png"
    canvas.convert("RGB").save(out, quality=96)
    return out


def main() -> None:
    for poster in POSTERS:
        print(compose(poster))


if __name__ == "__main__":
    main()
