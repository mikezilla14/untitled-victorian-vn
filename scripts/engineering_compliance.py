import argparse
import re
import sys
from pathlib import Path


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

    if all_violations:
        print("❌ ENGINEERING COMPLIANCE VIOLATIONS:")
        for violation in all_violations:
            print(f" - {violation}")
        sys.exit(1)

    print("✅ Engineering compliance checks passed.")
    sys.exit(0)


if __name__ == "__main__":
    main()
