# NARRATIVE SUMMARY & FLAG WIRING MANUAL

This document lists the real-life (IRL) gameplay timeline at the Savoy Hotel (Days 100 to 105) and acts as the technical mapping schema showing how player decisions and state variables are wired into Cora's branching manuscript (`book1`).

---

## 1. Timeline of IRL Activities (Days 100–105)

### DAY 100: Prologue — The Wiltshire Estate & Waterloo Arrival
* **Core Narrative:** Cora is dismissed from her position at Sir John Wiltshire's country estate after she is caught in proximity to a scandal involving Lady Eleanor and an under-housemaid, Margaret Pryce. She travels to London by train, holding forged credentials and her incomplete, transgressive manuscript.
* **Key Decisions:**
  - How Cora encountered the scandal (overhearing whispers vs reading private correspondence).
  - Her motivation for writing (earning money for home, cataloging human folly, or hunger for raw scandal).
  - Her posture upon arrival in London (careful survival, eager ambition, or desperate haste).

### DAY 101: Savoy Hotel — Day 1 & First Shift
* **Core Narrative:** Cora begins her employment as a chambermaid at the Savoy Hotel under the severe eye of Ms. Stern. She performs a corridor shift, spying on Sir Gideon Locke's guest suite through the keyhole.
* **Key Decisions:**
  - Spying strategy: Predator (watching for leverage), Prey (intimate and vulnerable exposure), or Ghost (dispassionate, silent observation).
  - Vocal performance during the job interview with Ms. Stern (performing a meek country-girl drawl vs presenting competent efficiency).
  - Reaction to Stern's commands (subservient compliance, silent resistance, or complicit agreement).
  - First encounter with the junior maid Missy/Miri (calming Missy's panic, unsettling her further by sharing details, or maintaining shared caution).
  - Focus of her private journal entry (analytical inspiration/order vs raw corruption/want).
  - Night Action: Write the first chapter of her manuscript or visit Missy in the servants' quarters.

### DAY 102: Savoy Hotel — Day 2 & The Contraband
* **Core Narrative:** Cora discovers stolen guest under-linen (contraband). She is caught up in a high-stakes tea-room confrontation involving Sir Gideon Locke, Lady Vance, and Ms. Stern.
* **Key Decisions:**
  - Handling of contraband: Stealing and wearing it (visceral physical tension) vs planting it in Gideon's traveling trunk (misdirection).
  - Behavior in the tea room: Playing the predator (helpful discovery of the item to protect Vance), prey (confessing she found it and failed to report it, seeking mercy), or ghost (keeping silent, leaving Miri/Missy to take the blame).
  - Breaking Missy's trust to escape blame vs absorbing the cost herself.
  - Night Action: Write Chapter II or indulge in raw prose.

### DAY 103: Savoy Hotel — Day 3 & Gideon's Challenge
* **Core Narrative:** Cora is summoned to Gideon Locke's guest suite. He challenges her identity and presents her with a hairbrush, forcing a moment of close-proximity styling. Later, he corners her by the basement furnace doors, delivering an ultimatum.
* **Key Decisions:**
  - Handling the brush in the suite (predator stroke, prey compliance, or ghost-like observational neutrality).
  - Stern's interrogation (answering foolishly, giving a partial truth, or lying).
  - Reaction to Gideon's furnace-room ultimatum: Defying him, bargaining terms, or surrendering.
  - Night Action: Write Chapter III or barricade the door.

### DAY 104: Savoy Hotel — Day 4 & The Lockbox Heist
* **Core Narrative:** Cora enters Gideon's suite while he is out, attempting to crack his lockbox and retrieve a compromising photograph. She must escape before he returns, utilizing a bold lie or sacrificing Missy's cover.
* **Key Decisions:**
  - Retaining the stolen photograph (leverage) vs failing to retrieve it.
  - Escape method: Climbing out the window/fireplace, deploying a bold lie, or using Missy as cover.
  - Atoning for her lies to Missy vs keeping up the deceit.
  - Night Action: Finishing the manuscript draft (Chapter IV).

### DAY 105: Savoy Hotel — Day 5 & The Climax
* **Core Narrative:** Sir Gideon Locke returns unexpectedly. Cora's leverage fantasy is tested. The absolute weight of Victorian class protection collapses her individual ambition. She must choose whether to take the hush money and run, refuse it, or destroy the evidence.
* **Key Decisions:**
  - Taking the money, refusing it, or deferring the choice.
  - Destroying the photograph vs letting Gideon burn it.
  - The final dynamic with Gideon: Muse (artistic synthesis), Protege (shared fall), Adversary (leverage), or Witness (observation of the machine).
  - Night Action: Writing the final, diagnostic Chapter V.

---

## 2. Flag-to-Narrative Wiring Map

The following variables in the Ren'Py python state (`story` and `player`) dictate the precise routing and textual content of the manuscript chapters:

| Variable | Target Type | Value | IRL Choice Context | Direct Impact on the Book Layer (`book1`) |
| :--- | :--- | :--- | :--- | :--- |
| **`player.corruption_level`** | `int` | `$\le 2$` | Did not cross major boundaries or take high risks in Day 1. | Routes to **Slop Chapter I** (`day1_slop_chapter`). The prose is respectable, generic, and bloodless. |
| | | `$> 2$` | Gained corruption XP by choosing transgressive, high-risk actions. | Routes to **Corrupted Alt Chapter I** (`day1_chapter`). The prose is raw, vivid, and transgressive (Lady Beatrice conservatory tryst). |
| **`story.day1_corridor_state`** | `str` | `"ghost"` | Spied on Locke's suite with dispassionate observation. | Chapter I/III/IV/V default to **Ghost Archetype**: prose is silent, evidentiary, and observational. Desire is written as omission. |
| | | `"predator"` | Spied on Locke's suite searching for tactical leverage. | Chapter I/III/IV/V default to **Predator Archetype**: prose is clinical, deliberate, and tactical. Desire is leverage. |
| | | `"prey"` | Spied on Locke's suite, allowing herself to feel vulnerable. | Chapter I/III/IV/V default to **Prey Archetype**: prose is intimate and exposed. Attraction and danger coexist. |
| **`story.day1_interview_state`** | `str` | `"meek"` | Performed a soft, subservient drawl for Ms. Stern. | Coralie performs a soft, compliant drawl to hide her true self/accent under a performed English mask. |
| | | `"competent"`| Showed calm, efficient precision to Ms. Stern. | Coralie performs a flawless, clinical Sussex accent—a polished mask of chalk hiding hands that know the knife. |
| **`story.day1_stern_relation`** | `str` | `"subservient"`| Yielded entirely to Stern's authority. | Coralie writes herself moving like clockwork, a golem animated only by Sterick's keys. |
| | | `"resistant"`| Kept distance, showing silent defiance to Stern. | Coralie writes herself bowing but clawing the wood—a lamb knowing the butcher is counting its fat. |
| | | `"complicit"`| Reached a quiet, professional understanding with Stern. | Coralie writes a shared understanding of two slaughtermen: discretion is the butcher's grease. |
| **`story.day1_vance_relation`** | `str` | `"protected"` | Protected Lady Vance during the corridor confrontation. | Coralie unpins Vance's hair, whispering comfort—building a wall around her fear to keep other predators out. |
| | | `"intimate"` | Allowed proximity and sensory tension with Vance. | Coralie presses the red pressure mark of Caldor's grip on Lady Vayne's collarbone. High dark-romance tension. |
| | | `"observed"` | Kept a cold, professional distance from Vance. | Coralie unpins Vance's dress with clinical distance, dissecting her vulnerability like a carcass on the block. |
| | | `"accomplice"` | Agreed to help Vance cover her tracks. | Leaning close in the dark corridor, sealing collusion as Vayne realizes they share the same animal appetite. |
| **`story.missy_day1_trust_state`**| `str` | `"soothed"` | Calmed Missy's panic with comforting words. | Pacified Miri with soft, grease-soft lies. Miri sleeps soundly, unaware of the butcher. |
| | | `"unsettled"` | Shared frightening details, heightening Missy's fear. | Miri's trust is shattered; used as a shield, she shivers at rising steam, knowing she could be boiled. |
| | | `"shared_caution"`| Agreed to stay alert and avoid trouble together. | Clinging to each other's heat in the corridor like birds caught in the same snare. |
| **`story.day1_ledger_focus`** | `str` | `"inspiration"`| Categorized observations systematically. | Pen dissects the scene, recording order, cost, and distance. |
| | | `"corruption"` | Recorded raw desires and boundary crossings. | Pen writes want—spit, sweat, white faces, and raw hunger. |
| **`story.day2_tea_choice`** | `str` | `"ghost"` | Let Missy take the blame for the contraband. | Routes to **Ghost Chapter II**: watching Lady Vayne's fury and Caldor's shadow from the margin. Miri is sacrificed. |
| | | `"predator"` | Stepped in to rescue Vance's propriety. | Routes to **Predator Chapter II**: Coralie crosses the salon to lift the lace, earning Caldor's courtly nod. |
| | | `"prey"` | Confessed to seeing the contraband, showing fear. | Routes to **Prey Chapter II**: Confession trembles on her tongue; Caldor's furnace gaze is a fire she walks toward. |
| **`story.day2_contraband_state`** | `str` | `"stolen_wearing"`| Stole the guest under-linen and wore it. | Coralie wears the secret contraband under her uniform, setting the chapter humming with raw physical/tactile heat. |
| | | `"planted_in_trunk"`| Planted the contraband in Gideon's trunk. | Savoring the thrill of a well-laid seduction/misdirection by planting it in Caldor's trunk. |
| **`story.missy_day2_trust_break`** | `bool` | `True` | Betrayed Missy to protect herself. | Miri is written as carrying the hatbox curse; the manuscript brands the debt like an unlaunderable stain. |
| | | `False` | Protected Missy or absorbed the suspicion. | Miri remains at the margin; Coralie grants her a bittersweet mercy that admits repair without return to innocence. |
| **`story.missy_day2_suspicion_state`**| `str` | `"uneasy"` | Let Missy take active suspicion from Stern. | Mr. Sterick questions Miri first. Hierarchy teaches that some throats are safer to close in public. |
| **`story.day3_ultimatum`** | `str` | `"defied"` | Refused Gideon's furnace-room terms. | Caldor corners her; she answers with refusal sharpened into a ceremonial blade. Refuses euphemism. |
| | | `"surrendered"` | Accepted Gideon's terms out of necessity. | Consent is survival arithmetic, showing how surrender can feel perilously close to coercion. |
| **`story.day3_twilight_action`** | `str` | `"frantic_write"`| Wrote frantically in her room at twilight. | Prose runs hot with velocity, as if dawn will confiscate the pages. |
| **`story.day4_escape_state`** | `str` | `"missy_cover"` | Escaped by using Missy as a distraction. | Coralie survives by spending Miri's credibility; the narrative records this cold exchange. |
| **`story.has_photograph`** | `bool` | `True` | Successfully stole the photograph from the lockbox.| The photograph is a ledger cipher that reframes fear as leverage. |
| **`story.day5_dynamic`** | `str` | `"muse"` / `"witness"` / `"adversary"` / `"protege"` | The final resolution dynamic with Gideon. | Chapter V shifts from personal confession to a systemic diagnosis of the machine that protects Caldor. |
