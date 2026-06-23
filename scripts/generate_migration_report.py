#!/usr/bin/env python3
"""Generate the balance economy compression migration report CSV."""

import csv
import re
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

from balance_resolver import load_profiles
from validation.balance_profile_lint import load_bespoke_allowlist

def parse_apply_effects_raw(raw_call: str) -> dict[str, int]:
    if not raw_call or "apply_effects" not in raw_call:
        return {}
    match = re.search(r"apply_effects\s*\((.*)\)", raw_call)
    if not match:
        return {}
    args_str = match.group(1)
    kwargs = {}
    for part in args_str.split(","):
        part = part.strip()
        if "=" in part:
            k, v = part.split("=", 1)
            try:
                kwargs[k.strip()] = int(v.strip())
            except ValueError:
                pass
    return kwargs

def main():
    config = load_profiles()
    allowlist = load_bespoke_allowlist()

    legacy_choices_path = ROOT / "main-game" / "pipeline" / "releases" / "release-1-mvp" / "graph" / "release1_choices.csv"
    new_catalogue_path = ROOT / "main-game" / "draft" / "releases" / "planning" / "balance" / "choice_catalogue.csv"
    out_report_path = ROOT / "main-game" / "draft" / "releases" / "planning" / "balance" / "reports" / "balance_economy_compression_migration_report.csv"

    if not legacy_choices_path.exists():
        print(f"Legacy choices file not found: {legacy_choices_path}", file=sys.stderr)
        return 1

    if not new_catalogue_path.exists():
        print(f"New choice catalogue file not found: {new_catalogue_path}", file=sys.stderr)
        return 1

    # Read legacy choices into dict keyed by (label, option_key/choice_id)
    legacy_choices = {}
    with legacy_choices_path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            choice_id = row.get("option_key") or row.get("choice_id", "")
            label = row.get("label", "")
            key = (label, choice_id)
            legacy_choices[key] = row

    # Read new catalogue
    new_choices = []
    with new_catalogue_path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            new_choices.append(row)

    out_report_path.parent.mkdir(parents=True, exist_ok=True)

    report_fields = [
        "source_file",
        "line_number",
        "label",
        "choice_id",
        "old_raw_call",
        "old_insp_delta",
        "old_corr_delta",
        "old_witness_delta",
        "old_profile",
        "old_intensity",
        "new_profile",
        "new_intensity",
        "new_witness",
        "new_insp_delta",
        "new_corr_delta",
        "new_witness_susp_delta",
        "bespoke_reason",
        "allowlist_id",
        "migration_reason",
    ]

    report_rows = []
    for new_row in new_choices:
        choice_id = new_row.get("choice_id", "")
        # Find label in design note or guess
        design_note = new_row.get("design_note", "")
        source_file = ""
        line_number = ""
        match_src = re.search(r"Imported from graph choices \(([^:]+):(\d+)\)", design_note)
        if match_src:
            source_file = match_src.group(1)
            line_number = match_src.group(2)

        # Look up old choice
        old_row = None
        for (lbl, cid), val in legacy_choices.items():
            if cid == choice_id:
                # verify source file match if possible
                if source_file and source_file in val.get("source_file", ""):
                    old_row = val
                    break
        
        if not old_row:
            # Fallback matching by choice_id
            for (lbl, cid), val in legacy_choices.items():
                if cid == choice_id:
                    old_row = val
                    break

        old_raw_call = ""
        old_insp = ""
        old_corr = ""
        old_witness_susp = ""
        label_name = ""
        if old_row:
            old_raw_call = old_row.get("apply_effects_raw", "")
            old_kwargs = parse_apply_effects_raw(old_raw_call)
            old_insp = str(old_kwargs.get("insp", ""))
            old_corr = str(old_kwargs.get("corr", ""))
            # get first non-zero witness susp
            for k, v in old_kwargs.items():
                if k.endswith("_susp") or k.endswith("_base"):
                    old_witness_susp = str(v)
                    break
            label_name = old_row.get("label", "")

        new_profile = new_row.get("effect_profile", "")
        new_intensity = new_row.get("effect_intensity", "")
        new_witness = new_row.get("effect_witness", "")
        new_insp = new_row.get("insp_delta", "")
        new_corr = new_row.get("corr_xp_delta", "")

        # new witness susp delta
        new_witness_susp = ""
        for field in ("stern_susp_delta", "vance_susp_delta", "missy_susp_delta", "gideon_susp_delta"):
            val = new_row.get(field, "")
            if val:
                new_witness_susp = val
                break

        # Check if allowlisted
        allowlist_id = ""
        bespoke_reason = ""
        if not new_profile:
            # check bespoke reasons inallowlist
            allowed_entries = allowlist.get("allowed_bespoke_effects", {})
            for entry_name, entry in allowed_entries.items():
                entry_file = entry.get("file", "").replace("\\", "/")
                norm_rel_file = source_file.replace("\\", "/")
                if entry_file in norm_rel_file and entry.get("label") == label_name:
                    allowlist_id = entry_name
                    bespoke_reason = entry.get("reason", "legacy_exception")
                    break
            
            # Check reasons of pure negative suspicion or write spend
            if not bespoke_reason:
                if any(int(new_row.get(f, 0) or 0) < 0 for f in ("stern_susp_delta", "vance_susp_delta", "missy_susp_delta", "gideon_susp_delta")):
                    bespoke_reason = "negative_suspicion"
                elif int(new_row.get("insp_delta", 0) or 0) < 0:
                    bespoke_reason = "write_spend"
                elif any(int(new_row.get(f, 0) or 0) > 0 for f in ("stern_susp_delta", "vance_susp_delta", "missy_susp_delta", "gideon_susp_delta")):
                    bespoke_reason = "gate_failure_penalty"

        # Determine migration reason
        migration_reason = "Aligned to schema v2 standard profile"
        if not new_profile:
            migration_reason = f"Bespoke effect: {bespoke_reason}"
        elif new_profile == "creative":
            migration_reason = "Mapped to creative standard (craft/writing focus)"
        elif new_profile == "curious":
            migration_reason = "Mapped to curious standard with witness (snooping focus)"
        elif new_profile == "transgressive":
            migration_reason = "Mapped to transgressive standard with witness (boundary crossing)"
        elif new_profile == "observant":
            migration_reason = "Mapped to observant standard (noticing focus)"
        elif new_profile == "deceptive":
            migration_reason = "Mapped to deceptive standard with witness (lying/concealment)"

        report_rows.append({
            "source_file": source_file or old_row.get("source_file", "") if old_row else "",
            "line_number": line_number or old_row.get("line_number", "") if old_row else "",
            "label": label_name,
            "choice_id": choice_id,
            "old_raw_call": old_raw_call,
            "old_insp_delta": old_insp,
            "old_corr_delta": old_corr,
            "old_witness_delta": old_witness_susp,
            "old_profile": "",  # no old profiles in MVP graph
            "old_intensity": "",
            "new_profile": new_profile,
            "new_intensity": new_intensity,
            "new_witness": new_witness,
            "new_insp_delta": new_insp,
            "new_corr_delta": new_corr,
            "new_witness_susp_delta": new_witness_susp,
            "bespoke_reason": bespoke_reason,
            "allowlist_id": allowlist_id,
            "migration_reason": migration_reason,
        })

    with out_report_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=report_fields)
        writer.writeheader()
        writer.writerows(report_rows)

    print(f"Wrote migration report to {out_report_path.relative_to(ROOT).as_posix()}")

if __name__ == "__main__":
    sys.exit(main())
