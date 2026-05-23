# FORMAT LEGEND:
# [ASSET] -> backgrounds, sprites, transitions, CG/UI callouts
# [STATE] -> variable changes, effects, conditions, jumps
# [CHOICE] -> menu blocks and inflection points
# [BEAT] -> narrative intent / scene intent notes

# ═══════════════════════════════════════════════════════════════
#  classes_non_canon.rpy
#  Writers' Room — promotion source for renpy_project/game/classes.rpy
#
#  NOT loaded at runtime. During Release 1 promotion, merge this file into
#  classes.rpy (or diff-merge the marked StoryState chain sections).
#  Baseline synced from renpy_project/game/classes.rpy at promotion time.
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
            self.corruption_level = 1
            self.corruption_xp = 0
            self.inspiration = 0
            self.suspicion = 0
            self.anxiety = 0
            self.stern_suspicion = 0
            self.vance_suspicion = 0
            self.missy_suspicion = 0

        @property
        def inspiration_cap(self):
            return 20 + (self.corruption_level * 10)

        def recalculate_anxiety(self):
            # Character suspicions must never be below 0 or above 100.
            self.stern_suspicion = max(0, min(100, self.stern_suspicion))
            self.vance_suspicion = max(0, min(100, self.vance_suspicion))
            self.missy_suspicion = max(0, min(100, self.missy_suspicion))

            # Accumulated Anxiety sum model
            self.anxiety = self.stern_suspicion + self.vance_suspicion + self.missy_suspicion

            # Total suspicion mirrors the combined anxiety, capped at 100
            self.suspicion = max(0, min(100, self.anxiety))

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

        def adjust_character_suspicion(self, character, amount):
            if character == "stern":
                self.stern_suspicion += amount
            elif character == "vance":
                self.vance_suspicion += amount
            elif character == "missy":
                self.missy_suspicion += amount
            else:
                raise ValueError("Invalid character: {}".format(character))
            self.update_stats()

        def has_story_fuel(self, required_total=15):
            """
            Read-only writing-gate check.
            Returns True if (Inspiration + Corruption XP) meets the threshold.
            Does not spend any resources — use attempt_write() for the actual gate.
            """
            return (self.inspiration + self.corruption_xp) >= required_total

    class StoryState(object):

        # ── Prologue ───────────────────────────────────────────────────
        VALID_PROLOGUE_FOUND_STATES  = ("none", "overheard", "read_letters")

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

        def __init__(self):
            # ── Prologue ───────────────────────────────────────────────
            self.prologue_found         = "none"

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
            self._set_boolean_flag("penance_triggered", value)

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

    # Instantiate global singletons for non-canon sandbox execution/validation
    player = PlayerStats()
    story = StoryState()
    time_manager = TimeManager()
