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
# book1_non_canon.rpy
# Label-based NVL manuscript engine and routing.
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


# [DAG_NODE id=book1_write_chapter type=write]
label book1_write_chapter(chapter_key="day1_chapter", current_day=101, word_delay=0.04, include_debug=False):

    nvl clear

    if audio_themes_private_ink:
        play music audio_themes_private_ink fadein 1.0

    # [STATE] State/progression update
    $ store._book1_word_delay = word_delay
    $ store._book1_page_line_count = 0
    $ store._book1_page_line_limit = 4
    $ store.book1_page_image = "ui_book_cover"

    if chapter_key == "day1_chapter" or chapter_key == "day1_slop_chapter":
        call book1_nvl_write_line("Chapter I - The Inciting Lever", word_delay=_book1_word_delay)

        # [STATE] State/progression update
        $ _combined_theme = "{}_{}".format(story.day1_corridor_state, story.day1_stern_relation)
        $ _book1_theme = _combined_theme if _combined_theme in book1.CHAPTER_BLOCKS[chapter_key] else story.day1_corridor_state
    elif chapter_key == "day2_chapter":
        call book1_nvl_write_line("Chapter II - The London Train", word_delay=_book1_word_delay)

        # [STATE] State/progression update
        $ _book1_theme = story.day2_tea_choice
    elif chapter_key == "day3_chapter":
        call book1_nvl_write_line("Chapter III - The Savoy's Shadows", word_delay=_book1_word_delay)

        # [STATE] State/progression update
        $ _book1_theme = story.day3_brush_choice
    elif chapter_key == "day4_triumphant_chapter":
        call book1_nvl_write_line("Chapter IV - The Fragile Lord", word_delay=_book1_word_delay)

        # [STATE] State/progression update
        $ _book1_theme = story.day2_tea_choice
    elif chapter_key == "day5_reckoning_chapter":
        call book1_nvl_write_line("Chapter V - A Mask Fixed Forever", word_delay=_book1_word_delay)

        # [STATE] State/progression update
        $ _book1_theme = story.day5_dynamic
    else:

        # [STATE] State/progression update
        $ _book1_theme = "default"

    $ _book1_chapter_map = book1.CHAPTER_BLOCKS.get(chapter_key, {})
    $ _book1_label = _book1_chapter_map.get(_book1_theme, _book1_chapter_map.get("default", "book1_block_unknown_chapter"))

    if include_debug:
        call book1_nvl_write_line("DEBUG - Book1 chapter: [chapter_key]", word_delay=_book1_word_delay)
        call book1_nvl_write_line("DEBUG - Book1 theme: [_book1_theme]", word_delay=_book1_word_delay)
        call book1_nvl_write_line("DEBUG - Book1 block: [_book1_label]", word_delay=_book1_word_delay)

    call expression _book1_label

    nvl clear
    return


# [DAG_NODE id=book1_nvl_write_line type=write]
label book1_nvl_write_line(line, word_delay=0.04):

    if store._book1_page_line_count >= store._book1_page_line_limit:
        nvl clear

        # [STATE] State/progression update
        $ store._book1_page_line_count = 0

    # [STATE] State/progression update
    $ _book1_revealed = book1_word_reveal_text(line, word_delay)
    nvl_narrator "[_book1_revealed]"

    # [STATE] State/progression update
    $ store._book1_page_line_count += 1

    return


# [DAG_NODE id=book1_set_page_image type=write]
label book1_set_page_image(image_name="ui_book_cover"):

    # [ASSET] Right-frame manuscript illustration update
    $ store.book1_page_image = image_name
    return

# [DAG_NODE id=book1_debug_chapter_route type=write]
label book1_debug_chapter_route(chapter_key="day2_chapter"):

    nvl clear
    nvl_narrator "DEBUG - Book1 chapter: [chapter_key]"

    if chapter_key == "day1_chapter" or chapter_key == "day1_slop_chapter":

        # [STATE] State/progression update
        $ _theme = story.day1_corridor_state
    elif chapter_key == "day2_chapter":

        # [STATE] State/progression update
        $ _theme = story.day2_tea_choice
    elif chapter_key == "day3_chapter":

        # [STATE] State/progression update
        $ _theme = story.day3_brush_choice
    elif chapter_key == "day4_triumphant_chapter":

        # [STATE] State/progression update
        $ _theme = story.day2_tea_choice
    elif chapter_key == "day5_reckoning_chapter":

        # [STATE] State/progression update
        $ _theme = story.day5_dynamic
    else:

        # [STATE] State/progression update
        $ _theme = "default"

    $ _chapter_map = book1.CHAPTER_BLOCKS.get(chapter_key, {})
    $ _label = _chapter_map.get(_theme, _chapter_map.get("default", "NO_ROUTE"))

    nvl_narrator "Theme: [_theme]"
    nvl_narrator "Resolved label: [_label]"

    nvl clear
    return


# [DAG_NODE id=book1_block_unknown_chapter type=write]
label book1_block_unknown_chapter:

    call book1_nvl_write_line("(Chapter not found: [chapter_key])", word_delay=_book1_word_delay)
    return


