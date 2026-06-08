# Release 1 Graph Gaps

## Missing DAG Tags

### gap_0007 - missing_dag_gate_tag

- Source: `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/days/day102_non_canon.rpy:1023`
- Label: `day102_3_gideon_interrupts_controls_vance`
- Description: Flow-affecting condition has no DAG_GATE tag.
- Recommended owner: Create/Rewrite Day Workflow
- Recommended next action: Add DAG_GATE metadata if this gate is balancing-relevant.

### gap_0008 - missing_dag_gate_tag

- Source: `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/days/day102_non_canon.rpy:1098`
- Label: `day102_4_cora_writes_a_chapter`
- Description: Flow-affecting condition has no DAG_GATE tag.
- Recommended owner: Create/Rewrite Day Workflow
- Recommended next action: Add DAG_GATE metadata if this gate is balancing-relevant.

### gap_0009 - missing_dag_gate_tag

- Source: `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/days/day102_non_canon.rpy:1100`
- Label: `day102_4_cora_writes_a_chapter`
- Description: Flow-affecting condition has no DAG_GATE tag.
- Recommended owner: Create/Rewrite Day Workflow
- Recommended next action: Add DAG_GATE metadata if this gate is balancing-relevant.

### gap_0010 - missing_dag_gate_tag

- Source: `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/days/day102_non_canon.rpy:1138`
- Label: `day102_4_cora_writes_a_chapter`
- Description: Flow-affecting condition has no DAG_GATE tag.
- Recommended owner: Create/Rewrite Day Workflow
- Recommended next action: Add DAG_GATE metadata if this gate is balancing-relevant.

### gap_0013 - missing_dag_gate_tag

- Source: `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/days/day103_non_canon.rpy:53`
- Label: `day103_morning`
- Description: Flow-affecting condition has no DAG_GATE tag.
- Recommended owner: Create/Rewrite Day Workflow
- Recommended next action: Add DAG_GATE metadata if this gate is balancing-relevant.

### gap_0017 - missing_dag_gate_tag

- Source: `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/days/day103_non_canon.rpy:1225`
- Label: `day103_3_bedroom_final_write`
- Description: Flow-affecting condition has no DAG_GATE tag.
- Recommended owner: Create/Rewrite Day Workflow
- Recommended next action: Add DAG_GATE metadata if this gate is balancing-relevant.

### gap_0018 - missing_dag_gate_tag

- Source: `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/days/day104_non_canon.rpy:970`
- Label: `day104_6_false_dawn_ending`
- Description: Flow-affecting condition has no DAG_GATE tag.
- Recommended owner: Create/Rewrite Day Workflow
- Recommended next action: Add DAG_GATE metadata if this gate is balancing-relevant.

### gap_0019 - missing_dag_choice_tag

- Source: `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/days/test_day2_writing_non_canon.rpy:26`
- Label: `test_day2_writing_harness`
- Description: Menu has no adjacent DAG_CHOICE tag.
- Recommended owner: Create/Rewrite Day Workflow
- Recommended next action: Add DAG_CHOICE beside the existing CHOICE marker.

### gap_0020 - missing_dag_gate_tag

- Source: `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/shared/functions_non_canon.rpy:82`
- Label: `file`
- Description: Flow-affecting condition has no DAG_GATE tag.
- Recommended owner: Create/Rewrite Day Workflow
- Recommended next action: Add DAG_GATE metadata if this gate is balancing-relevant.

### gap_0030 - missing_dag_gate_tag

- Source: `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/shared/story_chains_non_canon.rpy:26`
- Label: `check_confrontations`
- Description: Flow-affecting condition has no DAG_GATE tag.
- Recommended owner: Create/Rewrite Day Workflow
- Recommended next action: Add DAG_GATE metadata if this gate is balancing-relevant.

### gap_0031 - missing_dag_gate_tag

- Source: `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/shared/story_chains_non_canon.rpy:33`
- Label: `check_confrontations`
- Description: Flow-affecting condition has no DAG_GATE tag.
- Recommended owner: Create/Rewrite Day Workflow
- Recommended next action: Add DAG_GATE metadata if this gate is balancing-relevant.

### gap_0032 - missing_dag_gate_tag

- Source: `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/shared/story_chains_non_canon.rpy:37`
- Label: `check_confrontations`
- Description: Flow-affecting condition has no DAG_GATE tag.
- Recommended owner: Create/Rewrite Day Workflow
- Recommended next action: Add DAG_GATE metadata if this gate is balancing-relevant.

### gap_0033 - missing_dag_gate_tag

- Source: `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/shared/story_chains_non_canon.rpy:41`
- Label: `check_confrontations`
- Description: Flow-affecting condition has no DAG_GATE tag.
- Recommended owner: Create/Rewrite Day Workflow
- Recommended next action: Add DAG_GATE metadata if this gate is balancing-relevant.

### gap_0035 - missing_dag_gate_tag

- Source: `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/shared/story_chains_non_canon.rpy:797`
- Label: `end_slot`
- Description: Flow-affecting condition has no DAG_GATE tag.
- Recommended owner: Create/Rewrite Day Workflow
- Recommended next action: Add DAG_GATE metadata if this gate is balancing-relevant.

## Ambiguous Choice Groups

No findings.

## Missing / Incomplete apply_effects

No findings.

## Deprecated Generic Suspicion Usage

### gap_0011 - deprecated_generic_suspicion_usage

- Source: `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/days/day102_non_canon.rpy:1191`
- Label: `day102_4_cora_sneaks_a_feel`
- Description: apply_effects() uses deprecated generic susp field.
- Recommended owner: Non-Prod Code Agent
- Recommended next action: Replace with character-specific suspicion field.

## Unmapped Effect Fields

### gap_0012 - unmapped_effect_fields

- Source: `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/days/day102_non_canon.rpy:1191`
- Label: `day102_4_cora_sneaks_a_feel`
- Description: Unmapped apply_effects fields: susp.
- Recommended owner: Balancing Pass
- Recommended next action: Confirm runtime effect mapping.

## Router Outcome Mismatches

### gap_0037 - router_outcome_mismatches

- Source: `renpy_project/game/classes.rpy:0`
- Label: `StoryState.SLOT_EXIT_ROUTES`
- Description: Outcome d1_reflect_done has no extracted call site.
- Recommended owner: Chief Architect
- Recommended next action: Confirm unused route is expected.

### gap_0038 - router_outcome_mismatches

- Source: `renpy_project/game/classes.rpy:0`
- Label: `StoryState.SLOT_EXIT_ROUTES`
- Description: Outcome d1_write_ch1 has no extracted call site.
- Recommended owner: Chief Architect
- Recommended next action: Confirm unused route is expected.

### gap_0039 - router_outcome_mismatches

- Source: `renpy_project/game/classes.rpy:0`
- Label: `StoryState.SLOT_EXIT_ROUTES`
- Description: Outcome d1_visit_missy has no extracted call site.
- Recommended owner: Chief Architect
- Recommended next action: Confirm unused route is expected.

### gap_0040 - router_outcome_mismatches

- Source: `renpy_project/game/classes.rpy:0`
- Label: `StoryState.SLOT_EXIT_ROUTES`
- Description: Outcome d2_reflect_done has no extracted call site.
- Recommended owner: Chief Architect
- Recommended next action: Confirm unused route is expected.

### gap_0041 - router_outcome_mismatches

- Source: `renpy_project/game/classes.rpy:0`
- Label: `StoryState.SLOT_EXIT_ROUTES`
- Description: Outcome d2_write_night has no extracted call site.
- Recommended owner: Chief Architect
- Recommended next action: Confirm unused route is expected.

### gap_0042 - router_outcome_mismatches

- Source: `renpy_project/game/classes.rpy:0`
- Label: `StoryState.SLOT_EXIT_ROUTES`
- Description: Outcome d3_reflect_done has no extracted call site.
- Recommended owner: Chief Architect
- Recommended next action: Confirm unused route is expected.

### gap_0043 - router_outcome_mismatches

- Source: `renpy_project/game/classes.rpy:0`
- Label: `StoryState.SLOT_EXIT_ROUTES`
- Description: Outcome d3_twilight_done has no extracted call site.
- Recommended owner: Chief Architect
- Recommended next action: Confirm unused route is expected.

### gap_0044 - router_outcome_mismatches

- Source: `renpy_project/game/classes.rpy:0`
- Label: `StoryState.SLOT_EXIT_ROUTES`
- Description: Outcome d3_stern_done has no extracted call site.
- Recommended owner: Chief Architect
- Recommended next action: Confirm unused route is expected.

### gap_0045 - router_outcome_mismatches

- Source: `renpy_project/game/classes.rpy:0`
- Label: `StoryState.SLOT_EXIT_ROUTES`
- Description: Outcome d3_ultimatum_done has no extracted call site.
- Recommended owner: Chief Architect
- Recommended next action: Confirm unused route is expected.

### gap_0046 - router_outcome_mismatches

- Source: `renpy_project/game/classes.rpy:0`
- Label: `StoryState.SLOT_EXIT_ROUTES`
- Description: Outcome d3_write_night has no extracted call site.
- Recommended owner: Chief Architect
- Recommended next action: Confirm unused route is expected.

### gap_0047 - router_outcome_mismatches

- Source: `renpy_project/game/classes.rpy:0`
- Label: `StoryState.SLOT_EXIT_ROUTES`
- Description: Outcome d4_write_night has no extracted call site.
- Recommended owner: Chief Architect
- Recommended next action: Confirm unused route is expected.

### gap_0048 - router_outcome_mismatches

- Source: `renpy_project/game/classes.rpy:0`
- Label: `StoryState.SLOT_EXIT_ROUTES`
- Description: Outcome d4_dawn_gate has no extracted call site.
- Recommended owner: Chief Architect
- Recommended next action: Confirm unused route is expected.

### gap_0049 - router_outcome_mismatches

- Source: `renpy_project/game/classes.rpy:0`
- Label: `StoryState.SLOT_EXIT_ROUTES`
- Description: Outcome d5_write_night has no extracted call site.
- Recommended owner: Chief Architect
- Recommended next action: Confirm unused route is expected.

## Dynamic Jump Targets

### gap_0001 - dynamic_jump_targets

- Source: `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/days/day101_non_canon.rpy:630`
- Label: `day101_night_story_window`
- Description: story.resolve_chain_label() creates dynamic chain target.
- Recommended owner: Chief Architect
- Recommended next action: Resolve dynamically in future simulator.

### gap_0002 - dynamic_jump_targets

- Source: `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/days/day101_non_canon.rpy:636`
- Label: `day101_night_story_window`
- Description: story.resolve_chain_label() creates dynamic chain target.
- Recommended owner: Chief Architect
- Recommended next action: Resolve dynamically in future simulator.

### gap_0003 - dynamic_jump_targets

- Source: `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/days/day101_non_canon.rpy:642`
- Label: `day101_night_story_window`
- Description: story.resolve_chain_label() creates dynamic chain target.
- Recommended owner: Chief Architect
- Recommended next action: Resolve dynamically in future simulator.

### gap_0004 - dynamic_jump_targets

- Source: `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/days/day102_non_canon.rpy:420`
- Label: `day102_afternoon_story_window`
- Description: story.resolve_chain_label() creates dynamic chain target.
- Recommended owner: Chief Architect
- Recommended next action: Resolve dynamically in future simulator.

### gap_0005 - dynamic_jump_targets

- Source: `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/days/day102_non_canon.rpy:426`
- Label: `day102_afternoon_story_window`
- Description: story.resolve_chain_label() creates dynamic chain target.
- Recommended owner: Chief Architect
- Recommended next action: Resolve dynamically in future simulator.

### gap_0006 - dynamic_jump_targets

- Source: `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/days/day102_non_canon.rpy:432`
- Label: `day102_afternoon_story_window`
- Description: story.resolve_chain_label() creates dynamic chain target.
- Recommended owner: Chief Architect
- Recommended next action: Resolve dynamically in future simulator.

### gap_0014 - dynamic_jump_targets

- Source: `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/days/day103_non_canon.rpy:247`
- Label: `day103_1_optional_character_chain`
- Description: story.resolve_chain_label() creates dynamic chain target.
- Recommended owner: Chief Architect
- Recommended next action: Resolve dynamically in future simulator.

### gap_0015 - dynamic_jump_targets

- Source: `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/days/day103_non_canon.rpy:253`
- Label: `day103_1_optional_character_chain`
- Description: story.resolve_chain_label() creates dynamic chain target.
- Recommended owner: Chief Architect
- Recommended next action: Resolve dynamically in future simulator.

### gap_0016 - dynamic_jump_targets

- Source: `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/days/day103_non_canon.rpy:259`
- Label: `day103_1_optional_character_chain`
- Description: story.resolve_chain_label() creates dynamic chain target.
- Recommended owner: Chief Architect
- Recommended next action: Resolve dynamically in future simulator.

### gap_0034 - dynamic_jump_targets

- Source: `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/shared/story_chains_non_canon.rpy:61`
- Label: `advance_after_confrontation`
- Description: Dynamic jump target: _target[2].
- Recommended owner: Chief Architect
- Recommended next action: Confirm extractor/simulator can resolve this dynamic edge.

### gap_0036 - dynamic_jump_targets

- Source: `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/shared/story_chains_non_canon.rpy:818`
- Label: `end_slot`
- Description: Dynamic jump target: _target[2].
- Recommended owner: Chief Architect
- Recommended next action: Confirm extractor/simulator can resolve this dynamic edge.

## Gate Pass/Fail Ambiguity

No findings.

## Optional Chain Window Gaps

### gap_0021 - chain label has no explicit slot availability/window

- Source: `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/shared/story_chains_non_canon.rpy:69`
- Label: `stern_chain_1`
- Description: Phase 1 cannot infer appointment windows from chain labels alone.
- Recommended owner: Human Designer
- Recommended next action: Document slot availability or add DAG metadata.

### gap_0022 - chain label has no explicit slot availability/window

- Source: `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/shared/story_chains_non_canon.rpy:137`
- Label: `stern_chain_2`
- Description: Phase 1 cannot infer appointment windows from chain labels alone.
- Recommended owner: Human Designer
- Recommended next action: Document slot availability or add DAG metadata.

### gap_0023 - chain label has no explicit slot availability/window

- Source: `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/shared/story_chains_non_canon.rpy:202`
- Label: `stern_chain_3`
- Description: Phase 1 cannot infer appointment windows from chain labels alone.
- Recommended owner: Human Designer
- Recommended next action: Document slot availability or add DAG metadata.

### gap_0024 - chain label has no explicit slot availability/window

- Source: `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/shared/story_chains_non_canon.rpy:277`
- Label: `missy_chain_1`
- Description: Phase 1 cannot infer appointment windows from chain labels alone.
- Recommended owner: Human Designer
- Recommended next action: Document slot availability or add DAG metadata.

### gap_0025 - chain label has no explicit slot availability/window

- Source: `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/shared/story_chains_non_canon.rpy:342`
- Label: `missy_chain_2`
- Description: Phase 1 cannot infer appointment windows from chain labels alone.
- Recommended owner: Human Designer
- Recommended next action: Document slot availability or add DAG metadata.

### gap_0026 - chain label has no explicit slot availability/window

- Source: `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/shared/story_chains_non_canon.rpy:405`
- Label: `missy_chain_3`
- Description: Phase 1 cannot infer appointment windows from chain labels alone.
- Recommended owner: Human Designer
- Recommended next action: Document slot availability or add DAG metadata.

### gap_0027 - chain label has no explicit slot availability/window

- Source: `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/shared/story_chains_non_canon.rpy:478`
- Label: `vance_chain_1`
- Description: Phase 1 cannot infer appointment windows from chain labels alone.
- Recommended owner: Human Designer
- Recommended next action: Document slot availability or add DAG metadata.

### gap_0028 - chain label has no explicit slot availability/window

- Source: `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/shared/story_chains_non_canon.rpy:535`
- Label: `vance_chain_2`
- Description: Phase 1 cannot infer appointment windows from chain labels alone.
- Recommended owner: Human Designer
- Recommended next action: Document slot availability or add DAG metadata.

### gap_0029 - chain label has no explicit slot availability/window

- Source: `narrative/draft/releases/release-1-mvp/non_prod_renpy_project/game/shared/story_chains_non_canon.rpy:596`
- Label: `vance_chain_3`
- Description: Phase 1 cannot infer appointment windows from chain labels alone.
- Recommended owner: Human Designer
- Recommended next action: Document slot availability or add DAG metadata.

## Penance / Opportunity Cost Gaps

No findings.

## Storyboard Drift Notes

### gap_0050 - storyboard_label_missing_from_scripts

- Source: `narrative/draft/releases/release-1-mvp/planning/story_board.md:0`
- Label: `day101_4`
- Description: Storyboard references a label not extracted from scripts.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync or correct the storyboard reference.

### gap_0051 - storyboard_label_missing_from_scripts

- Source: `narrative/draft/releases/release-1-mvp/planning/story_board.md:0`
- Label: `day101_4_visit_missy`
- Description: Storyboard references a label not extracted from scripts.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync or correct the storyboard reference.

### gap_0052 - storyboard_label_missing_from_scripts

- Source: `narrative/draft/releases/release-1-mvp/planning/story_board.md:0`
- Label: `day101_4_writing_or_visiting`
- Description: Storyboard references a label not extracted from scripts.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync or correct the storyboard reference.

### gap_0053 - storyboard_label_missing_from_scripts

- Source: `narrative/draft/releases/release-1-mvp/planning/story_board.md:0`
- Label: `day102_non_canon`
- Description: Storyboard references a label not extracted from scripts.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync or correct the storyboard reference.

### gap_0054 - storyboard_label_missing_from_scripts

- Source: `narrative/draft/releases/release-1-mvp/planning/story_board.md:0`
- Label: `day104_6`
- Description: Storyboard references a label not extracted from scripts.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync or correct the storyboard reference.

### gap_0055 - storyboard_label_missing_from_scripts

- Source: `narrative/draft/releases/release-1-mvp/planning/story_board.md:0`
- Label: `day1_corridor_state`
- Description: Storyboard references a label not extracted from scripts.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync or correct the storyboard reference.

### gap_0056 - storyboard_label_missing_from_scripts

- Source: `narrative/draft/releases/release-1-mvp/planning/story_board.md:0`
- Label: `day1_interview_state`
- Description: Storyboard references a label not extracted from scripts.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync or correct the storyboard reference.

### gap_0057 - storyboard_label_missing_from_scripts

- Source: `narrative/draft/releases/release-1-mvp/planning/story_board.md:0`
- Label: `day1_ledger_focus`
- Description: Storyboard references a label not extracted from scripts.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync or correct the storyboard reference.

### gap_0058 - storyboard_label_missing_from_scripts

- Source: `narrative/draft/releases/release-1-mvp/planning/story_board.md:0`
- Label: `day2_chore_focus`
- Description: Storyboard references a label not extracted from scripts.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync or correct the storyboard reference.

### gap_0059 - storyboard_label_missing_from_scripts

- Source: `narrative/draft/releases/release-1-mvp/planning/story_board.md:0`
- Label: `day2_contraband_state`
- Description: Storyboard references a label not extracted from scripts.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync or correct the storyboard reference.

### gap_0060 - storyboard_label_missing_from_scripts

- Source: `narrative/draft/releases/release-1-mvp/planning/story_board.md:0`
- Label: `day2_tea_choice`
- Description: Storyboard references a label not extracted from scripts.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync or correct the storyboard reference.

### gap_0061 - storyboard_label_missing_from_scripts

- Source: `narrative/draft/releases/release-1-mvp/planning/story_board.md:0`
- Label: `day3_brush_choice`
- Description: Storyboard references a label not extracted from scripts.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync or correct the storyboard reference.

### gap_0062 - storyboard_label_missing_from_scripts

- Source: `narrative/draft/releases/release-1-mvp/planning/story_board.md:0`
- Label: `day3_corridor_chain`
- Description: Storyboard references a label not extracted from scripts.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync or correct the storyboard reference.

### gap_0063 - storyboard_label_missing_from_scripts

- Source: `narrative/draft/releases/release-1-mvp/planning/story_board.md:0`
- Label: `day3_ultimatum`
- Description: Storyboard references a label not extracted from scripts.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync or correct the storyboard reference.

### gap_0064 - storyboard_label_missing_from_scripts

- Source: `narrative/draft/releases/release-1-mvp/planning/story_board.md:0`
- Label: `day4_escape_state`
- Description: Storyboard references a label not extracted from scripts.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync or correct the storyboard reference.

### gap_0065 - storyboard_label_missing_from_scripts

- Source: `narrative/draft/releases/release-1-mvp/planning/story_board.md:0`
- Label: `day5_dynamic`
- Description: Storyboard references a label not extracted from scripts.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync or correct the storyboard reference.

### gap_0066 - storyboard_label_missing_from_scripts

- Source: `narrative/draft/releases/release-1-mvp/planning/story_board.md:0`
- Label: `game_over_deadline_1`
- Description: Storyboard references a label not extracted from scripts.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync or correct the storyboard reference.

### gap_0067 - storyboard_label_missing_from_scripts

- Source: `narrative/draft/releases/release-1-mvp/planning/story_board.md:0`
- Label: `game_over_deadline_2`
- Description: Storyboard references a label not extracted from scripts.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync or correct the storyboard reference.

### gap_0068 - storyboard_label_missing_from_scripts

- Source: `narrative/draft/releases/release-1-mvp/planning/story_board.md:0`
- Label: `game_over_dismissed`
- Description: Storyboard references a label not extracted from scripts.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync or correct the storyboard reference.

### gap_0069 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day100_2_desk_branch`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0070 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day100_2_parlour_branch`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0071 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day100_2_reconvergence`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0072 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day101_1_morning_interview`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0073 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day101_evening_consequence_window`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0074 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day101_night_story_window`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0075 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day102_1_cora_deceives_missy`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0076 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day102_1_missy_finds_a_thing`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0077 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day102_2_day2_corr_choice`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0078 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day102_2_day2_insp_choice`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0079 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day102_2_optional_character_chain`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0080 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day102_3_cora_confesses`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0081 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day102_3_cora_frames_missy`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0082 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day102_3_cora_pretends_to_find_it`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0083 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day102_3_vance_goes_incandescent`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0084 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day102_4_cora_sneaks_a_feel`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0085 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day102_afternoon_consequence_window`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0086 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day102_afternoon_story_window`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0087 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day102_night_consequence_window`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0088 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day103`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0089 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day103_1_corridor_corr_chain`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0090 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day103_1_corridor_insp_chain`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0091 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day103_1_optional_character_chain`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0092 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day103_2_cora_vs_gideon_corr`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0093 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day103_2_cora_vs_gideon_ghost`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0094 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day103_2_cora_vs_gideon_insp`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0095 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day103_2_night_bargain_gideon`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0096 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day103_2_night_defy_gideon`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0097 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day103_2_night_surrender_gideon`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0098 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day103_2_suite_cora_vs_gideon`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0099 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day103_3_frantic_write`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0100 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day103_3_indulge_words`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0101 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day103_3_prepare_mask`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0102 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day103_afternoon`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0103 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day103_evening`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0104 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day103_evening_consequence_window`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0105 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day103_morning_consequence_window`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0106 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day103_night`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0107 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day103_night_consequence_window`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0108 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day104`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0109 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day104_1_lockbox_evidence`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0110 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day104_2_escape_bold_lie`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0111 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day104_2_escape_fireplace`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0112 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day104_2_escape_missy_cover`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0113 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day104_4_atonement`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0114 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day104_4_missy_repair`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0115 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day104_evening`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0116 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day104_evening_consequence_window`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0117 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day104_morning`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0118 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day104_night`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0119 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day104_night_consequence_window`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0120 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day105_2_the_summons`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0121 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day105_4_motivation_ghost`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0122 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day105_4_motivation_observer`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0123 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day105_4_motivation_predator`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0124 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day105_4_motivation_prey`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

## Manual DAG Tags Preserved

No findings.
