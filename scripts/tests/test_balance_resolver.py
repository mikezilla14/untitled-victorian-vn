"""Unit tests for scripts/balance_resolver.py."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1]
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import balance_resolver  # noqa: E402


class BalanceResolverTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config = balance_resolver.load_profiles()

    def test_submissive_standard(self) -> None:
        result = balance_resolver.resolve_balanced_effect(
            "submissive",
            intensity_override="standard",
            config=self.config,
        )
        self.assertEqual(result, {"corr": 5, "insp": 5})

    def test_submissive_major_scales_whole_profile(self) -> None:
        result = balance_resolver.resolve_balanced_effect(
            "submissive",
            intensity_override="major",
            config=self.config,
        )
        self.assertEqual(result, {"corr": 8, "insp": 8})

    def test_submissive_minor_scales_down(self) -> None:
        result = balance_resolver.resolve_balanced_effect(
            "submissive",
            intensity_override="minor",
            config=self.config,
        )
        self.assertEqual(result, {"corr": 2, "insp": 2})

    def test_defiant_requires_witness(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            balance_resolver.resolve_balanced_effect(
                "defiant",
                intensity_override="standard",
                config=self.config,
            )
        self.assertIn("requires a named witness", str(ctx.exception))

    def test_defiant_standard_with_stern(self) -> None:
        result = balance_resolver.resolve_balanced_effect(
            "defiant",
            intensity_override="standard",
            witness="stern",
            config=self.config,
        )
        self.assertEqual(result, {"insp": 12, "stern_susp": 10})

    def test_deceptive_base_witness(self) -> None:
        result = balance_resolver.resolve_balanced_effect(
            "deceptive",
            witness="stern",
            base_witness=True,
            config=self.config,
        )
        self.assertEqual(result, {"insp": 5, "stern_base": 25})

    def test_unknown_profile(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            balance_resolver.resolve_balanced_effect("submisive", config=self.config)
        self.assertIn("Unknown balance profile", str(ctx.exception))

    def test_unknown_intensity(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            balance_resolver.resolve_balanced_effect(
                "submissive",
                intensity_override="medium",
                config=self.config,
            )
        self.assertIn("Unknown balance intensity override", str(ctx.exception))

    def test_unknown_witness(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            balance_resolver.resolve_balanced_effect(
                "defiant",
                witness="john",
                config=self.config,
            )
        self.assertIn("Unknown witness", str(ctx.exception))

    def test_numeric_intensity_multiplier(self) -> None:
        result = balance_resolver.resolve_balanced_effect(
            "observant",
            intensity_override=0.5,
            config=self.config,
        )
        self.assertEqual(result, {"insp": 2})

    def test_safe_trace(self) -> None:
        result = balance_resolver.resolve_balanced_effect("safe", config=self.config)
        self.assertEqual(result, {"insp": 2})

    def test_reckless_with_vance(self) -> None:
        result = balance_resolver.resolve_balanced_effect(
            "reckless",
            intensity_override="standard",
            witness="vance",
            config=self.config,
        )
        self.assertEqual(result, {"corr": 8, "insp": 12, "vance_susp": 25})


if __name__ == "__main__":
    unittest.main()
