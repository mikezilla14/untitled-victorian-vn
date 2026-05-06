import argparse
import fnmatch
import sys
from pathlib import Path


def parse_inline_list(value):
    return [item.strip() for item in value.strip("[]").split(",") if item.strip()]


def load_guardrails(yaml_path):
    """
    Load the small subset of YAML used by .guardrails.yml.

    Keeping this parser local avoids requiring PyYAML for everyday agent/local
    validation. CI can still install PyYAML, but the workflow does not depend on it.
    """
    domains = {}
    current_domain = None
    current_key = None
    in_domains = False

    for raw_line in Path(yaml_path).read_text(encoding="utf-8").splitlines():
        line = raw_line.split("#", 1)[0].rstrip()
        if not line.strip():
            continue

        if line == "domains:":
            in_domains = True
            continue
        if not in_domains:
            continue

        if raw_line.startswith("  ") and not raw_line.startswith("    ") and line.endswith(":"):
            current_domain = line.strip()[:-1]
            domains[current_domain] = {}
            current_key = None
            continue

        if current_domain is None:
            continue

        stripped = line.strip()
        if stripped.endswith(":"):
            current_key = stripped[:-1]
            domains[current_domain][current_key] = []
            continue

        if ":" in stripped:
            key, value = stripped.split(":", 1)
            key = key.strip()
            value = value.strip()
            current_key = key
            if value.startswith("[") and value.endswith("]"):
                domains[current_domain][key] = parse_inline_list(value)
            elif value:
                domains[current_domain][key] = value.strip('"')
            else:
                domains[current_domain][key] = []
            continue

        if stripped.startswith("- ") and current_key:
            domains[current_domain].setdefault(current_key, []).append(stripped[2:].strip())

    return {"domains": domains}


def check_permission(agent, files_changed, guardrails):
    violations = []

    for file in files_changed:
        matched_domain = False
        allowed = False

        for domain_name, domain_data in guardrails.get("domains", {}).items():
            for path_pattern in domain_data.get("paths", []):
                if fnmatch.fnmatch(file, path_pattern):
                    matched_domain = True
                    mutable_by = domain_data.get("mutable_by", [])
                    if agent in mutable_by or "all" in mutable_by:
                        allowed = True
                    break
            if allowed:
                break

        if matched_domain and not allowed:
            violations.append(file)

    return violations


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent", required=True, help="Name of the agent making the PR")
    parser.add_argument("--files", required=True, help="Comma separated list of files changed")
    args = parser.parse_args()

    files_list = [f.strip() for f in args.files.split(",") if f.strip()]
    guardrails = load_guardrails(".guardrails.yml")

    print(f"Gatekeeper Orchestrator checking permissions for '{args.agent}'...")

    violations = check_permission(args.agent, files_list, guardrails)

    if violations:
        print(f"SECURITY ALERT: Agent '{args.agent}' is not authorized to modify:")
        for violation in violations:
            print(f"   - {violation}")
        print("Merge rejected. Human override required.")
        sys.exit(1)

    print("All file modifications are within authorized domains.")
    sys.exit(0)
