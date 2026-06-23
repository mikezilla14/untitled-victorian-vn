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

    def test_creative_standard(self) -> None:
        result = balance_resolver.resolve_balanced_effect(
            "creative",
            intensity_override="standard",
            config=self.config,
        )
        self.assertEqual(result, {"insp": 5, "corr": 3})

    def test_curious_standard_with_witness(self) -> None:
        result = balance_resolver.resolve_balanced_effect(
            "curious",
            intensity_override="standard",
            witness="stern",
            config=self.config,
        )
        self.assertEqual(result, {"insp": 3, "corr": 6, "stern_susp": 10})

    def test_transgressive_major_with_witness(self) -> None:
        result = balance_resolver.resolve_balanced_effect(
            "transgressive",
            intensity_override="major",
            witness="vance",
            config=self.config,
        )
        self.assertEqual(result, {"corr": 24, "vance_susp": 25})

    def test_observant_standard(self) -> None:
        result = balance_resolver.resolve_balanced_effect(
            "observant",
            intensity_override="standard",
            config=self.config,
        )
        self.assertEqual(result, {"insp": 2})

    def test_deceptive_standard_with_witness(self) -> None:
        result = balance_resolver.resolve_balanced_effect(
            "deceptive",
            intensity_override="standard",
            witness="missy",
            config=self.config,
        )
        self.assertEqual(result, {"corr": 8, "missy_susp": 10})

    def test_safe_is_inactive(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            balance_resolver.resolve_balanced_effect("safe", config=self.config)
        self.assertIn("is inactive", str(ctx.exception))

    def test_obedient_is_inactive(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            balance_resolver.resolve_balanced_effect("obedient", config=self.config)
        self.assertIn("is inactive", str(ctx.exception))

    def test_reckless_is_inactive(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            balance_resolver.resolve_balanced_effect("reckless", config=self.config)
        self.assertIn("is inactive", str(ctx.exception))

    def test_trace_intensity_is_invalid(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            balance_resolver.resolve_balanced_effect("creative", intensity_override="trace", config=self.config)
        self.assertIn("Inactive or unknown intensity", str(ctx.exception))

    def test_severe_intensity_is_invalid(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            balance_resolver.resolve_balanced_effect("creative", intensity_override="severe", config=self.config)
        self.assertIn("Inactive or unknown intensity", str(ctx.exception))

    def test_numeric_intensity_is_invalid(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            balance_resolver.resolve_balanced_effect("creative", intensity_override=0.5, config=self.config)
        self.assertIn("Numeric intensity override not supported", str(ctx.exception))

    def test_unknown_witness_fails(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            balance_resolver.resolve_balanced_effect("curious", witness="john", config=self.config)
        self.assertIn("Unknown witness", str(ctx.exception))

    def test_curious_without_witness_fails(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            balance_resolver.resolve_balanced_effect("curious", config=self.config)
        self.assertIn("requires a named witness parameter", str(ctx.exception))

    def test_transgressive_without_witness_fails(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            balance_resolver.resolve_balanced_effect("transgressive", config=self.config)
        self.assertIn("requires a named witness parameter", str(ctx.exception))

    def test_deceptive_without_witness_fails(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            balance_resolver.resolve_balanced_effect("deceptive", config=self.config)
        self.assertIn("requires a named witness parameter", str(ctx.exception))

    def test_base_witness_fails_for_active_profiles(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            balance_resolver.resolve_balanced_effect(
                "curious",
                witness="stern",
                base_witness=True,
                config=self.config,
            )
        self.assertIn("base_witness=True is not allowed", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
