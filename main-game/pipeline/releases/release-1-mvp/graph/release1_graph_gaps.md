# Release 1 Graph Gaps

## Missing DAG Tags

### gap_0007 - missing_dag_gate_tag

- Source: `main-game/non-prod-game/game/days/day102_non_canon.rpy:1020`
- Label: `day102_3_gideon_interrupts_controls_vance`
- Description: Flow-affecting condition has no DAG_GATE tag.
- Recommended owner: Create/Rewrite Day Workflow
- Recommended next action: Add DAG_GATE metadata if this gate is balancing-relevant.

### gap_0008 - missing_dag_gate_tag

- Source: `main-game/non-prod-game/game/days/day102_non_canon.rpy:1092`
- Label: `day102_4_cora_writes_a_chapter`
- Description: Flow-affecting condition has no DAG_GATE tag.
- Recommended owner: Create/Rewrite Day Workflow
- Recommended next action: Add DAG_GATE metadata if this gate is balancing-relevant.

### gap_0009 - missing_dag_gate_tag

- Source: `main-game/non-prod-game/game/days/day102_non_canon.rpy:1094`
- Label: `day102_4_cora_writes_a_chapter`
- Description: Flow-affecting condition has no DAG_GATE tag.
- Recommended owner: Create/Rewrite Day Workflow
- Recommended next action: Add DAG_GATE metadata if this gate is balancing-relevant.

### gap_0010 - missing_dag_gate_tag

- Source: `main-game/non-prod-game/game/days/day102_non_canon.rpy:1132`
- Label: `day102_4_cora_writes_a_chapter`
- Description: Flow-affecting condition has no DAG_GATE tag.
- Recommended owner: Create/Rewrite Day Workflow
- Recommended next action: Add DAG_GATE metadata if this gate is balancing-relevant.

### gap_0013 - missing_dag_gate_tag

- Source: `main-game/non-prod-game/game/days/day103_non_canon.rpy:53`
- Label: `day103_morning`
- Description: Flow-affecting condition has no DAG_GATE tag.
- Recommended owner: Create/Rewrite Day Workflow
- Recommended next action: Add DAG_GATE metadata if this gate is balancing-relevant.

### gap_0017 - missing_dag_gate_tag

- Source: `main-game/non-prod-game/game/days/day103_non_canon.rpy:1216`
- Label: `day103_3_bedroom_final_write`
- Description: Flow-affecting condition has no DAG_GATE tag.
- Recommended owner: Create/Rewrite Day Workflow
- Recommended next action: Add DAG_GATE metadata if this gate is balancing-relevant.

### gap_0018 - missing_dag_gate_tag

- Source: `main-game/non-prod-game/game/days/day104_non_canon.rpy:964`
- Label: `day104_6_false_dawn_ending`
- Description: Flow-affecting condition has no DAG_GATE tag.
- Recommended owner: Create/Rewrite Day Workflow
- Recommended next action: Add DAG_GATE metadata if this gate is balancing-relevant.

### gap_0019 - missing_dag_choice_tag

- Source: `main-game/non-prod-game/game/days/test_day2_writing_non_canon.rpy:26`
- Label: `test_day2_writing_harness`
- Description: Menu has no adjacent DAG_CHOICE tag.
- Recommended owner: Create/Rewrite Day Workflow
- Recommended next action: Add DAG_CHOICE beside the existing CHOICE marker.

### gap_0020 - missing_dag_gate_tag

- Source: `main-game/non-prod-game/game/shared/functions_non_canon.rpy:82`
- Label: `file`
- Description: Flow-affecting condition has no DAG_GATE tag.
- Recommended owner: Create/Rewrite Day Workflow
- Recommended next action: Add DAG_GATE metadata if this gate is balancing-relevant.

### gap_0030 - missing_dag_gate_tag

- Source: `main-game/non-prod-game/game/shared/story_chains_non_canon.rpy:26`
- Label: `check_confrontations`
- Description: Flow-affecting condition has no DAG_GATE tag.
- Recommended owner: Create/Rewrite Day Workflow
- Recommended next action: Add DAG_GATE metadata if this gate is balancing-relevant.

### gap_0031 - missing_dag_gate_tag

- Source: `main-game/non-prod-game/game/shared/story_chains_non_canon.rpy:33`
- Label: `check_confrontations`
- Description: Flow-affecting condition has no DAG_GATE tag.
- Recommended owner: Create/Rewrite Day Workflow
- Recommended next action: Add DAG_GATE metadata if this gate is balancing-relevant.

### gap_0032 - missing_dag_gate_tag

- Source: `main-game/non-prod-game/game/shared/story_chains_non_canon.rpy:37`
- Label: `check_confrontations`
- Description: Flow-affecting condition has no DAG_GATE tag.
- Recommended owner: Create/Rewrite Day Workflow
- Recommended next action: Add DAG_GATE metadata if this gate is balancing-relevant.

### gap_0033 - missing_dag_gate_tag

- Source: `main-game/non-prod-game/game/shared/story_chains_non_canon.rpy:41`
- Label: `check_confrontations`
- Description: Flow-affecting condition has no DAG_GATE tag.
- Recommended owner: Create/Rewrite Day Workflow
- Recommended next action: Add DAG_GATE metadata if this gate is balancing-relevant.

### gap_0035 - missing_dag_gate_tag

- Source: `main-game/non-prod-game/game/shared/story_chains_non_canon.rpy:797`
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

- Source: `main-game/non-prod-game/game/days/day102_non_canon.rpy:1185`
- Label: `day102_4_cora_sneaks_a_feel`
- Description: apply_effects() uses deprecated generic susp field.
- Recommended owner: Non-Prod Code Agent
- Recommended next action: Replace with character-specific suspicion field.

## Unmapped Effect Fields

### gap_0012 - unmapped_effect_fields

- Source: `main-game/non-prod-game/game/days/day102_non_canon.rpy:1185`
- Label: `day102_4_cora_sneaks_a_feel`
- Description: Unmapped apply_effects fields: susp.
- Recommended owner: Balancing Pass
- Recommended next action: Confirm runtime effect mapping.

## Router Outcome Mismatches

### gap_0037 - router_outcome_mismatches

- Source: `main-game/prod-game/game/classes.rpy:0`
- Label: `StoryState.SLOT_EXIT_ROUTES`
- Description: Outcome d1_reflect_done has no extracted call site.
- Recommended owner: Chief Architect
- Recommended next action: Confirm unused route is expected.

### gap_0038 - router_outcome_mismatches

- Source: `main-game/prod-game/game/classes.rpy:0`
- Label: `StoryState.SLOT_EXIT_ROUTES`
- Description: Outcome d1_write_ch1 has no extracted call site.
- Recommended owner: Chief Architect
- Recommended next action: Confirm unused route is expected.

### gap_0039 - router_outcome_mismatches

- Source: `main-game/prod-game/game/classes.rpy:0`
- Label: `StoryState.SLOT_EXIT_ROUTES`
- Description: Outcome d1_visit_missy has no extracted call site.
- Recommended owner: Chief Architect
- Recommended next action: Confirm unused route is expected.

### gap_0040 - router_outcome_mismatches

- Source: `main-game/prod-game/game/classes.rpy:0`
- Label: `StoryState.SLOT_EXIT_ROUTES`
- Description: Outcome d2_reflect_done has no extracted call site.
- Recommended owner: Chief Architect
- Recommended next action: Confirm unused route is expected.

### gap_0041 - router_outcome_mismatches

- Source: `main-game/prod-game/game/classes.rpy:0`
- Label: `StoryState.SLOT_EXIT_ROUTES`
- Description: Outcome d2_write_night has no extracted call site.
- Recommended owner: Chief Architect
- Recommended next action: Confirm unused route is expected.

### gap_0042 - router_outcome_mismatches

- Source: `main-game/prod-game/game/classes.rpy:0`
- Label: `StoryState.SLOT_EXIT_ROUTES`
- Description: Outcome d3_reflect_done has no extracted call site.
- Recommended owner: Chief Architect
- Recommended next action: Confirm unused route is expected.

### gap_0043 - router_outcome_mismatches

- Source: `main-game/prod-game/game/classes.rpy:0`
- Label: `StoryState.SLOT_EXIT_ROUTES`
- Description: Outcome d3_twilight_done has no extracted call site.
- Recommended owner: Chief Architect
- Recommended next action: Confirm unused route is expected.

### gap_0044 - router_outcome_mismatches

- Source: `main-game/prod-game/game/classes.rpy:0`
- Label: `StoryState.SLOT_EXIT_ROUTES`
- Description: Outcome d3_stern_done has no extracted call site.
- Recommended owner: Chief Architect
- Recommended next action: Confirm unused route is expected.

### gap_0045 - router_outcome_mismatches

- Source: `main-game/prod-game/game/classes.rpy:0`
- Label: `StoryState.SLOT_EXIT_ROUTES`
- Description: Outcome d3_ultimatum_done has no extracted call site.
- Recommended owner: Chief Architect
- Recommended next action: Confirm unused route is expected.

### gap_0046 - router_outcome_mismatches

- Source: `main-game/prod-game/game/classes.rpy:0`
- Label: `StoryState.SLOT_EXIT_ROUTES`
- Description: Outcome d3_write_night has no extracted call site.
- Recommended owner: Chief Architect
- Recommended next action: Confirm unused route is expected.

### gap_0047 - router_outcome_mismatches

- Source: `main-game/prod-game/game/classes.rpy:0`
- Label: `StoryState.SLOT_EXIT_ROUTES`
- Description: Outcome d4_write_night has no extracted call site.
- Recommended owner: Chief Architect
- Recommended next action: Confirm unused route is expected.

### gap_0048 - router_outcome_mismatches

- Source: `main-game/prod-game/game/classes.rpy:0`
- Label: `StoryState.SLOT_EXIT_ROUTES`
- Description: Outcome d4_dawn_gate has no extracted call site.
- Recommended owner: Chief Architect
- Recommended next action: Confirm unused route is expected.

### gap_0049 - router_outcome_mismatches

- Source: `main-game/prod-game/game/classes.rpy:0`
- Label: `StoryState.SLOT_EXIT_ROUTES`
- Description: Outcome d5_write_night has no extracted call site.
- Recommended owner: Chief Architect
- Recommended next action: Confirm unused route is expected.

## Dynamic Jump Targets

### gap_0001 - dynamic_jump_targets

- Source: `main-game/non-prod-game/game/days/day101_non_canon.rpy:630`
- Label: `day101_night_story_window`
- Description: story.resolve_chain_label() creates dynamic chain target.
- Recommended owner: Chief Architect
- Recommended next action: Resolve dynamically in future simulator.

### gap_0002 - dynamic_jump_targets

- Source: `main-game/non-prod-game/game/days/day101_non_canon.rpy:636`
- Label: `day101_night_story_window`
- Description: story.resolve_chain_label() creates dynamic chain target.
- Recommended owner: Chief Architect
- Recommended next action: Resolve dynamically in future simulator.

### gap_0003 - dynamic_jump_targets

- Source: `main-game/non-prod-game/game/days/day101_non_canon.rpy:642`
- Label: `day101_night_story_window`
- Description: story.resolve_chain_label() creates dynamic chain target.
- Recommended owner: Chief Architect
- Recommended next action: Resolve dynamically in future simulator.

### gap_0004 - dynamic_jump_targets

- Source: `main-game/non-prod-game/game/days/day102_non_canon.rpy:420`
- Label: `day102_afternoon_story_window`
- Description: story.resolve_chain_label() creates dynamic chain target.
- Recommended owner: Chief Architect
- Recommended next action: Resolve dynamically in future simulator.

### gap_0005 - dynamic_jump_targets

- Source: `main-game/non-prod-game/game/days/day102_non_canon.rpy:426`
- Label: `day102_afternoon_story_window`
- Description: story.resolve_chain_label() creates dynamic chain target.
- Recommended owner: Chief Architect
- Recommended next action: Resolve dynamically in future simulator.

### gap_0006 - dynamic_jump_targets

- Source: `main-game/non-prod-game/game/days/day102_non_canon.rpy:432`
- Label: `day102_afternoon_story_window`
- Description: story.resolve_chain_label() creates dynamic chain target.
- Recommended owner: Chief Architect
- Recommended next action: Resolve dynamically in future simulator.

### gap_0014 - dynamic_jump_targets

- Source: `main-game/non-prod-game/game/days/day103_non_canon.rpy:244`
- Label: `day103_1_optional_character_chain`
- Description: story.resolve_chain_label() creates dynamic chain target.
- Recommended owner: Chief Architect
- Recommended next action: Resolve dynamically in future simulator.

### gap_0015 - dynamic_jump_targets

- Source: `main-game/non-prod-game/game/days/day103_non_canon.rpy:250`
- Label: `day103_1_optional_character_chain`
- Description: story.resolve_chain_label() creates dynamic chain target.
- Recommended owner: Chief Architect
- Recommended next action: Resolve dynamically in future simulator.

### gap_0016 - dynamic_jump_targets

- Source: `main-game/non-prod-game/game/days/day103_non_canon.rpy:256`
- Label: `day103_1_optional_character_chain`
- Description: story.resolve_chain_label() creates dynamic chain target.
- Recommended owner: Chief Architect
- Recommended next action: Resolve dynamically in future simulator.

### gap_0034 - dynamic_jump_targets

- Source: `main-game/non-prod-game/game/shared/story_chains_non_canon.rpy:61`
- Label: `advance_after_confrontation`
- Description: Dynamic jump target: _target[2].
- Recommended owner: Chief Architect
- Recommended next action: Confirm extractor/simulator can resolve this dynamic edge.

### gap_0036 - dynamic_jump_targets

- Source: `main-game/non-prod-game/game/shared/story_chains_non_canon.rpy:818`
- Label: `end_slot`
- Description: Dynamic jump target: _target[2].
- Recommended owner: Chief Architect
- Recommended next action: Confirm extractor/simulator can resolve this dynamic edge.

## Gate Pass/Fail Ambiguity

No findings.

## Optional Chain Window Gaps

### gap_0021 - chain label has no explicit slot availability/window

- Source: `main-game/non-prod-game/game/shared/story_chains_non_canon.rpy:69`
- Label: `stern_chain_1`
- Description: Phase 1 cannot infer appointment windows from chain labels alone.
- Recommended owner: Human Designer
- Recommended next action: Document slot availability or add DAG metadata.

### gap_0022 - chain label has no explicit slot availability/window

- Source: `main-game/non-prod-game/game/shared/story_chains_non_canon.rpy:137`
- Label: `stern_chain_2`
- Description: Phase 1 cannot infer appointment windows from chain labels alone.
- Recommended owner: Human Designer
- Recommended next action: Document slot availability or add DAG metadata.

### gap_0023 - chain label has no explicit slot availability/window

- Source: `main-game/non-prod-game/game/shared/story_chains_non_canon.rpy:202`
- Label: `stern_chain_3`
- Description: Phase 1 cannot infer appointment windows from chain labels alone.
- Recommended owner: Human Designer
- Recommended next action: Document slot availability or add DAG metadata.

### gap_0024 - chain label has no explicit slot availability/window

- Source: `main-game/non-prod-game/game/shared/story_chains_non_canon.rpy:277`
- Label: `missy_chain_1`
- Description: Phase 1 cannot infer appointment windows from chain labels alone.
- Recommended owner: Human Designer
- Recommended next action: Document slot availability or add DAG metadata.

### gap_0025 - chain label has no explicit slot availability/window

- Source: `main-game/non-prod-game/game/shared/story_chains_non_canon.rpy:342`
- Label: `missy_chain_2`
- Description: Phase 1 cannot infer appointment windows from chain labels alone.
- Recommended owner: Human Designer
- Recommended next action: Document slot availability or add DAG metadata.

### gap_0026 - chain label has no explicit slot availability/window

- Source: `main-game/non-prod-game/game/shared/story_chains_non_canon.rpy:405`
- Label: `missy_chain_3`
- Description: Phase 1 cannot infer appointment windows from chain labels alone.
- Recommended owner: Human Designer
- Recommended next action: Document slot availability or add DAG metadata.

### gap_0027 - chain label has no explicit slot availability/window

- Source: `main-game/non-prod-game/game/shared/story_chains_non_canon.rpy:478`
- Label: `vance_chain_1`
- Description: Phase 1 cannot infer appointment windows from chain labels alone.
- Recommended owner: Human Designer
- Recommended next action: Document slot availability or add DAG metadata.

### gap_0028 - chain label has no explicit slot availability/window

- Source: `main-game/non-prod-game/game/shared/story_chains_non_canon.rpy:535`
- Label: `vance_chain_2`
- Description: Phase 1 cannot infer appointment windows from chain labels alone.
- Recommended owner: Human Designer
- Recommended next action: Document slot availability or add DAG metadata.

### gap_0029 - chain label has no explicit slot availability/window

- Source: `main-game/non-prod-game/game/shared/story_chains_non_canon.rpy:596`
- Label: `vance_chain_3`
- Description: Phase 1 cannot infer appointment windows from chain labels alone.
- Recommended owner: Human Designer
- Recommended next action: Document slot availability or add DAG metadata.

## Penance / Opportunity Cost Gaps

No findings.

## Storyboard Drift Notes

### gap_0050 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day100_2_desk_branch`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0051 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day100_2_parlour_branch`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0052 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day100_2_reconvergence`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0053 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day102_2_day2_corr_choice`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0054 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day102_2_day2_insp_choice`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0055 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day102_3_cora_confesses`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0056 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day102_3_cora_frames_missy`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0057 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day102_3_cora_pretends_to_find_it`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0058 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day103`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0059 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day103_1_corridor_corr_chain`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0060 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day103_1_corridor_insp_chain`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0061 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day103_2_cora_vs_gideon_corr`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0062 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day103_2_cora_vs_gideon_ghost`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0063 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day103_2_cora_vs_gideon_insp`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0064 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day103_2_night_bargain_gideon`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0065 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day103_2_night_defy_gideon`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0066 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day103_2_night_surrender_gideon`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0067 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day103_2_suite_cora_vs_gideon`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0068 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day103_3_frantic_write`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0069 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day103_3_indulge_words`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0070 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day103_3_prepare_mask`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0071 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day104_1`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0072 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day104_2_escape_bold_lie`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0073 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day104_2_escape_fireplace`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0074 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day104_2_escape_missy_cover`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0075 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day104_4_atonement`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0076 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day104_4_missy_repair`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0077 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day105_2_the_summons`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0078 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day105_4_motivation_ghost`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0079 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day105_4_motivation_observer`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0080 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day105_4_motivation_predator`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

### gap_0081 - script_label_missing_from_storyboard

- Source: `n/a:0`
- Label: `day105_4_motivation_prey`
- Description: Script label not referenced in storyboard.
- Recommended owner: Documentation Steward
- Recommended next action: Run storyboard_sync if this label is planning-relevant.

## Manual DAG Tags Preserved

No findings.
