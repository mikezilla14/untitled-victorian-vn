# ═══════════════════════════════════════════════════════════════
#  day2.rpy — THE FIRST ENCOUNTER
#  First real player choices. Gideon speaks to Cora — unusual,
#  possibly dangerous. The writing desk gate is introduced.
#  Inspiration first becomes meaningful here.
# ═══════════════════════════════════════════════════════════════

label day2_morning:
    $ time_manager.current_day  = 2
    $ time_manager.time_of_day  = "Morning"

    sys "─── DAY 2: MORNING ───"

    cora   "Sir Gideon was in the suite when I arrived to clean."
    cora   "Gentlemen do not speak to chambermaids. That is the rule. You enter, you curtsy, you become invisible, you leave."

    gideon "Ah — you're the new girl. Cora, is it?"

    cora   "He knew my name. That was... unusual."

    $ story.gideon_spoke_day2 = True

    gideon "Don't look so startled. I asked Miss Stern — fearsome woman — who'd been keeping my rooms so spotless."
    cora   "He gestured at a volume of Keats on the mantelpiece."
    gideon "Do you read?"

    cora   "My heart hammered. A gentleman asking a maid if she reads. It could mean anything. Kindness. Curiosity. Or something else entirely."
    cora   "I said, 'A little, sir,' which was the safest lie."

    menu:
        "What do I do while he's distracted?"

        "Clean the desk and keep my head down (Safe)":
            $ player.lower_suspicion(10)
            $ player.gain_inspiration(5)
            cora "I dusted and polished and kept my eyes on the floor. Safe. Invisible. Exactly what Miss Stern expects."
            cora "I learned nothing. But I survived."

        "Glance at the letters on his writing desk (Risky)":
            $ player.raise_suspicion(20)
            $ player.gain_inspiration(15)
            $ story.read_letters = True
            cora "While Sir Gideon had his back turned, I caught a glimpse of the letters on his desk. The handwriting was feminine. The language was... heated."
            cora "One letter mentioned a 'midnight arrangement' and 'the usual discretion.'"
            cora "My pulse was racing when I left the room. Not from fear. From something far more dangerous — curiosity."

    $ player.update_stats()
    call check_suspicion
    jump day2_night


label day2_night:
    $ time_manager.time_of_day = "Night"

    sys "─── DAY 2: NIGHT ───"

    menu:
        "My shift is over. The gas lamps are dimmed in the servant's corridor."

        "Stay in my quarters and write a letter home (Pure)":
            $ player.gain_corruption_xp(-5)
            cora "I sat at my desk and wrote to my mother. Told her the hotel was grand, the work honest, and Miss Stern fair. All of it lies, except the first."
            cora "I told her I was saving well. That was true, at least."
            cora "The blank manuscript page stared at me from under the letter. I ignored it."

        "Explore the hidden servant's passage (Scandalous)" if not story.read_letters:
            $ player.gain_corruption_xp(10)
            $ player.gain_inspiration(15)
            $ player.raise_suspicion(10)
            cora "The Savoy was built with hidden corridors behind every wall — passages for the staff to move without being seen by guests. Tonight, I moved through them for a different reason."
            cora "I pressed my ear to the thin walls of the VIP floor. Voices. A woman laughing. The clink of crystal."
            cora "I saw nothing. But I heard enough to know that Sir Gideon Locke's evenings are not spent reading Keats."

        "Sneak to the servant's passage — I know where to listen (Scandalous)" if story.read_letters:
            $ player.gain_corruption_xp(10)
            $ player.gain_inspiration(20)
            $ player.raise_suspicion(10)
            cora "The letters mentioned a midnight arrangement. The servant's passage runs directly behind the VIP suites."
            cora "I pressed my ear to the wall. The voices were muffled but unmistakable. A woman. Sir Gideon. Laughter, then silence, then sounds I had only ever read about in the penny dreadfuls."
            cora "My face burned in the dark corridor. My mind was already composing sentences."

    $ player.update_stats()
    call check_suspicion
    jump day2_late_night


label day2_late_night:
    $ time_manager.time_of_day = "Late Night"

    sys "─── DAY 2: LATE NIGHT ───"

    menu:
        "Should I try the manuscript?"

        "Sit at the writing desk (Requires 30 Inspiration)":
            if player.inspiration >= 30:
                $ player.inspiration -= 20
                $ story.wrote_chapter_1  = True
                $ story.manuscript_sent  = True
                cora "I wrote. It was clumsy, overwrought, and naive — a schoolgirl's idea of scandal. But it was something."
                cora "I wrapped the pages in brown paper and wrote the Holywell Street address on the front."
                cora "Tomorrow morning, before Miss Stern's rounds, I'll slip it into the outgoing deliveries at the tradesmen's entrance. The errand boys won't question a sealed package."
                cora "My hands were shaking. Not from cold."
            else:
                cora "I sat at the desk and tried. But the words wouldn't come."
                cora "I don't have enough material. My prose is hollow — all structure, no heat. I need to observe more. I need to {i}experience{/i} more."

        "Blow out the candle and sleep":
            cora "I'm too exhausted. The writing can wait. It has to."

    $ player.update_stats()
    call check_suspicion
    jump day3_morning
