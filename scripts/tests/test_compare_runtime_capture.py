"""Tests for compare_runtime_to_model capture validation."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "main-game" / "pipeline" / "tools"
SCRIPTS = ROOT / "scripts"
for path in (str(TOOLS), str(SCRIPTS)):
    if path not in sys.path:
        sys.path.insert(0, path)

import balance_resolver  # noqa: E402
from compare_runtime_to_model import (  # noqa: E402
    ROLLBACK_CONTAMINATED,
    RESOLVER_MISMATCH,
    summarize_capture,
    validate_balanced_effect_events,
)


class CompareRuntimeCaptureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config = balance_resolver.load_profiles()

    def _balanced_event(self, **overrides) -> dict:
        kwargs = balance_resolver.resolve_balanced_effect(
            "curious",
            intensity_override="standard",
            witness="stern",
            config=self.config,
        )
        event = {
            "seq": 3,
            "event": "balanced_effect",
            "profile": "curious",
            "intensity": "standard",
            "witness": "stern",
            "base_witness": False,
            "resolved_kwargs": kwargs,
            "success": True,
        }
        event.update(overrides)
        return event

    def _base_events(self) -> list[dict]:
        return [
            {"seq": 1, "event": "run_start", "snapshot": {}},
            {"seq": 2, "event": "grain_enter", "label": "day101_main", "snapshot": {}},
            self._balanced_event(),
            {"seq": 4, "event": "choice", "snapshot": {}},
            {"seq": 5, "event": "gate", "snapshot": {}},
            {"seq": 6, "event": "run_end", "contains_rollback": False, "snapshot": {}},
        ]

    def test_validate_balanced_effect_passes(self) -> None:
        events = [self._balanced_event()]
        self.assertEqual(validate_balanced_effect_events(events, config=self.config), [])

    def test_validate_balanced_effect_mismatch(self) -> None:
        events = [self._balanced_event(resolved_kwargs={"insp": 99, "corr": 5})]
        errors = validate_balanced_effect_events(events, config=self.config)
        self.assertTrue(errors)

    def test_summarize_capture_balance_proof_valid(self) -> None:
        summary = summarize_capture("test", self._base_events(), config=self.config)
        self.assertTrue(summary["balance_proof_valid"])
        self.assertEqual(summary["balanced_effect_count"], 1)
        self.assertEqual(summary["balance_proof_blockers"], [])

    def test_summarize_capture_rejects_rollback(self) -> None:
        events = self._base_events()
        events.insert(-1, {"seq": 5, "event": "rollback_event", "snapshot": {}})
        events[-1]["seq"] = 7
        summary = summarize_capture("test", events, config=self.config)
        self.assertFalse(summary["balance_proof_valid"])
        self.assertIn(ROLLBACK_CONTAMINATED, summary["balance_proof_blockers"])

    def test_summarize_capture_rejects_resolver_mismatch(self) -> None:
        events = self._base_events()
        events[2] = self._balanced_event(resolved_kwargs={"insp": 99, "corr": 5})
        summary = summarize_capture("test", events, config=self.config)
        self.assertFalse(summary["balance_proof_valid"])
        self.assertIn(RESOLVER_MISMATCH, summary["balance_proof_blockers"])


if __name__ == "__main__":
    unittest.main()
