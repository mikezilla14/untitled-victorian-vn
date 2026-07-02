"""Tests for Book1 writing contract validation."""

from __future__ import annotations

import json
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from contract_schemas import validate_book_writing_context  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
EXAMPLE = ROOT / "docs/contracts/examples/book_writing_context.example.json"


def test_example_book_writing_context_is_valid() -> None:
    data = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    assert validate_book_writing_context(data) == []


def test_book_writing_context_requires_approved_images() -> None:
    data = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    data["approved_images"] = []
    errors = validate_book_writing_context(data)
    assert any("approved_images" in err for err in errors)


def test_book_import_header_validates() -> None:
    data = {
        "contract_version": "1",
        "kind": "book_import_header",
        "target_file": "main-game/non-prod-game/game/days/book1_day101_non_canon.rpy",
        "target_label": "book1_block_day1_alt_predator_core",
        "target_chapter": "day1_chapter",
        "target_archetype": "predator",
        "generation_mode": "multi_branch_code",
    }
    assert validate_book_writing_context(data) == []
