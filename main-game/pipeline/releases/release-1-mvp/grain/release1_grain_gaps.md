# Release 1 Grain Gaps

- Release: `release-1-mvp`
- Grains extracted: 237
- Gaps found: 8

## Blockers

No findings.

## Major

### grain_gap_0001 — untagged_balance_gate

- Severity: **major**
- Source: `main-game/non-prod-game/game/days/day102_non_canon.rpy:1023`
- Label: `day102_3_gideon_interrupts_controls_vance`
- Description: Balancing gate without DAG_GATE tag: `story.manuscript_progress == 0`.
- Owner: Grain Tagger
- Next action: Add DAG_GATE above the if/elif once grain id is stable.

### grain_gap_0002 — untagged_balance_gate

- Severity: **major**
- Source: `main-game/non-prod-game/game/days/day102_non_canon.rpy:1088`
- Label: `day102_4_cora_writes_a_chapter`
- Description: Balancing gate without DAG_GATE tag: `story.manuscript_progress == 0`.
- Owner: Grain Tagger
- Next action: Add DAG_GATE above the if/elif once grain id is stable.

### grain_gap_0003 — untagged_balance_gate

- Severity: **major**
- Source: `main-game/non-prod-game/game/days/day102_non_canon.rpy:1090`
- Label: `day102_4_cora_writes_a_chapter`
- Description: Balancing gate without DAG_GATE tag: `has_story_fuel(*WRITE_GATE_CH1)`.
- Owner: Grain Tagger
- Next action: Add DAG_GATE above the if/elif once grain id is stable.

### grain_gap_0004 — untagged_balance_gate

- Severity: **major**
- Source: `main-game/non-prod-game/game/days/day102_non_canon.rpy:1128`
- Label: `day102_4_cora_writes_a_chapter`
- Description: Balancing gate without DAG_GATE tag: `has_story_fuel(*WRITE_GATE_CH2)`.
- Owner: Grain Tagger
- Next action: Add DAG_GATE above the if/elif once grain id is stable.

### grain_gap_0001 — untagged_balance_gate

- Severity: **major**
- Source: `main-game/non-prod-game/game/days/day103_non_canon.rpy:53`
- Label: `day103_morning`
- Description: Balancing gate without DAG_GATE tag: `story.manuscript_progress == 0`.
- Owner: Grain Tagger
- Next action: Add DAG_GATE above the if/elif once grain id is stable.

### grain_gap_0002 — untagged_balance_gate

- Severity: **major**
- Source: `main-game/non-prod-game/game/days/day103_non_canon.rpy:1203`
- Label: `day103_3_bedroom_final_write`
- Description: Balancing gate without DAG_GATE tag: `has_story_fuel(*WRITE_GATE_CH3) or story.day3_twilight_action == "frantic_write"`.
- Owner: Grain Tagger
- Next action: Add DAG_GATE above the if/elif once grain id is stable.

### grain_gap_0001 — untagged_balance_gate

- Severity: **major**
- Source: `main-game/non-prod-game/game/days/day104_non_canon.rpy:960`
- Label: `day104_6_false_dawn_ending`
- Description: Balancing gate without DAG_GATE tag: `story.manuscript_progress < 2`.
- Owner: Grain Tagger
- Next action: Add DAG_GATE above the if/elif once grain id is stable.

### grain_gap_0001 — untagged_balance_gate

- Severity: **major**
- Source: `main-game/non-prod-game/game/days/day105_non_canon.rpy:756`
- Label: `day105_6_manuscript_reckoning`
- Description: Balancing gate without DAG_GATE tag: `player.corruption_level < WRITE_GATE_CH2[1]`.
- Owner: Grain Tagger
- Next action: Add DAG_GATE above the if/elif once grain id is stable.

## Warnings

No findings.
