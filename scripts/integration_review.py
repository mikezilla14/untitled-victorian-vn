#!/usr/bin/env python3
"""
Integration review for MVP planning — weekly or ad-hoc.

Covers checklist progress, backlog status, and specialist lens grades
(Chief Architect, Adult Market Reviewer, Lead Narrative Editor). These items
do not change daily and are not repeated in the daily standup.

Daily automated validation: scripts/daily_standup.py
"""

from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from pathlib import Path

from daily_standup import DEFAULT_SCHEDULE, load_epic_schedule, sync_backlog_to_registry
from standup_checks import CheckResult, run_all_daily_checks

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parents[1]
PLANNING_DIR = ROOT / "main-game" / "draft" / "releases" / "planning"
REVIEWS_DIR = PLANNING_DIR / "reviews"
CHECKLIST_PATH = PLANNING_DIR / "mvp_systems_integration_checklist.md"
BACKLOG_PATH = ROOT / "docs" / "backlog" / "mvp_backlog.md"


def parse_checklist() -> dict:
    results = {
        "global_total": 0,
        "global_completed": 0,
        "phases": {},
        "current_phase_tasks": [],
    }

    if not CHECKLIST_PATH.exists():
        return results

    content = CHECKLIST_PATH.read_text(encoding="utf-8")
    lines = content.splitlines()
    current_section = "General"
    results["phases"][current_section] = {"total": 0, "completed": 0}

    for line in lines:
        phase_match = re.match(
            r"^##\s+(Phase\s+\d+|Playtest\s+matrix|Partner\s+coordination\s+contract)\b(.*)",
            line,
            re.IGNORECASE,
        )
        if phase_match:
            current_section = f"{phase_match.group(1)}{phase_match.group(2)}".strip()
            results["phases"][current_section] = {"total": 0, "completed": 0}
            continue

        is_task = "[x]" in line.lower() or "[ ]" in line
        if not is_task:
            continue

        checked = "[x]" in line.lower()
        results["global_total"] += 1
        results["phases"][current_section]["total"] += 1
        if checked:
            results["global_completed"] += 1
            results["phases"][current_section]["completed"] += 1
        else:
            task_desc = line.strip().strip("-*|").strip()
            results["current_phase_tasks"].append((current_section, task_desc))

    return results


def parse_backlog() -> list[dict]:
    tasks = []
    if not BACKLOG_PATH.exists():
        return tasks

    content = BACKLOG_PATH.read_text(encoding="utf-8")
    pattern = re.compile(r"^###\s+([🔴🟡🟢])\s+\[([A-Z]-\d+)\]\s+(.+)$")
    lines = content.splitlines()
    current_task = None

    for line in lines:
        match = pattern.match(line)
        if match:
            if current_task:
                tasks.append(current_task)
            priority_emoji, task_id, title = match.groups()
            priority_name = (
                "High" if priority_emoji == "🔴" else "Medium" if priority_emoji == "🟡" else "Low"
            )
            current_task = {
                "id": task_id,
                "title": title,
                "priority_emoji": priority_emoji,
                "priority": priority_name,
                "description": "",
                "assignee": "Unknown",
                "completed": False,
            }
            continue

        if current_task:
            if line.strip().startswith("* **Description:**"):
                desc = line.replace("* **Description:**", "").strip()
                current_task["description"] = desc
                current_task["completed"] = desc.lower().startswith("complete")
            elif line.strip().startswith("* **Assignee:**"):
                current_task["assignee"] = line.replace("* **Assignee:**", "").replace("`", "").strip()

    if current_task:
        tasks.append(current_task)

    return tasks


def get_grade(score: float) -> str:
    if score >= 95:
        return "A"
    if score >= 90:
        return "A-"
    if score >= 85:
        return "B+"
    if score >= 80:
        return "B"
    if score >= 75:
        return "B-"
    if score >= 70:
        return "C+"
    if score >= 65:
        return "C"
    if score >= 60:
        return "C-"
    if score >= 55:
        return "D+"
    if score >= 50:
        return "D"
    return "F"


def calculate_grades(checklist_data: dict, backlog_tasks: list[dict], daily_checks: list[CheckResult]) -> dict:
    ca_score = 100.0
    failed_daily = [c for c in daily_checks if c.failed]
    ca_score -= min(30.0, len(failed_daily) * 8.0)

    eng_total = eng_completed = 0
    for section, data in checklist_data["phases"].items():
        if any(k in section.lower() for k in ["phase 1", "phase 2", "phase 6", "phase 7"]):
            eng_total += data["total"]
            eng_completed += data["completed"]
    if eng_total > 0:
        ca_score -= (1.0 - eng_completed / eng_total) * 20.0

    am_score = 100.0
    incomplete_ids = [t["id"] for t in backlog_tasks if not t.get("completed", False)]
    if "N-6" in incomplete_ids:
        am_score -= 10.0
    book_total = book_completed = 0
    for section, data in checklist_data["phases"].items():
        if "phase 5" in section.lower() or "phase 4" in section.lower():
            book_total += data["total"]
            book_completed += data["completed"]
    if book_total > 0:
        am_score -= (1.0 - book_completed / book_total) * 25.0

    ne_score = 100.0
    for nb in ("N-1", "N-2", "N-3", "N-4"):
        if nb in incomplete_ids:
            ne_score -= 5.0
    story_total = story_completed = 0
    for section, data in checklist_data["phases"].items():
        if "phase 3" in section.lower():
            story_total += data["total"]
            story_completed += data["completed"]
    if story_total > 0:
        ne_score -= (1.0 - story_completed / story_total) * 20.0

    overall = (ca_score + am_score + ne_score) / 3.0
    return {
        "chief_architect": {"score": ca_score, "grade": get_grade(ca_score)},
        "market_reviewer": {"score": am_score, "grade": get_grade(am_score)},
        "narrative_editor": {"score": ne_score, "grade": get_grade(ne_score)},
        "overall": {"score": overall, "grade": get_grade(overall)},
    }


def build_integration_report(
    schedule: dict,
    current_date: datetime.date,
    checklist_data: dict,
    backlog_tasks: list[dict],
    daily_checks: list[CheckResult],
    grades: dict,
) -> str:
    start_date = datetime.date.fromisoformat(schedule["epic_start_date"])
    elapsed_days = (current_date - start_date).days
    epic_week = (elapsed_days // 7) + 1
    week_str = str(epic_week) if epic_week <= 5 else "5 (Extended)"
    current_focus = schedule["weekly_foci"].get(str(epic_week), "Extended Polish & Bug Fixing")

    checklist_total = checklist_data["global_total"]
    checklist_done = checklist_data["global_completed"]
    checklist_pct = (checklist_done / checklist_total * 100) if checklist_total > 0 else 0.0
    incomplete_ids = [t["id"] for t in backlog_tasks if not t.get("completed", False)]

    lines: list[str] = []
    lines.append("========================================================================")
    lines.append(f"INTEGRATION REVIEW: {schedule['epic_name']}")
    lines.append(f"   Review Date: {current_date.strftime('%A, %B %d, %Y')}")
    lines.append(f"   Epic Week: {week_str} — {current_focus}")
    lines.append("   Cadence: weekly or ad-hoc (not daily)")
    lines.append("========================================================================")
    lines.append("")
    lines.append("PROJECT INTEGRITY GRADES (planning lenses — not daily automated tests)")
    lines.append(
        f"   Overall: [ {grades['overall']['grade']} ] "
        f"(Checklist: {checklist_done}/{checklist_total} — {checklist_pct:.1f}%)"
    )
    lines.append(f"   - Chief Architect:       [ {grades['chief_architect']['grade']} ]")
    lines.append(f"   - Adult Market Reviewer: [ {grades['market_reviewer']['grade']} ]")
    lines.append(f"   - Lead Narrative Editor: [ {grades['narrative_editor']['grade']} ]")
    lines.append("")
    lines.append("------------------------------------------------------------------------")
    lines.append("SPECIALIST NOTES")
    lines.append("------------------------------------------------------------------------")

    # Chief Architect lens
    lines.append("Chief Architect (@.agents/rules/chief_architect.md)")
    failed = [c for c in daily_checks if c.failed]
    if failed:
        lines.append(f"   Daily checks failing today ({len(failed)}):")
        for c in failed:
            lines.append(f"      - {c.name}: {c.summary}")
    else:
        lines.append("   Daily automated checks: all runnable checks passing.")
    hygiene = any(
        data["completed"] < data["total"]
        for section, data in checklist_data["phases"].items()
        if "phase 7" in section.lower()
    )
    if hygiene:
        lines.append("   Phase 7 code hygiene & promotion prep still has open items.")
    lines.append("")

    # Adult Market Reviewer lens
    lines.append("Adult Market Reviewer (@.agents/rules/adult_market_reviewer.md)")
    if "N-6" in incomplete_ids:
        lines.append("   [N-6] Story chains spicier rewrite still open.")
    else:
        lines.append("   Story chains and book chapter slots structurally complete.")
    book_open = any(
        data["completed"] < data["total"]
        for section, data in checklist_data["phases"].items()
        if "phase 5" in section.lower()
    )
    if book_open:
        lines.append("   Book routing / NVL verification checklist items remain open.")
    lines.append("")

    # Lead Narrative Editor lens
    lines.append("Lead Narrative Editor (@.agents/rules/lead_narrative_editor.md)")
    for tid in ("N-1", "N-2", "N-3", "N-4", "N-5"):
        if tid in incomplete_ids:
            task = next((t for t in backlog_tasks if t["id"] == tid), None)
            title = task["title"] if task else tid
            lines.append(f"   Open backlog: [{tid}] {title}")
    spine_open = any(
        data["completed"] < data["total"]
        for section, data in checklist_data["phases"].items()
        if "phase 3" in section.lower()
    )
    if spine_open:
        lines.append("   Main story spine walkthrough / branch smoke tests not signed off.")
    playtest_open = any(
        data["completed"] < data["total"]
        for section, data in checklist_data["phases"].items()
        if "playtest" in section.lower()
    )
    if playtest_open:
        lines.append("   Playtest matrix sign-off incomplete.")
    lines.append("")

    lines.append("------------------------------------------------------------------------")
    lines.append("CHECKLIST BY PHASE")
    lines.append("------------------------------------------------------------------------")
    for section, data in checklist_data["phases"].items():
        total, done = data["total"], data["completed"]
        if total > 0:
            pct = done / total * 100
            bar_len = 15
            filled = int(bar_len * done // total)
            bar = "=" * filled + "-" * (bar_len - filled)
            lines.append(f"   {section:<50} [ {bar} ] {done}/{total} ({pct:.0f}%)")
    lines.append("")

    lines.append("------------------------------------------------------------------------")
    lines.append("OPEN BACKLOG (high priority)")
    lines.append("------------------------------------------------------------------------")
    high_open = [t for t in backlog_tasks if t["priority"] == "High" and not t.get("completed", False)]
    if not high_open:
        lines.append("   No open high-priority backlog items.")
    else:
        for t in high_open:
            lines.append(f"   {t['priority_emoji']} [{t['id']}] {t['title']} (Assignee: {t['assignee']})")
    lines.append("")

    lines.append("------------------------------------------------------------------------")
    lines.append("SUGGESTED ACTIONS (planning — verify manually or via full review)")
    lines.append("------------------------------------------------------------------------")
    action_num = 0
    target_phrase = f"Phase {epic_week}"
    sprint_tasks = [t for s, t in checklist_data["current_phase_tasks"] if target_phrase in s]
    for task in sprint_tasks[:5]:
        action_num += 1
        lines.append(f"   {action_num}. [CHECKLIST] {task}")
    for t in high_open[:3]:
        action_num += 1
        lines.append(f"   {action_num}. [{t['id']}] {t['title']}")
    if action_num == 0:
        lines.append("   No sprint-scoped checklist or high-priority backlog actions flagged.")
    lines.append("")
    lines.append("Full narrative review template: planning/mvp_full_review_YYYY-MM-DD.md")
    lines.append("========================================================================")
    return "\n".join(lines)


def write_report(report_date: datetime.date, plain: str, output_dir: Path | None = None) -> Path:
    directory = output_dir or REVIEWS_DIR
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"integration_review_{report_date.isoformat()}.md"
    body = (
        f"# Integration Review\n\n"
        f"**Review date:** {report_date.strftime('%A, %B %d, %Y')}  \n"
        f"**Generated:** {datetime.datetime.now().isoformat(timespec='seconds')}\n\n"
        f"Weekly or ad-hoc planning review. Daily automated checks: "
        f"`py scripts/daily_standup.py --report`\n\n"
        f"```text\n{plain}\n```\n"
    )
    path.write_text(body, encoding="utf-8")
    latest = PLANNING_DIR / "integration_review_report.md"
    latest.write_text(body, encoding="utf-8")
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description="Run integration review (weekly/ad-hoc planning).")
    parser.add_argument("--report", action="store_true", help="Write dated markdown report.")
    parser.add_argument("--output-dir", type=Path, help="Override reviews output directory.")
    parser.add_argument("--date", help="Simulate date (YYYY-MM-DD).")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    schedule = load_epic_schedule()
    current_date = (
        datetime.date.fromisoformat(args.date)
        if args.date
        else datetime.date.today()
    )

    sync_backlog_to_registry()
    checklist_data = parse_checklist()
    backlog_tasks = parse_backlog()
    daily_checks = run_all_daily_checks()
    grades = calculate_grades(checklist_data, backlog_tasks, daily_checks)

    report = build_integration_report(
        schedule, current_date, checklist_data, backlog_tasks, daily_checks, grades
    )
    if not args.quiet:
        print(report)

    if args.report:
        path = write_report(current_date, report, args.output_dir)
        if not args.quiet:
            print(f"Report saved to {path.relative_to(ROOT).as_posix()}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
