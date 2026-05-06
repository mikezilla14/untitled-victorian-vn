import argparse
import re
import sys


# List of modern words that AI frequently hallucinates into historical fiction.
FORBIDDEN_WORDS = [
    "okay",
    "ok",
    "cool",
    "got it",
    "teenager",
    "teens",
    "weekend",
    "stress",
    "trauma",
    "projecting",
    "gaslight",
    "jeans",
    "cell",
    "phone",
    "hello",  # 'hello' wasn't widely used until the telephone.
]


def lint_file(filepath):
    errors = []
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        line_lower = line.lower()
        for word in FORBIDDEN_WORDS:
            if re.search(fr"\b{word}\b", line_lower):
                errors.append(f"Line {i + 1}: Found anachronism '{word}'.")

    return errors


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, help="Narrative file to lint (.md or .rpy)")
    args = parser.parse_args()

    print(f"Victorian Consultant checking {args.file}...")
    errors = lint_file(args.file)

    if errors:
        print("HISTORICAL VIOLATIONS FOUND:")
        for error in errors:
            print("  - " + error)
        sys.exit(1)

    print("Historically sound. No obvious anachronisms.")
    sys.exit(0)
