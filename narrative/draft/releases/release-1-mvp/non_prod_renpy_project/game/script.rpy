label start:
    show screen stats_overlay

    scene bg_savoy_front_facade:
        zoom 1.0
        xysize (1920,1080)
    with fade

    sys_msg "Holywell Street Studios — MVP Gray-Box v2.0"
    sys_msg "Setting: The Savoy Hotel, London. Winter 1891."

    cora "The Savoy. Two years old and already the most famous hotel in London. Electric lights in the corridors. Hot water in the suites. And me — Cora, village girl, board school graduate, chambermaid."
    cora "The hotel is quiet this time of year. A skeleton staff. Miss Stern runs the floor like a prison warden, and we have exactly one guest on the VIP floor — a Sir Gideon Locke."
    cora "I send seven shillings home every month. My parents are so proud I secured a position here. If I lose this place..."
    cora "But I didn't come to London just to scrub floors."

    jump day101_main


label thought_overlay_test:
show screen stats_overlay
    # Writer contract verification for the dual-layer thought overlay system.
    # This label is sandbox-only and must not be promoted to production.
    scene bg_savoy_corridor_morning with dissolve
    show stern_sprite neutral:
        zoom 0.25 
        xpos 0.66
        ypos 0.25

    stern "It's a most fascinating structure."
    cora_inner "She's not looking at the building."
    cora_inner "She's watching him."
    stern "Don't you agree?"

    return


label check_suspicion:
    if player.anxiety >= 100:
        jump game_over_dismissed
    return
