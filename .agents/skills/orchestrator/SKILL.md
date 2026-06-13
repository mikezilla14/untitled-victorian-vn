# Production Orchestrator (default entry)

Use this skill for **any** cross-repo production task when the user has not already named a narrow specialist.

## What to do

1. Load [`.agents/rules/orchestrator.md`](../../rules/orchestrator.md) as the governing system instructions.
2. Classify the user request using the **Classification Logic** in that file.
3. If ambiguous (bare "assess", "review", "compare" without lens), ask **one** follow-up before invoking agents.
4. For each pipeline stage, load the named agent's full rule file from `.agents/rules/` and pass artifacts per the Handoff Contract.

## Human docs

- [AGENTS.md](../../../AGENTS.md) — catalog and quick start
- [docs/agents/SKILL_CATALOG.md](../../../docs/agents/SKILL_CATALOG.md) — **skill → agent → pipeline → contract**
- [docs/agents/GETTING_STARTED.md](../../../docs/agents/GETTING_STARTED.md)
- [docs/agents/PIPELINE_REFERENCE.md](../../../docs/agents/PIPELINE_REFERENCE.md)

**Not this skill:** prose-first Writer → `writer_*` skills + `writers_desk.md`. Documentation hygiene → `documentation_audit` + `documentation_steward.md`.

## Do not

- Generate story content or edit files directly as the orchestrator.
- Skip gate order on new promotion drafts (narrative → forensic psychology → Victorian).
- Load `narrative/pipeline/**/ideas/` or `synthesis/` for new writing assignments unless the user requests archive mining.
