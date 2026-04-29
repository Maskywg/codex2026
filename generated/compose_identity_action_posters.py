from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
MODULE_PATH = ROOT / "make_three_matchup_posters.py"
spec = importlib.util.spec_from_file_location("matchup_posters", MODULE_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("Cannot load poster composer")
composer = importlib.util.module_from_spec(spec)
sys.modules["matchup_posters"] = composer
spec.loader.exec_module(composer)

FINAL = ROOT / "playoff_matchup_posters" / "final_identity_action"
RAW = ROOT / "playoff_matchup_posters" / "raw_identity"


def latest(prefix: str) -> Path:
    paths = sorted(RAW.glob(f"{prefix}_*.png"))
    if not paths:
        raise FileNotFoundError(prefix)
    return paths[-1]


MATCHUPS = [
    composer.Matchup(
        slug="franchise_fire_identity_action",
        title="FRANCHISE FIRE",
        left_name="BANCHERO",
        right_name="CUNNINGHAM",
        left_team="ORLANDO MAGIC",
        right_team="DETROIT PISTONS",
        top_label="EAST FIRST ROUND  GAME 5",
        left_color=(18, 92, 255),
        right_color=(226, 35, 48),
        accent=(112, 166, 255),
    ),
    composer.Matchup(
        slug="northern_pressure_identity_action",
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
    composer.Matchup(
        slug="legends_at_war_identity_action",
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


def main() -> None:
    FINAL.mkdir(parents=True, exist_ok=True)
    for matchup in MATCHUPS:
        raw = latest(matchup.slug)
        print(composer.compose(raw, matchup))
        out = ROOT / "playoff_matchup_posters" / "final" / f"{matchup.slug}_poster.png"
        if out.exists():
            target = FINAL / f"{matchup.slug}.png"
            out.replace(target)
            print(target)


if __name__ == "__main__":
    main()
