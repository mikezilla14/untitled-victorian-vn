# Writer: Write Book

Front door for authoring **Cora's Book1 manuscript** prose — the Holywell Street penny-dreadful
layer (e.g. "Write Coralie's Chapter 2 the prey way"). Plain language in; well-formed `book1_block_*`
prose out.

## What to do

1. Load [`.agents/rules/writers_desk.md`](../../rules/writers_desk.md).
2. Confirm layer = `book1_manuscript` and the chapter/state bucket in the Authoring Intent.
3. Honor the [Book Writing Contract](../../../docs/contracts/book_writing_contract.md):
   - prose lives in `book1_block_*` labels invoked via `book1_write_chapter(...)`;
   - manuscript transposition (Cora→Coralie Vale, Gideon→Lord Caldor, Vance→Lady Vayne, Stern→Mr.
     Sterick, Miri stays Miri; Ravenshade Conservatory setting);
   - NVL pagination constraint; no `story`/`player`/`time_manager` mutation in prose labels;
   - manuscript image changes are explicit cues for `call book1_set_page_image("image_name")`, not prose-embedded triggers;
   - no curly-brace macros or `BOOK1_PAYLOADS` for new MVP prose;
   - LLM safety fallback: tag risky passages `[HUMAN WRITE: SFW summary ...]` verbatim.
4. Capture prose verbatim into the Authoring Intent; run the **contract pre-check**.
5. Route to the [`book_writing_engine`](../book_writing_engine/SKILL.md) skill / Writers' Room for
   synthesis and gates; `non_prod_code_agent` supplies the Book Writing Context Packet and wraps approved prose into `book1_block_*` labels.

## Outputs

- Authoring Intent (book layer); `book1_block_*` prose labels (via Writers' Room + code agent);
  gate verdicts.
