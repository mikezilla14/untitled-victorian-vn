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

# Book 1 engine global state
default _book1_word_delay       = 0.04
default _book1_page_line_count  = 0
default _book1_page_line_limit  = 4
default book1_page_image        = "ui_book_cover"
default book1_page_mode         = "cover"
default book1_plate_caption     = ""
default book1_chapter_title     = ""
default book1_chapter_subtitle  = ""
default book1_author_thought    = ""
default book1_author_thought_id = 0
default book1_route_provenance  = ""
default book1_show_stats        = False
