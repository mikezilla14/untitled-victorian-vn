#!/usr/bin/env python3
"""Promote non-canon day file to prod with time-period spine labels."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PROD_HEADER = """# day{day}.rpy
# Release 1 / Day {day_num:02d} — promoted runtime canon
# Spine: time-period routing via explicit day labels and dynamic windows
"""

SPINE_101 = """
# [DAG_NODE id=day101 type=time_period day=101 period=Morning]
label day101:
    jump day101_morning


# [DAG_NODE id=day101_morning type=time_period day=101 period=Morning]
label day101_morning:
    $ time_manager.set_current_day(1)
    $ set_time_period("Morning")
    jump day101_main


"""

SPINE_102 = """
# [DAG_NODE id=day102 type=time_period day=102 period=Morning]
label day102:
    jump day102_morning


# [DAG_NODE id=day102_morning type=time_period day=102 period=Morning]
label day102_morning:
    $ time_manager.set_current_day(2)
    $ set_time_period("Morning")
    jump day102_1_cora_missy_first_shift


"""


def strip_non_canon_header(text: str, day: int) -> str:
    """Remove non-canon promotion header block after FORMAT LEGEND."""
    pattern = re.compile(
        r"(# Full policy: docs/contracts/sprite_layout_policy\.yaml.*?\n)\n"
        r"# day\d+_non_canon\.rpy\n.*?"
        r"(# ={5,}\n# DAY \d+ NODE MAP)",
        re.DOTALL,
    )
    replacement = (
        r"\1\n"
        + PROD_HEADER.format(day=day, day_num=day % 100)
        + r"\n\2"
    )
    return pattern.sub(replacement, text, count=1)


def remove_day102_morning_init(text: str) -> str:
    """Drop duplicate day/time init from first morning scene (now on spine)."""
    return text.replace(
        "label day102_1_cora_missy_first_shift:\n\n"
        "    # [STATE] State/progression update\n"
        "    $ time_manager.set_current_day(2)\n"
        "    $ set_time_period(\"Morning\")\n\n"
        "    scene",
        "label day102_1_cora_missy_first_shift:\n\n"
        "    scene",
        1,
    )


def insert_spine(text: str, day: int) -> str:
    spine = {101: SPINE_101, 102: SPINE_102}[day]
    marker = f"# [DAG_NODE id=day{day}_main type=work day={day}]"
    if day == 102:
        marker = "# [DAG_NODE id=day102_1_cora_missy_first_shift type=work day=102]"
    if spine.strip() in text:
        return text
    return text.replace(marker, spine + marker, 1)


def promote(day: int) -> None:
    src = ROOT / "main-game" / "non-prod-game" / "game" / "days" / f"day{day}_non_canon.rpy"
    dst = ROOT / "main-game" / "prod-game" / "game" / f"day{day}.rpy"
    text = src.read_text(encoding="utf-8")
    text = strip_non_canon_header(text, day)
    text = insert_spine(text, day)
    if day == 102:
        text = remove_day102_morning_init(text)
    dst.write_text(text, encoding="utf-8")
    print(f"Promoted {src.name} -> {dst.relative_to(ROOT)}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("days", nargs="+", type=int)
    args = parser.parse_args()
    for day in args.days:
        promote(day)


if __name__ == "__main__":
    main()
