# LLM PROMPT CATALOGUE: SAVOY HOTEL ADV LAYER

This catalogue contains flag-agnostic prompt templates for creating, rewriting, and revising (tuning length/spiciness of) dialogue and staging scripts for the real-life (IRL) Savoy Hotel ADV gameplay layer.

To ensure these prompts remain robust as variables or balance traits evolve over time, **all flag names and narrative wiring are decoupled from the prompt text**. The prompts direct the LLM to actively lookup current flag metadata from the companion export files:
- [system_prompt.md](file:///c:/Users/mikez/OneDrive/Documents/gh/git/untitled-victorian-vn/docs/normal-day-prose-export/system_prompt.md)
- [style_and_voice_guide.md](file:///c:/Users/mikez/OneDrive/Documents/gh/git/untitled-victorian-vn/docs/normal-day-prose-export/style_and_voice_guide.md)
- [variables_and_flag_wiring.md](file:///c:/Users/mikez/OneDrive/Documents/gh/git/untitled-victorian-vn/docs/normal-day-prose-export/variables_and_flag_wiring.md)

---

## 1. Prompt Template: Create New Content (New Day/Label)

Use this template when generating a new ADV script block for the Savoy Hotel.

```markdown
# TASK: Generate New Savoy ADV Dialogue & Staging Label

You are the Prose Generation Engine for the Savoy Hotel IRL layer. Generate a brand-new Ren'Py label script representing a scene shift.

## 1. Target Scene Profile
- **Target Label Name:** [INSERT LABEL NAME, e.g., day101_2_missy_meets_cora]
- **Target Day:** [INSERT DAY, e.g., Day 101]
- **Initial Background:** [INSERT BACKGROUND, e.g., bg_laundry_room_day]
- **Cast List:** [INSERT CAST LIST, e.g., Cora Hartley, Missy]
- **Scene Narrative Goal:** [INSERT NARRATIVE GOAL, e.g., Missy meets Cora in the laundry room and explains the wash-house routine.]

## 2. Dynamic Reference Lookup (Flag-Agnostic Rules)
1. **Identify Story Flags:** Look up the active variables and decision hooks for [TARGET DAY] in `variables_and_flag_wiring.md`.
2. **Retrieve Branch Values:** Read the valid values and micro-variant descriptions for those variables from the manual.
3. **Build branching menu:** Include an interactive choice (`menu:`) block. Ensure the choice outcomes execute the correct state calls (e.g., `$ apply_balanced_effect(...)` and `$ story.set_variable(...)`) mapped to the choices in the manual.
4. **Style Compliance:** Adhere to the language gap (Cora's performed Wiltshire dialogue vs. private Cork Irish monologue), class tension, and staging guidelines defined in `style_and_voice_guide.md`.

## 3. Formatting & Ren'Py ADV Rules
- **Dialogue Lines:** Use character labels (`cora "..."`, `missy "..."`, `cora_inner "..."` for monologue).
- **Sprite Staging:** Inline visual staging commands (`scene`, `show`, `hide`, and position tags like `left_full_body`, `right_full_body` with transitions like `with dissolve`).
- **Indentation:** Exactly 4 spaces for statements under labels/menus, and 8 spaces under menu options.
- **Linter Safety:** Avoid forbidden words (`okay`, `hello`, `gaslight`, `stress`, `trauma`).
```

---

## 2. Prompt Template: Rewrite Existing Content

Use this template to rewrite an existing ADV label to improve tone, formatting, or styling while keeping the code logic intact.

```markdown
# TASK: Rewrite Existing Ren'Py ADV Script (Staging Preservation)

You are the Prose Generation Engine. Rewrite the provided Ren'Py ADV script segment to improve its prose fidelity and stylistic tone without altering the code structure.

## 1. Target Prose Rules
- **Sentence Architecture:** Snappy, action-forward pacing. Avoid wordy, meandering descriptions.
- **The Dialogue Gap:** Ensure Cora's spoken lines remain short, formal, and contraction-free (Wiltshire maid persona) while her internal monologue (`cora_inner`) contains her sharp, cynical Cork Irish observations.
- **Forbidden Words:** Replace any modern terms (such as `okay`, `hello`, `gaslight`, `stress`, or `trauma`) with period-accurate language.

## 2. Staging and Logic Code Preservation (CRITICAL)
- **Do NOT alter or delete any staging statements:** Keep all `scene`, `show`, `hide`, positions, and transition commands exactly as written.
- **Do NOT alter logic code:** Keep all python calls (e.g. `$ apply_balanced_effect(...)`, `$ story.set_variable(...)`), branching headers, labels, and choice outcomes identical in structure. Only rewrite the text inside dialogue strings (`"..."`).

## 3. Source Script to Rewrite
```renpy
[PASTE SOURCE RENPY CODE HERE]
```
```

---

## 3. Prompt Template: Revise Existing Content (Tuning Pacing & Spice)

Use this template to adjust the length (pacing) or the "spice level" (intimacy/tension) of a script segment.

```markdown
# TASK: Tune Prose Pacing and Intimacy Level of Ren'Py Script

You are the Prose Generation Engine. Revise the provided Ren'Py ADV dialogue block to meet the specific pacing and intensity targets below.

## 1. Revision Targets
- **Prose Length Target:** [CHOOSE: "Shorter/Snappier" OR "Longer/More Sensory Details"]
  - *Shorter/Snappier:* Trim sentences. Focus purely on immediate actions, quick eye locks, and rapid-fire dialogue to accelerate the scene's pacing.
  - *Longer:* Add historical texture. Describe the physical environment (coal dust, candle grease, starched fabric, lavender water) and internal class dynamics.
- **Intimacy / Spice Target:** [CHOOSE: "Less Spicy (Respectable/Subdued)" OR "Spicier (Intimate/Transgressive)"]
  - *Less Spicy:* Keep interactions strictly formal and distant. Focus on the cold machinery of domestic labor. Cora remains submissive, fearful, or purely observant.
  - *Spicier:* Amplify tactile details, physical proximity, breath, pulse, and the tension of domination and submission (e.g., the red marks on a collarbone, the unlacing of stays, the shiver of skin against rough aprons).

## 2. Code & Logic Preservation
- Keep all Ren'Py script syntax intact (labels, menus, transitions, sprite calls, and `$ ...` Python state statements must not be removed or structurally altered). Only modify the strings within the dialogue and description fields.

## 3. Source Script to Revise
```renpy
[PASTE SOURCE RENPY CODE HERE]
```
```
