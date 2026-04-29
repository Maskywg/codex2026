from __future__ import annotations

import importlib.util
import math
import shutil
import sqlite3
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
POSTER_DIR = ROOT / "playoff_matchup_posters"
REF_DIR = POSTER_DIR / "identity_refs_next"
RAW_DIR = POSTER_DIR / "raw_identity_next"
FINAL_DIR = POSTER_DIR / "final_identity_next"
DRAW_SCRIPT = Path("/Users/masky/.agents/skills/draw/draw.py")
DRIVE_FOLDER_ID = "12chkJd-8YZf93qkrlBQgNxhCmD09GTye"

COMPOSER_PATH = ROOT / "make_three_matchup_posters.py"
spec = importlib.util.spec_from_file_location("matchup_posters", COMPOSER_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("Cannot load composer")
composer = importlib.util.module_from_spec(spec)
sys.modules["matchup_posters"] = composer
spec.loader.exec_module(composer)


@dataclass(frozen=True)
class Job:
    slug: str
    title: str
    left_name: str
    right_name: str
    left_team: str
    right_team: str
    top_label: str
    left_ref: Path
    right_ref: Path
    left_traits: str
    right_traits: str
    scene: str
    left_color: tuple[int, int, int]
    right_color: tuple[int, int, int]
    accent: tuple[int, int, int]


JOBS = [
    Job(
        slug="paint_warfare",
        title="PAINT WARFARE",
        left_name="CARTER JR",
        right_name="DUREN",
        left_team="ORLANDO MAGIC",
        right_team="DETROIT PISTONS",
        top_label="CENTER MATCHUP  DUNK VS BLOCK",
        left_ref=POSTER_DIR / "refs" / "wendell_carter_jr.png",
        right_ref=POSTER_DIR / "refs" / "jalen_duren.png",
        left_traits="strong oval face, close-cropped hair, trimmed beard, powerful big-man frame",
        right_traits="younger round face, short textured hair, clean jawline, explosive muscular frame",
        scene="Wendell Carter Jr. rises hard for a two-hand power dunk at the rim while Jalen Duren meets him in midair for a violent block attempt, bodies colliding in the paint, backboard and rim visible, vertical contact at the summit",
        left_color=(18, 92, 255),
        right_color=(226, 35, 48),
        accent=(112, 166, 255),
    ),
    Job(
        slug="second_unit_smoke",
        title="SECOND UNIT SMOKE",
        left_name="ISAAC",
        right_name="STEWART",
        left_team="ORLANDO MAGIC",
        right_team="DETROIT PISTONS",
        top_label="BENCH MOB  HARDCORE PLAY",
        left_ref=POSTER_DIR / "refs" / "jonathan_isaac.png",
        right_ref=POSTER_DIR / "refs" / "isaiah_stewart.png",
        left_traits="long narrow face, short hair, trimmed beard, tall lean defensive forward frame",
        right_traits="rounder strong face, short thick hair, full beard, rugged powerful enforcer build",
        scene="Jonathan Isaac and Isaiah Stewart dive onto the hardwood for a loose ball, arms stretched, one player ripping at the ball while the other crashes to the floor, hardcore scramble, bodies low, sneakers sliding, gritty physical 50-50 play",
        left_color=(18, 92, 255),
        right_color=(226, 35, 48),
        accent=(235, 237, 244),
    ),
]


def paste_portrait(board: Image.Image, path: Path, box: tuple[int, int, int, int]) -> None:
    portrait = Image.open(path).convert("RGBA")
    max_w = box[2] - box[0]
    max_h = box[3] - box[1]
    scale = min(max_w / portrait.width, max_h / portrait.height)
    portrait = portrait.resize((int(portrait.width * scale), int(portrait.height * scale)), Image.Resampling.LANCZOS)
    x = box[0] + (max_w - portrait.width) // 2
    y = box[1] + (max_h - portrait.height) // 2
    board.alpha_composite(portrait, (x, y))


def make_reference_board(job: Job) -> Path:
    REF_DIR.mkdir(parents=True, exist_ok=True)
    board = Image.new("RGBA", (1024, 1024), (12, 14, 24, 255))
    d = ImageDraw.Draw(board)
    title_font = ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 34)
    small_font = ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 21)
    d.rectangle((0, 0, 512, 1024), fill=(*job.left_color, 120))
    d.rectangle((512, 0, 1024, 1024), fill=(*job.right_color, 120))
    d.rectangle((40, 70, 984, 690), outline=(255, 255, 255, 160), width=3)
    d.line((512, 60, 512, 720), fill=(255, 255, 255, 90), width=4)
    paste_portrait(board, job.left_ref, (80, 130, 468, 642))
    paste_portrait(board, job.right_ref, (556, 130, 944, 642))
    d.text((80, 720), job.left_name, font=title_font, fill=(245, 248, 255))
    d.text((556, 720), job.right_name, font=title_font, fill=(245, 248, 255))
    d.text((80, 774), job.left_traits[:58], font=small_font, fill=(218, 228, 255))
    d.text((556, 774), job.right_traits[:58], font=small_font, fill=(255, 224, 224))
    d.text((80, 870), "Use these portraits only as identity references.", font=small_font, fill=(240, 240, 240))
    d.text((80, 906), "Generate a new full-body dynamic basketball action poster.", font=small_font, fill=(240, 240, 240))
    out = REF_DIR / f"{job.slug}_identity_reference.png"
    board.convert("RGB").save(out, quality=95)
    return out


def prompt(job: Job) -> str:
    return (
        "Create a new ultra-realistic full-body NBA playoff action photograph using the two portrait references only for facial identity and hairstyle. "
        "Do not copy the reference board layout. Do not paste headshots. "
        f"Left player should resemble {job.left_name}: {job.left_traits}, {job.left_team} uniform colors. "
        f"Right player should resemble {job.right_name}: {job.right_traits}, {job.right_team} uniform colors. "
        f"{job.scene}. Hardwood court, packed NBA arena, dramatic stadium lighting, sweat, motion blur, gritty cinematic sports photography. "
        "No readable text, no official logos, no watermark, leave darker lower area for later typography."
    )


def generate_action(job: Job, ref_board: Path) -> Path:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    existing = sorted(RAW_DIR.glob(f"{job.slug}_identity_action_*.png"))
    if existing:
        return existing[-1]
    subprocess.run(
        [
            "python3",
            str(DRAW_SCRIPT),
            prompt(job),
            "--edit",
            str(ref_board),
            "--name",
            f"{job.slug}_identity_action",
            "--size",
            "1024x1536",
            "--quality",
            "low",
            "--outdir",
            str(RAW_DIR),
        ],
        check=True,
    )
    return sorted(RAW_DIR.glob(f"{job.slug}_identity_action_*.png"))[-1]


def compose(job: Job, raw: Path) -> Path:
    FINAL_DIR.mkdir(parents=True, exist_ok=True)
    matchup = composer.Matchup(
        slug=job.slug,
        title=job.title,
        left_name=job.left_name,
        right_name=job.right_name,
        left_team=job.left_team,
        right_team=job.right_team,
        top_label=job.top_label,
        left_color=job.left_color,
        right_color=job.right_color,
        accent=job.accent,
    )
    old_final = composer.FINAL
    composer.FINAL = FINAL_DIR
    try:
        return composer.compose(raw, matchup)
    finally:
        composer.FINAL = old_final


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
                parent_row = cur.execute("select parent_stable_id from stable_parents where item_stable_id=? limit 1", (stable_id,)).fetchone()
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


def main() -> None:
    finals: list[Path] = []
    for job in JOBS:
        ref = make_reference_board(job)
        raw = generate_action(job, ref)
        finals.append(compose(job, raw))
    target = resolve_drive_folder(DRIVE_FOLDER_ID)
    if target:
        for path in finals:
            shutil.copy2(path, target / path.name)
    print("FINAL")
    for path in finals:
        print(path)
    print(f"DRIVE {target}" if target else "DRIVE unresolved")


if __name__ == "__main__":
    main()
