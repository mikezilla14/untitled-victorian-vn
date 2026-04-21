---
trigger: always_on
---

IV. REN'PY ENGINEERING FRAMEWORK

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