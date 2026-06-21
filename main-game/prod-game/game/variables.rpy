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

# Auto-Highlight speaker tracking
default speaking_char = None

# Set by story_window_penance_gate when pending penance consumes the chain slot.
default _penance_consumed = False

# Background slide used for static game menus (Load, Save, Preferences, etc.).
default game_menu_background_slide = None