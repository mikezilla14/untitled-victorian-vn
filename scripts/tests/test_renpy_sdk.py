"""Tests for Ren'Py SDK discovery."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1]
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import renpy_sdk  # noqa: E402


class RenpySdkDiscoveryTests(unittest.TestCase):
    def test_picks_highest_version_sdk(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            old = root / "renpy-8.4.0-sdk"
            new = root / "renpy-8.5.3-sdk"
            old.mkdir()
            new.mkdir()
            (old / "renpy.exe").write_text("", encoding="utf-8")
            (new / "renpy.exe").write_text("", encoding="utf-8")

            with mock.patch.object(renpy_sdk, "_search_roots", return_value=[root]):
                self.assertEqual(renpy_sdk.find_renpy_sdk_root(), new.resolve())

    def test_build_lint_command_uses_project_then_lint(self):
        with tempfile.TemporaryDirectory() as tmp:
            sdk = Path(tmp) / "renpy-8.5.3-sdk"
            sdk.mkdir()
            exe = sdk / "renpy.exe"
            exe.write_text("", encoding="utf-8")
            project = Path(tmp) / "game-project"
            project.mkdir()

            with mock.patch.object(renpy_sdk, "find_renpy_executable", return_value=exe):
                cmd = renpy_sdk.build_lint_command(project)

            self.assertEqual(cmd, [str(exe.resolve()), str(project.resolve()), "lint"])

    def test_env_renpy_sdk_takes_precedence(self):
        with tempfile.TemporaryDirectory() as tmp:
            sdk = Path(tmp) / "custom-sdk"
            sdk.mkdir()
            (sdk / "renpy.exe").write_text("", encoding="utf-8")

            with mock.patch.dict("os.environ", {"RENPY_SDK": str(sdk)}):
                self.assertEqual(renpy_sdk.find_renpy_sdk_root(), sdk.resolve())


if __name__ == "__main__":
    unittest.main()
