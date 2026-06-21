# STYLE & VOICE GUIDE: SAVOY HOTEL IRL NARRATIVE LAYER

This guide outlines the linguistic, stylistic, and technical rules that the external LLM must follow to produce prose matching the tone, staging, and syntax of Cora Hartley's Savoy Hotel ADV gameplay layer.

---

## 1. Style & Sentence Architecture

To capture the class-conscious, sharp, sensory realism of the Savoy Hotel, you must structure dialogue and descriptions using these parameters:

* **Realist and Concrete Pacing:** Avoid abstract romanticizing. Focus on the concrete details of the late-Victorian labor machine—the rattle of curate trays, the smell of carbolic soap, vinegar, vinegar washes, and laundry steam.
* **Sensory Contrast:** Contrast the heavy, lavish luxury of the guest suites (velvet cushions, mahogany panels, french powder, jasmine oils, lace wraps) with the cold, wet, cramped spaces of the service areas (damp brick, slate floors, service stairwells, sulfur coal grime, raw chapped skin).
* **Power & Observation:** Description must reflect Cora's constant surveillance of her surroundings. She maps the rooms not just to clean them, but to catalog secrets, keys, and vulnerabilities to write into her manuscript.

---

## 2. Character Voices & The Language Gap

* **Cora Hartley (Dialogue):** 
  - Speaks with the rounded, flat vowels of a **performed Wiltshire parson's daughter**. 
  - To superiors (Stern, Vance, Gideon), she is brief, quiet, respectful, and uses no contractions (*"Yes, Ma'am,"* *"I only wish to work hard"*).
  - To fellow servants (Missy/Miri), she is warm but cautious.
* **Cora Hartley (Internal Monologue - `cora_inner`):**
  - Highly literate, cynical, and observant. Traces Cork Irish syntax and terms privately (* Cork lilt, Cork Cork-Irish consonants, lye-stained skin, etc.).
  - Tracks the danger of exposure and class precarity.
* **Miss Stern (Housekeeper):** Speaks with administrative authority. Cold, clinical, measuring. She uses dialogue to establish absolute boundaries and transaction logic (*"Satisfaction is a transaction, Vale."*).
* **Miss Vance (Guest):** Petulant, volatile, and high-strung. She alternates between dramatic anger and submissive panic when Gideon is near.
* **Gideon Locke (Guest):** Speaks with flat, quiet, iron authority. He does not shout; his words carry absolute consequences.

---

## 3. Visual Staging & Sprite Constraints

You must inline staging commands directly within the narrative:

1. **Background Setup:** Set scenes using declared background handles:
   - `scene bg_savoy_corridor_morning` (or `bg_stern_office_entrance`, `bg_master_suite_day`, `bg_servants_corridor_dim`, `bg_laundry_room_day`)
   - Include transitions: `with fade` or `with dissolve`.
2. **Sprite Manipulation:** Show or hide character sprites at designated positions:
   - `show cora_sprite base_travel at left_full_body`
   - `show stern_sprite neutral at right_full_body`
   - Transitions for movement: `with moveinleft`, `with move`, `with dissolve`.
3. **Pacing with Staging:** Place descriptions of character expressions and movements immediately before or after dialogue lines to maintain spatial consistency.

---

## 4. Forbidden Vocabulary & Anachronisms

The historical linter will reject files containing modern jargon. Avoid the following forbidden words at all costs:
* *Okay, ok, cool, got it* (Use: *Very well, yes, as you wish, yes Ma'am*)
* *Hello* (Use: *Good day, greetings, yes sir*)
* *Stress, trauma, projecting, gaslight* (Use: *strain, dread, panic, madness, deception*)
* *Jeans, cell, phone, teenager, teens, weekend* (Use: *serge, trousers, chambers, carriage, Sabbath*)
