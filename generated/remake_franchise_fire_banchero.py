from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
POSTER_DIR = ROOT / "playoff_matchup_posters"
REF_DIR = POSTER_DIR / "identity_refs_rework"
RAW_DIR = POSTER_DIR / "raw_rework"
FINAL_DIR = POSTER_DIR / "final_rework"
DRAW_SCRIPT = Path("/Users/masky/.agents/skills/draw/draw.py")


def paste_portrait(board: Image.Image, path: Path, box: tuple[int, int, int, int]) -> None:
    portrait = Image.open(path).convert("RGBA")
    max_w = box[2] - box[0]
    max_h = box[3] - box[1]
    scale = min(max_w / portrait.width, max_h / portrait.height)
    portrait = portrait.resize((int(portrait.width * scale), int(portrait.height * scale)), Image.Resampling.LANCZOS)
    x = box[0] + (max_w - portrait.width) // 2
    y = box[1] + (max_h - portrait.height) // 2
    board.alpha_composite(portrait, (x, y))


def make_ref_board() -> Path:
    REF_DIR.mkdir(parents=True, exist_ok=True)
    board = Image.new("RGBA", (1024, 1024), (12, 14, 24, 255))
    d = ImageDraw.Draw(board)
    title = ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 31)
    small = ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 20)
    d.rectangle((0, 0, 512, 1024), fill=(16, 56, 150, 255))
    d.rectangle((512, 0, 1024, 1024), fill=(155, 26, 42, 255))
    d.line((512, 50, 512, 790), fill=(255, 255, 255, 96), width=4)
    paste_portrait(board, POSTER_DIR / "refs" / "paolo_banchero.png", (34, 70, 502, 690))
    paste_portrait(board, POSTER_DIR / "refs" / "cade_cunningham.png", (546, 70, 990, 690))
    d.text((50, 718), "PAOLO BANCHERO", font=title, fill=(248, 250, 255))
    d.text((562, 718), "CADE CUNNINGHAM", font=title, fill=(248, 250, 255))
    d.text((50, 770), "broad oval face, lighter brown skin, high forehead", font=small, fill=(230, 238, 255))
    d.text((50, 802), "long thin braids, youthful clean jaw, faint goatee", font=small, fill=(230, 238, 255))
    d.text((50, 834), "NOT narrow-faced, NOT full beard, NOT older-looking", font=small, fill=(255, 230, 230))
    d.text((562, 770), "rounder face, short curly afro, trimmed beard", font=small, fill=(255, 232, 232))
    d.text((562, 802), "Detroit guard build, focused defender", font=small, fill=(255, 232, 232))
    d.text((50, 910), "Use portraits only as identity references; generate a new full-body action photo.", font=small, fill=(245, 245, 245))
    out = REF_DIR / "franchise_fire_banchero_rework_reference.png"
    board.convert("RGB").save(out, quality=95)
    return out


def generate_action(ref: Path) -> Path:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    prompt = (
        "Create a new ultra-realistic full-body NBA playoff one-on-one isolation action photograph using the two portrait references only "
        "for facial identity, face shape, skin tone, hairstyle, and facial hair. Do not copy the reference board layout. Do not paste headshots. "
        "Left player must closely resemble Paolo Banchero from the ESPN headshot: broad oval face, lighter brown skin, high forehead, long thin braids, "
        "youthful clean jawline, faint mustache and small chin goatee, Orlando Magic blue uniform colors. Avoid a narrow face, avoid full beard, avoid older-looking features. "
        "Right player should resemble Cade Cunningham: rounder face, short curly afro, trimmed beard, Detroit Pistons red and blue uniform colors. "
        "Banchero attacks from the left wing with the ball while Cunningham defends tightly in a low stance, intense eye contact, hardwood court, packed NBA arena, "
        "dramatic stadium lighting, sweat, crisp sports photography, natural realistic anatomy. No readable text, no official logos, no watermark, leave darker lower area for later typography."
    )
    subprocess.run(
        [
            "python3",
            str(DRAW_SCRIPT),
            prompt,
            "--edit",
            str(ref),
            "--name",
            "franchise_fire_banchero_rework",
            "--size",
            "1024x1536",
            "--quality",
            "low",
            "--outdir",
            str(RAW_DIR),
        ],
        check=True,
    )
    return sorted(RAW_DIR.glob("franchise_fire_banchero_rework_*.png"))[-1]


def compose(raw: Path) -> Path:
    module_path = ROOT / "compose_clean_matchup_posters.py"
    spec = importlib.util.spec_from_file_location("clean_composer", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot load clean composer")
    clean = importlib.util.module_from_spec(spec)
    sys.modules["clean_composer"] = clean
    spec.loader.exec_module(clean)
    old_out = clean.OUTDIR
    clean.OUTDIR = FINAL_DIR
    try:
        poster = clean.Poster(
            "franchise_fire_identity_action_clean",
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
        clean.OUTDIR = old_out


def main() -> None:
    ref = make_ref_board()
    raw = generate_action(ref)
    print(compose(raw))


if __name__ == "__main__":
    main()
