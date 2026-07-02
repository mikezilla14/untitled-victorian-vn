# Normal day prose export

Self-contained export pack for **external LLM** generation of Savoy Hotel IRL ADV layer prose (`dayNNN_*` labels). These files are reference documentation — not runtime game source.

**Status:** `active-support` (authoring aid). Runtime truth lives in `main-game/non-prod-game/game/days/dayNNN_non_canon.rpy`.

## Files

| File | Purpose |
|------|---------|
| [system_prompt.md](system_prompt.md) | Master system prompt for Savoy ADV prose |
| [style_and_voice_guide.md](style_and_voice_guide.md) | Dialogue tone, staging, and syntax rules |
| [variables_and_flag_wiring.md](variables_and_flag_wiring.md) | Stat/flag wiring reference for IRL scenes |
| [prompt_catalogue.md](prompt_catalogue.md) | Templates for create / rewrite / revise tasks |
| [integration_guide.md](integration_guide.md) | Paste targets, indentation, and validation |
| [payload_example.json](payload_example.json) | Example structured payload for tooling |

## In-repo workflow

Prefer Writer's Desk → `writer-author`, `revise-narrative`, or `rewrite-narrative` for in-repo work. Use this export when handing context to an external model.

Scene direction and `[asset auto]` staging are applied in-repo after gates — see [`scene_direction`](../../.agents/skills/scene_direction/SKILL.md).

## Validation after import

```powershell
py scripts/validate.py --profile changed --agent human --files "main-game/non-prod-game/game/days/day101_non_canon.rpy"
py scripts/historical_linter.py main-game/non-prod-game/game/days/day101_non_canon.rpy
```
