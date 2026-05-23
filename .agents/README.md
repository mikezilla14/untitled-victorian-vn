# .agents/ — AI Production Stack for [Untitled Victorian VN]

## What is this?

This directory contains **agent system prompt definitions** for the AI-assisted production pipeline.
Each `.md` file is a role you paste as a system prompt into an AI session to give it a specific job.

**The entry point is always `ORCHESTRATOR.md`.** You never need to choose a specialist yourself.

---

## Quick Start

1. Open a new Claude Code session (or any AI assistant).
2. Copy and paste the full contents of `ORCHESTRATOR.md` as your system prompt.
3. Describe what you want in plain English.

The Orchestrator classifies your request, identifies the correct pipeline, and tells you which
specialist agents to invoke in what order. If your request is ambiguous, it will ask one
clarifying question before routing.

---

## Available Workflows

| What you want to do | Example prompt | Pipeline |
|---|---|---|
| Draft and ship a new day | "Produce day 106: morning, Cora finds the letter" | `produce-day` |
| Review a draft for story/history accuracy | "Review the day 104 draft for canon accuracy" | `review-scene` |
| Gate a PR before merging | "Review this PR: [diff or file list]" | `review-pr` |
| Implement an already-approved draft | "Implement the day 105 non-canon draft" | `implement-spec` |
| Ask a historical question | "Could Cora have a typewriter in 1891?" | `historical-check` |
| Update locked canon | "Update Cora's backstory to include the new reveal" | `canon-update` |
| Introduce a new character or location | "Add a new character: Dr. Farrow, house physician" | `new-entity` |
| Add a new game mechanic | "We need fatigue tracking as a new mechanic" | `add-mechanic` |
| Fix a broken day file | "Day 103 fails renpy lint with a NameError" | `debug-day` |

---

## Agent Roster

| Agent | File | Role |
|---|---|---|
| **Orchestrator** | `ORCHESTRATOR.md` | Entry point. Classifies tasks and routes to specialists. |
| **Writers' Room** | `specialists/writers-room.md` | Drafts story in Ren'Py-shaped non-canon scripts. |
| **Lead Narrative Editor** | `specialists/narrative-editor.md` | Gates canon accuracy, character voice, and stat alignment. |
| **Victorian Consultant** | `specialists/victorian-consultant.md` | Gates historical accuracy for 1891 England. |
| **Code Agent** | `specialists/code-agent.md` | Implements approved drafts as runnable Ren'Py. |
| **Chief Architect** | `specialists/chief-architect.md` | Gates all code; owns architecture and the episode promotion checklist. |

---

## Using a Specialist Directly

Each specialist file contains a complete system prompt. If you know which specialist you need:

1. Open a new AI session.
2. Paste the full contents of the specialist's `.md` file as your system prompt.
3. Provide your task input (a file path, scene text, diff, or question).

Each file starts with a **How to Invoke** section explaining its inputs and outputs.

---

## Human Approval Gates

These actions always require your explicit authorization before any agent proceeds:

- Any change to files in `narrative/canon/`
- Any change to `classes.rpy`, `screens.rpy`, or `variables.rpy`
- Any change to `.agents/` or `.guardrails.yml`
- The `canon-update` pipeline after the two review stages
- The `new-entity` pipeline after the two review stages
- The `add-mechanic` pipeline after the design stage

Agents will stop and surface both the analysis and a clear question. Your answer unlocks the next stage.

---

## Reference

- `reference/dev-bible.md` — Studio development bible. Scope guardrails, architecture contracts,
  release cadence. Not an agent — read for project context.
