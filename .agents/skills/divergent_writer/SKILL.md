# Divergent Writer (single persona)

Use when the writers' room needs one persona spec script (not the full orchestration pass).

## What to do

1. Load [`.agents/rules/divergent_writer_base.md`](../../rules/divergent_writer_base.md).
2. Load **one** `##` section from [`.agents/rules/divergent_writer_personas.md`](../../rules/divergent_writer_personas.md): `thematic`, `humour`, `tension`, `erotic`, `mystery`, or `class`.
3. Output: `main-game/pipeline/releases/<release>/dayrdd_<persona>_spec.rpy`

Do not load `main-game/pipeline/` for new assignments.

Parent workflow: [`.agents/rules/writers_room.md`](../../rules/writers_room.md).
