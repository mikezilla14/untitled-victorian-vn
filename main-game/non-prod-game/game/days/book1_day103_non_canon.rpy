# FORMAT LEGEND:
# [ASSET] -> backgrounds, sprites, transitions, CG/UI callouts
# [STATE] -> variable changes, effects, conditions, jumps
# [CHOICE] -> menu blocks and inflection points
# [BEAT] -> narrative intent / scene intent notes
#
# SPRITE DIRECTION (managed by scripts/scene_direction.py — how to preserve manual staging):
# [asset auto]              -> auto-placed sprite line; the agent may rewrite/replace it on re-run
# [asset keep]              -> on a show line: lock THAT line so the agent never edits it
# [asset lock:scene]        -> before/after a `scene`: the agent skips the entire scene block
# [asset pin:Name=slot]     -> force Name into slot for the rest of the scene block
# [enter:Name] / [exit:Name] -> declare cast changes so auto placement stays correct
# Full policy: docs/contracts/sprite_layout_policy.yaml | spec: docs/specs/scene-direction-agent.md

# [DAG_NODE id=book1_block_day3_default_core type=write]
label book1_block_day3_default_core:

    call book1_block_day3_common_open
    call book1_block_day3_ultimatum_beat
    call book1_block_day3_writing_cadence
    call book1_block_day3_stern_beat
    call book1_block_day3_furnace_beat
    return


# [DAG_NODE id=book1_block_day3_ghost_core type=write]
label book1_block_day3_ghost_core:

    call book1_block_day3_common_open
    call book1_nvl_write_line("The narration stays observational, dispassionate, and evidentiary; desire is implied through omission, not declaration.", word_delay=_book1_word_delay)
    if story.day1_ledger_focus == "inspiration":
        call book1_nvl_write_line("Each chapter tracks who paid the cost rather than who won the room.", word_delay=_book1_word_delay)
    call book1_block_day3_ultimatum_beat
    call book1_block_day3_writing_cadence
    call book1_block_day3_stern_beat
    call book1_block_day3_furnace_beat
    return


# [DAG_NODE id=book1_block_day3_predator_core type=write]
label book1_block_day3_predator_core:

    call book1_block_day3_common_open
    call book1_nvl_write_line("The narration is deliberate and tactical; heat appears as leverage, never as surrender.", word_delay=_book1_word_delay)
    if story.day1_ledger_focus == "corruption":
        call book1_nvl_write_line("Polished etiquette carries a visible edge.", word_delay=_book1_word_delay)
    call book1_block_day3_ultimatum_beat
    call book1_block_day3_writing_cadence
    call book1_block_day3_stern_beat
    call book1_block_day3_furnace_beat
    return


# [DAG_NODE id=book1_block_day3_prey_core type=write]
label book1_block_day3_prey_core:

    call book1_block_day3_common_open
    call book1_nvl_write_line("The narration is intimate and exposed; attraction and risk are allowed to coexist without tidy absolution.", word_delay=_book1_word_delay)
    if story.day3_twilight_action == "prepare_mask":
        call book1_nvl_write_line("Outward compliance shelters inward escalation.", word_delay=_book1_word_delay)
    call book1_block_day3_ultimatum_beat
    call book1_block_day3_writing_cadence
    call book1_block_day3_stern_beat
    call book1_block_day3_furnace_beat
    return


# [DAG_NODE id=book1_block_day3_common_open type=write]
label book1_block_day3_common_open:

    call book1_nvl_write_line("By twilight rehearsal, Lord Caldor's attention feels less like patronage and more like choreography.", word_delay=_book1_word_delay)
    call book1_nvl_write_line("Coralie stages mirror, brush, and breath as evidence, knowing witnesses can become accomplices by standing still.", word_delay=_book1_word_delay)
    call book1_nvl_write_line("Every line she writes asks whether danger is a place, a person, or a desire she cannot dismiss.", word_delay=_book1_word_delay)
    return


# [DAG_NODE id=book1_block_day3_ultimatum_beat type=write]
label book1_block_day3_ultimatum_beat:

    if story.day3_ultimatum == "defied":
        call book1_nvl_write_line("Lord Caldor corners the heroine by the furnace doors, offering terms in a velvet voice.", word_delay=_book1_word_delay)
        call book1_nvl_write_line("She answers with refusal sharpened into etiquette, making defiance feel like a ceremonial blade.", word_delay=_book1_word_delay)
        call book1_nvl_write_line("The chapter refuses euphemism and keeps the moral cost visible.", word_delay=_book1_word_delay)
    elif story.day3_ultimatum == "surrendered":
        call book1_nvl_write_line("Lord Caldor corners the heroine by the furnace doors, but this time consent is staged as survival arithmetic.", word_delay=_book1_word_delay)
        call book1_nvl_write_line("The chapter acknowledges how surrender can be chosen and still feel perilously close to coercion.", word_delay=_book1_word_delay)
        call book1_nvl_write_line("The chapter refuses euphemism and keeps the moral cost visible.", word_delay=_book1_word_delay)
    return


# [DAG_NODE id=book1_block_day3_writing_cadence type=write]
label book1_block_day3_writing_cadence:

    if story.day3_twilight_action == "frantic_write":
        call book1_nvl_write_line("Coralie writes as if dawn will confiscate the pages, every paragraph urgent and thin-breathed.", word_delay=_book1_word_delay)
        call book1_nvl_write_line("The prose runs hot with pursuit, turning fear into velocity.", word_delay=_book1_word_delay)
    else:
        call book1_nvl_write_line("Coralie writes slowly, pressing each sentence into structure before allowing heat to bloom.", word_delay=_book1_word_delay)
        call book1_nvl_write_line("The prose keeps its pulse but favors control over panic.", word_delay=_book1_word_delay)
    return


# [DAG_NODE id=book1_block_day3_stern_beat type=write]
label book1_block_day3_stern_beat:

    if story.day3_stern_response == "stupid" or story.day3_stern_response == "partial_truth":
        call book1_nvl_write_line("Mr. Sterick drills Coralie on silence and timing, turning etiquette into an instrument of surveillance.", word_delay=_book1_word_delay)
    return


# [DAG_NODE id=book1_block_day3_furnace_beat type=write]
label book1_block_day3_furnace_beat:

    if story.day3_ultimatum == "defied" or story.day3_ultimatum == "surrendered" or story.day3_ultimatum == "bargained":
        call book1_nvl_write_line("The furnace-room ultimatum is rewritten as social choreography where terms, not touches, decide the temperature.", word_delay=_book1_word_delay)
    return


