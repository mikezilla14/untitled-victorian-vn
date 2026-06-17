#!/usr/bin/env python3
"""Scene Direction Agent — deterministic Ren'Py sprite placement post-processor.

Reads draft `.rpy` scripts and adds/updates/preserves `show ... at <slot>` sprite
direction lines according to docs/contracts/sprite_layout_policy.yaml.

It NEVER touches dialogue, backgrounds, character names, manually locked direction,
`[asset keep]` lines, or block-form `show ...:` (ATL) statements. It only ever emits
or replaces `# [asset auto]` lines.

Idempotence is structural: every run first strips all `[asset auto]` lines, then
re-simulates the scene and re-inserts them. Running twice yields no diff.

Spec:   docs/specs/scene-direction-agent.md
Policy: docs/contracts/sprite_layout_policy.yaml

Usage:
    py scripts/scene_direction.py --files "<path1>,<path2>" [--check]

    --check   Report-only. Exit 1 if any file is not already in canonical form.
              Default (no flag) rewrites files in place.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "docs" / "contracts" / "sprite_layout_policy.yaml"

# characters.rpy is searched for in a few known locations (prod + non-prod draft).
CHARACTER_FILE_CANDIDATES = [
    ROOT / "main-game" / "prod-game" / "game" / "characters.rpy",
    ROOT / "main-game" / "non-prod-game" / "game" / "characters.rpy",
]

SCENE_RE = re.compile(r"^\s*scene\s+\S")
DIALOGUE_RE = re.compile(r'^(?P<indent>\s*)(?P<speaker>[A-Za-z_]\w*)\s+"')
ENTER_RE = re.compile(r"#\s*\[enter:\s*(?P<name>[A-Za-z_]\w*)\s*\]", re.IGNORECASE)
EXIT_RE = re.compile(r"#\s*\[exit:\s*(?P<name>[A-Za-z_]\w*)\s*\]", re.IGNORECASE)
PIN_RE = re.compile(
    r"#\s*\[asset pin:\s*(?P<name>[A-Za-z_]\w*)\s*=\s*(?P<slot>\w+)\s*\]", re.IGNORECASE
)
SCENE_LOCK_RE = re.compile(r"#\s*\[asset lock:scene\]", re.IGNORECASE)
KEEP_RE = re.compile(r"#\s*\[asset keep\]", re.IGNORECASE)
AUTO_RE = re.compile(r"#\s*\[asset auto\]", re.IGNORECASE)


# ─────────────────────────────────────────────────────────────────────────────
# IO / path helpers (mirror scripts/renpy_contract_linter.py conventions)
# ─────────────────────────────────────────────────────────────────────────────
def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def repo_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def resolve_file(path: str) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return ROOT / candidate


# ─────────────────────────────────────────────────────────────────────────────
# Policy + character registry
# ─────────────────────────────────────────────────────────────────────────────
def load_policy(policy_path: Path = POLICY_PATH) -> dict:
    data = yaml.safe_load(read_text(policy_path))
    return data["sprite_scene_direction_agent"]


def load_character_registry(candidates=None) -> dict:
    """Derive speaker -> {policy, tag} from characters.rpy (decision #1).

    Returns a dict keyed by lowercase speaker var, e.g.
        {"cora": {"policy": "Cora", "tag": "cora_sprite"}, ...}
    Only characters with a cb_name (i.e. a visible sprite owner) are included;
    narrator / inner-voice / system characters are excluded.
    """
    candidates = candidates or CHARACTER_FILE_CANDIDATES
    registry: dict[str, dict] = {}
    pattern = re.compile(
        r'define\s+(?P<var>\w+)\s*=\s*Character\([^\n]*cb_name\s*=\s*"(?P<cb>\w+)"'
    )
    for path in candidates:
        if not path.exists():
            continue
        for match in pattern.finditer(read_text(path)):
            var = match.group("var")
            cb = match.group("cb")
            registry[var.lower()] = {
                "policy": cb.capitalize(),
                "tag": f"{cb}_sprite",
            }
        if registry:
            break
    return registry


# ─────────────────────────────────────────────────────────────────────────────
# Layout resolver
# ─────────────────────────────────────────────────────────────────────────────
# Horizontal affinity for the general fallback (lower = further left).
# Canonical layouts and hard rules override this; it only orders the ~20
# character combinations the policy does not enumerate explicitly.
# Cora is the leftmost protagonist and always sits left of Stern (1-4 cast).
AFFINITY = {"Cora": 10, "Stern": 25, "Missy": 45, "Vance": 70, "Gideon": 90}


class OverflowError_(Exception):
    """Raised when more than four characters are visible."""


class LayoutResolver:
    def __init__(self, policy: dict):
        self.policy = policy
        self.slot_sets = {int(k): v for k, v in policy["slot_sets"].items()}
        self.aliases = policy.get("slot_aliases", {})
        self.canonical = self._index_canonical(policy.get("canonical_layouts", {}))
        self.hard_rules = policy.get("hard_rules", {})
        self.max_visible = policy.get("overflow_policy", {}).get("max_visible_characters", 4)

    def _index_canonical(self, canonical: dict) -> dict:
        indexed = {}
        for layout in canonical.values():
            key = frozenset(layout.keys())
            indexed[key] = {c: self.canonical_slot(s) for c, s in layout.items()}
        return indexed

    def canonical_slot(self, slot: str) -> str:
        return self.aliases.get(slot, slot)

    def resolve(self, visible_cast: list[str], pins: dict | None = None) -> dict:
        """Return {policy_name: slot}. Raises OverflowError_ if >max_visible."""
        pins = pins or {}
        cast = list(dict.fromkeys(visible_cast))  # de-dupe, preserve order
        n = len(cast)
        if n == 0:
            return {}
        if n > self.max_visible:
            raise OverflowError_(f"{n} visible characters")

        slots = list(self.slot_sets[n])

        # Priority 1 (within auto scope): explicit pins.
        assignment: dict[str, str] = {}
        if pins:
            for char, slot in pins.items():
                slot = self.canonical_slot(slot)
                if char in cast and slot in slots:
                    assignment[char] = slot
                    slots.remove(slot)

        # Priority: exact canonical layout (only when no pins force a deviation).
        if not pins:
            key = frozenset(cast)
            if key in self.canonical:
                return dict(self.canonical[key])

        # Hard rule: Cora + Missy alone.
        cma = self.hard_rules.get("cora_missy_alone")
        if cma and frozenset(cast) == frozenset(cma["when_visible_cast_exactly"]) and not pins:
            return {c: self.canonical_slot(s) for c, s in cma["positions"].items()}

        # General fallback: order remaining cast left-to-right by affinity.
        remaining = [c for c in cast if c not in assignment]
        remaining.sort(key=lambda c: (AFFINITY.get(c, 50), c))
        for char in remaining:
            assignment[char] = slots.pop(0)

        # Hard constraints (independent pairs).
        assignment = self._enforce_left_of(assignment, n, "Vance", "Gideon")
        assignment = self._enforce_left_of(assignment, n, "Cora", "Stern")
        return assignment

    def _enforce_left_of(self, assignment: dict, n: int, left: str, right: str) -> dict:
        """Guarantee `left` is positioned to the left of `right` when both present."""
        if left not in assignment or right not in assignment:
            return assignment
        order = self.slot_sets[n]
        if order.index(assignment[left]) > order.index(assignment[right]):
            assignment[left], assignment[right] = assignment[right], assignment[left]
        return assignment


# ─────────────────────────────────────────────────────────────────────────────
# Show-line parsing
# ─────────────────────────────────────────────────────────────────────────────
class ShowLine:
    def __init__(self, indent, tag, expr, slot, block_form, comment, raw):
        self.indent = indent
        self.tag = tag
        self.expr = expr
        self.slot = slot
        self.block_form = block_form
        self.comment = comment or ""
        self.raw = raw

    @property
    def is_auto(self):
        return bool(AUTO_RE.search(self.comment))

    @property
    def is_keep(self):
        return bool(KEEP_RE.search(self.comment))


def parse_show_line(line: str) -> ShowLine | None:
    stripped = line.rstrip("\n")
    indent_match = re.match(r"^(\s*)show\s+(.*)$", stripped)
    if not indent_match:
        return None
    indent, rest = indent_match.group(1), indent_match.group(2)

    comment = ""
    if "#" in rest:
        body, comment = rest.split("#", 1)
        comment = "#" + comment
    else:
        body = rest
    body = body.rstrip()

    block_form = body.endswith(":")
    if block_form:
        body = body[:-1].rstrip()

    if " at " not in body:
        return None
    left, slot_part = body.rsplit(" at ", 1)
    slot = slot_part.strip().split()[0] if slot_part.strip() else None
    if not slot:
        return None

    tokens = left.split()
    if not tokens:
        return None
    tag = tokens[0]
    expr = " ".join(tokens[1:]) if len(tokens) > 1 else None
    return ShowLine(indent, tag, expr, slot, block_form, comment, stripped)


# ─────────────────────────────────────────────────────────────────────────────
# Engine
# ─────────────────────────────────────────────────────────────────────────────
class SceneDirector:
    def __init__(self, policy: dict, registry: dict):
        self.policy = policy
        self.registry = registry
        self.resolver = LayoutResolver(policy)
        self.tag_to_policy = {v["tag"]: v["policy"] for v in registry.values()}
        self.policy_to_tag = {v["policy"]: v["tag"] for v in registry.values()}
        self.speaker_to_policy = {k: v["policy"] for k, v in registry.items()}
        self.defaults = policy.get("grammar", {}).get("default_expressions", {})
        trans = policy.get("transitions", {})
        self.t_left = trans.get("new_appearance_left", "moveinleft")
        self.t_right = trans.get("new_appearance_right", "moveinright")
        self.t_move = trans.get("reposition_existing", "move")
        self.warning = policy.get("overflow_policy", {}).get("if_more_than_4", {}).get(
            "warning_comment", "# [asset warning: more than 4 visible characters]"
        )

    # -- helpers ---------------------------------------------------------------
    def default_expr(self, policy_name: str) -> str:
        return self.defaults.get(policy_name, "neutral")

    def transition_for_slot(self, slot: str) -> str:
        if slot.startswith("left_") or "centre_left" in slot:
            return self.t_left
        return self.t_right

    def render_show(self, indent, policy_name, expr, slot, transition) -> str:
        tag = self.policy_to_tag[policy_name]
        expr = expr or self.default_expr(policy_name)
        with_clause = f" with {transition}" if transition else ""
        return f"{indent}show {tag} {expr} at {slot}{with_clause} # [asset auto]"

    def render_hide(self, indent, policy_name) -> str:
        tag = self.policy_to_tag[policy_name]
        return f"{indent}hide {tag} # [asset auto]"

    # -- scene splitting -------------------------------------------------------
    def split_blocks(self, lines: list[str]) -> list[tuple[int, int]]:
        """Return (start, end) line-index spans, one per scene block."""
        scene_idxs = [i for i, ln in enumerate(lines) if SCENE_RE.match(ln)]
        if not scene_idxs:
            return []
        spans = []
        for n, start in enumerate(scene_idxs):
            end = scene_idxs[n + 1] if n + 1 < len(scene_idxs) else len(lines)
            spans.append((start, end))
        return spans

    def block_is_locked(self, lines: list[str], start: int, end: int) -> bool:
        # Lock tag immediately before the scene line, or as a comment in the
        # block before the first show/dialogue statement.
        if start > 0 and SCENE_LOCK_RE.search(lines[start - 1]):
            return True
        for ln in lines[start:end]:
            if SCENE_LOCK_RE.search(ln):
                return True
            if parse_show_line(ln) or DIALOGUE_RE.match(ln):
                break
        return False

    # -- core transform --------------------------------------------------------
    def process_file(self, lines: list[str]) -> list[str]:
        spans = self.split_blocks(lines)
        if not spans:
            return lines

        # Work back-to-front so earlier spans' indices stay valid as we splice.
        out = list(lines)
        for start, end in reversed(spans):
            if self.block_is_locked(out, start, end):
                continue
            new_block = self.process_block(out[start:end])
            out[start:end] = new_block
        return out

    def process_block(self, block: list[str]) -> list[str]:
        # 1. Strip all existing auto show/hide lines (structural idempotence).
        stripped = [ln for ln in block if not self._is_auto_managed(ln)]

        # 2. Re-simulate and re-insert.
        result: list[str] = []
        visible: list[str] = []            # ordered policy names
        slots: dict[str, str] = {}         # policy -> current slot
        exprs: dict[str, str] = {}         # policy -> last known expression
        pins: dict[str, str] = {}
        overflowed = False

        def emit_layout(indent: str, newly: set[str]) -> list[str]:
            """Emit show/hide lines so on-screen state matches resolved layout."""
            nonlocal slots, overflowed
            try:
                target = self.resolver.resolve(visible, pins)
            except OverflowError_:
                if not overflowed:
                    overflowed = True
                    return [f"{indent}{self.warning}"]
                return []
            emitted = []
            order = {s: i for i, s in enumerate(self.resolver.slot_sets.get(len(visible), []))}
            for char in sorted(target, key=lambda c: order.get(target[c], 99)):
                slot = target[char]
                if slots.get(char) == slot:
                    continue
                if char in newly:
                    trans = self.transition_for_slot(slot)
                else:
                    trans = self.t_move
                emitted.append(self.render_show(indent, char, exprs.get(char), slot, trans))
                slots[char] = slot
            return emitted

        for line in stripped:
            pin_match = PIN_RE.search(line)
            if pin_match:
                pname = pin_match.group("name").capitalize()
                pins[pname] = self.resolver.canonical_slot(pin_match.group("slot"))

            enter_match = ENTER_RE.search(line)
            exit_match = EXIT_RE.search(line)
            show = parse_show_line(line)
            dlg = DIALOGUE_RE.match(line)

            # Enter tag.
            if enter_match:
                pname = enter_match.group("name").capitalize()
                result.append(line)
                if pname in self.policy_to_tag and pname not in visible:
                    visible.append(pname)
                    indent = re.match(r"^(\s*)", line).group(1)
                    result.extend(emit_layout(indent, {pname}))
                continue

            # Exit tag.
            if exit_match:
                pname = exit_match.group("name").capitalize()
                result.append(line)
                if pname in visible:
                    visible.remove(pname)
                    indent = re.match(r"^(\s*)", line).group(1)
                    result.append(self.render_hide(indent, pname))
                    slots.pop(pname, None)
                    result.extend(emit_layout(indent, set()))
                continue

            # Manual show line (kept verbatim; registers presence/expression/slot).
            if show is not None:
                result.append(line)
                pname = self.tag_to_policy.get(show.tag)
                if pname:
                    if pname not in visible:
                        visible.append(pname)
                    if show.expr:
                        exprs[pname] = show.expr
                    slots[pname] = self.resolver.canonical_slot(show.slot)
                continue

            # Dialogue: infer enter if speaker not yet visible.
            if dlg:
                speaker = dlg.group("speaker").lower()
                pname = self.speaker_to_policy.get(speaker)
                if pname and pname not in visible:
                    visible.append(pname)
                    indent = dlg.group("indent")
                    result.extend(emit_layout(indent, {pname}))
                result.append(line)
                continue

            result.append(line)

        return result

    def _is_auto_managed(self, line: str) -> bool:
        if not AUTO_RE.search(line):
            return False
        stripped = line.strip()
        return stripped.startswith("show ") or stripped.startswith("hide ")


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────
def is_excluded(path: Path, policy: dict) -> bool:
    norm = repo_path(path)
    for suffix in policy.get("excluded_files", []):
        if norm.endswith(suffix):
            return True
    return False


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Ren'Py Scene Direction Agent")
    parser.add_argument("--files", required=True, help="Comma-separated .rpy paths.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Report-only; exit 1 if any file is not already canonical.",
    )
    parser.add_argument("--policy", default=str(POLICY_PATH), help="Policy YAML path.")
    args = parser.parse_args(argv)

    policy = load_policy(Path(args.policy))
    registry = load_character_registry()
    if not registry:
        print("WARNING: no character registry derived from characters.rpy.", file=sys.stderr)
    director = SceneDirector(policy, registry)

    files = [f.strip() for f in args.files.split(",") if f.strip()]
    dirty = []
    processed = 0
    for f in files:
        path = resolve_file(f)
        if not path.exists() or path.suffix != ".rpy":
            continue
        if is_excluded(path, policy):
            print(f"SKIP (excluded by policy): {repo_path(path)}")
            continue
        original = read_text(path)
        lines = original.splitlines()
        new_lines = director.process_file(lines)
        trailing_nl = "\n" if original.endswith("\n") else ""
        new_text = "\n".join(new_lines) + trailing_nl
        processed += 1
        if new_text != original:
            dirty.append(path)
            if not args.check:
                path.write_text(new_text, encoding="utf-8")

    if not processed:
        print("No eligible .rpy files. Nothing to do.")
        return 0

    if args.check:
        if dirty:
            print("SCENE DIRECTION OUT OF DATE:")
            for p in dirty:
                print(f" - {repo_path(p)}")
            return 1
        print(f"Scene direction up to date ({processed} file(s)).")
        return 0

    if dirty:
        print(f"Updated scene direction in {len(dirty)} file(s):")
        for p in dirty:
            print(f" - {repo_path(p)}")
    else:
        print(f"Scene direction already current ({processed} file(s)).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
