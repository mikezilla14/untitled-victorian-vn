# Narrative Pressure UI, Objective Journal, and Manuscript Readiness System Spec

## Purpose and Target Workflow

The game should not present Cora’s progress as raw numerical stat management. The player is not “levelling up a maid.” They are guiding Cora through scandal, risk, compromise, discovery, and authorship.

This feature reframes stats as **narrative pressure systems**:
- **Inspiration** becomes chapter-bound manuscript material.
- **Corruption** unlocks darker approaches and manuscript variants.
- **Suspicion** represents character-specific external danger.
- **Objectives** give the player direction without making the game feel like a chore checklist.
- **The journal** becomes the central planning interface.
- **Non-diegetic cues** heighten tension without drowning scenes in popup spam.

### Target Workflow
- **Writers** can award standard or high-tier manuscript material, spend focus, activate/complete objectives, and trigger composite notifications using simple Ren'Py Python wrapper calls.
- **Runtime logic** manages material expiration, assignment readiness, objective transitions, and context-aware HUD prioritization.
- **Players** interact with a clean, thematic HUD and open an immersive journal to track their active leads, manuscripts, and immediate character risks.

---

## Status
Status: `planned`

---

## Source-of-Truth Files

Non-prod files:
- [narrative_pressure_data.rpy](../../main-game/non-prod-game/game/shared/narrative_pressure_data.rpy)
- [narrative_pressure_system.rpy](../../main-game/non-prod-game/game/shared/narrative_pressure_system.rpy)
- [narrative_notification_screen.rpy](../../main-game/non-prod-game/game/shared/narrative_notification_screen.rpy)
- [journal_screen.rpy](../../main-game/non-prod-game/game/shared/journal_screen.rpy)
- [hud_screen.rpy](../../main-game/non-prod-game/game/shared/hud_screen.rpy)

Production files (promoted after validation — not yet in tree):
- `main-game/prod-game/game/narrative_pressure_data.rpy`
- `main-game/prod-game/game/narrative_pressure_system.rpy`
- `main-game/prod-game/game/narrative_notification_screen.rpy`
- `main-game/prod-game/game/journal_screen.rpy`
- `main-game/prod-game/game/hud_screen.rpy`

---

## Validation Command or Review Path

To validate implementation:
```powershell
py scripts/validate.py --profile changed --agent human --files "main-game/prod-game/game/narrative_pressure_data.rpy" "main-game/prod-game/game/narrative_pressure_system.rpy" "main-game/prod-game/game/narrative_notification_screen.rpy" "main-game/prod-game/game/journal_screen.rpy" "main-game/prod-game/game/hud_screen.rpy"
py scripts/validate.py --profile changed --agent writers_room --skip-gate-checks --files "main-game/non-prod-game/game/shared/narrative_pressure_data.rpy" "main-game/non-prod-game/game/shared/narrative_pressure_system.rpy" "main-game/non-prod-game/game/shared/narrative_notification_screen.rpy" "main-game/non-prod-game/game/shared/journal_screen.rpy" "main-game/non-prod-game/game/shared/hud_screen.rpy"
```

Manual smoke-testing checklist:
- Verify that standard material allows completing the baseline draft.
- Verify that high-tier variants remain locked without their specific tier/tag/corruption requirements.
- Verify that overflow material converts to Draft Quality.
- Verify that focus consumption triggers objective expiration correctly.
- Verify that HUD risk prioritization adapts dynamically to scene relevance and character context.
- Verify that multiple stat updates flush to a single composite notification window instead of serial popups.

---

## Open Questions or Deferred Decisions

- **UI Visual Assets**: The exact styling, text styling, background frame designs, and icon visual design for the Journal and HUD screens.
- **Sound Design**: The specific audio files to play for standard vs breakpoint notifications.
- **Save/Load Compatibility**: Ensuring all dynamic lists and dictionaries (like `manuscript_material`, `objectives`, and `pending_notification_bundle`) are properly registered as Ren'Py defaults so they are correctly serialized in save slots.

---

## 1. Feature Summary

The game should not present Cora’s progress as raw numerical stat management. The player is not “levelling up a maid.” They are guiding Cora through scandal, risk, compromise, discovery, and authorship.

This feature reframes stats as **narrative pressure systems**:

* **Inspiration** becomes chapter-bound manuscript material.
* **Corruption** unlocks darker approaches and manuscript variants.
* **Suspicion** represents character-specific external danger.
* **Objectives** give the player direction without making the game feel like a chore checklist.
* **The journal** becomes the central planning interface.
* **Non-diegetic cues** heighten tension without drowning scenes in popup spam.

The revised implementation avoids three major traps:

1. Inspiration is no longer wiped wastefully after assignment completion.
2. Notification popups are composited into a single event layer rather than sequentially queued.
3. HUD risk display is based on scene relevance, not simply the highest global suspicion value.

---

## 2. Core Design Principle

The UI should always answer five questions:

1. **Can Cora write the next manuscript passage?**
2. **What does she still need?**
3. **Who is currently dangerous to her?**
4. **What darker option has opened?**
5. **What opportunity is about to vanish?**

Raw stats can exist internally, but the player-facing layer should prioritise thresholds, readiness, locks, and consequences.

Bad player-facing UI:

```text
Inspiration: 8
Corruption: 3
Suspicion: 4
```

Better player-facing UI:

```text
Current Manuscript: Ready
Scandalous draft unavailable — missing high-tier material.
Vance: Watchful in this scene.
```

---

## 3. Revised Core Loop

```text
Player needs manuscript material
            │
            ▼
Chooses safe, improper, or dangerous action
            │
            ▼
Gains material, flags, or leverage
            │
            ▼
Consumes limited chapter opportunity
            │
            ▼
Unlocks manuscript draft, optional route, or danger state
            │
            ▼
Writes / delays / escalates
```

The pressure should come from **opportunity cost**, **limited windows**, and **exclusive story paths**, not from arbitrary stat punishment.

Rejected model:

```text
Gain inspiration → magically increase suspicion
```

Better model:

```text
Use a safe action → gain low-tier material but spend limited focus.
Use a dangerous action → gain stronger material and unlock route flags, but risk character-specific suspicion.
```

---

## 4. Stat Reframing

### 4.1 Inspiration

#### Narrative Meaning

Inspiration is not generic creative mana. It is **usable manuscript material**:

* overheard secrets
* sensory details
* compromising observations
* emotional shocks
* private objects
* social contradictions
* leverage
* moments Cora can turn into fiction

#### Mechanical Role

Inspiration supports manuscript readiness, but it now has **tier and source metadata**.

There are three broad material tiers:

| Tier                           | Source                                                         |                    Yield | Manuscript Impact                     |
| ------------------------------ | -------------------------------------------------------------- | -----------------------: | ------------------------------------- |
| **Tier 1: Safe Detail**        | Chores, observation, mundane overhearing                       |     +1 standard material | Baseline / respectable draft only     |
| **Tier 2: Improper Discovery** | Eavesdropping, snooping, social manipulation                   | +2 material + chain flag | Scandalous draft prerequisites        |
| **Tier 3: High-Risk Secret**   | Theft, blackmail evidence, direct betrayal, dangerous intimacy |          unique catalyst | Blackmail / ruin / major route unlock |

The important change: **not all inspiration is equally useful.**

A player can fill the baseline requirement with safe material, but they cannot unlock the stronger manuscript variants without specific higher-tier material.

---

### 4.2 Corruption

#### Narrative Meaning

Corruption measures how far Cora has shifted from observer to participant.

It represents:

* willingness to exploit people
* comfort with impropriety
* appetite for scandal
* readiness to turn private harm into public fiction
* ability to pursue darker story chains

#### Mechanical Role

Corruption should unlock:

* riskier choices
* crueler dialogue options
* scandalous manuscript variants
* bolder blackmail strategies
* morally compromised routes

Corruption should **not** replace specific material requirements.

Bad:

```text
Scandalous Draft unlocked because Corruption >= 3
```

Better:

```text
Scandalous Draft requires:
- Corruption 3
- One Tier 2 or higher scandal material
```

This prevents corruption from becoming a generic master key.

---

### 4.3 Suspicion

#### Narrative Meaning

Suspicion is external danger and must remain character-specific.

```renpy
default suspicion = {
    "vance": 0,
    "gideon": 0,
    "stern": 0,
    "missy": 0,
}
```

#### Mechanical Role

Suspicion affects:

* confrontation scenes
* route closure
* access to private spaces
* dialogue tone
* whether a character watches Cora more closely
* whether optional objectives become dangerous or unavailable

Suspicion should increase from **concrete risky actions**, not from abstract inspiration gain.

Good causes:

```text
Cora is caught lingering.
Cora lies badly.
Cora steals an object.
Cora is seen near a forbidden door.
Cora asks the wrong question.
```

Bad cause:

```text
Cora had an internal creative insight.
```

---

## 5. Chapter Opportunity Economy

### 5.1 Focus Slots

Each chapter or chapter segment should have a finite number of **Focus Slots**.

These represent Cora’s limited opportunity to investigate, work, listen, write, manipulate, or take risks before the story moves on.

Example:

```renpy
default chapter_focus_remaining = 6
```

Actions consume focus:

| Action Type                 |                        Focus Cost |
| --------------------------- | --------------------------------: |
| Safe chore observation      |                                 1 |
| Minor snooping              |                                 1 |
| Risky eavesdropping         |                                 2 |
| Major optional chain action |                               2–3 |
| Writing assignment          | special action / scene transition |

The point is not to simulate time perfectly. The point is to prevent grinding.

---

### 5.2 Safe Material Cannot Feed High-Tier Manuscripts

Safe material can complete the baseline draft, but it cannot unlock the best variants.

Example assignment:

```text
The House Behind the Velvet Door

Baseline Draft:
- 5 standard material

Scandalous Draft:
- 5 standard material
- Corruption 2
- At least one Tier 2 scandal material

Blackmail Draft:
- 5 standard material
- Blackmail Material 1
- At least one Tier 3 secret
```

This creates the intended dilemma:

> “Do I take the safe inspiration now, or spend the opportunity chasing the dangerous chain?”

That is much better than punishing the player with arbitrary suspicion tax.

---

### 5.3 Vanishing Windows

Some optional objectives should expire when:

* focus is exhausted
* a scene changes
* a chapter ends
* the player chooses a safe alternative
* another chain is completed
* a character leaves the current location

Example:

```renpy
default objectives["obj_follow_vance"]["expires_when"] = {
    "chapter": "chapter_01",
    "focus_below": 2,
    "flags_blocking": ["completed_safe_evening_chore"]
}
```

Player-facing journal wording:

```text
Opportunity fading:
Vance will not remain alone for long.
```

This is far more elegant than turning every action into a stat penalty.

---

## 6. Inspiration Consumption and Overflow

### 6.1 No Hard Wipe

The old model said:

```renpy
current_inspiration = 0
```

That is too blunt. It risks wasting player effort.

The revised model uses **assignment consumption plus overflow conversion**.

When Cora writes an assignment:

1. Required material is consumed.
2. Excess usable material may convert into Draft Quality.
3. Chapter-specific material may expire at chapter end.
4. Some major material flags persist as story facts.

---

### 6.2 Material Bank Model

Instead of one flat inspiration number, track material entries.

```renpy
default manuscript_material = []
```

Example material object:

```renpy
{
    "id": "mat_locked_room_glimpse",
    "chapter_id": "chapter_01",
    "assignment_id": "assignment_01",
    "value": 2,
    "tier": 2,
    "tags": ["scandal", "vance", "locked_room"],
    "quality": "scandalous",
    "expires_after_chapter": True,
    "consumed": False,
}
```

This allows the journal and manuscript system to answer better questions:

* How much usable material does Cora have?
* Is it safe filler or high-tier scandal?
* Does it apply to the current assignment?
* Does it unlock a variant?
* Will it expire?

---

### 6.3 Assignment Completion Logic

Recommended MVP behavior:

```renpy
init python:

    def complete_assignment(assignment_id):
        assignment = writing_assignments[assignment_id]

        usable_material = get_usable_material_for_assignment(assignment_id)
        required_value = assignment["required_material"]

        consumed_material = consume_material_to_value(
            usable_material,
            required_value
        )

        overflow_value = get_unconsumed_usable_material_value(assignment_id)

        if overflow_value > 0:
            add_draft_quality(assignment_id, overflow_value * 10)

        apply_assignment_variant_flags(assignment_id)

        assignment["status"] = "complete"

        advance_to_next_assignment()
```

Important implementation rule:

> Do not silently destroy valuable player effort.

If material cannot carry forward, convert it into something visible:

```text
Surplus notes improved Draft Quality.
```

or:

```text
The lead has gone cold, but Cora salvages a sharper descriptive passage.
```

---

### 6.4 Chapter-End Decay

At chapter end:

* unspent chapter-specific material expires
* major flags persist
* some overflow converts into Draft Quality or “Notes”
* safe filler should not carry forward as full-value inspiration

Example:

```renpy
init python:

    def expire_chapter_material(chapter_id):
        for mat in manuscript_material:
            if mat["chapter_id"] == chapter_id and not mat["consumed"]:
                if mat.get("expires_after_chapter", True):
                    convert_expired_material_to_notes(mat)
                    mat["consumed"] = True
```

Player-facing journal text:

```text
Some material has gone cold.
Cora preserves what she can in her notes.
```

This keeps inspiration from becoming a hoardable stockpile.

---

## 7. Draft Quality and Manuscript Variants

### 7.1 Draft Quality Role

Draft Quality should not become another boring stat. It should be a behind-the-scenes modifier that affects:

* manuscript reception
* confidence in writing scenes
* later publication flavour
* ending epilogue details
* whether Cora’s work feels competent, scandalous, or genuinely dangerous

Recommended MVP model:

```renpy
default draft_quality = {
    "assignment_01": 0,
    "assignment_02": 0,
}
```

Use broad tiers:

| Draft Quality | Tier      | Narrative Meaning                          |
| ------------: | --------- | ------------------------------------------ |
|          0–19 | Rough     | Cora has material, but the writing is thin |
|         20–39 | Competent | The piece works                            |
|         40–59 | Striking  | The piece has force                        |
|           60+ | Dangerous | The piece could wound reputations          |

Do not make endings depend on tiny numeric differences. Use thresholds and flags.

---

### 7.2 Manuscript Variant Flags

Manuscript choices should be driven by both quality and content flags.

Example flags:

```renpy
default manuscript_flags = {
    "assignment_01_respectable": False,
    "assignment_01_scandalous": False,
    "assignment_01_blackmail_detail": False,
    "assignment_01_cruel_version": False,
}
```

Variant requirements:

```renpy
"variants": {
    "respectable": {
        "required_material": 5,
        "required_tier": 1,
    },
    "scandalous": {
        "required_material": 5,
        "required_corruption": 2,
        "required_tags": ["scandal"],
        "min_material_tier": 2,
    },
    "blackmail": {
        "required_material": 5,
        "required_blackmail_material": 1,
        "required_tags": ["evidence"],
        "min_material_tier": 3,
    }
}
```

This is the right model: **quality affects strength; flags affect content.**

---

### 7.3 Ending Impact Recommendation

For MVP, use **tiered manuscript outcomes**, not granular arithmetic.

Example ending modifiers:

```text
Respectable Author Ending:
- Completed required manuscripts
- Low scandal flags
- Low public fallout

Scandalous Success Ending:
- At least two scandalous manuscript flags
- Draft Quality average >= 30

Blackmail Ruin Ending:
- Blackmail manuscript flag
- Gideon leverage chain complete
- Suspicion or exposure state unresolved

Compromised Author Ending:
- High corruption
- Strong manuscripts
- personal relationships damaged
```

The ending should read player choices by **pattern**, not by one master score.

---

## 8. Objective Journal

### 8.1 Purpose

The journal gives the player direction and keeps the story spine visible.

It should make clear that Cora is not merely completing maid chores. She is:

* gathering material
* securing leverage
* surviving scrutiny
* preparing manuscripts
* deciding how far she is willing to go

---

### 8.2 Journal Sections

Recommended sections:

1. **Current Manuscript**
2. **Active Objectives**
3. **Optional Opportunities**
4. **Risks**
5. **Completed**
6. **Notes Gone Cold** — optional, useful for reinforcing decay

---

### 8.3 Current Manuscript Example

```text
Current Manuscript:
The House Behind the Velvet Door

Status:
Baseline Draft Ready

Material:
- Standard Material: 5 / 5
- Scandal Material: 0 / 1
- Blackmail Material: 0 / 1

Available Drafts:
- Respectable Draft

Locked Drafts:
- Scandalous Draft: requires one high-tier scandal material
- Blackmail Draft: requires blackmail evidence
```

This is much stronger than:

```text
Inspiration: 5
```

---

### 8.4 Optional Opportunity Example

```text
Optional Opportunity:
Follow Vance after supper.

Reward:
- Possible Tier 2 scandal material
- May unlock Vance chain

Cost:
- 2 Focus

Risk:
- Vance suspicion may increase if Cora is seen.

Expires:
- When evening duties are complete.
```

This gives the player a real strategic choice without turning the game into a spreadsheet.

---

## 9. Objective Data Model

```renpy
default objectives = {
    "obj_assignment_01_material": {
        "title": "Gather material for the first manuscript",
        "description": "Cora needs enough vivid material to turn private scandal into fiction.",
        "category": "manuscript",
        "status": "active",
        "required": True,
        "hidden": False,
        "focus_cost": 0,
        "expires_when": {},
        "rewards": {},
        "risk_text": "",
    },

    "obj_follow_vance": {
        "title": "Follow Vance after supper",
        "description": "Vance may lead Cora toward stronger material than ordinary chores can provide.",
        "category": "optional",
        "status": "active",
        "required": False,
        "hidden": False,
        "focus_cost": 2,
        "expires_when": {
            "chapter": "chapter_01",
            "focus_below": 2,
            "flags_blocking": ["completed_evening_duties"]
        },
        "rewards": {
            "material_id": "mat_vance_supper_secret"
        },
        "risk_text": "Vance suspicion may increase if Cora is seen.",
    },

    "obj_blackmail_gideon": {
        "title": "Find leverage against Gideon",
        "description": "Cora needs more than suspicion before she can safely move against him.",
        "category": "story",
        "status": "inactive",
        "required": True,
        "hidden": False,
        "focus_cost": 2,
        "expires_when": {},
        "rewards": {
            "blackmail_material": 1
        },
        "risk_text": "Failure may increase Gideon’s suspicion.",
    },
}
```

Statuses:

```renpy
"hidden"
"inactive"
"active"
"complete"
"failed"
"expired"
```

---

## 10. Suspicion Context and HUD Relevance

### 10.1 Problem

The HUD cannot simply show the highest suspicion value globally.

Example:

* Vance Suspicion: 4
* Ms. Stern Suspicion: 3
* Current scene: Cora is standing in front of Ms. Stern

The HUD should show Ms. Stern, because she is the immediate threat.

---

### 10.2 Character Context State

Track character presence and current scene relevance.

```renpy
default character_context = {
    "vance": {
        "present": False,
        "location": None,
        "scene_relevant": False,
    },
    "gideon": {
        "present": False,
        "location": None,
        "scene_relevant": False,
    },
    "stern": {
        "present": False,
        "location": None,
        "scene_relevant": False,
    },
    "missy": {
        "present": False,
        "location": None,
        "scene_relevant": False,
    },
}
```

Scene scripts should set context at scene start:

```renpy
$ set_scene_context(
    location="servants_corridor",
    present=["stern", "cora"],
    relevant=["stern"]
)
```

---

### 10.3 HUD Risk Priority

Recommended priority:

1. Present and scene-relevant character with highest suspicion.
2. Present character with highest suspicion.
3. Character attached to active objective in current location.
4. Global highest suspicion only if it has reached a major breakpoint.
5. Otherwise show no risk or show “No immediate watcher.”

Pseudo-code:

```renpy
init python:

    def get_hud_risk_character():
        candidates = []

        for char_id, ctx in character_context.items():
            suspicion_value = suspicion.get(char_id, 0)

            if suspicion_value <= 0:
                continue

            score = suspicion_value

            if ctx.get("present"):
                score += 100

            if ctx.get("scene_relevant"):
                score += 50

            if character_attached_to_active_objective(char_id):
                score += 25

            if suspicion_value >= get_major_breakpoint(char_id):
                score += 10

            candidates.append((score, char_id))

        if not candidates:
            return None

        candidates.sort(reverse=True)
        return candidates[0][1]
```

This prevents the HUD from panicking the player about someone irrelevant to the current scene.

It also avoids accidental spoilers.

---

## 11. Non-Diegetic Cue System

### 11.1 Revised MVP Rule

Do not build twelve animation states for v0.1.

Use only two cue levels:

1. **Standard Delta**

   * lightweight, non-blocking cue
   * appears briefly
   * does not halt dialogue flow

2. **Breakpoint Crossed**

   * stronger full-screen or modal cue
   * may pause the scene
   * may trigger inner monologue

This is enough for MVP.

---

### 11.2 Cue Categories

Each category has its own visual identity:

| Cue         | Visual Language                | Example                    |
| ----------- | ------------------------------ | -------------------------- |
| Inspiration | paper, quill, ink bloom        | “New material gained.”     |
| Corruption  | dark ink, wine/purple stain    | “Cora’s restraint slips.”  |
| Suspicion   | eye, red flash, sharp vignette | “Vance noticed something.” |
| Objective   | journal slip, checkmark        | “Objective updated.”       |
| Opportunity | fading page edge / hourglass   | “Opportunity fading.”      |

---

## 12. UI Composite Layer

### 12.1 Problem with Sequential Queues

A sequential popup queue will hurt pacing.

Example:

```text
Inspiration gained.
Suspicion increased.
Objective updated.
Assignment ready.
```

If these fire one after another, the player gets trapped watching UI animations instead of reading the scene.

---

### 12.2 Revised Solution

Use a **composite notification bundle**.

All stat changes caused by a single script beat are aggregated into one display event.

Example display:

```text
New Material Gained
A scene forms in Cora’s mind.

Vance noticed something.

Objective Updated:
Gather material for the first manuscript.
```

One screen. One animation. One duration.

---

### 12.3 Notification Bundle Model

```renpy
default pending_notification_bundle = None
```

Bundle shape:

```renpy
{
    "level": "standard",
    "items": [
        {
            "type": "inspiration",
            "title": "New Material Gained",
            "body": "A scene forms in Cora’s mind.",
            "icon": "quill",
        },
        {
            "type": "suspicion",
            "title": "Vance noticed something.",
            "body": "",
            "icon": "eye",
        },
        {
            "type": "objective",
            "title": "Objective Updated",
            "body": "Gather material for the first manuscript.",
            "icon": "journal",
        }
    ]
}
```

If any item crosses a breakpoint:

```renpy
"level": "breakpoint"
```

The composite screen then uses the strongest required presentation.

---

### 12.4 Notification Theme

```renpy
define notification_theme = {
    "suspicion": {
        "color": "#8b0000",
        "icon": "eye_icon"
    },
    "corruption": {
        "color": "#4b0082",
        "icon": "ink_bleed"
    },
    "inspiration": {
        "color": "#d2b48c",
        "icon": "quill_icon"
    },
    "objective": {
        "color": "#c0a060",
        "icon": "journal_icon"
    },
    "opportunity": {
        "color": "#8f7a5a",
        "icon": "hourglass_icon"
    }
}
```

---

### 12.5 Script Integration Pattern

Use a transaction-style wrapper around major beats.

Example:

```renpy
$ begin_notification_bundle()

$ add_material("mat_locked_room_glimpse")
$ add_stat_delta("suspicion", 1, character="vance", source="locked_room_glimpse")
$ activate_objective("obj_assignment_01_material")

$ flush_notification_bundle()
```

This prevents popup spam while keeping logic centralised.

---

## 13. HUD Behavior

### 13.1 Main HUD Should Show

The main HUD should show:

* manuscript readiness
* current material progress
* active opportunity warning if relevant
* immediate risk character
* journal updated marker

Example:

```text
Manuscript: Baseline Ready
Scandalous Draft Locked
Risk: Ms. Stern Watchful
Focus: 2 remaining
```

Do not permanently show all raw stats.

---

### 13.2 HUD Auto-Hide

Do not manually write `hide screen hud` everywhere.

Use a central control variable:

```renpy
default hud_enabled = True
default cinema_mode = False
```

HUD screen:

```renpy
screen narrative_hud():
    if hud_enabled and not cinema_mode and not renpy.get_screen("choice"):
        # show HUD
        pass
```

Alternatively, register the HUD as an overlay screen and control visibility centrally:

```renpy
init python:
    config.overlay_screens.append("narrative_hud")
```

This keeps script files clean.

---

## 14. Writing Assignment Data Model

```renpy
default writing_assignments = {
    "assignment_01": {
        "title": "The House Behind the Velvet Door",
        "chapter_id": "chapter_01",
        "status": "active",

        "required_material": 5,

        "variants": {
            "respectable": {
                "required_material": 5,
                "min_material_tier": 1,
                "required_tags": [],
                "required_corruption": 0,
                "required_blackmail_material": 0,
            },

            "scandalous": {
                "required_material": 5,
                "min_material_tier": 2,
                "required_tags": ["scandal"],
                "required_corruption": 2,
                "required_blackmail_material": 0,
            },

            "blackmail": {
                "required_material": 5,
                "min_material_tier": 3,
                "required_tags": ["evidence"],
                "required_corruption": 2,
                "required_blackmail_material": 1,
            }
        },

        "completion_label": "write_assignment_01",
    }
}
```

---

## 15. Core Functions

### 15.1 Add Material

```renpy
init python:

    def add_material(material_id):
        material = material_library[material_id].copy()
        manuscript_material.append(material)

        add_bundle_item({
            "type": "inspiration",
            "title": "New Material Gained",
            "body": material.get("journal_text", "Cora has found something worth writing."),
            "icon": "quill",
        })

        check_assignment_readiness()
```

---

### 15.2 Spend Focus

```renpy
init python:

    def spend_focus(amount):
        global chapter_focus_remaining
        chapter_focus_remaining = max(0, chapter_focus_remaining - amount)
        check_expiring_opportunities()
```

---

### 15.3 Check Assignment Readiness

```renpy
init python:

    def check_assignment_readiness():
        assignment = writing_assignments[current_assignment_id]

        if assignment["status"] != "active":
            return

        usable_value = get_usable_material_value(current_assignment_id)

        if usable_value >= assignment["required_material"]:
            assignment["status"] = "ready"
            add_bundle_item({
                "type": "inspiration",
                "title": "Manuscript Ready",
                "body": "Cora has enough material for a baseline draft.",
                "icon": "quill",
            })

        update_available_variants(current_assignment_id)
```

---

### 15.4 Update Available Variants

```renpy
init python:

    def update_available_variants(assignment_id):
        assignment = writing_assignments[assignment_id]

        for variant_id, reqs in assignment["variants"].items():
            if variant_requirements_met(assignment_id, reqs):
                unlock_assignment_variant(assignment_id, variant_id)
```

---

### 15.5 Complete Assignment

```renpy
init python:

    def complete_assignment(assignment_id, selected_variant):
        assignment = writing_assignments[assignment_id]

        consumed = consume_material_for_assignment(
            assignment_id,
            assignment["required_material"],
            selected_variant
        )

        overflow = get_unconsumed_usable_material_value(assignment_id)

        if overflow > 0:
            add_draft_quality(assignment_id, overflow * 10)

        apply_variant_flag(assignment_id, selected_variant)

        assignment["status"] = "complete"

        expire_assignment_locked_material(assignment_id)

        add_bundle_item({
            "type": "objective",
            "title": "Manuscript Complete",
            "body": assignment["title"],
            "icon": "journal",
        })
```

---

## 16. Scene Integration Example

```renpy
label locked_room_glimpse:

    $ begin_notification_bundle()

    $ spend_focus(2)

    $ add_material("mat_locked_room_glimpse")

    $ persistent_flags["witnessed_locked_room_scene"] = True

    $ add_stat_delta(
        "suspicion",
        1,
        character="vance",
        source="locked_room_glimpse"
    )

    $ activate_objective("obj_assignment_01_material")

    $ flush_notification_bundle()

    return
```

Player sees one composite cue:

```text
New Material Gained
A scene forms in Cora’s mind.

Vance noticed something.

Objective Updated:
Gather material for the first manuscript.
```

Not four separate popups. Good.

---

## 17. MVP Implementation Phases

### Phase 1: Data Layer

Create:
- `game/shared/narrative_pressure_data.rpy` (Non-Prod)
- `game/narrative_pressure_data.rpy` (Prod)

Include:
- suspicion dictionary
- corruption value
- material library
- manuscript material list
- objective dictionary
- writing assignment dictionary
- chapter focus state
- character context state
- draft quality dictionary

### Phase 2: Core Logic

Create:
- `game/shared/narrative_pressure_system.rpy` (Non-Prod)
- `game/narrative_pressure_system.rpy` (Prod)

Include:
- `add_material`
- `spend_focus`
- `add_stat_delta`
- `check_assignment_readiness`
- `update_available_variants`
- `complete_assignment`
- `expire_chapter_material`
- `activate_objective`
- `complete_objective`
- `fail_objective`
- `expire_objective`
- `set_scene_context`
- `get_hud_risk_character`

### Phase 3: Composite Notification Layer

Create:
- `game/shared/narrative_notification_screen.rpy` (Non-Prod)
- `game/narrative_notification_screen.rpy` (Prod)

Include:
- notification bundle storage
- composite display screen
- standard cue presentation
- breakpoint cue presentation
- theme dictionary

MVP supports only:
- Standard Delta
- Breakpoint Crossed

No twelve-state animation monster.

### Phase 4: Journal Screen

Create:
- `game/shared/journal_screen.rpy` (Non-Prod)
- `game/journal_screen.rpy` (Prod)

Include:
- current manuscript
- material progress
- available drafts
- locked drafts
- active objectives
- optional opportunities
- risks
- completed objectives
- expired/gone-cold notes if needed

### Phase 5: HUD Screen

Create:
- `game/shared/hud_screen.rpy` (Non-Prod)
- `game/hud_screen.rpy` (Prod)

Include:
- manuscript readiness
- variant lock summary
- focus remaining
- immediate risk character
- journal update indicator

HUD visibility should be controlled centrally.

---

## 18. Acceptance Criteria

### 18.1 Inspiration and Material

Passes when:
* Inspiration is tracked as material entries, not only a flat number.
* Material has tier, tags, chapter, assignment, and expiry metadata.
* Safe material can complete baseline drafts.
* High-tier variants require specific material, not just total value.
* Assignment completion does not silently waste excess material.
* Overflow converts into Draft Quality or visible notes.
* Chapter-end decay prevents hoarding across chapters.

### 18.2 Focus and Opportunity

Passes when:
* Chapters can define finite focus slots.
* Actions can consume focus.
* Optional objectives can expire based on focus, flags, or chapter state.
* Safe choices can lock out dangerous opportunities through opportunity cost.
* The player can see when an opportunity is fading.

### 18.3 Suspicion

Passes when:
* Suspicion is character-specific.
* Suspicion increases only from concrete risky actions.
* HUD risk display considers scene context.
* High offscreen suspicion does not override immediate present danger unless at a major global breakpoint.
* Suspicion breakpoint events can trigger stronger cue presentation.

### 18.4 Notifications

Passes when:
* Multiple changes from the same beat appear in one composite notification.
* The system does not force sequential popup delays.
* MVP supports only standard and breakpoint cue levels.
* Cues remain visually distinct by type.

### 18.5 Journal

Passes when:
* The journal clearly shows manuscript readiness.
* The journal distinguishes baseline, scandalous, and blackmail draft requirements.
* Optional opportunities show reward, cost, risk, and expiry.
* Completed objectives remain reviewable.
* Expired opportunities are marked clearly rather than disappearing silently.

### 18.6 HUD

Passes when:
* Raw stats are not the main presentation.
* HUD shows manuscript state first.
* HUD shows immediate relevant risk, not global highest risk by default.
* HUD can hide automatically during cinematic scenes, menus, or special presentation moments.
* HUD is controlled centrally rather than manually hidden in every script file.

---

## 19. Final Design Position

This system should make the player feel like they are constantly choosing between:
```text
safe but thin material
dangerous but powerful material
moral compromise
lost opportunity
immediate suspicion
future leverage
```

The key guardrail is not punishment. It is exclusion.

A safe path gives Cora enough to write something acceptable.
A dangerous path gives her the material to write something that can wound, expose, or transform her future.

That is the real pressure engine.
