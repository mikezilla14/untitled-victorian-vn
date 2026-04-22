# ═══════════════════════════════════════════════════════════════
#  script.rpy — ENTRY POINT ONLY
#
#  This file should stay thin. Its only job is to launch the
#  game and hand off to day101.rpy. All other logic lives in its
#  own file. Do not add narrative content or stat manipulation
#  here.
#
#  File load order (Ren'Py loads alphabetically):
#    characters.rpy → classes.rpy → functions.rpy → screens.rpy → variables.rpy
#    → day101.rpy → day102.rpy → day103.rpy → day104.rpy → day105.rpy
#    → endings.rpy → script.rpy
# ═══════════════════════════════════════════════════════════════

label start:
    show screen stats_overlay

    sys "Holywell Street Studios — MVP Gray-Box v2.0"
    sys "Setting: The Savoy Hotel, London. Winter 1891."

    cora "The Savoy. Two years old and already the most famous hotel in London. Electric lights in the corridors. Hot water in the suites. And me — Cora, village girl, board school graduate, chambermaid."
    cora "The hotel is quiet this time of year. A skeleton staff. Miss Stern runs the floor like a prison warden, and we have exactly one guest on the VIP floor — a Sir Gideon Locke."
    cora "I send seven shillings home every month. My parents are so proud I secured a position here. If I lose this place..."
    cora "But I didn't come to London just to scrub floors."

    jump day1_morning


# ── GLOBAL GUARD LABEL ─────────────────────────────────────────
# Called after stat-modifying choices and before passive decay.
# If suspicion has hit 100, the run ends immediately.
label check_suspicion:
    if player.suspicion >= 100:
        jump game_over_dismissed
    return
