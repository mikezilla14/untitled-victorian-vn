import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def scan_files():
    patterns = [
        re.compile(r'apply_balanced_effect'),
        re.compile(r'apply_effects'),
    ]
    
    files = list((ROOT / "main-game" / "non-prod-game" / "game" / "days").glob("*.rpy"))
    files.append(ROOT / "main-game" / "non-prod-game" / "game" / "shared" / "story_chains_non_canon.rpy")
    
    for path in files:
        if path.name == "balance_profiles_non_canon.rpy" or path.name == "functions_non_canon.rpy":
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except Exception:
            continue
            
        print(f"\n=== FILE: {path.relative_to(ROOT).as_posix()} ===")
        lines = content.splitlines()
        for idx, line in enumerate(lines, start=1):
            if any(pat.search(line) for pat in patterns):
                # Print 3 lines lookback for comments
                lookback = []
                for i in range(max(0, idx - 4), idx - 1):
                    lookback.append(lines[i].strip())
                print(f"L{idx}: {' | '.join(lookback)}")
                print(f"  {line.strip()}")

if __name__ == "__main__":
    scan_files()
