# GAME MECHANICS BIBLE
**Project:** [Pending Title]  
**Version:** 1.1  
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

#### Suspicion
- Risk/fail-state meter.
- If threshold is reached, route to dismissal game over.

### 3) Writing gate mechanic
- Player must gather enough narrative resource (primarily Inspiration; with Corruption pressure) to progress chapter-writing beats.
- Writing scenes are the reward loop and progression unlock.

### 4) Choice architecture contract
- Choices must produce visible consequence through one or more of:
  - stat deltas,
  - branch text/state flags,
  - ending route pressure.
- Choices should not be cosmetic-only in critical beats.

### 5) Fail and ending structure
- Hard fail: Suspicion overflow -> `game_over_dismissed`.
- Soft fail: insufficient corruption trajectory by Day 5 -> `bad_ending_rejection`.
- Success path: Day 5 climax -> cliffhanger continuation.

---

## II. Implementation Contracts (Code-facing)

- Source of truth is class-backed state in `classes.rpy`.
- Runtime state instances are declared in `variables.rpy`.
- Day scripts mutate state through methods when available.
- Repeated mechanics should be consolidated in `functions.rpy` over time.

---

## III. Deferred Mechanics (Post-MVP, Not Enforced)

- Full pseudo-sandbox hub with click navigation screens.
- Agency alignment dials:
  - `Influence (Dominant/Predator)`
  - `Submission (Submissive/Prey)`
- Full paperdoll/layeredimage character assembly system.
- Advanced option-lock UI patterns (gray/lock states) beyond MVP baseline.

These may be reactivated once MVP shipping risk is reduced.
