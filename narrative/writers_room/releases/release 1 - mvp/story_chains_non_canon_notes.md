# Technical Documentation: Character-Specific Suspicion & Story Chains

This document details the architectural additions implemented in the Release 1 sandbox (`narrative/writers_room/releases/release 1 - mvp/`) to support the new character-specific story chains and confrontations. These mockups are designed to be 100% backwards-compatible with existing scripts, while laying the technical foundation for Release 2's granular choice design.

---

## 1. Character-Specific Suspicion Architecture

In `classes_non_canon.rpy`, the `PlayerStats` class has been extended to support individual suspicion pools for core characters (Stern, Vance, and Missy) alongside the global general suspicion.

### Backing State Variables
Inside `PlayerStats.__init__`, the following state attributes have been defined:
- `self.stern_suspicion = 0` (integer, ranges `[0, 100]`)
- `self.vance_suspicion = 0` (integer, ranges `[0, 100]`)
- `self.missy_suspicion = 0` (integer, ranges `[0, 100]`)
- `self.base_suspicion = 0` (integer, backing variable for general/non-specific suspicion changes)

### Recalculation and Clamping in `update_stats()`
All attributes are validated, clamped, and consolidated inside `PlayerStats.update_stats()` to ensure integrity:
1. **Character Suspicion Clamping**:
   Individual character suspicions are clamped between `0` and `100`:
   ```python
   self.stern_suspicion = max(0, min(100, self.stern_suspicion))
   self.vance_suspicion = max(0, min(100, self.vance_suspicion))
   self.missy_suspicion = max(0, min(100, self.missy_suspicion))
   ```
2. **Derived Global Suspicion (Anxiety Score)**:
   Global `self.suspicion` is calculated dynamically as the sum of all character suspicions plus the base general suspicion, capped between `0` and `100`:
   ```python
   self.suspicion = max(0, min(100, self.base_suspicion + self.stern_suspicion + self.vance_suspicion + self.missy_suspicion))
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
  To maintain backward-compatibility with Day 1–4 legacy scripts, general suspicion calls are routed through `self.base_suspicion` rather than directly modifying `self.suspicion`. This ensures that global stat increases propagate correctly to the final consolidated score via `update_stats()`.

---

## 2. Updated Effect Application Utility

The global `apply_effects` utility in `functions_non_canon.rpy` has been updated with an expanded signature to seamlessly route character-specific changes.

### Function Signature
```python
def apply_effects(insp=0, corr=0, susp=0, stern_susp=0, vance_susp=0, missy_susp=0):
```

### Routing Logic
Within `apply_effects`, keyword arguments are validated and routed directly to the appropriate `PlayerStats` method:
```python
# Character-specific suspicions:
if stern_susp != 0:
    player.adjust_character_suspicion("stern", stern_susp)
if vance_susp != 0:
    player.adjust_character_suspicion("vance", vance_susp)
if missy_susp != 0:
    player.adjust_character_suspicion("missy", missy_susp)
```
At the end of effect application, `player.update_stats()` is called to compile the state modifications and ensure the global `suspicion` is accurately calculated.

---

## 3. Technical Contracts & Design Guidelines for Promotion

When promoting these features from the non-production mockup files to production:

> [!IMPORTANT]
> **Strict Sandboxing**:
> Ensure that all production edits are only performed during an official promotion cycle. Do not edit `renpy_project/game/classes.rpy` or `renpy_project/game/functions.rpy` outside a designated merge window.

### Canonical Integration Steps
1. **Promote Classes**: 
   Port the attributes, clamping logic, and `adjust_character_suspicion` method from `classes_non_canon.rpy` into `renpy_project/game/classes.rpy`.
2. **Promote Functions**:
   Port the updated `apply_effects` keyword arguments and character routing block into `renpy_project/game/functions.rpy`.
3. **Verify State Consistency**:
   Verify that any persistent save file schemas or serialization scripts accommodate the new variables (`stern_suspicion`, `vance_suspicion`, `missy_suspicion`, `base_suspicion`).

### Writing Guidelines for Release 2
- **Character-Specific suspicion increases**: Use `apply_effects(stern_susp=10)` when a character is directly alienated or made suspicious.
- **Global suspicion / anxiety increases**: Use `apply_effects(susp=10)` when Cora makes general mistakes or displays suspicious behavior not specific to one observer.
