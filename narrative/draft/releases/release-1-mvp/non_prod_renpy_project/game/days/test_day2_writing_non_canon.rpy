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

        "Render book1 prose directly: day2_chapter (predator)":

            # [STATE] State/progression update
            jump test_day2_render_book1_day2_predator

        "Render book1 prose directly: day2_chapter (ghost + misdirect + stern/missy pressure)":

            # [STATE] State/progression update
            jump test_day2_render_book1_day2_ghost

        "Render book1 prose directly: day2_chapter (prey + partial confession)":

            # [STATE] State/progression update
            jump test_day2_render_book1_day2_prey

        "Run inline macro engine unit tests":

            # [STATE] State/progression update
            jump test_book1_inline_macros


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

    call book1_write_chapter(chapter_key="day2_chapter", current_day=102, include_debug=True)
    return


label test_book1_inline_macros:
    call test_day2_reset_state
    
    python:
        # Define some test fragments in BOOK1_COMMON_FRAGMENTS for testing
        BOOK1_COMMON_FRAGMENTS["test_paragraph_list"] = [
            "This is paragraph one of the variable reference.",
            "This is paragraph two of the variable reference."
        ]
        BOOK1_COMMON_FRAGMENTS["test_single_string"] = "This is a single string variable."
        
        # Test Case 1: Simple Literal Option (first match wins)
        story.obsession = 60
        story.writer_route = True
        
        test_str1 = "{ \"silence\" default; \"pen\" if writer_route; \"obsession\" if obsession >= 60; }"
        res1 = Book1MacroEngine.resolve_inline_macros(test_str1)
        assert res1 == ["pen"], "Expected ['pen'], got {}".format(res1)
        
        # Test Case 2: Primitive logical condition
        story.writer_route = False
        res2 = Book1MacroEngine.resolve_inline_macros(test_str1)
        assert res2 == ["obsession"], "Expected ['obsession'], got {}".format(res2)
        
        # Test Case 3: Default fallback
        story.obsession = 30
        res3 = Book1MacroEngine.resolve_inline_macros(test_str1)
        assert res3 == ["silence"], "Expected ['silence'], got {}".format(res3)
        
        # Test Case 4: Compound conditions (and/or precedence)
        story.obsession = 55
        player.corruption_level = 6
        test_str4 = "{ \"no\" default; \"yes\" if obsession >= 50 and corruption_level >= 5; }"
        res4 = Book1MacroEngine.resolve_inline_macros(test_str4)
        assert res4 == ["yes"], "Expected ['yes'], got {}".format(res4)
        
        player.corruption_level = 2
        res4_fail = Book1MacroEngine.resolve_inline_macros(test_str4)
        assert res4_fail == ["no"], "Expected ['no'], got {}".format(res4_fail)
        
        # Test 'or' condition:
        test_str4_or = "{ \"no\" default; \"yes\" if obsession >= 60 or corruption_level >= 5; }"
        res4_or = Book1MacroEngine.resolve_inline_macros(test_str4_or)
        assert res4_or == ["no"], "Expected ['no'], got {}".format(res4_or)
        
        player.corruption_level = 7
        res4_or_ok = Book1MacroEngine.resolve_inline_macros(test_str4_or)
        assert res4_or_ok == ["yes"], "Expected ['yes'], got {}".format(res4_or_ok)
        
        # Test Case 5: Variable references (strings)
        test_str5 = "She said { test_single_string default; } to the maid."
        res5 = Book1MacroEngine.resolve_inline_macros(test_str5)
        assert res5 == ["She said This is a single string variable. to the maid."], "Expected resolved string, got {}".format(res5)
        
        # Test Case 6: Variable references (multi-paragraph lists) - Full line macro
        test_str6 = "{ test_paragraph_list default; }"
        res6 = Book1MacroEngine.resolve_inline_macros(test_str6)
        expected_list = [
            "This is paragraph one of the variable reference.",
            "This is paragraph two of the variable reference."
        ]
        assert res6 == expected_list, "Expected paragraphs list, got {}".format(res6)
        
        # Test Case 7: Ren'Py styling tag safety
        test_str7 = "This is a {b}bold{/b} text with macro: { \"yes\" default; }."
        res7 = Book1MacroEngine.resolve_inline_macros(test_str7)
        assert res7 == ["This is a {b}bold{/b} text with macro: yes."], "Expected tag preserved, got {}".format(res7)
        
        # Test Case 8: Multi-line option layout
        test_str8 = """{
          "Line 1" if writer_route;
          "Line 2" default;
        }"""
        res8 = Book1MacroEngine.resolve_inline_macros(test_str8)
        assert res8 == ["Line 2"], "Expected ['Line 2'], got {}".format(res8)
        
        # Test Case 9: String equality comparison
        story.set_corridor_state("prey")
        test_str9 = "{ \"is prey\" if day1_corridor_state == \"prey\"; \"not prey\" default; }"
        res9 = Book1MacroEngine.resolve_inline_macros(test_str9)
        assert res9 == ["is prey"], "Expected ['is prey'], got {}".format(res9)
        
        # Test Case 10: String inequality comparison
        test_str10 = "{ \"is not prey\" if day1_corridor_state != \"prey\"; \"is prey\" default; }"
        res10 = Book1MacroEngine.resolve_inline_macros(test_str10)
        assert res10 == ["is prey"], "Expected ['is prey'], got {}".format(res10)
        
        story.set_corridor_state("ghost")
        res10_ghost = Book1MacroEngine.resolve_inline_macros(test_str10)
        assert res10_ghost == ["is not prey"], "Expected ['is not prey'], got {}".format(res10_ghost)

        # Test Case 11: Bool equality comparison
        story.set_missy_day2_trust_break(True)
        test_str11 = "{ \"break\" if missy_day2_trust_break == True; \"no break\" default; }"
        res11 = Book1MacroEngine.resolve_inline_macros(test_str11)
        assert res11 == ["break"], "Expected ['break'], got {}".format(res11)
        
        # Clean up test fragments
        BOOK1_COMMON_FRAGMENTS.pop("test_paragraph_list", None)
        BOOK1_COMMON_FRAGMENTS.pop("test_single_string", None)
        
    nvl clear
    nvl_narrator "Inline Prose Macro Unit Tests passed successfully!"
    nvl clear
    return
