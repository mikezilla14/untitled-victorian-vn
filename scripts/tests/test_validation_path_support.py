"""Regression tests for production and current non-production Ren'Py layouts."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest import mock


SCRIPTS = Path(__file__).resolve().parents[1]
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import engineering_compliance  # noqa: E402
import renpy_contract_linter  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
NON_PROD_GAME = ROOT / "main-game" / "non-prod-game" / "game"


class EngineeringCompliancePathTests(unittest.TestCase):
    def test_non_prod_variables_is_a_central_variables_file(self):
        relative = "main-game/non-prod-game/game/variables.rpy"
        absolute = str(NON_PROD_GAME / "variables.rpy")
        self.assertEqual(
            engineering_compliance.check_no_new_defaults_outside_variables(
                [relative, absolute]
            ),
            [],
        )


class RenPyContractPathTests(unittest.TestCase):
    def test_non_prod_day_is_discovered_from_relative_and_absolute_paths(self):
        relative = "main-game/non-prod-game/game/days/day100_non_canon.rpy"
        absolute = str(NON_PROD_GAME / "days" / "day100_non_canon.rpy")
        targets = renpy_contract_linter.changed_game_scripts([relative, absolute])
        self.assertEqual([path.resolve() for path in targets], [
            (ROOT / relative).resolve(),
            Path(absolute).resolve(),
        ])

    def test_non_prod_definitions_are_loaded_from_shared_layout(self):
        speakers = renpy_contract_linter.load_defined_speakers(NON_PROD_GAME)
        symbols = renpy_contract_linter.load_defined_symbols(NON_PROD_GAME)
        self.assertIn("cora", speakers)
        self.assertIn("PlayerStats", symbols)
        self.assertIn("suspicion_tier", symbols)
        self.assertIn("player", symbols)

    def test_python_and_renpy_builtins_are_not_false_positives(self):
        path = NON_PROD_GAME / "days" / "day199_non_canon.rpy"
        source = (
            'init python:\n'
            '    def local_helper():\n'
            '        return "ok"\n'
            'label day199_1_test_scene:\n'
            '    $ setattr(story, "example", local_helper())\n'
            '    nvl_narrator "Text"\n'
        )
        with mock.patch.object(renpy_contract_linter, "read_text", return_value=source):
            self.assertEqual(renpy_contract_linter.check_speakers([path]), [])
            self.assertEqual(
                renpy_contract_linter.check_callable_symbols([path]),
                [],
            )

    def test_advertised_interpolation_and_label_contracts_report_violations(self):
        path = NON_PROD_GAME / "days" / "day199_non_canon.rpy"
        source = (
            'label day199_bad:\n'
            '    menu:\n'
            '        "[Inspiration] Continue":\n'
            '            return\n'
        )
        with mock.patch.object(renpy_contract_linter, "read_text", return_value=source):
            self.assertTrue(
                renpy_contract_linter.check_bracket_interpolation([path])
            )
            self.assertTrue(renpy_contract_linter.check_label_naming([path]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
