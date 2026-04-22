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
            self.read_letters = False
            self.saw_voyeur_scene = False
            self.heard_stern_humming = False
            self.gideon_spoke_day2 = False
            self.gideon_showed_depth = False
            self.manuscript_sent = False
            self.payment_received = False
            self.wrote_chapter_1 = False
            self.wrote_chapter_2 = False
            self.chose_bold_day4 = False
