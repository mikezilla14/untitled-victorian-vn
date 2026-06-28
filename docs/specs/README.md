# Feature specs

This folder holds implementation-facing feature specifications. Specs may describe shipped,
partially implemented, planned, or backlog work; each spec should state that status explicitly.

## Current specs

| Spec | Status cue |
|------|------------|
| [art-prompt-workflow.md](art-prompt-workflow.md) | Documentation workflow spec for repo-owned art prompt production. |
| [book-writing-styling.md](book-writing-styling.md) | Styling and authoring guidance for the book-writing engine. |
| [book1-writing-engine.md](book1-writing-engine.md) | Book 1 writing engine requirements and implementation status. |
| [character-specific-suspicion.md](character-specific-suspicion.md) | Planned replacement for the removed anxiety-scaled suspicion vignette: per-character suspicion, Cora anxiety, breakpoint monologues, and subtle eye/focus UI. |
| [character-specific-suspicion-implementation-plan.md](character-specific-suspicion-implementation-plan.md) | Planned implementation phases, task list, risks, and validation path for character-specific suspicion. |
| [narrative-pressure-system.md](narrative-pressure-system.md) | Planned reframing of stats as narrative pressure systems, objective journal, and manuscript readiness. |
| [narrative-pressure-system-implementation-plan.md](narrative-pressure-system-implementation-plan.md) | Planned implementation phases, task list, risks, and validation path for the narrative pressure system. |
| [scene-direction-agent.md](scene-direction-agent.md) | Implemented deterministic sprite placement agent and policy. |
| [story-chain-routing-refactor.md](story-chain-routing-refactor.md) | Planned non-prod routing refactor: time-period day spines, returning dynamic windows, queued penance, and DAG sync acceptance. |
| [writers-desk-agent-framework.md](writers-desk-agent-framework.md) | Partial — scaffolded prose-first agent + skill layer: lets a non-technical writer add flags/effects/branches and prose without Ren'Py, with interactive contract checks and human-overridable exceptions. |

## Required spec sections

- Purpose and target user/workflow.
- Current implementation status: `implemented`, `partial`, `planned`, or `backlog`.
- Source-of-truth files.
- Validation command or review path.
- Open questions or deferred decisions.
