"""Abstract balance simulation helpers for Release 1 MVP."""

from __future__ import annotations

import csv
import re
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore


WRITE_COST = 20
CORRUPTION_XP_PER_LEVEL = 20
STARTING_STATE = {
    "inspiration": 0,
    "corruption_level": 1,
    "corruption_xp": 0,
    "anxiety": 0,
    "manuscript_progress": 0,
}

# Typical prologue floor before Day 101 (abstract; not a route walk).
PROLOGUE_BY_POLICY: dict[str, tuple[int, int, int, int, int, int]] = {
    "corruption_forward": (20, 30, 0, 0, 0, 0),
    "cautious": (20, 25, 5, 5, 0, 0),
    "passive": (15, 18, 3, 3, 0, 0),
    "reckless": (15, 35, 10, 12, 5, 0),
    "recovery": (15, 20, 5, 5, 0, 0),
    "deadline_skip": (10, 5, 0, 0, 0, 0),
    "ch1_only": (15, 22, 4, 4, 0, 0),
    "anxiety_push": (10, 10, 25, 25, 20, 0),
    "penance_force": (15, 25, 12, 12, 8, 0),
}


@dataclass
class PlayerState:
    inspiration: int = 0
    corruption_level: int = 1
    corruption_xp: int = 0
    anxiety: int = 0
    manuscript_progress: int = 0
    stern_susp: int = 0
    vance_susp: int = 0
    missy_susp: int = 0
    gideon_susp: int = 0
    day: int = 100
    ending: str = ""
    notes: list[str] = field(default_factory=list)

    @property
    def inspiration_cap(self) -> int:
        return 20 + self.corruption_level * 10

    def clone(self) -> PlayerState:
        return PlayerState(
            inspiration=self.inspiration,
            corruption_level=self.corruption_level,
            corruption_xp=self.corruption_xp,
            anxiety=self.anxiety,
            manuscript_progress=self.manuscript_progress,
            stern_susp=self.stern_susp,
            vance_susp=self.vance_susp,
            missy_susp=self.missy_susp,
            gideon_susp=self.gideon_susp,
            day=self.day,
            ending=self.ending,
            notes=list(self.notes),
        )

    def apply_delta(self, insp: int = 0, corr: int = 0, stern: int = 0, vance: int = 0, missy: int = 0, gideon: int = 0) -> None:
        if insp:
            self.inspiration = min(self.inspiration_cap, self.inspiration + insp)
        if corr:
            self.corruption_xp += corr
        self.stern_susp = max(0, self.stern_susp + stern)
        self.vance_susp = max(0, self.vance_susp + vance)
        self.missy_susp = max(0, self.missy_susp + missy)
        self.gideon_susp = max(0, self.gideon_susp + gideon)
        while self.corruption_xp >= CORRUPTION_XP_PER_LEVEL:
            self.corruption_xp -= CORRUPTION_XP_PER_LEVEL
            self.corruption_level += 1
        self.inspiration = max(0, min(self.inspiration_cap, self.inspiration))
        self._recalculate_anxiety()

    def _recalculate_anxiety(self) -> None:
        safety = 1.0
        for susp in (self.stern_susp, self.vance_susp, self.missy_susp, self.gideon_susp):
            safety *= 1.0 - min(100, susp) / 100.0
        self.anxiety = max(0, min(100, int(round(100.0 * (1.0 - safety)))))

    def has_story_fuel(self, required_insp: int, required_corr: int) -> bool:
        return self.inspiration >= required_insp and self.corruption_level >= required_corr

    def attempt_write(self, required_insp: int, required_corr: int, cost: int = WRITE_COST) -> bool:
        if not self.has_story_fuel(required_insp, required_corr):
            return False
        if self.inspiration < cost:
            return False
        self.inspiration -= cost
        return True


@dataclass
class GateSpec:
    gate_id: str
    gate_type: str
    required_insp: int | None = None
    required_corr_level: int | None = None
    required_manuscript_progress: int | None = None
    required_anxiety_max: int | None = None
    required_anxiety_min: int | None = None
    on_pass: str = ""
    on_fail: str = ""


@dataclass
class PolicySpec:
    policy_id: str
    description: str
    choice_rule: str
    write_rule: str
    risk_rule: str
    expected_result: str


@dataclass
class DayBudget:
    day: int
    insp: int
    corr: int
    stern: int
    vance: int
    missy: int
    gideon: int


def _parse_int(value: Any) -> int | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    return int(float(text))


def load_gate_catalogue(path: Path) -> list[GateSpec]:
    gates: list[GateSpec] = []
    with path.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            gates.append(
                GateSpec(
                    gate_id=row["gate_id"],
                    gate_type=row.get("gate_type", ""),
                    required_insp=_parse_int(row.get("required_insp")),
                    required_corr_level=_parse_int(row.get("required_corr_level")),
                    required_manuscript_progress=_parse_int(row.get("required_manuscript_progress")),
                    required_anxiety_max=_parse_int(row.get("required_anxiety_max")),
                    required_anxiety_min=_parse_int(row.get("required_anxiety_min")),
                    on_pass=row.get("on_pass", ""),
                    on_fail=row.get("on_fail", ""),
                )
            )
    return gates


def load_run_policies(path: Path) -> list[PolicySpec]:
    policies: list[PolicySpec] = []
    with path.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            policies.append(
                PolicySpec(
                    policy_id=row["policy_id"],
                    description=row.get("description", ""),
                    choice_rule=row.get("choice_rule", ""),
                    write_rule=row.get("write_rule", ""),
                    risk_rule=row.get("risk_rule", ""),
                    expected_result=row.get("expected_result", ""),
                )
            )
    return policies


def load_balance_targets(path: Path) -> dict[str, Any]:
    if yaml is None:
        raise RuntimeError("PyYAML is required to load balance_targets.yaml")
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_choice_catalogue(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _day_from_row(row: dict[str, str]) -> int | None:
    for key in ("design_note", "source_file"):
        text = row.get(key, "")
        match = re.search(r"day(\d{3})", text)
        if match:
            return int(match.group(1))
    return None


def build_day_budgets(choices: list[dict[str, str]], policies: list[PolicySpec]) -> dict[str, dict[int, DayBudget]]:
    by_day: dict[int, list[dict[str, str]]] = defaultdict(list)
    for row in choices:
        day = _day_from_row(row)
        if day is not None:
            by_day[day].append(row)

    budgets: dict[str, dict[int, DayBudget]] = {}
    for policy in policies:
        budgets[policy.policy_id] = {}
        for day, rows in sorted(by_day.items()):
            budgets[policy.policy_id][day] = _budget_for_policy(policy.choice_rule, policy.risk_rule, rows)
    return budgets


def _score_row(row: dict[str, str], mode: str) -> float:
    insp = int(row.get("insp_delta") or 0)
    corr = int(row.get("corr_xp_delta") or 0)
    susp = sum(int(row.get(k) or 0) for k in ("stern_susp_delta", "vance_susp_delta", "missy_susp_delta", "gideon_susp_delta"))
    if mode == "maximize_corr":
        return corr * 2 + insp - susp * 0.25
    if mode == "minimize_corr":
        return insp - corr * 3 - susp
    if mode == "maximize_suspicion":
        return susp * 2 + corr - insp * 0.1
    if mode == "safe_choices":
        return insp - corr * 2 - susp * 1.5
    if mode == "safe_then_risky":
        return insp - corr - susp
    if mode == "avoid_corr":
        return insp - corr * 4 - susp
    if mode == "confrontation_first":
        return susp + corr * 0.5
    return insp + corr * 0.5 - susp


def _budget_for_policy(choice_rule: str, risk_rule: str, rows: list[dict[str, str]]) -> DayBudget:
    mode_map = {
        "maximize_corr": "maximize_corr",
        "minimize_suspicion": "safe_choices",
        "avoid_corr": "avoid_corr",
        "maximize_suspicion": "maximize_suspicion",
        "safe_choices": "safe_choices",
        "safe_then_risky": "safe_then_risky",
        "risky_choices": "maximize_suspicion",
        "confrontation_first": "confrontation_first",
        "minimal_write": "safe_choices",
        "skip_writes": "avoid_corr",
    }
    mode = mode_map.get(choice_rule, "safe_choices")
    ranked = sorted(rows, key=lambda row: _score_row(row, mode), reverse=True)
    picks = ranked[: min(8 if mode == "maximize_corr" else 6, len(ranked))]
    insp = sum(int(r.get("insp_delta") or 0) for r in picks)
    corr = sum(int(r.get("corr_xp_delta") or 0) for r in picks)
    stern = sum(int(r.get("stern_susp_delta") or 0) for r in picks)
    vance = sum(int(r.get("vance_susp_delta") or 0) for r in picks)
    missy = sum(int(r.get("missy_susp_delta") or 0) for r in picks)
    gideon = sum(int(r.get("gideon_susp_delta") or 0) for r in picks)
    if risk_rule == "accept_suspicion":
        stern = int(stern * 1.2)
        vance = int(vance * 1.2)
        missy = int(missy * 1.2)
    elif risk_rule in {"avoid_suspicion", "low_risk"}:
        stern = int(stern * 0.5)
        vance = int(vance * 0.5)
        missy = int(missy * 0.5)
    elif risk_rule == "max_suspicion":
        stern = int(stern * 1.5)
        vance = int(vance * 1.5)
        missy = int(missy * 1.5)
    day = _day_from_row(picks[0]) if picks else 100
    return DayBudget(day=day or 100, insp=insp, corr=corr, stern=stern, vance=vance, missy=missy, gideon=gideon)


def gate_lookup(gates: list[GateSpec]) -> dict[str, GateSpec]:
    return {gate.gate_id: gate for gate in gates}


def simulate_policy(
    policy: PolicySpec,
    gates: list[GateSpec],
    day_budgets: dict[int, DayBudget],
) -> PlayerState:
    state = PlayerState(**STARTING_STATE)
    gate_by_id = gate_lookup(gates)
    ch1 = gate_by_id["ch1_write_gate"]
    ch2 = gate_by_id["ch2_write_gate"]
    ch3 = gate_by_id["ch3_write_gate"]
    deadline1 = gate_by_id["deadline_ch1"]
    deadline2 = gate_by_id["deadline_ch2"]

    prologue = PROLOGUE_BY_POLICY.get(policy.policy_id, (10, 15, 0, 0, 0, 0))
    state.apply_delta(*prologue)
    state.notes.append(
        f"Prologue baseline: insp={state.inspiration}, corr={state.corruption_level}"
    )

    def apply_day(day: int) -> None:
        budget = day_budgets.get(day)
        if not budget:
            return
        state.day = day
        stern, vance, missy, gideon = budget.stern, budget.vance, budget.missy, budget.gideon
        if policy.policy_id not in {"anxiety_push", "reckless"}:
            stern = int(stern * 0.35)
            vance = int(vance * 0.35)
            missy = int(missy * 0.35)
            gideon = int(gideon * 0.35)
        state.apply_delta(budget.insp, budget.corr, stern, vance, missy, gideon)
        if state.anxiety >= 100:
            state.ending = "game_over_dismissed"
            state.notes.append(f"Anxiety hit 100 on day {day}")

    def should_write(slot: str) -> bool:
        rule = policy.write_rule
        if rule == "never_write":
            return False
        if rule == "ch1_only":
            return slot == "ch1"
        if rule in {"defer_writes", "skip_writes"}:
            return False
        if rule == "write_only_if_required":
            return slot == "ch1"
        return True

    def try_write(gate: GateSpec, chapter: str, slop_ok: bool = False) -> None:
        if state.ending:
            return
        if not should_write(chapter):
            state.notes.append(f"Skipped write for {chapter} per policy")
            return
        req_insp = gate.required_insp or 0
        req_corr = gate.required_corr_level or 0
        if state.attempt_write(req_insp, req_corr):
            if chapter == "ch1" and slop_ok and state.corruption_level <= 2:
                state.notes.append("Day 101 slop path — no manuscript_progress")
            else:
                state.manuscript_progress += 1
                state.notes.append(f"Wrote {chapter}; manuscript_progress={state.manuscript_progress}")
        else:
            state.notes.append(
                f"Failed {gate.gate_id}: insp={state.inspiration}, corr={state.corruption_level}"
            )

    for day in (100, 101, 102, 103, 104, 105):
        if state.ending:
            break
        apply_day(day)
        if state.anxiety >= 100:
            state.ending = "game_over_dismissed"
            break

        if day == 101:
            try_write(ch1, "ch1", slop_ok=True)
        elif day == 102:
            if state.manuscript_progress == 0:
                try_write(ch1, "ch1")
            try_write(ch2, "ch2")
        elif day == 103:
            if state.manuscript_progress == 0:
                state.ending = deadline1.on_fail or "game_over_deadline_1"
                state.notes.append("Deadline 1 triggered at Day 103 morning")
                break
            try_write(ch3, "ch3")
        elif day == 104:
            if state.manuscript_progress < (deadline2.required_manuscript_progress or 2):
                state.ending = deadline2.on_fail or "game_over_deadline_2"
                state.notes.append("Deadline 2 triggered at Day 104 close")
                break
            if state.anxiety < 85 and should_write("ch4"):
                if state.attempt_write(ch2.required_insp or 30, ch2.required_corr_level or 3):
                    state.manuscript_progress += 1
                    state.notes.append("Day 104 triumphant write")
        elif day == 105:
            if should_write("ch5"):
                if state.attempt_write(ch2.required_insp or 30, ch2.required_corr_level or 3):
                    state.manuscript_progress += 1
                    state.notes.append("Day 105 reckoning write")
            soft = gate_by_id.get("soft_fail_rejection")
            if soft and state.corruption_level < (soft.required_corr_level or 3):
                state.ending = soft.on_fail or "bad_ending_rejection"
            elif state.manuscript_progress >= 5 and state.corruption_level >= 3:
                state.ending = "day105_7_release_one_ending"
            elif state.manuscript_progress >= 3 and state.corruption_level >= 3:
                state.ending = "day105_7_release_one_ending"
            elif state.manuscript_progress >= 1 and state.corruption_level < 3:
                state.ending = "bad_ending_rejection"
            elif state.manuscript_progress >= 3:
                state.ending = "weak_completion"
            else:
                state.ending = "unexpected_stop"

    if not state.ending:
        state.ending = "unexpected_stop"
    return state


def evaluate_assertions(state: PlayerState, assertions: list[dict[str, Any]]) -> list[tuple[str, bool, str]]:
    results: list[tuple[str, bool, str]] = []
    for assertion in assertions:
        if "assert_ending" in assertion:
            expected = assertion["assert_ending"]
            ok = state.ending == expected
            results.append((f"assert_ending:{expected}", ok, state.ending))
        elif "assert_ending_one_of" in assertion:
            expected = assertion["assert_ending_one_of"]
            ok = state.ending in expected
            results.append((f"assert_ending_one_of:{','.join(expected)}", ok, state.ending))
        elif "assert_reaches_day_at_least" in assertion:
            ok = state.day >= int(assertion["assert_reaches_day_at_least"])
            results.append((f"assert_reaches_day_at_least:{assertion['assert_reaches_day_at_least']}", ok, str(state.day)))
        elif "assert_stat_floor" in assertion:
            floors = assertion["assert_stat_floor"]
            ok = all(getattr(state, key, 0) >= value for key, value in floors.items())
            results.append((f"assert_stat_floor:{floors}", ok, f"manuscript_progress={state.manuscript_progress}"))
        elif "assert_event_seen" in assertion:
            # Abstract sim does not traverse confrontation labels yet.
            results.append(
                (
                    f"assert_event_seen:{assertion['assert_event_seen']}",
                    False,
                    "INCOMPLETE — requires runtime capture or graph walk",
                )
            )
        else:
            results.append((str(assertion), False, "unsupported assertion"))
    return results
