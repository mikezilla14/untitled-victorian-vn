# MVP Systems Integration Checklist

> **Owner:** Technical / systems (you)  
> **Partner scope:** Prose rewrite inside existing labels and `book1_block_*` blocks  
> **Post-prose scope:** Scene-specific CGs and any new backgrounds/sprites the rewrite introduces  
> **Target tree:** `main-game/non-prod-game/`  
> **Design reference:** `planning/story_board.md`, `planning/continuity_handoff.md`

Use this as the gate for **“structure done — ready for final prose drop.”** Check boxes as you complete and verify each item.

---

## Milestone definitions

| Milestone | Meaning |
|-----------|---------|
| **M1 — Trustworthy spine** | A player can reach Day 105 ending without test harness; gates and progress counters behave per `story_board.md` |
| **M2 — Dynamic systems** | Chains, penance, soft/hard fails all fire and recover correctly |
| **M3 — Book loop** | All five write slots call `book1_write_chapter` with correct theme keys and update `manuscript_progress` |
| **M4 — Structural assets** | UI, audio, and non-prose backgrounds/sprites in place; game is playable without gray-box shame |
| **M5 — Prose drop ready** | M1–M4 done; partner can land rewrite without touching routing |
| **M6 — Ship candidate** | Partner prose merged; manifest closed for new art; full QA matrix green |

---

## Partner coordination contract (freeze while you integrate)

- [ ] **Label names frozen** — no renames to `day[R][dd]_[p]_*` spine labels without sync to you
- [ ] **Menu structure frozen** — choices may change copy, not branch count or jump targets
- [ ] **State blocks frozen** — partner does not edit `$ apply_effects(...)`, `$ story.set_*`, or `complete_manuscript_chapter` lines
- [ ] **Book1 boundary clear** — IRL hotel prose in `day*_non_canon.rpy`; penny-dreadful pseudonym prose in `book1_block_*` (`book1_non_canon.rpy`)
- [ ] **Rewrite intake path agreed** — partner delivers per-day or full pass; you run gates after merge

---

## Phase 1 — Writing gates & manuscript progress (M1, M3)

*Prose-agnostic. Do first — current build can soft-lock on deadlines.*

### 1.1 `has_story_fuel` contract — **AND semantics (decided)**

Both `player.inspiration` and `player.corruption_level` must meet their floors. **Not a sum.**

Constants in `functions_non_canon.rpy`:

| Constant | Values | Use |
|----------|--------|-----|
| `WRITE_GATE_CH1` | (15, 2) | D101 write menu, D102 Ch1 catch-up |
| `WRITE_GATE_CH2` | (30, 3) | D102 Ch2; `bad_ending_rejection` floor |
| `WRITE_GATE_CH3` | (45, 3) | D103 Ch3 |
| `WRITE_SLOP_MAX_CORRUPTION_LEVEL` | 2 | D101 slop vs real chapter |

| # | Task | Files | Done |
|---|------|-------|------|
| 1.1.1 | AND contract + constants | `functions_non_canon.rpy` | [x] |
| 1.1.2 | `PlayerStats.has_story_fuel` docstring + default `required_corr=3` | `classes_non_canon.rpy` | [x] |
| 1.1.3 | Global wrapper + constants | `functions_non_canon.rpy` | [x] |
| 1.1.4 | `attempt_write()` default `required_corr=3` | `functions_non_canon.rpy` | [x] |
| 1.1.5 | Document in `classes_non_canon_notes.md` + `story_board.md` | planning docs | [x] |

### 1.2 Per-slot gate alignment (`story_board.md` § Daily Story Gates)

| Slot | Gate | Hook | Done |
|------|------|------|------|
| Day 101 night write menu | `WRITE_GATE_CH1` | `has_story_fuel(*WRITE_GATE_CH1)` | [x] |
| Day 101 slop vs real chapter | `corruption_level <= 2` → slop | `WRITE_SLOP_MAX_CORRUPTION_LEVEL` | [x] |
| Day 102 night Ch1 catch-up | `WRITE_GATE_CH1` | `has_story_fuel(*WRITE_GATE_CH1)` | [x] |
| Day 102 night Ch2 | `WRITE_GATE_CH2` | `has_story_fuel(*WRITE_GATE_CH2)` | [x] |
| Day 103 night Ch3 | `WRITE_GATE_CH3` | `has_story_fuel(*WRITE_GATE_CH3)` or frantic_write | [x] |
| Day 104 twilight triumphant | `ANXIETY_WRITE_PARALYSIS` (85) blocks write | Single menu branch; atonement + `missy_repair_available()` escape | [x] |

**Files:** `days/day101_non_canon.rpy`, `days/day102_non_canon.rpy`, `days/day103_non_canon.rpy`, `days/day104_non_canon.rpy`

### 1.3 `manuscript_progress` / `complete_manuscript_chapter`

**Problem:** Day 101 write never calls `complete_manuscript_chapter` — `manuscript_progress` stays 0 → `game_over_deadline_1` at `day103_morning`.

| # | Task | Files | Done |
|---|------|-------|------|
| 1.3.1 | Real D101 chapter (`corruption_level > 2`) calls `complete_manuscript_chapter("day1_chapter")`; slop does not | `day101_non_canon.rpy` | [x] |
| 1.3.2 | Day 102 catch-up only when `manuscript_progress == 0` | `day102_non_canon.rpy` | [x] |
| 1.3.3 | Ch2 via `complete_manuscript_chapter("day2_chapter")` | `day102_non_canon.rpy` | [x] |
| 1.3.4 | Ch3 / Ch4 triumphant / Ch5 reckoning increment via `complete_manuscript_chapter` | `day103`–`day105` | [x] |
| 1.3.5 | HUD inkwell chapter ticks match `story.manuscript_progress` | `screens.rpy` | [x] |
| 1.3.6 | Ledger UI shows correct chapter count | `screens.rpy` (`ledger_ui`) | [x] |

### 1.4 Deadline gates (hard fail)

| Label | Trigger | Expected | Verify | Done |
|-------|---------|----------|--------|------|
| `day103_morning` | `manuscript_progress == 0` | `game_over_deadline_1` | Reachable only when player skipped all Ch1 paths | [ ] |
| `day104_6_false_dawn_ending` | `manuscript_progress < 2` | `game_over_deadline_2` | Reachable when Ch1+Ch2 not done by Day 4 night | [ ] |

**Files:** `days/day103_non_canon.rpy`, `days/day104_non_canon.rpy`, `endings.rpy`

---

## Phase 2 — Fail states (M1, M2)

### 2.1 Hard fails

| Ending | Trigger | Wired? | Task | Done |
|--------|---------|--------|------|------|
| `game_over_dismissed` | `player.anxiety >= 100` | `script.rpy` `check_suspicion`; `story_chains_non_canon.rpy` `check_confrontations` | Playtest: force anxiety to 100 mid-run | [ ] |
| `game_over_deadline_1` | No Ch1 by Day 3 morning | `day103_morning` | Playtest: skip all writing | [ ] |
| `game_over_deadline_2` | `manuscript_progress < 2` by Day 4 close | `day104_6_false_dawn_ending` | Playtest: only Ch1 complete | [ ] |

### 2.2 Soft fail / bad ending

| Ending | Trigger (README / design) | Wired? | Task | Done |
|--------|---------------------------|--------|------|------|
| `bad_ending_rejection` | `corruption_level < 3` by Day 5 night | `day105_6_manuscript_reckoning` | Wired via `WRITE_GATE_CH2[1]` | [x] |

**Files:** `endings.rpy`, `days/day105_non_canon.rpy`

### 2.3 Soft consequences (non-terminal)

| System | Behavior | Verify | Done |
|--------|----------|--------|------|
| Day 101 slop chapter | Low-corruption first write → `day1_slop_chapter` | Reachable + does not brick deadlines per design | [ ] |
| Day 103 barricade | Failed Ch3 gate → barricade path | Still advances to Day 104 | [ ] |
| Day 104 anxiety block | Cannot triumphant write at `ANXIETY_WRITE_PARALYSIS` | Atonement always; Missy repair when cover used | [x] |
| Penance acute relief | −35 acute on confrontation | Anxiety drops after penance | [ ] |

---

## Phase 3 — Main story spine (M1)

*Walk every handoff once without test harness.*

### 3.1 Day-by-day spine checklist

| Day | Entry label | Exit / handoff | Time periods routed | Done |
|-----|-------------|----------------|---------------------|------|
| 100 | `day100_main` | → `day101_1_cora_waiting` | Prologue complete | [x] |
| 101 | `day101_main` | → `day102_1_cora_missy_first_shift` | Morning → Afternoon → Evening consequence → Night window/write | [ ] |
| 102 | `day102_1_cora_missy_first_shift` | → `day103_morning` | Morning contraband → Afternoon chains → Evening tea crisis → Night write/indulge | [ ] |
| 103 | `day103_morning` | → `day104_1_false_dawn_suite_window` | Morning consequence → Afternoon Gideon → Evening frantic → Night ultimatum + write | [ ] |
| 104 | `day104_morning` | → `day105_1_monster_reemerges` | Morning heist → Afternoon escape → Evening twilight → Night triumphant/false dawn | [ ] |
| 105 | `day105_1_monster_reemerges` | → `day105_7_release_one_ending` | Summons → leverage → motivation → marks → reckoning → MVP end | [ ] |

**Files:** `days/day100_non_canon.rpy` … `day105_non_canon.rpy`, `script.rpy`

### 3.2 Branch smoke tests (one run each)

| Branch axis | Values to hit once | Done |
|-------------|-------------------|------|
| `day1_corridor_state` | predator / prey / ghost | [ ] |
| `day1_ledger_focus` | inspiration / corruption | [ ] |
| `day2_contraband_state` | stolen_wearing / planted_in_trunk | [ ] |
| `day2_tea_choice` | prey / predator / ghost | [ ] |
| `day3_brush_choice` | predator / prey / ghost | [ ] |
| `day3_ultimatum` | defied / bargained / surrendered | [ ] |
| `day4_escape_state` | fireplace / bold_lie / missy_cover | [ ] |
| `day5_dynamic` | muse / protege / adversary / witness | [ ] |
| `day5_money_choice` | taken / refused / deferred | [ ] |

---

## Phase 4 — Dynamic content: story chains & penance (M2)

### 4.1 Consequence windows

**Watch-only** (story-chain window consumes penance): `call watch_suspicion` → `return`.

**Watch + consume** (no story window follows): `call watch_suspicion` → `call consume_pending_penance(window_id)` → `return`.

Shared labels in `story_chains_non_canon.rpy`: `watch_suspicion`, `consume_pending_penance`, `story_window_penance_gate`.

| Window | Day | Mode | Done |
|--------|-----|------|------|
| `day101_evening_consequence_window` | 101 | watch-only | [x] |
| `day102_afternoon_consequence_window` | 102 | watch-only | [x] |
| `day102_night_consequence_window` | 102 | watch + consume | [x] |
| `day103_morning_consequence_window` | 103 | watch-only | [x] |
| `day103_evening_consequence_window` | 103 | watch + consume | [x] |
| `day103_night_consequence_window` | 103 | watch + consume | [x] |
| `day104_evening_consequence_window` | 104 | watch + consume | [x] |
| `day104_night_consequence_window` | 104 | watch + consume | [x] |

**Files:** `days/day101_non_canon.rpy` … `day104_non_canon.rpy`, `shared/story_chains_non_canon.rpy`

### 4.2 Optional story-chain windows

Story windows: `call story_window_penance_gate(window_id)` at entry; if `_penance_consumed`, `return` (sacrifices chain slot). All dynamic blocks `return` to spine — spine owns `jump` to next period/day.

| Window | Characters | Done |
|--------|------------|------|
| `day101_night_story_window` | stern / missy / vance chains | [x] |
| `day102_afternoon_story_window` | stern / missy / vance chains | [x] |
| `day103_1_optional_character_chain` | corridor + chains | [x] |

**Verify:** `story.chain_available(character)` gates levels 1–3; `resolve_chain_label` returns valid label; chain labels `return` to caller.

**Files:** `shared/story_chains_non_canon.rpy`, `shared/classes_non_canon.rpy` (`stern_chain_level`, etc.)

### 4.3 Penance labels

| Label | Character | Fires at combined susp ≥ 50 | Done |
|-------|-----------|-------------------------------|------|
| `confrontation_stern` | Stern | [x] | [x] |
| `confrontation_vance` | Vance | [x] | [x] |
| `confrontation_missy` | Missy | [x] | [x] |

### 4.4 Deprecated routers (do not use in new code)

- [x] Confirm no new `jump end_slot` or `jump advance_after_confrontation` in day files
- [x] Compatibility labels remain but are not on critical path

---

## Phase 5 — Book writing system (M3)

### 5.1 Write slot inventory

| Night / slot | Label | `book1_write_chapter` key | Theme key variable | `complete_manuscript_chapter` | Done |
|--------------|-------|---------------------------|--------------------|------------------------------|------|
| D101 night | `day101_4_write_the_chapter` | `day1_chapter` / `day1_slop_chapter` | `day1_corridor_state` | real Ch1 only (`corruption_level > 2`) | [x] |
| D102 night catch-up | `day102_4_cora_writes_a_chapter` | `day1_chapter` | `day1_corridor_state` | `day1_chapter` | [x] |
| D102 night Ch2 | same | `day2_chapter` | `day2_tea_choice` | `day2_chapter` | [x] |
| D103 night | `day103_3_bedroom_final_write` | `day3_chapter` | `day3_brush_choice` | `day3_chapter` | [x] |
| D104 night | `day104_5_triumphant_chapter` | `day4_triumphant_chapter` | `day2_tea_choice` | `day4_triumphant_chapter` | [x] |
| D105 night | `day105_6_manuscript_reckoning` | `day5_reckoning_chapter` | `day5_dynamic` | `day5_reckoning_chapter` | [x] |

**Files:** `days/book1_non_canon.rpy`, day files above, `screens.rpy` (`screen nvl`)

### 5.2 Book1 routing

- [x] Every key in `book1.CHAPTER_BLOCKS` has a reachable `book1_block_*` label
- [x] `book1_block_unknown_chapter` is unreachable in normal play
- [x] `book1_page_image` store var set per branch when CG art exists (stub acceptable until Phase 6)
- [x] NVL screen renders without missing-image crashes (fallbacks acceptable)
- [x] `book1_write_chapter` plays `audio_themes_private_ink` when file present

### 5.3 Test harness (dev only)

| Label | Purpose | Done |
|-------|---------|------|
| `test_day2_writing_harness` | Branch matrix for book1 | [x] |
| `test_book1_render_day*` | Per-chapter render | [x] |

**File:** `days/test_day2_writing_non_canon.rpy` — keep for QA; exclude from player `start` path.

---

## Phase 6 — Structural assets (M4)

*Do not wait for prose rewrite — these unblock integration testing.*

### 6.1 UI (book writing + HUD)

| Asset ID | Path expected | Status | Done |
|----------|---------------|--------|------|
| `ui_book_writing_paper` | `images/ui/book_writing_paper.png` | Missing | [ ] |
| `ui_book_cover` | `images/ui/book_cover.png` | Missing | [ ] |
| `ui_book_ui_bg` | `images/ui/book_ui_bg.png` | Missing | [ ] |
| `ui_illustration_border` | `images/ui/illustration_border.png` | Missing | [ ] |
| `ui_price_badge` | `images/ui/price_badge.png` | Missing | [ ] |
| `ui_sidebar_bg` | `images/ui/ui_sidebar_bg.png` | Copied from `ui_sidebar_bg.png_` | [x] |
| `ui_sidebar_divider` | `images/ui/ui_sidebar_divider.png` | Missing | [ ] |
| `ui_vignette_ambient` | `images/ui/ui_vignette_ambient.webp` | Present | [x] |
| `ui_suspicion_vignette` | `images/ui/ui_suspicion_vignette.webp` | Present | [x] |
| `ui_cora_base` / `ui_cora_corrupted` | `images/sprites/cora/ui/` | Present | [x] |
| `mc_sprite_thought_icon` | placeholder acceptable for M4 | [ ] |

**File:** `game/assets_manifest.rpy`, `game/screens.rpy`

### 6.2 Backgrounds (structural)

| Asset ID | Used in | On disk? | In manifest? | Done |
|----------|---------|----------|--------------|------|
| `bg_train_carriage_day` | Day 100 | No | Yes (fallback) | [x] |
| `bg_country_estate_study` | Day 100 flashback | No | Yes (fallback) | [x] |
| `bg_cora_desk_night` | Write scenes | No | Yes (fallback) | [ ] |
| `bg_master_suite_night` | Day 103 night | No | Yes (fallback) | [ ] |
| `bg_servants_quarters_dusk` | Quarters scenes | No | Yes (fallback) | [ ] |
| Savoy corridor / laundry / suite day | Days 101–105 | Mostly yes | Yes | [x] |

### 6.3 Sprites (structural)

| Asset | Issue | Done |
|-------|-------|------|
| `gideon_sprite neutral` | Manifest points to `neutralf.png` interim | [x] |
| Core cast expressions for spine scenes | Audit vs `story_board.md` § Assets | [ ] |

### 6.4 Audio

**Current state:** `game/audio/` dirs created; files still needed. Day 100 + book1 use guarded `if audio_*` plays.

| Priority | Alias | Suggested use | Done |
|----------|-------|---------------|------|
| P0 | `themes/private_ink` | All write scenes | [ ] |
| P0 | `sfx/ink_scratch` | `book1_write_chapter` | [ ] |
| P1 | `themes/master_suite_pressure` | Gideon suite (103, 105) | [ ] |
| P1 | `ambient/hotel_corridor_muffled` | Corridors | [ ] |
| P1 | `themes/savoy_tension` | General hotel | [ ] |
| P2 | Remaining manifest aliases | Per `assets_manifest.rpy` | [ ] |

**Tasks:**
- [ ] Add audio files under `game/audio/`
- [x] Guard `play music`/`play sound` with `if audio_*` pattern (Day 100, book1)
- [x] Declare `themes/melancholy`, `sfx/train_whistle` in manifest (Day 100)
- [ ] Strip or wire remaining `[ASSET]` audio callouts in day scripts

---

## Phase 7 — Code hygiene & promotion prep (M5)

| # | Task | Done |
|---|------|------|
| 7.1 | `renpy lint` — zero errors on non_prod project | [ ] |
| 7.2 | Update `non_prod_main-game/prod-game/README.md` (file names, flat insp cap 50, endings list) | [ ] |
| 7.3 | Resolve `classes_non_canon.rpy` header comment (“NOT loaded”) — Ren'Py loads all `.rpy` under `game/` | [ ] |
| 7.4 | Run asset compliance script when available; fix unmanifested references | [x] |
| 7.5 | `storyboard_sync` after mechanics land — close graph drift | [ ] |
| 7.6 | Remove dev debris from `images/` (`ChatGPT Image*.png`, `*.png~`, `rembg.bat`) or gitignore | [ ] |

---

## Phase 8 — After partner prose rewrite (M6)

*Your partner owns prose; you own manifest + integration.*

| # | Task | Done |
|---|------|------|
| 8.1 | Merge prose — no label/menu/routing changes without your review | [ ] |
| 8.2 | Re-run narrative gates if branch structure changed | [ ] |
| 8.3 | Scan new `[ASSET]` / `scene` / `show` lines for manifest entries | [ ] |
| 8.4 | Add manuscript CGs: `cg_manuscript_retelling_d1`–`d4` per `story_board.md` | [ ] |
| 8.5 | Add `cg_gideon_photograph`, `cg_photograph_burning` — uncomment show lines in Day 104–105 | [ ] |
| 8.6 | Set `book1_page_image` per branch for NVL illustration frame | [ ] |
| 8.7 | Final playthrough matrix (below) all green | [ ] |

---

## Playtest matrix — “structure done” sign-off

Run from `label start` with **no test harness** and no debug cheats.

### Required paths

| # | Path | Reach | Done |
|---|------|-------|------|
| P1 | **Corruption-leaning** — prey corridor, corruption ledger, write nights, defied ultimatum, fireplace escape, adversary motivation | `day105_7_release_one_ending` | [ ] |
| P2 | **Cautious** — ghost corridor, inspiration ledger, barricade or low Ch3, atonement twilight | `day105_7_release_one_ending` | [ ] |
| P3 | **Low corruption** — trigger `bad_ending_rejection` OR confirm design replaced it | `bad_ending_rejection` | [ ] |
| P4 | **Deadline fail 1** — skip all Ch1 | `game_over_deadline_1` | [ ] |
| P5 | **Deadline fail 2** — Ch1 only, skip Ch2 by Day 4 | `game_over_deadline_2` | [ ] |
| P6 | **Anxiety collapse** | `game_over_dismissed` | [ ] |
| P7 | **Penance** — one confrontation per character across runs | confrontation labels | [ ] |

### Manuscript verification per path

- [ ] balance report static pass — `py scripts/balance_report.py --release release-1-mvp` (no `FAIL`; `INCOMPLETE` expected until simulator/captures exist)
- [ ] P1: `manuscript_progress >= 2` before Day 104 false-dawn gate
- [ ] P1: `book1_write_chapter` fires at least 3 times with distinct theme keys
- [ ] P2: Story completes with lower corruption without dead-ending on deadlines unintentionally

---

## Quick reference — key files

| Concern | Path |
|---------|------|
| Entry / anxiety check | `game/script.rpy` |
| State classes | `game/shared/classes_non_canon.rpy` |
| Effect helpers | `game/shared/functions_non_canon.rpy` |
| Chains & penance | `game/shared/story_chains_non_canon.rpy` |
| Book engine | `game/days/book1_non_canon.rpy` |
| Endings | `game/endings.rpy` |
| HUD / NVL / ledger | `game/screens.rpy` |
| Asset declarations | `game/assets_manifest.rpy` |
| Day scripts | `game/days/day100_non_canon.rpy` … `day105_non_canon.rpy` |
| Testing / balance (static) | `scripts/balance_report.py` → `main-game/pipeline/releases/release-1-mvp/reports/balance_report.md` |
| Design gates | `planning/story_board.md` |
| Continuity | `planning/continuity_handoff.md` |
| Graph audit | `main-game/pipeline/releases/release-1-mvp/graph/release1_graph_audit.md` |

---

## Suggested work order (single thread)

1. Phase 1 (gates + `complete_manuscript_chapter` on D101)  
2. Phase 2 (`bad_ending_rejection` wire)  
3. Phase 3 spine walkthrough — fix jumps as you go  
4. Phase 4 penance spot-check  
5. Phase 5 book slot verification  
6. Phase 6 UI + desk BG + Gideon neutral + P0 audio  
7. Phase 7 lint + README  
8. **→ M5: hand prose rewrite to partner**  
9. Phase 8 after merge  

---

*Last updated: 2026-06-09 — generated from MVP joint review.*
