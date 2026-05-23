label start:
    show screen stats_overlay

    scene bg_savoy_front_facade
    with fade

    sys_msg "Holywell Street Studios — MVP Gray-Box v2.0"
    sys_msg "Setting: The Savoy Hotel, London. Winter 1891."

    cora "The Savoy. Two years old and already the most famous hotel in London. Electric lights in the corridors. Hot water in the suites. And me — Cora, village girl, board school graduate, chambermaid."
    cora "The hotel is quiet this time of year. A skeleton staff. Miss Stern runs the floor like a prison warden, and we have exactly one guest on the VIP floor — a Sir Gideon Locke."
    cora "I send seven shillings home every month. My parents are so proud I secured a position here. If I lose this place..."
    cora "But I didn't come to London just to scrub floors."

    jump day101_main


label check_suspicion:
    if player.suspicion >= 100:
        jump game_over_dismissed
    return
