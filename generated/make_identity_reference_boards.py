from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
POSTER_DIR = ROOT / "playoff_matchup_posters"
REF_DIR = POSTER_DIR / "identity_refs"


@dataclass(frozen=True)
class RefBoard:
    slug: str
    left_name: str
    right_name: str
    left_path: Path
    right_path: Path
    left_notes: str
    right_notes: str


BOARDS = [
    RefBoard(
        slug="franchise_fire",
        left_name="PAOLO BANCHERO",
        right_name="CADE CUNNINGHAM",
        left_path=POSTER_DIR / "refs" / "paolo_banchero.png",
        right_path=POSTER_DIR / "refs" / "cade_cunningham.png",
        left_notes="oval face, long braids, serious expression",
        right_notes="rounder face, short curly hair, trimmed beard",
    ),
    RefBoard(
        slug="northern_pressure",
        left_name="SCOTTIE BARNES",
        right_name="DONOVAN MITCHELL",
        left_path=Path("/Users/masky/Desktop/NBA/Barns.png"),
        right_path=Path("/Users/masky/Desktop/NBA/donovan michell.png"),
        left_notes="wide smile, short braids, youthful face",
        right_notes="short textured hair, trimmed beard, chain",
    ),
    RefBoard(
        slug="legends_at_war",
        left_name="KEVIN DURANT",
        right_name="LEBRON JAMES",
        left_path=Path("/Users/masky/Desktop/NBA/kevin durent.png"),
        right_path=POSTER_DIR / "refs" / "lebron_james.png",
        left_notes="slender face, short hair, thin mustache and goatee",
        right_notes="broad face, close-cropped hair, full beard",
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


def main() -> None:
    REF_DIR.mkdir(parents=True, exist_ok=True)
    title_font = ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 34)
    small_font = ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 21)
    for item in BOARDS:
        board = Image.new("RGBA", (1024, 1024), (12, 14, 24, 255))
        d = ImageDraw.Draw(board)
        d.rectangle((0, 0, 512, 1024), fill=(18, 30, 70, 255))
        d.rectangle((512, 0, 1024, 1024), fill=(82, 18, 30, 255))
        d.rectangle((40, 70, 984, 690), outline=(255, 255, 255, 160), width=3)
        d.line((512, 60, 512, 720), fill=(255, 255, 255, 90), width=4)
        paste_portrait(board, item.left_path, (80, 130, 468, 642))
        paste_portrait(board, item.right_path, (556, 130, 944, 642))
        d.text((80, 720), item.left_name, font=title_font, fill=(245, 248, 255))
        d.text((556, 720), item.right_name, font=title_font, fill=(245, 248, 255))
        d.text((80, 774), item.left_notes, font=small_font, fill=(218, 228, 255))
        d.text((556, 774), item.right_notes, font=small_font, fill=(255, 224, 224))
        d.text((80, 870), "Use these portraits only as identity references.", font=small_font, fill=(240, 240, 240))
        d.text((80, 906), "Generate a new full-body one-on-one basketball action poster.", font=small_font, fill=(240, 240, 240))
        out = REF_DIR / f"{item.slug}_identity_reference.png"
        board.convert("RGB").save(out, quality=95)
        print(out)


if __name__ == "__main__":
    main()
