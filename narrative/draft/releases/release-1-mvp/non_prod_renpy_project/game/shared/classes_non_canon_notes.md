# Technical Documentation: Refined Writing Gate Mechanics & Flat Inkwell Cap

This document details the architectural updates implemented in the Release 1 sandbox (`narrative/draft/releases/release-1-mvp/`) to support the refined writing gate mechanics, flat inspiration capacity, and separated resource validation. These changes have been implemented in `classes_non_canon.rpy` and `functions_non_canon.rpy` for review by the Chief Architect before promotion to production.

---

## 1. Flat Inspiration Capacity (The Inkwell)

In the previous design, the player's inspiration capacity scaled dynamically with their corruption level:
```python
# Old Dynamic Cap
self.inspiration_cap = 20 + (self.corruption_level * 10)
```

To simplify the in-game economy and align with the "inkwell" capacity lore:
- **Flat Cap**: Inspiration capacity is now hard-capped at **50**.
- **Enforcement**: In `PlayerStats.inspiration_cap`, we return a flat value of `50`. The clamping of `player.inspiration` between `0` and `50` is automatically enforced on every statistic update inside `update_stats()`:
  ```python
  self.inspiration = max(0, min(self.inspiration_cap, self.inspiration))
  ```

---

## 2. Writing Gate (`has_story_fuel`) — AND semantics

Writing gates use **AND**, not sum: both floors must clear.

```python
WRITE_GATE_CH1 = (15, 2)   # inspiration >= 15 AND corruption_level >= 2
WRITE_GATE_CH2 = (30, 3)   # inspiration >= 30 AND corruption_level >= 3
WRITE_GATE_CH3 = (45, 3)   # inspiration >= 45 AND corruption_level >= 3
WRITE_SLOP_MAX_CORRUPTION_LEVEL = 2  # Day 101 slop chapter when corruption_level <= 2
```

Call sites use `has_story_fuel(*WRITE_GATE_CH1)` etc. Day 101 menu write option uses the same CH1 gate.

### Upgraded Python Implementations
These gates are updated across the class definition and global wrappers to maintain absolute synchronization:

- **Inside `PlayerStats` (classes_non_canon.rpy)**:
  ```python
  def has_story_fuel(self, required_insp=30, required_corr=30):
      """
      Read-only writing-gate check.
      Returns True if:
      1. Inspiration available is >= required_insp (defaults to 30).
      2. Corruption level is >= required_corr (defaults to 30).
      """
      return self.inspiration >= required_insp and self.corruption_level >= required_corr
  ```

- **Inside global helper functions (functions_non_canon.rpy)**:
  ```python
  def has_story_fuel(required_insp=30, required_corr=30):
      """
      Read-only writing-gate check.
      Returns True if:
      1. Inspiration available is >= required_insp (defaults to 30).
      2. Corruption level is >= required_corr (defaults to 30).
      """
      return player.has_story_fuel(required_insp, required_corr)
  ```

---

## 3. Writing Execution Safety (`attempt_write`)

The actual writing gate in `functions_non_canon.rpy` has been updated to protect narrative choice actions. It now enforces both the required inspiration floor and the required corruption floor alongside dynamic cost spending:

```python
def attempt_write(required_insp=30, cost=20, required_corr=30):
    """
    Shared writing-gate helper.
    """
    if player.inspiration < required_insp or player.corruption_level < required_corr:
        return False
    return player.spend_inspiration(cost)
```

This guarantees that:
- Any script trying to call `attempt_write` directly will safely fail if Cora does not meet both custom or default thresholds.
- It remains fully backwards-compatible with existing day scripts (which pass legacy positional argument thresholds) and passes validation checks cleanly.

---

## 4. Confrontation Threshold Encapsulation (`PlayerStats.CONFRONTATION_THRESHOLD`)

Previously, the suspicion threshold that triggers a confrontation scene (50) was hardcoded directly in the `check_confrontations` label in `story_chains_non_canon.rpy`. This was a business-logic leak into episodic script.

The threshold is now a class constant on `PlayerStats`:

```python
CONFRONTATION_THRESHOLD = 50
```

And exposed via a delegation method:

```python
def is_confrontation_ready(self, char):
    """Returns True if char's total suspicion has reached the confrontation threshold."""
    return self.get_total_suspicion(char) >= self.CONFRONTATION_THRESHOLD
```

`check_confrontations` now calls `player.is_confrontation_ready("stern")` etc. If the design threshold ever changes, only the class constant needs updating.

**Promotion note:** Add `CONFRONTATION_THRESHOLD` constant and `is_confrontation_ready` method to `PlayerStats` in `renpy_project/game/classes.rpy`.

---

## 5. Deprecated compatibility: old penance bridge decoupled from route queries

Previously, `StoryState.get_post_penance_target` silently reset `penance_triggered` as a side effect inside a query method — a Command-Query Separation (CQS) violation. Any caller that read `penance_triggered` after calling the method would observe unexpected state.

`get_post_penance_target` is now a pure query with no side effects. The old explicit reset command remains only as a deprecated compatibility shim:

```python
def consume_penance(self):
    """DEPRECATED compatibility shim; migrated windows pop pending_penance directly."""
    self.set_penance_triggered(False)
    self.clear_penance()
```

Old compatibility callers may still call `story.consume_penance()` after reading the routing target. Migrated day files must not use this path; they consume queued labels with `story.pop_penance_for_window(...)`.

**Promotion note:** If old route-owner labels remain in production during migration, keep `consume_penance()` as a deprecated compatibility shim. Otherwise remove the old bridge and use the queued penance helpers below.

---

## 6. Time-period routing refactor: pending penance queue

`StoryState` now includes a non-canon `pending_penance` list for the time-period routing refactor in `docs/specs/story-chain-routing-refactor.md`.

Added helpers:

```python
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

`pending_penance` is now the active non-canon penance route. `check_confrontations` queues a concrete penance label such as `confrontation_stern`; named consequence windows consume that queue with `story.pop_penance_for_window(...)`, call the returned label, then return control to the day-owned time spine.

`penance_triggered` and `consume_penance()` remain only as deprecated compatibility infrastructure for old route-owner labels. The migrated non-canon day files now route penance through named consequence windows instead of the bridge.

**Promotion note:** When this refactor is promoted, add `pending_penance` and the queue helper methods to `StoryState` in `renpy_project/game/classes.rpy`. Prefer removing `penance_triggered` once production no longer needs old route-owner compatibility labels.
