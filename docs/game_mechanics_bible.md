# GAME MECHANICS BIBLE
**Project:** [Pending Title]  
**Version:** 1.2  
**Scope:** Player-facing mechanics and implementation contracts for MVP.

This document separates:
- **Active MVP mechanics (enforced now)**  
- **Deferred mechanics (post-MVP, not enforced)**

---

## I. Active MVP Mechanics (Enforced Now)

### 1) Runtime loop (current build)
- Structure is **day-based narrative flow** with menu choices (Day 1 -> Day 5).
- Time states are used (`Morning`, `Night`, `Late Night`) via `TimeManager`.
- Loop is not full hub/clickmap sandbox in MVP; player progression is branch-driven.

### 2) Core tracked resources

#### Inspiration
- Primary writing resource.
- Gained through observation/risk choices.
- Spent when writing chapters.

#### Corruption
- Implemented as `corruption_xp` and `corruption_level` in code.
- Represents boundary crossing intensity and unlock pressure.
- Gates late content/outcomes.

#### Anxiety (Consolidated Risk)
- Consolidated psychological risk computed modularly from character-specific suspicions using independent probability.
- **Two-Tiered Suspicion**: Each tracked character (Stern, Vance, Gideon, Missy) has a permanent **Base Suspicion** (representing established suspicion) and a temporary **Acute Suspicion** (representing active interactive heat).
- **Interactive vs. Milestone (Option B)**: The user's active choices directly adjust volatile **Acute Suspicion** (active heat they can influence), while programmatically calculated **Base Suspicion Deltas** are applied at key narrative milestones.
- **Sum-clamping & Squeezing**: The combined sum of base and acute suspicion for any character is capped strictly at `100`. Permanent base suspicion takes priority floor, dynamically squeezing acute suspicion down if base increases and the sum would exceed 100.
- **Anxiety Formula**: Global anxiety is calculated using independent probability (the probability of getting caught by at least one witness):
  $$\text{player.anxiety} = 100 \cdot (1 - \prod_{i} (1 - \frac{\text{Susp}_i}{100}))$$
  Where $\text{Susp}_i$ is the total suspicion (`base + acute`) for each active tracked character in `player.tracked_characters`.
- If Anxiety reaches 100, the narrative routes to the `game_over_dismissed` fail-state.

### 3) Writing gate mechanic
- Player must gather enough narrative resource (primarily Inspiration; with Corruption pressure) to progress chapter-writing beats.
- Writing scenes are the reward loop and progression unlock.

### 4) Choice architecture contract
- Choices must produce visible consequence through one or more of:
  - stat deltas,
  - branch text/state (see **State & stat management** below),
  - ending route pressure.
- Choices should not be cosmetic-only in critical beats.

#### State & stat management (authoritative in `classes.rpy`)
- **Class encapsulation:** Tracked state lives on `PlayerStats` and `StoryState` (and time on `TimeManager`); not as loose script globals.
- **Binary** outcomes: `bool` attributes and typed setters.
- **Mutually exclusive** outcomes: one `str` per fork with a default (e.g. `"none"`), a **fixed whitelist** in Python, and **only** designated setters in scripts to change it (e.g. `set_corridor_state`). Do not use several booleans for the same choice.
- **Validation:** String branch updates must be rejected at runtime if not whitelisted; game scripts use `story.set_*(...)` only, not direct `story.<field> =` for those fields. Reading is allowed in `if` / conditions.

### 5) Fail and ending structure
- Hard fail: Anxiety overflow (100) -> `game_over_dismissed`.
- Soft fail: insufficient corruption trajectory by Day 5 -> `bad_ending_rejection`.
- Success path: Day 5 climax -> cliffhanger continuation.

---

## II. Implementation Contracts (Code-facing)

- Source of truth is class-backed state in `classes.rpy`.
- Runtime state instances are declared in `variables.rpy`.
- Day scripts mutate `StoryState` and stats through setters and helpers that enforce contracts (booleans via `set_has_*` / equivalent; exclusive branches via whitelisted setters such as `set_corridor_state`).
- Repeated mechanics should be consolidated in `functions.rpy` over time.
- CI: `scripts/engineering_compliance.py` enforces parts of the above for touched files; pair with `renpy lint`.

---

## III. Deferred Mechanics (Post-MVP, Not Enforced)

- Full pseudo-sandbox hub with click navigation screens.
- Agency alignment dials:
  - `Influence (Dominant/Predator)`
  - `Submission (Submissive/Prey)`
- Full paperdoll/layeredimage character assembly system.
- Advanced option-lock UI patterns (gray/lock states) beyond MVP baseline.

These may be reactivated once MVP shipping risk is reduced.
