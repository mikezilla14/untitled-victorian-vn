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

# [DAG_NODE id=book1_block_day1_slop_core type=write]
label book1_block_day1_slop_core:

    call book1_nvl_write_line("Draft Fragment - Unsellable Night Pages", word_delay=_book1_word_delay)
    call book1_nvl_write_line("Coralie tries to restage the corridor scandal at Ravenshade Conservatory, but every sentence arrives scrubbed and timid.", word_delay=_book1_word_delay)
    call book1_nvl_write_line("Lord Caldor becomes vague menace, Lady Vayne becomes posture without hunger, and Mr. Sterick reads like a wax seal with no heat behind it.", word_delay=_book1_word_delay)
    call book1_nvl_write_line("Miri's fear is flattened into polite summary, as if danger can be made respectable by removing all appetite from the telling.", word_delay=_book1_word_delay)
    call book1_nvl_write_line("The result is technically clean and emotionally vacant - a manuscript page that sounds safe, market-proof, and dead on arrival.", word_delay=_book1_word_delay)
    return


# [DAG_NODE id=book1_block_day1_default_core type=write]
label book1_block_day1_default_core:

    call book1_block_day1_common_open
    return


# [DAG_NODE id=book1_block_day1_ghost_core type=write]
label book1_block_day1_ghost_core:

    call book1_block_day1_common_open
    call book1_nvl_write_line("The narration stays observational, dispassionate, and evidentiary; desire is implied through omission, not declaration.", word_delay=_book1_word_delay)
    if story.day1_ledger_focus == "inspiration":
        call book1_nvl_write_line("Each chapter tracks who paid the cost rather than who won the room.", word_delay=_book1_word_delay)
    return


# [DAG_NODE id=book1_block_day1_predator_core type=write]
label book1_block_day1_predator_core:

    call book1_block_day1_common_open
    call book1_nvl_write_line("The narration is deliberate and tactical; heat appears as leverage, never as surrender.", word_delay=_book1_word_delay)
    if story.day1_ledger_focus == "corruption":
        call book1_nvl_write_line("Polished etiquette carries a visible edge.", word_delay=_book1_word_delay)
    return


# [DAG_NODE id=book1_block_day1_prey_core type=write]
label book1_block_day1_prey_core:

    call book1_block_day1_common_open
    call book1_nvl_write_line("The narration is intimate and exposed; attraction and risk are allowed to coexist without tidy absolution.", word_delay=_book1_word_delay)
    call book1_nvl_write_line("Curiosity is framed as both hunger and hazard.", word_delay=_book1_word_delay)
    return


# [DAG_NODE id=book1_block_day1_common_open type=write]
label book1_block_day1_common_open:

    call book1_nvl_write_line("At Ravenshade Conservatory, Coralie Vale learns that service is theater and every corridor has an audience.", word_delay=_book1_word_delay)
    call book1_nvl_write_line("She studies Lady Vayne's posture, Mr. Sterick's clipped authority, and the predatory stillness of Lord Caldor.", word_delay=_book1_word_delay)
    call book1_nvl_write_line("The scandal behind the music room door becomes her first private map of power.", word_delay=_book1_word_delay)
    return


# [DAG_NODE id=book1_block_day1_ghost_subservient type=write]
label book1_block_day1_ghost_subservient:

    call book1_block_day1_common_open
    call book1_nvl_write_line("In the draft, Coralie stands like marble under Lady Vayne's critical gaze, yet her thoughts run feverish. She transposes the housekeeper's stiff threat into a dance of silent surrender.", word_delay=_book1_word_delay)
    call book1_nvl_write_line("Miri's submissive posture is written with thick, liquid ink—a girl who has learned to find a quiet pleasure in being shaped by a stronger hand.", word_delay=_book1_word_delay)
    if story.day1_ledger_focus == "inspiration":
        call book1_nvl_write_line("She writes of the invisible observer, who sees all because she claims to feel nothing at all.", word_delay=_book1_word_delay)
    return


# [DAG_NODE id=book1_block_day1_predator_complicit type=write]
label book1_block_day1_predator_complicit:

    call book1_block_day1_common_open
    call book1_nvl_write_line("On these pages, the relationship between the governess and Coralie is charged with a dangerous, shared guilt. The governess adjusts her collar, and the touch is described as a brand.", word_delay=_book1_word_delay)
    call book1_nvl_write_line("The narrative is sharp and heavy with complicity; they are not mistress and servant, but two conspirators measuring each other's appetite in the dark.", word_delay=_book1_word_delay)
    if story.day1_ledger_focus == "corruption":
        call book1_nvl_write_line("Every gesture is a barter, every look a silent pact between two women who both plan to consume the house.", word_delay=_book1_word_delay)
    return


# [DAG_NODE id=book1_block_day1_prey_resistant type=write]
label book1_block_day1_prey_resistant:

    call book1_block_day1_common_open
    call book1_nvl_write_line("Coralie's resistance is written as a trembling, wild thing. When the housekeeper draws near, she flinches, yet her diary catches the heat of the encounter.", word_delay=_book1_word_delay)
    call book1_nvl_write_line("She writes of a bird that beats against the cage, not to escape, but because the bars themselves are warm. Desire and danger are bound in the same lock.", word_delay=_book1_word_delay)
    return


