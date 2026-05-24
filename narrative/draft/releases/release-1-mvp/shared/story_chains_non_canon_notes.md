# Technical Documentation: Character-Specific Suspicion & Story Chains

This document details the architectural additions implemented in the Release 1 sandbox (`narrative/draft/releases/release-1-mvp/`) to support the new character-specific story chains and confrontations. These mockups are designed to be 100% backwards-compatible with existing scripts, while laying the technical foundation for Release 2's granular choice design.

---

## 1. Character-Specific Suspicion Architecture

In `classes_non_canon.rpy`, the `PlayerStats` class has been extended to support individual suspicion pools for core characters (Stern, Vance, and Missy) alongside the global general suspicion.

### Backing State Variables
Inside `PlayerStats.__init__`, the following state attributes have been defined:
- `self.stern_suspicion = 0` (integer, ranges `[0, 100]`)
- `self.vance_suspicion = 0` (integer, ranges `[0, 100]`)
- `self.missy_suspicion = 0` (integer, ranges `[0, 100]`)
- `self.anxiety = 0` (integer, consolidated score)
- `self.tracked_characters = ["stern", "vance", "missy"]` (list of active tracked characters)

### Recalculation and Clamping in `update_stats()`
All attributes are validated, clamped, and consolidated inside `PlayerStats.recalculate_anxiety()` (which is called by `update_stats()`):
1. **Character Suspicion Clamping**:
   Individual character suspicions are clamped between `0` and `100`:
   ```python
   self.stern_suspicion = max(0, min(100, self.stern_suspicion))
   self.vance_suspicion = max(0, min(100, self.vance_suspicion))
   self.missy_suspicion = max(0, min(100, self.missy_suspicion))
   ```
2. **Derived Consolidated Anxiety Score**:
   Global `self.anxiety` is calculated dynamically as:
   $$\text{self.anxiety} = \lfloor \frac{\text{total\_susp}}{N} \rfloor$$
   Where $N$ is the number of active tracked characters in `self.tracked_characters`, and `total_susp` is the sum of character suspicions.
   ```python
   import math
   total_susp = 0
   for char in self.tracked_characters:
       total_susp += getattr(self, "{}_suspicion".format(char), 0)

   n = len(self.tracked_characters)
   if n > 0:
       self.anxiety = int(math.floor(float(total_susp) / n))
   else:
       self.anxiety = 0
   ```

### State Modification Methods
- `adjust_character_suspicion(character, amount)`: A routing helper that increments or decrements character-specific suspicions.
  ```python
  def adjust_character_suspicion(self, character, amount):
      if character == "stern":
          self.stern_suspicion += amount
      elif character == "vance":
          self.vance_suspicion += amount
      elif character == "missy":
          self.missy_suspicion += amount
  ```
- `raise_suspicion(amount)` and `lower_suspicion(amount)`:
  Legacy general suspicion methods are completely deprecated and raise `NotImplementedError` if invoked.

---

## 2. Updated Effect Application Utility

The global `apply_effects` utility in `functions_non_canon.rpy` has been updated with an expanded signature to route character-specific changes and raise a `ValueError` for legacy general `susp` calls.

### Function Signature
```python
def apply_effects(insp=0, corr=0, susp=0, stern_susp=0, vance_susp=0, missy_susp=0):
```

### Routing Logic
Within `apply_effects`, keyword arguments are validated and routed directly to the appropriate `PlayerStats` method. If legacy general `susp` is called with a non-zero value, it raises a `ValueError`:
```python
# Legacy susp deprecation:
if susp != 0:
    raise ValueError("Legacy general 'susp' is deprecated. Suspicion must target a specific witness (stern_susp, vance_susp, missy_susp).")

# Character-specific suspicions:
if stern_susp != 0:
    player.adjust_character_suspicion("stern", stern_susp)
if vance_susp != 0:
    player.adjust_character_suspicion("vance", vance_susp)
if missy_susp != 0:
    player.adjust_character_suspicion("missy", missy_susp)
```
At the end of effect application, `player.update_stats()` is called to compile the state modifications and recalculate global `anxiety`.

---

## 3. Technical Contracts & Design Guidelines for Promotion

When promoting these features from the non-production mockup files to production:

> [!IMPORTANT]
> **Strict Sandboxing**:
> Ensure that all production edits are only performed during an official promotion cycle. Do not edit `renpy_project/game/classes.rpy` or `renpy_project/game/functions.rpy` outside a designated merge window.

### Canonical Integration Steps
1. **Promote Classes**: 
   Port the attributes, dynamic anxiety math, and `adjust_character_suspicion` method from `classes_non_canon.rpy` into `renpy_project/game/classes.rpy`.
2. **Promote Functions**:
   Port the updated `apply_effects` keyword arguments and character routing block (including the ValueError check for susp != 0) into `renpy_project/game/functions.rpy`.
3. **Verify State Consistency**:
   Verify that any persistent save file schemas or serialization scripts accommodate the new variables (`stern_suspicion`, `vance_suspicion`, `missy_suspicion`, `anxiety`).

### Writing Guidelines for Release 2
- **Character-Specific suspicion increases**: Use `apply_effects(stern_susp=10)` when a character is directly alienated or made suspicious.
- **Global suspicion / anxiety increases**: Legacy general `apply_effects(susp=10)` is strictly forbidden and throws a runtime exception. All suspicion must be attributed to a specific observer context.
