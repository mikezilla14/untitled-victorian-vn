#!/usr/bin/env python3
"""Audit and catalogue cross-project documentation."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
CATALOG_MD = DOCS / "DOCUMENTATION_CATALOG.md"
AUDIT_MD = DOCS / "DOCUMENTATION_AUDIT.md"
CATALOG_JSON = DOCS / "documentation_catalog.json"

DOC_ROOTS = [
    ROOT / "README.md",
    ROOT / "AGENTS.md",
    ROOT / "CLAUDE.md",
    ROOT / ".agents",
    ROOT / "docs",
    ROOT / "assets_source",
    ROOT / "narrative",
    ROOT / "renpy_project",
    ROOT / ".github",
]
IGNORED_PARTS = {".git", ".venv", "__pycache__", ".claude"}
LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
TITLE_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
STALE_PATTERNS = {
    "legacy speculative path": "speculative/",
    "legacy writers room path": "narrative/writers_room",
    "space-based release slug": "release 1 - mvp",
    "absolute local file URL": "file:///",
}


@dataclass
class Finding:
    severity: str
    path: str
    message: str

    def to_json(self) -> dict[str, str]:
        return {"severity": self.severity, "path": self.path, "message": self.message}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def should_skip(path: Path) -> bool:
    if any(part in IGNORED_PARTS for part in path.parts):
        return True
    rel_path = path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else ""
    if rel_path.startswith("narrative/pipeline/releases/"):
        return True
    if rel_path.startswith("narrative/draft/releases/"):
        return True
    return False


def skip_readme_requirement(directory: Path) -> bool:
    rel_path = rel(directory)
    parts = directory.relative_to(ROOT).parts
    if "releases" in parts and ("days" in parts or "non_prod_renpy_project" in parts):
        return True
    if rel_path.startswith("renpy_project/game/gui") or rel_path.startswith("renpy_project/game/images"):
        return True
    if rel_path.startswith("renpy_project/game/"):
        return True
    return False


def iter_doc_files() -> list[Path]:
    files: set[Path] = set()
    generated_outputs = {CATALOG_MD, AUDIT_MD}
    for root in DOC_ROOTS:
        if not root.exists():
            continue
        if root.is_file():
            if root.suffix.lower() == ".md" and root not in generated_outputs and not should_skip(root):
                files.add(root)
            continue
        for path in root.rglob("*.md"):
            if path.is_file() and path not in generated_outputs and not should_skip(path):
                files.add(path)
    return sorted(files, key=lambda item: rel(item).lower())


def iter_candidate_readme_dirs() -> list[Path]:
    roots = [
        ROOT / "docs",
        ROOT / ".agents",
        ROOT / "scripts",
        ROOT / "narrative",
        ROOT / "renpy_project",
        ROOT / "assets_source",
    ]
    candidates: list[Path] = []
    for root in roots:
        if not root.exists():
            continue
        for directory in [root, *[item for item in root.rglob("*") if item.is_dir()]]:
            if should_skip(directory):
                continue
            if skip_readme_requirement(directory):
                continue
            files = [item for item in directory.iterdir() if item.is_file()]
            subdirs = [item for item in directory.iterdir() if item.is_dir() and not should_skip(item)]
            operational = [
                item
                for item in files
                if item.suffix.lower() in {".md", ".py", ".rpy", ".json", ".yaml", ".yml"}
                and item.name != "README.md"
            ]
            if len(operational) >= 3 or len(subdirs) >= 3:
                candidates.append(directory)
    return sorted(set(candidates), key=lambda item: rel(item).lower())


def classify(path: Path) -> str:
    name = path.name.lower()
    parts = path.relative_to(ROOT).parts
    if path == ROOT / "AGENTS.md" or path == ROOT / ".agents" / "README.md":
        return "agent-index"
    if ".agents" in parts and "rules" in parts:
        return "agent-rule"
    if ".agents" in parts and "skills" in parts:
        return "agent-skill"
    if name == "readme.md":
        return "readme"
    if "contracts" in parts:
        return "contract"
    if "specs" in parts:
        return "feature-spec"
    if "backlog" in parts:
        return "backlog"
    if "onboarding" in parts or name == "getting_started.md":
        return "onboarding"
    if "agents" in parts:
        return "workflow"
    if path in {CATALOG_MD, AUDIT_MD}:
        return "catalogue"
    if name.endswith("_workflow.md") or "workflow" in name:
        return "workflow"
    return "reference"


def title_for(path: Path, text: str) -> str:
    match = TITLE_RE.search(text)
    if match:
        return match.group(1).strip("` ")
    return path.stem.replace("_", " ").replace("-", " ").title()


def area_for(path: Path) -> str:
    parts = path.relative_to(ROOT).parts
    if len(parts) == 1:
        return "repo-root"
    if parts[0] == ".agents" and len(parts) > 2:
        return "/".join(parts[:3])
    if parts[0] == "docs" and len(parts) > 2:
        return "/".join(parts[:2])
    return parts[0]


def summary_for(text: str) -> str:
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith("|") or line.startswith("```"):
            continue
        if line.startswith("- ") or line.startswith("* "):
            line = line[2:].strip()
        return line[:220]
    return ""


def resolve_link(source: Path, target: str) -> tuple[str, str]:
    if target.startswith("#"):
        return target, "anchor-only"
    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
        return target, "external"
    clean = target.split("#", 1)[0].replace("%20", " ").strip()
    if not clean:
        return target, "anchor-only"
    candidate = (source.parent / clean).resolve()
    try:
        candidate.relative_to(ROOT)
    except ValueError:
        return target, "missing"
    return target, "ok" if candidate.exists() else "missing"


def audit_file(path: Path, text: str) -> tuple[list[dict[str, str]], list[str], list[Finding]]:
    links: list[dict[str, str]] = []
    entry_findings: list[str] = []
    findings: list[Finding] = []
    rel_path = rel(path)

    for target in LINK_RE.findall(text):
        target = target.strip()
        resolved_target, status = resolve_link(path, target)
        links.append({"target": resolved_target, "status": status})
        if status == "missing":
            msg = f"Broken relative link: {target}"
            entry_findings.append(msg)
            findings.append(Finding("error", rel_path, msg))

    for label, pattern in STALE_PATTERNS.items():
        if pattern in text:
            if pattern == "release 1 - mvp" and f"not `{pattern}`" in text:
                continue
            if pattern == "speculative/" and "Previously `speculative/`" in text:
                continue
            msg = f"Possible stale reference ({label}): {pattern}"
            entry_findings.append(msg)
            findings.append(Finding("warning", rel_path, msg))

    if classify(path) == "feature-spec":
        lowered = text.lower()
        status_words = ["implemented", "partial", "planned", "backlog", "deferred", "current implementation status"]
        if not any(word in lowered for word in status_words):
            msg = "Feature spec does not clearly state implementation status."
            entry_findings.append(msg)
            findings.append(Finding("warning", rel_path, msg))

    if classify(path) == "contract" and path.suffix == ".md":
        has_contract_link = any(token in text for token in [".schema.json", ".json", ".yaml", ".yml"])
        if not has_contract_link and "Machine-readable schema: not yet defined" not in text:
            msg = "Contract document does not link to a machine-readable schema or data file."
            entry_findings.append(msg)
            findings.append(Finding("warning", rel_path, msg))

    return links, entry_findings, findings


def build_catalog(generated_at: str | None = None) -> dict:
    entries = []
    findings: list[Finding] = []

    for path in iter_doc_files():
        text = path.read_text(encoding="utf-8", errors="replace")
        links, entry_findings, file_findings = audit_file(path, text)
        findings.extend(file_findings)
        entries.append(
            {
                "path": rel(path),
                "kind": classify(path),
                "title": title_for(path, text),
                "area": area_for(path),
                "summary": summary_for(text),
                "links": links,
                "findings": entry_findings,
            }
        )

    for directory in iter_candidate_readme_dirs():
        if not (directory / "README.md").exists():
            findings.append(Finding("warning", rel(directory), "Complex folder has no README.md index."))

    if generated_at is None:
        generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    return {
        "schema_version": 1,
        "generated_at": generated_at,
        "repo_root": ROOT.name,
        "entries": entries,
        "findings": [finding.to_json() for finding in findings],
    }


def markdown_catalog(catalog: dict) -> str:
    lines = [
        "# Documentation catalogue",
        "",
        "> Generated by `py scripts/documentation_audit.py --write`. Edit source docs, then regenerate.",
        "",
        f"- Generated: `{catalog['generated_at']}`",
        f"- Documents indexed: `{len(catalog['entries'])}`",
        f"- Findings: `{len(catalog['findings'])}`",
        "",
        "## By area",
        "",
    ]
    by_area: dict[str, list[dict]] = {}
    for entry in catalog["entries"]:
        by_area.setdefault(entry["area"], []).append(entry)
    for area in sorted(by_area):
        lines.extend([f"### {area}", "", "| Path | Kind | Summary | Findings |", "|------|------|---------|----------|"])
        for entry in sorted(by_area[area], key=lambda item: item["path"].lower()):
            summary = entry["summary"].replace("|", "\\|")
            lines.append(f"| [{entry['path']}]({entry['path']}) | {entry['kind']} | {summary} | {len(entry['findings'])} |")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def markdown_audit(catalog: dict) -> str:
    lines = [
        "# Documentation audit",
        "",
        "> Generated by `py scripts/documentation_audit.py --write`. Fix findings in source docs, then regenerate.",
        "",
        f"- Generated: `{catalog['generated_at']}`",
        f"- Findings: `{len(catalog['findings'])}`",
        "",
        "## Findings",
        "",
    ]
    if catalog["findings"]:
        lines.extend(["| Severity | Path | Message |", "|----------|------|---------|"])
        for finding in catalog["findings"]:
            msg = finding["message"].replace("|", "\\|")
            lines.append(f"| {finding['severity']} | `{finding['path']}` | {msg} |")
        lines.append("")
    else:
        lines.extend(["No documentation gaps detected.", ""])

    missing_readmes = [
        finding for finding in catalog["findings"]
        if finding["message"] == "Complex folder has no README.md index."
    ]
    lines.extend(["## Missing README Coverage", ""])
    if missing_readmes:
        for finding in missing_readmes:
            lines.append(f"- `{finding['path']}`")
    else:
        lines.append("All complex documentation folders have README coverage.")
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_outputs(catalog: dict) -> None:
    DOCS.mkdir(exist_ok=True)
    CATALOG_JSON.write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    CATALOG_MD.write_text(markdown_catalog(catalog), encoding="utf-8")
    AUDIT_MD.write_text(markdown_audit(catalog), encoding="utf-8")


def generated_at_for_check() -> str:
    if not CATALOG_JSON.exists():
        return "1970-01-01T00:00:00+00:00"
    try:
        data = json.loads(CATALOG_JSON.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return "1970-01-01T00:00:00+00:00"
    return data.get("generated_at", "1970-01-01T00:00:00+00:00")


def check_outputs(catalog: dict) -> int:
    expected = {
        CATALOG_JSON: json.dumps(catalog, indent=2, ensure_ascii=False) + "\n",
        CATALOG_MD: markdown_catalog(catalog),
        AUDIT_MD: markdown_audit(catalog),
    }
    stale = []
    for path, content in expected.items():
        if not path.exists() or path.read_text(encoding="utf-8", errors="replace") != content:
            stale.append(rel(path))
    if stale:
        print("Documentation catalogue is stale. Regenerate with:")
        print("  py scripts/documentation_audit.py --write")
        for path in stale:
            print(f"  - {path}")
        return 1
    print("Documentation catalogue is current.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Refresh catalogue and audit artifacts.")
    parser.add_argument("--check", action="store_true", help="Fail if generated artifacts are stale.")
    args = parser.parse_args()

    if not args.write and not args.check:
        parser.error("Use --write or --check.")

    generated_at = None if args.write else generated_at_for_check()
    catalog = build_catalog(generated_at=generated_at)
    if args.write:
        write_outputs(catalog)
        print(f"Wrote {rel(CATALOG_MD)}, {rel(AUDIT_MD)}, and {rel(CATALOG_JSON)}.")
        return 0
    return check_outputs(catalog)


if __name__ == "__main__":
    sys.exit(main())
