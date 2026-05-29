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

## 2. Refined Writing Gate (`has_story_fuel`)

The story-writing progression was previously gated by a combined sum of Inspiration and Corruption XP exceeding a progressive threshold:
```python
# Old Sum-based Check
def has_story_fuel(self, required_total=15):
    return (self.inspiration + self.corruption_xp) >= required_total
```

This has been replaced by a modular, parameterized check accepting individual targets for both required inspiration and required corruption:
1. **Inspiration Check**: Cora must have available inspiration meeting or exceeding `required_insp` (defaults to `30`).
2. **Corruption Check**: Cora must have a corruption level meeting or exceeding `required_corr` (defaults to `30`).

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

## 5. Command-Query Separation: `consume_penance` decoupled from `get_post_penance_target`

Previously, `StoryState.get_post_penance_target` silently reset `penance_triggered` as a side effect inside a query method — a Command-Query Separation (CQS) violation. Any caller that read `penance_triggered` after calling the method would observe unexpected state.

`get_post_penance_target` is now a pure query with no side effects. A new explicit command method handles the reset:

```python
def consume_penance(self):
    """Command — clears penance_triggered. Always call explicitly after routing."""
    self.set_penance_triggered(False)
```

Callers (`advance_after_confrontation`, `end_slot d4_twilight_done`) now call `story.consume_penance()` explicitly after reading the routing target.

**Promotion note:** Apply the same split to `StoryState` in `renpy_project/game/classes.rpy`. Add `consume_penance` method and remove the `set_penance_triggered(False)` call from `get_post_penance_target`.
