# GAME MECHANICS BIBLE
**Project:** [Pending Title]  
**Version:** 1.0  
**Document Scope:** Definition of core interactive systems, state trackers, user interface mechanics, and choice architecture. 

## I. MECHANICS WORKFLOW & GOVERNANCE
This document serves as the absolute source of truth for all player-facing mechanics. 
* **Exclusion of Economy:** This document defines *what* the levers are and *how* they function mechanically. It does not dictate the numerical balancing of the in-game economy (e.g., exactly how many points an action costs). Balancing is handled via a separate external tracker.
* **Feature Expansion Protocol:** If the narrative requires a new mechanic (e.g., a new relationship tracker or inventory system), it must first undergo a cost-benefit analysis regarding asset generation and code bloat. Only upon approval is the mechanic added to this document, prior to mathematical balancing and implementation.

## II. CORE GAMEPLAY LOOP (THE PSEUDO-SANDBOX)
The game utilizes a "pseudo point-and-click" architecture rather than standard linear text progression. 

### 1. Time & Navigation
* **The Hub:** Navigation relies on UI screens overlaid on 2D backgrounds, allowing the player to click specific doors, items, or NPCs.
* **Time Progression:** The game operates on a Time System (e.g., Morning, Afternoon, Night). 
* **The Loop:** Completing an action or event advances the time of day and returns the player to the central sandbox loop rather than advancing to a forced linear text block.
* **Day/Night Duality:** The "Day" phase functions as a resource gatherer where the MC maintains her "Mask" of propriety. The "Night" phase is when the "Veil" lifts, allowing the player to spend gathered resources to advance the plot.

### 2. The Writing Gating Mechanic
* **The Function:** The player's primary objective is to write chapters of a manuscript. 
* **The Gate:** The player cannot proceed with writing until they have gathered the necessary experiential resources (stats) by observing or participating in world events.
* **The Reward:** Initiating the writing action triggers the explicit content (the MC's imagination/drafts) as a reward for successful sandbox navigation.

## III. PRIMARY STATE TRACKERS (THE DIALS)
Loose variables are strictly prohibited for core logic; all state tracking is managed via Object-Oriented Python classes to allow for deep, trackable properties. 

### 1. The Core Economy
* **Inspiration:** Gained by snooping, witnessing events, or finding clues. This acts as the primary currency required to successfully write manuscript chapters.
* **Corruption:** Gained by participating in illicit acts, trying on scandalous clothing, or crossing moral boundaries. It is required to write believable explicit content and unlocks darker narrative options.
* **Suspicion:** A fail-state tracker. Gained by performing risky actions, being caught snooping, or failing social checks. If Suspicion reaches its maximum threshold, the game triggers a "Game Over" state.

### 2. The Agency Alignment (Predator vs. Prey)
The player's approach to gathering Inspiration and Corruption is tracked on a spectrum of agency, determining their psychological alignment.
* **Influence (Dominant / Predator):** Increased by actions where the MC actively manipulates NPCs, sets traps, or orchestrates downfalls (e.g., hiding an item to watch an NPC take the blame).
* **Submission (Submissive / Prey):** Increased by actions where the MC deliberately crosses lines to invite attention or subjugation (e.g., stealing an item to try it on secretly).

## IV. VISUAL STATE REPRESENTATION (THE PAPERDOLL)
To reflect the changing internal state of the MC and maintain high retention, the game utilizes a dynamic "Paper Doll" UI.

### 1. The Mirror UI
* The player has access to a persistent "Status" image or "Mirror" button within the UI to view the MC's current physical build and corruption level.
* Interacting with the mirror triggers dynamic internal monologue text that shifts based on the MC's current Corruption stat.

### 2. Layers of Propriety
The paperdoll tracks the MC's clothing as layers, which are assembled dynamically in-engine based on current class properties.
* **Layer 1 (The Shell):** The heavy, modest outer dress representing the public safe zone.
* **Layer 2 (The Cage):** The corset and petticoats representing societal restraint.
* **Layer 3 (The Secret):** The undergarments, or lack thereof, representing hidden corruption.
* **Layer 4 (The Skin):** Permanent physical markers, such as sweat, flush, or tattoos.

## V. CHOICE ARCHITECTURE & CONSEQUENCE
To maintain high-stakes tension, player choices must feel permanent and deeply impactful this will be done primarily through creating consequential narrative choices but also through the following mechanics.
* **Option Locking:** As the MC's Corruption stat increases, "Pure" or wholesome dialogue options are not hidden; they remain visible but are grayed out or locked with a padlock icon to visually reinforce what the player has permanently lost.
* **Mutually Exclusive Branching:** Time is a strict resource. Committing to an action in a specific location locks the player out of simultaneous events occurring elsewhere, forcing strategic prioritization.
