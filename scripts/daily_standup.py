#!/usr/bin/env python3
"""
Daily automated health check for the Victorian Visual Novel project.

Runs live validation only (no stale errors.txt or static checklist narration).
For checklist progress, backlog grades, and specialist lenses, use
`scripts/integration_review.py` (weekly or ad-hoc).
"""

from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from pathlib import Path

from standup_checks import CheckResult, run_all_daily_checks

# Fix terminal encoding issues on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parents[1]
PLANNING_DIR = ROOT / "main-game" / "draft" / "releases" / "planning"
STANDUP_REPORTS_DIR = PLANNING_DIR / "standups"
CONFIG_PATH = PLANNING_DIR / "epic_schedule.json"
BACKLOG_PATH = ROOT / "docs" / "backlog" / "mvp_backlog.md"

DEFAULT_SCHEDULE = {
    "epic_name": "Release 1 - MVP",
    "epic_start_date": "2026-05-18",
    "weekly_foci": {
        "1": "Sprint 1: Spine Routing & Fuel Gates (Milestones 1 & 3)",
        "2": "Sprint 2: Dynamic Systems, Story Chains & Fail States (Milestones 1 & 2)",
        "3": "Sprint 3: UI & Structural Assets Integration (Milestone 4)",
        "4": "Sprint 4: Full-fidelity Verification & Prose Drop (Milestone 5)",
        "5": "Sprint 5: Soft Launch to Subscribers, Next Release Planning & Playtest Bug Fixes (Milestone 6 / Ship)",
    },
}


class Colors:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    END = "\033[0m"
    BOLD = "\033[1m"


def load_epic_schedule() -> dict:
    if not CONFIG_PATH.parent.exists():
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not CONFIG_PATH.exists():
        CONFIG_PATH.write_text(json.dumps(DEFAULT_SCHEDULE, indent=2), encoding="utf-8")
        return DEFAULT_SCHEDULE
    try:
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"Warning: Failed to load epic schedule config ({e}). Using defaults.")
        return DEFAULT_SCHEDULE


# --- Backlog sync (shared with resolve_work_item / integration_review) ---

AGENT_MAPPING = {
    "non_prod_code_agent": {
        "lane": "code",
        "agent": "non_prod_code_agent",
        "skill": "implement_spec",
        "pipeline": "implement-spec",
        "pipeline_stage": 1,
    },
    "prod_code_agent": {
        "lane": "code",
        "agent": "prod_code_agent",
        "skill": "promote_day",
        "pipeline": "promote-day",
        "pipeline_stage": 3,
    },
    "writers_room": {
        "lane": "prose",
        "agent": "writers_room",
        "skill": "rewrite_narrative",
        "pipeline": "rewrite-narrative",
        "pipeline_stage": 1,
    },
    "convergent_writer": {
        "lane": "prose",
        "agent": "convergent_writer",
        "skill": "convergent_writer",
        "pipeline": "produce-day",
        "pipeline_stage": 1,
    },
    "victorian_consultant": {
        "lane": "prose",
        "agent": "victorian_consultant",
        "skill": "historical_check",
        "pipeline": "historical-check",
        "pipeline_stage": 1,
    },
    "lead_narrative_editor": {
        "lane": "gate",
        "agent": "lead_narrative_editor",
        "skill": "review_scene",
        "pipeline": "review-scene",
        "pipeline_stage": 1,
    },
    "chief_architect": {
        "lane": "audit",
        "agent": "chief_architect",
        "skill": "check_assets",
    },
}


def find_agent_info(assignee_str: str) -> dict:
    assignee_str = assignee_str.replace("`", "").strip()
    for k, v in AGENT_MAPPING.items():
        if k in assignee_str:
            return v
    return {}


def parse_markdown_backlog(content: str) -> dict[str, dict]:
    tasks = {}
    pattern = re.compile(r"^###\s+([🔴🟡🟢])\s+\[([A-Z]-\d+)\]\s+(.+)$", re.MULTILINE)
    matches = list(pattern.finditer(content))
    for i, match in enumerate(matches):
        _emoji, task_id, title = match.groups()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        body = content[start:end]

        assignee = ""
        assignee_match = re.search(r"\*\s+\*\*Assignee:\*\*\s*`?([a-zA-Z_0-9\-]+)`?", body)
        if assignee_match:
            assignee = assignee_match.group(1).strip()

        verify = []
        verify_match = re.search(r"```powershell\n(.*?)\n```", body, re.DOTALL)
        if verify_match:
            verify = [line.strip() for line in verify_match.group(1).splitlines() if line.strip()]

        files = []
        link_matches = re.findall(r"\[.*?\]\(\.\./\.\./(.*?)\)", body)
        for link in link_matches:
            clean_link = link.split("#")[0].strip()
            if clean_link and clean_link not in files:
                files.append(clean_link)

        tasks[task_id] = {
            "title": title.strip(),
            "assignee": assignee,
            "verify": verify,
            "files": files,
        }
    return tasks


def sync_backlog_to_registry() -> None:
    registry_path = ROOT / "docs" / "backlog" / "task_registry.json"

    if not BACKLOG_PATH.exists() or not registry_path.exists():
        return

    try:
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"Warning: Failed to load task registry for sync ({e})")
        return

    content = BACKLOG_PATH.read_text(encoding="utf-8")
    tasks = parse_markdown_backlog(content)

    updated = False
    for task_id, info in tasks.items():
        if task_id not in registry.get("tasks", {}):
            registry.setdefault("tasks", {})[task_id] = {}

        t = registry["tasks"][task_id]
        assignee = info.get("assignee", "")
        agent_info = find_agent_info(assignee)
        title = info.get("title", "")

        if title and t.get("title") != title:
            t["title"] = title
            updated = True

        if assignee:
            agent = agent_info.get("agent", "orchestrator")
            if t.get("agent") != agent:
                t["agent"] = agent
                updated = True
            lane = agent_info.get("lane", "integration")
            if t.get("lane") != lane:
                t["lane"] = lane
                updated = True
            skill = agent_info.get("skill", "orchestrator")
            if t.get("skill") != skill:
                t["skill"] = skill
                updated = True
            if "pipeline" in agent_info:
                if t.get("pipeline") != agent_info["pipeline"]:
                    t["pipeline"] = agent_info["pipeline"]
                    updated = True
                if t.get("pipeline_stage") != agent_info.get("pipeline_stage"):
                    t["pipeline_stage"] = agent_info["pipeline_stage"]
                    updated = True

        if "backlog_anchor" not in t:
            t["backlog_anchor"] = task_id
            updated = True

        files = info.get("files", [])
        if files and t.get("files") != files:
            t["files"] = files
            updated = True

        verify = info.get("verify", [])
        if verify and t.get("verify") != verify:
            t["verify"] = verify
            updated = True

    if updated:
        try:
            registry_path.write_text(json.dumps(registry, indent=2), encoding="utf-8")
            print("Task registry synced successfully with backlog.")
        except Exception as e:
            print(f"Warning: Failed to write updated registry ({e})")


# --- Daily report (automated checks only) ---

CHECK_REGISTRY_IDS = {
    "renpy_contract": "RENPY_CONTRACT_FAIL",
    "engineering_compliance": "ENGINEERING_COMPLIANCE_FAIL",
    "scene_direction": "DISCOVERED_SCENE_DIR",
    "format_non_canon": "DISCOVERED_FORMAT",
    "historical_linter": "DISCOVERED_HISTORICAL",
    "asset_disk": "ASSET_DISK_FAIL",
    "renpy_lint": "RENPY_LINT_FAIL",
}


def _status_glyph(check: CheckResult, use_color: bool) -> str:
    c_green = Colors.GREEN if use_color else ""
    c_red = Colors.RED if use_color else ""
    c_yellow = Colors.YELLOW if use_color else ""
    c_end = Colors.END if use_color else ""
    if check.status == "pass":
        return f"{c_green}PASS{c_end}"
    if check.status == "fail":
        return f"{c_red}FAIL{c_end}"
    return f"{c_yellow}SKIP{c_end}"


def build_action_items(checks: list[CheckResult]) -> list[tuple[str, str, str | None]]:
    """(kind, summary, per-file fix command) tuples for failed checks."""
    items: list[tuple[str, str, str | None]] = []
    for check in checks:
        if not check.failed:
            continue
        if check.check_id in ("scene_direction", "format_non_canon", "historical_linter") and check.details:
            for detail in check.details:
                if check.check_id == "scene_direction":
                    fix = f'py scripts/scene_direction.py --files "{detail}"'
                    items.append(("DISCOVERED", f"Update scene direction for {detail}", fix))
                elif check.check_id == "format_non_canon":
                    fix = f'py scripts/format_non_canon.py "{detail}"'
                    items.append(("DISCOVERED", f"Format {detail}", fix))
                elif check.check_id == "historical_linter":
                    fix = f'py scripts/historical_linter.py --file "{detail}"'
                    items.append(("DISCOVERED", f"Fix historical linter errors in {detail}", fix))
        else:
            items.append(("FAIL", f"{check.name}: {check.summary}", check.fix_command))
    return items


def build_daily_report(
    schedule: dict,
    current_date: datetime.date,
    checks: list[CheckResult],
    use_color: bool = False,
) -> str:
    start_date = datetime.date.fromisoformat(schedule["epic_start_date"])
    elapsed_days = (current_date - start_date).days
    epic_day = elapsed_days + 1
    epic_week = (elapsed_days // 7) + 1
    sprint_day = (elapsed_days % 7) + 1
    epic_length_days = 35
    days_remaining_epic = max(0, epic_length_days - elapsed_days)
    days_remaining_sprint = max(0, 7 - sprint_day)
    week_str = str(epic_week) if epic_week <= 5 else "5 (Extended)"
    current_focus = schedule["weekly_foci"].get(str(epic_week), "Extended Polish & Bug Fixing")

    c_hdr = Colors.HEADER if use_color else ""
    c_blue = Colors.BLUE if use_color else ""
    c_cyan = Colors.CYAN if use_color else ""
    c_green = Colors.GREEN if use_color else ""
    c_yellow = Colors.YELLOW if use_color else ""
    c_red = Colors.RED if use_color else ""
    c_bold = Colors.BOLD if use_color else ""
    c_end = Colors.END if use_color else ""

    ran = [c for c in checks if c.status != "skip"]
    passed = sum(1 for c in ran if c.passed)
    failed = sum(1 for c in checks if c.failed)
    skipped = sum(1 for c in checks if c.status == "skip")

    lines: list[str] = []
    lines.append(f"{c_bold}========================================================================{c_end}")
    lines.append(f"📅 {c_hdr}{c_bold}DAILY AUTOMATED HEALTH CHECK: {schedule['epic_name']}{c_end}")
    lines.append(f"   {c_bold}Current Date:{c_end} {current_date.strftime('%A, %B %d, %Y')}")
    lines.append(
        f"   {c_bold}Epic Cadence:{c_end} Week {week_str}, Sprint Day {sprint_day} of 7 "
        f"(Epic Day {epic_day} of 35)"
    )
    lines.append(
        f"   {c_bold}Days Left in Sprint:{c_end} {c_cyan}{days_remaining_sprint} days{c_end} | "
        f"{c_bold}Days Left in Epic:{c_end} {c_red}{days_remaining_epic} days{c_end}"
    )
    lines.append(f"   {c_bold}Active Sprint Focus:{c_end} {c_blue}{current_focus}{c_end}")
    lines.append(f"{c_bold}========================================================================{c_end}")
    lines.append("")
    lines.append(
        f"🔬 {c_bold}AUTOMATED CHECKS{c_end} "
        f"({len(ran)} run, {passed} passed, {failed} failed, {skipped} skipped)"
    )
    lines.append(f"{c_bold}------------------------------------------------------------------------{c_end}")

    for check in checks:
        glyph = _status_glyph(check, use_color)
        lines.append(f"   [{glyph}] {check.name} — {check.summary}")
        for detail in check.details[:5]:
            lines.append(f"      - {detail}")
        if len(check.details) > 5:
            lines.append(f"      - ... and {len(check.details) - 5} more.")
        if check.failed and check.fix_command and not check.details:
            lines.append(f"      ↳ {check.fix_command}")

    lines.append("")
    lines.append(f"{c_bold}------------------------------------------------------------------------{c_end}")
    lines.append(f"🔥 {c_bold}ACTION QUEUE{c_end} (failed checks only)")
    lines.append(f"{c_bold}------------------------------------------------------------------------{c_end}")

    actions = build_action_items(checks)
    if not actions:
        lines.append(f"   {c_green}🎉 All runnable checks passed. No automated blockers.{c_end}")
        lines.append("")
        lines.append(
            f"   {c_yellow}For checklist progress, backlog, and specialist lenses, run:{c_end}"
        )
        lines.append("   py scripts/integration_review.py --report")
    else:
        for idx, (kind, summary, fix_cmd) in enumerate(actions, start=1):
            if kind == "DISCOVERED":
                lines.append(f"   {idx}. 🔍 {c_bold}[DISCOVERED]{c_end} {summary}")
            else:
                lines.append(f"   {idx}. {c_red}{c_bold}[FAIL]{c_end} {summary}")
            if fix_cmd:
                lines.append(f"      ↳ {fix_cmd}")

    lines.append("")
    lines.append(f"{c_bold}========================================================================{c_end}")
    return "\n".join(lines)


def standup_report_path(report_date: datetime.date, output_dir: Path | None = None) -> Path:
    directory = output_dir or STANDUP_REPORTS_DIR
    return directory / f"daily_standup_{report_date.isoformat()}.md"


def append_agent_work_queue(markdown_content: str, plain_report: str) -> str:
    try:
        scripts_dir = Path(__file__).resolve().parent
        if str(scripts_dir) not in sys.path:
            sys.path.insert(0, str(scripts_dir))
        from resolve_work_item import build_work_queue_yaml, enrich_standup_items, parse_standup_actions

        items = enrich_standup_items(parse_standup_actions(plain_report))
        if not items:
            return markdown_content

        queue_json = build_work_queue_yaml(items)
        return markdown_content + (
            "\n## Agent work queue\n\n"
            "Point code or prose agents at this report, then resolve the next item:\n\n"
            "```powershell\n"
            "py scripts/resolve_work_item.py --from-standup --next\n"
            "```\n\n"
            "Skill: `.agents/skills/action_from_standup/SKILL.md`  \n"
            "Registry: `docs/backlog/task_registry.json`  \n"
            "Contract: `main-game/draft/releases/planning/standup_agent_contract.md`\n\n"
            f"```json\n{queue_json}\n```\n"
        )
    except Exception as exc:
        return markdown_content + f"\n<!-- agent work queue skipped: {exc} -->\n"


def write_markdown_report(
    report_date: datetime.date,
    plain_report: str,
    output_dir: Path | None = None,
) -> Path:
    directory = output_dir or STANDUP_REPORTS_DIR
    directory.mkdir(parents=True, exist_ok=True)
    report_path = standup_report_path(report_date, directory)
    markdown_content = (
        f"# Daily Automated Health Check\n\n"
        f"**Report date:** {report_date.strftime('%A, %B %d, %Y')}  \n"
        f"**Generated:** {datetime.datetime.now().isoformat(timespec='seconds')}\n\n"
        f"Live validation only. For checklist/backlog/specialist review: "
        f"`py scripts/integration_review.py --report`\n\n"
        f"```text\n{plain_report}\n```\n"
    )
    markdown_content = append_agent_work_queue(markdown_content, plain_report)
    report_path.write_text(markdown_content, encoding="utf-8")

    latest_path = PLANNING_DIR / "daily_standup_report.md"
    latest_path.write_text(markdown_content, encoding="utf-8")
    return report_path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run daily automated health checks (live validation only)."
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="Write standup report to standups/daily_standup_YYYY-MM-DD.md (and update daily_standup_report.md).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Override standup report directory (default: planning/standups/).",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress terminal output (useful for scheduled runs).",
    )
    parser.add_argument("--date", help="Simulate a specific date (YYYY-MM-DD format).")
    parser.add_argument(
        "--start-date",
        help="Set or temporarily override the Epic start date (YYYY-MM-DD format).",
    )
    args = parser.parse_args()

    schedule = load_epic_schedule()
    if args.start_date:
        schedule["epic_start_date"] = args.start_date

    if args.date:
        try:
            current_date = datetime.date.fromisoformat(args.date)
        except ValueError:
            print("Error: Invalid date format. Use YYYY-MM-DD.")
            return 1
    else:
        current_date = datetime.date.today()

    sync_backlog_to_registry()
    checks = run_all_daily_checks()

    terminal_report = build_daily_report(schedule, current_date, checks, use_color=True)
    if not args.quiet:
        print(terminal_report)

    if args.report:
        plain_report = build_daily_report(schedule, current_date, checks, use_color=False)
        report_path = write_markdown_report(current_date, plain_report, args.output_dir)
        if not args.quiet:
            print(f"Report saved to {report_path.relative_to(ROOT).as_posix()}")

    return 1 if any(c.failed for c in checks) else 0


if __name__ == "__main__":
    sys.exit(main())
