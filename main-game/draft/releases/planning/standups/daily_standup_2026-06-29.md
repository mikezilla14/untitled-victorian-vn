# Daily Automated Health Check

**Report date:** Monday, June 29, 2026  
**Generated:** 2026-06-29T09:10:43

Live validation only. For checklist/backlog/specialist review: `py scripts/integration_review.py --report`

```text
========================================================================
📅 DAILY AUTOMATED HEALTH CHECK: Release 1 - MVP
   Current Date: Monday, June 29, 2026
   Epic Cadence: Week 5 (Extended), Sprint Day 1 of 7 (Epic Day 43 of 35)
   Days Left in Sprint: 6 days | Days Left in Epic: 0 days
   Active Sprint Focus: Extended Polish & Bug Fixing
========================================================================

🔬 AUTOMATED CHECKS (7 run, 6 passed, 1 failed, 0 skipped)
------------------------------------------------------------------------
   [PASS] Ren'Py contract lint (non-prod) — 54 script(s) checked.
   [PASS] Engineering compliance (non-prod) — 54 script(s) checked.
   [PASS] Scene direction ([asset auto]) — 19 draft script(s) checked.
   [PASS] Non-canon prose formatting — 19 draft script(s) checked.
   [PASS] Historical linter (drafts + bible) — 29 file(s) checked.
   [FAIL] Asset manifest disk sync (non-prod) — 13 declared asset(s) missing from both engines.
      - Image 'lady_eleanor_sprite furious' → images/sprites/cora/angry.png
      - Image 'ui_sidebar_bg' → images/ui/ui_sidebar_bg.webp
      - Image 'ui_book_blank' → images/ui/book/book_blank.png
      - Image 'ui_book_plate_paper_overlay' → images/ui/book/plate_paper_overlay.png
      - Image 'ui_book_plate_hatch_overlay' → images/ui/book/plate_hatch_overlay.png
      - ... and 5 more.
   [PASS] renpy lint (non-prod project) — Zero Ren'Py engine lint errors via renpy-8.5.3-sdk.

------------------------------------------------------------------------
🔥 ACTION QUEUE (failed checks only)
------------------------------------------------------------------------
   1. [FAIL] Asset manifest disk sync (non-prod): 13 declared asset(s) missing from both engines.
      ↳ py scripts/daily_asset_manifest.py

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
      "registry_id": "ASSET_DISK_FAIL",
      "lane": "audit",
      "title": "Resolve missing declared assets on disk",
      "agent": "chief_architect",
      "skill": "check_assets"
    }
  ]
}
```
