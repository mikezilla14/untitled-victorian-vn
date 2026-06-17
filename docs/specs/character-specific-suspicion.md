# Character-Specific Suspicion Spec

## Purpose

Replace the global suspicion vignette with a quieter social-perception system. Suspicion belongs to the character watching Cora; anxiety belongs to Cora. The player should feel a glance land badly, not see a generic danger overlay.

Target workflow:

- Writers and non-prod code agents can mark who noticed Cora with an explicit `raise_suspicion(character, amount, reason=None, scene_context=None)` call.
- Runtime code tracks suspicion per character and Cora anxiety separately.
- UI/audio feedback identifies the suspicious character only when suspicion changes or crosses a breakpoint.
- Breakpoint monologues are short, authored lines selected from a table, not generated at runtime.

Status: `partial`

Implementation plan: [character-specific-suspicion-implementation-plan.md](character-specific-suspicion-implementation-plan.md)

Implemented so far:

- `raise_suspicion(...)` helper.
- Breakpoint memory on `PlayerStats`.
- Breakpoint monologue fallback table.
- `apply_effects(..._susp, ..._base)` routing through suspicion feedback.
- Small character-specific attention UI at `xpos 0.4`, `ypos 0.5`.
- Callback-driven sprite emphasis where suspicion focus wins over active speaker focus.
- Authored suspicion prose separated from trigger/runtime logic.

Deferred:

- Final eye art.
- Sound cue polish.
- Expanded character/reason/scene monologue table.

## Replaces

The previous implementation rendered `ui_suspicion_vignette` in `stats_overlay` at `alpha = player.anxiety / 100`. That treated anxiety as a global screen effect and made every anxious moment visually identical. This spec removes that behavior and reserves heavy full-screen effects for rare future critical moments only.

## Source Of Truth Files

Runtime implementation targets:

- `main-game/prod-game/game/classes.rpy`
- `main-game/prod-game/game/functions.rpy`
- `main-game/prod-game/game/suspicion_monologues.rpy`
- `main-game/prod-game/game/screens.rpy`
- `main-game/prod-game/game/assets_manifest.rpy`
- `main-game/prod-game/game/asset_transforms.rpy`
- `main-game/prod-game/game/00auto_highlight.rpy`

Non-prod mirror targets:

- `main-game/non-prod-game/game/shared/classes_non_canon.rpy`
- `main-game/non-prod-game/game/shared/functions_non_canon.rpy`
- `main-game/non-prod-game/game/shared/suspicion_monologues_non_canon.rpy`
- `main-game/non-prod-game/game/screens.rpy`
- `main-game/non-prod-game/game/shared/assets_manifest.rpy`
- `main-game/non-prod-game/game/shared/asset_transforms.rpy`
- `main-game/non-prod-game/game/shared/00auto_highlight.rpy`

Feature CI/CD path:

1. Implement and validate changes in the non-prod Ren'Py project under `main-game/non-prod-game/game/`.
2. Promote the validated non-prod shape into `main-game/prod-game/game/`.
3. Do not implement new feature behavior in production first.

## Model

Tracked characters for MVP:

- `stern`
- `vance`
- `gideon`
- `missy`

Suspicion is character-specific. Cora anxiety is separate.

```renpy
default suspicion_breakpoints_seen = {
    "stern": [],
    "vance": [],
    "gideon": [],
    "missy": [],
}

default suspicion_focus = None
default suspicion_focus_intensity = 0
```

If suspicion remains class-backed on `PlayerStats`, do not introduce loose global suspicion numbers. Use existing per-character suspicion helpers where present, and add breakpoint history either to `PlayerStats` or an adjacent class-backed state object.

## Tiers

Suspicion breakpoints:

```renpy
define SUSPICION_BREAKPOINTS = [15, 35, 60, 85]
```

| Value | Tier | Meaning |
|---:|---|---|
| 0-14 | clear | Nothing meaningful has landed. |
| 15-34 | noticed | Something felt wrong. |
| 35-59 | watching | They are evaluating Cora. |
| 60-84 | dangerous | They suspect a pattern. |
| 85-100 | critical | One more mistake could expose her. |

Anxiety tiers:

| Value | Tier | Meaning |
|---:|---|---|
| 0-34 | low | Controlled, cold, or confident. |
| 35-69 | medium | Alert and pressured. |
| 70-100 | high | Panic-tinged perception. |

## API

Primary call:

```renpy
$ raise_suspicion("vance", 12, reason="recognised_detail", scene_context="suite_evening")
```

Required behavior:

- Clamp suspicion totals to `0..100`.
- Apply minor feedback on every non-zero suspicion change.
- Trigger a scene interruption only when the character crosses a new breakpoint upward.
- Store seen breakpoints by character so repeated checks do not retrigger old monologues.
- Suspicion increases may raise anxiety, but not automatically. Writers should call anxiety changes separately when intended.

## Feedback Rules

Minor suspicion change:

- Set `suspicion_focus` to the affected character.
- Set `suspicion_focus_intensity = 1`.
- Pulse a small per-character eye/attention UI for `1.5` seconds.
- Optionally play a soft notice sound when sound is enabled.
- Clear focus after a short pause.

Breakpoint crossing:

- Set `suspicion_focus_intensity = 2`.
- Show the same eye/attention UI at a stronger state.
- Select and show one short Cora inner monologue line.
- Clear focus after the monologue returns.

Do not use a persistent red full-screen vignette for ordinary suspicion or anxiety.

## Dialogue Highlight Integration

Sprite emphasis should prioritize psychological focus over ordinary speaker focus:

1. If the character is `suspicion_focus`, apply suspicion emphasis.
2. Else if the character is `active_speaker`, apply normal speaker highlight.
3. Else apply idle dim.

The suspicion emphasis should stay restrained: small scale/contrast/brightness shifts are acceptable. Full-screen pulses are reserved for critical future polish, not MVP.

## Eye UI

The eye UI is per-character, not global.

MVP display:

- Small eye/attention indicator near the dialogue box or HUD edge.
- Current placeholder position is `xpos 0.4`, `ypos 0.5`, center-anchored.
- Character name or short label beside it.
- Eye openness reflects that character's current suspicion tier.
- Hidden when no suspicion event is active.

Exact values and breakpoint history remain hidden from the player. Ledger/debug displays may expose broad states for testing, but the player-facing flow should avoid visible numeric suspicion meters.

## Monologue Selection

Monologues are table-driven and hand-authored.

The prose table lives outside the trigger/runtime functions so writers can update authored reaction lines without editing suspicion mechanics:

- Non-prod source: `main-game/non-prod-game/game/shared/suspicion_monologues_non_canon.rpy`
- Production mirror: `main-game/prod-game/game/suspicion_monologues.rpy`

Lookup inputs:

- character
- suspicion tier
- anxiety tier
- optional reason
- optional scene context

Fallback priority:

1. character + suspicion tier + anxiety tier + reason + scene context
2. character + suspicion tier + anxiety tier + reason
3. character + suspicion tier + anxiety tier
4. character + suspicion tier
5. generic + suspicion tier + anxiety tier
6. generic fallback

Lines should usually be one sentence. The system should read like Cora noticing the room shift, not like a diary interruption.

## Character Flavor

Vance: intimate, unstable, socially dangerous; recognition and mutual performance.

Stern: procedural and disciplinary; rules, hierarchy, inspection, memory.

Gideon: predatory and amused; power, patience, civility as threat.

Missy: emotionally costly; trust, hurt, confusion, moral consequence.

## MVP Passes

Pass 1: Mechanical suspicion

- Implement `raise_suspicion`.
- Track breakpoints seen by character.
- Select monologue lines at breakpoints.
- Use existing inner monologue speaker/screen.

Pass 2: UI and sprite focus

- Add `suspicion_focus` state.
- Add small per-character eye/attention screen.
- Wire suspicion focus into existing sprite/dialogue highlight priority.

Pass 3: Text table

- Add 5-8 lines each for Vance, Stern, Gideon, and Missy.
- Add generic fallback lines for missing combinations.
- Keep reason/scene tags sparse until writers prove they need more.

## Validation

After implementation:

```powershell
py scripts/validate.py --profile changed --agent human --files "main-game/prod-game/game/classes.rpy" "main-game/prod-game/game/functions.rpy" "main-game/prod-game/game/screens.rpy"
py scripts/validate.py --profile changed --agent writers_room --skip-gate-checks --files "main-game/non-prod-game/game/shared/classes_non_canon.rpy" "main-game/non-prod-game/game/shared/functions_non_canon.rpy" "main-game/non-prod-game/game/screens.rpy"
```

Manual smoke checks:

- Raising suspicion without crossing a breakpoint produces only minor feedback.
- Crossing `15`, `35`, `60`, or `85` produces exactly one monologue for that character and breakpoint.
- Raising Vance suspicion while Stern is speaking emphasizes Vance, not Stern.
- High anxiety changes monologue flavor without creating a persistent full-screen red overlay.

## Remaining Pickup Tasks

- Add or update a lightweight script/test fixture if an appropriate Ren'Py function-level harness exists.
- Manually smoke test the minor popup timing and placement.
- Manually smoke test Vance crossing `15` from below.
- Manually smoke test Vance rising within the same tier.
- Manually smoke test Stern jumping across multiple breakpoints; only the highest crossed breakpoint should monologue.
- Manually smoke test suspicion reduction.
- Manually smoke test high-anxiety monologue selection.

## Recorded Decisions

- Breakpoint history lives on `PlayerStats`.
- Breakpoint detection uses total suspicion, including both base and acute suspicion.
- The MVP eye UI uses a text/symbol placeholder; final art is deferred polish.
- Player-facing UI does not show exact suspicion numbers.
