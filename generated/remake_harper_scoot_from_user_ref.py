from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
POSTER_DIR = ROOT / "playoff_matchup_posters"
REF_DIR = POSTER_DIR / "refs_harper_scoot"
RAW_DIR = POSTER_DIR / "raw_harper_scoot"
FINAL_DIR = POSTER_DIR / "final_harper_scoot"
DRAW_SCRIPT = Path("/Users/masky/.agents/skills/draw/draw.py")

HARPER_USER = Path("/Users/masky/Desktop/NBA/G4y8q9RaoAAAsX-.jpeg")
SCOOT_USER = Path("/Users/masky/Desktop/NBA/hq720.jpg")


def crop_cover(src: Image.Image, crop: tuple[int, int, int, int], size: tuple[int, int]) -> Image.Image:
    im = src.crop(crop).convert("RGB")
    tw, th = size
    scale = max(tw / im.width, th / im.height)
    im = im.resize((int(im.width * scale), int(im.height * scale)), Image.Resampling.LANCZOS)
    left = (im.width - tw) // 2
    top = (im.height - th) // 2
    return im.crop((left, top, left + tw, top + th))


def alpha_fit(src: Image.Image, size: tuple[int, int]) -> Image.Image:
    im = src.convert("RGBA")
    bbox = im.getbbox()
    if bbox:
        im = im.crop(bbox)
    bg = Image.new("RGB", im.size, (18, 20, 28))
    bg.paste(im, mask=im.getchannel("A"))
    tw, th = size
    scale = min(tw / bg.width, th / bg.height)
    resized = bg.resize((int(bg.width * scale), int(bg.height * scale)), Image.Resampling.LANCZOS)
    out = Image.new("RGB", size, (18, 20, 28))
    out.paste(resized, ((tw - resized.width) // 2, (th - resized.height) // 2))
    return out


def make_ref_board() -> Path:
    REF_DIR.mkdir(parents=True, exist_ok=True)
    harper = Image.open(HARPER_USER).convert("RGB")
    scoot = Image.open(SCOOT_USER).convert("RGB")

    board = Image.new("RGB", (1536, 1536), (12, 14, 22))
    d = ImageDraw.Draw(board)
    title = ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 42)
    small = ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 25)

    d.rectangle((0, 0, 768, 1536), fill=(24, 26, 30))
    d.rectangle((768, 0, 1536, 1536), fill=(78, 22, 26))
    d.line((768, 0, 768, 1536), fill=(245, 245, 245), width=4)

    board.paste(crop_cover(harper, (290, 20, 690, 440), (540, 520)), (114, 70))
    board.paste(crop_cover(harper, (60, 0, 875, 1125), (330, 460)), (72, 650))
    board.paste(crop_cover(harper, (250, 260, 865, 1040), (330, 460)), (420, 650))
    d.text((84, 1160), "DYLAN HARPER", font=title, fill=(250, 252, 255))
    d.text((84, 1230), "Use this exact identity: rounded youthful face,", font=small, fill=(230, 236, 246))
    d.text((84, 1270), "high loose afro curls, thin mustache, small chin", font=small, fill=(230, 236, 246))
    d.text((84, 1310), "goatee, lean left-handed Spurs #2 driving guard.", font=small, fill=(230, 236, 246))

    board.paste(crop_cover(scoot, (170, 0, 555, 365), (590, 520)), (858, 80))
    board.paste(crop_cover(scoot, (30, 20, 665, 380), (430, 320)), (938, 655))
    d.text((858, 1060), "SCOOT HENDERSON", font=title, fill=(250, 252, 255))
    d.text((858, 1130), "Use this exact identity: compact athletic face,", font=small, fill=(255, 230, 230))
    d.text((858, 1170), "wide high afro, expressive mouth, light mustache,", font=small, fill=(255, 230, 230))
    d.text((858, 1210), "chin goatee, Blazers #00 explosive guard.", font=small, fill=(255, 230, 230))

    d.text(
        (84, 1430),
        "Generate a NEW one-on-one action photo. Do not paste these source images or copy this board.",
        font=small,
        fill=(245, 245, 245),
    )
    out = REF_DIR / "harper_user_scoot_reference_board.png"
    board.save(out, quality=95)
    return out


def generate_action(ref: Path) -> Path:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    prompt = (
        "Create a new ultra-realistic full-body NBA one-on-one isolation action photograph using the reference board only for player identity, hairstyle, "
        "body feel, and uniform color cues. Do not copy the reference board layout, do not paste the source images, do not create a collage. "
        "Left player must closely resemble Dylan Harper from the left reference: rounded youthful face, high loose afro curls, thin mustache, small chin goatee, "
        "lean left-handed driving guard build, San Antonio Spurs white/black #2 uniform feel. Right player should resemble Scoot Henderson from the right reference: "
        "compact athletic face, wide high afro, expressive mouth, light mustache and chin goatee, Portland Trail Blazers red and black #00 uniform feel. "
        "Harper drives left-to-right with a low left-hand dribble in white Spurs uniform, Scoot jumps into a hard defensive contest from the right in red Blazers uniform, "
        "hand up and body angled to cut off the lane, intense eye contact, hardwood court, packed NBA arena, dramatic stadium lighting, sweat, realistic motion blur, "
        "cinematic sports photography. No readable text, no official logos, no watermark, leave darker lower area for later typography."
    )
    subprocess.run(
        [
            "python3",
            str(DRAW_SCRIPT),
            prompt,
            "--edit",
            str(ref),
            "--name",
            "next_wave_collision_user_harper",
            "--size",
            "1024x1536",
            "--quality",
            "low",
            "--outdir",
            str(RAW_DIR),
        ],
        check=True,
    )
    return sorted(RAW_DIR.glob("next_wave_collision_user_harper_*.png"))[-1]


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
            "next_wave_collision_identity_action_v2",
            raw,
            "NEXT WAVE COLLISION",
            "HARPER",
            "HENDERSON",
            "SAN ANTONIO SPURS",
            "PORTLAND TRAIL BLAZERS",
            "WEST YOUNG GUARDS  ONE-ON-ONE",
            (226, 229, 232),
            (224, 58, 62),
            (246, 248, 250),
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
