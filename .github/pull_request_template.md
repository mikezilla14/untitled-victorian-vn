## PR Purpose

- What does this change do for the 5-day MVP?
- Which day labels/flows does it impact?

## MVP Compliance (Required)

Reference: `docs/compliance_checklist.md`

- [ ] Scope supports 5-day MVP (no unrelated feature expansion)
- [ ] No new mandatory tooling/pipeline outside MVP
- [ ] No new global `default` outside `renpy_project/game/variables.rpy`
- [ ] Avoid direct `player.<stat>` assignments when mutation methods exist
- [ ] Suspicion guard flow remains safe (`check_suspicion` before passive decay)
- [ ] `script.rpy` remains thin (entry/guards, no heavy logic)
- [ ] Endings and route conditions still coherent
- [ ] Historical linter concerns reviewed for changed writers-room markdown

## Verification

- [ ] `renpy lint` run locally (if available)
- [ ] Relevant path(s) manually played/smoke tested

## Notes

- Risks:
- Follow-ups:
- Deferred:
