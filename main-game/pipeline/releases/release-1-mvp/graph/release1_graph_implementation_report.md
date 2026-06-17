# Release 1 Graph Implementation Report

## Files Created

- `release1_graph_manifest.json`
- `release1_nodes.csv`
- `release1_edges.csv`
- `release1_choices.csv`
- `release1_gates.csv`
- `release1_effects.csv`
- `release1_router_outcomes.csv`
- `release1_graph_gaps.md`
- `release1_graph_audit.md`
- `release1_graph_mermaid.mmd`
- `release1_graph_implementation_report.md`

## Files Scanned

- `main-game/non-prod-game/game/days/book1_non_canon.rpy`
- `main-game/non-prod-game/game/days/day100_non_canon.rpy`
- `main-game/non-prod-game/game/days/day101_non_canon.rpy`
- `main-game/non-prod-game/game/days/day102_non_canon.rpy`
- `main-game/non-prod-game/game/days/day103_non_canon.rpy`
- `main-game/non-prod-game/game/days/day104_non_canon.rpy`
- `main-game/non-prod-game/game/days/day105_non_canon.rpy`
- `main-game/non-prod-game/game/days/test_day2_writing_non_canon.rpy`
- `main-game/non-prod-game/game/shared/classes_non_canon.rpy`
- `main-game/non-prod-game/game/shared/functions_non_canon.rpy`
- `main-game/non-prod-game/game/shared/story_chains_non_canon.rpy`

## Commands Run

- `py main-game/pipeline/tools/build_story_graph_manifest.py --release release-1-mvp --out-dir main-game/pipeline/releases/release-1-mvp/graph --storyboard main-game/draft/releases/planning/story_board.md`

## Extraction Counts

- Nodes: 169
- Edges: 149
- Choices: 97
- Gates: 13
- Effects: 92
- Gaps: 81

## Storyboard Audit

- Run: yes

## Recommended Next Owner

- Balancing Pass / Human Designer for gap triage.
