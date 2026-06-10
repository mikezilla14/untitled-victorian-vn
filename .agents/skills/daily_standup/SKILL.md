# Management: Daily Standup Ceremony

Simulates a daily check-in ceremony to refocus on the MVP systems integration checklist, project backlog, and codebase health. It coordinates the reports and letter grades of the **Chief Architect**, **Adult Market Reviewer**, and **Lead Narrative Editor** to align work with the weekly sprint and 5-week epic cadence.

Use this daily at the start of a session or whenever you want to refocus and reprioritize.

## What to do

1. **Calculate the Sprint Timeline**:
   Check where the project is within the 5-week epic release cadence:
   * **Week 1 (Sprint 1)**: Spine Routing & Fuel Gates (M1, M3)
   * **Week 2 (Sprint 2)**: Dynamic Systems, Story Chains & Fail States (M2)
   * **Week 3 (Sprint 3)**: UI & Structural Assets Integration (M4)
   * **Week 4 (Sprint 4)**: Full-fidelity Verification & Prose Drop (M5)
   * **Week 5 (Sprint 5)**: Soft Launch to Subscribers, Next Release Planning, & Playtest Bug Fixes (M6 / Ship)

2. **Execute the Standup Audit**:
   Run the daily standup script to automatically query the codebase status, parse checklists, and inspect the backlog:
   ```powershell
   # Console report only
   py scripts/daily_standup.py

   # Write dated markdown (also updates planning/daily_standup_report.md)
   py scripts/daily_standup.py --report
   ```
   Dated artifacts: `narrative/draft/releases/release-1-mvp/planning/standups/daily_standup_YYYY-MM-DD.md`

   **Scheduled (Windows, daily 6:00 AM local):**
   ```powershell
   .\scripts\register_daily_standup_task.ps1
   .\scripts\run_daily_standup.ps1   # smoke test
   ```

3. **Align Specialist Tasks & Grades**:
   Evaluate the status of the three distinct domains:
   * **Chief Architect (`@.agents/rules/chief_architect.md`)**: Analyzes compilation errors in the non-prod project (via `errors.txt`), linter issues, and missing asset declarations.
   * **Adult Market Reviewer (`@.agents/rules/adult_market_reviewer.md`)**: Focuses on erotic pacing, spicier story chains rewrite (Task `[N-6]`), and book chapters slots.
   * **Lead Narrative Editor (`@.agents/rules/lead_narrative_editor.md`)**: Audits character voice lock, historical linting sweep (Task `[N-1]`), and day gate verdicts.

4. **Action Today's Checklist**:
   Prioritize "Today's Critical Actions" printed by the script, beginning with compile blockers and high-priority backlog tasks.

## Customization

To initialize or shift the Epic start date, modify `narrative/draft/releases/release-1-mvp/planning/epic_schedule.json` or pass the `--start-date` argument:
```powershell
py scripts/daily_standup.py --start-date 2026-05-18
```
