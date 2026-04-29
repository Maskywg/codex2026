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
        slug="rim_lockdown",
        title="RIM LOCKDOWN",
        left_name="POELTL",
        right_name="ALLEN",
        left_team="TORONTO RAPTORS",
        right_team="CLEVELAND CAVALIERS",
        top_label="CENTER MATCHUP  DUNK VS BLOCK",
        left_ref=POSTER_DIR / "refs" / "jakob_poeltl.png",
        right_ref=POSTER_DIR / "refs" / "jarrett_allen.png",
        left_traits="long face, short brown hair, clean-shaven or very light stubble, tall solid center frame",
        right_traits="long narrow face, full afro hair, trimmed beard, long athletic rim-protector frame",
        scene=(
            "Jakob Poeltl rolls hard to the rim for a two-hand dunk while Jarrett Allen launches upward "
            "with both arms extended to block the shot, bodies meeting above the restricted area, backboard and rim visible"
        ),
        left_color=(206, 17, 65),
        right_color=(111, 38, 61),
        accent=(255, 206, 84),
    ),
    workflow.Job(
        slug="bench_heat_check",
        title="BENCH HEAT CHECK",
        left_name="DICK",
        right_name="MERRILL",
        left_team="TORONTO RAPTORS",
        right_team="CLEVELAND CAVALIERS",
        top_label="BENCH MOB  HARDCORE PLAY",
        left_ref=POSTER_DIR / "refs" / "gradey_dick.png",
        right_ref=POSTER_DIR / "refs" / "sam_merrill.png",
        left_traits="young lean face, short light hair, clean-shaven wing frame",
        right_traits="mature lean face, short brown hair, trimmed beard, wiry shooter guard frame",
        scene=(
            "Gradey Dick and Sam Merrill dive into a gritty loose-ball scramble near the sideline, both players "
            "low to the hardwood with arms stretched for the ball, one sliding forward while the other rips for possession"
        ),
        left_color=(206, 17, 65),
        right_color=(111, 38, 61),
        accent=(255, 206, 84),
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
