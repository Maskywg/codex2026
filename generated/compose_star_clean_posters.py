from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
MODULE_PATH = ROOT / "compose_clean_matchup_posters.py"
spec = importlib.util.spec_from_file_location("clean_composer", MODULE_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("Cannot load clean composer")
clean = importlib.util.module_from_spec(spec)
sys.modules["clean_composer"] = clean
spec.loader.exec_module(clean)

POSTER_DIR = ROOT / "playoff_matchup_posters"

POSTERS = [
    clean.Poster(
        "franchise_fire_identity_action_clean",
        clean.latest("raw_identity", "franchise_fire_identity_action_*.png"),
        "FRANCHISE FIRE",
        "BANCHERO",
        "CUNNINGHAM",
        "ORLANDO MAGIC",
        "DETROIT PISTONS",
        "EAST FIRST ROUND  GAME 5",
        (18, 92, 255),
        (226, 35, 48),
        (112, 166, 255),
    ),
    clean.Poster(
        "northern_pressure_identity_action_clean",
        clean.latest("raw_identity", "northern_pressure_identity_action_*.png"),
        "NORTHERN PRESSURE",
        "BARNES",
        "MITCHELL",
        "TORONTO RAPTORS",
        "CLEVELAND CAVALIERS",
        "EAST FIRST ROUND  GAME 5",
        (206, 17, 65),
        (111, 38, 61),
        (255, 206, 84),
    ),
    clean.Poster(
        "legends_at_war_identity_action_clean",
        clean.latest("raw_identity", "legends_at_war_identity_action_*.png"),
        "LEGENDS AT WAR",
        "DURANT",
        "LEBRON",
        "HOUSTON ROCKETS",
        "LOS ANGELES LAKERS",
        "WEST FIRST ROUND  GAME 5",
        (206, 17, 65),
        (85, 37, 130),
        (253, 185, 39),
    ),
]


def main() -> None:
    for poster in POSTERS:
        print(clean.compose(poster))


if __name__ == "__main__":
    main()
