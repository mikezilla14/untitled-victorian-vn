# ═══════════════════════════════════════════════════════════════
#  debug_run_capture.rpy
#  Non-prod JSONL playtest telemetry for the testing/balance framework.
#  Excluded from public build profile (Phase 10).
# ═══════════════════════════════════════════════════════════════

init -5 python:
    import json
    import os
    import time

    ENDING_LABELS = frozenset([
        "game_over_dismissed",
        "bad_ending_rejection",
        "game_over_deadline_1",
        "game_over_deadline_2",
        "day105_7_release_one_ending",
        "day105_cliffhanger",
    ])

    CONFRONTATION_LABELS = frozenset([
        "confrontation_stern",
        "confrontation_vance",
        "confrontation_missy",
    ])

    _CAPTURE_FLAG_KEYS = (
        "day1_corridor_state",
        "day1_ledger_focus",
        "day2_contraband_state",
        "day2_tea_choice",
        "day3_brush_choice",
        "day3_ultimatum",
        "day4_escape_state",
        "day5_dynamic",
        "day5_money_choice",
    )

    class BalanceCapture(object):
        def __init__(self):
            self.active = False
            self.run_id = ""
            self._handle = None
            self.sequence = 0
            self.contains_rollback = False
            self.current_label = ""
            self._pending_menu_caption = ""

        def _capture_dir(self):
            path = os.path.join(config.basedir, "debug_captures")
            if not os.path.isdir(path):
                os.makedirs(path)
            return path

        def _snapshot(self):
            snap = {
                "stats": {
                    "inspiration": player.inspiration,
                    "inspiration_cap": player.inspiration_cap,
                    "corruption_level": player.corruption_level,
                    "corruption_xp": player.corruption_xp,
                    "anxiety": player.anxiety,
                    "manuscript_progress": story.manuscript_progress,
                },
                "suspicion": {
                    "stern": player.get_total_suspicion("stern"),
                    "missy": player.get_total_suspicion("missy"),
                    "vance": player.get_total_suspicion("vance"),
                    "gideon": player.get_total_suspicion("gideon"),
                },
                "flags": {},
            }
            for key in _CAPTURE_FLAG_KEYS:
                if hasattr(story, key):
                    snap["flags"][key] = getattr(story, key)
            snap["flags"]["current_day"] = time_manager.current_day
            snap["flags"]["time_of_day"] = time_manager.time_of_day
            return snap

        def log_event(self, event_type, **payload):
            if not self.active or self._handle is None:
                return
            self.sequence += 1
            record = {
                "seq": self.sequence,
                "ts": time.time(),
                "event": event_type,
                "run_id": self.run_id,
                "label": self.current_label,
            }
            record.update(payload)
            record["snapshot"] = self._snapshot()
            self._handle.write(json.dumps(record, sort_keys=True) + "\n")
            self._handle.flush()

        def start(self, run_id):
            if self.active:
                self.stop("replaced_by_new_run")
            safe_id = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in run_id)
            path = os.path.join(self._capture_dir(), "{}.jsonl".format(safe_id))
            self._handle = open(path, "w", encoding="utf-8")
            self.active = True
            self.run_id = run_id
            self.sequence = 0
            self.contains_rollback = False
            self.log_event("run_start", capture_path=path)

        def stop(self, note=""):
            if not self.active:
                return
            self.log_event("run_end", note=note, contains_rollback=self.contains_rollback)
            if self._handle is not None:
                self._handle.close()
            self._handle = None
            self.active = False

        def on_label(self, label_name, abnormal):
            self.current_label = label_name
            if not self.active:
                return
            grain_type = "ending" if label_name in ENDING_LABELS else "label"
            self.log_event(
                "grain_enter",
                grain_id=label_name,
                label=label_name,
                grain_type=grain_type,
                day=time_manager.current_day,
                period=time_manager.time_of_day,
                abnormal=bool(abnormal),
            )
            if label_name in ENDING_LABELS:
                self.log_event("ending", ending_id=label_name)
            if label_name in CONFRONTATION_LABELS:
                self.log_event("flag", flag="confrontation", value=label_name)

        def on_menu_arguments(self, items):
            if not self.active:
                return
            captions = []
            for item in items:
                if isinstance(item, tuple) and item:
                    captions.append(str(item[0]))
            self._pending_menu_caption = "|".join(captions[:8])

        def on_menu_choice(self, choice):
            if not self.active:
                return
            self.log_event(
                "choice",
                choice_group=self.current_label,
                choice_made=str(choice),
                menu_caption=self._pending_menu_caption,
            )
            self._pending_menu_caption = ""

        def on_gate(self, gate_id, passed, required_insp=None, required_corr=None):
            if not self.active:
                return
            self.log_event(
                "gate",
                gate_id=gate_id,
                pass_fail="pass" if passed else "fail",
                required_insp=required_insp,
                required_corr=required_corr,
            )

        def on_rollback(self):
            if not self.active:
                return
            self.contains_rollback = True
            self.log_event(
                "rollback_event",
                grain_id=self.current_label,
                note="renpy_rollback",
            )

        def on_apply_effects(self, kwargs, success):
            if not self.active:
                return
            self.log_event("flag", mutation="apply_effects", kwargs=kwargs, success=success)


init python:
    def toggle_debug_grain_overlay():
        store.debug_grain_overlay_visible = not store.debug_grain_overlay_visible
        if store.debug_grain_overlay_visible:
            renpy.show_screen("debug_grain_overlay")
        else:
            renpy.hide_screen("debug_grain_overlay")

    config.keymap["toggle_debug_grain_overlay"] = ["K_F10"]
    config.underlay.append(renpy.Keymap(
        toggle_debug_grain_overlay=toggle_debug_grain_overlay,
    ))


init 999 python:
    def _balance_capture_instance():
        return getattr(store, "balance_capture", None)

    def _balance_capture_label_callback(name, abnormal):
        bc = _balance_capture_instance()
        if bc is not None:
            bc.on_label(name, abnormal)
        if store._balance_capture_prev_label_callback is not None:
            store._balance_capture_prev_label_callback(name, abnormal)

    store._balance_capture_prev_label_callback = config.label_callback
    config.label_callback = _balance_capture_label_callback

    # Ren'Py 8.5 has no config.rollback_callbacks; detect rollback via interact hook.
    store._balance_capture_prev_in_rollback = False

    def _balance_capture_interact_callback():
        bc = _balance_capture_instance()
        if bc is None:
            return
        in_rb = renpy.in_rollback()
        if in_rb and not store._balance_capture_prev_in_rollback:
            bc.on_rollback()
        store._balance_capture_prev_in_rollback = in_rb

    if _balance_capture_interact_callback not in config.interact_callbacks:
        config.interact_callbacks.append(_balance_capture_interact_callback)

    def _balance_capture_menu_arguments_callback(*args, **kwargs):
        if store._balance_capture_prev_menu_arguments_callback is not None:
            args, kwargs = store._balance_capture_prev_menu_arguments_callback(*args, **kwargs)
        return args, kwargs

    store._balance_capture_prev_menu_arguments_callback = config.menu_arguments_callback
    config.menu_arguments_callback = _balance_capture_menu_arguments_callback

    def _balance_capture_note_menu_items(items):
        bc = _balance_capture_instance()
        if bc is not None:
            bc.on_menu_arguments(items)

    _orig_display_menu = renpy.exports.display_menu

    def _balance_capture_display_menu(items, *args, **kwargs):
        _balance_capture_note_menu_items(items)
        result = _orig_display_menu(items, *args, **kwargs)
        bc = _balance_capture_instance()
        if bc is not None:
            bc.on_menu_choice(result)
        return result

    renpy.exports.display_menu = _balance_capture_display_menu
    renpy.store.menu = _balance_capture_display_menu

    _orig_apply_effects = apply_effects

    def apply_effects(*args, **kwargs):
        result = _orig_apply_effects(*args, **kwargs)
        bc = _balance_capture_instance()
        if bc is not None:
            bc.on_apply_effects(dict(kwargs), result)
        return result

    _orig_has_story_fuel = has_story_fuel

    def has_story_fuel(required_insp=30, required_corr=3):
        result = _orig_has_story_fuel(required_insp, required_corr)
        gate_id = None
        for ch, gate in (
            ("ch1_write_gate", WRITE_GATE_CH1),
            ("ch2_write_gate", WRITE_GATE_CH2),
            ("ch3_write_gate", WRITE_GATE_CH3),
        ):
            if required_insp == gate[0] and required_corr == gate[1]:
                gate_id = ch
                break
        if gate_id is None:
            gate_id = "write_gate_{}_{}".format(required_insp, required_corr)
        bc = _balance_capture_instance()
        if bc is not None:
            bc.on_gate(gate_id, result, required_insp, required_corr)
        return result

    _orig_attempt_write = attempt_write

    def attempt_write(required_insp=30, cost=20, required_corr=3):
        result = _orig_attempt_write(required_insp, cost, required_corr)
        gate_id = "attempt_write_{}_{}".format(required_insp, required_corr)
        bc = _balance_capture_instance()
        if bc is not None:
            bc.on_gate(gate_id, result, required_insp, required_corr)
        return result


label debug_capture_start:
    $ balance_capture.start(_capture_run_id)
    jump start


label debug_capture_stop:
    $ balance_capture.stop("manual_stop")
    return
