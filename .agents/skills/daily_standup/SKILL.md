# Management: Daily Automated Health Check

Runs **live automated validation** at the start of a session or on a daily schedule. Reports only checks that execute fresh each run — no stale `errors.txt`, checklist narration, or specialist grades.

For checklist progress, backlog, and Adult Market / narrative planning lenses, use [`integration_review`](../integration_review/SKILL.md) (weekly or ad-hoc).

## What to do

1. **Run the daily check**:

   ```powershell
   # Console report only (exit code 1 if any check failed)
   py scripts/daily_standup.py

   # Write dated markdown (also updates planning/daily_standup_report.md)
   py scripts/daily_standup.py --report
   ```

   Dated artifacts: `main-game/draft/releases/planning/standups/daily_standup_YYYY-MM-DD.md`

   **Scheduled (Windows, daily 6:00 AM local):**

   ```powershell
   ./scripts/register_daily_standup_task.ps1
   ./scripts/run_daily_standup.ps1   # smoke test
   ```

2. **What runs each day** (all live — nothing read from cache files):

   | Check | Script |
   |-------|--------|
   | Ren'Py contract lint (non-prod) | `renpy_contract_linter.py` |
   | Engineering compliance (non-prod) | `engineering_compliance.py` |
   | Scene direction | `scene_direction.py --check` |
   | Non-canon formatting | `format_non_canon.py --check` |
   | Historical linter | `historical_linter.py` |
   | Asset manifest disk sync | manifest vs disk |
   | `renpy lint` | `renpy_sdk.py` discovers newest SDK on PATH, `RENPY_SDK`, or `Documents/Renpy` |

3. **Action queue**: Failed checks only. Point agents at the report and use [action_from_standup](../action_from_standup/SKILL.md):

   ```powershell
   py scripts/resolve_work_item.py --from-standup --next
   ```

   Registry: [`docs/backlog/task_registry.json`](../../../docs/backlog/task_registry.json)  
   Contract: [`planning/standup_agent_contract.md`](../../../main-game/draft/releases/planning/standup_agent_contract.md)

4. **Planning / specialist review** (not daily): when you need checklist bars, backlog grades, or Adult Market Reviewer lens:

   ```powershell
   py scripts/integration_review.py --report
   ```

## Customization

Epic start date: `main-game/draft/releases/planning/epic_schedule.json` or `--start-date YYYY-MM-DD`.
