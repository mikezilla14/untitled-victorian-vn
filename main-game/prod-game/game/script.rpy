label start:
    show screen stats_overlay
    show screen sidebar

    scene bg_savoy_front_facade:
        zoom 1.75
    with fade

    sys_msg "Holywell Street Studios — MVP Gray-Box v2.0"
    sys_msg "Setting: The Savoy Hotel, London. Winter 1891."

    cora "The Savoy. Two years old and already the most famous hotel in London. Electric lights in the corridors. Hot water in the suites. And me — Cora, village girl, board school graduate, chambermaid."
    cora "The hotel is quiet this time of year. A skeleton staff. Miss Stern runs the floor like a prison warden, and we have exactly one guest on the VIP floor — a Sir Gideon Locke."
    cora "I send seven shillings home every month. My parents are so proud I secured a position here. If I lose this place..."
    cora "But I didn't come to London just to scrub floors."

    jump day100_main


label check_suspicion:
    if player.anxiety >= 100:
        jump game_over_dismissed
    return


label suspicion_feedback_minor(character, old, new):
    $ suspicion_focus = character
    $ suspicion_focus_intensity = 1
    show screen suspicion_attention(character)
    pause 1.5
    $ suspicion_focus_intensity = 0
    $ suspicion_focus = None
    hide screen suspicion_attention
    return


label suspicion_breakpoint(character, breakpoint, reason=None, scene_context=None):
    $ tier = suspicion_tier(player.get_total_suspicion(character))
    $ anxiety = anxiety_tier(player.anxiety)
    $ line = get_suspicion_monologue(character, tier, anxiety, reason, scene_context)
    $ suspicion_focus = character
    $ suspicion_focus_intensity = 2
    show screen suspicion_attention(character)
    cora_inner "[line]"
    $ suspicion_focus_intensity = 0
    $ suspicion_focus = None
    hide screen suspicion_attention
    return
