#!/usr/bin/env python3
"""Deterministic abstract balance simulation for Release 1 MVP."""

from __future__ import annotations

import argparse
import csv
import random
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_RELEASE = "release-1-mvp"

if str(ROOT / "main-game" / "pipeline" / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "main-game" / "pipeline" / "tools"))

from balance_model import (  # noqa: E402
    DayBudget,
    GateSpec,
    PlayerState,
    PolicySpec,
    build_day_budgets,
    evaluate_assertions,
    gate_lookup,
    load_balance_targets,
    load_choice_catalogue,
    load_gate_catalogue,
    load_run_policies,
    simulate_policy,
)


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def run_gate_report(gates: list[GateSpec], policy_results: list[dict]) -> list[dict]:
    rows: list[dict] = []
    gate_by_id = gate_lookup(gates)
    for gate in gates:
        for result in policy_results:
            policy_id = result["policy_id"]
            state = result["_state"]
            if gate.gate_type == "write_gate":
                req_insp = gate.required_insp or 0
                req_corr = gate.required_corr_level or 0
                actual_pass = state.has_story_fuel(req_insp, req_corr)
            elif gate.gate_type == "deadline_gate":
                threshold = gate.required_manuscript_progress or 0
                actual_pass = state.manuscript_progress >= threshold
            elif gate.gate_type == "ending_gate":
                actual_pass = state.corruption_level >= (gate.required_corr_level or 0)
            elif gate.gate_type == "anxiety_gate":
                actual_pass = state.anxiety < (gate.required_anxiety_min or 100)
            else:
                actual_pass = True
            rows.append(
                {
                    "gate_id": gate.gate_id,
                    "policy_id": policy_id,
                    "gate_type": gate.gate_type,
                    "required_insp": gate.required_insp or "",
                    "required_corr_level": gate.required_corr_level or "",
                    "required_manuscript_progress": gate.required_manuscript_progress or "",
                    "actual_inspiration": state.inspiration,
                    "actual_corruption_level": state.corruption_level,
                    "actual_manuscript_progress": state.manuscript_progress,
                    "actual_anxiety": state.anxiety,
                    "actual_pass": actual_pass,
                    "intended_note": gate.on_pass,
                }
            )
    return rows


def run_fuzz(policies: list[PolicySpec], day_budgets: dict[str, dict[int, DayBudget]], gates: list[GateSpec], runs: int, seed: int) -> list[dict]:
    rng = random.Random(seed)
    policy_ids = [p.policy_id for p in policies if p.policy_id not in {"penance_force"}]
    distribution: dict[str, int] = {}
    for _ in range(runs):
        policy_id = rng.choice(policy_ids)
        jittered = {}
        for day, budget in day_budgets.get(policy_id, {}).items():
            jittered[day] = DayBudget(
                day=budget.day,
                insp=max(0, budget.insp + rng.randint(-5, 5)),
                corr=max(0, budget.corr + rng.randint(-3, 3)),
                stern=budget.stern,
                vance=budget.vance,
                missy=budget.missy,
                gideon=budget.gideon,
            )
        policy = next(p for p in policies if p.policy_id == policy_id)
        state = simulate_policy(policy, gates, jittered)
        distribution[state.ending] = distribution.get(state.ending, 0) + 1
    rows = []
    for ending, count in sorted(distribution.items(), key=lambda item: (-item[1], item[0])):
        rows.append(
            {
                "ending": ending,
                "count": count,
                "percentage": round(100.0 * count / runs, 2),
            }
        )
    return rows


def write_markdown_report(
    out_path: Path,
    *,
    release: str,
    policy_rows: list[dict],
    matrix_rows: list[dict],
    fuzz_rows: list[dict],
    runs: int,
) -> None:
    passes = sum(1 for row in matrix_rows if row["pass"])
    total = len(matrix_rows)
    lines = [
        "# Release 1 balance simulation report",
        "",
        f"**Release:** `{release}`",
        f"**Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        f"**Model:** abstract day-budget simulator (not full Ren'Py route walk)",
        "",
        "## Verdict",
        "",
    ]
    if passes == total:
        lines.append("**PASS** — all supported matrix assertions matched.")
    elif passes >= total - 1:
        lines.append("**WARN** — matrix mostly matches; see incomplete assertions.")
    else:
        lines.append("**INCOMPLETE** — abstract model diverges from targets or lacks coverage.")
    lines.extend(
        [
            "",
            "## Policy results",
            "",
            "| Policy | Ending | Insp | Corr | MS | Anxiety | Notes |",
            "|--------|--------|-----:|-----:|---:|--------:|-------|",
        ]
    )
    for row in policy_rows:
        lines.append(
            f"| {row['policy_id']} | {row['ending']} | {row['inspiration']} | {row['corruption_level']} | "
            f"{row['manuscript_progress']} | {row['anxiety']} | {row['notes_summary']} |"
        )
    lines.extend(["", "## Matrix assertions", "", "| Run | Assertion | Pass | Actual |", "|-----|-----------|------|--------|"])
    for row in matrix_rows:
        mark = "yes" if row["pass"] else "no"
        lines.append(f"| {row['run_id']} | {row['assertion']} | {mark} | {row['actual']} |")
    lines.extend(["", f"## Fuzz distribution ({runs} runs)", "", "| Ending | Count | % |", "|--------|------:|--:|"])
    for row in fuzz_rows:
        lines.append(f"| {row['ending']} | {row['count']} | {row['percentage']} |")
    lines.extend(
        [
            "",
            "## Limitations",
            "",
            "- Does not walk label-level branches; uses per-day economy budgets from choice catalogue.",
            "- Penance/confrontation assertions require runtime capture (marked INCOMPLETE).",
            "- Anxiety model is simplified from acute suspicion totals.",
            "",
        ]
    )
    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run abstract Release 1 balance simulation.")
    parser.add_argument("--release", default=DEFAULT_RELEASE)
    parser.add_argument(
        "--balance-dir",
        default="main-game/draft/releases/planning/balance",
    )
    parser.add_argument(
        "--out-dir",
        default=f"main-game/pipeline/releases/{DEFAULT_RELEASE}/balance",
    )
    parser.add_argument("--deep", action="store_true", help="Run deep fuzz count from balance_targets.yaml")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    balance_dir = Path(args.balance_dir)
    out_dir = Path(args.out_dir)
    if not balance_dir.is_absolute():
        balance_dir = ROOT / balance_dir
    if not out_dir.is_absolute():
        out_dir = ROOT / out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    gates = load_gate_catalogue(balance_dir / "gate_catalogue.csv")
    policies = load_run_policies(balance_dir / "run_policies.csv")
    targets = load_balance_targets(balance_dir / "balance_targets.yaml")
    choices = load_choice_catalogue(balance_dir / "choice_catalogue.csv")
    if not choices:
        print("choice_catalogue.csv missing — run build_choice_catalogue.py first", file=sys.stderr)
        return 1

    day_budgets = build_day_budgets(choices, policies)
    policy_rows: list[dict] = []
    policy_lookup = {p.policy_id: p for p in policies}

    for policy in policies:
        state = simulate_policy(policy, gates, day_budgets[policy.policy_id])
        policy_rows.append(
            {
                "policy_id": policy.policy_id,
                "ending": state.ending,
                "inspiration": state.inspiration,
                "corruption_level": state.corruption_level,
                "manuscript_progress": state.manuscript_progress,
                "anxiety": state.anxiety,
                "notes_summary": "; ".join(state.notes[:3]),
                "_state": state,
            }
        )

    gate_rows = run_gate_report(gates, policy_rows)
    matrix_rows: list[dict] = []
    for mapping in targets.get("matrix_execution_mapping", []):
        run_id = mapping["run_id"]
        policy_id = mapping["policy_target"]
        policy = policy_lookup.get(policy_id)
        if not policy:
            continue
        state = simulate_policy(policy, gates, day_budgets[policy_id])
        for assertion_name, ok, actual in evaluate_assertions(state, mapping.get("assertions", [])):
            matrix_rows.append(
                {
                    "run_id": run_id,
                    "policy_id": policy_id,
                    "assertion": assertion_name,
                    "pass": ok,
                    "actual": actual,
                }
            )

    fuzz_cfg = targets.get("fuzz", {})
    fuzz_runs = int(fuzz_cfg.get("deep_runs" if args.deep else "local_default_runs", 100))
    fuzz_rows = run_fuzz(policies, day_budgets, gates, fuzz_runs, args.seed)

    with (out_dir / "policy_results.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["policy_id", "ending", "inspiration", "corruption_level", "manuscript_progress", "anxiety", "notes_summary"],
        )
        writer.writeheader()
        for row in policy_rows:
            writer.writerow({k: row[k] for k in writer.fieldnames})

    with (out_dir / "gate_results.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(gate_rows[0].keys()) if gate_rows else [])
        if gate_rows:
            writer.writeheader()
            writer.writerows(gate_rows)

    with (out_dir / "fuzz_distribution.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["ending", "count", "percentage"])
        writer.writeheader()
        writer.writerows(fuzz_rows)

    write_markdown_report(
        out_dir / "simulation_report.md",
        release=args.release,
        policy_rows=policy_rows,
        matrix_rows=matrix_rows,
        fuzz_rows=fuzz_rows,
        runs=fuzz_runs,
    )

    supported = [row for row in matrix_rows if "INCOMPLETE" not in row["actual"]]
    passed = sum(1 for row in supported if row["pass"])
    print(f"Wrote simulation outputs to {_rel(out_dir)}")
    print(f"Matrix assertions: {passed}/{len(supported)} supported checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
