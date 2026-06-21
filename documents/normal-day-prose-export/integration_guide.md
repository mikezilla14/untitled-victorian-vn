# INTEGRATION & SYNTAX VALIDATION GUIDE: SAVOY HOTEL IRL LAYER

This guide outlines the procedure for importing and validating external LLM-generated Savoy ADV dialogue scripts back into the project codebase.

---

## 1. Code Placement & Formatting

1. **Target File:** Real-life hotel scripts reside in:
   - `main-game/non-prod-game/game/days/dayXXX_non_canon.rpy`
2. **Indentation Standards:** Ren'Py has strict indentation requirements.
   - **Label Level:** `label dayXXX_label_name:` is flush left (0 spaces).
   - **Block Level:** All statements inside a label must be indented exactly **4 spaces**.
   - **Condition / Menu Options Level:** Blocks under `if`, `else`, or menu choice options must be indented exactly **8 spaces**.
   - *Do NOT mix tabs and spaces. Use exactly 4 spaces per indentation level.*
3. **DAG Nodes:** Maintain the DAG comments at the top of each block to preserve structural testing hooks:
   - `# [DAG_NODE id=day101_1_morning_interview type=work day=101]`

---

## 2. Sprite Staging Integrity

To prevent visual glitches at runtime, ensure all sprite calls follow these guidelines:
- **Consistent Entrances/Exits:** Always use `show sprite_name expression at position` before a character speaks, and `hide sprite_name` when they leave the screen.
- **Valid Positions:** Use standard Ren'Py position handles: `left`, `right`, `left_full_body`, `right_full_body`, `left_reframe`, `right_reframe`, `left_bust`, `right_bust`.
- **Transitions:** Combine sprite staging with transitions (e.g. `with dissolve`, `with move`) to keep the staging fluid.

---

## 3. Pre-Integration Verification Pipeline

After pasting the generated block into the target file, you must run the project validation suite to ensure it is structurally and historically sound.

1. **Verify Indentation & Ren'Py Syntax:**
   Run the contract validation and syntax linter:
   ```powershell
   python scripts/validate.py --profile changed --agent human --files "main-game/non-prod-game/game/days/day101_non_canon.rpy"
   ```
2. **Scan for Historical Anachronisms:**
   Ensure no blacklisted terms (e.g. `okay`, `hello`, `gaslight`, `stress`) slipped into the dialogue:
   ```powershell
   python scripts/historical_linter.py --file "main-game/non-prod-game/game/days/day101_non_canon.rpy"
   ```
3. **Check Staging & Asset References:**
   Ensure all referenced backgrounds and character sprite expressions exist in the asset manifest:
   ```powershell
   python scripts/check_assets.py
   ```
