"""Tests for daily standup (live checks only — no stale errors.txt)."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1]
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import daily_standup  # noqa: E402
import standup_checks  # noqa: E402
from standup_checks import CheckResult  # noqa: E402


class DailyStandupReportTests(unittest.TestCase):
    def test_report_uses_action_queue_not_specialist_grades(self):
        checks = [
            CheckResult("renpy_contract", "Ren'Py contract lint (non-prod)", "pass", "ok"),
            CheckResult("historical_linter", "Historical linter", "fail", "1 file", details=["a.rpy"]),
        ]
        report = daily_standup.build_daily_report(
            daily_standup.DEFAULT_SCHEDULE,
            __import__("datetime").date(2026, 6, 29),
            checks,
            use_color=False,
        )
        self.assertIn("ACTION QUEUE", report)
        self.assertIn("AUTOMATED CHECKS", report)
        self.assertNotIn("Adult Market Reviewer", report)
        self.assertNotIn("PROJECT INTEGRITY GRADES", report)
        self.assertNotIn("errors.txt", report)

    def test_build_action_items_for_historical_failure(self):
        checks = [
            CheckResult(
                "historical_linter",
                "Historical linter",
                "fail",
                "1 file",
                details=["main-game/non-prod-game/game/shared/story_chains_non_canon.rpy"],
            )
        ]
        items = daily_standup.build_action_items(checks)
        self.assertEqual(len(items), 1)
        self.assertIn("historical_linter.py", items[0][2])


class StaleErrorsTxtTests(unittest.TestCase):
    def test_run_all_daily_checks_does_not_read_errors_txt(self):
        errors_path = Path(__file__).resolve().parents[2] / "main-game" / "non-prod-game" / "errors.txt"
        fake_error = (
            'File "game/shared/journal_screen.rpy", line 26: stale fake error\n'
        )

        with mock.patch.object(
            standup_checks, "run_renpy_contract_check", return_value=CheckResult("renpy_contract", "x", "pass", "ok")
        ), mock.patch.object(
            standup_checks, "run_engineering_compliance", return_value=CheckResult("engineering_compliance", "x", "pass", "ok")
        ), mock.patch.object(
            standup_checks, "run_scene_direction_check", return_value=CheckResult("scene_direction", "x", "pass", "ok")
        ), mock.patch.object(
            standup_checks, "run_formatting_check", return_value=CheckResult("format_non_canon", "x", "pass", "ok")
        ), mock.patch.object(
            standup_checks, "run_historical_check", return_value=CheckResult("historical_linter", "x", "pass", "ok")
        ), mock.patch.object(
            standup_checks, "audit_non_prod_assets_on_disk", return_value=CheckResult("asset_disk", "x", "pass", "ok")
        ), mock.patch.object(
            standup_checks, "run_renpy_lint_optional", return_value=CheckResult("renpy_lint", "x", "skip", "skipped")
        ):
            if errors_path.exists():
                original = errors_path.read_text(encoding="utf-8")
                errors_path.write_text(fake_error, encoding="utf-8")
                try:
                    results = standup_checks.run_all_daily_checks()
                finally:
                    errors_path.write_text(original, encoding="utf-8")
            else:
                results = standup_checks.run_all_daily_checks()

        for r in results:
            self.assertNotIn("stale fake error", r.summary)


if __name__ == "__main__":
    unittest.main()
