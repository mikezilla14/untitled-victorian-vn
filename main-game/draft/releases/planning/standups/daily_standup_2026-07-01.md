# Daily Automated Health Check

**Report date:** Wednesday, July 01, 2026  
**Generated:** 2026-07-01T06:00:12

Live validation only. For checklist/backlog/specialist review: `py scripts/integration_review.py --report`

```text
========================================================================
📅 DAILY AUTOMATED HEALTH CHECK: Release 1 - MVP
   Current Date: Wednesday, July 01, 2026
   Epic Cadence: Week 5 (Extended), Sprint Day 3 of 7 (Epic Day 45 of 35)
   Days Left in Sprint: 4 days | Days Left in Epic: 0 days
   Active Sprint Focus: Extended Polish & Bug Fixing
========================================================================

🔬 AUTOMATED CHECKS (7 run, 6 passed, 1 failed, 0 skipped)
------------------------------------------------------------------------
   [PASS] Ren'Py contract lint (non-prod) — 54 script(s) checked.
   [PASS] Engineering compliance (non-prod) — 54 script(s) checked.
   [PASS] Scene direction ([asset auto]) — 19 draft script(s) checked.
   [FAIL] Non-canon prose formatting — 1 file(s) need formatting.
      - C:\Users\mikez\OneDrive\Documents\gh\git\untitled-victorian-vn\main-game\non-prod-game\game\shared\story_chains_non_canon.rpy
   [PASS] Historical linter (drafts + bible) — 29 file(s) checked.
   [PASS] Asset manifest disk sync (non-prod) — All declared assets exist on disk (non-prod or prod pool).
   [PASS] renpy lint (non-prod project) — Zero Ren'Py engine lint errors via renpy-8.5.3-sdk.

------------------------------------------------------------------------
🔥 ACTION QUEUE (failed checks only)
------------------------------------------------------------------------
   1. 🔍 [DISCOVERED] Format C:\Users\mikez\OneDrive\Documents\gh\git\untitled-victorian-vn\main-game\non-prod-game\game\shared\story_chains_non_canon.rpy
      ↳ py scripts/format_non_canon.py "C:\Users\mikez\OneDrive\Documents\gh\git\untitled-victorian-vn\main-game\non-prod-game\game\shared\story_chains_non_canon.rpy"

========================================================================
```

## Agent work queue

Point code or prose agents at this report, then resolve the next item:

```powershell
py scripts/resolve_work_item.py --from-standup --next
```

Skill: `.agents/skills/action_from_standup/SKILL.md`  
Registry: `docs/backlog/task_registry.json`  
Contract: `main-game/draft/releases/planning/standup_agent_contract.md`

```json
{
  "items": [
    {
      "priority": 1,
      "registry_id": "DISCOVERED_FORMAT",
      "lane": "prose",
      "title": "Format file C:\\Users\\mikez\\OneDrive\\Documents\\gh\\git\\untitled-victorian-vn\\main-game\\non-prod-game\\game\\shared\\story_chains_non_canon.rpy",
      "agent": "writers_room",
      "skill": "revise_narrative"
    }
  ]
}
```
