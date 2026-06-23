"""Tests for scripts/balance_catalogue.py."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import balance_catalogue  # noqa: E402
import balance_resolver  # noqa: E402


class BalanceCatalogueTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config = balance_resolver.load_profiles()

    def test_parse_balanced_effect_line(self) -> None:
        effect = balance_catalogue.parse_balanced_effect_line(
            '$ apply_balanced_effect("curious", intensity="standard", witness="stern")'
        )
        self.assertIsNotNone(effect)
        assert effect is not None
        self.assertEqual(effect.profile, "curious")
        self.assertEqual(effect.witness, "stern")

    def test_effect_to_catalogue_columns_profile(self) -> None:
        effect = balance_catalogue.ExtractedEffect(
            kind="profile",
            profile="curious",
            intensity="standard",
            witness="stern",
        )
        cols = balance_catalogue.effect_to_catalogue_columns(effect, config=self.config)
        self.assertEqual(cols["effect_profile"], "curious")
        self.assertEqual(cols["effect_resolved_from_profile"], "true")
        self.assertEqual(cols["insp_delta"], "3")
        self.assertEqual(cols["corr_xp_delta"], "6")
        self.assertEqual(cols["stern_susp_delta"], "10")

    def test_validate_catalogue_row_pass(self) -> None:
        effect = balance_catalogue.ExtractedEffect(
            kind="profile",
            profile="curious",
            intensity="standard",
            witness="stern",
        )
        row = {
            "choice_id": "test",
            **balance_catalogue.effect_to_catalogue_columns(effect, config=self.config),
            "effect_resolved_from_profile": "true",
        }
        self.assertEqual(balance_catalogue.validate_catalogue_row(row, config=self.config), [])

    def test_extract_effect_stops_at_sibling_menu_option(self) -> None:
        lines = [
            '        "Careful choice":',
            "            $ story.set_flag()",
            '        "Eager choice":',
            '            $ apply_balanced_effect("observant", intensity="standard")',
        ]
        effect = balance_catalogue.extract_effect_near_line(lines, 1)
        self.assertEqual(effect.kind, "none")

    def test_validate_catalogue_row_fail_mismatch(self) -> None:
        row = {
            "choice_id": "test",
            "effect_profile": "curious",
            "effect_intensity": "standard",
            "effect_witness": "stern",
            "effect_base_witness": "false",
            "effect_resolved_from_profile": "true",
            "insp_delta": "99",
            "corr_xp_delta": "6",
            "stern_susp_delta": "10",
        }
        errors = balance_catalogue.validate_catalogue_row(row, config=self.config)
        self.assertTrue(any("insp_delta mismatch" in err for err in errors))


if __name__ == "__main__":
    unittest.main()
