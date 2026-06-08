#!/usr/bin/env python3
"""Build a static graph manifest from Release 1 non-canon Ren'Py drafts.

Phase 1 is intentionally line-based: it extracts labels, menus, jumps, calls,
effects, router outcomes, DAG comments, and review gaps without executing Ren'Py.
"""

from __future__ import annotations

import argparse
import ast
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_RELEASE = "release-1-mvp"

LABEL_RE = re.compile(r"^label\s+([A-Za-z_]\w*)(?:\([^)]*\))?:")
DAG_RE = re.compile(r"#\s*\[(DAG_[A-Z_]+)\s+([^\]]*)\]")
MENU_RE = re.compile(r"^(?P<indent>\s*)menu\s*:")
MENU_OPTION_RE = re.compile(r'^(?P<indent>\s*)"(?P<text>[^"]+)"(?:\s+if\s+(?P<condition>[^:]+))?:\s*$')
JUMP_RE = re.compile(r"^\s*jump\s+([A-Za-z_]\w*)\s*$")
JUMP_EXPR_RE = re.compile(r"^\s*jump\s+expression\s+(.+)$")
CALL_RE = re.compile(r"^\s*call\s+([A-Za-z_]\w*)(?:\((.*)\))?")
END_SLOT_RE = re.compile(r'^\s*call\s+end_slot\(outcome="([^"]+)"\)')
APPLY_RE = re.compile(r"\$?\s*apply_effects\((.*)\)")
SETTER_RE = re.compile(r'\$?\s*story\.(set_[A-Za-z_]\w*)\(([^)]*)\)')
CHAIN_AVAILABLE_RE = re.compile(r'story\.chain_available\("([^"]+)"\)')
RESOLVE_CHAIN_RE = re.compile(r'story\.resolve_chain_label\("([^"]+)"\)')
COMPLETE_CHAIN_RE = re.compile(r'story\.complete_chain_beat\("([^"]+)"\)')
IF_RE = re.compile(r"^\s*(if|elif)\s+(.+):\s*$")
ROUTE_ENTRY_RE = re.compile(r'"([^"]+)":\s*\(([^)]*)\)')
PENANCE_ENTRY_RE = re.compile(r'\((\d+),\s*"([^"]+)"\):\s*\(([^)]*)\)')

EFFECT_FIELD_MAP = {
    "insp": "inspiration_delta",
    "corr": "corruption_delta",
    "stern_susp": "stern_acute_susp_delta",
    "vance_susp": "vance_acute_susp_delta",
    "missy_susp": "missy_acute_susp_delta",
    "gideon_susp": "gideon_acute_susp_delta",
    "stern_base": "stern_base_susp_delta",
    "vance_base": "vance_base_susp_delta",
    "missy_base": "missy_base_susp_delta",
    "gideon_base": "gideon_base_susp_delta",
}

RELEVANT_GATE_SNIPPETS = (
    "player.anxiety",
    "has_story_fuel",
    "story.manuscript_progress",
    "player.inspiration",
    "story.chain_available",
    "player.is_confrontation_ready",
)


@dataclass
class Node:
    node_id: str
    label: str
    node_type: str
    day: str = ""
    period: str = ""
    slot: str = ""
    source_file: str = ""
    line_number: int = 0
    has_dag_node_tag: bool = False
    has_menu: bool = False
    has_check_confrontations: bool = False
    has_end_slot: bool = False
    has_apply_effects: bool = False
    confidence: str = "medium"


@dataclass
class Edge:
    edge_id: str
    from_label: str
    to_label: str
    edge_type: str
    condition: str = ""
    branch_option: str = ""
    router_outcome: str = ""
    source_file: str = ""
    line_number: int = 0
    confidence: str = "medium"


@dataclass
class Choice:
    choice_id: str
    label: str
    choice_group: str
    option_key: str
    menu_text: str
    sets_state: str = ""
    apply_effects_raw: str = ""
    effects_mapped: str = ""
    jump_to: str = ""
    source_file: str = ""
    line_number: int = 0
    has_dag_choice_tag: bool = False
    has_dag_branch_tag: bool = False
    stat_effects_known: str = "unknown"
    confidence: str = "low"


@dataclass
class Gate:
    gate_id: str
    label: str
    gate_type: str
    condition: str
    pass_to: str = ""
    fail_to: str = ""
    source_file: str = ""
    line_number: int = 0
    has_dag_gate_tag: bool = False
    confidence: str = "medium"


@dataclass
class Effect:
    effect_id: str
    label: str
    branch_option: str
    raw_call: str
    source_file: str
    line_number: int
    confidence: str = "medium"
    values: dict[str, str] = field(default_factory=dict)
    unmapped_fields: list[str] = field(default_factory=list)


@dataclass
class Gap:
    gap_id: str
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


def parse_dag_attrs(raw: str) -> dict[str, str | bool]:
    attrs: dict[str, str | bool] = {}
    for token in re.findall(r'(\w+)="[^"]*"|\w+=[^\s]+|\w+', raw):
        pass
    for match in re.finditer(r'(\w+)="([^"]*)"|(\w+)=([^\s]+)|(\w+)', raw):
        if match.group(1):
            attrs[match.group(1)] = match.group(2)
        elif match.group(3):
            attrs[match.group(3)] = match.group(4)
        elif match.group(5):
            attrs[match.group(5)] = True
    return attrs


def split_args(raw: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for part in re.split(r",(?![^\(]*\))", raw):
        part = part.strip()
        if not part or "=" not in part:
            continue
        key, value = part.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def infer_node_type(label: str, dag_attrs: dict[str, Any], lines: list[str], start: int, end: int) -> str:
    if isinstance(dag_attrs.get("type"), str):
        value = str(dag_attrs["type"])
        if value in {"work", "choice", "reflect", "write", "chain", "penance_check", "router", "hard_fail", "unknown"}:
            return value
    if label == "check_confrontations":
        return "penance_check"
    if label in {"advance_after_confrontation", "end_slot"} or label.startswith("end_slot"):
        return "router"
    if label.startswith("game_over_") or label.startswith("bad_ending"):
        return "hard_fail"
    if label.startswith("confrontation_"):
        return "penance"
    if re.match(r"^(stern|missy|vance)_chain_\d+$", label):
        return "chain"
    block = "\n".join(lines[start:end])
    if "book1_write_chapter" in block or "manuscript" in label or "write" in label or "writing" in label:
        return "write"
    if "menu:" in block or "choice" in label or "coras_choice" in label:
        return "choice"
    return "work" if label.startswith("day") else "unknown"


def parse_tuple(raw: str) -> list[str]:
    normalized = "(" + raw.replace("None", "None") + ")"
    try:
        parsed = ast.literal_eval(normalized)
    except Exception:
        return [part.strip().strip('"') for part in raw.split(",")]
    if not isinstance(parsed, tuple):
        return []
    return ["" if item is None else str(item) for item in parsed]


def extract_routes(classes_path: Path) -> tuple[dict[str, tuple[str, str, str]], dict[str, tuple[str, str, str]]]:
    text = classes_path.read_text(encoding="utf-8")
    slot_routes: dict[str, tuple[str, str, str]] = {}
    penance_routes: dict[str, tuple[str, str, str]] = {}
    for name, store, regex in (
        ("SLOT_EXIT_ROUTES", slot_routes, ROUTE_ENTRY_RE),
        ("POST_PENANCE_ROUTES", penance_routes, PENANCE_ENTRY_RE),
    ):
        start = text.find(name + " = {")
        if start < 0:
            continue
        end = text.find("\n        }", start)
        block = text[start:end]
        for match in regex.finditer(block):
            if name == "SLOT_EXIT_ROUTES":
                outcome = match.group(1)
                values = parse_tuple(match.group(2))
                if len(values) >= 3:
                    store[outcome] = (values[0], values[1], values[2])
            else:
                outcome = f"penance:{match.group(1)}:{match.group(2)}"
                values = parse_tuple(match.group(3))
                if len(values) >= 3:
                    store[outcome] = (values[0], values[1], values[2])
    return slot_routes, penance_routes


def label_ranges(lines: list[str]) -> list[tuple[str, int, int]]:
    found: list[tuple[str, int, int]] = []
    for idx, line in enumerate(lines):
        match = LABEL_RE.match(line)
        if match:
            found.append((match.group(1), idx, len(lines)))
    for i in range(len(found) - 1):
        label, start, _ = found[i]
        found[i] = (label, start, found[i + 1][1])
    return found


def append_gap(gaps: list[Gap], gap_type: str, source_file: str, line_number: int, label: str, description: str, owner: str, action: str) -> None:
    gaps.append(
        Gap(
            gap_id=f"gap_{len(gaps) + 1:04d}",
            gap_type=gap_type,
            source_file=source_file,
            line_number=line_number,
            label=label,
            description=description,
            recommended_owner=owner,
            recommended_next_action=action,
        )
    )


def scan_scripts(files: list[Path]) -> dict[str, Any]:
    nodes: dict[str, Node] = {}
    edges: list[Edge] = []
    choices: list[Choice] = []
    gates: list[Gate] = []
    effects: list[Effect] = []
    gaps: list[Gap] = []
    dag_counts: Counter[str] = Counter()
    marker_counts: Counter[str] = Counter()
    end_slot_call_sites: dict[str, list[str]] = defaultdict(list)
    penance_summary = {
        "interrupt_id": "check_confrontations",
        "trigger": "",
        "confrontation_targets": [],
        "hard_fail_target": "",
        "post_penance_router": "advance_after_confrontation",
        "confidence": "medium",
    }

    for path in files:
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        source = rel(path)
        ranges = label_ranges(lines)
        line_to_label = {}
        for label, start, end in ranges:
            for idx in range(start, end):
                line_to_label[idx] = label

        pending_dag: dict[str, dict[str, Any]] = {}
        label_menu_count: Counter[str] = Counter()
        current_menu_group = ""
        current_label = "file"
        last_choice: Choice | None = None

        for label, start, end in ranges:
            dag_attrs: dict[str, Any] = {}
            has_dag = False
            if start > 0:
                for lookback in range(max(0, start - 3), start):
                    match = DAG_RE.search(lines[lookback])
                    if match and match.group(1) == "DAG_NODE":
                        dag_attrs = parse_dag_attrs(match.group(2))
                        has_dag = True
            day = str(dag_attrs.get("day", ""))
            if not day:
                day_match = re.match(r"day(\d{3})", label)
                day = day_match.group(1) if day_match else ""
            block = lines[start:end]
            node = Node(
                node_id=str(dag_attrs.get("id", label)),
                label=label,
                node_type=infer_node_type(label, dag_attrs, lines, start, end),
                day=day,
                period=str(dag_attrs.get("period", "")),
                slot=str(dag_attrs.get("slot", "")),
                source_file=source,
                line_number=start + 1,
                has_dag_node_tag=has_dag,
                has_menu=any(MENU_RE.match(line) for line in block),
                has_check_confrontations=any("call check_confrontations" in line for line in block),
                has_end_slot=any("call end_slot" in line for line in block),
                has_apply_effects=any("apply_effects(" in line for line in block),
                confidence="high" if has_dag else "medium",
            )
            nodes[label] = node
            if node.node_type == "chain":
                if not any(COMPLETE_CHAIN_RE.search(line) for line in block):
                    append_gap(gaps, "chain label has no complete_chain_beat", source, start + 1, label, "Optional chain label does not complete its chain beat.", "Non-Prod Code Agent", "Confirm whether this chain should advance state.")
                if not any("apply_effects(" in line for line in block):
                    append_gap(gaps, "chain label has no apply_effects", source, start + 1, label, "Optional chain label has no stat/effect call.", "Balancing Pass", "Add or explicitly document no-op effect.")
                append_gap(gaps, "chain label has no explicit slot availability/window", source, start + 1, label, "Phase 1 cannot infer appointment windows from chain labels alone.", "Human Designer", "Document slot availability or add DAG metadata.")

        for idx, line in enumerate(lines):
            current_label = line_to_label.get(idx, current_label)
            stripped = line.strip()

            for marker in ("[STATE]", "[CHOICE]", "[BEAT]", "[ASSET]"):
                if marker in line:
                    marker_counts[marker.strip("[]")] += 1

            dag_match = DAG_RE.search(line)
            if dag_match:
                tag_type = dag_match.group(1)
                dag_counts[tag_type] += 1
                pending_dag[tag_type] = parse_dag_attrs(dag_match.group(2))
                if pending_dag[tag_type].get("manual"):
                    append_gap(gaps, "manual_dag_tag_preserved", source, idx + 1, current_label, f"Manual {tag_type} tag preserved.", "Human Designer", "Use explicit overwrite-manual DAG request to update this tag.")
                continue

            menu_match = MENU_RE.match(line)
            if menu_match:
                label_menu_count[current_label] += 1
                attrs = pending_dag.pop("DAG_CHOICE", {})
                current_menu_group = str(attrs.get("group", f"{current_label}_menu_{label_menu_count[current_label]}"))
                if current_label in nodes:
                    nodes[current_label].has_menu = True
                if not attrs:
                    append_gap(gaps, "missing_dag_choice_tag", source, idx + 1, current_label, "Menu has no adjacent DAG_CHOICE tag.", "Create/Rewrite Day Workflow", "Add DAG_CHOICE beside the existing CHOICE marker.")
                continue

            option_match = MENU_OPTION_RE.match(line)
            if option_match and current_menu_group:
                option_key = f"option_{len([c for c in choices if c.label == current_label and c.choice_group == current_menu_group]) + 1}"
                hint = re.search(r"\[\[([^\]]+)\]\]", option_match.group("text"))
                if hint:
                    option_key = re.sub(r"\W+", "_", hint.group(1).strip().lower()).strip("_")[:48] or option_key
                branch_attrs = pending_dag.pop("DAG_BRANCH", {})
                if branch_attrs.get("option"):
                    option_key = str(branch_attrs["option"])
                choice = Choice(
                    choice_id=f"choice_{len(choices) + 1:04d}",
                    label=current_label,
                    choice_group=current_menu_group,
                    option_key=option_key,
                    menu_text=option_match.group("text"),
                    source_file=source,
                    line_number=idx + 1,
                    has_dag_choice_tag=True,
                    has_dag_branch_tag=bool(branch_attrs),
                    confidence="medium" if current_menu_group else "low",
                )
                choices.append(choice)
                last_choice = choice
                continue

            if setter := SETTER_RE.search(line):
                if last_choice and last_choice.label == current_label:
                    last_choice.sets_state = f"story.{setter.group(1)}({setter.group(2)})"

            if effect_match := APPLY_RE.search(line):
                raw_args = effect_match.group(1)
                values = split_args(raw_args)
                mapped: dict[str, str] = {}
                unmapped: list[str] = []
                for key, value in values.items():
                    if key == "susp":
                        append_gap(gaps, "deprecated_generic_suspicion_usage", source, idx + 1, current_label, "apply_effects() uses deprecated generic susp field.", "Non-Prod Code Agent", "Replace with character-specific suspicion field.")
                        unmapped.append(key)
                    elif key in EFFECT_FIELD_MAP:
                        mapped[EFFECT_FIELD_MAP[key]] = value
                    else:
                        unmapped.append(key)
                if unmapped:
                    append_gap(gaps, "unmapped_effect_fields", source, idx + 1, current_label, f"Unmapped apply_effects fields: {', '.join(unmapped)}.", "Balancing Pass", "Confirm runtime effect mapping.")
                effect = Effect(
                    effect_id=f"effect_{len(effects) + 1:04d}",
                    label=current_label,
                    branch_option=last_choice.option_key if last_choice and last_choice.label == current_label else "",
                    raw_call=f"apply_effects({raw_args})",
                    source_file=source,
                    line_number=idx + 1,
                    values=mapped,
                    unmapped_fields=unmapped,
                )
                effects.append(effect)
                if current_label in nodes:
                    nodes[current_label].has_apply_effects = True
                if last_choice and last_choice.label == current_label:
                    last_choice.apply_effects_raw = effect.raw_call
                    last_choice.effects_mapped = json.dumps(mapped, sort_keys=True)
                    last_choice.stat_effects_known = "yes" if mapped and not unmapped else "partial"

            if gate_match := IF_RE.match(line):
                condition = gate_match.group(2).strip()
                if any(snippet in condition for snippet in RELEVANT_GATE_SNIPPETS):
                    gate_type = "condition"
                    if "anxiety" in condition:
                        gate_type = "anxiety"
                    elif "has_story_fuel" in condition or "inspiration" in condition:
                        gate_type = "writing_fuel"
                    elif "chain_available" in condition:
                        gate_type = "chain_available"
                    elif "is_confrontation_ready" in condition:
                        gate_type = "confrontation"
                    gates.append(
                        Gate(
                            gate_id=f"gate_{len(gates) + 1:04d}",
                            label=current_label,
                            gate_type=gate_type,
                            condition=condition,
                            source_file=source,
                            line_number=idx + 1,
                            has_dag_gate_tag="DAG_GATE" in pending_dag,
                            confidence="medium",
                        )
                    )
                    if "DAG_GATE" not in pending_dag:
                        append_gap(gaps, "missing_dag_gate_tag", source, idx + 1, current_label, "Flow-affecting condition has no DAG_GATE tag.", "Create/Rewrite Day Workflow", "Add DAG_GATE metadata if this gate is balancing-relevant.")

            if jump_match := JUMP_RE.match(line):
                target = jump_match.group(1)
                edges.append(Edge(f"edge_{len(edges) + 1:04d}", current_label, target, "jump", source_file=source, line_number=idx + 1, confidence="high"))
                if last_choice and last_choice.label == current_label and not last_choice.jump_to:
                    last_choice.jump_to = target

            if jump_expr_match := JUMP_EXPR_RE.match(line):
                expr = jump_expr_match.group(1).strip()
                target = "dynamic:story.resolve_chain_label(character)" if "_chain_label" in expr else f"dynamic:{expr}"
                edges.append(Edge(f"edge_{len(edges) + 1:04d}", current_label, target, "jump_expression", source_file=source, line_number=idx + 1, confidence="low"))
                append_gap(gaps, "dynamic_jump_targets", source, idx + 1, current_label, f"Dynamic jump target: {expr}.", "Chief Architect", "Confirm extractor/simulator can resolve this dynamic edge.")

            if end_slot_match := END_SLOT_RE.match(line):
                outcome = end_slot_match.group(1)
                end_slot_call_sites[outcome].append(f"{source}:{idx + 1}")
                edges.append(Edge(f"edge_{len(edges) + 1:04d}", current_label, "router:end_slot", "router", router_outcome=outcome, source_file=source, line_number=idx + 1, confidence="high"))
                if current_label in nodes:
                    nodes[current_label].has_end_slot = True
                if last_choice and last_choice.label == current_label and not last_choice.jump_to:
                    last_choice.jump_to = f"router:{outcome}"

            if call_match := CALL_RE.match(line):
                call_name = call_match.group(1)
                if call_name == "check_confrontations":
                    if current_label in nodes:
                        nodes[current_label].has_check_confrontations = True
                    edges.append(Edge(f"edge_{len(edges) + 1:04d}", current_label, "check_confrontations", "penance", source_file=source, line_number=idx + 1, confidence="high"))
                elif call_name == "book1_write_chapter":
                    edges.append(Edge(f"edge_{len(edges) + 1:04d}", current_label, "book1_write_chapter", "call", source_file=source, line_number=idx + 1, confidence="medium"))

            if available := CHAIN_AVAILABLE_RE.search(line):
                append_gap(gaps, "optional_chain_window_gaps", source, idx + 1, current_label, f"Chain availability for {available.group(1)} lacks explicit slot/window metadata.", "Human Designer", "Add DAG metadata for chain windows.")
            if RESOLVE_CHAIN_RE.search(line):
                append_gap(gaps, "dynamic_jump_targets", source, idx + 1, current_label, "story.resolve_chain_label() creates dynamic chain target.", "Chief Architect", "Resolve dynamically in future simulator.")

            if current_label == "check_confrontations":
                if "player.anxiety >= 100" in line:
                    penance_summary["trigger"] = "anxiety >= 100 or individual character confrontation threshold"
                if 'player.is_confrontation_ready("' in line:
                    char = re.search(r'player\.is_confrontation_ready\("([^"]+)"\)', line)
                    if char:
                        penance_summary["confrontation_targets"].append(char.group(1))
                if "jump game_over_dismissed" in line:
                    penance_summary["hard_fail_target"] = "game_over_dismissed"

    return {
        "nodes": list(nodes.values()),
        "edges": edges,
        "choices": choices,
        "gates": gates,
        "effects": effects,
        "gaps": gaps,
        "dag_counts": dag_counts,
        "marker_counts": marker_counts,
        "end_slot_call_sites": dict(end_slot_call_sites),
        "penance_summary": penance_summary,
    }


def storyboard_labels(storyboard: Path) -> set[str]:
    if not storyboard or not storyboard.exists():
        return set()
    text = storyboard.read_text(encoding="utf-8")
    return set(re.findall(r"`([A-Za-z_]\w*)`", text))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def write_outputs(args: argparse.Namespace, data: dict[str, Any], slot_routes: dict[str, tuple[str, str, str]], penance_routes: dict[str, tuple[str, str, str]], files: list[Path]) -> None:
    out_dir = Path(args.out_dir)
    if not out_dir.is_absolute():
        out_dir = ROOT / out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    nodes: list[Node] = data["nodes"]
    edges: list[Edge] = data["edges"]
    choices: list[Choice] = data["choices"]
    gates: list[Gate] = data["gates"]
    effects: list[Effect] = data["effects"]
    gaps: list[Gap] = data["gaps"]
    call_sites: dict[str, list[str]] = data["end_slot_call_sites"]

    for outcome, sites in call_sites.items():
        if outcome not in slot_routes:
            append_gap(gaps, "router_outcome_mismatches", "", 0, "end_slot", f"Outcome {outcome} is called but not defined in SLOT_EXIT_ROUTES.", "Chief Architect", "Add route or correct call site.")
    for outcome in slot_routes:
        if outcome not in call_sites:
            append_gap(gaps, "router_outcome_mismatches", "renpy_project/game/classes.rpy", 0, "StoryState.SLOT_EXIT_ROUTES", f"Outcome {outcome} has no extracted call site.", "Chief Architect", "Confirm unused route is expected.")

    if args.storyboard and not args.no_storyboard_audit:
        labels_in_board = storyboard_labels(Path(args.storyboard))
        script_labels = {node.label for node in nodes}
        for label in sorted(labels_in_board - script_labels):
            if label.startswith(("day", "stern_", "missy_", "vance_", "book1_", "game_over_")):
                append_gap(gaps, "storyboard_label_missing_from_scripts", rel(Path(args.storyboard)), 0, label, "Storyboard references a label not extracted from scripts.", "Documentation Steward", "Run storyboard_sync or correct the storyboard reference.")
        for label in sorted(script_labels - labels_in_board):
            if label.startswith("day10"):
                append_gap(gaps, "script_label_missing_from_storyboard", "", 0, label, "Script label not referenced in storyboard.", "Documentation Steward", "Run storyboard_sync if this label is planning-relevant.")

    prefix = "release1"
    manifest = {
        "release": args.release,
        "files_scanned": [rel(path) for path in files],
        "counts": {
            "nodes": len(nodes),
            "edges": len(edges),
            "choices": len(choices),
            "gates": len(gates),
            "effects": len(effects),
            "router_outcomes": len(slot_routes),
            "gaps": len(gaps),
        },
        "penance_summary": data["penance_summary"],
        "dag_tags": dict(data["dag_counts"]),
        "markers": dict(data["marker_counts"]),
    }
    (out_dir / f"{prefix}_graph_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    write_csv(
        out_dir / f"{prefix}_nodes.csv",
        ["node_id", "label", "node_type", "day", "period", "slot", "source_file", "line_number", "has_dag_node_tag", "has_menu", "has_check_confrontations", "has_end_slot", "has_apply_effects", "confidence"],
        [node.__dict__ for node in nodes],
    )
    write_csv(out_dir / f"{prefix}_edges.csv", ["edge_id", "from_label", "to_label", "edge_type", "condition", "branch_option", "router_outcome", "source_file", "line_number", "confidence"], [edge.__dict__ for edge in edges])
    write_csv(out_dir / f"{prefix}_choices.csv", ["choice_id", "label", "choice_group", "option_key", "menu_text", "sets_state", "apply_effects_raw", "effects_mapped", "jump_to", "source_file", "line_number", "has_dag_choice_tag", "has_dag_branch_tag", "stat_effects_known", "confidence"], [choice.__dict__ for choice in choices])
    write_csv(out_dir / f"{prefix}_gates.csv", ["gate_id", "label", "gate_type", "condition", "pass_to", "fail_to", "source_file", "line_number", "has_dag_gate_tag", "confidence"], [gate.__dict__ for gate in gates])
    effect_rows = []
    for effect in effects:
        row = {
            "effect_id": effect.effect_id,
            "label": effect.label,
            "branch_option": effect.branch_option,
            "raw_call": effect.raw_call,
            "source_file": effect.source_file,
            "line_number": effect.line_number,
            "confidence": effect.confidence,
            "unmapped_fields": ";".join(effect.unmapped_fields),
        }
        for field in EFFECT_FIELD_MAP.values():
            row[field] = effect.values.get(field, "")
        effect_rows.append(row)
    write_csv(out_dir / f"{prefix}_effects.csv", ["effect_id", "label", "branch_option", "raw_call", "inspiration_delta", "corruption_delta", "stern_acute_susp_delta", "stern_base_susp_delta", "vance_acute_susp_delta", "vance_base_susp_delta", "missy_acute_susp_delta", "missy_base_susp_delta", "gideon_acute_susp_delta", "gideon_base_susp_delta", "unmapped_fields", "source_file", "line_number", "confidence"], effect_rows)

    router_rows = []
    for outcome, route in {**slot_routes, **penance_routes}.items():
        router_rows.append(
            {
                "outcome": outcome,
                "target_day": route[0],
                "target_period": route[1],
                "target_label": route[2],
                "source": "StoryState.POST_PENANCE_ROUTES" if outcome.startswith("penance:") else "StoryState.SLOT_EXIT_ROUTES",
                "call_sites": ";".join(call_sites.get(outcome, [])),
                "confidence": "high",
            }
        )
    write_csv(out_dir / f"{prefix}_router_outcomes.csv", ["outcome", "target_day", "target_period", "target_label", "source", "call_sites", "confidence"], router_rows)

    gap_sections = [
        "Missing DAG Tags",
        "Ambiguous Choice Groups",
        "Missing / Incomplete apply_effects",
        "Deprecated Generic Suspicion Usage",
        "Unmapped Effect Fields",
        "Router Outcome Mismatches",
        "Dynamic Jump Targets",
        "Gate Pass/Fail Ambiguity",
        "Optional Chain Window Gaps",
        "Penance / Opportunity Cost Gaps",
        "Storyboard Drift Notes",
        "Manual DAG Tags Preserved",
    ]
    section_map = {
        "missing_dag": "Missing DAG Tags",
        "ambiguous": "Ambiguous Choice Groups",
        "apply_effects": "Missing / Incomplete apply_effects",
        "deprecated": "Deprecated Generic Suspicion Usage",
        "unmapped": "Unmapped Effect Fields",
        "router": "Router Outcome Mismatches",
        "dynamic": "Dynamic Jump Targets",
        "gate": "Gate Pass/Fail Ambiguity",
        "chain": "Optional Chain Window Gaps",
        "penance": "Penance / Opportunity Cost Gaps",
        "storyboard": "Storyboard Drift Notes",
        "manual": "Manual DAG Tags Preserved",
    }
    by_section: dict[str, list[Gap]] = defaultdict(list)
    for gap in gaps:
        section = "Penance / Opportunity Cost Gaps"
        for needle, target in section_map.items():
            if needle in gap.gap_type:
                section = target
                break
        by_section[section].append(gap)
    gap_md = ["# Release 1 Graph Gaps", ""]
    for section in gap_sections:
        gap_md.extend([f"## {section}", ""])
        rows = by_section.get(section, [])
        if not rows:
            gap_md.extend(["No findings.", ""])
            continue
        for gap in rows:
            gap_md.extend(
                [
                    f"### {gap.gap_id} - {gap.gap_type}",
                    "",
                    f"- Source: `{gap.source_file or 'n/a'}:{gap.line_number}`",
                    f"- Label: `{gap.label}`",
                    f"- Description: {gap.description}",
                    f"- Recommended owner: {gap.recommended_owner}",
                    f"- Recommended next action: {gap.recommended_next_action}",
                    "",
                ]
            )
    (out_dir / f"{prefix}_graph_gaps.md").write_text("\n".join(gap_md), encoding="utf-8")

    readiness = "Ready for first balancing spreadsheet skeleton" if nodes and effects and not any(g.gap_type == "router_outcome_mismatches" and "called but not defined" in g.description for g in gaps) else "Partial - graph skeleton usable, balancing inputs incomplete"
    audit = [
        "# Release 1 Graph Audit",
        "",
        f"- Files scanned: {len(files)}",
        f"- Labels found: {len(nodes)}",
        f"- Menus found: {sum(1 for node in nodes if node.has_menu)}",
        f"- Branches extracted: {len(choices)}",
        f"- apply_effects calls parsed: {len(effects)}",
        f"- Router outcomes found: {len(slot_routes)}",
        f"- Penance routes found: {len(penance_routes)}",
        f"- Gates found: {len(gates)}",
        f"- Chain labels found: {sum(1 for node in nodes if node.node_type == 'chain')}",
        f"- check_confrontations calls found: {sum(1 for node in nodes if node.has_check_confrontations)}",
        f"- DAG tags found by type: {dict(data['dag_counts'])}",
        f"- Gaps found by type: {dict(Counter(gap.gap_type for gap in gaps))}",
        f"- Readiness assessment: {readiness}",
        "",
    ]
    (out_dir / f"{prefix}_graph_audit.md").write_text("\n".join(audit), encoding="utf-8")

    mermaid = ["flowchart TD"]
    for edge in edges:
        if edge.edge_type not in {"jump", "router", "penance", "jump_expression"}:
            continue
        from_id = re.sub(r"\W+", "_", edge.from_label)
        to_id = re.sub(r"\W+", "_", edge.to_label)
        label = edge.router_outcome or edge.edge_type
        mermaid.append(f'  {from_id}["{edge.from_label}"] -->|"{label}"| {to_id}["{edge.to_label}"]')
        if len(mermaid) > 240:
            mermaid.append("  %% truncated for readability")
            break
    (out_dir / f"{prefix}_graph_mermaid.mmd").write_text("\n".join(mermaid) + "\n", encoding="utf-8")

    report = [
        "# Release 1 Graph Implementation Report",
        "",
        "## Files Created",
        "",
        *[f"- `{name}`" for name in [
            f"{prefix}_graph_manifest.json",
            f"{prefix}_nodes.csv",
            f"{prefix}_edges.csv",
            f"{prefix}_choices.csv",
            f"{prefix}_gates.csv",
            f"{prefix}_effects.csv",
            f"{prefix}_router_outcomes.csv",
            f"{prefix}_graph_gaps.md",
            f"{prefix}_graph_audit.md",
            f"{prefix}_graph_mermaid.mmd",
            f"{prefix}_graph_implementation_report.md",
        ]],
        "",
        "## Files Scanned",
        "",
        *[f"- `{rel(path)}`" for path in files],
        "",
        "## Commands Run",
        "",
        "- `py narrative/pipeline/tools/build_story_graph_manifest.py --release release-1-mvp --out-dir narrative/pipeline/releases/release-1-mvp/graph --storyboard narrative/draft/releases/release-1-mvp/planning/story_board.md`",
        "",
        "## Extraction Counts",
        "",
        f"- Nodes: {len(nodes)}",
        f"- Edges: {len(edges)}",
        f"- Choices: {len(choices)}",
        f"- Gates: {len(gates)}",
        f"- Effects: {len(effects)}",
        f"- Gaps: {len(gaps)}",
        "",
        "## Storyboard Audit",
        "",
        f"- Run: {'no' if args.no_storyboard_audit else 'yes'}",
        "",
        "## Recommended Next Owner",
        "",
        "- Balancing Pass / Human Designer for gap triage.",
        "",
    ]
    (out_dir / f"{prefix}_graph_implementation_report.md").write_text("\n".join(report), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Release 1 graph manifest from non-canon Ren'Py drafts.")
    parser.add_argument("--release", default=DEFAULT_RELEASE)
    parser.add_argument("--out-dir", default=f"narrative/pipeline/releases/{DEFAULT_RELEASE}/graph")
    parser.add_argument("--script-dir")
    parser.add_argument("--shared-dir")
    parser.add_argument("--storyboard")
    parser.add_argument("--no-storyboard-audit", action="store_true")
    parser.add_argument("--write-mermaid", action="store_true", help="Accepted for spec compatibility; Mermaid is always written.")
    args = parser.parse_args()

    script_dir = Path(args.script_dir) if args.script_dir else ROOT / "narrative" / "draft" / "releases" / args.release / "non_prod_renpy_project" / "game" / "days"
    shared_dir = Path(args.shared_dir) if args.shared_dir else ROOT / "narrative" / "draft" / "releases" / args.release / "non_prod_renpy_project" / "game" / "shared"
    if not script_dir.is_absolute():
        script_dir = ROOT / script_dir
    if not shared_dir.is_absolute():
        shared_dir = ROOT / shared_dir

    files = sorted(script_dir.glob("*.rpy")) + sorted(shared_dir.glob("*.rpy"))
    if not files:
        print("No .rpy files found for graph extraction.", file=sys.stderr)
        return 1

    data = scan_scripts(files)
    slot_routes, penance_routes = extract_routes(ROOT / "renpy_project" / "game" / "classes.rpy")
    write_outputs(args, data, slot_routes, penance_routes, files)
    print("Graph manifest written.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
