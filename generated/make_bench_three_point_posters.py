from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
MODULE_PATH = ROOT / "make_next_two_matchup_posters.py"
spec = importlib.util.spec_from_file_location("bench_three_workflow", MODULE_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("Cannot load workflow")
workflow = importlib.util.module_from_spec(spec)
sys.modules["bench_three_workflow"] = workflow
spec.loader.exec_module(workflow)

POSTER_DIR = ROOT / "playoff_matchup_posters"

workflow.RAW_DIR = POSTER_DIR / "raw_bench_three"
workflow.FINAL_DIR = POSTER_DIR / "final_bench_three"
workflow.REF_DIR = POSTER_DIR / "identity_refs_bench_three"

JOBS = [
    workflow.Job(
        slug="deuce_under_fire",
        title="DEUCE UNDER FIRE",
        left_name="MCBRIDE",
        right_name="DANIELS",
        left_team="NEW YORK KNICKS",
        right_team="ATLANTA HAWKS",
        top_label="BENCH SHOOTER  THREE-POINT CONTEST",
        left_ref=POSTER_DIR / "refs" / "miles_mcbride.png",
        right_ref=POSTER_DIR / "refs" / "dyson_daniels.png",
        left_traits="compact face, short hair, trimmed beard, strong guard frame, focused shooter expression",
        right_traits="long athletic face, short textured hair, lean defensive guard frame, intense contest expression",
        scene=(
            "Miles McBride rises into a high-arc three-point jumper above the arc while Dyson Daniels leaps forward "
            "with one arm fully extended to contest the shot, closeout pressure, shooter balanced in midair, defender flying past"
        ),
        left_color=(0, 107, 182),
        right_color=(225, 68, 52),
        accent=(245, 132, 38),
    ),
    workflow.Job(
        slug="green_light_contest",
        title="GREEN LIGHT CONTEST",
        left_name="PRITCHARD",
        right_name="GRIMES",
        left_team="BOSTON CELTICS",
        right_team="PHILADELPHIA 76ERS",
        top_label="BENCH SHOOTER  THREE-POINT CONTEST",
        left_ref=POSTER_DIR / "refs" / "payton_pritchard.png",
        right_ref=POSTER_DIR / "refs" / "quentin_grimes.png",
        left_traits="short light-brown hair, clean-shaven face, compact guard frame, confident shooter expression",
        right_traits="short dark hair, trimmed beard, strong wing guard frame, aggressive closeout expression",
        scene=(
            "Payton Pritchard pulls up for a deep catch-and-shoot three while Quentin Grimes jumps with a hard closeout, "
            "hand across the shooter's vision, ball just leaving fingertips, sideline bench reacting in the background"
        ),
        left_color=(0, 122, 51),
        right_color=(0, 107, 182),
        accent=(139, 111, 78),
    ),
    workflow.Job(
        slug="mile_high_release",
        title="MILE HIGH RELEASE",
        left_name="STRAWTHER",
        right_name="DOSUNMU",
        left_team="DENVER NUGGETS",
        right_team="MINNESOTA TIMBERWOLVES",
        top_label="BENCH SHOOTER  THREE-POINT CONTEST",
        left_ref=POSTER_DIR / "refs" / "julian_strawther.png",
        right_ref=POSTER_DIR / "refs" / "ayo_dosunmu.png",
        left_traits="young lean face, short curly hair, light facial hair, smooth wing shooter frame",
        right_traits="lean face, short hair, light beard, wiry defensive guard frame, explosive leaping closeout",
        scene=(
            "Julian Strawther elevates for a corner three-pointer while Ayo Dosunmu explodes into a jumping contest, "
            "arm stretched across the release point, ball leaving the shooter's hand, crowd rising behind the play"
        ),
        left_color=(13, 34, 64),
        right_color=(12, 35, 64),
        accent=(255, 198, 39),
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
