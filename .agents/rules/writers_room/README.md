# Writers' Room — Agent Rule Index

Writing orchestration rules live in the parent `.agents/rules/` directory (flat layout, same as `orchestrator.md` and other agents). This folder is an index only — do not duplicate rule files here.

## Entry point

| File | Role |
|------|------|
| [../writers_room.md](../writers_room.md) | **Writing Orchestration Agent** — intake, divergent pool, convergent handoff, contracts, context firewall |

## Sub-agents (load full file as system prompt)

| File | Role |
|------|------|
| [../divergent_writer_base.md](../divergent_writer_base.md) | Shared divergent rules (spec scripts, sidecars, framework calls) |
| [../divergent_writer_personas.md](../divergent_writer_personas.md) | Persona lenses — load **one** section: `thematic`, `humour`, `tension`, `erotic`, `mystery`, `class` |
| [../convergent_writer.md](../convergent_writer.md) | Red-pen synthesis → `dayrdd_non_canon.rpy` + required `dayrdd_convergent_report.md` |
| [../spiciness_tuning_agent.md](../spiciness_tuning_agent.md) | Optional 1-5 erotic intensity tuning rule for story/day/scene/passage/visual variants |
| [../forensic_psychology_consultant.md](../forensic_psychology_consultant.md) | Psychology gate and character profile consultant |

## Invoke pattern

**Divergent (per persona):** `divergent_writer_base.md` + the matching `##` section from `divergent_writer_personas.md`

**Order:** divergent → **convergent** → **lead_narrative_editor** → **forensic_psychology_consultant** → **victorian_consultant**

**Continuity:** Load `continuity_handoff.md` section `## Handoff → Day [dd]` only (not prior `dayrdd_non_canon.rpy`). Convergent updates `## Handoff → Day [dd+1]` after gates pass.

**Convergent:** `convergent_writer.md` after spec scripts. Delivers `dayrdd_non_canon.rpy` + decision report.

**Gates (on promotion draft only):** narrative editor first, then forensic psychology consultant, then Victorian consultant.

**Spice tuning:** If a task specifies level 1-5, a subset, or all levels, load [../spiciness_tuning_agent.md](../spiciness_tuning_agent.md). Single-level drafts proceed through normal writers-room gates. Multi-level outputs stay in `speculative/writing_experiments/` until the human selects a variant.

**Revisions (code, editor, or psychology):** `non_prod_code_agent`, `lead_narrative_editor`, or `forensic_psychology_consultant` files `dayrdd_narrative_change_brief.md` → workflows **D/E/E2** (scale S/M/L). Orchestrator: `revise-narrative`.

## Outputs (see also [speculative/README.md](../../../speculative/README.md))

- Spec scripts: `speculative/spec_scripts/releases/<release>/dayrdd_<persona>_spec.rpy`
- Brainstorming / idea logs: `speculative/idea_archive/releases/<release>/dayrdd_<persona>_ideas.md`
- Convergent Decision Report: `speculative/idea_archive/releases/<release>/dayrdd_convergent_report.md`
- Continuity handoff: `narrative/writers_room/releases/<release>/continuity_handoff.md` (read current day; write next day after gates)
- Promotion draft: `narrative/writers_room/releases/<release>/dayrdd_non_canon.rpy`
- Gate verdicts: `dayrdd_gate_lead_narrative.md`, `dayrdd_gate_forensic_psychology.md`, `dayrdd_gate_victorian.md`
- Psychology profile reports: `dayrdd_forensic_psychology_profile_report.md` when character profiles or voice guides change

## Production pipeline

Stage 1 of `produce-day` is documented in [../orchestrator.md](../orchestrator.md).
