# ═══════════════════════════════════════════════════════════════
#  variables.rpy
#  All persistent game state in one place.
#  This is the single source of truth for every flag and stat.
#  Never declare defaults anywhere else.
# ═══════════════════════════════════════════════════════════════

default time_manager = TimeManager()
default player       = PlayerStats()
default story        = StoryState()

# HUD sidebar visibility (layout in screens.rpy).
default hud_sidebar_visible = True

# Legacy/alternate sidebar visibility used by screen sidebar().
default sidebar_open = True

# Auto-highlight speaker tracking.
default speaking_char = None

# Suspicion attention pulse state.
default suspicion_focus = None
default suspicion_focus_intensity = 0
