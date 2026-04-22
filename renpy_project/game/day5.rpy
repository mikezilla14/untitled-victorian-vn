# ═══════════════════════════════════════════════════════════════
#  day5.rpy — THE RECKONING
#  The deadline. Miss Stern's inspection is the final gauntlet.
#  The corruption_level gate either unlocks the climax scene
#  or routes to the bad ending. The cliffhanger closes the MVP.
# ═══════════════════════════════════════════════════════════════

label day5_morning:
    $ time_manager.set_current_day(5)
    $ set_time_period("Morning")

    sys "─── DAY 5: MORNING — THE RECKONING ───"

    cora  "I knew something was wrong the moment I heard her footsteps outside my door."

    stern "Cora. Open this door."

    cora  "Miss Stern stood in my doorway like the angel of judgement. Her eyes swept the room — the bed, the washstand, the desk."

    stern "I've noticed you've been keeping irregular hours. The night porter reported movement in the service corridors past midnight."
    stern "Is there something you'd like to tell me?"

    cora  "My manuscript was sitting in plain view on the desk, covered by a single sheet of writing paper."

    menu:
        "She's looking at the desk."

        "Hide the manuscript — destroy the draft pages (Costly)":
            $ apply_effects(insp=-15)
            cora  "While her back was turned checking the wardrobe, I shoved the loose pages under the mattress and crumpled the visible sheet."
            cora  "She found nothing. But I've lost material. Pages I'll have to rewrite from memory."
            stern "Hmm. See that you keep proper hours, Cora. I will not have slovenly behaviour on my floor."
            cora  "She left. My knees buckled."

        "Bluff — 'It's a letter to my mother, ma'am' (Dangerous)":
            $ apply_effects(susp=20)
            cora  "'It's a letter to my mother, ma'am. I write to her every week.'"
            stern "Every week, is it. You seem to do a great deal of writing for a chambermaid."
            cora  "She picked up the sheet on top. My heart stopped."
            cora  "It was, mercifully, the cover page — an innocuous description of the hotel. The explicit material was underneath."
            stern "See that your correspondence doesn't interfere with your duties."
            cora  "She left. I almost vomited."

    $ resolve_turn()
    jump day5_night


label day5_night:
    $ set_time_period("Night")

    sys "─── DAY 5: NIGHT — THE CLIMAX ───"

    cora "This is it. The deadline. The publisher on Holywell Street expects the final chapter by morning."

    if player.corruption_level >= 3:
        cora "I sat at my desk. I dipped the nib in the ink."
        cora "And I wrote."
        cora "Not the timid, blushing prose of Day 1. Not the overwrought fantasies of Day 3. This was something else entirely."
        cora "It was raw. It was explicit. It was terrifyingly good."
        cora "I wrote about a woman who watches. A woman who desires. A woman who has spent her entire life being invisible and who discovers, in the act of writing, that she has a voice — and that voice is filthy, and powerful, and entirely her own."

        sys "[[CG #3 PLACEHOLDER — DAY 5 CLIMAX: The full, polished payoff scene. 3-4 stages. This is the money shot. This sells subscriptions. Cora's manuscript brought to life in its most explicit form.]"

        cora "When I finished, I stared at the pages."

        if story.has_received_manuscript_payment:
            cora "Three shillings for the first chapter. What would they pay for this?"
            cora "More than I earn in a month scrubbing Sir Gideon's floors. The bitter irony was not lost on me."

        cora "I wrapped the manuscript. The errand boy would carry it to Holywell Street at dawn."
        cora "I sat in the candlelight and looked at my ink-stained fingers and realised something terrible."
        cora "I am good at this."
        cora "And I will never be able to stop."

        jump day5_cliffhanger

    else:
        jump bad_ending_rejection


label day5_cliffhanger:
    $ set_time_period("Late Night")

    sys "─── DAY 5: LATE NIGHT — THE CLIFFHANGER ───"

    cora   "I was about to blow out the candle when I heard it."
    cora   "A knock. Soft. Not Miss Stern's sharp rap — something quieter, more deliberate."
    cora   "I opened the door."
    cora   "Sir Gideon Locke stood in the servant's corridor. In his hand was a single page of manuscript — one I must have dropped on the stairs."
    cora   "He read a line aloud. His voice was steady. His eyes were not."

    gideon "You have a very... vivid imagination, Cora."

    cora   "My blood ran cold. Then hot. Then something in between."

    gideon "Lock the door."

    sys "═══════════════════════════════════════"
    sys "TO BE CONTINUED."
    sys "═══════════════════════════════════════"
    sys "[[CTA: SubscribeStar link. 'Chapter 2 is in development. Subscribe to play it first.']"

    return
