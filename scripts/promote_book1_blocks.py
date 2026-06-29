#!/usr/bin/env python3
"""Promote book1 chapter block files from non-prod days/ to prod game/."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NON_PROD_DAYS = ROOT / "main-game" / "non-prod-game" / "game" / "days"
PROD_GAME = ROOT / "main-game" / "prod-game" / "game"

PROMOTE_MAP = {
    "book1_day101_non_canon.rpy": "book1_day101.rpy",
    "book1_day104_non_canon.rpy": "book1_day104.rpy",
}


def promote_one(src_name: str, dst_name: str) -> None:
    src = NON_PROD_DAYS / src_name
    dst = PROD_GAME / dst_name
    text = src.read_text(encoding="utf-8")
    text = text.replace("_non_canon.rpy", ".rpy", 1)
    dst.write_text(text, encoding="utf-8")
    print(f"Promoted {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}")


def main() -> None:
    for src, dst in PROMOTE_MAP.items():
        promote_one(src, dst)


if __name__ == "__main__":
    main()
