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

# ═══════════════════════════════════════════════════════════════
#  classes_non_canon.rpy
#  Writers' Room — promotion source for main-game/prod-game/game/classes.rpy
#
#  NOT loaded at runtime. During Release 1 promotion, merge this file into
#  classes.rpy (or diff-merge the marked StoryState chain sections).
#  Baseline synced from main-game/prod-game/game/classes.rpy at promotion time.
# ═══════════════════════════════════════════════════════════════

init -1 python:

    class TimeManager(object):
        ALLOWED_PERIODS = (
            "Early Morning",
            "Morning",
            "Afternoon",
            "Evening",
            "Night",
            "Late Night",
        )

        def __init__(self):
            self.current_day = 1
            self._time_of_day = "Morning"
            self.last_displayed_day = None
            self.last_displayed_period = None

        @property
        def time_of_day(self):
            return self._time_of_day

        @time_of_day.setter
        def time_of_day(self, value):
            if value not in self.ALLOWED_PERIODS:
                raise ValueError(
                    "Invalid time_of_day '{}'. Allowed values: {}".format(
                        value, ", ".join(self.ALLOWED_PERIODS)
                    )
                )
            self._time_of_day = value

        def set_time_of_day(self, value):
            self.time_of_day = value

        def set_current_day(self, value):
            if not isinstance(value, int):
                raise TypeError("current_day must be an int, got {}".format(type(value).__name__))
            if value < 1:
                raise ValueError("current_day must be >= 1")
            self.current_day = value

    class PlayerStats(object):
        def __init__(self):
            # Core Stats
            self.corruption_level = 1
            self.corruption_xp = 0
            self.inspiration = 0
            self.anxiety = 0
            
            # Archetype Focus counters
            self.ghost_focus = 0
            self.prey_focus = 0
            self.predator_focus = 0
            
            # TWO-TIERED SUSPICION: Base (Permanent) + Acute (Temporary Heat)
            self.stern_base_susp = 0
            self.stern_acute_susp = 0
            
            self.vance_base_susp = 0
            self.vance_acute_susp = 0
            
            self.gideon_base_susp = 0
            self.gideon_acute_susp = 0
            
            # Chapter 2 Future-proofing
            self.missy_base_susp = 0
            self.missy_acute_susp = 0
            
            # The Tracking List
            self.tracked_characters = ["stern", "vance", "gideon", "missy"]
            self.suspicion_breakpoints_seen = {
                "stern": [],
                "vance": [],
                "gideon": [],
                "missy": [],
            }
            
            # ASYMPTOTIC DECAY RATES (d)
            self.decay_rates = {
                "stern": 0.15,   # Slow decay: Requires grueling labor
                "vance": 0.60,   # Rapid reset: Oblivious to 'furniture'
                "gideon": 0.50,  # Shifting equation: High initially, drops to 0.0 later
                "missy": 0.90    # Instant decay: The Teflon Slate, eager for a friend
            }

            # Anxiety Warnings & Threshold tracking
            self.has_reached_70_before = False
            self.has_reached_75_before = False
            self.anxiety_70_warning_shown = False
            self.anxiety_75_warning_shown = False

        CONFRONTATION_THRESHOLD = 50
        ANXIETY_THRESHOLD = 70

        @property
        def inspiration_cap(self):
            return 50

        # ── Backward-compatible properties for existing .rpy script checks ──
        @property
        def stern_suspicion(self):
            return self.get_total_suspicion("stern")

        @property
        def vance_suspicion(self):
            return self.get_total_suspicion("vance")

        @property
        def missy_suspicion(self):
            return self.get_total_suspicion("missy")

        @property
        def gideon_suspicion(self):
            return self.get_total_suspicion("gideon")

        def get_total_suspicion(self, char):
            """Calculates Total Suspicion (Base + Acute) for a character, strictly capped at 100."""
            base = getattr(self, "{}_base_susp".format(char), 0)
            acute = getattr(self, "{}_acute_susp".format(char), 0)
            return max(0, min(100, base + acute))

        def _ensure_suspicion_breakpoints_seen(self):
            if not hasattr(self, "suspicion_breakpoints_seen"):
                self.suspicion_breakpoints_seen = {}
            for char in self.tracked_characters:
                if char not in self.suspicion_breakpoints_seen:
                    self.suspicion_breakpoints_seen[char] = []

        def record_suspicion_breakpoints(self, character, breakpoints):
            """Record newly crossed suspicion breakpoints and return only unseen values."""
            self._ensure_suspicion_breakpoints_seen()
            seen = self.suspicion_breakpoints_seen[character]
            newly_seen = []
            for breakpoint in breakpoints:
                if breakpoint not in seen:
                    seen.append(breakpoint)
                    newly_seen.append(breakpoint)
            seen.sort()
            return newly_seen

        def recalculate_anxiety(self):
            """
            Calculates Anxiety using Independent Probability.
            Anxiety = 100 * (1 - product_of(1 - (Suspicion_i / 100)))
            Enforces strict clamping at every stage.
            """
            # Strict Clamping Safeguard: Cap the sum of Base and Acute suspicion at 100
            for char in self.tracked_characters:
                base_attr = "{}_base_susp".format(char)
                acute_attr = "{}_acute_susp".format(char)
                
                if hasattr(self, base_attr) and hasattr(self, acute_attr):
                    # Clamp permanent base suspicion first to [0, 100]
                    base_val = max(0, min(100, getattr(self, base_attr)))
                    setattr(self, base_attr, base_val)
                    
                    # Clamp acute suspicion to the remaining headroom [0, 100 - base]
                    acute_val = max(0, min(100 - base_val, getattr(self, acute_attr)))
                    setattr(self, acute_attr, acute_val)

            probability_of_safety = 1.0
            
            for char in self.tracked_characters:
                susp_val = self.get_total_suspicion(char)
                # Probability that this specific character does NOT catch Cora
                char_safety = 1.0 - (susp_val / 100.0)
                probability_of_safety *= char_safety
                
            # Anxiety is the probability of getting caught by ANYONE, capped at 100
            raw_anxiety = 100.0 * (1.0 - probability_of_safety)
            self.anxiety = max(0, min(100, int(round(raw_anxiety))))

        def update_stats(self):
            self.recalculate_anxiety()

            # Corruption XP must never be below 0.
            self.corruption_xp = max(0, self.corruption_xp)

            while self.corruption_xp >= 20:
                self.corruption_xp -= 20
                self.corruption_level += 1

            # Inspiration must never be below 0 or above the current cap.
            self.inspiration = max(0, min(self.inspiration_cap, self.inspiration))

        def gain_inspiration(self, amount):
            if amount < 0:
                raise ValueError("gain_inspiration() cannot receive a negative amount. Use spend_inspiration().")

            self.inspiration += amount
            self.update_stats()

        def spend_inspiration(self, amount):
            if amount < 0:
                raise ValueError("spend_inspiration() cannot receive a negative amount.")

            if self.inspiration >= amount:
                self.inspiration -= amount
                self.update_stats()
                return True

            return False

        def gain_corruption_xp(self, amount):
            if amount < 0:
                raise ValueError("Corruption cannot decrease.")

            self.corruption_xp += amount
            self.update_stats()

        def add_suspicion(self, char, acute_amount=0, base_amount=0):
            """Helper function to add heat/permanent suspicion and instantly update Anxiety."""
            if char in self.tracked_characters:
                current_acute = getattr(self, "{}_acute_susp".format(char), 0)
                current_base = getattr(self, "{}_base_susp".format(char), 0)
                
                # Apply changes and clamp individually between 0 and 100
                new_acute = max(0, min(100, current_acute + acute_amount))
                new_base = max(0, min(100, current_base + base_amount))
                
                setattr(self, "{}_acute_susp".format(char), new_acute)
                setattr(self, "{}_base_susp".format(char), new_base)
                
                self.update_stats()

        def appease_character(self, char, custom_rate=None):
            """
            Burns off Acute Suspicion using the Asymptotic Decay formula.
            S_t = S_0 * (1 - d)
            """
            if char not in self.tracked_characters:
                return

            # Use custom rate if provided (e.g., Gideon's trap), otherwise use character default
            rate = custom_rate if custom_rate is not None else self.decay_rates.get(char, 0.0)
            current_acute = getattr(self, "{}_acute_susp".format(char), 0)
            
            # Apply asymptotic decay and clamp individually to [0, 100]
            new_acute = max(0, min(100, current_acute * (1.0 - rate)))
            
            # If the ghost value drops below 1%, we snap it to 0 for clean UI
            if new_acute < 1.0:
                new_acute = 0
                
            setattr(self, "{}_acute_susp".format(char), new_acute)
            self.update_stats()

        def adjust_character_suspicion(self, character, amount):
            """Backwards-compatible helper mapping standard modifications to acute suspicion."""
            self.add_suspicion(character, acute_amount=amount)

        def is_confrontation_ready(self, char):
            """Returns True if char's total suspicion has reached the confrontation threshold."""
            return self.get_total_suspicion(char) >= self.CONFRONTATION_THRESHOLD

        def is_anxiety_ready(self):
            """Returns True if Cora's anxiety has reached or exceeded the dangerous threshold."""
            return self.anxiety >= self.ANXIETY_THRESHOLD

        def relieve_downtime_anxiety(self):
            """
            Relieves anxiety by dynamically decreasing suspicion for all characters
            based on their profile (decay rates and current suspicion levels).
            """
            for char in self.tracked_characters:
                current_acute = getattr(self, "{}_acute_susp".format(char), 0)
                if current_acute > 0:
                    if char == "stern":
                        rate = 0.30
                        min_drop = 12
                    elif char == "vance":
                        rate = 0.70
                        min_drop = 20
                    elif char == "missy":
                        rate = 0.95
                        min_drop = 25
                    else:  # gideon / fallback
                        rate = 0.60
                        min_drop = 15

                    reduction = max(min_drop, int(round(current_acute * rate)))
                    new_acute = max(0, current_acute - reduction)
                    setattr(self, "{}_acute_susp".format(char), new_acute)
            self.update_stats()

        def has_story_fuel(self, required_insp=30, required_corr=3):
            """
            Read-only writing-gate check (AND, not sum).
            Returns True only when BOTH inspiration and corruption_level meet their floors.
            """
            return self.inspiration >= required_insp and self.corruption_level >= required_corr

    class StoryState(object):

        # ── Archetype Focus ────────────────────────────────────────────
        VALID_ARCHETYPE_SEEDS            = ("none", "ghost", "prey", "predator")
        VALID_ARCHETYPE_FOCUS_STATES     = ("none", "ghost", "prey", "predator")

        # ── Prologue ───────────────────────────────────────────────────
        VALID_PROLOGUE_FOUND_STATES      = ("none", "overheard", "read_letters")
        VALID_PROLOGUE_WHY_WRITE_STATES  = ("none", "money_home", "cataloguer", "scandal_hungry")
        VALID_PROLOGUE_HOLYWELL_STATES   = ("none", "careful", "eager", "desperate")

        # ── Day 1 ──────────────────────────────────────────────────────
        VALID_CORRIDOR_STATES        = ("none", "ghost", "predator", "prey")
        VALID_INTERVIEW_STATES       = ("none", "meek", "competent")
        VALID_LEDGER_FOCUS_STATES    = ("none", "inspiration", "corruption")
        VALID_DAY1_NIGHT_ACTIONS     = ("none", "write", "visit_missy")
        VALID_MISSY_DAY1_TRUST_STATES = ("none", "soothed", "unsettled", "warned_cora", "shared_caution")

        # ── Day 2 ──────────────────────────────────────────────────────
        VALID_CONTRABAND_STATES           = ("none", "stolen_wearing", "planted_in_trunk")
        VALID_MISSY_DAY2_SUSPICION_STATES = ("none", "uneasy", "trusting")
        VALID_CHORE_FOCUS_STATES          = ("none", "inspiration", "corruption")
        VALID_TEA_CHOICE_STATES           = ("none", "prey", "predator", "ghost")
        VALID_DAY2_NIGHT_ACTIONS          = ("none", "write", "indulge")

        # ── Day 3 ──────────────────────────────────────────────────────
        VALID_CORRIDOR_CHAIN_STATES  = ("none", "inspiration", "corruption")
        VALID_BRUSH_CHOICE_STATES    = ("none", "predator", "prey", "ghost")
        VALID_DAY3_TWILIGHT_ACTIONS  = ("none", "frantic_write", "prepare_mask", "indulge_words")
        VALID_DAY3_STERN_RESPONSES   = ("none", "boring", "partial_truth", "stupid")
        VALID_ULTIMATUM_STATES       = ("none", "defied", "bargained", "surrendered")
        VALID_DAY3_NIGHT_ACTIONS     = ("none", "write", "barricade")

        # ── Day 4 ──────────────────────────────────────────────────────
        VALID_ESCAPE_STATES              = ("none", "fireplace", "bold_lie", "missy_cover")
        VALID_DAY4_STERN_RESPONSES       = ("none", "boring", "frightened", "missy_cover")
        VALID_DAY4_TWILIGHT_ACTIONS      = ("none", "atonement", "missy_repair")
        VALID_MISSY_DAY4_REPAIR_STATES   = ("none", "partial_truth", "comfort_lie")
        VALID_DAY4_NIGHT_ACTIONS         = ("none", "finish_manuscript")

        # ── Day 5 ──────────────────────────────────────────────────────
        VALID_DAY5_DYNAMICS         = ("none", "muse", "protege", "adversary", "witness")
        VALID_RELEASE1_FLAVOURS     = ("none", "observer", "predator", "prey", "ghost")
        VALID_MONEY_CHOICES         = ("none", "taken", "refused", "deferred")
        VALID_ENTANGLEMENT_LEVELS   = ("none", "accepted_money", "refused_money", "deferred_money")

        # ── Release 2 carry-forward ────────────────────────────────────
        VALID_RELEASE2_GIDEON_STATUSES = ("none", "marked_cora")
        VALID_RELEASE2_MISSY_STATUSES  = ("none", "wounded_trust", "uncertain_trust")

        # ── PROMOTE: Optional character grind chains (Release 1 REFLECT) ──
        VALID_CHAIN_CHARACTERS     = ("stern", "missy", "vance")
        MAX_CHARACTER_CHAIN_LEVEL  = 3

        # Maps (day, time_of_day) → (next_day, next_time, next_label).
        # Used by advance_after_confrontation. Add one entry per new day/slot.
        # DEPRECATED compatibility route table for the old route-owner pattern.
        # New time-period routing uses explicit day labels plus dynamic windows
        # that call optional content and return to the day spine.
        POST_PENANCE_ROUTES = {
            (1, "Morning"):   (1, "Night",     "day101_4_writing_or_visiting"),
            (1, "Evening"):   (2, "Morning",   "day102_1_cora_missy_first_shift"),
            (1, "Night"):     (2, "Morning",   "day102_1_cora_missy_first_shift"),
            (2, "Morning"):   (2, "Evening",   "day102_3_stern_fetches_cora"),
            (2, "Afternoon"): (2, "Evening",   "day102_3_stern_fetches_cora"),
            (2, "Night"):     (3, "Morning",   "day103_morning"),
            (3, "Morning"):   (3, "Afternoon", "day103_2_suite_gideon_tea"),
            (3, "Afternoon"): (3, "Night",     "day103_4_room_stern_suspicion"),
            (3, "Evening"):   (3, "Night",     "day103_4_room_stern_suspicion"),
            (3, "Night"):     (4, "Morning",   "day104_1_false_dawn_suite_window"),
            (4, "Evening"):   (4, "Night",     "day104_5_triumphant_chapter"),
            (4, "Night"):     (5, "Morning",   "day105_1_monster_reemerges"),
        }

        # Maps outcome string → (next_day_or_None, next_time_or_None, next_label).
        # Used by end_slot. None values mean "leave day/time unchanged".
        # d4_twilight_done is handled in get_slot_exit_target() due to conditional label.
        # DEPRECATED compatibility route table for old end_slot exits.
        # Refactored day files should jump directly to the next time period/day.
        SLOT_EXIT_ROUTES = {
            "d1_reflect_done":   (2, "Morning",    "day102_1_cora_missy_first_shift"),
            "d1_write_ch1":      (2, "Morning",    "day102_1_cora_missy_first_shift"),
            "d1_visit_missy":    (2, "Morning",    "day102_1_cora_missy_first_shift"),
            "d2_reflect_done":   (2, "Evening",    "day102_3_stern_fetches_cora"),
            "d2_write_night":    (3, "Morning",    "day103_morning"),
            "d3_reflect_done":   (3, "Afternoon",  "day103_2_suite_gideon_tea"),
            "d3_twilight_done":  (None, None,      "day103_4_room_stern_suspicion"),
            "d3_stern_done":     (3, "Night",      "day103_2_suite_night_tea"),
            "d3_ultimatum_done": (None, None,      "day103_3_bedroom_final_write"),
            "d3_write_night":    (4, "Morning",    "day104_1_false_dawn_suite_window"),
            "d4_write_night":    (None, None,      "day104_6_false_dawn_ending"),
            "d4_dawn_gate":      (5, "Morning",    "day105_1_monster_reemerges"),
            "d5_write_night":    (5, "Morning",    "day105_7_release_one_ending"),
        }

        def __init__(self):
            # ── Prologue ───────────────────────────────────────────────
            self.prologue_found             = "none"
            self.prologue_why_write         = "none"
            self.prologue_holywell_posture  = "none"
            self.run_archetype_seed         = "none"
            self.current_archetype_focus    = "none"

            # ── Day 1 ──────────────────────────────────────────────────
            self.day1_corridor_state    = "none"
            self.day1_interview_state   = "none"
            self.day1_ledger_focus      = "none"
            self.day1_night_action      = "none"
            self.has_witnessed_voyeur_scene  = False
            self.has_written_first_chapter   = False
            self.missy_day1_seed             = False
            self.missy_day1_trust_state      = "none"

            # ── Day 2 ──────────────────────────────────────────────────
            self.day2_contraband_state        = "none"
            self.missy_day2_suspicion_state   = "none"
            self.day2_chore_focus             = "none"
            self.day2_tea_choice              = "none"
            self.missy_day2_trust_break       = False
            self.day2_night_action            = "none"

            # ── Manuscript ─────────────────────────────────────────────
            self.manuscript_progress  = 0
            self.completed_chapters   = set()

            # ── Day 3 ──────────────────────────────────────────────────
            self.day3_corridor_chain          = "none"
            self.day3_brush_choice            = "none"
            self.day3_twilight_action         = "none"
            self.day3_frantic_pages_written   = False
            self.day3_stern_response          = "none"
            self.day3_ultimatum               = "none"
            self.day3_failed_write            = False
            self.day3_night_action            = "none"

            # ── Day 4 ──────────────────────────────────────────────────
            self.day4_evidence_discovered   = False
            self.day4_escape_state          = "none"
            self.has_photograph             = False
            self.missy_day4_used_as_cover   = False
            self.day4_stern_response        = "none"
            self.day4_twilight_action       = "none"
            self.missy_day4_repair_state    = "none"
            self.day4_night_action          = "none"

            # ── Day 5 ──────────────────────────────────────────────────
            self.day5_dynamic               = "none"
            self.cora_release1_flavour      = "none"
            self.day5_money_choice          = "none"
            self.gideon_entanglement_level  = "none"
            self.day5_evidence_destroyed    = False
            self.missy_debt_carried_forward = False
            self.release1_manuscript_completed = False
            self.release1_completed         = False

            # ── Release 2 carry-forward ────────────────────────────────
            self.gideon_recurring_pressure  = False
            self.release2_gideon_status     = "none"
            self.release2_guest_cast_pivot  = False
            self.release2_missy_status      = "none"

            # ── PROMOTE: Optional character grind chains ───────────────
            self.stern_chain_level  = 0
            self.missy_chain_level  = 0
            self.vance_chain_level  = 0
            self.penance_triggered  = False
            self.pending_penance    = []

        # ── Internal helpers ───────────────────────────────────────────

        def _set_boolean_flag(self, field_name, value):
            if not isinstance(value, bool):
                raise TypeError("{} must be a bool, got {}".format(field_name, type(value).__name__))
            setattr(self, field_name, value)

        def _set_string_state(self, field_name, value, valid_values):
            if value not in valid_values:
                raise ValueError(
                    "Invalid {} '{}'. Must be one of: {}".format(
                        field_name, value, ", ".join(valid_values)
                    )
                )
            setattr(self, field_name, value)

        # ── Prologue setters ───────────────────────────────────────────

        def set_prologue_found(self, value):
            self._set_string_state("prologue_found", value, self.VALID_PROLOGUE_FOUND_STATES)

        def set_prologue_why_write(self, value):
            self._set_string_state("prologue_why_write", value, self.VALID_PROLOGUE_WHY_WRITE_STATES)

        def set_prologue_holywell_posture(self, value):
            self._set_string_state("prologue_holywell_posture", value, self.VALID_PROLOGUE_HOLYWELL_STATES)

        # ── Archetype Focus setters ────────────────────────────────────

        def set_run_archetype_seed(self, value):
            self._set_string_state("run_archetype_seed", value, self.VALID_ARCHETYPE_SEEDS)

        def set_current_archetype_focus(self, value):
            self._set_string_state("current_archetype_focus", value, self.VALID_ARCHETYPE_FOCUS_STATES)

        # ── Day 1 setters ──────────────────────────────────────────────

        def set_corridor_state(self, value):
            self._set_string_state("day1_corridor_state", value, self.VALID_CORRIDOR_STATES)

        def set_day1_interview_state(self, value):
            self._set_string_state("day1_interview_state", value, self.VALID_INTERVIEW_STATES)

        def set_day1_ledger_focus(self, value):
            self._set_string_state("day1_ledger_focus", value, self.VALID_LEDGER_FOCUS_STATES)

        def set_day1_night_action(self, value):
            self._set_string_state("day1_night_action", value, self.VALID_DAY1_NIGHT_ACTIONS)

        def set_has_witnessed_voyeur_scene(self, value):
            self._set_boolean_flag("has_witnessed_voyeur_scene", value)

        def set_has_written_first_chapter(self, value):
            self._set_boolean_flag("has_written_first_chapter", value)

        def set_missy_day1_seed(self, value):
            self._set_boolean_flag("missy_day1_seed", value)

        def set_missy_day1_trust_state(self, value):
            self._set_string_state("missy_day1_trust_state", value, self.VALID_MISSY_DAY1_TRUST_STATES)

        # ── Day 2 setters ──────────────────────────────────────────────

        def set_day2_contraband_state(self, value):
            self._set_string_state("day2_contraband_state", value, self.VALID_CONTRABAND_STATES)

        def set_missy_day2_suspicion_state(self, value):
            self._set_string_state("missy_day2_suspicion_state", value, self.VALID_MISSY_DAY2_SUSPICION_STATES)

        def set_day2_chore_focus(self, value):
            self._set_string_state("day2_chore_focus", value, self.VALID_CHORE_FOCUS_STATES)

        def set_day2_tea_choice(self, value):
            self._set_string_state("day2_tea_choice", value, self.VALID_TEA_CHOICE_STATES)

        def set_missy_day2_trust_break(self, value):
            self._set_boolean_flag("missy_day2_trust_break", value)

        def set_day2_night_action(self, value):
            self._set_string_state("day2_night_action", value, self.VALID_DAY2_NIGHT_ACTIONS)

        # ── Manuscript ─────────────────────────────────────────────────

        def complete_manuscript_chapter(self, chapter_id):
            if chapter_id not in self.completed_chapters:
                self.completed_chapters.add(chapter_id)
                self.manuscript_progress = len(self.completed_chapters)
            if chapter_id == "day1_chapter":
                self.has_written_first_chapter = True

        def complete_release1_manuscript(self, value):
            self._set_boolean_flag("release1_manuscript_completed", value)

        # ── Day 3 setters ──────────────────────────────────────────────

        def set_day3_corridor_chain(self, value):
            self._set_string_state("day3_corridor_chain", value, self.VALID_CORRIDOR_CHAIN_STATES)

        def set_day3_brush_choice(self, value):
            self._set_string_state("day3_brush_choice", value, self.VALID_BRUSH_CHOICE_STATES)

        def set_day3_twilight_action(self, value):
            self._set_string_state("day3_twilight_action", value, self.VALID_DAY3_TWILIGHT_ACTIONS)

        def set_day3_frantic_pages_written(self, value):
            self._set_boolean_flag("day3_frantic_pages_written", value)

        def set_day3_stern_response(self, value):
            self._set_string_state("day3_stern_response", value, self.VALID_DAY3_STERN_RESPONSES)

        def set_day3_ultimatum(self, value):
            self._set_string_state("day3_ultimatum", value, self.VALID_ULTIMATUM_STATES)

        def set_day3_failed_write(self, value):
            self._set_boolean_flag("day3_failed_write", value)

        def set_day3_night_action(self, value):
            self._set_string_state("day3_night_action", value, self.VALID_DAY3_NIGHT_ACTIONS)

        # ── Day 4 setters ──────────────────────────────────────────────

        def set_day4_evidence_discovered(self, value):
            self._set_boolean_flag("day4_evidence_discovered", value)

        def set_day4_escape_state(self, value):
            self._set_string_state("day4_escape_state", value, self.VALID_ESCAPE_STATES)

        def set_has_photograph(self, value):
            self._set_boolean_flag("has_photograph", value)

        def set_missy_day4_used_as_cover(self, value):
            self._set_boolean_flag("missy_day4_used_as_cover", value)

        def set_day4_stern_response(self, value):
            self._set_string_state("day4_stern_response", value, self.VALID_DAY4_STERN_RESPONSES)

        def set_day4_twilight_action(self, value):
            self._set_string_state("day4_twilight_action", value, self.VALID_DAY4_TWILIGHT_ACTIONS)

        def set_missy_day4_repair_state(self, value):
            self._set_string_state("missy_day4_repair_state", value, self.VALID_MISSY_DAY4_REPAIR_STATES)

        def set_day4_night_action(self, value):
            self._set_string_state("day4_night_action", value, self.VALID_DAY4_NIGHT_ACTIONS)

        # ── Day 5 setters ──────────────────────────────────────────────

        def set_day5_dynamic(self, value):
            self._set_string_state("day5_dynamic", value, self.VALID_DAY5_DYNAMICS)

        def set_cora_release1_flavour(self, value):
            self._set_string_state("cora_release1_flavour", value, self.VALID_RELEASE1_FLAVOURS)

        def set_day5_money_choice(self, value):
            self._set_string_state("day5_money_choice", value, self.VALID_MONEY_CHOICES)

        def set_gideon_entanglement_level(self, value):
            self._set_string_state("gideon_entanglement_level", value, self.VALID_ENTANGLEMENT_LEVELS)

        def set_day5_evidence_destroyed(self, value):
            self._set_boolean_flag("day5_evidence_destroyed", value)

        def set_missy_debt_carried_forward(self, value):
            self._set_boolean_flag("missy_debt_carried_forward", value)

        def set_release1_completed(self, value):
            self._set_boolean_flag("release1_completed", value)

        # ── Release 2 carry-forward setters ───────────────────────────

        def set_gideon_recurring_pressure(self, value):
            self._set_boolean_flag("gideon_recurring_pressure", value)

        def set_release2_gideon_status(self, value):
            self._set_string_state("release2_gideon_status", value, self.VALID_RELEASE2_GIDEON_STATUSES)

        def set_release2_guest_cast_pivot(self, value):
            self._set_boolean_flag("release2_guest_cast_pivot", value)

        def set_release2_missy_status(self, value):
            self._set_string_state("release2_missy_status", value, self.VALID_RELEASE2_MISSY_STATUSES)

        # ── PROMOTE: Character grind chain progression ───────────────

        def _set_chain_level(self, field_name, value):
            if not isinstance(value, int) or value < 0 or value > self.MAX_CHARACTER_CHAIN_LEVEL:
                raise ValueError(
                    "Invalid {} '{}'. Must be an int from 0 to {}.".format(
                        field_name, value, self.MAX_CHARACTER_CHAIN_LEVEL
                    )
                )
            setattr(self, field_name, value)

        def set_stern_chain_level(self, value):
            self._set_chain_level("stern_chain_level", value)

        def set_missy_chain_level(self, value):
            self._set_chain_level("missy_chain_level", value)

        def set_vance_chain_level(self, value):
            self._set_chain_level("vance_chain_level", value)

        def set_penance_triggered(self, value):
            """DEPRECATED compatibility bridge; use pending_penance queue helpers."""
            self._set_boolean_flag("penance_triggered", value)

        def queue_penance(self, penance_label):
            if penance_label not in self.pending_penance:
                self.pending_penance.append(penance_label)
                self.set_penance_triggered(True)

        def has_pending_penance(self):
            return len(self.pending_penance) > 0

        def consume_penance_at_window(self, window_id):
            """Pop the next queued penance label for a dynamic window. Character confrontations take precedence."""
            if not self.pending_penance:
                return None
            
            # Enforce character confrontation precedence
            for label in self.pending_penance:
                if label.startswith("confrontation_"):
                    self.pending_penance.remove(label)
                    if not self.pending_penance:
                        self.set_penance_triggered(False)
                    return label

            # Fallback to popping the first available label (e.g., anxiety breakdown)
            penance_label = self.pending_penance.pop(0)
            if not self.pending_penance:
                self.set_penance_triggered(False)
            return penance_label

        def pop_penance_for_window(self, window_id):
            """Backward-compatible alias for consume_penance_at_window."""
            return self.consume_penance_at_window(window_id)

        def clear_penance(self):
            self.pending_penance = []

        def get_character_chain_level(self, character):
            if character not in self.VALID_CHAIN_CHARACTERS:
                raise ValueError(
                    "Invalid chain character '{}'. Must be one of: {}".format(
                        character, ", ".join(self.VALID_CHAIN_CHARACTERS)
                    )
                )
            return getattr(self, "{}_chain_level".format(character))

        def chain_available(self, character):
            return self.get_character_chain_level(character) < self.MAX_CHARACTER_CHAIN_LEVEL

        def resolve_chain_label(self, character):
            level = self.get_character_chain_level(character)
            if level >= self.MAX_CHARACTER_CHAIN_LEVEL:
                return None
            return "{}_chain_{}".format(character, level + 1)

        def complete_chain_beat(self, character):
            """Advance a character's chain level by one. Call once at the end of any chain scene."""
            current = self.get_character_chain_level(character)
            if current < self.MAX_CHARACTER_CHAIN_LEVEL:
                self._set_chain_level("{}_chain_level".format(character), current + 1)

        def get_post_penance_target(self, current_day, time_of_day):
            """Pure query — returns (next_day, next_time, next_label). No side effects."""
            if current_day == 4 and self.has_pending_penance():
                return (4, "Night", "day104_6_false_dawn_ending")
            return self.POST_PENANCE_ROUTES.get((current_day, time_of_day))

        def consume_penance(self):
            """DEPRECATED compatibility shim; migrated windows pop pending_penance directly."""
            self.set_penance_triggered(False)
            self.clear_penance()

        def get_slot_exit_target(self, outcome):
            """Return (next_day_or_None, next_time_or_None, next_label) for end_slot."""
            if outcome == "d4_twilight_done":
                return None  # handled in end_slot label (requires player.anxiety check)
            return self.SLOT_EXIT_ROUTES.get(outcome)

    # Instantiate global singletons for non-canon sandbox execution/validation
    player = PlayerStats()
    story = StoryState()
    time_manager = TimeManager()
