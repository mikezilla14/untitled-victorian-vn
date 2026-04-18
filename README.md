# Project Name: [Pending Title]

An AI-accelerated, adult pseudo-sandbox RPG visual novel set in a Victorian hotel. This project explores themes of dark gothic corruption, voyeurism, and the loss of purity, utilizing a dynamic "paper doll" visual state system.

## Repository Structure (Monorepo)

This repository is structured as a Monorepo to maintain all creative, technical, and developmental assets in a single location. This structure is specifically designed to provide localized context for AI coding assistants (like those used in the Anti-gravity IDE).

* **`/docs`**: Production and architecture documentation. Contains the Game Dev Bible, Game Mechanics Bible, financial tracking, and development roadmap.
* **`/narrative`**: The Story Bible and scripts. Strictly divided into immutable "Canon" files (setting, core character backstories) and dynamic "Writing Studio" plot files (version-controlled episodic scripts).
* **`/art_pipeline`**: Asset generation tools. Contains ComfyUI workflows, Stable Diffusion prompts, and raw "Paperdoll" mannequin assets before they are exported.
* **`/renpy_project`**: The actual playable game. Contains the standard Ren'Py structure (the `game` folder, `classes.rpy`, `ui_screens.rpy`, etc.).

## Tech Stack & Tools

* **Game Engine**: Ren'Py (v8+ for Python 3 support)
* **IDE**: Anti-gravity
* **AI Art Generation**: Stable Diffusion (ComfyUI) using Pony Diffusion V6 XL
* **Version Control**: Git / GitHub

## Development Philosophy & Scoping

* **Agentic AI Context**: By opening the root directory in the IDE, AI assistants have full access to cross-reference game mechanics (`/docs`) while generating Python logic (`/renpy_project`).
* **Consistency > Quality**: Visual consistency is the primary product. The art pipeline prioritizes fixed seeds, control networks, and layer-based inpainting (the "Paperdoll" method) over hyper-detailed but inconsistent prompt generation.
* **The "Rule of 3" Scope Cap**: To ensure rapid episodic releases, each module is strictly capped at 3 primary characters, 6 primary backgrounds, and 5 highly-polished event CGs.
* **Time Tracking**: All development time is tracked using a 4-tag schema (`CapEx_Infrastructure`, `OpEx_Production`, `Writing_Design`, `Marketing_Admin`) to calculate accurate Break-Even Points.
