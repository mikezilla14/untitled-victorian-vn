# Management: Integration Review (weekly / ad-hoc)

Planning review for items that **do not have clear daily automated tests** or that change slowly: MVP checklist progress, backlog status, and specialist lens notes (Chief Architect, Adult Market Reviewer, Lead Narrative Editor).

Use this before sprint planning, promotion decisions, or when authoring an [`mvp_full_review`](../../../main-game/draft/releases/planning/mvp_full_review_2026-06-28.md)-style narrative.

**Do not** expect this to run on the daily schedule — use [`daily_standup`](../daily_standup/SKILL.md) for live validation.

## What to do

1. **Run the review**:

   ```powershell
   py scripts/integration_review.py
   py scripts/integration_review.py --report
   ```

   Dated artifacts: `main-game/draft/releases/planning/reviews/integration_review_YYYY-MM-DD.md`  
   Latest pointer: `planning/integration_review_report.md`

2. **What it covers**:

   - Checklist completion by phase (from `mvp_systems_integration_checklist.md`)
   - Open high-priority backlog items
   - Letter grades from planning lenses (not re-run market review prose)
   - Specialist notes referencing today's daily check results when relevant
   - Suggested planning actions (checklist + backlog — manual verification)

3. **Optional weekly schedule (Windows)** — register if desired:

   ```powershell
   # Example: Monday 7:00 AM (manual registration — not installed by default)
   $action = New-ScheduledTaskAction -Execute "powershell.exe" `
     -Argument "-NoProfile -ExecutionPolicy Bypass -Command `"cd '$PWD'; py scripts/integration_review.py --report --quiet`""
   $trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At "07:00"
   Register-ScheduledTask -TaskName "VictorianVN-WeeklyIntegrationReview" -Action $action -Trigger $trigger
   ```

4. **Full narrative review**: For deep Chief Architect / Adult Market / Lead Editor write-ups, copy the structure in `planning/mvp_full_review_YYYY-MM-DD.md` and gather evidence with `validate.py --profile full`, playtest matrix, and human playthrough notes.
