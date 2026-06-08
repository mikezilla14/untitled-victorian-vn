#!/usr/bin/env python3
"""
Print the next agent rule file to load for a pipeline stage.

Usage:
  py scripts/agent_next_step.py --pipeline produce-day
  py scripts/agent_next_step.py --pipeline produce-day --stage 2 --day 105 --release "release 1 - mvp"
  py scripts/agent_next_step.py --list-pipelines
  py scripts/agent_next_step.py --list-agents
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULES = ROOT / ".agents" / "rules"

PIPELINES: dict[str, list[dict]] = {
    "produce-day": [
        {"stage": 1, "agent": "writers_room", "note": "Workflow A: divergent -> convergent -> 3 gates (sequential)"},
        {"stage": 2, "agent": "non_prod_code_agent", "note": "After all gates pass; verbatim prose"},
        {"stage": 3, "agent": "chief_architect", "note": "Sandbox code validation"},
    ],
    "review-scene": [
        {
            "stage": 1,
            "agent": "lead_narrative_editor",
            "parallel": ["forensic_psychology_consultant", "victorian_consultant"],
            "note": "Run stage-1 agents in parallel",
        },
    ],
    "market-review": [
        {"stage": 1, "agent": "adult_market_reviewer", "note": "Read-only"},
    ],
    "spice-tune": [
        {"stage": 1, "agent": "spiciness_tuning_agent"},
        {"stage": 2, "agent": "writers_room", "note": "If prose must change"},
        {"stage": 3, "agent": "lead_narrative_editor"},
        {"stage": 4, "agent": "forensic_psychology_consultant"},
        {"stage": 5, "agent": "victorian_consultant"},
    ],
    "implement-spec": [
        {"stage": 1, "agent": "non_prod_code_agent"},
        {"stage": 2, "agent": "chief_architect"},
    ],
    "promote-day": [
        {"stage": 1, "agent": "chief_architect"},
        {"stage": 2, "agent": "forensic_psychology_consultant", "note": "Pre-prod psychology"},
        {"stage": 3, "agent": "prod_code_agent"},
        {"stage": 4, "agent": "forensic_psychology_consultant", "note": "Post-prod psychology"},
        {"stage": 5, "agent": "chief_architect", "note": "Lint / structure"},
    ],
    "promote-framework": [
        {"stage": 1, "agent": "chief_architect"},
        {"stage": 2, "agent": "prod_code_agent"},
        {"stage": 3, "agent": "chief_architect"},
    ],
    "historical-check": [
        {"stage": 1, "agent": "victorian_consultant"},
    ],
    "revise-narrative": [
        {"stage": 1, "agent": "writers_room", "note": "Brief scale S/M/L -> workflows B / partial / A"},
        {"stage": 2, "agent": "lead_narrative_editor"},
        {"stage": 3, "agent": "forensic_psychology_consultant"},
        {"stage": 4, "agent": "victorian_consultant"},
        {"stage": 5, "agent": "writers_room", "note": "Close brief; handoff to requester"},
        {"stage": 6, "agent": "non_prod_code_agent", "note": "Typical resume target"},
    ],
    "rewrite-narrative": [
        {"stage": 1, "agent": "writers_room", "note": "Workflow A: full divergent pool -> convergent -> 3 gates (sequential)"},
        {"stage": 2, "agent": "non_prod_code_agent", "note": "After all gates pass; verbatim prose"},
        {"stage": 3, "agent": "chief_architect", "note": "Sandbox code validation"},
    ],
    "canon-update": [
        {"stage": 1, "agent": "lead_narrative_editor"},
        {"stage": 2, "agent": "forensic_psychology_consultant"},
        {"stage": 3, "agent": "victorian_consultant"},
        {"stage": 4, "agent": "human", "note": "HARD STOP — human approval required"},
        {"stage": 5, "agent": "lead_narrative_editor", "note": "Or forensic_psychology_consultant if authorized"},
    ],
    "documentation-audit": [
        {"stage": 1, "agent": "documentation_steward", "note": "Update docs first, then refresh catalogue and audit artifacts"},
    ],
    "dag-tag-update": [
        {
            "stage": 1,
            "agent": "non_prod_code_agent",
            "note": "Update only [DAG_*] comments; preserve manual DAG tags unless explicitly told to overwrite them",
        },
        {
            "stage": 2,
            "agent": "documentation_steward",
            "note": "Confirm downstream graph outputs and storyboard references are refreshed or reported stale",
        },
    ],
    "storyboard-sync": [
        {
            "stage": 1,
            "agent": "documentation_steward",
            "note": "Update story_board.md from current .rpy scripts and graph audit evidence; .rpy remains source of truth",
        },
    ],
    "writer-author": [
        {
            "stage": 1,
            "agent": "writers_desk",
            "note": "Prose-first intake -> Authoring Intent (intents/dayrdd_authoring_intent.md) -> full-fidelity contract pre-check (advisory)",
        },
        {"stage": 2, "agent": "writers_room", "note": "Convergent/gates on captured prose (scale S/M/L)"},
        {"stage": 3, "agent": "non_prod_code_agent", "note": "Shape verbatim prose + tags + DAG/asset sync after gates pass"},
        {"stage": 4, "agent": "chief_architect", "note": "Sandbox code validation"},
    ],
    "flag-wiring-only": [
        {
            "stage": 1,
            "agent": "writers_desk",
            "note": "Capture flag in plain language: boolean by default; if one-of-N, prompt for allowed values + record whitelist request",
        },
        {
            "stage": 2,
            "agent": "non_prod_code_agent",
            "note": "Wire attribute/whitelist/setter into classes_non_canon.rpy + classes_non_canon_notes.md",
        },
        {"stage": 3, "agent": "chief_architect", "note": "Framework mockup review; queue for promote-framework"},
    ],
}

AGENT_FILES: dict[str, str] = {
    "orchestrator": "orchestrator.md",
    "writers_room": "writers_room.md",
    "divergent_writer": "divergent_writer_base.md (+ one section of divergent_writer_personas.md)",
    "convergent_writer": "convergent_writer.md",
    "lead_narrative_editor": "lead_narrative_editor.md",
    "forensic_psychology_consultant": "forensic_psychology_consultant.md",
    "victorian_consultant": "victorian_consultant.md",
    "spiciness_tuning_agent": "spiciness_tuning_agent.md",
    "adult_market_reviewer": "adult_market_reviewer.md",
    "non_prod_code_agent": "non_prod_code_agent.md",
    "prod_code_agent": "prod_code_agent.md",
    "chief_architect": "chief_architect.md",
    "gatekeeper_orchestrator": "gatekeeper_orchestrator.md",
    "documentation_steward": "documentation_steward.md",
    "writers_desk": "writers_desk.md",
    "human": "(no rule file — human decision)",
}


def rule_path(agent: str) -> Path | None:
    if agent == "human":
        return None
    filename = AGENT_FILES.get(agent, f"{agent}.md")
    if "(" in filename:
        return RULES / "divergent_writer_base.md"
    path = RULES / filename
    return path if path.exists() else None


def print_stage(pipeline: str, step: dict, day: str | None, release: str | None) -> None:
    stage = step["stage"]
    agent = step["agent"]
    print(f"\n## {pipeline} — stage {stage}")
    if step.get("parallel"):
        print("Run in parallel:")
        for p in step["parallel"]:
            p_path = rule_path(p)
            print(f"  - {p}")
            if p_path:
                print(f"    Rule: {p_path.relative_to(ROOT).as_posix()}")
    print(f"Agent: {agent}")
    path = rule_path(agent)
    if path:
        print(f"Rule file: {path.relative_to(ROOT).as_posix()}")
    if step.get("note"):
        print(f"Note: {step['note']}")
    if day and release:
        dd = day.replace("day", "") if day.startswith("day") else day
        rid = day if day.startswith("day") else f"day{dd}"
        print("\nArtifacts:")
        print(
            f"  Draft: narrative/draft/releases/{release}/non_prod_renpy_project/game/days/{rid}_non_canon.rpy"
        )
        print(
            f"  Specs: narrative/pipeline/releases/{release}/days/{rid}/specs/"
        )
        print(
            f"  Gates: narrative/pipeline/releases/{release}/days/{rid}/gates/"
        )
        print(
            f"  Report: narrative/pipeline/releases/{release}/days/{rid}/synthesis/{rid}_convergent_report.md"
        )
    print("\nHandoff: paste the full rule file as system prompt + prior stage verdicts.")
    print('Validate: py scripts/validate.py --profile changed --agent <name> --files "<paths>"')


def main() -> int:
    parser = argparse.ArgumentParser(description="Show next agent to invoke for a pipeline.")
    parser.add_argument("--pipeline", help="Pipeline id (e.g. produce-day)")
    parser.add_argument("--stage", type=int, default=1, help="Stage number (default: 1)")
    parser.add_argument("--day", help="Day id e.g. 105 or day105")
    parser.add_argument("--release", default="release-1-mvp", help="Release slug (e.g. release-1-mvp)")
    parser.add_argument("--list-pipelines", action="store_true")
    parser.add_argument("--list-agents", action="store_true")
    args = parser.parse_args()

    if args.list_pipelines:
        print("Pipelines:")
        for name, steps in PIPELINES.items():
            print(f"  {name} ({len(steps)} stages)")
        return 0

    if args.list_agents:
        print("Agents:")
        for agent, filename in sorted(AGENT_FILES.items()):
            print(f"  {agent}: {filename}")
        return 0

    if not args.pipeline:
        parser.error("Provide --pipeline or --list-pipelines / --list-agents")

    pipeline = args.pipeline
    if pipeline not in PIPELINES:
        print(f"Unknown pipeline: {pipeline}", file=sys.stderr)
        print(f"Available: {', '.join(PIPELINES)}", file=sys.stderr)
        return 1

    steps = PIPELINES[pipeline]
    step = next((s for s in steps if s["stage"] == args.stage), None)
    if not step:
        print(f"Stage {args.stage} not defined for {pipeline}.", file=sys.stderr)
        print(f"Stages: {[s['stage'] for s in steps]}", file=sys.stderr)
        return 1

    print("=" * 60)
    print("Agent next step")
    print("Orchestrator index: .agents/rules/orchestrator.md")
    print("Human index: AGENTS.md")
    print_stage(pipeline, step, args.day, args.release)

    next_stage = args.stage + 1
    nxt = next((s for s in steps if s["stage"] == next_stage), None)
    if nxt:
        print(f"\nNext: py scripts/agent_next_step.py --pipeline {pipeline} --stage {next_stage}", end="")
        if args.day:
            print(f" --day {args.day}", end="")
        if args.release:
            print(f' --release "{args.release}"', end="")
        print()
    else:
        print("\nFinal stage of pipeline. Run validate.py / orchestrate_review.py before PR.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
