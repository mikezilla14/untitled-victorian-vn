# Contract: Book Writing Engine (Inline Prose Macros & Holywell Street Style)

This contract defines the syntax and creative workflow for writing `book1` NVL chapter prose in the non-canon draft.

---

## 1. Inline Prose Macro Syntax Reference

The writing engine uses a custom micro-DSL enclosed in curly braces `{ ... }` to specify conditional variations in line-level text.

### Syntax Rules
* **Format**: `{ "[literal text]" [condition]; "[another literal]" if [condition2]; "[fallback text]" default; }`
* **Options Separation**: Options must be separated by semicolons `;`.
* **String Literals**: Quoted in double quotes `"..."`.
* **Variable References**: Unquoted identifiers (resolved against globals or common fragments).
* **Evaluation Order**: Deterministic "first match wins" (evaluated top-to-bottom, stopping at the first positive condition or falling back to `default`).

### Examples of Supported Expressions
* **Boolean check**: `{ "Cora was nervous." if missy_day2_trust_break; "Cora was calm." default; }`
* **Boolean equality comparison**: `{ "Cora was nervous." if missy_day2_trust_break == True; }`
* **String equality comparison**: `{ "She hid the contraband." if day2_contraband_state == "stolen_wearing"; }`
* **String inequality comparison**: `{ "She was not a guest." if day1_corridor_state != "ghost"; }`
* **Numeric comparison**: `{ "Her obsession was high." if obsession >= 60; }`
* **Compound condition (`and` / `or`)**: `{ "The master was furious." if day3_ultimatum == "defied" and player.corruption_level >= 30; }`

---

## 2. Creative Workflow: Holywell Street Penny Dreadful

When the book writing engine is called for new chapters (e.g., Day 2's chapters) or a rewrite is requested, the Writers' Room must execute the following creative workflow:

### A. The Holywell Street Aesthetic
Prose must be written against the expectations of a **melodramatic penny dreadful**, as sold by the publishers of ill repute on **Holywell Street**:
* **Tone**: Sensational, salacious, high-tension, and emotionally charged.
* **Transposition**: Cora's real-life (IRL) experiences at the Savoy Hotel (e.g., Stern, Vance, Gideon Locke, Miri) are transposed into the sensationalized book-world of **Ravenshade Conservatory**:
  * *Gideon Locke* -> *Lord Caldor* (predatory stillness, velvet voice, furnace-room terms).
  * *Lady Vance* -> *Lady Vayne* (lacquered poise, submissive fury, music-room door scandal).
  * *Miss Stern* -> *Mr. Sterick* (iron authority, public discipline, surveillance etiquette).
  * *Miri (Missy)* -> *Miri* (fragile readiness, courier, the conservatory ledger debt).
  * *Cora* -> *Coralie Vale* (the heroine, service as theater, private maps of power).

### B. Cooperative Flag-Driven Branching
1. **Flag Compilation**: Before writing begins, the **Non-Prod Code Agent** compiles a list of active gameplay flags/states up to that point in the story.
2. **Three-Variant Foundation**: The **Writers' Room** brainstorms and writes spec variants for the 3 main branches:
   * **Prey**: Intimate, exposed, danger and desire entangled.
   * **Predator**: Tactical, agentic, heat as leverage rather than surrender.
   * **Ghost**: Detached, observational, dispassionate moral accounting.
3. **Branching Catch-up**: Where the flags compiled by the code agent affect the narrative, the writers must write branching storylines in the curly-brace macro format for each possible state of the flag. This branching logic must capture all possible playthrough state paths until the book narrative catches up to the current point in Cora's IRL story.

---

## 3. NVL Pagination Contract
To maintain compatibility with the parchment layout, the NVL rendering system paginates every **3 lines** using `nvl clear` internally. Writers should structure paragraph lengths and macro branches with this pacing constraints in mind.

---

## 4. LLM Safety Guardrails & SFW Fallback Policy
If any requested prose or scene description runs a risk of triggering LLM safety filters for suggestive, intimate, or adult content:
* **No Suggestive Generation**: The writing agent must **not** attempt to generate highly suggestive, intimate, or explicit text.
* **SFW Narrative Summary**: Instead, write a clean, Safe for Work (SFW) narrative summary of what happens in the scene or option.
* **Human Hand-off Tag**: Clearly tag the summary block for human writing intervention using the exact tag: `[HUMAN WRITE: SFW summary of suggestive scene details]`. This prevents safety blocks and allows the pipeline to continue.
