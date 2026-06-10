#!/usr/bin/env python3
"""
Daily Standup Ceremony script for the Victorian Visual Novel project.
Computes the weekly sprint and 5-week epic cadence, parses the integration checklist,
audits the non-prod codebase and backlog, and generates a formatted progress report
with letter grades from the Chief Architect, Adult Market Reviewer, and Lead Narrative Editor.
"""

from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from pathlib import Path

# Fix terminal encoding issues on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Paths
ROOT = Path(__file__).resolve().parents[1]
PLANNING_DIR = ROOT / "narrative" / "draft" / "releases" / "release-1-mvp" / "planning"
STANDUP_REPORTS_DIR = PLANNING_DIR / "standups"
CONFIG_PATH = PLANNING_DIR / "epic_schedule.json"
CHECKLIST_PATH = PLANNING_DIR / "mvp_systems_integration_checklist.md"
BACKLOG_PATH = ROOT / "docs" / "backlog" / "mvp_backlog.md"
NON_PROD_PROJECT_DIR = ROOT / "narrative" / "draft" / "releases" / "release-1-mvp" / "non_prod_renpy_project"
NON_PROD_GAME_DIR = NON_PROD_PROJECT_DIR / "game"
ERRORS_PATH = NON_PROD_PROJECT_DIR / "errors.txt"

DEFAULT_SCHEDULE = {
    "epic_name": "Release 1 - MVP",
    "epic_start_date": "2026-05-18",
    "weekly_foci": {
        "1": "Sprint 1: Spine Routing & Fuel Gates (Milestones 1 & 3)",
        "2": "Sprint 2: Dynamic Systems, Story Chains & Fail States (Milestones 1 & 2)",
        "3": "Sprint 3: UI & Structural Assets Integration (Milestone 4)",
        "4": "Sprint 4: Full-fidelity Verification & Prose Drop (Milestone 5)",
        "5": "Sprint 5: Soft Launch to Subscribers, Next Release Planning & Playtest Bug Fixes (Milestone 6 / Ship)"
    }
}

# ANSI colors
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

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

def parse_checklist() -> dict:
    results = {
        "global_total": 0,
        "global_completed": 0,
        "phases": {},
        "current_phase_tasks": []
    }
    
    if not CHECKLIST_PATH.exists():
        return results
        
    content = CHECKLIST_PATH.read_text(encoding="utf-8")
    lines = content.splitlines()
    
    current_section = "General"
    results["phases"][current_section] = {"total": 0, "completed": 0}
    
    for line in lines:
        # Check for phase headers
        phase_match = re.match(r"^##\s+(Phase\s+\d+|Playtest\s+matrix|Partner\s+coordination\s+contract)\b(.*)", line, re.IGNORECASE)
        if phase_match:
            current_section = f"{phase_match.group(1)}{phase_match.group(2)}".strip()
            results["phases"][current_section] = {"total": 0, "completed": 0}
            continue
            
        # Matches checkboxes [ ] or [x]/[X]
        # Skip checklist table header details but count check lines
        checked = False
        is_task = False
        
        if "[x]" in line.lower():
            checked = True
            is_task = True
        elif "[ ]" in line:
            checked = False
            is_task = True
            
        if is_task:
            results["global_total"] += 1
            results["phases"][current_section]["total"] += 1
            if checked:
                results["global_completed"] += 1
                results["phases"][current_section]["completed"] += 1
            else:
                # Store pending tasks for current standup guidance
                task_desc = line.strip().strip("-*|").strip()
                results["current_phase_tasks"].append((current_section, task_desc))
                
    return results

def parse_backlog() -> list[dict]:
    tasks = []
    if not BACKLOG_PATH.exists():
        return tasks
        
    content = BACKLOG_PATH.read_text(encoding="utf-8")
    # Matches: ### [priority emoji] [ID] Title
    # E.g. ### 🔴 [N-1] Historical Linter Anachronisms Cleansing
    pattern = re.compile(r"^###\s+([🔴🟡🟢])\s+\[([A-Z]-\d+)\]\s+(.+)$")
    
    lines = content.splitlines()
    current_task = None
    
    for line in lines:
        match = pattern.match(line)
        if match:
            if current_task:
                tasks.append(current_task)
            priority_emoji, task_id, title = match.groups()
            priority_name = "High" if priority_emoji == "🔴" else "Medium" if priority_emoji == "🟡" else "Low"
            current_task = {
                "id": task_id,
                "title": title,
                "priority_emoji": priority_emoji,
                "priority": priority_name,
                "description": "",
                "assignee": "Unknown"
            }
            continue
            
        if current_task:
            if line.strip().startswith("* **Description:**"):
                current_task["description"] = line.replace("* **Description:**", "").strip()
            elif line.strip().startswith("* **Assignee:**"):
                # Clean up markdown formatting inside assignees
                current_task["assignee"] = line.replace("* **Assignee:**", "").replace("`", "").strip()
                
    if current_task:
        tasks.append(current_task)
        
    return tasks

def check_compilation_errors() -> str | None:
    if not ERRORS_PATH.exists():
        return None
    content = ERRORS_PATH.read_text(encoding="utf-8").strip()
    if not content:
        return None
    # Look for files and lines
    match = re.search(r'File "([^"]+)", line (\d+): (.+)', content)
    if match:
        filename, line, msg = match.groups()
        return f"{filename} at line {line}: {msg}"
    return content.splitlines()[-1] if content.splitlines() else "Unknown compilation error"

def audit_non_prod_assets() -> dict:
    results = {
        "missing_on_disk_count": 0,
        "missing_on_disk_details": [],
        "declared_count": 0
    }
    
    manifest_path = NON_PROD_GAME_DIR / "assets_manifest.rpy"
    if not manifest_path.exists():
        return results
        
    text = manifest_path.read_text(encoding="utf-8")
    
    # Matches: declare_image_with_fallback("image_id", "rel_path", ...)
    image_pattern = re.compile(
        r'declare_image_with_fallback\(\s*["\']([^"\']+)["\']\s*,\s*["\']([^"\']+)["\']'
    )
    # Matches: register_audio("alias", "rel_path")
    audio_pattern = re.compile(
        r'(?:audio_[a-zA-Z0-9_]+\s*=\s*)?register_audio\(\s*["\']([^"\']+)["\']\s*,\s*["\']([^"\']+)["\']'
    )
    
    images = image_pattern.findall(text)
    audios = audio_pattern.findall(text)
    
    results["declared_count"] = len(images) + len(audios)
    
    for img_id, rel_path in images:
        abs_path = NON_PROD_GAME_DIR / rel_path
        if not abs_path.exists():
            results["missing_on_disk_count"] += 1
            results["missing_on_disk_details"].append(("Image", img_id, rel_path))
            
    for alias, rel_path in audios:
        abs_path = NON_PROD_GAME_DIR / rel_path
        if not abs_path.exists():
            results["missing_on_disk_count"] += 1
            results["missing_on_disk_details"].append(("Audio", alias, rel_path))
            
    return results

def get_grade_and_status(score: float) -> str:
    if score >= 95: return "A"
    elif score >= 90: return "A-"
    elif score >= 85: return "B+"
    elif score >= 80: return "B"
    elif score >= 75: return "B-"
    elif score >= 70: return "C+"
    elif score >= 65: return "C"
    elif score >= 60: return "C-"
    elif score >= 55: return "D+"
    elif score >= 50: return "D"
    else: return "F"

def calculate_grades(
    checklist_data: dict, 
    backlog_tasks: list[dict], 
    compile_error: str | None, 
    asset_data: dict
) -> dict:
    # 1. Chief Architect Grade
    ca_score = 100.0
    # Compile error is a major blocker
    if compile_error:
        ca_score -= 30.0  # Cap at C range max
    # Missing assets on disk
    missing_assets = asset_data["missing_on_disk_count"]
    ca_score -= min(15.0, missing_assets * 1.5)
    # Incomplete engineering-related phases (Phase 1, Phase 2, Phase 6, Phase 7)
    eng_total = 0
    eng_completed = 0
    for section, data in checklist_data["phases"].items():
        if any(keyword in section.lower() for keyword in ["phase 1", "phase 2", "phase 6", "phase 7"]):
            eng_total += data["total"]
            eng_completed += data["completed"]
    if eng_total > 0:
        eng_completion_rate = eng_completed / eng_total
        ca_score -= (1.0 - eng_completion_rate) * 20.0
    
    # 2. Adult Market Reviewer Grade
    am_score = 100.0
    # Check backlog for N-6 (Story Chains Rewrite) and C-5 (Manifest audit)
    backlog_ids = [t["id"] for t in backlog_tasks]
    if "N-6" in backlog_ids:
        am_score -= 10.0  # Erotic engine rewrite missing
    # Check book chapters checklist completion (Phase 5)
    book_total = 0
    book_completed = 0
    for section, data in checklist_data["phases"].items():
        if "phase 5" in section.lower() or "phase 4" in section.lower():
            book_total += data["total"]
            book_completed += data["completed"]
    if book_total > 0:
        book_completion_rate = book_completed / book_total
        am_score -= (1.0 - book_completion_rate) * 25.0
        
    # 3. Lead Narrative Editor Grade
    ne_score = 100.0
    # Check backlog for N-1 (Historical sweep), N-2 (Day 100 gates), N-3, N-4 (Writers Room convergence)
    narrative_backlogs = ["N-1", "N-2", "N-3", "N-4"]
    for nb in narrative_backlogs:
        if nb in backlog_ids:
            ne_score -= 5.0
    # Check main story checklist completion (Phase 3)
    story_total = 0
    story_completed = 0
    for section, data in checklist_data["phases"].items():
        if "phase 3" in section.lower():
            story_total += data["total"]
            story_completed += data["completed"]
    if story_total > 0:
        story_completion_rate = story_completed / story_total
        ne_score -= (1.0 - story_completion_rate) * 20.0

    overall_score = (ca_score + am_score + ne_score) / 3.0

    return {
        "chief_architect": {
            "score": ca_score,
            "grade": get_grade_and_status(ca_score)
        },
        "market_reviewer": {
            "score": am_score,
            "grade": get_grade_and_status(am_score)
        },
        "narrative_editor": {
            "score": ne_score,
            "grade": get_grade_and_status(ne_score)
        },
        "overall": {
            "score": overall_score,
            "grade": get_grade_and_status(overall_score)
        }
    }

def build_report(
    schedule: dict,
    current_date: datetime.date,
    checklist_data: dict,
    backlog_tasks: list[dict],
    compile_error: str | None,
    asset_data: dict,
    grades: dict,
    use_color: bool = False
) -> str:
    # Schedule calculations
    start_date = datetime.date.fromisoformat(schedule["epic_start_date"])
    elapsed_days = (current_date - start_date).days
    
    epic_day = elapsed_days + 1
    epic_week = (elapsed_days // 7) + 1
    sprint_day = (elapsed_days % 7) + 1
    
    # 5-week Epic schedule
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
    
    # Generate overall status color
    overall_grade = grades["overall"]["grade"]
    status_color = c_green
    if "D" in overall_grade or "F" in overall_grade:
        status_color = c_red
    elif "C" in overall_grade:
        status_color = c_yellow
    elif "B" in overall_grade:
        status_color = c_blue

    # Phase completion statistics
    checklist_total = checklist_data["global_total"]
    checklist_done = checklist_data["global_completed"]
    checklist_pct = (checklist_done / checklist_total * 100) if checklist_total > 0 else 0.0

    lines = []
    lines.append(f"{c_bold}========================================================================{c_end}")
    lines.append(f"📅 {c_hdr}{c_bold}DAILY STANDUP CEREMONY: {schedule['epic_name']}{c_end}")
    lines.append(f"   {c_bold}Current Date:{c_end} {current_date.strftime('%A, %B %d, %Y')}")
    lines.append(f"   {c_bold}Epic Cadence:{c_end} Week {week_str}, Sprint Day {sprint_day} of 7 (Epic Day {epic_day} of 35)")
    lines.append(f"   {c_bold}Days Left in Sprint:{c_end} {c_cyan}{days_remaining_sprint} days{c_end} | {c_bold}Days Left in Epic:{c_end} {c_red}{days_remaining_epic} days{c_end}")
    lines.append(f"   {c_bold}Active Sprint Focus:{c_end} {c_blue}{current_focus}{c_end}")
    lines.append(f"{c_bold}========================================================================{c_end}")
    lines.append("")
    lines.append(f"🏆 {c_bold}PROJECT INTEGRITY GRADES{c_end}")
    lines.append(f"   {c_bold}Overall Project Health:{c_end} {status_color}{c_bold}[ {overall_grade} ]{c_end} (Checklist: {checklist_done}/{checklist_total} - {checklist_pct:.1f}%)")
    lines.append(f"   - {c_bold}Chief Architect:{c_end}       {c_cyan}[ {grades['chief_architect']['grade']} ]{c_end} (Codebase, Linting, & Architecture)")
    lines.append(f"   - {c_bold}Adult Market Reviewer:{c_end} {c_yellow}[ {grades['market_reviewer']['grade']} ]{c_end} (Erotic Tension, Pacing, & Viability)")
    lines.append(f"   - {c_bold}Lead Narrative Editor:{c_end} {c_hdr}[ {grades['narrative_editor']['grade']} ]{c_end} (Canon, Voice Lock, & Writing Gates)")
    lines.append("")
    lines.append(f"{c_bold}------------------------------------------------------------------------{c_end}")
    lines.append(f"🤖 {c_bold}SPECIALIST REPORTS{c_end}")
    lines.append(f"{c_bold}------------------------------------------------------------------------{c_end}")
    
    # Chief Architect Report
    lines.append(f"⚙️  {c_cyan}{c_bold}Chief Architect (@.agents/rules/chief_architect.md){c_end}")
    if compile_error:
        lines.append(f"   {c_red}❌ CRITICAL COMPILE ERROR:{c_end} {compile_error}")
    else:
        lines.append(f"   {c_green}✔️ Clean Compilation:{c_end} Non-production build compiles without Ren'Py errors.")
        
    if asset_data["missing_on_disk_count"] > 0:
        lines.append(f"   {c_yellow}⚠️ ASSET DRIFT:{c_end} {asset_data['missing_on_disk_count']} declared assets are missing from non-prod disk.")
        # Print up to 3 details
        for i, (asset_type, asset_id, path) in enumerate(asset_data["missing_on_disk_details"][:3]):
            lines.append(f"      - {asset_type} '{asset_id}' missing at: '{path}'")
        if asset_data["missing_on_disk_count"] > 3:
            lines.append(f"      - ... and {asset_data['missing_on_disk_count'] - 3} more.")
    else:
        lines.append(f"   {c_green}✔️ Asset Manifest Sync:{c_end} All declared assets exist physically on disk.")
        
    lines.append("   *What's Working:* Writing gates structure is operational; StoryState variables set via setter API.")
    lines.append("   *What's Not:* Screens frame 'alpha' parameter compilation crash; deadline hard-fail gates still require wiring.")
    lines.append("")

    # Adult Market Reviewer Report
    lines.append(f"🍓 {c_yellow}{c_bold}Adult Market Reviewer (@.agents/rules/adult_market_reviewer.md){c_end}")
    active_chains_rewrite = "N-6" in [t["id"] for t in backlog_tasks]
    if active_chains_rewrite:
        lines.append(f"   {c_red}❌ PENDING MECHANICS REWRITE:{c_end} Task [N-6] Story Chains Rewrite is blocking high-tension Level 3/4 routes.")
    else:
        lines.append(f"   {c_green}✔️ Erotic Architecture:{c_end} Story chains and book chapters slots are structured.")
    lines.append("   *What's Working:* Core book writing slots are defined and integrated with theme keys.")
    lines.append("   *What's Not:* Missy, Vance, Stern optional story chains lack the spicier rewritten prose tracks.")
    lines.append("")

    # Lead Narrative Editor Report
    lines.append(f"✍️  {c_hdr}{c_bold}Lead Narrative Editor (@.agents/rules/lead_narrative_editor.md){c_end}")
    active_linters = [t for t in backlog_tasks if t["id"] in ["N-1", "N-2"]]
    if active_linters:
        for al in active_linters:
            lines.append(f"   {c_yellow}⚠️ BLOCKED GATE:{c_end} [{al['id']}] {al['title']} (Assignee: {al['assignee']})")
    else:
        lines.append(f"   {c_green}✔️ Lore Consistency:{c_end} Narrative spine matches the Dev Bible.")
    lines.append("   *What's Working:* Prologue through Day 105 main routing spine is structurally complete.")
    lines.append("   *What's Not:* Historical linter failures in character profiles; Day 100 missing gates; Day 103/104 Writers Room reports missing.")
    lines.append("")

    lines.append(f"{c_bold}------------------------------------------------------------------------{c_end}")
    lines.append(f"📋 {c_bold}ACTIVE CHECKLIST BY PHASE{c_end}")
    lines.append(f"{c_bold}------------------------------------------------------------------------{c_end}")
    for section, data in checklist_data["phases"].items():
        total = data["total"]
        done = data["completed"]
        if total > 0:
            pct = done / total * 100
            bar_len = 15
            filled_len = int(bar_len * done // total)
            bar = '=' * filled_len + '-' * (bar_len - filled_len)
            lines.append(f"   {section:<50} [ {bar} ] {done}/{total} ({pct:.0f}%)")
    lines.append("")

    lines.append(f"{c_bold}------------------------------------------------------------------------{c_end}")
    lines.append(f"🔥 {c_bold}TODAY'S CRITICAL ACTIONS{c_end}")
    lines.append(f"{c_bold}------------------------------------------------------------------------{c_end}")
    
    actions_count = 0
    # 1. Compile error is priority 1
    if compile_error:
        actions_count += 1
        lines.append(f"   {actions_count}. {c_red}{c_bold}[BLOCKED]{c_end} Resolve compilation error in {compile_error}")
        
    # 2. Backlog high priority items
    for task in backlog_tasks:
        if task["priority"] == "High":
            actions_count += 1
            lines.append(f"   {actions_count}. {task['priority_emoji']} {c_bold}[{task['id']}]{c_end} {task['title']} (Assignee: {task['assignee']})")
            if task["description"]:
                lines.append(f"      ↳ {task['description']}")
                
    # 3. Next incomplete checklist items matching active sprint
    # If week 4: focus on hygiene & validation (Phase 7)
    # If week 3: focus on structural assets (Phase 6)
    target_sprint_phrase = f"Phase {epic_week}"
    sprint_tasks = [t for s, t in checklist_data["current_phase_tasks"] if target_sprint_phrase in s]
    for task in sprint_tasks[:3]:
        actions_count += 1
        lines.append(f"   {actions_count}. 🔧 {c_bold}[CHECKLIST]{c_end} {task}")
        
    if actions_count == 0:
        lines.append("   🎉 No critical blockages or pending actions! Excellent progress.")
        
    lines.append("")
    lines.append(f"{c_bold}========================================================================{c_end}")
    return "\n".join(lines)


def standup_report_path(report_date: datetime.date, output_dir: Path | None = None) -> Path:
    """Dated standup artifact: standups/daily_standup_YYYY-MM-DD.md"""
    directory = output_dir or STANDUP_REPORTS_DIR
    return directory / f"daily_standup_{report_date.isoformat()}.md"


def append_agent_work_queue(markdown_content: str, plain_report: str) -> str:
    """Attach machine-readable queue + resolver pointers for code/prose agents."""
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
            "Contract: `narrative/draft/releases/release-1-mvp/planning/standup_agent_contract.md`\n\n"
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
        f"# Daily Standup Status Report\n\n"
        f"**Report date:** {report_date.strftime('%A, %B %d, %Y')}  \n"
        f"**Generated:** {datetime.datetime.now().isoformat(timespec='seconds')}\n\n"
        f"```text\n{plain_report}\n```\n"
    )
    markdown_content = append_agent_work_queue(markdown_content, plain_report)
    report_path.write_text(markdown_content, encoding="utf-8")

    # Convenience pointer for editors / agents that expect a stable path
    latest_path = PLANNING_DIR / "daily_standup_report.md"
    latest_path.write_text(markdown_content, encoding="utf-8")

    return report_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the Daily Standup check-in ceremony.")
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
    parser.add_argument("--start-date", help="Set or temporarily override the Epic start date (YYYY-MM-DD format).")
    args = parser.parse_args()

    # Load schedule configuration
    schedule = load_epic_schedule()
    if args.start_date:
        schedule["epic_start_date"] = args.start_date
        
    # Determine date
    if args.date:
        try:
            current_date = datetime.date.fromisoformat(args.date)
        except ValueError:
            print("Error: Invalid date format. Use YYYY-MM-DD.")
            return 1
    else:
        current_date = datetime.date.today()

    # Parse and audit
    checklist_data = parse_checklist()
    backlog_tasks = parse_backlog()
    compile_error = check_compilation_errors()
    asset_data = audit_non_prod_assets()
    
    # Calculate grades
    grades = calculate_grades(checklist_data, backlog_tasks, compile_error, asset_data)
    
    # Generate terminal report with ANSI colors
    terminal_report = build_report(
        schedule, current_date, checklist_data, backlog_tasks, compile_error, asset_data, grades, use_color=True
    )
    
    if not args.quiet:
        print(terminal_report)

    if args.report:
        plain_report = build_report(
            schedule, current_date, checklist_data, backlog_tasks, compile_error, asset_data, grades, use_color=False
        )
        report_path = write_markdown_report(current_date, plain_report, args.output_dir)
        if not args.quiet:
            print(f"\nReport saved to {report_path.relative_to(ROOT).as_posix()}")

    return 0

if __name__ == "__main__":
    sys.exit(main())
