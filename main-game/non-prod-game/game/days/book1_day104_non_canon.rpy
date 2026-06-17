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

# [DAG_NODE id=book1_block_day4_default_core type=write]
label book1_block_day4_default_core:

    call book1_block_day4_common_open
    call book1_block_day4_moral_frame
    call book1_block_day4_missy_debt_or_repair
    call book1_block_day4_stern_pressure
    call book1_block_day4_writing_cadence
    call book1_block_day4_escape_and_evidence
    return


# [DAG_NODE id=book1_block_day4_ghost_core type=write]
label book1_block_day4_ghost_core:

    call book1_block_day4_common_open
    call book1_nvl_write_line("The narration stays observational, dispassionate, and evidentiary; desire is implied through omission, not declaration.", word_delay=_book1_word_delay)
    call book1_block_day4_moral_frame
    call book1_block_day4_missy_debt_or_repair
    call book1_block_day4_stern_pressure
    call book1_block_day4_writing_cadence
    call book1_block_day4_escape_and_evidence
    return


# [DAG_NODE id=book1_block_day4_predator_core type=write]
label book1_block_day4_predator_core:

    call book1_block_day4_common_open
    call book1_nvl_write_line("The narration is deliberate and tactical; heat appears as leverage, never as surrender.", word_delay=_book1_word_delay)
    call book1_block_day4_moral_frame
    call book1_block_day4_missy_debt_or_repair
    call book1_block_day4_stern_pressure
    call book1_block_day4_writing_cadence
    call book1_block_day4_escape_and_evidence
    return


# [DAG_NODE id=book1_block_day4_prey_core type=write]
label book1_block_day4_prey_core:

    call book1_block_day4_common_open
    call book1_nvl_write_line("The narration is intimate and exposed; attraction and risk are allowed to coexist without tidy absolution.", word_delay=_book1_word_delay)
    call book1_block_day4_moral_frame
    call book1_block_day4_missy_debt_or_repair
    call book1_block_day4_stern_pressure
    call book1_block_day4_writing_cadence
    call book1_block_day4_escape_and_evidence
    return


# [DAG_NODE id=book1_block_day4_common_open type=write]
label book1_block_day4_common_open:

    call book1_nvl_write_line("A hidden photograph becomes a coded sketch in the conservatory ledger, enough to threaten a lord without naming him.", word_delay=_book1_word_delay)
    call book1_nvl_write_line("Coralie drafts a false victory in which the heroine traps her patron using impeccable manners and one precise secret.", word_delay=_book1_word_delay)
    call book1_nvl_write_line("The chapter glows with triumph while quietly admitting the danger is merely sleeping.", word_delay=_book1_word_delay)
    return


# [DAG_NODE id=book1_block_day4_moral_frame type=write]
label book1_block_day4_moral_frame:

    if story.day1_corridor_state == "ghost" and story.day1_ledger_focus == "inspiration":
        call book1_nvl_write_line("Each chapter tracks who paid the cost rather than who won the room.", word_delay=_book1_word_delay)
    elif story.day1_corridor_state == "predator" and story.day1_ledger_focus == "corruption":
        call book1_nvl_write_line("Polished etiquette carries a visible edge.", word_delay=_book1_word_delay)
    elif story.day1_corridor_state == "prey":
        call book1_nvl_write_line("Curiosity is framed as both hunger and hazard.", word_delay=_book1_word_delay)
    return


# [DAG_NODE id=book1_block_day4_missy_debt_or_repair type=write]
label book1_block_day4_missy_debt_or_repair:

    if story.missy_day2_trust_break or story.missy_day4_used_as_cover:
        call book1_nvl_write_line("Miri is written as a courier who trusted the wrong corridor map, and Coralie keeps the betrayal visible.", word_delay=_book1_word_delay)
        call book1_nvl_write_line("The scene does not absolve her; it records the debt like a stain that cannot be laundered out.", word_delay=_book1_word_delay)
    else:
        call book1_nvl_write_line("Miri becomes a distant apprentice, cautious but present, and Coralie writes her with earned restraint.", word_delay=_book1_word_delay)
        call book1_nvl_write_line("The page allows partial repair, but never pretends innocence returned unchanged.", word_delay=_book1_word_delay)
    return


# [DAG_NODE id=book1_block_day4_stern_pressure type=write]
label book1_block_day4_stern_pressure:

    if story.missy_day2_suspicion_state == "uneasy" or story.day4_stern_response == "missy_cover":
        call book1_nvl_write_line("Mr. Sterick interrogates Miri first, because hierarchy makes her easier to bruise in public.", word_delay=_book1_word_delay)
        call book1_nvl_write_line("Coralie notes how authority can sound procedural while functioning as punishment.", word_delay=_book1_word_delay)
    else:
        call book1_nvl_write_line("Mr. Sterick keeps the reprimand diffuse, but Miri still absorbs most of the room's panic.", word_delay=_book1_word_delay)
        call book1_nvl_write_line("Coralie records the moment as proof that class discipline rarely needs raised volume.", word_delay=_book1_word_delay)
    return


# [DAG_NODE id=book1_block_day4_writing_cadence type=write]
label book1_block_day4_writing_cadence:

    if story.day4_night_action == "finish_manuscript":
        call book1_nvl_write_line("Coralie writes as if dawn will confiscate the pages, every paragraph urgent and thin-breathed.", word_delay=_book1_word_delay)
        call book1_nvl_write_line("The prose runs hot with pursuit, turning fear into velocity.", word_delay=_book1_word_delay)
    else:
        call book1_nvl_write_line("Coralie writes slowly, pressing each sentence into structure before allowing heat to bloom.", word_delay=_book1_word_delay)
        call book1_nvl_write_line("The prose keeps its pulse but favors control over panic.", word_delay=_book1_word_delay)
    return


# [DAG_NODE id=book1_block_day4_escape_and_evidence type=write]
label book1_block_day4_escape_and_evidence:

    if story.day4_escape_state == "missy_cover" or story.missy_day4_used_as_cover:
        call book1_nvl_write_line("Coralie survives by spending Miri's credibility, and the chapter refuses to romanticize that exchange.", word_delay=_book1_word_delay)
    if story.has_photograph or story.day4_evidence_discovered:
        call book1_nvl_write_line("The hidden photograph becomes a ledger cipher, reframing fear as admissible leverage.", word_delay=_book1_word_delay)
    return


