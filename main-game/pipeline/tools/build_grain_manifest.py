#!/usr/bin/env python3
"""Build balance grain manifest from non-prod Ren'Py sandbox scripts.

Phase 1 extractor: infers test/balance grains from labels, menus, gates, and
DAG tags without executing Ren'Py. Complements build_story_graph_manifest.py
(graph/routing audit) with balance-focused grain boundaries.
"""

from __future__ import annotations

import argparse
import ast
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_RELEASE = "release-1-mvp"

LABEL_RE = re.compile(r"^label\s+([A-Za-z_]\w*)(?:\(([^)]*)\))?:")
DAG_BRACKET_RE = re.compile(r"#\s*\[(DAG_[A-Z_]+)\s+([^\]]*)\]")
DAG_HASH_RE = re.compile(r"#\s*(DAG_[A-Z]+)\s+(.+)$")
MENU_RE = re.compile(r"^\s*menu\s*:")
IF_RE = re.compile(r"^\s*(if|elif)\s+(.+):\s*$")
JUMP_FAIL_RE = re.compile(r"^\s*jump\s+(game_over_\w+|bad_ending_\w+)\s*$")
CALL_BOOK_RE = re.compile(r"^\s*call\s+book1_write_chapter\b")
COMPLETE_MS_RE = re.compile(r'complete_manuscript_chapter\("([^"]+)"\)')

WRITE_GATE_SNIPPETS = ("has_story_fuel", "WRITE_GATE", "attempt_write")
DEADLINE_SNIPPETS = ("manuscript_progress == 0", "manuscript_progress < 2", "manuscript_progress < 3")
CONSEQUENCE_SNIPPETS = ("call watch_suspicion", "watch_suspicion")
PENANCE_SNIPPETS = (
    "story_window_penance_gate",
    "consume_pending_penance",
    "call check_confrontations",
)

GRAIN_INFER_PATTERNS: tuple[tuple[str, tuple[str, ...], str], ...] = (
    ("write_gate", WRITE_GATE_SNIPPETS, "major"),
    ("deadline_gate", DEADLINE_SNIPPETS, "blocker"),
    ("consequence_window", CONSEQUENCE_SNIPPETS, "major"),
    ("penance", PENANCE_SNIPPETS, "major"),
    ("book1", ("book1_write_chapter",), "major"),
    ("ending", ("game_over_", "bad_ending_"), "blocker"),
)


@dataclass
class Grain:
    grain_id: str
    grain_type: str
    label: str = ""
    day: str = ""
    period: str = ""
    capture: str = ""
    source_file: str = ""
    line_number: int = 0
    parent_label: str = ""
    condition: str = ""
    inference: str = "inferred"
    confidence: str = "medium"
    tag_type: str = ""

    def to_row(self) -> dict[str, str]:
        return {
            "grain_id": self.grain_id,
            "grain_type": self.grain_type,
            "label": self.label,
            "day": self.day,
            "period": self.period,
            "capture": self.capture,
            "source_file": self.source_file,
            "line_number": str(self.line_number),
            "parent_label": self.parent_label,
            "condition": self.condition,
            "inference": self.inference,
            "confidence": self.confidence,
            "tag_type": self.tag_type,
        }


@dataclass
class GrainGap:
    gap_id: str
    severity: str
    gap_type: str
    source_file: str
    line_number: int
    label: str
    description: str
    recommended_owner: str
    recommended_next_action: str


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def parse_tag_attrs(raw: str) -> dict[str, str]:
    attrs: dict[str, str] = {}
    for match in re.finditer(r'(\w+)="([^"]*)"|(\w+)=([^\s,]+)', raw):
        if match.group(1):
            attrs[match.group(1)] = match.group(2)
        elif match.group(3):
            attrs[match.group(3)] = match.group(4).strip(",")
    if "group" in attrs and "id" not in attrs:
        attrs["id"] = attrs["group"]
    return attrs


def parse_dag_line(line: str) -> tuple[str, dict[str, str]] | None:
    bracket = DAG_BRACKET_RE.search(line)
    if bracket:
        return bracket.group(1), parse_tag_attrs(bracket.group(2))
    plain = DAG_HASH_RE.search(line)
    if plain:
        return plain.group(1), parse_tag_attrs(plain.group(2))
    return None


def infer_day_period(label: str) -> tuple[str, str]:
    day_match = re.search(r"day(\d{3})", label)
    day = day_match.group(1) if day_match else ""
    period = ""
    for token in ("prologue", "morning", "afternoon", "evening", "night", "manuscript", "ending"):
        if token in label.lower():
            period = token
            break
    if not period:
        slot_match = re.search(r"_(\d)_", label)
        if slot_match:
            period_map = {"1": "morning", "2": "afternoon", "3": "evening", "4": "night", "5": "night", "6": "ending", "7": "ending"}
            period = period_map.get(slot_match.group(1), "")
    return day, period


def label_at_line(line_to_label: dict[int, str], line_idx: int) -> str:
    return line_to_label.get(line_idx, "file")


def build_line_to_label(lines: list[str]) -> dict[int, str]:
    current = "file"
    mapping: dict[int, str] = {}
    for idx, line in enumerate(lines):
        label_match = LABEL_RE.match(line)
        if label_match:
            current = label_match.group(1)
        mapping[idx] = current
    return mapping


def is_illegal_tag_context(lines: list[str], idx: int) -> bool:
    window = "\n".join(lines[max(0, idx - 2) : idx + 1])
    if "init python:" in window or '"""' in window or "'''" in window:
        return True
    return False


def normalize_condition(expr: str) -> tuple[str, str]:
    expr = expr.strip()
    try:
        parsed = ast.parse(expr, mode="eval")
        return ast.dump(parsed, annotate_fields=False), "high"
    except SyntaxError:
        if "has_story_fuel(*WRITE_GATE_CH" in expr:
            return expr, "medium"
        return expr, "low"


def infer_grain_type_from_block(block: str, label: str) -> str | None:
    if label.startswith("game_over_") or label.startswith("bad_ending_"):
        return "ending"
    if "book1_write_chapter" in block or label.startswith("book1_"):
        return "book1"
    for grain_type, snippets, _ in GRAIN_INFER_PATTERNS:
        if any(snippet in block for snippet in snippets):
            return grain_type
    if "menu:" in block:
        return "choice"
    if label.startswith("day") and re.match(r"day\d{3}_(main|morning|afternoon|evening|night)", label):
        return "spine"
    if re.match(r"^day\d{3}_", label):
        return "spine"
    return None


def append_gap(
    gaps: list[GrainGap],
    *,
    severity: str,
    gap_type: str,
    source_file: str,
    line_number: int,
    label: str,
    description: str,
    owner: str,
    action: str,
) -> None:
    gaps.append(
        GrainGap(
            gap_id=f"grain_gap_{len(gaps) + 1:04d}",
            severity=severity,
            gap_type=gap_type,
            source_file=source_file,
            line_number=line_number,
            label=label,
            description=description,
            recommended_owner=owner,
            recommended_next_action=action,
        )
    )


def scan_file(path: Path) -> tuple[list[Grain], list[GrainGap], Counter[str]]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    source = rel(path)
    line_to_label = build_line_to_label(lines)
    grains: list[Grain] = []
    gaps: list[GrainGap] = []
    tag_counts: Counter[str] = Counter()

    seen_ids: dict[str, int] = {}
    pending_tags: dict[str, dict[str, str]] = {}
    menus_with_state: list[tuple[int, str, str]] = []
    untagged_balance_gates: list[tuple[int, str, str]] = []

    def register_grain(grain: Grain) -> None:
        if grain.grain_id in seen_ids:
            append_gap(
                gaps,
                severity="blocker",
                gap_type="duplicate_grain_id",
                source_file=source,
                line_number=grain.line_number,
                label=grain.label,
                description=f"Duplicate grain id `{grain.grain_id}`.",
                owner="Grain Tagger",
                action="Rename one grain or merge boundaries.",
            )
        seen_ids[grain.grain_id] = grain.line_number
        grains.append(grain)

    for idx, line in enumerate(lines):
        label = label_at_line(line_to_label, idx)
        stripped = line.strip()

        parsed = parse_dag_line(line)
        if parsed:
            tag_type, attrs = parsed
            tag_counts[tag_type] += 1
            if is_illegal_tag_context(lines, idx):
                append_gap(
                    gaps,
                    severity="blocker",
                    gap_type="illegal_tag_placement",
                    source_file=source,
                    line_number=idx + 1,
                    label=label,
                    description=f"{tag_type} tag appears in forbidden context.",
                    owner="Grain Tagger",
                    action="Move tag directly above target label/menu/gate boundary.",
                )
            pending_tags[tag_type] = attrs
            continue

        label_match = LABEL_RE.match(line)
        if label_match:
            label_name = label_match.group(1)
            dag = pending_tags.pop("DAG_GRAIN", {})
            day, period = infer_day_period(label_name)
            grain_type = str(dag.get("type") or infer_grain_type_from_block("\n".join(lines[idx : idx + 40]), label_name) or "spine")
            grain_id = str(dag.get("id") or label_name)
            register_grain(
                Grain(
                    grain_id=grain_id,
                    grain_type=grain_type,
                    label=label_name,
                    day=str(dag.get("day") or day),
                    period=str(dag.get("period") or period),
                    capture=str(dag.get("capture", "")),
                    source_file=source,
                    line_number=idx + 1,
                    inference="dag_grain" if dag else "label",
                    confidence="high" if dag else "medium",
                    tag_type="DAG_GRAIN" if dag else "",
                )
            )
            pending_tags.clear()
            continue

        if MENU_RE.match(line):
            dag = pending_tags.pop("DAG_CHOICE", {})
            choice_id = str(dag.get("id") or f"{label}_menu_{idx + 1}")
            register_grain(
                Grain(
                    grain_id=choice_id,
                    grain_type="choice",
                    label=label,
                    day=str(dag.get("day") or infer_day_period(label)[0]),
                    period=str(dag.get("period") or infer_day_period(label)[1]),
                    source_file=source,
                    line_number=idx + 1,
                    parent_label=label,
                    inference="dag_choice" if dag else "menu",
                    confidence="high" if dag else "medium",
                    tag_type="DAG_CHOICE" if dag else "",
                )
            )
            pending_tags.clear()
            continue

        if_match = IF_RE.match(line)
        if if_match:
            condition = if_match.group(2).strip()
            if any(snippet in condition for snippet in WRITE_GATE_SNIPPETS + DEADLINE_SNIPPETS):
                dag = pending_tags.pop("DAG_GATE", {})
                normalized, conf = normalize_condition(condition)
                gate_type = str(dag.get("type") or ("write_gate" if "has_story_fuel" in condition or "attempt_write" in condition else "deadline_gate"))
                grain_id = str(dag.get("id") or f"{label}_gate_{idx + 1}")
                register_grain(
                    Grain(
                        grain_id=grain_id,
                        grain_type=gate_type,
                        label=label,
                        day=str(dag.get("day") or infer_day_period(label)[0]),
                        period=str(dag.get("period") or infer_day_period(label)[1]),
                        source_file=source,
                        line_number=idx + 1,
                        parent_label=label,
                        condition=normalized,
                        inference="dag_gate" if dag else "if_gate",
                        confidence="high" if dag else conf,
                        tag_type="DAG_GATE" if dag else "",
                    )
                )
                if not dag:
                    untagged_balance_gates.append((idx + 1, label, condition))
            pending_tags.clear()
            continue

        if JUMP_FAIL_RE.match(line):
            target = JUMP_FAIL_RE.match(line).group(1)
            register_grain(
                Grain(
                    grain_id=f"{label}_to_{target}",
                    grain_type="ending",
                    label=label,
                    day=infer_day_period(label)[0],
                    period=infer_day_period(label)[1],
                    source_file=source,
                    line_number=idx + 1,
                    parent_label=label,
                    condition=f"jump {target}",
                    inference="jump_fail",
                    confidence="high",
                )
            )

        if CALL_BOOK_RE.match(line):
            register_grain(
                Grain(
                    grain_id=f"{label}_book1_write_{idx + 1}",
                    grain_type="book1",
                    label=label,
                    day=infer_day_period(label)[0],
                    period=infer_day_period(label)[1],
                    source_file=source,
                    line_number=idx + 1,
                    parent_label=label,
                    inference="book1_call",
                    confidence="high",
                )
            )

        complete_match = COMPLETE_MS_RE.search(line)
        if complete_match:
            chapter = complete_match.group(1)
            register_grain(
                Grain(
                    grain_id=f"{label}_manuscript_{chapter}",
                    grain_type="book1",
                    label=label,
                    day=infer_day_period(label)[0],
                    period=infer_day_period(label)[1],
                    source_file=source,
                    line_number=idx + 1,
                    parent_label=label,
                    condition=chapter,
                    inference="manuscript_progress",
                    confidence="high",
                )
            )

        if "apply_effects(" in stripped or "story.set_" in stripped:
            if idx > 0 and parse_dag_line(lines[idx - 1]) and parse_dag_line(lines[idx - 1])[0] == "DAG_CHOICE":
                menus_with_state.append((idx + 1, label, stripped[:80]))

    for line_no, label, condition in untagged_balance_gates:
        append_gap(
            gaps,
            severity="major",
            gap_type="untagged_balance_gate",
            source_file=source,
            line_number=line_no,
            label=label,
            description=f"Balancing gate without DAG_GATE tag: `{condition[:120]}`.",
            owner="Grain Tagger",
            action="Add DAG_GATE above the if/elif once grain id is stable.",
        )

    for line_no, label, _ in menus_with_state:
        append_gap(
            gaps,
            severity="warning",
            gap_type="untagged_choice_with_state",
            source_file=source,
            line_number=line_no,
            label=label,
            description="Menu branch mutates state but no explicit DAG_CHOICE axis metadata on preceding tag.",
            owner="Grain Tagger",
            action="Confirm choice group is catalogued or add DAG_CHOICE metadata.",
        )

    return grains, gaps, tag_counts


def scan_scripts(files: list[Path]) -> dict[str, Any]:
    all_grains: list[Grain] = []
    all_gaps: list[GrainGap] = []
    tag_counts: Counter[str] = Counter()
    for path in files:
        grains, gaps, counts = scan_file(path)
        all_grains.extend(grains)
        all_gaps.extend(gaps)
        tag_counts.update(counts)

    by_type = Counter(g.grain_type for g in all_grains)
    by_day = Counter(g.day for g in all_grains if g.day)

    required_types = {"write_gate", "deadline_gate", "ending", "book1", "consequence_window"}
    missing_types = sorted(required_types - set(by_type))
    for grain_type in missing_types:
        append_gap(
            all_gaps,
            severity="major",
            gap_type="missing_grain_type",
            source_file="",
            line_number=0,
            label="",
            description=f"No grains of type `{grain_type}` inferred in scanned files.",
            owner="Balancing Pass",
            action="Confirm implementation exists or extend inference rules.",
        )

    return {
        "grains": all_grains,
        "gaps": all_gaps,
        "tag_counts": dict(tag_counts),
        "counts": {
            "grains": len(all_grains),
            "gaps": len(all_gaps),
            "by_type": dict(by_type),
            "by_day": dict(by_day),
        },
    }


def write_outputs(release: str, out_dir: Path, files: list[Path], data: dict[str, Any]) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    prefix = "release1"
    grains: list[Grain] = data["grains"]
    gaps: list[GrainGap] = data["gaps"]

    manifest = {
        "release": release,
        "source_files": [rel(path) for path in files],
        "grain_count": len(grains),
        "gap_count": len(gaps),
        "tag_counts": data["tag_counts"],
        "counts": data["counts"],
        "grains": [grain.to_row() for grain in grains],
    }
    (out_dir / f"{prefix}_grain_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )

    fieldnames = list(Grain("", "").to_row().keys())
    with (out_dir / f"{prefix}_grains.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for grain in grains:
            writer.writerow(grain.to_row())

    gap_md = [
        "# Release 1 Grain Gaps",
        "",
        f"- Release: `{release}`",
        f"- Grains extracted: {len(grains)}",
        f"- Gaps found: {len(gaps)}",
        "",
    ]
    blockers = [g for g in gaps if g.severity == "blocker"]
    majors = [g for g in gaps if g.severity == "major"]
    warnings = [g for g in gaps if g.severity == "warning"]

    for title, rows in (
        ("Blockers", blockers),
        ("Major", majors),
        ("Warnings", warnings),
    ):
        gap_md.extend([f"## {title}", ""])
        if not rows:
            gap_md.append("No findings.")
            gap_md.append("")
            continue
        for gap in rows:
            gap_md.extend(
                [
                    f"### {gap.gap_id} — {gap.gap_type}",
                    "",
                    f"- Severity: **{gap.severity}**",
                    f"- Source: `{gap.source_file or 'n/a'}:{gap.line_number or 'n/a'}`",
                    f"- Label: `{gap.label or 'n/a'}`",
                    f"- Description: {gap.description}",
                    f"- Owner: {gap.recommended_owner}",
                    f"- Next action: {gap.recommended_next_action}",
                    "",
                ]
            )

    (out_dir / f"{prefix}_grain_gaps.md").write_text("\n".join(gap_md), encoding="utf-8")


def collect_files(script_dir: Path, shared_dir: Path) -> list[Path]:
    files = sorted(script_dir.glob("*.rpy")) + sorted(shared_dir.glob("*.rpy"))
    return [path for path in files if "test_" not in path.name]


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Release 1 balance grain manifest.")
    parser.add_argument("--release", default=DEFAULT_RELEASE)
    parser.add_argument(
        "--out-dir",
        default=f"main-game/pipeline/releases/{DEFAULT_RELEASE}/grain",
    )
    parser.add_argument("--script-dir")
    parser.add_argument("--shared-dir")
    args = parser.parse_args()

    script_dir = Path(args.script_dir) if args.script_dir else ROOT / "main-game" / "non-prod-game" / "game" / "days"
    shared_dir = Path(args.shared_dir) if args.shared_dir else ROOT / "main-game" / "non-prod-game" / "game" / "shared"
    out_dir = Path(args.out_dir)
    if not script_dir.is_absolute():
        script_dir = ROOT / script_dir
    if not shared_dir.is_absolute():
        shared_dir = ROOT / shared_dir
    if not out_dir.is_absolute():
        out_dir = ROOT / out_dir

    files = collect_files(script_dir, shared_dir)
    if not files:
        print("No .rpy files found for grain extraction.", file=sys.stderr)
        return 1

    data = scan_scripts(files)
    write_outputs(args.release, out_dir, files, data)
    blockers = sum(1 for gap in data["gaps"] if gap.severity == "blocker")
    print(f"Grain manifest written ({data['counts']['grains']} grains, {blockers} blockers).")
    return 1 if blockers else 0


if __name__ == "__main__":
    raise SystemExit(main())
