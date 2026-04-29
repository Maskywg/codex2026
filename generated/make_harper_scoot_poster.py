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

HARPER = REF_DIR / "dylan_harper_espn.png"
SCOOT = REF_DIR / "scoot_henderson_espn.png"


def crop_fit(src: Image.Image, size: tuple[int, int]) -> Image.Image:
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
    harper = Image.open(HARPER)
    scoot = Image.open(SCOOT)

    board = Image.new("RGB", (1536, 1536), (12, 14, 22))
    d = ImageDraw.Draw(board)
    title = ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 42)
    small = ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 25)

    d.rectangle((0, 0, 768, 1536), fill=(18, 26, 52))
    d.rectangle((768, 0, 1536, 1536), fill=(70, 24, 28))
    d.line((768, 0, 768, 1536), fill=(245, 245, 245), width=4)

    board.paste(crop_fit(harper, (590, 520)), (88, 80))
    board.paste(crop_fit(harper, (430, 320)), (170, 655))
    d.text((88, 1060), "DYLAN HARPER", font=title, fill=(250, 252, 255))
    d.text((88, 1130), "Identity notes: youthful broad face, full eyebrows,", font=small, fill=(226, 234, 255))
    d.text((88, 1170), "short tight curls, clean-shaven look, strong guard", font=small, fill=(226, 234, 255))
    d.text((88, 1210), "build, San Antonio Spurs black/silver #2 feel.", font=small, fill=(226, 234, 255))

    board.paste(crop_fit(scoot, (590, 520)), (858, 80))
    board.paste(crop_fit(scoot, (430, 320)), (938, 655))
    d.text((858, 1060), "SCOOT HENDERSON", font=title, fill=(250, 252, 255))
    d.text((858, 1130), "Identity notes: compact athletic face, defined jaw,", font=small, fill=(255, 230, 230))
    d.text((858, 1170), "short high twists / locs, light mustache and goatee,", font=small, fill=(255, 230, 230))
    d.text((858, 1210), "Portland Trail Blazers red/black #00 guard feel.", font=small, fill=(255, 230, 230))

    d.text(
        (88, 1390),
        "Use these portraits only for identity. Create a new action photo, not a headshot collage.",
        font=small,
        fill=(245, 245, 245),
    )
    out = REF_DIR / "harper_scoot_reference_board.png"
    board.save(out, quality=95)
    return out


def generate_action(ref: Path) -> Path:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    prompt = (
        "Create a new ultra-realistic full-body NBA one-on-one isolation action photograph using the two portrait references only for facial identity, hairstyle, "
        "body feel, and uniform color cues. Do not copy the reference board layout, do not paste headshots, do not create a collage. "
        "Left player should resemble Dylan Harper: youthful broad face, full eyebrows, short tight curls, clean-shaven look, strong young guard build, "
        "San Antonio Spurs black and silver #2 uniform feel. Right player should resemble Scoot Henderson: compact athletic face, defined jaw, short high twists or locs, "
        "light mustache and goatee, Portland Trail Blazers red and black #00 uniform feel. "
        "Harper attacks downhill with a low left-hand dribble, Scoot slides laterally in a hard defensive stance with one hand contesting the handle, intense eye contact, "
        "hardwood court, packed NBA arena, dramatic stadium lighting, sweat, realistic motion blur, cinematic sports photography. "
        "No readable text, no official logos, no watermark, leave darker lower area for later typography."
    )
    subprocess.run(
        [
            "python3",
            str(DRAW_SCRIPT),
            prompt,
            "--edit",
            str(ref),
            "--name",
            "next_wave_collision_identity_action",
            "--size",
            "1024x1536",
            "--quality",
            "low",
            "--outdir",
            str(RAW_DIR),
        ],
        check=True,
    )
    return sorted(RAW_DIR.glob("next_wave_collision_identity_action_*.png"))[-1]


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
            "next_wave_collision_identity_action",
            raw,
            "NEXT WAVE COLLISION",
            "HARPER",
            "HENDERSON",
            "SAN ANTONIO SPURS",
            "PORTLAND TRAIL BLAZERS",
            "WEST YOUNG GUARDS  ONE-ON-ONE",
            (196, 206, 212),
            (224, 58, 62),
            (238, 242, 246),
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
