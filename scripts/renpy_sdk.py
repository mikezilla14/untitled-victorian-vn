#!/usr/bin/env python3
"""Locate a Ren'Py SDK install and build engine lint commands."""

from __future__ import annotations

import os
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Windows default used by this project's author; also scanned via OneDrive home path.
_WINDOWS_RENPY_DOCUMENTS = Path(r"C:\Users\mikez\OneDrive\Documents\Renpy")

_SDK_DIR_RE = re.compile(r"renpy-(\d+)\.(\d+)\.(\d+)-sdk", re.IGNORECASE)


def _sdk_executable(sdk_root: Path) -> Path | None:
    if sys.platform == "win32":
        candidate = sdk_root / "renpy.exe"
    else:
        candidate = sdk_root / "renpy.sh"
    return candidate if candidate.is_file() else None


def _parse_sdk_version(name: str) -> tuple[int, int, int] | None:
    match = _SDK_DIR_RE.match(name)
    if not match:
        return None
    return tuple(int(part) for part in match.groups())  # type: ignore[return-value]


def _search_roots() -> list[Path]:
    roots: list[Path] = []
    env_root = os.environ.get("RENPY_SDK")
    if env_root:
        roots.append(Path(env_root).expanduser())
    if sys.platform == "win32":
        roots.append(_WINDOWS_RENPY_DOCUMENTS)
        roots.append(Path.home() / "OneDrive" / "Documents" / "Renpy")
    roots.extend(
        [
            Path.home() / "renpy",
            Path("/opt/renpy"),
            Path("C:/renpy"),
        ]
    )
    seen: set[Path] = set()
    ordered: list[Path] = []
    for root in roots:
        resolved = root.expanduser()
        if resolved in seen:
            continue
        seen.add(resolved)
        ordered.append(resolved)
    return ordered


def _latest_sdk_in_root(root: Path) -> Path | None:
    if not root.is_dir():
        return None

    candidates: list[tuple[tuple[int, int, int], float, Path]] = []
    for child in root.iterdir():
        if not child.is_dir() or _sdk_executable(child) is None:
            continue
        version = _parse_sdk_version(child.name) or (0, 0, 0)
        candidates.append((version, child.stat().st_mtime, child))

    if not candidates:
        return None

    candidates.sort(key=lambda item: (item[0], item[1]), reverse=True)
    return candidates[0][2]


def find_renpy_sdk_root() -> Path | None:
    """Return the newest Ren'Py SDK root directory, or None if not found."""
    env_root = os.environ.get("RENPY_SDK")
    if env_root:
        direct = Path(env_root).expanduser()
        if _sdk_executable(direct) is not None:
            return direct.resolve()

    for root in _search_roots():
        if env_root and Path(env_root).expanduser() == root:
            continue
        sdk = _latest_sdk_in_root(root)
        if sdk is not None:
            return sdk.resolve()
    return None


def find_renpy_executable() -> Path | None:
    """Return renpy.exe / renpy.sh from PATH or the newest discovered SDK."""
    on_path = shutil.which("renpy")
    if on_path:
        return Path(on_path).resolve()

    sdk_root = find_renpy_sdk_root()
    if sdk_root is None:
        return None

    exe = _sdk_executable(sdk_root)
    return exe.resolve() if exe is not None else None


def build_lint_command(project_dir: Path) -> list[str] | None:
    """Build ``[<renpy>, <project>, lint]`` or None when no SDK is available."""
    exe = find_renpy_executable()
    if exe is None:
        return None
    return [str(exe), str(project_dir.resolve()), "lint"]


def lint_fix_hint(project_dir: Path | None = None) -> str:
    project = project_dir or (ROOT / "main-game" / "non-prod-game")
    cmd = build_lint_command(project)
    if cmd:
        return " ".join(cmd)
    return (
        'Set RENPY_SDK to your SDK folder or install Ren\'Py under '
        f"{_WINDOWS_RENPY_DOCUMENTS}, then run: "
        f'renpy "{project.resolve()}" lint'
    )
