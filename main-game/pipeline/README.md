# Narrative pipeline (pre-draft exploration)

Everything here is **non-canon** and supports the writers' room before and during gate review. Nothing in `pipeline/` ships in the game.

## Why this exists

Previously `main-game/pipeline/` mixed spec scripts, brainstorm logs, gate verdicts, and JSON handoffs in one flat release folder — hard to browse and easy for agents to load the wrong context. Pipeline artifacts are grouped **by day** and **by type**.

## Folder types

| Subfolder | Written by | Agent context |
|-----------|------------|---------------|
| `specs/` | Divergent personas | Convergent stage only (current day) |
| `ideas/` | Divergent personas | **Excluded** from new assignments |
| `synthesis/` | Convergent writer | **Excluded** from new assignments |
| `gates/` | Lead editor, forensic psych, Victorian | After convergent; sequential order |
| `handoffs/` | Forensic psych, prod promotion | CI contracts; not prose context |

## Naming (unchanged)

| Artifact | Pattern | Example |
|----------|---------|---------|
| Spec script | `dayrdd_<persona>_spec.rpy` | `day105_tension_spec.rpy` |
| Idea log | `dayrdd_<persona>_ideas.md` | `day105_humour_ideas.md` |
| Convergent report | `dayrdd_convergent_report.md` | `day105_convergent_report.md` |
| Gate verdict | `dayrdd_gate_<gate>.md` + `.json` | `day105_gate_victorian.md` |
| Profile delta | `dayrdd_profile_delta.json` | in `handoffs/` |
| Promotion handoff | `dayrdd_promotion_handoff.json` | in `handoffs/` |

`r` = release number, `dd` = 2-digit day slot (`00`–`99`).

## Experiments

Ad-hoc spice comparisons and throwaway tries: `main-game/pipeline/experiments/` only.

## Promotion path

Approved prose lives in `main-game/draft/releases/<slug>/days/<day>/dayrdd_non_canon.rpy`. Runtime canon: `main-game/prod-game/game/dayrdd.rpy`.
