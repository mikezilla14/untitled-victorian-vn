# Story Chain Routing Refactor Spec

Status: planned.

Chief Architect verdict: approved for non-production implementation after the contract updates in this spec. This is a routing hygiene refactor only. It must preserve the player-facing Ren'Py experience: prose, dialogue, menu meaning, stat effects, branch availability, and visible scene order stay the same unless a separate gated narrative change brief is approved.

## Purpose

Release 1 non-canon drafts currently let optional story chains and penance/confrontation labels seize control of day flow. The target architecture is:

```text
days own time; dynamic content interrupts and returns
```

Day files should be readable writer-first Ren'Py scripts with explicit time-period spines. Optional chains and queued consequences may interrupt a time period, but they return to the caller and do not decide the next day or time period.

## Source Of Truth

- Non-production scripts: `main-game/non-prod-game/game/days/`
- Non-production shared routing: `main-game/non-prod-game/game/shared/`
- Implementation contracts: `.agents/rules/writers_room.md`, `.agents/rules/non_prod_code_agent.md`, `.agents/rules/prod_code_agent.md`, `.agents/rules/chief_architect.md`
- Book writing contract: `docs/contracts/book_writing_contract.md`
- DAG spec and graph tooling: `docs/specs/DAG-tag-implementation.md`, `main-game/pipeline/tools/build_story_graph_manifest.py`

Production files under `main-game/prod-game/` are read-only during the non-prod refactor. Promotion happens later through `prod_code_agent` after gates.

## Architect Findings

1. The draft direction is correct: `jump expression _chain_label` from day files and `jump advance_after_confrontation` from chain labels are the core smells.
2. The original draft spec conflicted with the older label contract. Final ruling: structural time-period labels such as `day103_morning` are allowed as routing spine labels. Major authored scene labels should still use the existing `dayRdd_p_location_description` pattern unless they are intentionally replacing a time-period spine.
3. `check_confrontations` should stop acting as a routine checkpoint in ordinary prose labels. Confrontation/penance content should be queued and consumed only by authored consequence windows.
4. `end_slot`, `POST_PENANCE_ROUTES`, and `advance_after_confrontation` should remain temporarily as compatibility infrastructure, but migrated labels must not call them.
5. DAG/context tags are part of the acceptance surface. The implementation must maintain existing `[ASSET]`, `[STATE]`, `[CHOICE]`, `[BEAT]`, and `[DAG_*]` comments, preserve manual DAG tags, and run graph sync after `.rpy` edits.

## Required Structure

Each refactored day gets a visible time-period spine:

```renpy
label day103:
    jump day103_morning

label day103_morning:
    $ time_manager.set_current_day(3)
    $ set_time_period("Morning")
    jump day103_1_servants_corridor

label day103_afternoon:
    $ set_time_period("Afternoon")
    jump day103_2_suite_gideon_tea

label day103_evening:
    $ set_time_period("Evening")
    jump day103_3_bedroom_cora_frantic_writing_event

label day103_night:
    $ set_time_period("Night")
    jump day103_2_suite_night_tea
```

Compatibility labels may remain during migration. Prefer moving routing responsibility to the time-period spine without moving or rewriting prose unless necessary.

## Dynamic Windows

Optional chain content appears only through explicit, day-specific windows:

```renpy
label day103_morning_story_window:
    menu:
        "Follow Stern's discipline before the guest wing wakes." if story.chain_available("stern"):
            $ _chain_label = story.resolve_chain_label("stern")
            call expression _chain_label

        "Find Missy while the house is still bruised from yesterday." if story.chain_available("missy"):
            $ _chain_label = story.resolve_chain_label("missy")
            call expression _chain_label

        "Watch the Locke Suite door before the tea order becomes a summons." if story.chain_available("vance"):
            $ _chain_label = story.resolve_chain_label("vance")
            call expression _chain_label

        "Keep moving with the cart and give no one a reason.":
            $ apply_effects(insp=10, corr=0)

    return
```

Rules:

- Optional chains are called, not jumped to.
- Dynamic windows return to their time-period label.
- Chain labels return to their dynamic window.
- A day should normally have one or two dynamic windows, not one resolver per scene.
- Do not introduce a generic `resolve_content(...)` day framework.

## Penance Queue

Add penance queue support to `classes_non_canon.rpy` first:

```renpy
self.pending_penance = []
```

Required methods:

```renpy
def queue_penance(self, penance_label):
    if penance_label not in self.pending_penance:
        self.pending_penance.append(penance_label)

def has_pending_penance(self):
    return len(self.pending_penance) > 0

def pop_penance_for_window(self, window_id):
    if not self.pending_penance:
        return None
    return self.pending_penance.pop(0)

def clear_penance(self):
    self.pending_penance = []
```

Keep `penance_triggered` temporarily as a compatibility bridge until migrated files no longer reference it.

Consequence windows consume queued penance:

```renpy
label day103_evening_consequence_window:
    $ _penance_label = story.pop_penance_for_window("day103_evening")
    if _penance_label:
        call expression _penance_label
    return
```

Existing `confrontation_stern`, `confrontation_vance`, and `confrontation_missy` labels may remain as compatibility aliases, but migrated penance labels must end with `return`, not `jump advance_after_confrontation`.

## Prose Preservation

Implementation agents must preserve all narration, dialogue, menu meaning, and manuscript prose verbatim.

Allowed technical edits:

- Add time-period labels.
- Add dynamic window labels.
- Add compatibility aliases.
- Move existing prose between labels only when player-facing order and branch conditions remain unchanged.
- Convert `jump expression _chain_label` to `call expression _chain_label`.
- Convert migrated chain/penance label exits from `jump advance_after_confrontation` to `return`.
- Replace routine `call check_confrontations` with explicit consequence windows where the spec maps one.

Forbidden without a narrative change brief:

- New bridge prose.
- Rewritten dialogue or narration.
- Changed menu text meaning.
- Changed stat effects, branch gates, or psychological branch intent.
- Moving Book1 manuscript prose into day labels.

## Day Migration Map

Phase 1: shared routing cleanup.

- Update `classes_non_canon.rpy` with `pending_penance` and helper methods.
- Update `classes_non_canon_notes.md`.
- Convert `stern_chain_1/2/3`, `missy_chain_1/2/3`, and `vance_chain_1/2/3` to return.
- Convert confrontation/penance labels to return.
- Mark `advance_after_confrontation`, `POST_PENANCE_ROUTES`, and `end_slot` as deprecated compatibility infrastructure.

Phase 2: Day 103 pilot.

- Introduce or normalize `day103`, `day103_morning`, `day103_afternoon`, `day103_evening`, and `day103_night`.
- Convert `day103_1_optional_character_chain` into `day103_morning_story_window` or a compatibility wrapper around that window.
- Replace optional-chain dynamic jumps with dynamic calls.
- Remove routine `call check_confrontations` from ordinary Day 103 prose labels.
- Add `day103_evening_consequence_window` only if queued penance needs to land there.
- Keep Gideon brush-test and ultimatum branches as fixed core content, not optional story-chain content.
- Run graph sync and review Day 103 before touching other days.

Phase 3: Day 101 and Day 102.

- Add `day101_night_story_window`.
- Add `day102_afternoon_story_window`.
- Remove `end_slot` from refactored day endings where the next day/time is explicit.

Phase 4: Day 104.

- Preserve the false-dawn heist spine.
- Distinguish atonement from penance: atonement is a chosen safety action; penance is an imposed queued consequence.
- Add `day104_evening_consequence_window` only if queued penance needs a landing point.

Phase 5: Day 105.

- Keep this light. Add time-period labels only if they improve graph readability.
- Do not over-engineer the fixed confrontation day.

## DAG And Context Tags

Implementation must maintain existing marker comments:

```text
[ASSET]
[STATE]
[CHOICE]
[BEAT]
```

Add or refresh DAG tags for new structural labels when practical:

```renpy
# [DAG_NODE id=day103_morning type=time_period day=103 period=Morning]
# [DAG_NODE id=day103_morning_story_window type=dynamic_window day=103 period=Morning window=story_chain returns_to=day103_morning]
# [DAG_DYNAMIC allows=stern,missy,vance penance=false]
# [DAG_NODE id=stern_chain_1 type=story_chain chain=stern tier=1 returns_to=caller]
# [DAG_NODE id=day103_evening_consequence_window type=dynamic_window day=103 period=Evening window=consequence penance=true returns_to=day103_evening]
```

Manual DAG tags are human-authored. Preserve any `[DAG_* ... manual]` tag unless the human explicitly asks to overwrite manual DAG tags.

## Acceptance Criteria

The implementation is complete when:

1. Each migrated day has a readable time-period spine.
2. Normal passage of time uses explicit `jump` targets owned by the day file.
3. Optional chains are called from named dynamic windows.
4. Optional story-chain labels return.
5. Penance/consequence labels return.
6. No migrated chain or penance label uses `jump advance_after_confrontation`.
7. No migrated day label uses `jump expression _chain_label` for optional chains.
8. `check_confrontations` is not called as a routine checkpoint in ordinary prose labels.
9. Penance lands only through authored consequence windows.
10. Existing `[ASSET]`, `[STATE]`, `[CHOICE]`, `[BEAT]`, and `[DAG_*]` context tags are preserved or deliberately refreshed under the DAG tag rules.
11. Book1 manuscript prose remains in `book1_block_*` labels and continues to be invoked through `book1_write_chapter(...)`.
12. Graph outputs show time-period flow with optional breakouts returning to the day spine.
13. Verbatim creative preservation is verified before review.

## Validation And Sync

Run after implementation:

```powershell
py scripts/orchestrate_review.py --files "main-game/non-prod-game/game/days/day103_non_canon.rpy"
py scripts/validate.py --profile changed --agent non_prod_code_agent --skip-gate-checks --files "main-game/non-prod-game/game/days/day103_non_canon.rpy"
py main-game/pipeline/tools/build_story_graph_manifest.py --release release-1-mvp --out-dir main-game/pipeline/releases/release-1-mvp/graph --storyboard main-game/draft/releases/planning/story_board.md
```

For multi-file implementation, include every changed `.rpy`, shared mockup, and notes file in validation. After graph generation, run `storyboard_sync` only if `release1_graph_gaps.md` or `release1_graph_audit.md` reports storyboard drift.

Promotion validation later remains the `prod_code_agent` path, including Ren'Py lint with zero errors.

## Open Questions

- Which exact Day 104 consequence window should consume queued penance if it blocks writing opportunity?
- Should `check_confrontations` be fully retired after migration, or kept indefinitely as a compatibility alias for old graph artifacts?
- Should the graph extractor eventually enforce `returns_to=caller` for `story_chain` nodes, or continue reporting it as audit metadata only?
