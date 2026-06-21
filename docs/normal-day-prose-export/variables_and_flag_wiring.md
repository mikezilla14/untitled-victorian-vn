# VARIABLES & FLAG WIRING MANUAL: SAVOY HOTEL IRL LAYER

This manual lists the variables, stats, and Python state tracking hooks used to track choices and balance profiles in the Savoy Hotel ADV gameplay layer.

---

## 1. Savoy Hotel Story State Flags (`story`)

These variables track specific choices and relationships built during the day:

| Variable Name | Valid Values | Narrative Context |
|---|---|---|
| `story.day1_corridor_state` | `"none"`, `"ghost"`, `"predator"`, `"prey"` | Tracks Cora's dominant posture during the conservatory tryst. |
| `story.day1_interview_state` | `"none"`, `"meek"`, `"competent"` | Choice in Miss Stern's morning interview. |
| `story.day1_stern_relation` | `"none"`, `"subservient"`, `"resistant"`, `"complicit"` | Relation to Miss Stern after her invasive touch. |
| `story.day1_stern_secret_bound` | `"none"`, `"fearful"`, `"loyal"`, `"exploitative"` | Response to Stern's warning about guest secrets. |
| `story.day1_vance_relation` | `"none"`, `"subservient"`, `"defiant"`, `"ghostly"`, `"protected"`, `"intimate"`, `"observed"`, `"loyal_witness"`, `"accomplice"`, `"silent_observer"` | Relationship to Miss Vance across dressing room/stairwell. |
| `story.missy_day1_trust_state` | `"none"`, `"soothed"`, `"unsettled"`, `"warned_cora"`, `"shared_caution"` | Missy/Miri's trust state during laundry/corridor shifts. |
| `story.day1_ledger_focus` | `"none"`, `"inspiration"`, `"corruption"` | Focus of Cora's manuscript writing at the end of Day 1. |
| `story.day1_night_action` | `"none"`, `"write"`, `"visit_missy"` | Cora's choice of twilight activity. |

---

## 2. Player Stats (`player`)

These metrics change dynamically and are referenced by the routing logic:

* **`player.corruption_level`** (integer): Tracks Cora's moral compromises. High corruption (>2) unlocks alternate transgressive chapters.
* **`player.inspiration`** (integer, 0 to 50): Tracks literary material.
* **`player.anxiety`** (integer, 0 to 100): Tracks internal panic.
* **`player.ghost_focus`, `player.prey_focus`, `player.predator_focus`** (integers): Tracks Cora's dialogue choices and posture bias.

---

## 3. Python Staging & Balancing Hooks

In choices, you must call these exact Python functions to record effects:

1. **`apply_balanced_effect(trait, intensity="standard", witness=None)`**
   - Updates the player's semantic balance profile.
   - *Valid Traits:* `"submissive"`, `"defiant"`, `"obedient"`, `"transgressive"`, `"observant"`, `"self_protective"`, `"reckless"`.
   - *Example:* `$ apply_balanced_effect("submissive", intensity="standard")`
2. **`apply_archetype_edge(archetype, amount=1)`**
   - Increments the player's focus statistic for a specific narrative voice archetype.
   - *Valid Archetypes:* `"ghost"`, `"prey"`, `"predator"`.
   - *Example:* `$ apply_archetype_edge("prey", 1)`
3. **`story.set_variable_name(value)`**
   - Sets a story state flag.
   - *Example:* `$ story.set_day1_interview_state("meek")`
