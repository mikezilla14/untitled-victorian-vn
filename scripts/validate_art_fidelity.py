#!/usr/bin/env python3
"""
Art-Narrative Fidelity Contract Linter (stdlib only).
Validates character visual asset cards and narrative documents against the visual contract.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_contract() -> dict[str, dict[str, list[str]]]:
    path = ROOT / "docs" / "contracts" / "art_fidelity_contract.json"
    if not path.exists():
        print(f"[ERROR] Fidelity contract database missing: {path.as_posix()}")
        sys.exit(1)
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] Failed to load fidelity contract: {e}")
        sys.exit(1)


def check_character_card(char_id: str, contract: dict[str, list[str]]) -> list[str]:
    errors = []
    card_path = ROOT / "assets_source" / "character_cards" / f"{char_id}.md"
    if not card_path.exists():
        errors.append(f"Missing active character card: assets_source/character_cards/{char_id}.md")
        return errors

    content = card_path.read_text(encoding="utf-8")
    
    # Parse out frontmatter and body
    parts = content.split("---", 2)
    frontmatter = ""
    body = ""
    if len(parts) >= 3:
        frontmatter = parts[1]
        body = parts[2]
    else:
        body = content

    # Clean frontmatter for scanning: ignore metadata keys containing the forbidden words themselves
    frontmatter_lines = []
    for line in frontmatter.splitlines():
        if not line.strip():
            continue
        if any(line.strip().startswith(prefix) for prefix in ["forbidden_contradictions:", "negative_prompt_notes:"]):
            continue
        frontmatter_lines.append(line)

    searchable_content = "\n".join(frontmatter_lines) + "\n" + body
    searchable_content_lower = searchable_content.lower()

    # Verify at least one match for required attributes
    for category in ["hair", "eyes", "skin", "clothing"]:
        tokens = contract[category]
        if not any(token.lower() in searchable_content_lower for token in tokens):
            errors.append(
                f"assets_source/character_cards/{char_id}.md does not contain any matching token for required {category}: {tokens}"
            )

    # Verify no forbidden contradictions
    for forbidden in contract["forbidden_contradictions"]:
        if re.search(r'\b' + re.escape(forbidden.lower()) + r'\b', searchable_content_lower):
            errors.append(
                f"assets_source/character_cards/{char_id}.md contains forbidden visual contradiction token: {forbidden!r}"
            )

    return errors


def check_narrative_canon(char_id: str, contract: dict[str, list[str]]) -> list[str]:
    errors = []
    canon_path = ROOT / "main-game" / "canon" / f"{char_id}_character_canon.md"
    if not canon_path.exists():
        # Fallback to check if characters_canon.md exists but individual doesn't
        return errors

    content = canon_path.read_text(encoding="utf-8")
    content_lower = content.lower()

    # Check for forbidden visual contradictions in character canon file
    for forbidden in contract["forbidden_contradictions"]:
        # Find matches with word boundaries to avoid partial substring hits
        pattern = r'\b' + re.escape(forbidden.lower()) + r'\b'
        matches = list(re.finditer(pattern, content_lower))
        if matches:
            for match in matches:
                # Find line number
                line_no = content[:match.start()].count("\n") + 1
                errors.append(
                    f"main-game/canon/{char_id}_character_canon.md:{line_no} contains forbidden visual contradiction token: {forbidden!r}"
                )

    return errors


def check_draft_scripts(char_id: str, contract: dict[str, list[str]]) -> list[str]:
    errors = []
    drafts_dir = ROOT / "main-game" / "draft"
    if not drafts_dir.exists():
        return errors

    # Check for draft Ren'Py files
    for rpy_path in drafts_dir.rglob("*.rpy"):
        content = rpy_path.read_text(encoding="utf-8")
        rel_path = rpy_path.relative_to(ROOT).as_posix()
        
        # We look for references to character dialogue speaker or custom actions
        # and see if forbidden tokens appear in close proximity or overall context
        lines = content.splitlines()
        for idx, line in enumerate(lines):
            line_lower = line.lower()
            
            # Simple check: if character name is in the line (either as speaker or mentioned)
            # and it contains a forbidden contradiction for that character, throw a warning/error
            if char_id in line_lower:
                for forbidden in contract["forbidden_contradictions"]:
                    if re.search(r'\b' + re.escape(forbidden.lower()) + r'\b', line_lower):
                        errors.append(
                            f"{rel_path}:{idx + 1} reference to character {char_id!r} contains forbidden visual contradiction: {forbidden!r}"
                        )
                        
    return errors


def main() -> int:
    print("Running Art-Narrative Fidelity Contract Audit...\n")
    contracts = load_contract()
    failures = 0

    for char_id, contract in contracts.items():
        print(f"Checking visual continuity contract for character: {char_id}")
        
        card_errors = check_character_card(char_id, contract)
        if card_errors:
            failures += len(card_errors)
            for e in card_errors:
                print(f"  [ERROR] {e}")
        else:
            print("  [OK] Character Visual Card")

        canon_errors = check_narrative_canon(char_id, contract)
        if canon_errors:
            failures += len(canon_errors)
            for e in canon_errors:
                print(f"  [ERROR] {e}")
        else:
            print("  [OK] Canonical Profile")

        script_errors = check_draft_scripts(char_id, contract)
        if script_errors:
            failures += len(script_errors)
            for e in script_errors:
                print(f"  [ERROR] {e}")
        else:
            print("  [OK] Draft Scripts")
            
        print()

    if failures:
        print(f"Fidelity Audit FAILED with {failures} contract error(s).")
        return 1
    
    print("Fidelity Audit PASSED. All active assets and narratives are aligned.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
