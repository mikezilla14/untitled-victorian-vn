# LLM PROMPT CATALOGUE: BOOK WRITING ENGINE

This catalogue contains flag-agnostic prompt templates for generating every Day and Archetype variant combination of Cora Hartley's penny dreadful manuscript (`book1`).

To ensure these prompts remain robust as variables or balancing details evolve over time, **all flag names, values, and narrative wiring are decoupled from the prompt text**. The prompts direct the LLM to actively lookup current flag metadata from the companion export files:
- [system_prompt.md](file:///c:/Users/mikez/OneDrive/Documents/gh/git/untitled-victorian-vn/docs/book-writing-engine-export/system_prompt.md)
- [narrative_summary_and_flag_wiring.md](file:///c:/Users/mikez/OneDrive/Documents/gh/git/untitled-victorian-vn/docs/book-writing-engine-export/narrative_summary_and_flag_wiring.md)
- [style_and_voice_guide.md](file:///c:/Users/mikez/OneDrive/Documents/gh/git/untitled-victorian-vn/docs/book-writing-engine-export/style_and_voice_guide.md)
- [characters_and_locations.md](file:///c:/Users/mikez/OneDrive/Documents/gh/git/untitled-victorian-vn/docs/book-writing-engine-export/characters_and_locations.md)

---

## 1. Master Chapter Prompt Template

Copy and fill this template for any specific day and archetype generation.

```markdown
# TASK: Generate Branching Ren'Py Dialogue (Chapter Generator)

You are the Prose Generation Engine for the visual novel. Your task is to generate the branching label code for a specific manuscript chapter.

## 1. Target Execution Profile
- **Target Day:** [INSERT DAY, e.g., Day 101]
- **Target Archetype:** [INSERT ARCHETYPE, e.g., Prey]
- **Style Lenses:** [INSERT LENSES, e.g., Dracula / Jekyll & Hyde]
- **Target Label Name:** [INSERT LABEL NAME, e.g., book1_block_day1_alt_prey_core]

## 2. Mandatory Metadata Header
You must output this exact comment block at the very top of your script response:
```renpy
# =========================================================================
# METADATA: BOOK ENGINE IMPORT HEADER
# Target File: main-game/non-prod-game/game/days/[TARGET_FILE_NAME, e.g., book1_day101_non_canon.rpy]
# Target Label: [TARGET_LABEL_NAME]
# Target Chapter: [TARGET_CHAPTER_NAME, e.g., day1_chapter]
# Target Archetype: [TARGET_ARCHETYPE]
# Style Lens: [STYLE_LENSES]
# Generation Mode: multi_branch_code
# =========================================================================
```

## 3. Dynamic Reference Lookup (Flag-Agnostic Rules)
To write the branching logic, you must inspect the active context files:
1. **Locate Active Variables:** Look up the section for [TARGET DAY] in `narrative_summary_and_flag_wiring.md`. Identify all story flags, stats, and relations mapped to this day.
2. **Retrieve Branch Values:** Read the valid values and micro-variant descriptions for those variables from the manual.
3. **Build the Logic Branches:** Write conditional Ren'Py blocks (`if / elif / else`) evaluating every value of the mapped flags.
4. **Style Compliance:** Apply the stylistic rules, sentence structures, and character voices defined in `style_and_voice_guide.md` and `characters_and_locations.md` for this archetype and lenses.

## 4. Syntax & Formatting Rules
- **Method Call:** Display all story lines using the Ren'Py command:
  `call book1_nvl_write_line("Line text")`
- **Inner Thoughts:** Wrap Cora's metacomments in `cora_inner "..."` statement lines.
- **NVL Clear:** Group paragraphs into 3–4 lines, followed by the page clear command:
  `nvl clear`
- **Indentation:** Use exactly 4 spaces for statements under labels, and 8 spaces under conditional blocks. Do not output tab characters.
- **No Anachronisms:** Do not output forbidden terms such as `okay`, `hello`, `gaslight` (use `gas-lamp` or `gas-jet`), `stress`, or `trauma`.
```

---

## 2. Chapter Directory & Target Profiles

Use the target profiles below to populate the **Master Chapter Prompt Template**:

### Chapter I: The Inciting Lever (Day 101)
* **Prey Path:**
  - **Target Label:** `book1_block_day1_alt_prey_core`
  - **Lenses:** Dracula / Jekyll & Hyde / Carmilla
  - **Context Reference:** Look up Day 101 variables in `narrative_summary_and_flag_wiring.md` (Missy trust state, interview state, Stern relation, Vance relation, ledger focus).
* **Predator Path:**
  - **Target Label:** `book1_block_day1_alt_predator_core`
  - **Lenses:** Sweeney Todd / Dracula / Carmilla
  - **Context Reference:** Look up Day 101 variables.
* **Ghost Path:**
  - **Target Label:** `book1_block_day1_alt_ghost_core`
  - **Lenses:** Jack the Ripper / Jekyll & Hyde / Sweeney Todd
  - **Context Reference:** Look up Day 101 variables.

### Chapter II: The London Train (Day 102)
* **Prey Path:**
  - **Target Label:** `book1_block_day2_alt_prey_core`
  - **Lenses:** Dracula / Jekyll & Hyde
  - **Context Reference:** Look up Day 102 variables in `narrative_summary_and_flag_wiring.md` (tea choice, Missy trust break, suspicion state, contraband state).
* **Predator Path:**
  - **Target Label:** `book1_block_day2_alt_predator_core`
  - **Lenses:** Carmilla / Frankenstein
  - **Context Reference:** Look up Day 102 variables.
* **Ghost Path:**
  - **Target Label:** `book1_block_day2_alt_ghost_core`
  - **Lenses:** Jack the Ripper / Sweeney Todd
  - **Context Reference:** Look up Day 102 variables.

### Chapter III: The Savoy's Shadows (Day 103)
* **Prey Path:**
  - **Target Label:** `book1_block_day3_alt_prey_core`
  - **Lenses:** Dracula / Carmilla
  - **Context Reference:** Look up Day 103 variables in `narrative_summary_and_flag_wiring.md` (brush choice, Caldor ultimatum, twilight action).
* **Predator Path:**
  - **Target Label:** `book1_block_day3_alt_predator_core`
  - **Lenses:** Sweeney Todd / Jack the Ripper
  - **Context Reference:** Look up Day 103 variables.
* **Ghost Path:**
  - **Target Label:** `book1_block_day3_alt_ghost_core`
  - **Lenses:** Frankenstein / Jekyll & Hyde
  - **Context Reference:** Look up Day 103 variables.

### Chapter IV: The Fragile Lord (Day 104)
* **Prey Path:**
  - **Target Label:** `book1_block_day4_alt_prey_core`
  - **Lenses:** Dracula / Jekyll & Hyde
  - **Context Reference:** Look up Day 104 variables in `narrative_summary_and_flag_wiring.md` (Missy used as cover, possession of photograph).
* **Predator Path:**
  - **Target Label:** `book1_block_day4_alt_predator_core`
  - **Lenses:** Sweeney Todd / Frankenstein
  - **Context Reference:** Look up Day 104 variables.
* **Ghost Path:**
  - **Target Label:** `book1_block_day4_alt_ghost_core`
  - **Lenses:** Jack the Ripper / Carmilla
  - **Context Reference:** Look up Day 104 variables.

### Chapter V: A Mask Fixed Forever (Day 105)
* **Protege Path (Prey-Aligned):**
  - **Target Label:** `book1_block_day5_protege`
  - **Lenses:** Dracula / Jekyll & Hyde / Carmilla (The Shared Fall)
  - **Context Reference:** Look up Day 105 variables in `narrative_summary_and_flag_wiring.md` (final dynamic resolution).
* **Adversary Path (Predator-Aligned):**
  - **Target Label:** `book1_block_day5_adversary`
  - **Lenses:** Sweeney Todd / Jack the Ripper (Combatant Leverage)
  - **Context Reference:** Look up Day 105 variables.
* **Witness Path (Ghost-Aligned):**
  - **Target Label:** `book1_block_day5_witness`
  - **Lenses:** Frankenstein / Jack the Ripper (Silent Observation)
  - **Context Reference:** Look up Day 105 variables.
* **Muse / Default Path:**
  - **Target Label:** `book1_block_day5_muse`
  - **Lenses:** Frankenstein / Sweeney Todd (Systemic Diagnosis)
  - **Context Reference:** Look up Day 105 variables.
