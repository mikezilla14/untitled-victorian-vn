# ═══════════════════════════════════════════════════════════════
#  classes.rpy
#  All Python class definitions.
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

        def update_stats(self):
            self.suspicion -= 5
            self.suspicion = max(0, min(100, self.suspicion))

            self.corruption_xp = max(0, self.corruption_xp)

            while self.corruption_xp >= 20:
                self.corruption_xp -= 20
                self.corruption_level += 1

            inspiration_cap = 20 + (self.corruption_level * 10)
            self.inspiration = max(0, min(inspiration_cap, self.inspiration))
            
        def gain_inspiration(self, amount):
            self.inspiration += amount

        def gain_corruption_xp(self, amount):
            self.corruption_xp += amount

        def raise_suspicion(self, amount):
            self.suspicion += amount

        def lower_suspicion(self, amount):
            self.suspicion -= amount

        def spend_inspiration(self, amount):
            if self.inspiration >= amount:
                self.inspiration -= amount
                return True
            return False

    class StoryState(object):
        def __init__(self):
            self.has_read_gideon_letters = False
            self.has_witnessed_voyeur_scene = False
            self.has_heard_stern_humming = False
            self.has_gideon_spoken_to_cora_day2 = False
            self.has_gideon_revealed_vulnerability = False
            self.has_sent_manuscript = False
            self.has_received_manuscript_payment = False
            self.has_written_first_chapter = False
            self.has_written_second_chapter = False
            self.has_chosen_bold_option_day4 = False

        def _set_boolean_flag(self, field_name, value):
            if not isinstance(value, bool):
                raise TypeError("{} must be a bool, got {}".format(field_name, type(value).__name__))
            setattr(self, field_name, value)

        def set_has_read_gideon_letters(self, value):
            self._set_boolean_flag("has_read_gideon_letters", value)

        def set_has_witnessed_voyeur_scene(self, value):
            self._set_boolean_flag("has_witnessed_voyeur_scene", value)

        def set_has_heard_stern_humming(self, value):
            self._set_boolean_flag("has_heard_stern_humming", value)

        def set_has_gideon_spoken_to_cora_day2(self, value):
            self._set_boolean_flag("has_gideon_spoken_to_cora_day2", value)

        def set_has_gideon_revealed_vulnerability(self, value):
            self._set_boolean_flag("has_gideon_revealed_vulnerability", value)

        def set_has_sent_manuscript(self, value):
            self._set_boolean_flag("has_sent_manuscript", value)

        def set_has_received_manuscript_payment(self, value):
            self._set_boolean_flag("has_received_manuscript_payment", value)

        def set_has_written_first_chapter(self, value):
            self._set_boolean_flag("has_written_first_chapter", value)

        def set_has_written_second_chapter(self, value):
            self._set_boolean_flag("has_written_second_chapter", value)

        def set_has_chosen_bold_option_day4(self, value):
            self._set_boolean_flag("has_chosen_bold_option_day4", value)
