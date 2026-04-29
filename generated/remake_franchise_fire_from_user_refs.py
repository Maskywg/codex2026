from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
POSTER_DIR = ROOT / "playoff_matchup_posters"
REF_DIR = POSTER_DIR / "identity_refs_user"
RAW_DIR = POSTER_DIR / "raw_user_refs"
FINAL_DIR = POSTER_DIR / "final_user_refs"
DRAW_SCRIPT = Path("/Users/masky/.agents/skills/draw/draw.py")

BANCHERO = Path("/Users/masky/Library/CloudStorage/GoogleDrive-maskywg@gmail.com/我的雲端硬碟/NBA球星海報/4 30/Paolo Banchero.png")
CUNNINGHAM = Path("/Users/masky/Library/CloudStorage/GoogleDrive-maskywg@gmail.com/我的雲端硬碟/NBA球星海報/4 30/cunningham_20260427_133219_poster.png")


def crop_fit(src: Image.Image, crop: tuple[int, int, int, int], size: tuple[int, int]) -> Image.Image:
    im = src.crop(crop)
    tw, th = size
    scale = max(tw / im.width, th / im.height)
    im = im.resize((int(im.width * scale), int(im.height * scale)), Image.Resampling.LANCZOS)
    left = (im.width - tw) // 2
    top = (im.height - th) // 2
    return im.crop((left, top, left + tw, top + th))


def make_ref_board() -> Path:
    REF_DIR.mkdir(parents=True, exist_ok=True)
    b = Image.open(BANCHERO).convert("RGB")
    c = Image.open(CUNNINGHAM).convert("RGB")
    board = Image.new("RGB", (1536, 1536), (13, 15, 24))
    d = ImageDraw.Draw(board)
    title = ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 34)
    small = ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 23)

    d.rectangle((0, 0, 768, 1536), fill=(14, 36, 78))
    d.rectangle((768, 0, 1536, 1536), fill=(92, 20, 30))
    d.line((768, 0, 768, 1536), fill=(255, 255, 255), width=4)

    # Banchero: profile face, dunk/action, dribble body from user-provided poster.
    board.paste(crop_fit(b, (515, 20, 925, 610), (600, 470)), (84, 80))
    board.paste(crop_fit(b, (80, 155, 500, 620), (290, 350)), (78, 610))
    board.paste(crop_fit(b, (95, 880, 500, 1510), (430, 470)), (292, 610))
    d.text((84, 1110), "PAOLO BANCHERO", font=title, fill=(250, 252, 255))
    d.text((84, 1170), "Use this exact identity: broad oval face, headband,", font=small, fill=(230, 238, 255))
    d.text((84, 1210), "long thin braids, youthful face, faint mustache,", font=small, fill=(230, 238, 255))
    d.text((84, 1250), "small chin goatee, Orlando Magic #5 body feel.", font=small, fill=(230, 238, 255))

    # Cunningham: profile face and action body from user-provided poster.
    board.paste(crop_fit(c, (70, 85, 520, 660), (600, 520)), (852, 70))
    board.paste(crop_fit(c, (385, 500, 760, 1050), (330, 400)), (838, 635))
    board.paste(crop_fit(c, (650, 405, 925, 795), (300, 400)), (1188, 635))
    d.text((852, 1110), "CADE CUNNINGHAM", font=title, fill=(250, 252, 255))
    d.text((852, 1170), "Use this exact identity: short curly afro,", font=small, fill=(255, 230, 230))
    d.text((852, 1210), "rounder face, trimmed beard, Detroit Pistons #2", font=small, fill=(255, 230, 230))
    d.text((852, 1250), "guard build and focused expression.", font=small, fill=(255, 230, 230))

    d.text((84, 1390), "Generate a NEW one-on-one action photo. Do not copy poster text, logos, or collage layout.", font=small, fill=(245, 245, 245))
    out = REF_DIR / "franchise_fire_user_reference_board.png"
    board.save(out, quality=95)
    return out


def generate_action(ref: Path) -> Path:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    prompt = (
        "Create a new ultra-realistic full-body NBA playoff one-on-one isolation action photograph using the reference board only for player identity, "
        "face shape, hairstyle, body feel, and uniform color cues. Do not copy the reference board layout, do not copy poster typography, do not paste cutouts. "
        "Left player must closely resemble Paolo Banchero from the left reference: broad oval face, black headband, long thin braids, youthful face, faint mustache, "
        "small chin goatee, Orlando Magic blue #5 star-forward look. Right player must closely resemble Cade Cunningham from the right reference: short curly afro, "
        "rounder face, trimmed beard, Detroit Pistons red/blue #2 guard look. Banchero attacks off the dribble from the left wing, Cunningham defends in a low stance, "
        "intense eye contact, hardwood court, packed playoff arena, crisp sports photography, realistic sweat, natural anatomy. No readable text, no official logos, no watermark, "
        "leave darker lower area for later typography."
    )
    subprocess.run(
        [
            "python3",
            str(DRAW_SCRIPT),
            prompt,
            "--edit",
            str(ref),
            "--name",
            "franchise_fire_user_refs",
            "--size",
            "1024x1536",
            "--quality",
            "low",
            "--outdir",
            str(RAW_DIR),
        ],
        check=True,
    )
    return sorted(RAW_DIR.glob("franchise_fire_user_refs_*.png"))[-1]


def compose(raw: Path) -> Path:
    module_path = ROOT / "compose_clean_matchup_posters.py"
    spec = importlib.util.spec_from_file_location("clean_composer", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot load clean composer")
    clean = importlib.util.module_from_spec(spec)
    sys.modules["clean_composer"] = clean
    spec.loader.exec_module(clean)
    old = clean.OUTDIR
    clean.OUTDIR = FINAL_DIR
    try:
        poster = clean.Poster(
            "franchise_fire_user_refs_clean",
            raw,
            "FRANCHISE FIRE",
            "BANCHERO",
            "CUNNINGHAM",
            "ORLANDO MAGIC",
            "DETROIT PISTONS",
            "EAST FIRST ROUND  GAME 5",
            (18, 92, 255),
            (226, 35, 48),
            (112, 166, 255),
        )
        return clean.compose(poster)
    finally:
        clean.OUTDIR = old


def main() -> None:
    ref = make_ref_board()
    raw = generate_action(ref)
    print(compose(raw))


if __name__ == "__main__":
    main()
