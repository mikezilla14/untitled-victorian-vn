# Untitled Victorian VN

A visual novel developed in Ren'Py, set in the historic Savoy Hotel, London, during the winter of 1891.

## Synopsis

Play as **Cora**, a young village girl and board school graduate working as a chambermaid at the newly opened Savoy Hotel. While attempting to maintain a spotless record under the tyrannical eye of housekeeper **Miss Stern**, Cora harbors a secret ambition: writing scandalous stories for a publisher on Holywell Street to send money back home.

Navigate the treacherous balance of your duties, the curiosity surrounding the enigmatic VIP guest **Sir Gideon Locke**, and your own burgeoning career as a writer of forbidden tales.

## Characters

| Character | Role | Colour |
|---|---|---|
| **Cora** | Protagonist — chambermaid & aspiring writer | Gold `#d4a574` |
| **Sir Gideon Locke** | Enigmatic VIP guest on the upper floor | Crimson `#a30000` |
| **Miss Stern** | Tyrannical housekeeper | Grey `#555555` |

## Features

- **Resource Management & Stats**: Three core statistics are tracked via a persistent HUD:
  - **Inspiration** — A spendable currency collected through actions and spent to write chapters. The cap scales with your Corruption Level (`20 + level × 10`), preventing grinding and encouraging narrative progression.
  - **Corruption** — Earned as XP during interactions (20 XP = 1 level). Higher levels unlock bolder choices, raise your Inspiration cap, and determine which ending you reach.
  - **Suspicion** — A risk/heat meter (0–100). Rises from risky choices and decays passively by 5 per time slot. Hitting 100 triggers an immediate game over.
- **Day/Time System**: The story progresses through five days, each divided into time slots (Morning, Afternoon, Evening). The current day and period are always visible in the stat overlay.
- **Narrative Flags**: Key story beats are tracked as one-way boolean flags (set once, never reset). These gate character moments and branching choices throughout the five days.
- **Multiple Endings**: Your Corruption level and choices determine your fate. Currently implemented endings:
  - **Game Over — Dismissed Without Character**: Suspicion reaches 100. Cora is fired and left with nothing.
  - **Bad Ending — Rejection**: Corruption level too low by Day 5. Cora's manuscript is returned — "We asked for fire. You sent us porridge."
  - **Cliffhanger** *(Day 5)*: The MVP arc concludes on a cliffhanger, pending future chapters.

## Narrative Structure

The story is split across five day files, loaded alphabetically by Ren'Py:

| File | Content |
|---|---|
| `script.rpy` | Entry point — intro monologue, jumps to `day1_morning` |
| `day1.rpy` | Day 1 — Cora's first shift; meeting the hotel |
| `day2.rpy` | Day 2 — Gideon initiates conversation |
| `day3.rpy` | Day 3 — The grate scene; Stern's hidden vulnerability |
| `day4.rpy` | Day 4 — Gideon's loneliness revealed; the passage choice |
| `day5.rpy` | Day 5 — Climax and cliffhanger |
| `endings.rpy` | Fail states and bad endings branching out of the main flow |

## Narrative Flags

| Flag | Meaning |
|---|---|
| `read_letters` | Cora glimpsed Gideon's private correspondence |
| `saw_voyeur_scene` | Cora witnessed a scene through the grate (Day 3) |
| `heard_stern_humming` | Cora saw Stern's hidden vulnerability (Day 3) |
| `gideon_spoke_day2` | Gideon initiated a conversation (Day 2) |
| `gideon_showed_depth` | Gideon's loneliness was revealed (Day 4) |
| `manuscript_sent` | Any chapter dispatched to Holywell Street |
| `payment_received` | Publisher's payment arrived |
| `wrote_chapter_1` | First chapter completed |
| `wrote_chapter_2` | Second chapter completed |
| `chose_bold_day4` | Cora held her nerve in the passage (Day 4) |

## Development

- Built with **Ren'Py Visual Novel Engine**
- Current status: **MVP Gray-Box Skeleton v2.0** — all five days scripted with placeholder prose, stat systems fully wired
- Publisher: **Holywell Street Studios** *(working title)*

## Repository Structure

```text
untitled-victorian-vn/
├── game/                    # Core game logic and assets
│   ├── audio/               # Sound effects and music
│   ├── gui/                 # UI graphics and assets
│   ├── images/              # Character sprites and backgrounds
│   ├── saves/               # Local save files (git-ignored)
│   ├── characters.rpy       # All character definitions
│   ├── variables.rpy        # All default game state (flags & stats)
│   ├── functions.rpy        # Python-side game logic (stat helpers)
│   ├── screens.rpy          # UI screen definitions (HUD overlay)
│   ├── gui.rpy              # Ren'Py UI configuration variables
│   ├── options.rpy          # Ren'Py project configuration
│   ├── script.rpy           # Entry point — launches the game
│   ├── day1.rpy             # Day 1 narrative
│   ├── day2.rpy             # Day 2 narrative
│   ├── day3.rpy             # Day 3 narrative
│   ├── day4.rpy             # Day 4 narrative
│   ├── day5.rpy             # Day 5 narrative & cliffhanger
│   └── endings.rpy          # Fail states and bad endings
├── utilities/
│   └── stats_refactor.py    # Dev script used to refactor stat mechanics
└── .gitignore               # Git ignore rules for Ren'Py
```

## Running the Game

Open the project in the **Ren'Py launcher** and click **Launch Project**, or point the launcher at the `game/` directory. Requires Ren'Py 7.x or 8.x.
