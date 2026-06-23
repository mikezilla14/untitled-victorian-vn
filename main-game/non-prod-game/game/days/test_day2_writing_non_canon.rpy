label test_day2_writing_harness:
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

    # [ASSET] Visual/staging command
    scene bg_cora_desk_night
    with dissolve

    menu:
        "Book1 MVP test harness — choose category"

        "A) Direct API tests":

            # [STATE] State/progression update
            jump test_b1_api_menu

        "B) Vertical slice: day2 predator block":

            # [STATE] State/progression update
            jump test_b1_vertical_slice_predator

        "C) Integration tests (full chapter routes)":

            # [STATE] State/progression update
            jump test_b1_integration_menu


# ==========================================================
# NAVIGATION: API menu
# ==========================================================

label test_b1_api_menu:

    # [ASSET] Visual/staging command
    scene bg_cora_desk_night
    with dissolve

    menu:
        "Book1 API tests — choose test"

        "book1_write_beat (page_break / thought / clear_thought / word_delay)":

            # [STATE] State/progression update
            jump test_b1_api_write_beat

        "Visual modes: cover → tableau → plate → blank → detail":

            # [STATE] State/progression update
            jump test_b1_api_visual_modes

        "book1_set_chapter_title (title + subtitle)":

            # [STATE] State/progression update
            jump test_b1_api_chapter_title

        "book1_author_thought + book1_clear_author_thought":

            # [STATE] State/progression update
            jump test_b1_api_author_thought


# ==========================================================
# NAVIGATION: Integration menu
# ==========================================================

label test_b1_integration_menu:

    # [ASSET] Visual/staging command
    scene bg_cora_desk_night
    with dissolve

    menu:
        "Integration: full chapter routes via book1_write_chapter"

        "day2_chapter: predator (trust break)":

            # [STATE] State/progression update
            jump test_day2_render_book1_day2_predator

        "day2_chapter: ghost (suspicion + trust break)":

            # [STATE] State/progression update
            jump test_day2_render_book1_day2_ghost

        "day2_chapter: prey (partial confession)":

            # [STATE] State/progression update
            jump test_day2_render_book1_day2_prey

        "day1_chapter":

            # [STATE] State/progression update
            jump test_book1_render_day1_chapter

        "day3_chapter":

            # [STATE] State/progression update
            jump test_book1_render_day3_chapter

        "day4_triumphant_chapter":

            # [STATE] State/progression update
            jump test_book1_render_day4_triumphant_chapter

        "day5_reckoning_chapter":

            # [STATE] State/progression update
            jump test_book1_render_day5_reckoning_chapter


# ==========================================================
# SHARED HELPERS
# ==========================================================

label test_day2_reset_state:
    python:
        # Fresh instances make repeated test runs deterministic.
        store.player = PlayerStats()
        store.story = StoryState()
        store.time_manager = TimeManager()
    return


# Mirrors the state init in book1_write_chapter without routing
# or calling a chapter block. Call this before exercising
# individual Book1 API labels directly.
label test_b1_book1_init:
    nvl clear

    # [STATE] State/progression update
    $ store._book1_word_delay       = 0.04
    $ store._book1_page_line_count  = 0
    $ store._book1_page_line_limit  = 4
    $ store.book1_page_image        = "ui_book_cover"
    $ store.book1_page_mode         = "cover"
    $ store.book1_plate_caption     = ""
    $ store.book1_chapter_title     = ""
    $ store.book1_chapter_subtitle  = ""
    $ store.book1_author_thought    = ""
    $ store.book1_author_thought_id = 0
    $ store.book1_route_provenance  = ""
    $ store.book1_show_stats        = False
    call book1_show_cover()
    return


# ==========================================================
# SECTION A: Direct API tests
# ==========================================================

# [TEST] book1_write_beat
# Exercises: page_break, thought, thought linger, clear_thought, word_delay override.
label test_b1_api_write_beat:
    call test_day2_reset_state
    call test_b1_book1_init

    call book1_set_chapter_title(title="WRITE BEAT TEST", subtitle="API Unit Test")

    # Baseline: no params beyond text.
    call book1_write_beat("Beat 1 — baseline. No thought, no page break, default word delay.")

    # page_break clears NVL before writing; thought appears in margin.
    call book1_write_beat(
        "Beat 2 — page_break=True opens a fresh NVL page. Author thought set in margin.",
        thought="This marginalia note should appear in the margin column.",
        page_break=True
    )

    # Thought lingers when next beat omits the param.
    call book1_write_beat("Beat 3 — thought param omitted. Prior thought should still linger in margin.")

    # clear_thought wipes margin after the line renders.
    call book1_write_beat(
        "Beat 4 — clear_thought=True. Marginalia should vanish after this line.",
        clear_thought=True
    )

    # Confirm margin is clear.
    call book1_write_beat("Beat 5 — margin should be empty now.")

    # word_delay override.
    call book1_write_beat(
        "Beat 6 — word_delay=0.01 override. Word reveal should be noticeably faster.",
        word_delay=0.01
    )

    nvl clear
    return


# [TEST] Visual modes
# Exercises: book1_show_cover, book1_show_tableau, book1_show_plate (with and without
# explicit image), book1_show_blank, book1_show_detail. One prose beat per mode
# so the illustration panel is visible alongside each transition.
label test_b1_api_visual_modes:
    call test_day2_reset_state
    call test_b1_book1_init

    call book1_set_chapter_title(title="VISUAL MODES TEST", subtitle="Mode Cycle Check")

    # Cover (default after init)
    call book1_write_beat("Mode: cover (default). Illustration panel shows book cover image.")

    # Tableau
    call book1_show_tableau("cg_book_d2_hatbox_tableau")
    call book1_write_beat("Mode: tableau. Full illustration, no plate treatment.")

    # Plate — reuses current image via image_name=None default
    call book1_show_plate(caption="Plate II — Plate Mode Caption Check")
    call book1_write_beat("Mode: plate (image=None → reuses current). Sepia + hatch + paper overlays active. Caption visible below frame.")

    # Plate — explicit image override
    call book1_show_plate("ui_book_cover", caption="Plate mode — explicit image override")
    call book1_write_beat("Mode: plate with explicit image override. Overlays still applied.")

    # Blank
    call book1_show_blank(caption="Blank mode — writing-only surface")
    call book1_write_beat("Mode: blank. No illustration, aged paper surface only. Caption visible.")

    # Detail
    call book1_show_detail("cg_book_d2_hatbox_tableau", caption="Detail caption")
    call book1_write_beat("Mode: detail. Full illustration with dissolve transition.")

    # Return to cover
    call book1_show_cover()
    call book1_write_beat("Mode: cover restored.")

    nvl clear
    return


# [TEST] book1_set_chapter_title
# Exercises: title only, title + subtitle, cleared (restores static fallback).
label test_b1_api_chapter_title:
    call test_day2_reset_state
    call test_b1_book1_init

    call book1_write_beat("Chapter title test. No title set — static fallback masthead should show.")

    call book1_set_chapter_title(title="CHAPTER THE FIRST")
    call book1_write_beat("Title only set. Subtitle line should not appear in masthead.")

    call book1_set_chapter_title(title="CHAPTER THE SECOND", subtitle="Derived from a Night of Contraband")
    call book1_write_beat("Title + subtitle set. Route-provenance line should appear below title in masthead.")

    # Empty strings restore the static fallback
    call book1_set_chapter_title(title="", subtitle="")
    call book1_write_beat("Title and subtitle cleared. Static fallback masthead should return.")

    nvl clear
    return


# [TEST] book1_author_thought + book1_clear_author_thought
# Exercises: standalone thought setter, linger across beats, explicit clear.
label test_b1_api_author_thought:
    call test_day2_reset_state
    call test_b1_book1_init

    call book1_set_chapter_title(title="AUTHOR THOUGHT TEST", subtitle="Marginalia Check")

    call book1_write_beat("Author thought test. Margin should be empty at start.")

    call book1_author_thought("Standalone thought via book1_author_thought. Should appear in margin.")
    call book1_write_beat("Prose beat after standalone thought. Thought should linger.")
    call book1_write_beat("Second prose beat — thought still lingers (no clear call yet).")

    call book1_clear_author_thought()
    call book1_write_beat("book1_clear_author_thought called. Margin should now be empty.")

    nvl clear
    return


# ==========================================================
# SECTION B: Vertical slice — refactored day2 predator block
# Calls book1_block_day2_predator_core directly (bypasses
# book1_write_chapter routing overhead) to isolate the new API.
# Exercises: book1_set_chapter_title, book1_write_beat with
# thought/page_break/clear_thought, book1_show_tableau,
# book1_show_plate, and the conditional corruption branch.
# ==========================================================

label test_b1_vertical_slice_predator:
    call test_day2_reset_state

    # [STATE] Predator route with trust break
    $ setattr(player, "inspiration", 22)
    $ setattr(player, "corruption_level", 35)
    $ player.update_stats()

    $ story.set_corridor_state("predator")
    $ story.set_day1_ledger_focus("corruption")
    $ story.set_day2_contraband_state("stolen_wearing")
    $ story.set_day2_tea_choice("predator")
    $ story.set_missy_day2_trust_break(True)

    call test_b1_book1_init

    call book1_block_day2_predator_core

    nvl clear
    return


# ==========================================================
# SECTION C: Integration tests — full chapter routes
# ==========================================================

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
