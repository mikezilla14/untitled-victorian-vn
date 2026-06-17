#!/usr/bin/env python3
"""
Resolve standup / backlog / checklist items to agent-ready work packets.

Agents start from daily_standup_report.md, then use this script to find specs,
skills, pipelines, and verification commands before taking action.

Usage:
  py scripts/resolve_work_item.py --from-standup
  py scripts/resolve_work_item.py --from-standup --next
  py scripts/resolve_work_item.py --task N-6
  py scripts/resolve_work_item.py --from-standup --format json
  py scripts/resolve_work_item.py --list-tasks
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "docs" / "backlog" / "task_registry.json"
BACKLOG_PATH = ROOT / "docs" / "backlog" / "mvp_backlog.md"
DEFAULT_STANDUP = (
    ROOT
    / "main-game"
    / "draft"
    / "releases"
    / "planning"
    / "daily_standup_report.md"
)
RULES_DIR = ROOT / ".agents" / "rules"
SKILLS_DIR = ROOT / ".agents" / "skills"


def load_registry() -> dict:
    try:
        scripts_dir = Path(__file__).resolve().parent
        if str(scripts_dir) not in sys.path:
            sys.path.insert(0, str(scripts_dir))
        from daily_standup import sync_backlog_to_registry
        sync_backlog_to_registry()
    except Exception as e:
        print(f"Warning: Backlog-to-registry sync failed during load: {e}")
        
    if not REGISTRY_PATH.exists():
        raise FileNotFoundError(f"Task registry missing: {REGISTRY_PATH}")
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def agent_rule_path(agent_slug: str) -> str:
    return f".agents/rules/{agent_slug}.md"


def skill_path(skill_slug: str) -> str:
    return f".agents/skills/{skill_slug}/SKILL.md"


def extract_standup_body(markdown: str) -> str:
    match = re.search(r"```text\n(.*?)```", markdown, re.DOTALL)
    return match.group(1) if match else markdown


def parse_standup_actions(standup_text: str) -> list[dict[str, Any]]:
    """Parse TODAY'S CRITICAL ACTIONS from standup plain-text body."""
    items: list[dict[str, Any]] = []
    in_actions = False
    priority = 0

    for line in standup_text.splitlines():
        if "TODAY'S CRITICAL ACTIONS" in line:
            in_actions = True
            continue
        if in_actions and line.strip().startswith("===="):
            break
        if not in_actions:
            continue

        stripped = line.strip()
        if not stripped or stripped.startswith("🎉"):
            continue

        # Numbered action lines: "   1. ..."
        num_match = re.match(r"^\d+\.\s+", stripped)
        if not num_match:
            continue

        priority += 1
        body = re.sub(r"^\d+\.\s+", "", stripped)

        backlog_match = re.search(r"\[([NC]-\d+)\]", body)
        if backlog_match:
            items.append(
                {
                    "priority": priority,
                    "kind": "backlog",
                    "registry_id": backlog_match.group(1),
                    "summary": body,
                }
            )
            continue

        if "[BLOCKED]" in body:
            items.append(
                {
                    "priority": priority,
                    "kind": "blocked",
                    "registry_id": "COMPILE_ERROR",
                    "summary": body,
                }
            )
            continue

        if "[CHECKLIST]" in body:
            checklist_body = body.split("[CHECKLIST]", 1)[-1].strip()
            registry_id = _match_checklist_registry_id(checklist_body)
            items.append(
                {
                    "priority": priority,
                    "kind": "checklist",
                    "registry_id": registry_id,
                    "summary": checklist_body,
                    "checklist_line": checklist_body,
                }
            )
            continue

        if "[DISCOVERED]" in body:
            discovered_body = body.split("[DISCOVERED]", 1)[-1].strip()
            if "scene direction" in discovered_body.lower():
                registry_id = "DISCOVERED_SCENE_DIR"
            elif "format" in discovered_body.lower():
                registry_id = "DISCOVERED_FORMAT"
            elif "historical" in discovered_body.lower():
                registry_id = "DISCOVERED_HISTORICAL"
            else:
                registry_id = "DISCOVERED_GENERIC"
                
            items.append(
                {
                    "priority": priority,
                    "kind": "discovered",
                    "registry_id": registry_id,
                    "summary": discovered_body,
                }
            )
            continue

        items.append(
            {
                "priority": priority,
                "kind": "unknown",
                "registry_id": None,
                "summary": body,
            }
        )

    return items


def _match_checklist_registry_id(checklist_line: str) -> str | None:
    registry = load_registry()
    for task_id, task in registry.get("tasks", {}).items():
        match_key = task.get("match_checklist")
        if match_key and match_key in checklist_line:
            return task_id
    phase_match = re.search(r"Phase\s+(\d+)", checklist_line, re.IGNORECASE)
    if phase_match:
        return f"PHASE_{phase_match.group(1)}"
    return None


def _phase_default_packet(phase_num: str, summary: str) -> dict[str, Any]:
    registry = load_registry()
    phase_key = f"Phase {phase_num}"
    defaults = registry.get("phase_defaults", {}).get(phase_key, {})
    agent = defaults.get("agent", "orchestrator")
    skill = defaults.get("skill", "orchestrator")
    return {
        "registry_id": f"PHASE_{phase_num}",
        "title": f"Checklist work — {phase_key}",
        "lane": defaults.get("lane", "integration"),
        "summary": summary,
        "agent": agent,
        "agent_rule": agent_rule_path(agent),
        "skill": skill,
        "skill_path": skill_path(skill),
        "pipeline": defaults.get("pipeline"),
        "pipeline_stage": defaults.get("pipeline_stage"),
        "specs": defaults.get("specs", []),
        "files": defaults.get("files", []),
        "deliverables": defaults.get("deliverables", []),
        "verify": defaults.get("verify", []),
        "blocked_by": [],
        "resolution": "phase_default",
        "backlog_excerpt": None,
    }


def _backlog_excerpt(task_id: str) -> str | None:
    if not BACKLOG_PATH.exists():
        return None
    content = BACKLOG_PATH.read_text(encoding="utf-8")
    pattern = rf"###\s+[🔴🟡🟢]\s+\[{re.escape(task_id)}\][^\n]*\n(.*?)(?=\n###\s+|\Z)"
    match = re.search(pattern, content, re.DOTALL)
    return match.group(0).strip() if match else None


def resolve_task(registry_id: str | None, summary: str = "") -> dict[str, Any]:
    registry = load_registry()

    if registry_id and registry_id.startswith("PHASE_"):
        return _phase_default_packet(registry_id.replace("PHASE_", ""), summary)

    if registry_id and registry_id.startswith("DISCOVERED_"):
        file_path = ""
        file_match = re.search(r"(?:for|in|Format|errors in)\s+(\S+\.rpy|\S+\.md)", summary)
        if file_match:
            file_path = file_match.group(1).strip()
            file_path = re.sub(r'[\(\)\`\'\"]', '', file_path).strip()
            
        if registry_id == "DISCOVERED_SCENE_DIR":
            return {
                "registry_id": registry_id,
                "title": f"Update scene direction for {file_path}",
                "lane": "code",
                "summary": summary,
                "agent": "scene_direction_agent",
                "agent_rule": agent_rule_path("scene_direction_agent"),
                "skill": "scene_direction",
                "skill_path": skill_path("scene_direction"),
                "files": [file_path] if file_path else [],
                "verify": [f"py scripts/scene_direction.py --files \"{file_path}\" --check"] if file_path else ["py scripts/scene_direction.py --check"],
                "action_note": f"Run scene direction agent: py scripts/scene_direction.py --files \"{file_path}\"",
                "resolution": "discovered_scene_dir",
                "deliverables": [],
                "specs": [
                    "docs/specs/scene-direction-agent.md",
                    "docs/contracts/sprite_layout_policy.yaml"
                ],
                "pipeline": None,
                "pipeline_stage": None,
                "blocked_by": [],
                "backlog_excerpt": None
            }
        elif registry_id == "DISCOVERED_FORMAT":
            return {
                "registry_id": registry_id,
                "title": f"Format file {file_path}",
                "lane": "prose",
                "agent": "writers_room",
                "agent_rule": agent_rule_path("writers_room"),
                "skill": "revise_narrative",
                "skill_path": skill_path("revise_narrative"),
                "files": [file_path] if file_path else [],
                "verify": [f"py scripts/format_non_canon.py --check \"{file_path}\""] if file_path else ["py scripts/format_non_canon.py --check"],
                "action_note": f"Run formatter: py scripts/format_non_canon.py \"{file_path}\"",
                "resolution": "discovered_format",
                "deliverables": [],
                "specs": [
                    "main-game/draft/releases/planning/mvp_systems_integration_checklist.md"
                ],
                "pipeline": None,
                "pipeline_stage": None,
                "blocked_by": [],
                "backlog_excerpt": None
            }
        elif registry_id == "DISCOVERED_HISTORICAL":
            return {
                "registry_id": registry_id,
                "title": f"Fix historical linter errors in {file_path}",
                "lane": "prose",
                "agent": "victorian_consultant",
                "agent_rule": agent_rule_path("victorian_consultant"),
                "skill": "historical_check",
                "skill_path": skill_path("historical_check"),
                "files": [file_path] if file_path else [],
                "verify": [f"py scripts/historical_linter.py --file \"{file_path}\""] if file_path else [],
                "action_note": f"Run historical linter: py scripts/historical_linter.py --file \"{file_path}\"",
                "resolution": "discovered_historical",
                "deliverables": [],
                "specs": [
                    "docs/backlog/mvp_backlog.md"
                ],
                "pipeline": None,
                "pipeline_stage": None,
                "blocked_by": [],
                "backlog_excerpt": None
            }

    task = registry.get("tasks", {}).get(registry_id or "")
    if not task:
        return {
            "registry_id": registry_id,
            "title": summary or "Unresolved work item",
            "lane": "unknown",
            "summary": summary,
            "agent": "orchestrator",
            "agent_rule": agent_rule_path("orchestrator"),
            "skill": "orchestrator",
            "skill_path": skill_path("orchestrator"),
            "pipeline": None,
            "pipeline_stage": None,
            "specs": [
                "docs/backlog/mvp_backlog.md",
                "main-game/draft/releases/planning/mvp_systems_integration_checklist.md",
                "docs/specs/README.md",
            ],
            "files": [],
            "deliverables": [],
            "verify": [],
            "blocked_by": [],
            "resolution": "fallback",
            "backlog_excerpt": None,
            "action_note": (
                "No registry entry matched. Search docs/backlog/mvp_backlog.md and "
                "planning/mvp_systems_integration_checklist.md for the task, then "
                "ask the human to add a task_registry.json entry if this repeats."
            ),
        }

    agent = task.get("agent", "orchestrator")
    skill = task.get("skill", "orchestrator")
    anchor = task.get("backlog_anchor", registry_id)

    packet: dict[str, Any] = {
        "registry_id": registry_id,
        "title": task.get("title", registry_id),
        "lane": task.get("lane", "integration"),
        "summary": summary,
        "agent": agent,
        "agent_rule": agent_rule_path(agent),
        "skill": skill,
        "skill_path": skill_path(skill),
        "pipeline": task.get("pipeline"),
        "pipeline_stage": task.get("pipeline_stage"),
        "specs": task.get("specs", []),
        "files": task.get("files", []),
        "deliverables": task.get("deliverables", []),
        "verify": task.get("verify", []),
        "blocked_by": task.get("blocked_by", []),
        "resolution": "registry",
        "backlog_excerpt": _backlog_excerpt(anchor) if anchor else None,
    }

    if registry_id == "COMPILE_ERROR" and summary:
        file_match = re.search(r"game/[^\s:]+\.rpy", summary)
        if file_match:
            rel = (
                "main-game/non-prod-game/"
                + file_match.group(0)
            )
            packet["files"] = list(dict.fromkeys([rel, *packet["files"]]))

    return packet


def enrich_standup_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    enriched = []
    for item in items:
        packet = resolve_task(item.get("registry_id"), item.get("summary", ""))
        packet["priority"] = item.get("priority")
        packet["standup_kind"] = item.get("kind")
        if item.get("checklist_line"):
            packet["checklist_line"] = item["checklist_line"]
        enriched.append(packet)
    return enriched


def build_work_queue_yaml(items: list[dict[str, Any]]) -> str:
    """Compact queue for embedding in standup markdown."""
    queue = []
    for item in items:
        queue.append(
            {
                "priority": item.get("priority"),
                "registry_id": item.get("registry_id"),
                "lane": item.get("lane"),
                "title": item.get("title"),
                "agent": item.get("agent"),
                "skill": item.get("skill"),
            }
        )
    return json.dumps({"items": queue}, indent=2)


def format_brief(packet: dict[str, Any]) -> str:
    lines = [
        f"# Work packet: {packet.get('registry_id', '?')} — {packet.get('title', '')}",
        "",
        f"**Lane:** {packet.get('lane')}  ",
        f"**Priority:** {packet.get('priority', 'n/a')}  ",
        f"**Resolution:** {packet.get('resolution')}",
        "",
    ]

    if packet.get("summary"):
        lines.extend(["## Standup summary", "", packet["summary"], ""])

    if packet.get("blocked_by"):
        lines.extend(["## Blocked by", "", ", ".join(packet["blocked_by"]), ""])

    lines.extend(
        [
            "## Agent routing",
            "",
            f"1. Load rule: `{packet['agent_rule']}`",
            f"2. Follow skill: `{packet['skill_path']}`",
        ]
    )
    if packet.get("pipeline"):
        stage = packet.get("pipeline_stage") or 1
        lines.append(
            f"3. Pipeline: `{packet['pipeline']}` stage {stage} "
            f"(`py scripts/agent_next_step.py --pipeline {packet['pipeline']} --stage {stage}`)"
        )

    lines.extend(["", "## Read these specs (in order)", ""])
    for spec in packet.get("specs", []):
        exists = "ok" if (ROOT / spec).exists() else "MISSING"
        lines.append(f"- [{exists}] `{spec}`")

    if packet.get("files"):
        lines.extend(["", "## Primary files", ""])
        for path in packet["files"]:
            exists = "ok" if (ROOT / path).exists() else "MISSING"
            lines.append(f"- [{exists}] `{path}`")

    if packet.get("deliverables"):
        lines.extend(["", "## Deliverables", ""])
        for path in packet["deliverables"]:
            lines.append(f"- `{path}`")

    if packet.get("backlog_excerpt"):
        lines.extend(["", "## Backlog excerpt", "", "```markdown", packet["backlog_excerpt"], "```"])

    if packet.get("action_note"):
        lines.extend(["", "## Note", "", packet["action_note"]])

    lines.extend(["", "## Verify after edits", ""])
    if packet.get("verify"):
        for cmd in packet["verify"]:
            lines.append(f"```powershell\n{cmd}\n```")
    else:
        lines.append("_No verify command in registry — run appropriate `py scripts/validate.py` profile._")

    lines.extend(
        [
            "",
            "## Completion",
            "",
            "When done, mark the matching checkbox in "
            "`planning/mvp_systems_integration_checklist.md` or remove/close the backlog item, "
            "then regenerate standup: `py scripts/daily_standup.py --report`.",
        ]
    )

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Resolve standup items to agent work packets.")
    parser.add_argument("--from-standup", nargs="?", const=str(DEFAULT_STANDUP), metavar="PATH")
    parser.add_argument("--task", help="Resolve a registry task id (e.g. N-6, C-2, COMPILE_ERROR).")
    parser.add_argument("--next", action="store_true", help="With --from-standup, show highest-priority item only.")
    parser.add_argument("--list-tasks", action="store_true", help="List registry task ids.")
    parser.add_argument(
        "--format",
        choices=["brief", "json", "queue"],
        default="brief",
        help="Output format (default: brief markdown).",
    )
    args = parser.parse_args()

    if args.list_tasks:
        registry = load_registry()
        for task_id in sorted(registry.get("tasks", {})):
            title = registry["tasks"][task_id].get("title", "")
            lane = registry["tasks"][task_id].get("lane", "")
            print(f"{task_id:20} [{lane:12}] {title}")
        return 0

    if args.task:
        packet = resolve_task(args.task.upper())
        if args.format == "json":
            print(json.dumps(packet, indent=2))
        else:
            print(format_brief(packet))
        return 0

    if args.from_standup:
        standup_path = Path(args.from_standup)
        if not standup_path.is_absolute():
            standup_path = ROOT / standup_path
        if not standup_path.exists():
            print(f"Standup report not found: {standup_path}", file=sys.stderr)
            return 1

        body = extract_standup_body(standup_path.read_text(encoding="utf-8"))
        items = enrich_standup_items(parse_standup_actions(body))

        if not items:
            print("No actionable items found in standup report.", file=sys.stderr)
            return 1

        if args.next:
            items = [items[0]]

        if args.format == "queue":
            print(build_work_queue_yaml(items))
            return 0

        if args.format == "json":
            print(json.dumps(items, indent=2))
            return 0

        for i, packet in enumerate(items):
            if i > 0:
                print("\n" + "=" * 72 + "\n")
            print(format_brief(packet))
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
