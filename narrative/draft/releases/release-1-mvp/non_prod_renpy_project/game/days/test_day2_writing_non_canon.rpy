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

# ==========================================================
# test_day2_writing_non_canon.rpy
# Fast harness for Day 2 writing flow and book1 NVL output.
# ==========================================================

label test_day2_writing_harness:

    # [ASSET] Visual/staging command
    scene bg_cora_desk_night
    with dissolve

    menu:
        "Day 2 writing test setup"

        "Render label-based book1 prose: day2_chapter (predator + trust break)":

            # [STATE] State/progression update
            jump test_day2_render_book1_day2_predator

        "Render label-based book1 prose: day2_chapter (ghost + stern/missy pressure)":

            # [STATE] State/progression update
            jump test_day2_render_book1_day2_ghost

        "Render label-based book1 prose: day2_chapter (prey + partial confession)":

            # [STATE] State/progression update
            jump test_day2_render_book1_day2_prey

        "Render book1 event: day1_chapter":

            # [STATE] State/progression update
            jump test_book1_render_day1_chapter

        "Render book1 event: day3_chapter":

            # [STATE] State/progression update
            jump test_book1_render_day3_chapter

        "Render book1 event: day4_triumphant_chapter":

            # [STATE] State/progression update
            jump test_book1_render_day4_triumphant_chapter

        "Render book1 event: day5_reckoning_chapter":

            # [STATE] State/progression update
            jump test_book1_render_day5_reckoning_chapter


label test_day2_reset_state:
    python:
        # Fresh instances make repeated test runs deterministic.
        store.player = PlayerStats()
        store.story = StoryState()
        store.time_manager = TimeManager()
    return


label test_day2_render_book1_day2_predator:
    call test_day2_reset_state

    # [STATE] State/progression update
    $ setattr(player, "inspiration", 22)
    $ setattr(player, "corruption_level", 35)
    $ player.update_stats()

    $ story.set_corridor_state("predator")
    $ story.set_day1_ledger_focus("corruption")
    $ story.set_day2_contraband_state("stolen_wearing")
    $ story.set_day2_tea_choice("predator")
    $ story.set_missy_day2_trust_break(True)

    call book1_debug_chapter_route(chapter_key="day2_chapter")
    call book1_write_chapter(chapter_key="day2_chapter", current_day=102, include_debug=True)
    return


label test_day2_render_book1_day2_ghost:
    call test_day2_reset_state

    # [STATE] State/progression update
    $ setattr(player, "inspiration", 22)
    $ setattr(player, "corruption_level", 34)
    $ player.update_stats()

    $ story.set_corridor_state("ghost")
    $ story.set_day1_ledger_focus("inspiration")
    $ story.set_day2_contraband_state("planted_in_trunk")
    $ story.set_day2_tea_choice("ghost")
    $ story.set_missy_day2_suspicion_state("uneasy")
    $ story.set_missy_day2_trust_break(True)

    call book1_debug_chapter_route(chapter_key="day2_chapter")
    call book1_write_chapter(chapter_key="day2_chapter", current_day=102, include_debug=True)
    return


label test_day2_render_book1_day2_prey:
    call test_day2_reset_state

    # [STATE] State/progression update
    $ setattr(player, "inspiration", 28)
    $ setattr(player, "corruption_level", 12)
    $ player.update_stats()

    $ story.set_corridor_state("prey")
    $ story.set_day1_ledger_focus("inspiration")
    $ story.set_day2_contraband_state("stolen_wearing")
    $ story.set_day2_tea_choice("prey")
    $ story.set_missy_day2_suspicion_state("uneasy")

    call book1_debug_chapter_route(chapter_key="day2_chapter")
    call book1_write_chapter(chapter_key="day2_chapter", current_day=102, include_debug=True)
    return


label test_book1_render_day1_chapter:
    call test_day2_reset_state

    # [STATE] State/progression update
    $ story.set_corridor_state("predator")
    $ story.set_day1_ledger_focus("corruption")

    call book1_debug_chapter_route(chapter_key="day1_chapter")
    call book1_write_chapter(chapter_key="day1_chapter", current_day=101, include_debug=True)
    return


label test_book1_render_day3_chapter:
    call test_day2_reset_state

    # [STATE] State/progression update
    $ story.set_day1_ledger_focus("inspiration")
    $ story.set_day3_brush_choice("prey")
    $ story.set_day3_twilight_action("frantic_write")
    $ story.set_day3_ultimatum("defied")
    $ story.set_day3_stern_response("partial_truth")

    call book1_debug_chapter_route(chapter_key="day3_chapter")
    call book1_write_chapter(chapter_key="day3_chapter", current_day=103, include_debug=True)
    return


label test_book1_render_day4_triumphant_chapter:
    call test_day2_reset_state

    # [STATE] State/progression update
    $ story.set_corridor_state("ghost")
    $ story.set_day1_ledger_focus("inspiration")
    $ story.set_missy_day2_suspicion_state("uneasy")
    $ story.set_missy_day2_trust_break(True)
    $ story.set_day4_night_action("finish_manuscript")
    $ story.set_day4_escape_state("missy_cover")
    $ story.set_has_photograph(True)

    call book1_debug_chapter_route(chapter_key="day4_triumphant_chapter")
    call book1_write_chapter(chapter_key="day4_triumphant_chapter", current_day=104, include_debug=True)
    return


label test_book1_render_day5_reckoning_chapter:
    call test_day2_reset_state

    # [STATE] State/progression update
    $ story.set_day5_dynamic("adversary")
    $ story.set_missy_day2_suspicion_state("uneasy")
    $ story.set_missy_day2_trust_break(True)
    $ story.set_day3_ultimatum("defied")
    $ story.set_day4_escape_state("missy_cover")
    $ story.set_has_photograph(True)
    $ story.complete_release1_manuscript(True)
    $ story.set_release1_completed(True)

    call book1_debug_chapter_route(chapter_key="day5_reckoning_chapter")
    call book1_write_chapter(chapter_key="day5_reckoning_chapter", current_day=105, include_debug=True)
    return
