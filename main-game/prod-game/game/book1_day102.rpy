# [DAG_NODE id=book1_block_day2_ghost_core type=write]
label book1_block_day2_ghost_core:

    call book1_nvl_write_line("Chapter the Second opens upon a lady's hatbox in the conservatory suite, sealed like a coffin for silk and scandal.", word_delay=_book1_word_delay)
    call book1_nvl_write_line("The tea service steams; every cup rings as if the house itself were counting who shall be ruined before the cakes grow cold.", word_delay=_book1_word_delay)
    call book1_nvl_write_line("Coralie does not touch the lid. She watches instead: Lady Vayne's lacquered fury, Lord Caldor's patient shadow, Mr. Sterick's iron courtesy sharpening into a blade.", word_delay=_book1_word_delay)
    call book1_nvl_write_line("When the missing under-linen is demanded, Coralie names no one — and lets the silence appoint its victim.", word_delay=_book1_word_delay)
    call book1_nvl_write_line("Her pen makes Miri the chapter's sacrifice — courier, confidante, fool — while Coralie's cuffs remain immaculate and her conscience a blank ledger sheet.", word_delay=_book1_word_delay)
    call book1_nvl_write_line("Betrayal, written for the stalls, sounds less like shouting than paper slid under a door that will not open again.", word_delay=_book1_word_delay)

    if story.day1_ledger_focus == "inspiration":
        call book1_nvl_write_line("Each paragraph records who paid the reckoning, not who won the salon.", word_delay=_book1_word_delay)

    call book1_block_day2_missy_debt_or_repair
    call book1_block_day2_stern_suspicion_or_diffuse
    call book1_block_day2_contraband_state
    call book1_block_day2_stern_pressure_if_needed

    return


# [DAG_NODE id=book1_block_day2_predator_core type=write]
label book1_block_day2_predator_core:

    # Route-provenance cue — must appear within the first screen.
    call book1_set_chapter_title(
        title="CHAPTER THE SECOND",
        subtitle="Derived from a Night of Contraband"
    )

    call book1_write_beat(
        "Chapter the Second opens upon a lady's hatbox in the conservatory suite, sealed like a coffin for silk and scandal.",
        thought="Too neat. She would not remember it so cleanly.",
        page_break=True
    )

    call book1_write_beat(
        "The tea service steams; every cup rings as if the house itself were counting who shall be ruined before the cakes grow cold.",
        thought="Not listened. Witnessed."
    )

    call book1_write_beat(
        "Coralie crosses the salon with helpful hands and a voice trained to rescue propriety from its own carelessness.",
        thought="Rescue is the oldest word for acquisition."
    )

    # Falls back to ui_book_cover until the asset is assembled.
    call book1_show_tableau("cg_book_d2_hatbox_tableau")

    call book1_write_beat(
        "She lifts the lace as though innocence were a thing one could hold by two fingers, and the room admires her lie the way great houses admire plausible furnishings."
    )

    call book1_write_beat(
        "Her pen crowns her the heroine who saved a great lady's honour from sloven packing and worse appetites; even Lord Caldor's stillness seems, by the final stanza, almost courtly.",
        thought="There. Let the lie wear gloves."
    )

    # Tentpole override: book1_show_plate("plate_book_d2_hatbox_curse", caption="...")
    call book1_show_plate(caption="Plate II — The Hatbox Curse")

    call book1_write_beat(
        "Desire in these pages is never surrender but upholstery — something guests lean upon while arranging whom to ruin next.",
        thought="The reader is meant to blush. Then turn the page anyway.",
        clear_thought=True
    )

    if story.day1_ledger_focus == "corruption":
        call book1_write_beat(
            "Etiquette wears a jewelled edge; appetite arrives as garnish upon a blade already drawn."
        )

    call book1_block_day2_missy_debt_or_repair
    call book1_block_day2_stern_suspicion_or_diffuse
    call book1_block_day2_contraband_state
    call book1_block_day2_stern_pressure_if_needed

    return


# [DAG_NODE id=book1_block_day2_prey_core type=write]
label book1_block_day2_prey_core:

    call book1_nvl_write_line("Chapter the Second opens upon a lady's hatbox in the conservatory suite, sealed like a coffin for silk and scandal.", word_delay=_book1_word_delay)
    call book1_nvl_write_line("The tea service steams; every cup rings as if the house itself were counting who shall be ruined before the cakes grow cold.", word_delay=_book1_word_delay)
    call book1_nvl_write_line("Coralie speaks before her knees can betray her: she saw the forbidden article, failed to report it, and now offers confession where others offer alibis.", word_delay=_book1_word_delay)
    call book1_nvl_write_line("The partial truth trembles on her tongue like communion in a chapel that prefers spectacle to mercy.", word_delay=_book1_word_delay)
    call book1_nvl_write_line("Her pen drives the heroine's pulse into the margin till shame and fascination share one fevered line; Lady Vayne's wrath becomes a bodice laced too tight, Lord Caldor's notice a furnace door she cannot stop walking toward.", word_delay=_book1_word_delay)
    call book1_nvl_write_line("The reader is meant to blush — and then turn the page anyway.", word_delay=_book1_word_delay)
    call book1_nvl_write_line("Honesty is dressed as modesty until the crowd learns modesty was only another curtain call.", word_delay=_book1_word_delay)

    call book1_block_day2_missy_debt_or_repair
    call book1_block_day2_stern_suspicion_or_diffuse
    call book1_block_day2_contraband_state
    call book1_block_day2_stern_pressure_if_needed

    return


# [DAG_NODE id=book1_block_day2_default_core type=write]
label book1_block_day2_default_core:

    call book1_nvl_write_line("Chapter the Second opens upon a lady's hatbox in the conservatory suite, sealed like a coffin for silk and scandal.", word_delay=_book1_word_delay)
    call book1_nvl_write_line("The tea service steams; every cup rings as if the house itself were counting who shall be ruined before the cakes grow cold.", word_delay=_book1_word_delay)

    call book1_block_day2_missy_debt_or_repair
    call book1_block_day2_stern_suspicion_or_diffuse
    call book1_block_day2_contraband_state
    call book1_block_day2_stern_pressure_if_needed

    return


# [DAG_NODE id=book1_block_day2_missy_debt_or_repair type=write]
label book1_block_day2_missy_debt_or_repair:

    if story.missy_day2_trust_break:
        call book1_nvl_write_line("Miri, the faithful courier, is made to carry the hatbox curse in Coralie's stead — betrayed in a whisper that never once stained the heroine's cuffs.", word_delay=_book1_word_delay)
        call book1_nvl_write_line("The manuscript does not absolve her; it brands the debt like a stain that cannot be laundered out.", word_delay=_book1_word_delay)
    else:
        call book1_nvl_write_line("Miri lingers at the chapter's edge — wary, still loyal enough to ache — and Coralie grants her a mercy Ravenshade never did: a page that admits repair without pretending innocence returned unmarked.", word_delay=_book1_word_delay)

    return


# [DAG_NODE id=book1_block_day2_stern_suspicion_or_diffuse type=write]
label book1_block_day2_stern_suspicion_or_diffuse:

    if story.missy_day2_suspicion_state == "uneasy":
        call book1_nvl_write_line("Mr. Sterick questions Miri before he questions Heaven, for hierarchy teaches that some throats are safer to close in public.", word_delay=_book1_word_delay)
        call book1_nvl_write_line("Coralie's narration counts each polite syllable as a blow delivered without raising a hand.", word_delay=_book1_word_delay)
    else:
        call book1_nvl_write_line("Even when Mr. Sterick keeps his reprimand diffuse, Miri drinks the room's panic as if it were her tea.", word_delay=_book1_word_delay)
        call book1_nvl_write_line("Coralie writes the moment as proof that discipline need not shout to draw blood.", word_delay=_book1_word_delay)

    return


# [DAG_NODE id=book1_block_day2_contraband_state type=write]
label book1_block_day2_contraband_state:

    if story.day2_contraband_state == "stolen_wearing":
        call book1_nvl_write_line("The contraband never left Coralie's keeping; she wears the secret under her uniform and sets the chapter humming with a heat no respectable printer would confess aloud.", word_delay=_book1_word_delay)
    elif story.day2_contraband_state == "planted_in_trunk":
        call book1_nvl_write_line("The contraband is slipped into a gentleman's travelling trunk, and the narrative savours misdirection the way Holywell Street savours a well-laid seduction.", word_delay=_book1_word_delay)

    return


# [DAG_NODE id=book1_block_day2_stern_pressure_if_needed type=write]
label book1_block_day2_stern_pressure_if_needed:

    if story.missy_day2_suspicion_state == "uneasy" or story.missy_day2_trust_break:
        call book1_nvl_write_line("Mr. Sterick turns the full theatre of blame upon Miri, and Coralie — whether witness or architect — records how guilt rolls downhill like marbles on polished oak.", word_delay=_book1_word_delay)
        call book1_nvl_write_line("The reprimand is couched in serviceable English and executed in the old currency: rank.", word_delay=_book1_word_delay)

    return


