# Scene Direction

Use this skill to **apply deterministic sprite placement** to a draft Ren'Py script — adding,
updating, or preserving `show ... at <slot>` direction lines according to the fixed layout policy,
without touching dialogue, backgrounds, or manual staging.

## When to use

- **After the Writers' Room produces or rewrites a scene** and before `non_prod_code_agent` wraps it
  (pipeline Stage 1.5 of `produce-day` / `rewrite-narrative`; Stage 5.5 of `revise-narrative`).
- **After dialogue expansion or scene restructuring** changed who is on screen.
- **As a regression check** in CI / pre-PR to catch stale or duplicated `[asset auto]` lines.

## What to do

1. **Check first (report-only, no writes):**
   ```powershell
   py scripts/scene_direction.py --check --files "<path1>,<path2>"
   ```
   - Exit `0` → `[COMPLIANCE PASS]` equivalent: direction already canonical.
   - Exit `1` → files listed need re-direction.
2. **Apply in place:**
   ```powershell
   py scripts/scene_direction.py --files "<path1>,<path2>"
   ```
3. **Re-format afterwards.** The `[asset auto]` lines are staging commands, so run the non-canon
   formatter **after** directing (it adds the `# [ASSET]` marker comments):
   ```powershell
   py scripts/format_non_canon.py <path1> <path2>
   ```
   Order matters: scene-direction first, then format. The pair is a stable fixpoint.
4. **Review the diff.** Only `# [asset auto]` `show`/`hide` lines (and their `# [ASSET]` markers)
   should change. Dialogue, `# [asset lock:scene]` blocks, `# [asset keep]` lines, manual shows, and
   block-form `show ...:` ATL statements must be byte-for-byte unchanged.
5. **Resolve warnings.** A `# [asset warning: more than 4 visible characters; ...]` means the scene
   exceeds the four-slot layout and needs manual staging — do not let the tool guess.

## Compliance Contract

- The layout policy is [`docs/contracts/sprite_layout_policy.yaml`](../../../docs/contracts/sprite_layout_policy.yaml)
  (schema: `sprite_layout_policy.schema.json`).
- Sprite tags are derived from `characters.rpy`; an undeclared speaker is skipped, not guessed.
- `day100_non_canon.rpy` and `day101_non_canon.rpy` are excluded (hand-directed).
- Running the tool twice must yield no diff (idempotence). A non-zero exit from `--check` in CI is a
  compliance breach: re-run without `--check` and commit the result.
