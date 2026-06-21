# STYLE & VOICE GUIDE: THE PENNY DREADFUL MANUSCRIPT LAYER

This guide outlines the linguistic, stylistic, and formatting rules that the external LLM must follow to produce prose matching the tone and aesthetics of Cora Hartley's Holywell Street manuscript (`book1`).

---

## 1. Style & Sentence Architecture

To capture the sensational, late-Victorian "penny dreadful" genre, you must structure sentences and select words using these parameters:

* **Snappy, Action-Forward Cadence:** Avoid long, meandering, or overly complicated sentences. Keep sentences short, sharp, and punchy. Vary sentence lengths, but bias heavily toward brevity. Let actions land like quick physical impacts. Every sentence must drive the scene forward.
* **Visceral and Somatic Focus:** Ground the scene in immediate physical reactions and dark romance setpieces—the sudden grip on a wrist, the brush of fingers unlacing a corset, the sharp intake of breath, a throat pulse, the heat of skin, or a sudden shiver. Show, don't over-explain.
* **Refusal of Euphemisms:** Write transgressive scenes with clean but raw sensory detail. Focus on skin warmth, spit, sweat, tearing silk, tight stays, and the scent of jasmine, damp earth, or boiling soap-lye. Keep the dark romance raw, intense, and action-focused.
* **Engaging Power Dynamics:** Frame interactions as active combat or physical seduction. The dialogue and action must move fast—a sudden challenge, a quick step backward, a clinical lock of gazes. Keep the tension taut and the pacing rapid.
* **Aphoristic and Taxonomic Narration:** Coralie Vale categorizes her world quickly. Keep her insights brief and razor-sharp (e.g., *"Hierarchy teaches that some throats are safer to close in public,"* or *"Propriety is not a moral truth, but a weapon"*).

## 1.5 Gothic Grafting & Literary Seeding
The manuscript grafts Cora's hotel experiences onto six classic motifs. You must use these specific thematic guidelines when writing about the corresponding characters/states:
* **Sweeney Todd (Industrial Erasure):** Wired to **Ms. Stern/Mr. Sterick** and servant labor (laundry/boiler rooms). Describe labor as boiling tallow, processing lives for grease, and counting cattle for the slaughter.
* **Dracula (Hypnotic Possession):** Wired to **Sir Gideon/Lord Caldor** and **Missy/Miri**. Describe Caldor's gaze paralyzing the chest, the trance of service, salt-barriers, and sweet iron scents.
* **Jack the Ripper (Social Vivisection):** Wired to **The Ledger** and Cora's spying. The ledger is a clinical diary of dissections; Cora's accent is a heavy plaster mask held by bloody fingers.
* **Carmilla (Sapphic Seduction):** Wired to **Lady Vance/Lady Vayne** and **Missy's trust**. Unlacing Vayne's corset is a slow bite where Coralie feeds on pride; secrets shared like blood in sleepwalking attics.
* **Jekyll & Hyde (Internal Duality):** Wired to Cora's voice shift and Gideon's private beast. The performed accent is a potion swallowed to chain the Irish beast; Caldor's study is where the private beast reigns.
* **Frankenstein (Stitched Identity):** Wired to the manuscript creation and servant animation. The manuscript is sewn from dead scandals; maids are golems of cotton and lye.

---

## 2. Voice Guidelines: Performed vs. Internal

* **The English Mask (Dialogue):** When speaking to upper-class figures (Mr. Sterick, Lord Caldor, Lady Vayne), the dialogue must remain short, compliant, and hyper-decent. Avoid contractions. Perform the meek English maid.
* **The Irish Engine (Monologue):** The internal voice is highly literate, analytical, cynical, and observant. It registers the ambient prejudice and class violence without apology or self-pity.
* **The Slip:** In moments of high tension or intellectual provocation, let the performed English mask slip slightly—using a sharper word than a maid should know, or displaying a trace of Irish vocabulary or syntax.

---

## 3. Sensory Vocabulary Dictionary

Incorporate these period-accurate, atmospheric terms to ground the prose in the late-Victorian industrial/Gothic setting:

* **Domestic & Industrial Labor:** *Lye, lye-soap, caustic soda, lye-chapped hands, boiling vats, rising steam, tallow candles, paraffin, grease-ink, soot, hearth-ash, bone-boiling, marrow, lard, starch, copper pails.*
* **Costume & Body:** *Stays, corset-laces, starched cuffs, crinoline, silk petticoats, linen chemise, chapped red fingers, collarbone, throat pulse, throat-hollow, heels anchoring, lowered lashes.*
* **Gothic & Environmental:** *Damp jasmine, stagnant conservatory water, rotting soil, Waterloo smoke, gaslight flickers, wainscoting, coal-grime, amber hearth-glow, London smog, carriage cabins.*
* **Class & Leverage:** *Sovereigns, curate, parish, gentry, reference letters, credentials, ledgers, ciphers, trade monopolies, custody, gutter, destitution.*

---

## 4. Ren'Py Formatting & Reveal Mechanics

To integrate with the Ren'Py NVL engine, the generated prose must adhere to the following strict formatting rules:

1. **Plain Text Output:** Write the output as normal, clean plain text. Do NOT insert manual word delay tags like `{w=0.04}`. The game engine has a built-in Python function `book1_word_reveal_text` that automatically splits the string by spaces and injects typewriter delay at runtime.
2. **Page Boundaries:** The Ren'Py NVL screen can hold up to 4 lines of dialogue before it must be cleared. Group paragraphs into chunks of 3–4 lines. At the end of each chunk, output the page clear command:
   - `--- nvl clear ---`
3. **Internal Monologue Tagging:** Cora's inner thoughts while writing (metacomments on her writing process) must be enclosed in `cora_inner "..."` tags.
   - *Example:* `cora_inner "In the real hotel, I lacked the claws. But the page demands a bolder blood."`
4. **Debugging Metadata Header:** Precede every output with a YAML block detailing the input flags evaluated and the macro-variant routed.
