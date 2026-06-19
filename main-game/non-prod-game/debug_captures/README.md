# Runtime balance captures (non-prod only)

JSONL playtest telemetry for the Release 1 MVP route matrix (P1–P7).

## Output location

```text
main-game/non-prod-game/debug_captures/<run_id>.jsonl
```

Example: `P1_corruption_forward.jsonl`

## How to capture

1. Launch the **non-prod** Ren'Py project (`main-game/non-prod-game/`).
2. Press **F10** to show the balance debug overlay.
3. Click **P1** (or start a run from the Ren'Py console):

   ```renpy
   $ _capture_run_id = "P2_cautious"
   jump debug_capture_start
   ```

4. Play forward from `label start` without stat cheats.
5. Stop capture with the overlay **Stop** button or `jump debug_capture_stop`.

## Event types

Each line is one JSON object: `run_start`, `grain_enter`, `choice`, `gate`, `flag`, `rollback_event`, `ending`, `run_end`.

Every event includes a stats/suspicion snapshot per `testing_balance_framework_spec.md` Phase 3.

## Compare captures

```powershell
py main-game/pipeline/tools/compare_runtime_to_model.py --release release-1-mvp
py main-game/pipeline/tools/compare_runtime_to_model.py --release release-1-mvp --capture P1_corruption_forward
```

Captures with rollback are valid; summary reports mark `contains_rollback: true`.

## Public build

These files and `debug_run_capture.rpy` / overlay screens in `screens.rpy` are excluded from player-facing builds (Phase 10).
