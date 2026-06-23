# ==========================================================
# book1.rpy
# Book1 manuscript engine -- routing, rendering, and visual
# API for the penny dreadful payload layer.
#
# Architecture:
#   book1_write_chapter(...)        Entry point called by day scripts
#   book1_write_beat(...)           Primary prose API (preferred)
#   book1_nvl_write_line(...)       Low-level word-reveal primitive
#   book1_set_visual(...)           Core visual controller
#   book1_show_*(...)               Convenience wrappers
#   book1_set_chapter_title(...)    Masthead + route-provenance subtitle
#   book1_author_thought(...)       Standalone marginalia setter
#   book1_apply_visual_transition(...)  Centralised transition dispatch
#
# State isolation rule:
#   Book1 reads resolved hotel state. It NEVER mutates story, player,
#   time_manager, or persistent state. Day scripts own gameplay state.
#   Book1 owns presentation and manuscript rendering.
# ==========================================================

init python in book1:
    _constant = True

    CHAPTER_BLOCKS = {
        "day1_slop_chapter": {
            "ghost": "book1_block_day1_ghost_core",
            "predator": "book1_block_day1_predator_core",
            "prey": "book1_block_day1_prey_core",
            "ghost_subservient": "book1_block_day1_ghost_subservient",
            "predator_complicit": "book1_block_day1_predator_complicit",
            "prey_resistant": "book1_block_day1_prey_resistant",
            "default": "book1_block_day1_default_core",
        },
        "day1_chapter": {
            "ghost": "book1_block_day1_alt_ghost_core",
            "predator": "book1_block_day1_alt_predator_core",
            "prey": "book1_block_day1_alt_prey_core",
            "ghost_subservient": "book1_block_day1_alt_ghost_subservient",
            "predator_complicit": "book1_block_day1_alt_predator_complicit",
            "prey_resistant": "book1_block_day1_alt_prey_resistant",
            "default": "book1_block_day1_alt_default_core",
        },
        "day2_chapter": {
            "ghost": "book1_block_day2_ghost_core",
            "predator": "book1_block_day2_predator_core",
            "prey": "book1_block_day2_prey_core",
            "default": "book1_block_day2_default_core",
        },
        "day3_chapter": {
            "ghost": "book1_block_day3_ghost_core",
            "predator": "book1_block_day3_predator_core",
            "prey": "book1_block_day3_prey_core",
            "default": "book1_block_day3_default_core",
        },
        "day4_triumphant_chapter": {
            "ghost": "book1_block_day4_ghost_core",
            "predator": "book1_block_day4_predator_core",
            "prey": "book1_block_day4_prey_core",
            "default": "book1_block_day4_default_core",
        },
        "day5_reckoning_chapter": {
            "muse": "book1_block_day5_muse_core",
            "protege": "book1_block_day5_protege_core",
            "adversary": "book1_block_day5_adversary_core",
            "witness": "book1_block_day5_witness_core",
            "default": "book1_block_day5_default_core",
        },
    }


init python:
    def book1_word_reveal_text(line, word_delay=0.04):
        words = line.split()
        if not words:
            return line
        return ("{w=" + str(word_delay) + "} ").join(words)


# -- MODULE A: PROSE ROUTER ----------------------------------------------
# Entry point called by day scripts and harness tests.
# Resolves theme -> chapter block label, initialises all Book1
# presentation state, then delegates to the block label.
# Must not mutate story, player, or time_manager.

# [DAG_NODE id=book1_write_chapter type=write]
label book1_write_chapter(chapter_key="day1_chapter", current_day=101, word_delay=0.04, include_debug=False):

    nvl clear

    if audio_themes_private_ink:
        play music audio_themes_private_ink fadein 1.0

    # _book1_page_line_limit is a defensive fallback only; page flow
    # is controlled through authored page_break beats, not line counting.

    $ store._book1_word_delay       = word_delay
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

    # Chapter title is now owned by the block label via book1_set_chapter_title.
    if chapter_key == "day1_chapter" or chapter_key == "day1_slop_chapter":

        $ _combined_theme = "{}_{}".format(story.day1_corridor_state, story.day1_stern_relation)
        $ _book1_theme = _combined_theme if _combined_theme in book1.CHAPTER_BLOCKS[chapter_key] else story.day1_corridor_state

    elif chapter_key == "day2_chapter":

        $ _book1_theme = story.day2_tea_choice

    elif chapter_key == "day3_chapter":

        $ _book1_theme = story.day3_brush_choice

    elif chapter_key == "day4_triumphant_chapter":

        $ _book1_theme = story.day2_tea_choice

    elif chapter_key == "day5_reckoning_chapter":

        $ _book1_theme = story.day5_dynamic

    else:

        $ _book1_theme = "default"

    $ _book1_chapter_map = book1.CHAPTER_BLOCKS.get(chapter_key, {})
    $ _book1_label = _book1_chapter_map.get(_book1_theme, _book1_chapter_map.get("default", "book1_block_unknown_chapter"))

    if include_debug:
        call book1_nvl_write_line("DEBUG - chapter_key: [chapter_key]", word_delay=_book1_word_delay)
        call book1_nvl_write_line("DEBUG - theme: [_book1_theme]", word_delay=_book1_word_delay)
        call book1_nvl_write_line("DEBUG - block: [_book1_label]", word_delay=_book1_word_delay)

    call expression _book1_label

    nvl clear
    return


# -- MODULE B: PROSE RENDERER --------------------------------------------

# Low-level word-reveal primitive. Kept for compatibility.
# Prefer book1_write_beat for new prose.
label book1_nvl_write_line(line, word_delay=0.04):

    if audio_sfx_ink_scratch:
        play sound audio_sfx_ink_scratch

    # Defensive overflow guard -- not the primary pagination mechanism.
    if store._book1_page_line_count >= store._book1_page_line_limit:
        nvl clear

        $ store._book1_page_line_count = 0

    $ _book1_revealed = book1_word_reveal_text(line, word_delay)
    nvl_narrator "[_book1_revealed]"

    $ store._book1_page_line_count += 1
    return


# Primary prose beat API. Use this for all new Book1 prose.
# Unifies prose text, optional author thought, and intentional page breaks.
label book1_write_beat(text, thought=None, word_delay=None, page_break=False, clear_thought=False):

    if page_break:
        nvl clear

        $ store._book1_page_line_count = 0

    if word_delay is None:

        $ word_delay = store._book1_word_delay

    if thought is not None:

        $ store.book1_author_thought    = thought
        $ store.book1_author_thought_id += 1

    call book1_nvl_write_line(text, word_delay=word_delay)

    if clear_thought:

        $ store.book1_author_thought = ""

    return


# -- MODULE C: AUTHOR THOUGHT RENDERER -----------------------------------
# Standalone helpers for when a thought must linger across multiple
# prose beats. Prefer the thought= param on book1_write_beat.

label book1_author_thought(text, linger=True):

    $ store.book1_author_thought    = text
    $ store.book1_author_thought_id += 1
    return


label book1_clear_author_thought():

    $ store.book1_author_thought = ""
    return


# -- MODULE D: VISUAL CONTROLLER -----------------------------------------

# Core visual state setter. Called by all convenience wrappers.
label book1_set_visual(image_name="ui_book_cover", mode="cover", caption="", transition="dissolve"):

    $ store.book1_page_image    = image_name
    $ store.book1_page_mode     = mode
    $ store.book1_plate_caption = caption
    call book1_apply_visual_transition(transition)
    return


# Compatibility wrapper -- keeps existing call sites working.
# [DAG_NODE id=book1_set_page_image type=write]
label book1_set_page_image(image_name="ui_book_cover"):
    call book1_set_visual(image_name=image_name, mode="cover", caption="", transition="none")
    return


# Chapter masthead + route-provenance subtitle setter.
# Call early in each chapter block so the provenance cue appears
# on the first screen the player sees.
label book1_set_chapter_title(title="", subtitle=""):

    $ store.book1_chapter_title    = title
    $ store.book1_chapter_subtitle = subtitle
    return


# -- MODULE E: PAGE MODE CONVENIENCE WRAPPERS ----------------------------

label book1_show_cover():
    call book1_set_visual("ui_book_cover", mode="cover", caption="", transition="dissolve")
    return


label book1_show_tableau(image_name, caption=""):
    # transition="none": illustration changes mid-NVL must snap.
    # "dissolve" captures and blends the whole NVL screen, causing a jarring refresh.
    call book1_set_visual(image_name=image_name, mode="tableau", caption=caption, transition="none")
    return


# If image_name is None, reuses the current tableau through runtime
# plate treatment applied by the screen.
label book1_show_plate(image_name=None, caption=""):
    if image_name is None:

        $ image_name = store.book1_page_image
    # transition="none": plate treatment snaps onto the existing image.
    # "fade" causes a full-screen blackout in NVL context because with fade
    # applies to the master layer, not just the illustration frame.
    call book1_set_visual(image_name=image_name, mode="plate", caption=caption, transition="none")
    return


label book1_show_detail(image_name, caption=""):
    call book1_set_visual(image_name=image_name, mode="detail", caption=caption, transition="none")
    return


label book1_show_blank(caption=""):
    call book1_set_visual(image_name="ui_book_blank", mode="blank", caption=caption, transition="none")
    return


# -- MODULE F: TRANSITION LAYER ------------------------------------------
# Centralised so visual language can improve without touching prose labels.
# page_turn_stub / ink_spread_stub / plate_transform_stub are named
# placeholders for future animation upgrades.

label book1_apply_visual_transition(transition="dissolve"):
    if transition == "fade":

        with fade
    elif transition == "dissolve":

        with dissolve
    # else "none" or unknown: no transition applied
    return



# -- FALLBACK ----------------------------------------------------

# [DAG_NODE id=book1_block_unknown_chapter type=write]
label book1_block_unknown_chapter:
    call book1_nvl_write_line("(Chapter block not found for route: [_book1_label])", word_delay=_book1_word_delay)
    return


