# Contract: Book1 Label-Based Writing Engine

This contract defines how Book1 manuscript prose is authored in the non-canon Ren'Py draft.

Machine-readable schema: not defined. Track future executable schema work in
[../backlog/narrative-json-beat-pipeline.md](../backlog/narrative-json-beat-pipeline.md) if this
contract becomes executable.

## 1. Active Authoring Model

Book1 prose lives in Ren'Py labels. The active MVP system does not use the older inline curly-brace macro DSL for new prose.

Each major chapter branch should be a label named with the pattern:

```renpy
label book1_block_dayN_bucket_core:
    call book1_nvl_write_line("...", word_delay=_book1_word_delay)
    return
```

Optional reusable beats may be separate labels:

```renpy
label book1_block_day2_missy_debt_or_repair:
    if story.missy_day2_trust_break:
        call book1_nvl_write_line("...", word_delay=_book1_word_delay)
    else:
        call book1_nvl_write_line("...", word_delay=_book1_word_delay)
    return
```

## 2. Routing Contract

`book1.CHAPTER_BLOCKS` is the immutable routing table. It maps chapter keys and state buckets to prose labels.

Writers normally should not edit `CHAPTER_BLOCKS`. It changes only when adding a new top-level route bucket, such as a new chapter key or new major state variant.

Current MVP chapter keys:

- `day1_slop_chapter`
- `day1_chapter`
- `day2_chapter`
- `day3_chapter`
- `day4_triumphant_chapter`
- `day5_reckoning_chapter`

Day scripts call `book1_write_chapter(...)`; they do not contain manuscript prose.

Day time-period refactors must not move manuscript prose into day labels. Day files continue to call `book1_write_chapter(...)`; Book1 prose remains in `book1_block_*` labels.

## 3. Prose Label Rules

Allowed:

- Use `call book1_nvl_write_line("...", word_delay=_book1_word_delay)` for manuscript paragraphs.
- Use ordinary Ren'Py `if` / `elif` / `else` for local variation.
- Call other `book1_block_*` labels for optional multi-paragraph beats.
- End every prose label with `return`.

Forbidden:

- Do not mutate `story`, `player`, or `time_manager` inside prose labels.
- Do not apply stats, spend fuel, complete chapters, or route via `end_slot`.
- Do not write new prose inside `BOOK1_PAYLOADS`.
- Do not add curly-brace macro prose for new MVP content.

## 4. NVL Pagination And Word Reveal

All manuscript prose should pass through `book1_nvl_write_line(...)`.

That helper:

- reveals words one at a time through `book1_word_reveal_text(...)`;
- clears the NVL page after 4 rendered lines;
- preserves bottom whitespace on the current MVP NVL layout.

If future visual styling changes alter page capacity, adjust the page limit centrally in `book1_write_chapter(...)`; do not hand-clear pages inside prose labels.

## 5. Holywell Street Style

Book1 prose is Cora's sensational manuscript layer, not literal hotel narration.

- Cora becomes Coralie Vale.
- Gideon Locke becomes Lord Caldor.
- Lady Vance becomes Lady Vayne.
- Miss Stern becomes Mr. Sterick.
- Missy/Miri remains Miri as courier, witness, debt, or sacrifice.

The manuscript layer may be hotter, more symbolic, and more melodramatic than the hotel layer, but it must still reveal Cora's psychology: what she changes, emphasizes, hides, or makes herself enjoy is the dramatic point.

## 6. Safety Fallback

If a requested prose passage risks blocking generation:

- write a clean SFW summary instead of explicit prose;
- mark the passage with `[HUMAN WRITE: SFW summary of suggestive scene details]`;
- keep the label structurally valid and return cleanly.
