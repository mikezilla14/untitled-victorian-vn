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
# Label-based NVL manuscript artifact pilot with legacy macro fallback.
# ==========================================================

init python in book1:
    _constant = True

    CHAPTER_BLOCKS = {
        "day1_slop_chapter": {
            "default": "book1_block_day1_slop_core",
        },
        "day1_chapter": {
            "ghost": "book1_block_day1_ghost_core",
            "predator": "book1_block_day1_predator_core",
            "prey": "book1_block_day1_prey_core",
            "default": "book1_block_day1_default_core",
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
    import re

    # ==========================================================
    # PART 1: LEGACY PARSING & EVALUATION TOOLS
    # ==========================================================
    # DEPRECATED:
    # Book1MacroEngine exists only for legacy payload experiments.
    # New Book1 prose should use label-based prose blocks.

    class Book1MacroEngine(object):
        @staticmethod
        def split_options(block_content):
            """Splits the macro options by semicolon, ignoring semicolons inside quotes."""
            segments = []
            current = []
            in_quotes = False
            for char in block_content:
                if char == '"':
                    in_quotes = not in_quotes
                    current.append(char)
                elif char == ';' and not in_quotes:
                    segments.append("".join(current).strip())
                    current = []
                else:
                    current.append(char)
            remainder = "".join(current).strip()
            if remainder:
                segments.append(remainder)
            return [seg for seg in segments if seg]

        @staticmethod
        def parse_macro_block(block_content):
            """Parses individual options to extract string literals, variables, and conditions."""
            segments = Book1MacroEngine.split_options(block_content)
            options = []
            for segment in segments:
                # Try to match double-quoted string literal
                match = re.match(r'^"([^"]*)"\s*(.*)$', segment, re.DOTALL)
                if match:
                    value, trailing = match.groups()
                    is_literal = True
                else:
                    # Try to match unquoted variable/identifier reference
                    match = re.match(r'^([a-zA-Z0-9_]+)\s*(.*)$', segment)
                    if match:
                        value, trailing = match.groups()
                        is_literal = False
                    else:
                        continue
                
                trailing = trailing.strip()
                if not trailing or trailing == "default":
                    options.append({
                        "value": value,
                        "is_literal": is_literal,
                        "default": True,
                        "cond": None
                    })
                elif trailing.startswith("if "):
                    cond_expr = trailing[3:].strip()
                    options.append({
                        "value": value,
                        "is_literal": is_literal,
                        "default": False,
                        "cond": cond_expr
                    })
            return options

        @staticmethod
        def resolve_variable(var_name):
            """Resolves variable references against BOOK1_COMMON_FRAGMENTS and game singletons."""
            fragments = globals().get("BOOK1_COMMON_FRAGMENTS", {})
            if var_name in fragments:
                return fragments[var_name]
                
            story_obj = globals().get("story")
            if story_obj and hasattr(story_obj, var_name):
                return getattr(story_obj, var_name)
                
            player_obj = globals().get("player")
            if player_obj and hasattr(player_obj, var_name):
                return getattr(player_obj, var_name)
                
            if var_name in globals():
                return globals()[var_name]
                
            return ""

        @staticmethod
        def evaluate_primitive_condition(cond_expr):
            """Evaluates basic flags, negated flags, and comparison operations (numeric or string)."""
            cond_expr = cond_expr.strip()
            if not cond_expr:
                return False
                
            # Match comparison operations: var_name op value (e.g. day1_corridor_state == "prey")
            comp_match = re.match(r'^([a-zA-Z0-9_]+)\s*(>=|<=|==|!=|<|>)\s*(?:"([^"]*)"|\'([^\']*)\'|([a-zA-Z0-9_]+))$', cond_expr)
            if comp_match:
                stat_name, op, val_str_dq, val_str_sq, val_raw = comp_match.groups()
                
                current_val = None
                story_obj = globals().get("story")
                player_obj = globals().get("player")
                if story_obj and hasattr(story_obj, stat_name):
                    current_val = getattr(story_obj, stat_name)
                elif player_obj and hasattr(player_obj, stat_name):
                    current_val = getattr(player_obj, stat_name)
                elif stat_name in globals():
                    current_val = globals()[stat_name]
                    
                if current_val is None:
                    return False
                    
                # Determine expected value and type
                if val_str_dq is not None:
                    expected_val = val_str_dq
                    current_val = str(current_val)
                elif val_str_sq is not None:
                    expected_val = val_str_sq
                    current_val = str(current_val)
                elif val_raw in ("True", "true", "False", "false"):
                    expected_val = val_raw.lower() == "true"
                    current_val = bool(current_val)
                elif val_raw.isdigit():
                    expected_val = int(val_raw)
                    try:
                        current_val = int(current_val)
                    except (ValueError, TypeError):
                        return False
                else:
                    # E.g. checking against another variable
                    expected_val = Book1MacroEngine.resolve_variable(val_raw)
                    if isinstance(current_val, int):
                        try:
                            expected_val = int(expected_val)
                        except (ValueError, TypeError):
                            pass
                    else:
                        current_val = str(current_val)
                        expected_val = str(expected_val)
                        
                if op == '==': return current_val == expected_val
                if op == '!=': return current_val != expected_val
                if op == '>=': return current_val >= expected_val
                if op == '<=': return current_val <= expected_val
                if op == '<': return current_val < expected_val
                if op == '>': return current_val > expected_val

            # Match negated flag
            if cond_expr.startswith("not "):
                flag_name = cond_expr[4:].strip()
                val = None
                story_obj = globals().get("story")
                player_obj = globals().get("player")
                if story_obj and hasattr(story_obj, flag_name):
                    val = getattr(story_obj, flag_name)
                elif player_obj and hasattr(player_obj, flag_name):
                    val = getattr(player_obj, flag_name)
                elif flag_name in globals():
                    val = globals()[flag_name]
                return not bool(val)

            # Match positive flag
            val = None
            story_obj = globals().get("story")
            player_obj = globals().get("player")
            if story_obj and hasattr(story_obj, cond_expr):
                val = getattr(story_obj, cond_expr)
            elif player_obj and hasattr(player_obj, cond_expr):
                val = getattr(player_obj, cond_expr)
            elif cond_expr in globals():
                val = globals()[cond_expr]
            return bool(val)

        @staticmethod
        def evaluate_macro_condition(cond_expr):
            """Evaluates logical compound expressions with and/or, respecting 'and' precedence."""
            or_parts = cond_expr.split(" or ")
            for or_part in or_parts:
                and_parts = or_part.split(" and ")
                and_ok = True
                for and_part in and_parts:
                    if not Book1MacroEngine.evaluate_primitive_condition(and_part):
                        and_ok = False
                        break
                if and_ok:
                    return True
            return False

        @staticmethod
        def evaluate_macro_block(block_content):
            """Scans block options and evaluates the first matching one (first match wins)."""
            options = Book1MacroEngine.parse_macro_block(block_content)
            
            # Check non-default options first (top-to-bottom)
            for opt in options:
                if not opt["default"] and opt["cond"]:
                    if Book1MacroEngine.evaluate_macro_condition(opt["cond"]):
                        val = opt["value"]
                        return val if opt["is_literal"] else Book1MacroEngine.resolve_variable(val)
                        
            # Check default fallback
            for opt in options:
                if opt["default"]:
                    val = opt["value"]
                    return val if opt["is_literal"] else Book1MacroEngine.resolve_variable(val)
                    
            return ""

        @staticmethod
        def resolve_inline_macros(text):
            """Finds all macro blocks and evaluates them. Returns a list of paragraphs."""
            segments = []
            last_idx = 0
            idx = 0
            n = len(text)
            
            while idx < n:
                if text[idx] == '{':
                    start_macro = idx
                    macro_content_chars = []
                    in_dq = False
                    in_sq = False
                    escaped = False
                    depth = 1
                    j = idx + 1
                    
                    while j < n and depth > 0:
                        char = text[j]
                        if escaped:
                            macro_content_chars.append(char)
                            escaped = False
                        elif char == '\\':
                            macro_content_chars.append(char)
                            escaped = True
                        elif char == '"' and not in_sq:
                            in_dq = not in_dq
                            macro_content_chars.append(char)
                        elif char == "'" and not in_dq:
                            in_sq = not in_sq
                            macro_content_chars.append(char)
                        elif not in_dq and not in_sq:
                            if char == '{':
                                depth += 1
                                macro_content_chars.append(char)
                            elif char == '}':
                                depth -= 1
                                if depth > 0:
                                    macro_content_chars.append(char)
                            else:
                                macro_content_chars.append(char)
                        else:
                            macro_content_chars.append(char)
                        j += 1
                    
                    if depth == 0:
                        macro_content = "".join(macro_content_chars).strip()
                        is_macro = False
                        if macro_content:
                            first_char = macro_content[0]
                            if first_char in ('"', "'") or first_char.isalpha() or first_char == '_':
                                has_semi = False
                                tmp_in_dq = False
                                tmp_in_sq = False
                                tmp_esc = False
                                for c in macro_content:
                                    if tmp_esc:
                                        tmp_esc = False
                                    elif c == '\\':
                                        tmp_esc = True
                                    elif c == '"' and not tmp_in_sq:
                                        tmp_in_dq = not tmp_in_dq
                                    elif c == "'" and not tmp_in_dq:
                                        tmp_in_sq = not tmp_in_sq
                                    elif c == ';' and not tmp_in_dq and not tmp_in_sq:
                                        has_semi = True
                                        break
                                if has_semi:
                                    is_macro = True
                                    
                        if is_macro:
                            resolved = Book1MacroEngine.evaluate_macro_block(macro_content)
                            if start_macro > last_idx:
                                segments.append((text[last_idx:start_macro], False))
                            segments.append((resolved, True))
                            last_idx = j
                            idx = j - 1
                idx += 1
                
            if last_idx < n:
                segments.append((text[last_idx:], False))
                
            if len(segments) == 1 and segments[0][1]:
                resolved_val = segments[0][0]
                if isinstance(resolved_val, (list, tuple)):
                    return list(resolved_val)
                return [str(resolved_val)]
                
            parts = []
            for content, was_macro in segments:
                if was_macro:
                    if isinstance(content, (list, tuple)):
                        parts.append(" ".join(str(c) for c in content))
                    else:
                        parts.append(str(content))
                else:
                    parts.append(content)
            return ["".join(parts)]


    # ==========================================================
    # PART 2: LEGACY GAMEPLAY DATA & DICTIONARIES
    # ==========================================================
    # DEPRECATED:
    # Legacy macro fragments and payload dictionaries are quarantined.
    # Active MVP Book1 rendering uses label routes in book1.CHAPTER_BLOCKS.

    BOOK1_COMMON_FRAGMENTS = {
        "missy_name": "Miri",
        "missy_role": "courier",
        "debt_image": "a stain that cannot be laundered out",
        "caldor_pressure": "Lord Caldor corners the heroine by the furnace doors",
        "caldor_voice": "offering terms in a velvet voice",
        "decision_frame": "The chapter refuses euphemism and keeps the moral cost visible.",
        "writing_urgency": "Coralie writes as if dawn will confiscate the pages, every paragraph urgent and thin-breathed.",
        "writing_control": "Coralie writes slowly, pressing each sentence into structure before allowing heat to bloom.",
    }

    BOOK1_PAYLOADS = {}


    # ==========================================================
    # PART 3: LEGACY CORE RESOLUTION FUNCTIONS
    # ==========================================================
    # DEPRECATED:
    # _book1_render_line and build_book1_chapter_packet are fallback
    # helpers for chapters not yet migrated to label-based prose.

    def _book1_render_line(template_line):
        resolved_lines = Book1MacroEngine.resolve_inline_macros(template_line)
        final_lines = []
        for line in resolved_lines:
            final_lines.append(line.format(**BOOK1_COMMON_FRAGMENTS))
        return final_lines

    def build_book1_chapter_packet(chapter_key, include_debug=False):
        chapter = BOOK1_PAYLOADS.get(chapter_key)
        if not chapter:
            return ["(Chapter not found: {})".format(chapter_key)]

        lines = []
        lines.append(chapter.get("title", chapter_key))

        if include_debug:
            lines.append("DEBUG - Chapter: {}".format(chapter_key))

        for line in chapter.get("lines", ()):
            lines.extend(_book1_render_line(line))

        return lines

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
    $ _book1_word_delay = word_delay
    $ _book1_page_line_count = 0
    $ _book1_page_line_limit = 4
    $ book1_page_image = "ui_book_cover"

    if chapter_key == "day1_chapter":
        call book1_nvl_write_line("Chapter I - The Conservatory Door", word_delay=_book1_word_delay)

        # [STATE] State/progression update
        $ _book1_theme = story.day1_corridor_state
    elif chapter_key == "day2_chapter":
        call book1_nvl_write_line("Chapter II - The Hatbox Oath", word_delay=_book1_word_delay)

        # [STATE] State/progression update
        $ _book1_theme = story.day2_tea_choice
    elif chapter_key == "day3_chapter":
        call book1_nvl_write_line("Chapter III - Furnace Parlour", word_delay=_book1_word_delay)

        # [STATE] State/progression update
        $ _book1_theme = story.day3_brush_choice
    elif chapter_key == "day4_triumphant_chapter":
        call book1_nvl_write_line("Chapter IV - The Sealed Envelope", word_delay=_book1_word_delay)

        # [STATE] State/progression update
        $ _book1_theme = story.day2_tea_choice
    elif chapter_key == "day5_reckoning_chapter":
        call book1_nvl_write_line("Chapter V - Diagnosis At Dawn", word_delay=_book1_word_delay)

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

    if _book1_page_line_count >= _book1_page_line_limit:
        nvl clear

        # [STATE] State/progression update
        $ _book1_page_line_count = 0

    # [STATE] State/progression update
    $ _book1_revealed = book1_word_reveal_text(line, word_delay)
    nvl_narrator "[_book1_revealed]"

    # [STATE] State/progression update
    $ _book1_page_line_count += 1

    return


# [DAG_NODE id=book1_set_page_image type=write]
label book1_set_page_image(image_name="ui_book_cover"):

    # [ASSET] Right-frame manuscript illustration update
    $ book1_page_image = image_name
    return

# [DAG_NODE id=book1_debug_chapter_route type=write]
label book1_debug_chapter_route(chapter_key="day2_chapter"):

    nvl clear
    nvl_narrator "DEBUG - Book1 chapter: [chapter_key]"

    if chapter_key == "day1_chapter":

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


