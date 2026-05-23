#!/usr/bin/env python3
"""
Promotion & Code Review Orchestrator

This script orchestrates the various agent compliance checks.
It can be run ad-hoc on any file(s) or as part of a promotion pipeline.
It generates a Markdown-formatted Remediation Report.

Usage:
    py scripts/orchestrate_review.py --files "path/to/file1.rpy,path/to/file2.rpy"

Will run all agent contracts on the specified files and generate a remediation report.

Example:
    py scripts/orchestrate_review.py --files "narrative/draft/releases/release-1-mvp/days/day103/day103_non_canon.rpy,renpy_project/game/day103.rpy"
"""

import argparse
import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Tuple

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

class AgentContract:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def run_check(self, files: List[str]) -> Tuple[bool, str]:
        """Returns (success_boolean, output_string)"""
        raise NotImplementedError

class ScriptWrapperContract(AgentContract):
    def __init__(self, name: str, description: str, script_name: str, args_flag: str = "--files"):
        super().__init__(name, description)
        self.script_name = script_name
        self.args_flag = args_flag

    def run_check(self, files: List[str]) -> Tuple[bool, str]:
        script_path = ROOT / "scripts" / self.script_name
        if not script_path.exists():
            return False, f"Error: {self.script_name} not found."
        
        all_success = True
        all_output = []
        
        if self.args_flag == "--file":
            # Run once per file
            for file in files:
                cmd = [sys.executable, str(script_path), self.args_flag, file]
                try:
                    result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT))
                    if result.returncode != 0:
                        all_success = False
                        out = result.stdout.strip()
                        if result.stderr.strip():
                            out += "/n" + result.stderr.strip()
                        all_output.append(f"[{file}]/n{out}")
                except Exception as e:
                    all_success = False
                    all_output.append(f"[{file}] Failed to execute: {e}")
            
            if all_success:
                return True, ""
            return False, "/n/n".join(all_output)
        else:
            # Run once with comma-separated list
            cmd = [sys.executable, str(script_path), self.args_flag, ",".join(files)]
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT))
                success = result.returncode == 0
                output = result.stdout.strip()
                if result.stderr.strip():
                    output += "/n" + result.stderr.strip()
                return success, output
            except Exception as e:
                return False, f"Failed to execute {self.script_name}: {e}"

class WritersRoomPipelineContract(AgentContract):
    def __init__(self):
        super().__init__(
            "Writers' Room Pipeline",
            "Convergent report, spec scripts, and gate verdict artifacts for non-canon days.",
        )

    def run_check(self, files: List[str]) -> Tuple[bool, str]:
        from writers_room_pipeline import validate_day_pipeline

        non_canon = [
            f
            for f in files
            if f.replace("//", "/").startswith("narrative/draft/")
            and f.replace("//", "/").endswith("_non_canon.rpy")
        ]
        if not non_canon:
            return True, "No non-canon day scripts in scope."

        failures = 0
        lines: List[str] = []
        for file in non_canon:
            count, messages = validate_day_pipeline(
                file,
                require_gates=True,
                partial_gates=True,
            )
            failures += count
            lines.extend(messages)

        if failures:
            return False, "/n".join(lines)
        return True, "Writers' room pipeline artifacts OK."


class FileNamingContract(AgentContract):
    def __init__(self):
        super().__init__("Gatekeeper Orchestrator", "Enforces file naming conventions")

    def run_check(self, files: List[str]) -> Tuple[bool, str]:
        violations = []
        for f in files:
            path = Path(f)
            name = path.name
            norm = path.as_posix()
            
            # Legacy naming checks
            if "day" in name and "non_canon" in name and not name.endswith("_non_canon.rpy"):
                if name.endswith(".md"):
                    violations.append(f"{f}: Legacy .md narrative drafts are no longer supported. Use .rpy.")
            
        if violations:
            return False, "/n".join(violations)
        return True, "File naming conventions passed."


def generate_report(results: Dict[str, Tuple[bool, str]]) -> str:
    report = []
    report.append("# Agent Contract Remediation Report/n")
    
    all_passed = all(success for success, _ in results.values())
    
    if all_passed:
        report.append("✅ **All Agent Contracts Passed!** The code is ready for promotion/merge./n")
        return "/n".join(report)
    
    report.append("❌ **Action Required:** One or more agent contracts failed. Please review the issues below and provide this report to your AI assistant for remediation./n")
    
    for agent_name, (success, output) in results.items():
        if not success:
            report.append(f"## 🛑 {agent_name} Violations")
            report.append("```text")
            report.append(output)
            report.append("```/n")
            
    report.append("---/n")
    report.append("### 🤖 Prompt for AI Assistant")
    report.append("Copy and paste the following into your chat:/n")
    report.append("> **Please fix the following agent contract violations in my files:**")
    for agent_name, (success, output) in results.items():
        if not success:
            report.append(f"> /n> **{agent_name}:**/n> {output.replace(chr(10), chr(10)+'> ')}")
            
    return "/n".join(report)

def main():
    parser = argparse.ArgumentParser(description="Orchestrate agent contract reviews.")
    parser.add_argument("--files", required=True, help="Comma-separated list of files to review")
    args = parser.parse_args()

    files = [f.strip() for f in args.files.split(",") if f.strip()]
    if not files:
        print("No files provided.")
        return 0

    # Define the contracts to enforce
    contracts = [
        FileNamingContract(),
        WritersRoomPipelineContract(),
        ScriptWrapperContract(
            name="Chief Architect & Prod Code Agent (Engineering)",
            description="Enforces state mutations, syntax, and architecture.",
            script_name="engineering_compliance.py"
        ),
        ScriptWrapperContract(
            name="Chief Architect (Ren'Py Contracts)",
            description="Enforces speaker definitions, variable interpolation, and callable symbols.",
            script_name="renpy_contract_linter.py"
        ),
        ScriptWrapperContract(
            name="Victorian Consultant (Historical Accuracy)",
            description="Checks for anachronisms in narrative drafts.",
            script_name="historical_linter.py",
            args_flag="--file" # Note: historical_linter.py might only take one file, but we'll try passing comma sep or adapt it.
        )
    ]

    results = {}
    print("Running Agent Contract Checks.../n")
    for contract in contracts:
        print(f"[{contract.name}] checking...")
        success, output = contract.run_check(files)
        results[contract.name] = (success, output)

    print("/n" + "="*50 + "/n")
    report = generate_report(results)
    print(report)
    
    all_passed = all(success for success, _ in results.values())
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
