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

- `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/days/book1_non_canon.rpy`
- `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/days/day100_non_canon.rpy`
- `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/days/day101_non_canon.rpy`
- `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/days/day102_non_canon.rpy`
- `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/days/day103_non_canon.rpy`
- `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/days/day104_non_canon.rpy`
- `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/days/day105_non_canon.rpy`
- `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/days/test_day2_writing_non_canon.rpy`
- `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/shared/classes_non_canon.rpy`
- `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/shared/functions_non_canon.rpy`
- `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/shared/story_chains_non_canon.rpy`

## Commands Run

- `py narrative/pipeline/tools/build_story_graph_manifest.py --release release-1-mvp --out-dir narrative/pipeline/releases/release-1-mvp/graph --storyboard narrative/draft/releases/release-1-mvp/planning/story_board.md`

## Extraction Counts

- Nodes: 169
- Edges: 157
- Choices: 97
- Gates: 13
- Effects: 92
- Gaps: 81

## Storyboard Audit

- Run: yes

## Recommended Next Owner

- Balancing Pass / Human Designer for gap triage.
