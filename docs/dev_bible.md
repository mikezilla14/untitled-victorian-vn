# STUDIO DEVELOPMENT BIBLE

**Project:** [Pending Title]
**Version:** 1.0
**Document Scope:** Studio ways of work, production cadence, time/cost tracking, and foundational Ren'Py technical architecture. 

---

## I. DEVELOPMENT PHILOSOPHY & SCOPING RULES

### 1. Consistency > Quality
In a visual novel, visual consistency is the primary product. A player will forgive a simpler art style if the character model remains identical across scenes, but will abandon a high-fidelity game if the character's face or body proportions morph. All AI generation pipelines must prioritize fixed seeds, control networks, and layer-based inpainting over complex "hyper-detailed" prompt generation.

### 2. The "Rule of 3" Scope Cap
To ensure deliverability within set constraints, the Minimum Viable Product (MVP) and all subsequent episodic updates must adhere to strict asset caps to prevent scope creep. Unless explicitly budgeted for in the OpEx tracker, a standard release module is capped at:
* **Max 3 Primary Characters** requiring dynamic sprite generation.
* **Max 6 Primary Backgrounds**.
* **Max 5 Highly-Polished Event CGs**.

---

## II. WAYS OF WORK & RESOURCE TRACKING

All development time and associated hardware costs (e.g., cloud GPU usage) must be tracked to calculate the true Marginal Cost of Production and establish accurate Break-Even Points (BEP). 

### 1. Time Tracking Protocol
All development hours must be logged using a frictionless tracking tool (e.g., Toggl) utilizing a strict 4-tag schema:

* **`CapEx_Infrastructure`:** One-time startup costs. Building reusable Ren'Py code, master UI screens, training base AI models/LoRAs, and defining core sandbox logic. This is permanent studio equity.
* **`OpEx_Production`:** Recurring episode costs. Writing specific scene scripts, generating event-specific CGs, coding scene logic, and engine assembly. 
* **`Writing_Design`:** Brainstorming, drafting narrative trees, and roadmap planning.
* **`Marketing_Admin`:** Top-of-funnel acquisition tasks, platform setup, community management, and technical research/learning.

### 2. Hardware Cost Allocation
Cloud GPU costs must be audited against the time tracker.
* GPU time spent training base models or establishing "Golden Master" characters is billed to `CapEx_Infrastructure`.
* GPU time spent generating specific scene art is billed to `OpEx_Production`.

---

## III. PRODUCTION CADENCE

The studio operates on a rapid, AI-accelerated release schedule to maintain recurring revenue retention.

* **MVP Phase:** An 8-week sprint dedicated to building the `CapEx_Infrastructure` and the foundational Chapter 1 `OpEx_Production`.
* **Episodic Cycle:** Post-MVP, the studio will operate on a strict 4-to-5 week release rhythm per episode:
    * **Week 1:** Scripting and dialogue locking.
    * **Week 2:** AI Art / CG Generation.
    * **Week 3:** Ren'Py assembly and logic coding.
    * **Week 4:** QA and Early Access release to paid tiers.
    * **Week 5:** Public release and marketing push.

---

## IV. REN'PY ENGINEERING FRAMEWORK

To prevent "spaghetti code" and ensure the game can scale episodically, the project utilizes Object-Oriented Python and modular Ren'Py scripting.

### 1. File Modularity
The codebase must be strictly organized into discrete `.rpy` files based on function:
* `script.rpy`: Core game flow and main entry point.
* `variables.rpy`: Defines default variables and data structures. Acts as the single source of truth for persistent game state.
* `functions.rpy`: Contains all Python-side game logic and helper functions.
* `characters.rpy`: Defines character objects.
* `screens.rpy`, `gui.rpy`, `options.rpy`: Contains custom UI screens, GUI styling, and configuration options.
* `day[N].rpy` and `endings.rpy`: Contains the actual narrative scripts separated by chronological days and ending branches.

### 2. Data Structures & State Tracking
Loose variables (e.g., `$ character_stat = 10`) are strictly prohibited for core game logic. All entities must be defined via Python Classes to allow for deep, trackable properties that can be easily referenced by the UI.
* Entities are instantiated at the start of the game.
* Methods within the class are used to mutate state (e.g., `character.add_stat(5)`), ensuring all state changes are centralized and predictable.

### 3. Visual State Representation (Dynamic Assembly)
To reflect the changing internal state of characters without exponentially increasing art assets, the game relies on Ren'Py's `layeredimage` functionality.
* Characters are not rendered as single flat PNGs for every permutation.
* They are assembled dynamically in-engine using a base "Mannequin" body layer, with conditional attribute layers (clothing, physical markers, expressions) overlaid based on the character's current class properties.

### 4. Interactive UI & Navigation
Standard linear text progression is replaced by a "pseudo point-and-click" architecture.
* Navigation and interaction rely on Ren'Py Screen Language, overlaying `imagebutton` or `imagemap` elements onto 2D background spaces.
* Completing an event calls the player back to the central sandbox loop rather than advancing to a linear text block.

### 5. Enforcing Choice Permanence
To maintain high-stakes tension and give weight to state changes, the standard Ren'Py rollback feature (mouse-wheel scrolling to undo a choice) can be restricted as a game option.
* As an in-game option following major branching decisions or resource expenditure, the `renpy.block_rollback()` function must be executed to force the player to live with the consequences of their actions or manually reload a hard save.
