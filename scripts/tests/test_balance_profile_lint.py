"""Tests for scripts/validation/balance_profile_lint.py."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import balance_resolver  # noqa: E402
from validation.balance_profile_lint import (  # noqa: E402
    is_balance_lint_target,
    lint_file,
    BalanceProfileLintResult,
)


class BalanceProfileLintTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config = balance_resolver.load_profiles()

    def test_is_balance_lint_target_day_script(self) -> None:
        path = Path("main-game/non-prod-game/game/days/day101_non_canon.rpy")
        self.assertTrue(is_balance_lint_target(path))
        self.assertFalse(is_balance_lint_target(Path("main-game/non-prod-game/game/shared/functions_non_canon.rpy")))

        path_chains = Path("main-game/non-prod-game/game/shared/story_chains_non_canon.rpy")
        self.assertTrue(is_balance_lint_target(path_chains))

    def test_valid_profile_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "day101_non_canon.rpy"
            path.write_text(
                '$ apply_balanced_effect("curious", intensity="standard", witness="stern")\n',
                encoding="utf-8",
            )
            result = lint_file(path, config=self.config, root=Path(tmp))
            self.assertEqual(result.profile_calls, 1)
            self.assertEqual(result.failures, [])
            self.assertEqual(result.warnings, [])

    def test_unknown_profile_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "day101_non_canon.rpy"
            path.write_text('$ apply_balanced_effect("not_a_profile")\n', encoding="utf-8")
            result = lint_file(path, config=self.config, root=Path(tmp))
            self.assertEqual(result.profile_calls, 1)
            self.assertTrue(any("unknown balance profile" in item for item in result.failures))

    def test_inactive_profile_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "day101_non_canon.rpy"
            path.write_text('$ apply_balanced_effect("submissive", intensity="standard")\n', encoding="utf-8")
            result = lint_file(path, config=self.config, root=Path(tmp))
            self.assertTrue(any("inactive balance profile" in item for item in result.failures))

    def test_witness_required_profile_fails_without_witness(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "day101_non_canon.rpy"
            path.write_text('$ apply_balanced_effect("curious", intensity="standard")\n', encoding="utf-8")
            result = lint_file(path, config=self.config, root=Path(tmp))
            self.assertTrue(any("requires a witness" in item for item in result.failures))

    def test_unmarked_apply_effects_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "day101_non_canon.rpy"
            path.write_text("$ apply_effects(insp=5, corr=0)\n", encoding="utf-8")
            result = lint_file(path, config=self.config, root=Path(tmp))
            self.assertEqual(result.unmarked_apply_effects, 1)
            self.assertTrue(any("without strict `# [STATE bespoke: <reason>]`" in item for item in result.failures))

    def test_strict_bespoke_marker_accepted(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "day101_non_canon.rpy"
            path.write_text(
                "# [STATE bespoke: negative_suspicion]\n$ apply_effects(stern_susp=-10)\n",
                encoding="utf-8",
            )
            result = lint_file(path, config=self.config, root=Path(tmp))
            self.assertEqual(result.bespoke_calls, 1)
            self.assertEqual(result.failures, [])

    def test_strict_bespoke_marker_invalid_kwargs_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "day101_non_canon.rpy"
            path.write_text(
                "# [STATE bespoke: negative_suspicion]\n$ apply_effects(stern_susp=-10, insp=5)\n",
                encoding="utf-8",
            )
            result = lint_file(path, config=self.config, root=Path(tmp))
            self.assertEqual(result.bespoke_calls, 1)
            self.assertTrue(any("negative_suspicion cannot modify 'insp'" in item for item in result.failures))

    def test_direct_player_mutation_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "day101_non_canon.rpy"
            path.write_text("$ player.stern_acute_susp = 5\n", encoding="utf-8")
            result = lint_file(path, config=self.config, root=Path(tmp))
            self.assertEqual(result.direct_mutations, 1)
            self.assertTrue(result.failures)


if __name__ == "__main__":
    unittest.main()
