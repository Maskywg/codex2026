from __future__ import annotations

import math
import shutil
import sqlite3
import subprocess
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parent
OUTDIR = ROOT / "playoff_matchup_posters"
RAW = OUTDIR / "raw"
FINAL = OUTDIR / "final"
DRAW_SCRIPT = Path("/Users/masky/.agents/skills/draw/draw.py")
DRIVE_FOLDER_ID = "12chkJd-8YZf93qkrlBQgNxhCmD09GTye"

POSTER_W, POSTER_H = 1080, 1620
TITLE_FONT = "/System/Library/Fonts/Avenir Next Condensed.ttc"
NAME_FONT = "/System/Library/Fonts/Avenir Next.ttc"
TEAM_FONT = "/System/Library/Fonts/Supplemental/Arial Narrow Bold.ttf"


@dataclass(frozen=True)
class Matchup:
    slug: str
    title: str
    left_name: str
    right_name: str
    left_team: str
    right_team: str
    top_label: str
    left_color: tuple[int, int, int]
    right_color: tuple[int, int, int]
    accent: tuple[int, int, int]
    source_image: Path | None = None


MATCHUPS = [
    Matchup(
        slug="franchise_fire",
        title="FRANCHISE FIRE",
        left_name="BANCHERO",
        right_name="CUNNINGHAM",
        left_team="ORLANDO MAGIC",
        right_team="DETROIT PISTONS",
        top_label="EAST FIRST ROUND  GAME 5",
        left_color=(18, 92, 255),
        right_color=(226, 35, 48),
        accent=(112, 166, 255),
        source_image=ROOT / "banchero_cunningham_1v1_20260429_002202.png",
    ),
    Matchup(
        slug="northern_pressure",
        title="NORTHERN PRESSURE",
        left_name="BARNES",
        right_name="MITCHELL",
        left_team="TORONTO RAPTORS",
        right_team="CLEVELAND CAVALIERS",
        top_label="EAST FIRST ROUND  GAME 5",
        left_color=(206, 17, 65),
        right_color=(111, 38, 61),
        accent=(255, 206, 84),
    ),
    Matchup(
        slug="legends_at_war",
        title="LEGENDS AT WAR",
        left_name="DURANT",
        right_name="LEBRON",
        left_team="HOUSTON ROCKETS",
        right_team="LOS ANGELES LAKERS",
        top_label="WEST FIRST ROUND  GAME 5",
        left_color=(206, 17, 65),
        right_color=(85, 37, 130),
        accent=(253, 185, 39),
    ),
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


def prompt(matchup: Matchup) -> str:
    return (
        f"Ultra-realistic vertical NBA playoff poster photograph of {matchup.left_name.title()} from {matchup.left_team.title()} "
        f"going one-on-one against {matchup.right_name.title()} from {matchup.right_team.title()}. "
        "Two elite basketball players locked in an isolation duel, one attacking with the ball, the other defending in a low stance, "
        "intense eye contact, full-body action, hardwood court, packed NBA arena, dramatic overhead stadium lights, sweat, rim light, "
        "shallow depth of field, cinematic 85mm sports photography, team-color lighting split across the image, realistic anatomy, "
        "authentic basketball uniform colors but no official logos, no readable jersey text, no generated lettering, no watermark, "
        "clean darker space near the bottom for later poster typography."
    )


def generate_raw(matchup: Matchup) -> Path:
    RAW.mkdir(parents=True, exist_ok=True)
    if matchup.source_image and matchup.source_image.exists():
        return matchup.source_image
    existing = sorted(RAW.glob(f"{matchup.slug}_*.png"))
    if existing:
        return existing[-1]
    subprocess.run(
        [
            "python3",
            str(DRAW_SCRIPT),
            prompt(matchup),
            "--name",
            matchup.slug,
            "--size",
            "1024x1536",
            "--quality",
            "low",
            "--outdir",
            str(RAW),
        ],
        check=True,
    )
    return sorted(RAW.glob(f"{matchup.slug}_*.png"))[-1]


def add_color_grade(image: Image.Image, matchup: Matchup) -> Image.Image:
    image = ImageEnhance.Contrast(image).enhance(1.18)
    image = ImageEnhance.Color(image).enhance(1.12).convert("RGBA")
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)

    for y in range(POSTER_H):
        top_alpha = int(max(0, 120 * (1 - y / (POSTER_H * 0.38))))
        bottom_alpha = int(max(0, 235 * ((y - POSTER_H * 0.54) / (POSTER_H * 0.46)) ** 1.55)) if y > POSTER_H * 0.54 else 0
        od.line((0, y, POSTER_W, y), fill=(4, 5, 13, max(top_alpha, bottom_alpha)))

    for x in range(POSTER_W):
        left_alpha = int(92 * max(0, 1 - x / (POSTER_W * 0.48)))
        right_alpha = int(92 * max(0, (x - POSTER_W * 0.52) / (POSTER_W * 0.48)))
        if left_alpha:
            od.line((x, 0, x, POSTER_H), fill=(*matchup.left_color, left_alpha))
        if right_alpha:
            od.line((x, 0, x, POSTER_H), fill=(*matchup.right_color, right_alpha))

    for i in range(5):
        y = 220 + i * 92
        od.line((-160, y, POSTER_W + 160, y + 300), fill=(*matchup.left_color, 35), width=9)
        od.line((-160, y + 36, POSTER_W + 160, y + 336), fill=(*matchup.right_color, 31), width=7)
    return Image.alpha_composite(image, overlay.filter(ImageFilter.GaussianBlur(0.4)))


def compose(raw_path: Path, matchup: Matchup) -> Path:
    FINAL.mkdir(parents=True, exist_ok=True)
    src = Image.open(raw_path).convert("RGB")
    if src.width > src.height:
        backdrop = cover_resize(src.filter(ImageFilter.GaussianBlur(18)), (POSTER_W, POSTER_H), 0.5, 0.5).convert("RGBA")
        sharp = cover_resize(src, (POSTER_W, 900), 0.5, 0.42).convert("RGBA")
        base = backdrop
        base.alpha_composite(sharp, (0, 230))
    else:
        base = cover_resize(src, (POSTER_W, POSTER_H), 0.5, 0.46).convert("RGBA")
    canvas = add_color_grade(base, matchup)
    draw = ImageDraw.Draw(canvas)

    draw.rectangle((54, 58, POSTER_W - 54, 116), fill=(5, 8, 22, 188), outline=(255, 255, 255, 74), width=2)
    center_text(draw, POSTER_W // 2, 72, matchup.top_label, font(TEAM_FONT, 32), (230, 234, 244))

    title_face = fit_font(draw, matchup.title, TITLE_FONT, 980, 162, 96)
    shadow = Image.new("RGBA", (POSTER_W, POSTER_H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    center_text(sd, POSTER_W // 2 + 8, 1162 + 8, matchup.title, title_face, (0, 0, 0, 230), stroke_width=6, stroke_fill=(0, 0, 0))
    canvas = Image.alpha_composite(canvas, shadow.filter(ImageFilter.GaussianBlur(3.5)))
    draw = ImageDraw.Draw(canvas)
    center_text(draw, POSTER_W // 2, 1162, matchup.title, title_face, (248, 250, 255), stroke_width=4, stroke_fill=(5, 8, 20))
    center_text(draw, POSTER_W // 2, 1157, matchup.title, title_face, matchup.accent, stroke_width=1, stroke_fill=(5, 8, 20))

    left_face = fit_font(draw, matchup.left_name, NAME_FONT, 410, 62, 42)
    right_face = fit_font(draw, matchup.right_name, NAME_FONT, 410, 62, 42)
    slash_face = font(TITLE_FONT, 90)
    left_x = 88
    right_w = text_w(draw, matchup.right_name, right_face)
    draw.text((left_x, 1355), matchup.left_name, font=left_face, fill=(246, 248, 255), stroke_width=2, stroke_fill=(5, 8, 18))
    center_text(draw, POSTER_W // 2, 1337, "/", slash_face, (255, 255, 255, 218), stroke_width=2, stroke_fill=(5, 8, 18))
    draw.text((POSTER_W - 88 - right_w, 1355), matchup.right_name, font=right_face, fill=(246, 248, 255), stroke_width=2, stroke_fill=(5, 8, 18))

    draw.rectangle((88, 1438, 466, 1448), fill=matchup.left_color)
    draw.rectangle((POSTER_W - 466, 1438, POSTER_W - 88, 1448), fill=matchup.right_color)
    center_text(draw, POSTER_W // 2, 1480, f"{matchup.left_team}  VS  {matchup.right_team}", font(TEAM_FONT, 40), (232, 235, 242), stroke_width=1, stroke_fill=(5, 8, 18))

    grain = Image.effect_noise((POSTER_W, POSTER_H), 12).convert("L")
    grain_rgba = Image.new("RGBA", (POSTER_W, POSTER_H), (255, 255, 255, 0))
    grain_rgba.putalpha(grain.point(lambda p: int(p * 0.10)))
    canvas = Image.alpha_composite(canvas, grain_rgba)

    out = FINAL / f"{matchup.slug}_poster.png"
    canvas.convert("RGB").save(out, quality=96)
    return out


def resolve_drive_folder(folder_id: str) -> Path | None:
    base = Path.home() / "Library/Application Support/Google/DriveFS"
    for db in base.glob("*/mirror_metadata_sqlite.db"):
        try:
            conn = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
            cur = conn.cursor()
            row = cur.execute("select stable_id from stable_ids where cloud_id=?", (folder_id,)).fetchone()
            if not row:
                conn.close()
                continue
            stable_id = row[0]
            parts: list[str] = []
            seen = set()
            while stable_id and stable_id not in seen:
                seen.add(stable_id)
                title_row = cur.execute("select local_title from items where stable_id=?", (stable_id,)).fetchone()
                if title_row and title_row[0]:
                    parts.append(title_row[0])
                parent_row = cur.execute(
                    "select parent_stable_id from stable_parents where item_stable_id=? limit 1",
                    (stable_id,),
                ).fetchone()
                stable_id = parent_row[0] if parent_row else None
            conn.close()
            parts.reverse()
            for cloud_root in (Path.home() / "Library/CloudStorage").glob("GoogleDrive-*"):
                candidate = cloud_root.joinpath(*parts)
                if candidate.exists():
                    return candidate
        except sqlite3.Error:
            continue
    return None


def copy_to_drive(paths: list[Path]) -> Path | None:
    target = resolve_drive_folder(DRIVE_FOLDER_ID)
    if not target:
        return None
    for path in paths:
        shutil.copy2(path, target / path.name)
    return target


def main() -> None:
    outputs: list[Path] = []
    for matchup in MATCHUPS:
        raw = generate_raw(matchup)
        outputs.append(compose(raw, matchup))
    target = copy_to_drive(outputs)
    print("FINAL")
    for path in outputs:
        print(path)
    print(f"DRIVE {target}" if target else "DRIVE unresolved")


if __name__ == "__main__":
    main()
