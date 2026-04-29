from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
MODULE_PATH = ROOT / "make_next_two_matchup_posters.py"
spec = importlib.util.spec_from_file_location("next_two", MODULE_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("Cannot load next-two workflow")
workflow = importlib.util.module_from_spec(spec)
sys.modules["next_two"] = workflow
spec.loader.exec_module(workflow)


POSTER_DIR = ROOT / "playoff_matchup_posters"

JOBS = [
    workflow.Job(
        slug="low_post_collision",
        title="LOW POST COLLISION",
        left_name="SENGUN",
        right_name="AYTON",
        left_team="HOUSTON ROCKETS",
        right_team="LOS ANGELES LAKERS",
        top_label="CENTER MATCHUP  DUNK VS BLOCK",
        left_ref=POSTER_DIR / "refs" / "alperen_sengun.png",
        right_ref=POSTER_DIR / "refs" / "deandre_ayton.png",
        left_traits="oval face, short dark hair, full short beard, strong skilled center frame",
        right_traits="long face, short hair, trimmed beard, tall powerful rim-protector frame",
        scene=(
            "Alperen Sengun spins into the lane and rises for a powerful dunk while Deandre Ayton explodes upward "
            "to block the shot at the rim, backboard and rim visible, bodies colliding in midair, paint-area impact"
        ),
        left_color=(206, 17, 65),
        right_color=(85, 37, 130),
        accent=(253, 185, 39),
    ),
    workflow.Job(
        slug="spark_plug_showdown",
        title="SPARK PLUG SHOWDOWN",
        left_name="SHEPPARD",
        right_name="REAVES",
        left_team="HOUSTON ROCKETS",
        right_team="LOS ANGELES LAKERS",
        top_label="BENCH MOB  HARDCORE PLAY",
        left_ref=POSTER_DIR / "refs" / "reed_sheppard.png",
        right_ref=POSTER_DIR / "refs" / "austin_reaves.png",
        left_traits="young narrow face, short light-brown hair, clean-shaven guard look, compact quick frame",
        right_traits="lean face, shaggy light-brown hair, light stubble, wiry competitive guard frame",
        scene=(
            "Reed Sheppard and Austin Reaves dive across the hardwood for a loose ball, both stretched low with "
            "hands reaching, one player sliding on his chest while the other claws for possession, gritty 50-50 ball scramble"
        ),
        left_color=(206, 17, 65),
        right_color=(85, 37, 130),
        accent=(253, 185, 39),
    ),
]


def main() -> None:
    finals = []
    for job in JOBS:
        ref = workflow.make_reference_board(job)
        raw = workflow.generate_action(job, ref)
        finals.append(workflow.compose(job, raw))
    print("FINAL")
    for path in finals:
        print(path)


if __name__ == "__main__":
    main()
