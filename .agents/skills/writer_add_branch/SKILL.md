# Writer: Add Branch

Lets the Writer add a **choice / branching path** described by meaning, not syntax (e.g. "Add a
choice to warn Missy or stay silent"). The Desk derives the structure; she never picks `jump`/`call`
or names labels.

## What to do

1. Load [`.agents/rules/writers_desk.md`](../../rules/writers_desk.md).
2. For each arm capture: **player-facing text**, the **psychological mode** it expresses
   (**Observer / Predator / Prey / Ghost** — cosmetic-only menus are forbidden), the flag it sets,
   and the effects it applies.
3. Derive structure per the routing-refactor contract
   ([`docs/specs/story-chain-routing-refactor.md`](../../../docs/specs/story-chain-routing-refactor.md)):
   fixed forks in time-period spines; optional content in a **named dynamic window** that is called
   and returns; queued consequences in authored consequence windows.
4. Record the branch in the **Authoring Intent** (`requested_branches`). New per-arm flags follow
   `writer_add_flag`; new effects follow `writer_add_effect`.
5. If arms need new dialogue, **route prose to the Writers' Room** (`revise-narrative` /
   `produce-day`); route structure to `non_prod_code_agent`. Run the contract pre-check first.

## Outputs

- Updated Authoring Intent; branch structure + verbatim prose in draft; gate verdicts.
