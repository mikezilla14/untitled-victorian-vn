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

# Non-prod balance capture (debug_run_capture.rpy defines BalanceCapture at init -5).
default balance_capture = BalanceCapture()
default debug_grain_overlay_visible = False

# Book 1 engine global state
# Existing primitives (keep):
default _book1_word_delay      = 0.04
default _book1_page_line_count = 0
default _book1_page_line_limit = 4   # defensive fallback only -- not primary pagination
default book1_page_image       = "ui_book_cover"

# MVP payload presentation state:
default book1_page_mode         = "cover"   # cover | tableau | plate | detail | blank
default book1_plate_caption     = ""
default book1_chapter_title     = ""
default book1_chapter_subtitle  = ""
default book1_author_thought    = ""
default book1_author_thought_id = 0         # increments on change, triggers fade-in
default book1_route_provenance  = ""
default book1_show_stats        = False     # must remain False for writing screen

# Background slide used for static game menus (Load, Save, Preferences, etc.).
default game_menu_background_slide = None

# Narrative Pressure UI, Objective Journal, and Manuscript Readiness System defaults
default suspicion = {
    "vance": 0,
    "gideon": 0,
    "stern": 0,
    "missy": 0,
}

default corruption = 0

default manuscript_material = []

default objectives = {
    "obj_prologue_retrieve_pages": {
        "title": "Retrieve Confiscated Pages",
        "description": "Snoop through Lady Eleanor's withdrawing room to find the missing three pages of your manuscript.",
        "category": "story",
        "status": "active",
        "required": True,
        "hidden": False,
        "focus_cost": 0,
        "expires_when": {},
        "rewards": {},
        "risk_text": "",
    }
}

default writing_assignments = {
    "prologue_assignment": {
        "title": "Wiltshire Revelations",
        "chapter_id": "prologue",
        "status": "active",
        "required_material": 3,
        "variants": {
            "respectable": {
                "required_material": 3,
                "min_material_tier": 1,
                "required_tags": [],
                "required_corruption": 0,
                "required_blackmail_material": 0,
            }
        },
        "completion_label": None,
        "available_variants": ["respectable"],
    }
}

default current_assignment_id = "prologue_assignment"
default current_chapter_id = "prologue"
default chapter_focus_remaining = 6

default character_context = {
    "vance": {
        "present": False,
        "location": None,
        "scene_relevant": False,
    },
    "gideon": {
        "present": False,
        "location": None,
        "scene_relevant": False,
    },
    "stern": {
        "present": False,
        "location": None,
        "scene_relevant": False,
    },
    "missy": {
        "present": False,
        "location": None,
        "scene_relevant": False,
    },
}

default draft_quality = {
    "assignment_01": 0,
}

default pending_notification_bundle = None
default journal_tab = "manuscript"
default hud_enabled = True
default cinema_mode = False
default journal_updated_indicator = False