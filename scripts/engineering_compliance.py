import argparse
import re
import sys
from pathlib import Path

ALLOWED_TIME_PERIODS = {
    "Early Morning",
    "Morning",
    "Afternoon",
    "Evening",
    "Night",
    "Late Night",
}

DAYRXX_RPY_RE = re.compile(r"^day([1-9]\d*)([0-9]\d)\.rpy$")
DAYRXX_NON_CANON_RE = re.compile(
    r"^day([1-9]\d*)([0-9]\d)_non_canon\.rpy$"
)
LEGACY_DAY_NON_CANON_RE = re.compile(r"^day\d+_non_canon\.(md|rpy)$")
LEGACY_DAY_RPY_RE = re.compile(r"^day\d+\.rpy$")


def read_lines(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.readlines()


def check_no_new_defaults_outside_variables(files):
    violations = []
    for file in files:
        if not file.endswith(".rpy"):
            continue
        if file.replace("\\", "/") == "renpy_project/game/variables.rpy":
            continue
        full_path = Path(file)
        if not full_path.exists():
            continue
        for idx, line in enumerate(read_lines(full_path), start=1):
            if re.match(r"^\s*default\s+\w+\s*=", line):
                violations.append(
                    f"{file}:{idx} new `default` declaration outside variables.rpy"
                )
    return violations


def check_no_direct_player_field_writes(files):
    """
    Prefer method-based mutation over direct stat field writes.
    """
    violations = []
    pattern = re.compile(
        r"^\s*\$\s*player\.(inspiration|suspicion|corruption_xp|corruption_level)\s*[-+*/]?="
    )
    for file in files:
        if not file.endswith(".rpy"):
            continue
        full_path = Path(file)
        if not full_path.exists():
            continue
        for idx, line in enumerate(read_lines(full_path), start=1):
            if pattern.search(line):
                violations.append(
                    f"{file}:{idx} direct `player.<stat>` assignment; use mutation methods"
                )
    return violations


def check_suspicion_guard_order(files):
    """
    Enforce expected ordering in day scripts:
    call check_suspicion
    $ player.update_stats()
    """
    violations = []
    for file in files:
        norm = file.replace("\\", "/")
        if not re.match(r"renpy_project/game/day\d+\.rpy$", norm):
            continue
        full_path = Path(file)
        if not full_path.exists():
            continue
        content = full_path.read_text(encoding="utf-8")
        bad_pattern = re.compile(
            r"\$\s*player\.update_stats\(\)\s*\n\s*call\s+check_suspicion",
            re.MULTILINE,
        )
        if bad_pattern.search(content):
            violations.append(
                f"{file}: contains `update_stats` before `check_suspicion` in at least one flow block"
            )
    return violations


def check_script_thin_if_touched(files):
    violations = []
    target = "renpy_project/game/script.rpy"
    if target not in [f.replace("\\", "/") for f in files]:
        return violations

    full_path = Path(target)
    if not full_path.exists():
        return violations
    lines = read_lines(full_path)
    for idx, line in enumerate(lines, start=1):
        if re.match(r"^\s*\$\s*player\.", line) or re.match(r"^\s*\$\s*story\.", line):
            violations.append(
                f"{target}:{idx} script.rpy should remain thin (avoid direct state mutation)"
            )
    return violations


def check_no_direct_story_corridor_state_assignment(files):
    """
    Mutually exclusive branch strings must be updated only via StoryState.set_corridor_state()
    in game scripts, never by assigning story.day1_corridor_state.
    """
    violations = []
    # assignment only, not == or other operators
    pattern = re.compile(r"story\.day1_corridor_state\s*=(?!=)")
    for file in files:
        if not file.endswith(".rpy"):
            continue
        norm = file.replace("\\", "/")
        if not norm.startswith("renpy_project/game/"):
            continue
        full_path = Path(file)
        if not full_path.exists():
            continue
        for idx, line in enumerate(read_lines(full_path), start=1):
            if pattern.search(line):
                violations.append(
                    f"{file}:{idx} direct `story.day1_corridor_state` assignment; "
                    f"use `story.set_corridor_state(...)` (whitelist in classes.rpy)"
                )
    return violations


def check_no_bare_set_corridor_state_call(files):
    """
    Disallow unqualified set_corridor_state(...) in game scripts; require story.set_corridor_state(...).
    """
    violations = []
    pattern = re.compile(r"^\s*\$?\s*set_corridor_state\s*\(")
    for file in files:
        if not file.endswith(".rpy"):
            continue
        norm = file.replace("\\", "/")
        if not norm.startswith("renpy_project/game/"):
            continue
        full_path = Path(file)
        if not full_path.exists():
            continue
        for idx, line in enumerate(read_lines(full_path), start=1):
            stripped = line.lstrip()
            if stripped.startswith("#") or stripped.startswith("##"):
                continue
            if pattern.search(line) and "story.set_corridor_state" not in line:
                violations.append(
                    f"{file}:{idx} use `story.set_corridor_state(...)` — "
                    f"unqualified set_corridor_state is not a supported pattern"
                )
    return violations


def check_time_period_literals(files):
    """
    Enforce standardized time-of-day literals.
    """
    violations = []
    direct_assign = re.compile(r'^\s*\$\s*time_manager\.time_of_day\s*=\s*"([^"]+)"')
    helper_assign = re.compile(r'^\s*\$\s*set_time_period\(\s*"([^"]+)"\s*\)')

    for file in files:
        if not file.endswith(".rpy"):
            continue
        full_path = Path(file)
        if not full_path.exists():
            continue

        for idx, line in enumerate(read_lines(full_path), start=1):
            match = direct_assign.search(line) or helper_assign.search(line)
            if not match:
                continue
            literal = match.group(1)
            if literal not in ALLOWED_TIME_PERIODS:
                violations.append(
                    f"{file}:{idx} invalid time period '{literal}'. "
                    f"Allowed: {sorted(ALLOWED_TIME_PERIODS)}"
                )
    return violations


def check_day_file_naming_contract(files):
    """
    Enforce day file naming contract:
    - Narrative drafts: dayrdd_non_canon.rpy (e.g. day100_non_canon.rpy)
    - Runtime files: dayrxx.rpy (e.g. day101.rpy)
    where r = release number and dd = 2-digit day slot (00-99).
    """
    violations = []
    for file in files:
        norm = file.replace("\\", "/")
        name = Path(norm).name
        full_path = Path(file)
        if not full_path.exists():
            continue

        if norm.startswith("narrative/writers_room/") and name.endswith("_non_canon.rpy"):
            if not DAYRXX_NON_CANON_RE.fullmatch(name):
                violations.append(
                    f"{file} invalid non-canon day filename. Expected dayrdd_non_canon.rpy (example: day100_non_canon.rpy)."
                )
            continue

        if norm.startswith("renpy_project/game/") and name.endswith(".rpy"):
            if LEGACY_DAY_RPY_RE.fullmatch(name) and not DAYRXX_RPY_RE.fullmatch(name):
                violations.append(
                    f"{file} uses legacy episodic filename. Expected dayrxx.rpy (example: day101.rpy)."
                )
            continue

        # Explicitly guard against legacy narrative naming where applicable.
        if LEGACY_DAY_NON_CANON_RE.fullmatch(name) and not DAYRXX_NON_CANON_RE.fullmatch(name):
            violations.append(
                f"{file} uses legacy non-canon filename. Expected dayrdd_non_canon.rpy (example: day100_non_canon.rpy)."
            )

    return violations


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--files",
        required=True,
        help="Comma-separated changed file paths.",
    )
    args = parser.parse_args()
    files = [f.strip() for f in args.files.split(",") if f.strip()]

    if not files:
        print("No files provided. Skipping engineering compliance.")
        sys.exit(0)

    all_violations = []
    all_violations.extend(check_no_new_defaults_outside_variables(files))
    all_violations.extend(check_no_direct_player_field_writes(files))
    all_violations.extend(check_suspicion_guard_order(files))
    all_violations.extend(check_script_thin_if_touched(files))
    all_violations.extend(check_time_period_literals(files))
    all_violations.extend(check_no_direct_story_corridor_state_assignment(files))
    all_violations.extend(check_no_bare_set_corridor_state_call(files))
    all_violations.extend(check_day_file_naming_contract(files))

    if all_violations:
        print("ENGINEERING COMPLIANCE VIOLATIONS:")
        for violation in all_violations:
            print(f" - {violation}")
        sys.exit(1)

    print("Engineering compliance checks passed.")
    sys.exit(0)


if __name__ == "__main__":
    main()
