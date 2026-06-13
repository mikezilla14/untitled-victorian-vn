# Book1 Writing Feature MVP Backlog

Status: active non-prod MVP backlog.

This backlog tracks the remaining work required before the Book1 manuscript rendering feature is ready for MVP promotion review.

## Current State

- Non-prod Book1 engine/routing lives in `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/days/book1_non_canon.rpy`.
- Book1 manuscript prose lives in per-day files: `book1_day101_non_canon.rpy` through `book1_day105_non_canon.rpy`.
- Active MVP chapters route through label-based prose blocks.
- `book1_nvl_write_line(...)` provides word-by-word reveal and 4-line NVL pagination.
- `test_day2_writing_non_canon.rpy` provides direct render harness entries for the active chapter events.

## P0 - Stability

### B1-1: Ren'Py launcher lint and playtest

Run the non-prod project in Ren'Py 8.5.2 and test every direct Book1 harness entry.

Acceptance:

- no parse errors;
- no missing-label errors;
- no page overflow at normal text speed;
- Day 1, Day 2 predator/ghost/prey, Day 3, Day 4, and Day 5 render.

### B1-2: Confirm pagination limit

Verify `_book1_page_line_limit = 4` leaves 3-4 lines of visual whitespace at the bottom of the actual NVL screen.

Acceptance:

- adjust only the central page limit if screen testing shows overflow or excessive blank space.

### B1-3: Keep generated cache out of commits

Do not commit `non_prod_renpy_project/game/cache/shaders.txt`.

Acceptance:

- restore or ignore generated cache changes before feature commits.

## P1 - Architecture Completion

### B1-4: Remove quarantined macro code

After one successful Ren'Py playtest pass, delete the retired inline macro parser and legacy payload helper code from `book1_non_canon.rpy`.

Acceptance:

- no `Book1MacroEngine`;
- no active `BOOK1_PAYLOADS`;
- no `_book1_render_line` or `build_book1_chapter_packet`;
- Book1 render tests still pass.

### B1-5: Strengthen route debug coverage

Expand `book1_debug_chapter_route(...)` or add harness calls so every MVP chapter key can display its resolved route before rendering.

Acceptance:

- all active chapter keys report a concrete `book1_block_*` label.

## P2 - Presentation Polish

### B1-6: Align with visual styling spec

Compare the current NVL-only MVP implementation against `docs/specs/book-writing-styling.md`.

Acceptance:

- choose either current NVL-only presentation for MVP or a separate approved task for manuscript-page visuals.

### B1-7: Optional writing feedback

Consider cosmetic page-turn or ink-scratch feedback.

Acceptance:

- cosmetic only;
- no new persistent state;
- no changes to day routing, fuel, stats, or chapter completion.

## Validation

Use:

```powershell
py scripts/format_non_canon.py <changed .rpy files>
py scripts/validate.py --profile changed --agent non_prod_code_agent --files "<changed files>"
```

Manual Ren'Py QA remains required for final MVP acceptance.
