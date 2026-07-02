# Book writing engine export

Self-contained export pack for **external LLM** generation of Cora Hartley's Book1 manuscript (`book1_*` labels). These files are reference documentation — not runtime game source.

**Status:** `active-support` (authoring aid). Runtime truth lives in `main-game/non-prod-game/game/days/book1_non_canon.rpy` and related shared modules.

## Files

| File | Purpose |
|------|---------|
| [system_prompt.md](system_prompt.md) | Master system prompt for the prose generation engine |
| [style_and_voice_guide.md](style_and_voice_guide.md) | Manuscript tone, formatting, and voice rules |
| [characters_and_locations.md](characters_and_locations.md) | IRL → fictional cast/setting mapping |
| [narrative_summary_and_flag_wiring.md](narrative_summary_and_flag_wiring.md) | Day timeline and flag wiring schema |
| [prompt_catalogue.md](prompt_catalogue.md) | Flag-agnostic prompt templates per day/archetype |
| [integration_guide.md](integration_guide.md) | Import header format and validation after paste |
| [engine_payload_example.json](engine_payload_example.json) | Example structured payload for tooling |

## In-repo workflow

Prefer the Writer's Desk and [`book_writing_engine`](../../.agents/skills/book_writing_engine/SKILL.md) skill for in-repo work. Use this export when handing context to an external model or offline prompt runner.

## Validation after import

```powershell
py scripts/validate.py --profile changed --agent human --files "main-game/non-prod-game/game/days/book1_day101_non_canon.rpy"
```

Contract: [`docs/contracts/book_writing_contract.md`](../../docs/contracts/book_writing_contract.md) · Schema: [`book_writing_contract.schema.json`](../../docs/contracts/book_writing_contract.schema.json) · Routing: [`book1_chapter_routing.json`](../../docs/contracts/book1_chapter_routing.json)
