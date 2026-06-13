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
import subprocess
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
                "assignee": "Unknown",
                "completed": False
            }
            continue
            
        if current_task:
            if line.strip().startswith("* **Description:**"):
                desc = line.replace("* **Description:**", "").strip()
                current_task["description"] = desc
                current_task["completed"] = desc.lower().startswith("complete")
            elif line.strip().startswith("* **Assignee:**"):
                # Clean up markdown formatting inside assignees
                current_task["assignee"] = line.replace("* **Assignee:**", "").replace("`", "").strip()
                
    if current_task:
        tasks.append(current_task)
        
    return tasks

AGENT_MAPPING = {
    "non_prod_code_agent": {
        "lane": "code",
        "agent": "non_prod_code_agent",
        "skill": "implement_spec",
        "pipeline": "implement-spec",
        "pipeline_stage": 1
    },
    "prod_code_agent": {
        "lane": "code",
        "agent": "prod_code_agent",
        "skill": "promote_day",
        "pipeline": "promote-day",
        "pipeline_stage": 3
    },
    "writers_room": {
        "lane": "prose",
        "agent": "writers_room",
        "skill": "rewrite_narrative",
        "pipeline": "rewrite-narrative",
        "pipeline_stage": 1
    },
    "convergent_writer": {
        "lane": "prose",
        "agent": "convergent_writer",
        "skill": "convergent_writer",
        "pipeline": "produce-day",
        "pipeline_stage": 1
    },
    "victorian_consultant": {
        "lane": "prose",
        "agent": "victorian_consultant",
        "skill": "historical_check",
        "pipeline": "historical-check",
        "pipeline_stage": 1
    },
    "lead_narrative_editor": {
        "lane": "gate",
        "agent": "lead_narrative_editor",
        "skill": "review_scene",
        "pipeline": "review-scene",
        "pipeline_stage": 1
    },
    "chief_architect": {
        "lane": "audit",
        "agent": "chief_architect",
        "skill": "check_assets"
    }
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
        emoji, task_id, title = match.groups()
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
            "files": files
        }
    return tasks

def sync_backlog_to_registry():
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

def discover_scene_direction_issues(rpy_paths: list[str]) -> list[str]:
    if not rpy_paths:
        return []
    files_arg = ",".join(rpy_paths)
    cmd = [sys.executable, str(ROOT / "scripts" / "scene_direction.py"), "--files", files_arg, "--check"]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if res.returncode == 0:
        return []
    out_of_date = []
    for line in res.stdout.splitlines():
        if line.strip().startswith("-"):
            file_path = line.strip().strip("- ").strip()
            out_of_date.append(file_path)
    return out_of_date

def discover_formatting_issues(rpy_paths: list[str]) -> list[str]:
    if not rpy_paths:
        return []
    cmd = [sys.executable, str(ROOT / "scripts" / "format_non_canon.py"), "--check"] + rpy_paths
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if res.returncode == 0:
        return []
    out_of_date = []
    for line in res.stdout.splitlines():
        if line.strip().startswith("-"):
            file_path = line.strip().strip("- ").strip()
            out_of_date.append(file_path)
    return out_of_date

def discover_historical_issues(files: list[str]) -> list[str]:
    issues = []
    for f in files:
        cmd = [sys.executable, str(ROOT / "scripts" / "historical_linter.py"), "--file", f]
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        if res.returncode != 0:
            issues.append(f)
    return issues

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
    incomplete_backlog_ids = [t["id"] for t in backlog_tasks if not t.get("completed", False)]
    if "N-6" in incomplete_backlog_ids:
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
    narrative_backlogs = ["N-1", "N-2", "N-3", "N-4"]
    for nb in narrative_backlogs:
        if nb in incomplete_backlog_ids:
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
    use_color: bool = False,
    scene_dir_issues: list[str] = None,
    formatting_issues: list[str] = None,
    historical_issues: list[str] = None
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
        for i, (asset_type, asset_id, path) in enumerate(asset_data["missing_on_disk_details"][:3]):
            lines.append(f"      - {asset_type} '{asset_id}' missing at: '{path}'")
        if asset_data["missing_on_disk_count"] > 3:
            lines.append(f"      - ... and {asset_data['missing_on_disk_count'] - 3} more.")
    else:
        lines.append(f"   {c_green}✔️ Asset Manifest Sync:{c_end} All declared assets exist physically on disk.")
        
    checklist_content = CHECKLIST_PATH.read_text(encoding="utf-8") if CHECKLIST_PATH.exists() else ""
    deadline_gates_incomplete = "game_over_deadline_1" in checklist_content and re.search(r'game_over_deadline_1.*\[\s*\]', checklist_content) is not None
    deadline_gates_incomplete = deadline_gates_incomplete or (
        "game_over_deadline_2" in checklist_content and re.search(r'game_over_deadline_2.*\[\s*\]', checklist_content) is not None
    )
    
    hygiene_incomplete = False
    for section, data in checklist_data["phases"].items():
        if "phase 7" in section.lower():
            if data["completed"] < data["total"]:
                hygiene_incomplete = True
                
    ca_working = ["Writing gates structure is operational", "StoryState variables set via setter API"]
    ca_not_working = []
    
    if compile_error:
        ca_not_working.append(f"Compilation error: {compile_error}")
    if deadline_gates_incomplete:
        ca_not_working.append("Deadline hard-fail gates still require wiring")
    if asset_data["missing_on_disk_count"] > 0:
        ca_not_working.append(f"Asset drift ({asset_data['missing_on_disk_count']} missing assets)")
    if hygiene_incomplete:
        ca_not_working.append("Code hygiene & promotion prep (e.g. linting, dev debris cleanup) still pending")
        
    if not ca_not_working:
        ca_not_working.append("None (all architectural checks passing)")
        
    lines.append(f"   *What's Working:* {'; '.join(ca_working)}.")
    lines.append(f"   *What's Not:* {'; '.join(ca_not_working)}.")
    lines.append("")

    # Adult Market Reviewer Report
    lines.append(f"🍓 {c_yellow}{c_bold}Adult Market Reviewer (@.agents/rules/adult_market_reviewer.md){c_end}")
    incomplete_backlog_ids = [t["id"] for t in backlog_tasks if not t.get("completed", False)]
    active_chains_rewrite = "N-6" in incomplete_backlog_ids
    if active_chains_rewrite:
        lines.append(f"   {c_red}❌ PENDING MECHANICS REWRITE:{c_end} Task [N-6] Story Chains Rewrite is blocking high-tension Level 3/4 routes.")
    else:
        lines.append(f"   {c_green}✔️ Erotic Architecture:{c_end} Story chains and book chapters slots are structured.")
        
    am_working = ["Core book writing slots are defined and integrated with theme keys"]
    if not active_chains_rewrite:
        am_working.append("Missy, Vance, Stern optional story chains rewritten and integrated with high-tension tracks")
        
    am_not_working = []
    if active_chains_rewrite:
        am_not_working.append("Missy, Vance, Stern optional story chains lack the spicier rewritten prose tracks")
        
    book_routing_incomplete = False
    for section, data in checklist_data["phases"].items():
        if "phase 5" in section.lower():
            if data["completed"] < data["total"]:
                book_routing_incomplete = True
                
    if book_routing_incomplete:
        am_not_working.append("Book 1 chapter routing, NVL rendering verification, or writing test harnesses are still pending")
        
    if not am_not_working:
        am_not_working.append("None (all market and erotic engine structures verified)")
        
    lines.append(f"   *What's Working:* {'; '.join(am_working)}.")
    lines.append(f"   *What's Not:* {'; '.join(am_not_working)}.")
    lines.append("")

    # Lead Narrative Editor Report
    lines.append(f"✍️  {c_hdr}{c_bold}Lead Narrative Editor (@.agents/rules/lead_narrative_editor.md){c_end}")
    
    n1_done = "N-1" not in incomplete_backlog_ids
    n2_done = "N-2" not in incomplete_backlog_ids
    n3_done = "N-3" not in incomplete_backlog_ids
    n4_done = "N-4" not in incomplete_backlog_ids
    n5_done = "N-5" not in incomplete_backlog_ids
    
    active_narrative_tasks = [t for t in backlog_tasks if t["id"] in ["N-1", "N-2", "N-3", "N-4"] and not t["completed"]]
    if active_narrative_tasks:
        for al in active_narrative_tasks:
            lines.append(f"   {c_yellow}⚠️ BLOCKED GATE:{c_end} [{al['id']}] {al['title']} (Assignee: {al['assignee']})")
    else:
        lines.append(f"   {c_green}✔️ Lore Consistency:{c_end} Narrative spine matches the Dev Bible.")
        
    ne_working = ["Prologue through Day 105 main routing spine is structurally complete"]
    if n1_done:
        ne_working.append("Lore consistency sweeps are clean (character profiles period vocabulary aligned)")
    if n2_done:
        ne_working.append("Day 100 prologue specialist gates cleared")
    if n3_done and n4_done:
        ne_working.append("Day 103/104 Writers Room pipeline convergent reports and gates generated")
        
    ne_not_working = []
    if not n1_done or (historical_issues and any("bible" in x or "characters" in x for x in historical_issues)):
        ne_not_working.append("Historical linter failures in character profiles")
    if not n2_done:
        ne_not_working.append("Day 100 missing gates")
    if not n3_done or not n4_done:
        ne_not_working.append("Day 103/104 Writers Room reports or gates missing")
    if not n5_done or (formatting_issues and any("day102" in x for x in formatting_issues)):
        ne_not_working.append("Day 102 prose formatting repair is pending")
        
    discovered_narrative_failures = []
    if scene_dir_issues:
        discovered_narrative_failures.append(f"Scene direction out-of-date ({len(scene_dir_issues)} files)")
    if formatting_issues:
        other_formatting = [x for x in formatting_issues if "day102" not in x]
        if other_formatting:
            discovered_narrative_failures.append(f"Prose formatting repair needed ({len(other_formatting)} files)")
    if historical_issues:
        other_historical = [x for x in historical_issues if "bible" not in x and "characters" not in x]
        if other_historical:
            discovered_narrative_failures.append(f"Historical linter violations in day files ({len(other_historical)} files)")
            
    if discovered_narrative_failures:
        ne_not_working.append(f"Linter/validation failures: {', '.join(discovered_narrative_failures)}")
        
    spine_incomplete = False
    for section, data in checklist_data["phases"].items():
        if "phase 3" in section.lower():
            if data["completed"] < data["total"]:
                spine_incomplete = True
                
    if spine_incomplete:
        ne_not_working.append("Main story spine walkthrough and branch smoke tests still require manual validation")
        
    if not ne_not_working:
        ne_not_working.append("None (all narrative gating and validation checks passing)")
        
    lines.append(f"   *What's Working:* {'; '.join(ne_working)}.")
    lines.append(f"   *What's Not:* {'; '.join(ne_not_working)}.")
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
        if task["priority"] == "High" and not task.get("completed", False):
            actions_count += 1
            lines.append(f"   {actions_count}. {task['priority_emoji']} {c_bold}[{task['id']}]{c_end} {task['title']} (Assignee: {task['assignee']})")
            if task["description"]:
                lines.append(f"      ↳ {task['description']}")
                
    # 3. Discovered issues
    if scene_dir_issues:
        for f in scene_dir_issues:
            actions_count += 1
            lines.append(f"   {actions_count}. 🔍 {c_bold}[DISCOVERED]{c_end} Update scene direction for {f}")
            lines.append(f"      ↳ Run scene direction linter: py scripts/scene_direction.py --files \"{f}\"")
            
    if formatting_issues:
        for f in formatting_issues:
            actions_count += 1
            lines.append(f"   {actions_count}. 🔍 {c_bold}[DISCOVERED]{c_end} Format {f}")
            lines.append(f"      ↳ Run formatter: py scripts/format_non_canon.py \"{f}\"")
            
    if historical_issues:
        for f in historical_issues:
            actions_count += 1
            lines.append(f"   {actions_count}. 🔍 {c_bold}[DISCOVERED]{c_end} Fix historical linter errors in {f}")
            lines.append(f"      ↳ Run historical check: py scripts/historical_linter.py --file \"{f}\"")

    # 4. Next incomplete checklist items matching active sprint
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

    # Sync backlog to registry first!
    sync_backlog_to_registry()

    # Parse and audit
    checklist_data = parse_checklist()
    backlog_tasks = parse_backlog()
    compile_error = check_compilation_errors()
    asset_data = audit_non_prod_assets()
    
    # Run discovery phase
    non_prod_game_dir = ROOT / "narrative" / "draft" / "releases" / "release-1-mvp" / "non_prod_renpy_project" / "game"
    rpy_files = sorted(non_prod_game_dir.rglob("*_non_canon.rpy"))
    rpy_paths = [f.relative_to(ROOT).as_posix() for f in rpy_files]
    
    bible_dir = ROOT / "narrative" / "draft" / "bible"
    bible_files = sorted(bible_dir.glob("*.md"))
    bible_paths = [f.relative_to(ROOT).as_posix() for f in bible_files]
    
    scene_dir_issues = discover_scene_direction_issues(rpy_paths)
    formatting_issues = discover_formatting_issues(rpy_paths)
    historical_issues = discover_historical_issues(rpy_paths + bible_paths)
    
    # Calculate grades
    grades = calculate_grades(checklist_data, backlog_tasks, compile_error, asset_data)
    
    # Generate terminal report with ANSI colors
    terminal_report = build_report(
        schedule, current_date, checklist_data, backlog_tasks, compile_error, asset_data, grades, use_color=True,
        scene_dir_issues=scene_dir_issues, formatting_issues=formatting_issues, historical_issues=historical_issues
    )
    
    if not args.quiet:
        print(terminal_report)

    if args.report:
        plain_report = build_report(
            schedule, current_date, checklist_data, backlog_tasks, compile_error, asset_data, grades, use_color=False,
            scene_dir_issues=scene_dir_issues, formatting_issues=formatting_issues, historical_issues=historical_issues
        )
        report_path = write_markdown_report(current_date, plain_report, args.output_dir)
        if not args.quiet:
            print(f"Report saved to {report_path.relative_to(ROOT).as_posix()}")

    return 0

if __name__ == "__main__":
    sys.exit(main())
