# Writer: Add Effect

Lets the Writer attach a **stat consequence** to a moment in emotional terms (e.g. "Refusing the
money should sting her inspiration but feed the corruption"). The Desk maps it to the existing stat
vocabulary — it never invents counters.

## What to do

1. Load [`.agents/rules/writers_desk.md`](../../rules/writers_desk.md).
2. Translate her intent to the **existing** vocabulary only:
   - `insp` (inspiration), `corr` (corruption_xp), `anxiety`.
   - two-tier suspicion: `<char>_acute_susp` (heat) / `<char>_base_susp` (permanent) for
     `stern` / `vance` / `gideon` / `missy`. Generic `susp` is deprecated — steer to acute/base.
3. Record `apply_effects(...)`-shaped deltas in the **Authoring Intent** (`requested_effects`).
4. If she asks for a **genuinely new stat or mechanic**, **stop and escalate to**
   [`.agents/rules/chief_architect.md`](../../rules/chief_architect.md) — do not fabricate one.
5. Placement is handled downstream by `non_prod_code_agent` during shaping.

## Outputs

- Updated Authoring Intent with effect deltas; effects placed in draft (via code agent).
