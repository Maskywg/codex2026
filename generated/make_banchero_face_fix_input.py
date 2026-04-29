from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
POSTER_DIR = ROOT / "playoff_matchup_posters"
OUT = POSTER_DIR / "identity_refs_rework" / "banchero_face_fix_input.png"


def main() -> None:
    action = Image.open(POSTER_DIR / "raw_rework" / "franchise_fire_banchero_rework_v2_20260429_212153.png").convert("RGB")
    head = Image.open(POSTER_DIR / "refs" / "paolo_banchero.png").convert("RGBA")
    board = Image.new("RGB", (1536, 1536), (10, 12, 22))
    action = action.resize((1024, 1536), Image.Resampling.LANCZOS)
    board.paste(action, (0, 0))
    side = Image.new("RGBA", (512, 1536), (8, 10, 18, 255))
    head.thumbnail((430, 600), Image.Resampling.LANCZOS)
    side.alpha_composite(head, ((512 - head.width) // 2, 90))
    d = ImageDraw.Draw(side)
    title = ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 30)
    small = ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 24)
    d.text((44, 740), "PAOLO BANCHERO FACE REFERENCE", font=title, fill=(250, 250, 255))
    d.text((44, 805), "Apply this face to the LEFT player only.", font=small, fill=(230, 238, 255))
    d.text((44, 850), "Keep the action scene. Remove this side panel.", font=small, fill=(255, 230, 230))
    d.text((44, 920), "Key traits:", font=small, fill=(250, 250, 255))
    d.text((44, 965), "- broad oval face", font=small, fill=(230, 238, 255))
    d.text((44, 1005), "- lighter brown skin", font=small, fill=(230, 238, 255))
    d.text((44, 1045), "- long thin braids", font=small, fill=(230, 238, 255))
    d.text((44, 1085), "- faint mustache and small chin goatee", font=small, fill=(230, 238, 255))
    board.paste(side.convert("RGB"), (1024, 0))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    board.save(OUT, quality=95)
    print(OUT)


if __name__ == "__main__":
    main()
