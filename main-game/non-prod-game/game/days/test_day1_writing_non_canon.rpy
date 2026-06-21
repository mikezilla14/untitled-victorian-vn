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
# test_day1_writing_non_canon.rpy
# Fast harness for Day 1 writing flow and book1 NVL output.
# ==========================================================

label test_day1_writing_harness:

    # [ASSET] Visual/staging command
    scene bg_cora_desk_night
    with dissolve

    menu:
        "Day 1 writing test setup"

        "Manual Render (Edit variables directly in script to test custom paths)":

            # [STATE] State/progression update
            jump test_day1_render_manual

        "Run: Corruption Test Run (Predator + Complicit, High Corruption)":

            # [STATE] State/progression update
            jump test_day1_render_corruption_run

        "Run: Cautious Test Run (Ghost + Subservient, Low Corruption)":

            # [STATE] State/progression update
            jump test_day1_render_cautious_run

        "Render Slop Path: Default (Low Corruption)":

            # [STATE] State/progression update
            jump test_day1_render_slop_default

        "Render Slop Path: Ghost Core (Low Corruption)":

            # [STATE] State/progression update
            jump test_day1_render_slop_ghost

        "Render Slop Path: Predator Core (Low Corruption)":

            # [STATE] State/progression update
            jump test_day1_render_slop_predator

        "Render Slop Path: Prey Core (Low Corruption)":

            # [STATE] State/progression update
            jump test_day1_render_slop_prey

        "Render Slop Path: Ghost + Subservient (Low Corruption)":

            # [STATE] State/progression update
            jump test_day1_render_slop_ghost_subservient

        "Render Slop Path: Predator + Complicit (Low Corruption)":

            # [STATE] State/progression update
            jump test_day1_render_slop_predator_complicit

        "Render Slop Path: Prey + Resistant (Low Corruption)":

            # [STATE] State/progression update
            jump test_day1_render_slop_prey_resistant

        "Render Corrupted Path: Default (High Corruption)":

            # [STATE] State/progression update
            jump test_day1_render_alt_default

        "Render Corrupted Path: Alt Ghost (High Corruption)":

            # [STATE] State/progression update
            jump test_day1_render_alt_ghost

        "Render Corrupted Path: Alt Predator (High Corruption)":

            # [STATE] State/progression update
            jump test_day1_render_alt_predator

        "Render Corrupted Path: Alt Prey (High Corruption)":

            # [STATE] State/progression update
            jump test_day1_render_alt_prey

        "Render Corrupted Path: Alt Ghost + Subservient (High Corruption)":

            # [STATE] State/progression update
            jump test_day1_render_alt_ghost_subservient

        "Render Corrupted Path: Alt Predator + Complicit (High Corruption)":

            # [STATE] State/progression update
            jump test_day1_render_alt_predator_complicit

        "Render Corrupted Path: Alt Prey + Resistant (High Corruption)":

            # [STATE] State/progression update
            jump test_day1_render_alt_prey_resistant


label test_day1_reset_state:
    python:
        # Fresh instances make repeated test runs deterministic.
        store.player = PlayerStats()
        store.story = StoryState()
        store.time_manager = TimeManager()
    return


label test_day1_render_manual:
    call test_day1_reset_state

    # =========================================================================
    # MANUAL RENDER CONFIGURATION
    # Edit these values to test different combinations!
    # By default, this is tuned to the Corruption Path (Alt Predator + Complicit).
    # =========================================================================

    # [STATE] State/progression update
    $ player_inspiration = 20
    $ player_corruption_level = 3       # > 2 for Alt Chapter, <= 2 for Slop Chapter
    $ day1_corridor_state = "predator"  # "ghost", "predator", "prey", or "none"
    $ day1_stern_relation = "complicit"  # "complicit", "subservient", "resistant", or "none"
    $ day1_ledger_focus = "corruption"   # "corruption" or "inspiration"
    # =========================================================================

    # Apply manual values to player and story objects

    # [STATE] State/progression update
    $ setattr(player, "inspiration", player_inspiration)
    $ setattr(player, "corruption_level", player_corruption_level)
    $ player.update_stats()

    $ story.set_corridor_state(day1_corridor_state)
    $ story.set_day1_stern_relation(day1_stern_relation)
    $ story.set_day1_ledger_focus(day1_ledger_focus)

    # Determine chapter key based on corruption level
    if player.corruption_level <= 2:

        # [STATE] State/progression update
        $ _chapter_key = "day1_slop_chapter"
    else:

        # [STATE] State/progression update
        $ _chapter_key = "day1_chapter"

    call book1_debug_chapter_route(chapter_key=_chapter_key)
    call book1_write_chapter(chapter_key=_chapter_key, current_day=101, include_debug=True)
    return


label test_day1_render_corruption_run:
    call test_day1_reset_state

    # [STATE] State/progression update
    $ setattr(player, "inspiration", 20)
    $ setattr(player, "corruption_level", 3)
    $ player.update_stats()

    $ story.set_corridor_state("predator")
    $ story.set_day1_stern_relation("complicit")
    $ story.set_day1_ledger_focus("corruption")

    call book1_debug_chapter_route(chapter_key="day1_chapter")
    call book1_write_chapter(chapter_key="day1_chapter", current_day=101, include_debug=True)
    return


label test_day1_render_cautious_run:
    call test_day1_reset_state

    # [STATE] State/progression update
    $ setattr(player, "inspiration", 20)
    $ setattr(player, "corruption_level", 2)
    $ player.update_stats()

    $ story.set_corridor_state("ghost")
    $ story.set_day1_stern_relation("subservient")
    $ story.set_day1_ledger_focus("inspiration")

    call book1_debug_chapter_route(chapter_key="day1_slop_chapter")
    call book1_write_chapter(chapter_key="day1_slop_chapter", current_day=101, include_debug=True)
    return


label test_day1_render_slop_default:
    call test_day1_reset_state

    # [STATE] State/progression update
    $ setattr(player, "inspiration", 20)
    $ setattr(player, "corruption_level", 2)
    $ player.update_stats()

    $ story.set_corridor_state("none")
    $ story.set_day1_stern_relation("none")
    $ story.set_day1_ledger_focus("inspiration")

    call book1_debug_chapter_route(chapter_key="day1_slop_chapter")
    call book1_write_chapter(chapter_key="day1_slop_chapter", current_day=101, include_debug=True)
    return


label test_day1_render_slop_ghost:
    call test_day1_reset_state

    # [STATE] State/progression update
    $ setattr(player, "inspiration", 20)
    $ setattr(player, "corruption_level", 2)
    $ player.update_stats()

    $ story.set_corridor_state("ghost")
    $ story.set_day1_stern_relation("none")
    $ story.set_day1_ledger_focus("inspiration")

    call book1_debug_chapter_route(chapter_key="day1_slop_chapter")
    call book1_write_chapter(chapter_key="day1_slop_chapter", current_day=101, include_debug=True)
    return


label test_day1_render_slop_predator:
    call test_day1_reset_state

    # [STATE] State/progression update
    $ setattr(player, "inspiration", 20)
    $ setattr(player, "corruption_level", 2)
    $ player.update_stats()

    $ story.set_corridor_state("predator")
    $ story.set_day1_stern_relation("none")
    $ story.set_day1_ledger_focus("corruption")

    call book1_debug_chapter_route(chapter_key="day1_slop_chapter")
    call book1_write_chapter(chapter_key="day1_slop_chapter", current_day=101, include_debug=True)
    return


label test_day1_render_slop_prey:
    call test_day1_reset_state

    # [STATE] State/progression update
    $ setattr(player, "inspiration", 20)
    $ setattr(player, "corruption_level", 2)
    $ player.update_stats()

    $ story.set_corridor_state("prey")
    $ story.set_day1_stern_relation("none")
    $ story.set_day1_ledger_focus("inspiration")

    call book1_debug_chapter_route(chapter_key="day1_slop_chapter")
    call book1_write_chapter(chapter_key="day1_slop_chapter", current_day=101, include_debug=True)
    return


label test_day1_render_slop_ghost_subservient:
    call test_day1_reset_state

    # [STATE] State/progression update
    $ setattr(player, "inspiration", 20)
    $ setattr(player, "corruption_level", 2)
    $ player.update_stats()

    $ story.set_corridor_state("ghost")
    $ story.set_day1_stern_relation("subservient")
    $ story.set_day1_ledger_focus("inspiration")

    call book1_debug_chapter_route(chapter_key="day1_slop_chapter")
    call book1_write_chapter(chapter_key="day1_slop_chapter", current_day=101, include_debug=True)
    return


label test_day1_render_slop_predator_complicit:
    call test_day1_reset_state

    # [STATE] State/progression update
    $ setattr(player, "inspiration", 20)
    $ setattr(player, "corruption_level", 2)
    $ player.update_stats()

    $ story.set_corridor_state("predator")
    $ story.set_day1_stern_relation("complicit")
    $ story.set_day1_ledger_focus("corruption")

    call book1_debug_chapter_route(chapter_key="day1_slop_chapter")
    call book1_write_chapter(chapter_key="day1_slop_chapter", current_day=101, include_debug=True)
    return


label test_day1_render_slop_prey_resistant:
    call test_day1_reset_state

    # [STATE] State/progression update
    $ setattr(player, "inspiration", 20)
    $ setattr(player, "corruption_level", 2)
    $ player.update_stats()

    $ story.set_corridor_state("prey")
    $ story.set_day1_stern_relation("resistant")
    $ story.set_day1_ledger_focus("inspiration")

    call book1_debug_chapter_route(chapter_key="day1_slop_chapter")
    call book1_write_chapter(chapter_key="day1_slop_chapter", current_day=101, include_debug=True)
    return


label test_day1_render_alt_default:
    call test_day1_reset_state

    # [STATE] State/progression update
    $ setattr(player, "inspiration", 20)
    $ setattr(player, "corruption_level", 3)
    $ player.update_stats()

    $ story.set_corridor_state("none")
    $ story.set_day1_stern_relation("none")
    $ story.set_day1_ledger_focus("inspiration")

    call book1_debug_chapter_route(chapter_key="day1_chapter")
    call book1_write_chapter(chapter_key="day1_chapter", current_day=101, include_debug=True)
    return


label test_day1_render_alt_ghost:
    call test_day1_reset_state

    # [STATE] State/progression update
    $ setattr(player, "inspiration", 20)
    $ setattr(player, "corruption_level", 3)
    $ player.update_stats()

    $ story.set_corridor_state("ghost")
    $ story.set_day1_stern_relation("none")
    $ story.set_day1_ledger_focus("inspiration")

    call book1_debug_chapter_route(chapter_key="day1_chapter")
    call book1_write_chapter(chapter_key="day1_chapter", current_day=101, include_debug=True)
    return


label test_day1_render_alt_predator:
    call test_day1_reset_state

    # [STATE] State/progression update
    $ setattr(player, "inspiration", 20)
    $ setattr(player, "corruption_level", 3)
    $ player.update_stats()

    $ story.set_corridor_state("predator")
    $ story.set_day1_stern_relation("none")
    $ story.set_day1_ledger_focus("corruption")

    call book1_debug_chapter_route(chapter_key="day1_chapter")
    call book1_write_chapter(chapter_key="day1_chapter", current_day=101, include_debug=True)
    return


label test_day1_render_alt_prey:
    call test_day1_reset_state

    # [STATE] State/progression update
    $ setattr(player, "inspiration", 20)
    $ setattr(player, "corruption_level", 3)
    $ player.update_stats()

    $ story.set_corridor_state("prey")
    $ story.set_day1_stern_relation("none")
    $ story.set_day1_ledger_focus("inspiration")

    call book1_debug_chapter_route(chapter_key="day1_chapter")
    call book1_write_chapter(chapter_key="day1_chapter", current_day=101, include_debug=True)
    return


label test_day1_render_alt_ghost_subservient:
    call test_day1_reset_state

    # [STATE] State/progression update
    $ setattr(player, "inspiration", 20)
    $ setattr(player, "corruption_level", 3)
    $ player.update_stats()

    $ story.set_corridor_state("ghost")
    $ story.set_day1_stern_relation("subservient")
    $ story.set_day1_ledger_focus("inspiration")

    call book1_debug_chapter_route(chapter_key="day1_chapter")
    call book1_write_chapter(chapter_key="day1_chapter", current_day=101, include_debug=True)
    return


label test_day1_render_alt_predator_complicit:
    call test_day1_reset_state

    # [STATE] State/progression update
    $ setattr(player, "inspiration", 20)
    $ setattr(player, "corruption_level", 3)
    $ player.update_stats()

    $ story.set_corridor_state("predator")
    $ story.set_day1_stern_relation("complicit")
    $ story.set_day1_ledger_focus("corruption")

    call book1_debug_chapter_route(chapter_key="day1_chapter")
    call book1_write_chapter(chapter_key="day1_chapter", current_day=101, include_debug=True)
    return


label test_day1_render_alt_prey_resistant:
    call test_day1_reset_state

    # [STATE] State/progression update
    $ setattr(player, "inspiration", 20)
    $ setattr(player, "corruption_level", 3)
    $ player.update_stats()

    $ story.set_corridor_state("prey")
    $ story.set_day1_stern_relation("resistant")
    $ story.set_day1_ledger_focus("inspiration")

    call book1_debug_chapter_route(chapter_key="day1_chapter")
    call book1_write_chapter(chapter_key="day1_chapter", current_day=101, include_debug=True)
    return
