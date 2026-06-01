#!/usr/bin/env python3
"""Tests for scripts/scene_direction.py (stdlib unittest; run with `py`).

    py scripts/tests/test_scene_direction.py
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import scene_direction as sd  # noqa: E402

# A registry mirroring characters.rpy so tests don't depend on file layout.
REGISTRY = {
    "cora": {"policy": "Cora", "tag": "cora_sprite"},
    "gideon": {"policy": "Gideon", "tag": "gideon_sprite"},
    "stern": {"policy": "Stern", "tag": "stern_sprite"},
    "vance": {"policy": "Vance", "tag": "vance_sprite"},
    "missy": {"policy": "Missy", "tag": "missy_sprite"},
}

POLICY = sd.load_policy()


def director():
    return sd.SceneDirector(POLICY, REGISTRY)


def run(text: str) -> str:
    d = director()
    lines = text.splitlines()
    return "\n".join(d.process_file(lines))


class ResolverTests(unittest.TestCase):
    def setUp(self):
        self.r = sd.LayoutResolver(POLICY)

    def test_single_character_centre(self):
        self.assertEqual(self.r.resolve(["Cora"]), {"Cora": "centre_bust"})
        self.assertEqual(self.r.resolve(["Gideon"]), {"Gideon": "centre_bust"})

    def test_cora_missy_alone(self):
        self.assertEqual(
            self.r.resolve(["Missy", "Cora"]),
            {"Cora": "left_bust", "Missy": "right_bust"},
        )

    def test_vance_gideon_two(self):
        self.assertEqual(
            self.r.resolve(["Gideon", "Vance"]),
            {"Vance": "left_bust", "Gideon": "right_bust"},
        )

    def test_cora_left_of_stern_two(self):
        # Not in canonical_layouts; Cora must sit left of Stern (project rule).
        self.assertEqual(
            self.r.resolve(["Cora", "Stern"]),
            {"Cora": "left_bust", "Stern": "right_bust"},
        )

    def test_cora_left_of_stern_three(self):
        # Cora+Stern+Missy is not canonical; Cora must still be left of Stern.
        res = self.r.resolve(["Cora", "Stern", "Missy"])
        order = self.r.slot_sets[3]
        self.assertLess(order.index(res["Cora"]), order.index(res["Stern"]))

    def test_cora_left_of_stern_canonical_three(self):
        # Canonical 3-person Cora+Stern combos already keep Cora left of Stern.
        for third in ("Vance", "Gideon"):
            res = self.r.resolve(["Cora", "Stern", third])
            order = self.r.slot_sets[3]
            self.assertLess(order.index(res["Cora"]), order.index(res["Stern"]))

    def test_four_canonical(self):
        self.assertEqual(
            self.r.resolve(["Cora", "Stern", "Vance", "Gideon"]),
            {
                "Cora": "left_bust4",
                "Stern": "centre_left_bust4",
                "Vance": "centre_right_bust4",
                "Gideon": "right_bust4",
            },
        )

    def test_vance_never_right_of_gideon(self):
        for cast in (["Vance", "Gideon"], ["Cora", "Vance", "Gideon"]):
            res = self.r.resolve(cast)
            order = self.r.slot_sets[len(cast)]
            self.assertLess(
                order.index(res["Vance"]),
                order.index(res["Gideon"]),
                f"Vance right of Gideon for {cast}",
            )

    def test_pin_overrides(self):
        res = self.r.resolve(["Cora", "Missy"], pins={"Missy": "left_bust"})
        self.assertEqual(res["Missy"], "left_bust")
        self.assertEqual(res["Cora"], "right_bust")

    def test_overflow_raises(self):
        with self.assertRaises(sd.OverflowError_):
            self.r.resolve(["Cora", "Stern", "Vance", "Gideon", "Missy"])

    def test_alias_folding(self):
        self.assertEqual(self.r.canonical_slot("left_centre_bust4"), "centre_left_bust4")
        self.assertEqual(self.r.canonical_slot("right_centre_bust4"), "centre_right_bust4")


class ShowParseTests(unittest.TestCase):
    def test_with_expression(self):
        s = sd.parse_show_line("    show cora_sprite angry at centre_bust")
        self.assertEqual((s.tag, s.expr, s.slot, s.block_form), ("cora_sprite", "angry", "centre_bust", False))

    def test_without_expression(self):
        s = sd.parse_show_line("    show gideon_sprite at right_bust")
        self.assertEqual((s.tag, s.expr, s.slot), ("gideon_sprite", None, "right_bust"))

    def test_block_form_detected(self):
        s = sd.parse_show_line("    show cora_sprite base_travel at left_bust:")
        self.assertTrue(s.block_form)

    def test_keep_and_auto_flags(self):
        keep = sd.parse_show_line("show cora_sprite neutral at left_bust # [asset keep]")
        auto = sd.parse_show_line("show cora_sprite neutral at left_bust # [asset auto]")
        self.assertTrue(keep.is_keep)
        self.assertTrue(auto.is_auto)


class TransformTests(unittest.TestCase):
    def test_brief_canonical_example(self):
        src = (
            "label x:\n"
            "    scene bg_corridor_day\n"
            "\n"
            "    # [enter:Cora]\n"
            '    cora "I was told to report here."\n'
            "\n"
            "    # [enter:Stern]\n"
            '    stern "Then you are late."\n'
            "\n"
            "    # [enter:Gideon]\n"
            '    gideon "Not late. Timely enough for my purposes."\n'
        )
        out = run(src)
        # First: Cora alone -> centre.
        self.assertIn("show cora_sprite base at centre_bust with moveinright # [asset auto]", out)
        # After Stern enters: Cora is left of Stern (project rule); Cora moves to left, Stern enters right.
        self.assertIn("show cora_sprite base at left_bust with move # [asset auto]", out)
        self.assertIn("show stern_sprite neutral at right_bust with moveinright # [asset auto]", out)
        # After Gideon enters: canonical Cora:left, Stern:centre, Gideon:right.
        self.assertIn("show stern_sprite neutral at centre_bust with move # [asset auto]", out)
        self.assertIn("show gideon_sprite neutral at right_bust with moveinright # [asset auto]", out)

    def test_idempotence(self):
        src = (
            "label x:\n"
            "    scene bg_corridor_day\n"
            "    # [enter:Cora]\n"
            '    cora "Hello."\n'
            "    # [enter:Stern]\n"
            '    stern "Late."\n'
        )
        once = run(src)
        twice = "\n".join(director().process_file(once.splitlines()))
        self.assertEqual(once, twice)

    def test_no_duplicate_auto_lines(self):
        src = (
            "label x:\n"
            "    scene bg\n"
            "    # [enter:Cora]\n"
            '    cora "A."\n'
        )
        out = run(run(src))  # run twice through text
        self.assertEqual(out.count("show cora_sprite"), 1)

    def test_scene_lock_skips_block(self):
        src = (
            "    # [asset lock:scene]\n"
            "    scene bg_suite_night\n"
            '    cora "Untouched."\n'
        )
        out = run(src)
        self.assertNotIn("[asset auto]", out)

    def test_asset_keep_preserved(self):
        src = (
            "    scene bg\n"
            "    show cora_sprite flushed at centre_bust # [asset keep]\n"
            '    cora "Hi."\n'
        )
        out = run(src)
        self.assertIn("show cora_sprite flushed at centre_bust # [asset keep]", out)
        # Cora already visible via the keep line -> no inferred auto show.
        self.assertNotIn("[asset auto]", out)

    def test_block_form_show_untouched(self):
        src = (
            "    scene bg\n"
            "    show cora_sprite base_travel at left_bust:\n"
            "        zoom 0.8\n"
            '    cora "Hi."\n'
        )
        out = run(src)
        self.assertIn("show cora_sprite base_travel at left_bust:", out)
        self.assertIn("        zoom 0.8", out)
        self.assertNotIn("[asset auto]", out)

    def test_dialogue_inference_inserts_before_line(self):
        src = (
            "    scene bg\n"
            '    missy "I only just arrived."\n'
        )
        out = run(src).splitlines()
        show_idx = next(i for i, l in enumerate(out) if "show missy_sprite" in l)
        dlg_idx = next(i for i, l in enumerate(out) if l.strip().startswith("missy "))
        self.assertLess(show_idx, dlg_idx)
        self.assertIn("# [asset auto]", out[show_idx])

    def test_exit_emits_hide(self):
        src = (
            "    scene bg\n"
            "    # [enter:Cora]\n"
            '    cora "Bye."\n'
            "    # [exit:Cora]\n"
        )
        out = run(src)
        self.assertIn("hide cora_sprite # [asset auto]", out)

    def test_overflow_warning(self):
        src = (
            "    scene bg\n"
            "    # [enter:Cora]\n"
            "    # [enter:Stern]\n"
            "    # [enter:Vance]\n"
            "    # [enter:Gideon]\n"
            "    # [enter:Missy]\n"
            '    missy "Too many."\n'
        )
        out = run(src)
        self.assertIn("asset warning", out)

    def test_dialogue_never_modified(self):
        src = (
            "    scene bg\n"
            "    # [enter:Cora]\n"
            '    cora "Precise words, kept exactly."\n'
        )
        out = run(src)
        self.assertIn('cora "Precise words, kept exactly."', out)

    def test_expression_preserved_on_reposition(self):
        src = (
            "    scene bg\n"
            "    show cora_sprite focused at centre_bust # [asset keep]\n"
            "    # [enter:Gideon]\n"
            '    gideon "We are not alone."\n'
        )
        out = run(src)
        # Cora was kept with 'focused'; when repositioned by Gideon's entry the
        # auto reposition must reuse 'focused', not the default.
        self.assertIn("show cora_sprite focused at left_bust with move # [asset auto]", out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
