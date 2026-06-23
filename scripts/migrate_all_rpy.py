import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# We will define exact string-to-string replacements for each file.
# This avoids regex lookbehind/lookahead complications.

replacements_100 = {
    'apply_balanced_effect("curious", intensity="major")': 'apply_balanced_effect("creative", intensity="standard")',
    'apply_balanced_effect("transgressive", intensity="major")': 'apply_balanced_effect("creative", intensity="standard")',
    'apply_balanced_effect("observant", intensity="minor")': 'apply_balanced_effect("observant", intensity="standard")',
    'apply_balanced_effect("obedient", intensity="minor")': 'apply_balanced_effect("observant", intensity="standard")',
    'apply_balanced_effect("safe", intensity="minor")': 'apply_balanced_effect("observant", intensity="standard")',
    'apply_balanced_effect("curious", intensity="minor")': 'apply_balanced_effect("creative", intensity="standard")',
    'apply_balanced_effect("transgressive", intensity="standard")': 'apply_balanced_effect("creative", intensity="standard")',
}

replacements_101 = {
    'apply_balanced_effect("submissive", intensity="standard")': 'apply_balanced_effect("observant", intensity="standard")',
    'apply_balanced_effect("defiant", intensity="standard", witness="stern")': 'apply_balanced_effect("curious", intensity="standard", witness="stern")',
    'apply_balanced_effect("obedient", intensity="standard")': 'apply_balanced_effect("observant", intensity="standard")',
    'apply_balanced_effect("defiant", intensity="standard", witness="stern")': 'apply_balanced_effect("observant", intensity="standard")',
    'apply_balanced_effect("transgressive", intensity="major")': 'apply_balanced_effect("transgressive", intensity="standard", witness="stern")',
    'apply_balanced_effect("reckless", intensity="major", witness="stern")': 'apply_balanced_effect("transgressive", intensity="standard", witness="stern")',
    'apply_balanced_effect("submissive", intensity="standard", witness="vance")': 'apply_balanced_effect("observant", intensity="standard")',
    'apply_balanced_effect("defiant", intensity="standard", witness="vance")': 'apply_balanced_effect("curious", intensity="standard", witness="vance")',
    'apply_balanced_effect("self_protective", intensity="standard", witness="vance")': 'apply_balanced_effect("observant", intensity="standard")',
    'apply_balanced_effect("transgressive", intensity="major", witness="vance")': 'apply_balanced_effect("transgressive", intensity="standard", witness="vance")',
    'apply_balanced_effect("observant", intensity="standard", witness="vance")': 'apply_balanced_effect("observant", intensity="standard")',
    'apply_balanced_effect("obedient", intensity="standard", witness="vance")': 'apply_balanced_effect("observant", intensity="standard")',
    'apply_balanced_effect("reckless", intensity="standard", witness="vance")': 'apply_balanced_effect("transgressive", intensity="standard", witness="vance")',
    'apply_balanced_effect("predatory", intensity="standard", witness="vance")': 'apply_balanced_effect("transgressive", intensity="standard", witness="vance")',
    'apply_balanced_effect("reckless", intensity=1.4, witness="vance")': 'apply_balanced_effect("transgressive", intensity="standard", witness="vance")',
    
    # L1128 & L1198
    'apply_balanced_effect("creative", intensity="major")': 'apply_balanced_effect("creative", intensity="standard")',

    # L993 Ghost path
    '# [STATE bespoke] Multi-witness suspicion reduction; cannot map to one profile\n            $ apply_effects(stern_susp=-5, vance_susp=-5, missy_susp=-5, insp=10, corr=0)':
    '$ apply_balanced_effect("creative", intensity="standard")\n            # [STATE bespoke: negative_suspicion]\n            $ apply_effects(stern_susp=-5, vance_susp=-5, missy_susp=-5)',

    '# [STATE] Multi-witness suspicion reduction; cannot map to one profile\n            $ apply_effects(stern_susp=-5, vance_susp=-5, missy_susp=-5, insp=10, corr=0)':
    '$ apply_balanced_effect("creative", intensity="standard")\n            # [STATE bespoke: negative_suspicion]\n            $ apply_effects(stern_susp=-5, vance_susp=-5, missy_susp=-5)',

    # L1268 Write spend
    '# [STATE bespoke] Fixed write spend; negative inspiration not profile-scaled\n    $ apply_effects(insp=-10, corr=0)':
    '# [STATE bespoke: write_spend]\n    $ apply_effects(insp=-10)',

    '# [STATE] Fixed write spend; negative inspiration not profile-scaled\n    $ apply_effects(insp=-10, corr=0)':
    '# [STATE bespoke: write_spend]\n    $ apply_effects(insp=-10)'
}

replacements_102 = {
    'apply_balanced_effect("transgressive", intensity="major", witness="vance")': 'apply_balanced_effect("transgressive", intensity="standard", witness="vance")',
    'apply_balanced_effect("curious", intensity="standard")': 'apply_balanced_effect("curious", intensity="standard", witness="missy")',
    'apply_balanced_effect("reckless", intensity="minor", witness="vance")': 'apply_balanced_effect("transgressive", intensity="standard", witness="vance")',
    'apply_balanced_effect("defiant", intensity="major", witness="stern")': 'apply_balanced_effect("transgressive", intensity="standard", witness="stern")',
    'apply_balanced_effect("predatory", intensity="major", witness="stern")': 'apply_balanced_effect("transgressive", intensity="standard", witness="stern")',
    'apply_balanced_effect("transgressive", intensity="major")': 'apply_balanced_effect("creative", intensity="standard")', # fallback for sneak feel
    
    # L330
    '# [STATE bespoke] Eager posture: careful observation drops Stern suspicion\n            $ apply_effects(stern_susp=-5, insp=15, corr=0)':
    '$ apply_balanced_effect("creative", intensity="standard")\n            # [STATE bespoke: negative_suspicion]\n            $ apply_effects(stern_susp=-5)',

    # L762 framing Missy
    '# [STATE] Semantic balance profile: Cora frames Missy by hiding the letters in her vanity\n    $ apply_balanced_effect("deceptive", intensity="standard", witness="stern")':
    '$ apply_balanced_effect("deceptive", intensity="standard", witness="stern")',

    'apply_balanced_effect("transgressive", intensity="major")': 'apply_balanced_effect("deceptive", intensity="standard", witness="stern")',

    # L1109 & L1155 write spend
    '# [STATE bespoke] Write spend: inspiration cost to write\n            $ apply_effects(vance_susp=0, insp=-10, corr=0)':
    '# [STATE bespoke: write_spend]\n            $ apply_effects(insp=-10)',

    '# [STATE bespoke] Write spend: inspiration cost to write (additional depth)\n            $ apply_effects(vance_susp=0, insp=-15, corr=0)':
    '# [STATE bespoke: write_spend]\n            $ apply_effects(insp=-15)'
}

replacements_103 = {
    'apply_balanced_effect("defiant", intensity="standard", witness="vance")': 'apply_balanced_effect("transgressive", intensity="standard", witness="vance")',
    'apply_balanced_effect("defiant", intensity="major", witness="stern")': 'apply_balanced_effect("transgressive", intensity="standard", witness="stern")',
    'apply_balanced_effect("transgressive", intensity="major", witness="vance")': 'apply_balanced_effect("transgressive", intensity="standard", witness="vance")',
    'apply_balanced_effect("creative", intensity="major")': 'apply_balanced_effect("creative", intensity="standard")',
    'apply_balanced_effect("defiant", intensity="major", witness="vance")': 'apply_balanced_effect("transgressive", intensity="standard", witness="vance")',
    'apply_balanced_effect("transgressive", intensity="major")': 'apply_balanced_effect("transgressive", intensity="standard", witness="stern")',
    'apply_balanced_effect("reckless", intensity="major", witness="vance")': 'apply_balanced_effect("transgressive", intensity="standard", witness="vance")',
    'apply_balanced_effect("curious", intensity="minor")': 'apply_balanced_effect("curious", intensity="standard", witness="stern")',
    'apply_balanced_effect("defiant", intensity="standard", witness="stern")': 'apply_balanced_effect("transgressive", intensity="standard", witness="stern")',

    # L160 split
    '# [STATE bespoke] Eager posture: careful observation drops Stern suspicion\n            $ apply_effects(stern_susp=-5, insp=15, corr=0)':
    '$ apply_balanced_effect("creative", intensity="standard")\n            # [STATE bespoke: negative_suspicion]\n            $ apply_effects(stern_susp=-5)',

    # L463
    '# [STATE bespoke] Submissive posture: accepting corruption to secure raw material\n    $ apply_effects(vance_susp=5, insp=5, corr=20)':
    '$ apply_balanced_effect("transgressive", intensity="standard", witness="vance")',

    # L704
    '# [STATE bespoke] Frantic write: inspiration gain with immediate Stern suspicion\n    $ apply_effects(stern_susp=10, insp=20, corr=0)':
    '$ apply_balanced_effect("curious", intensity="standard", witness="stern")',

    # L739
    '# [STATE bespoke] Penance: preparing the mask before Stern calls, dropping suspicion\n            $ apply_effects(stern_susp=-20, insp=0, corr=0)':
    '# [STATE bespoke: negative_suspicion]\n            $ apply_effects(stern_susp=-20)',

    # L832
    '# [STATE bespoke] Negative Stern suspicion: careful posture restores propriety\n            $ apply_effects(stern_susp=-10, insp=0, corr=0)':
    '# [STATE bespoke: negative_suspicion]\n            $ apply_effects(stern_susp=-10)',

    # L851
    '# [STATE bespoke] Positive Stern suspicion: inspiration with minor risk\n            $ apply_effects(stern_susp=5, insp=10, corr=0)':
    '$ apply_balanced_effect("observant", intensity="standard")',

    # L871
    '# [STATE bespoke] Positive Stern suspicion: minor corruption with suspicion increase\n            $ apply_effects(stern_susp=10, insp=0, corr=5)':
    '$ apply_balanced_effect("curious", intensity="standard", witness="stern")',

    # L1130
    '# [STATE bespoke] Erotic surrender: high corruption with heavy Vance suspicion\n    $ apply_effects(vance_susp=15, insp=10, corr=25)':
    '$ apply_balanced_effect("transgressive", intensity="standard", witness="vance")',

    # L1236 & L1255 & L1261
    '# [STATE bespoke] Write penalty: inspiration cost with Stern suspicion spike\n                $ apply_effects(stern_susp=5, insp=-20, corr=0)':
    '# [STATE bespoke: write_spend]\n                $ apply_effects(insp=-20)\n                # [STATE bespoke: gate_failure_penalty]\n                $ apply_effects(stern_susp=5)',

    '# [STATE bespoke] Eager write: inspiration gain with minor corruption\n                $ apply_effects(stern_susp=0, insp=5, corr=5)':
    '$ apply_balanced_effect("creative", intensity="standard")',

    '# [STATE bespoke] Delayed write: Stern suspicion penalty\n                $ apply_effects(stern_susp=10, insp=0, corr=0)':
    '# [STATE bespoke: gate_failure_penalty]\n                $ apply_effects(stern_susp=10)'
}

replacements_104 = {
    'apply_balanced_effect("creative", intensity="major")': 'apply_balanced_effect("creative", intensity="standard")',
    'apply_balanced_effect("reckless", intensity=1.4, witness="stern")': 'apply_balanced_effect("transgressive", intensity="standard", witness="stern")',
    'apply_balanced_effect("reckless", intensity=1.6, witness="vance")': 'apply_balanced_effect("transgressive", intensity="standard", witness="vance")',
    'apply_balanced_effect("submissive", intensity="standard", witness="stern")': 'apply_balanced_effect("observant", intensity="standard")',

    # L368 cover exception
    '# [STATE bespoke] Mixed witness recovery: Vance suspicion drops, Missy spikes, builds corruption\n            $ apply_effects(vance_susp=-15, missy_susp=20, insp=5, corr=20)':
    '# [STATE bespoke: legacy_exception]\n            $ apply_effects(vance_susp=-15, missy_susp=20, insp=5, corr=20)',

    # L509
    '# [STATE bespoke] Negative Stern suspicion: careful posture restores propriety\n            $ apply_effects(stern_susp=-15, insp=0, corr=0)':
    '# [STATE bespoke: negative_suspicion]\n            $ apply_effects(stern_susp=-15)',

    # L525
    '# [STATE bespoke] Positive Stern suspicion: inspiration with minor risk\n            $ apply_effects(stern_susp=5, insp=10, corr=0)':
    '$ apply_balanced_effect("observant", intensity="standard")',

    # L541 pressure exception
    '# [STATE bespoke] Mixed witness cost: Stern drops, Missy spikes, builds corruption\n            $ apply_effects(stern_susp=-10, missy_susp=10, insp=0, corr=10)':
    '# [STATE bespoke: legacy_exception]\n            $ apply_effects(stern_susp=-10, missy_susp=10, corr=10)',

    # L650, 659, 668
    '# [STATE bespoke] Negative suspicion relief: visible soot penance after fireplace escape\n    $ apply_effects(stern_susp=-30, insp=0, corr=0)':
    '# [STATE bespoke: negative_suspicion]\n    $ apply_effects(stern_susp=-30)',

    '# [STATE bespoke] Negative suspicion relief: saintly dullness after bold-lie escape\n    $ apply_effects(stern_susp=-25, insp=0, corr=0)':
    '# [STATE bespoke: negative_suspicion]\n    $ apply_effects(stern_susp=-25)',

    '# [STATE bespoke] Negative suspicion relief: visible usefulness after missy-cover escape\n    $ apply_effects(stern_susp=-10, insp=0, corr=0)':
    '# [STATE bespoke: negative_suspicion]\n    $ apply_effects(stern_susp=-10)',

    # L696
    '# [STATE bespoke] Negative Missy suspicion: opening the repair conversation\n  $ apply_effects(missy_susp=-15, insp=5, corr=0)':
    '$ apply_balanced_effect("creative", intensity="standard")\n            # [STATE bespoke: negative_suspicion]\n            $ apply_effects(missy_susp=-15)',

    # L727 Missy partial truth exception
    '# [STATE bespoke] Mixed witness repair: romantic truth rebuilds Missy, costs Vance\n  $ apply_effects(missy_susp=-25, vance_susp=5, insp=15, corr=10)':
    '# [STATE bespoke: legacy_exception]\n            $ apply_effects(missy_susp=-25, vance_susp=5, insp=15, corr=10)',

    # L750
    '# [STATE bespoke] Negative Missy suspicion: coward\'s comfort without real repair\n  $ apply_effects(missy_susp=-10, insp=0, corr=5)':
    '$ apply_balanced_effect("creative", intensity="standard")\n            # [STATE bespoke: negative_suspicion]\n            $ apply_effects(missy_susp=-10)',

    # L904 triumphant write spend
    '# [STATE bespoke] Triumphant write cost: inspiration spend with Stern suspicion spike\n  $ apply_effects(stern_susp=15, insp=-15, corr=0)':
    '# [STATE bespoke: write_spend]\n    $ apply_effects(insp=-15)\n    # [STATE bespoke: gate_failure_penalty]\n    $ apply_effects(stern_susp=15)'
}

replacements_105 = {
    'apply_balanced_effect("creative", intensity="major")': 'apply_balanced_effect("creative", intensity="standard")',
    'apply_balanced_effect("transgressive", intensity="major")': 'apply_balanced_effect("transgressive", intensity="standard", witness="gideon")',
    'apply_balanced_effect("transgressive", intensity="standard")': 'apply_balanced_effect("transgressive", intensity="standard", witness="gideon")',

    # L534
    '# [STATE bespoke] Negative Vance suspicion: ghost witness names the unseen machinery\n  $ apply_effects(vance_susp=-5, insp=15, corr=5)':
    '$ apply_balanced_effect("creative", intensity="standard")\n            # [STATE bespoke: negative_suspicion]\n            $ apply_effects(vance_susp=-5)',

    # L716
    '# [STATE bespoke] Negative Vance suspicion: ghost deferral without refusal\n  $ apply_effects(vance_susp=-5, insp=5, corr=5)':
    '$ apply_balanced_effect("creative", intensity="standard")\n            # [STATE bespoke: negative_suspicion]\n            $ apply_effects(vance_susp=-5)'
}

replacements_chains = {
    '# [STATE] Safe path: closes loop, drops suspicion\n  $ apply_effects(stern_susp=-10, insp=5, corr=0)':
    '$ apply_balanced_effect("creative", intensity="standard")\n  # [STATE bespoke: negative_suspicion]\n  $ apply_effects(stern_susp=-10)',

    '# [STATE] Charged path: locks in progression, spikes stats\n  $ apply_effects(stern_susp=15, insp=15, corr=5)':
    '$ apply_balanced_effect("transgressive", intensity="standard", witness="stern")',

    '# [STATE] Safe path: closes loop\n  $ apply_effects(stern_susp=-10, insp=5, corr=0)':
    '$ apply_balanced_effect("creative", intensity="standard")\n  # [STATE bespoke: negative_suspicion]\n  $ apply_effects(stern_susp=-10)',

    '# [STATE] Charged path: Level 3/4 tension, high suspicion spike\n  $ apply_effects(stern_susp=20, insp=20, corr=10)':
    '$ apply_balanced_effect("transgressive", intensity="standard", witness="stern")',

    '# [STATE] Safe path: closes loop\n  $ apply_effects(stern_susp=-15, insp=5, corr=0)':
    '$ apply_balanced_effect("creative", intensity="standard")\n  # [STATE bespoke: negative_suspicion]\n  $ apply_effects(stern_susp=-15)',

    '# [STATE] Charged path: Level 4 tease, triggers Penance checkpoint\n  $ apply_effects(stern_susp=25, insp=20, corr=20)':
    '$ apply_balanced_effect("transgressive", intensity="standard", witness="stern")',

    '# [STATE] Safe path: closes loop\n  $ apply_effects(missy_susp=-10, insp=10, corr=0)':
    '$ apply_balanced_effect("creative", intensity="standard")\n  # [STATE bespoke: negative_suspicion]\n  $ apply_effects(missy_susp=-10)',

    '# [STATE] Charged path: Level 3 tactile intimacy, builds romantic trust\n  $ apply_effects(missy_susp=10, insp=10, corr=5)':
    '$ apply_balanced_effect("curious", intensity="standard", witness="missy")',

    '# [STATE] Safe path: closes loop\n  $ apply_effects(missy_susp=-15, insp=10, corr=0)':
    '$ apply_balanced_effect("creative", intensity="standard")\n  # [STATE bespoke: negative_suspicion]\n  $ apply_effects(missy_susp=-15)',

    '# [STATE] Charged path: High intimacy, Level 3 tension, active desire\n  $ apply_effects(missy_susp=15, insp=15, corr=10)':
    '$ apply_balanced_effect("transgressive", intensity="standard", witness="missy")',

    '# [STATE] Safe path: closes loop\n  $ apply_effects(missy_susp=-20, insp=5, corr=0)':
    '$ apply_balanced_effect("creative", intensity="standard")\n  # [STATE bespoke: negative_suspicion]\n  $ apply_effects(missy_susp=-20)',

    '# [STATE] Charged path: Level 3 Erotic Climax, sovereign submission/intimacy\n  $ apply_effects(missy_susp=20, insp=20, corr=20)':
    '$ apply_balanced_effect("transgressive", intensity="standard", witness="missy")',

    '# [STATE] Safe path: closes loop\n  $ apply_effects(vance_susp=-10, insp=5, corr=0)':
    '$ apply_balanced_effect("creative", intensity="standard")\n  # [STATE bespoke: negative_suspicion]\n  $ apply_effects(vance_susp=-10)',

    '# [STATE] Charged path: Level 3 voyeurism\n  $ apply_effects(vance_susp=15, insp=15, corr=5)':
    '$ apply_balanced_effect("curious", intensity="standard", witness="vance")',

    '# [STATE] Safe path: closes loop\n  $ apply_effects(vance_susp=-15, insp=5, corr=0)':
    '$ apply_balanced_effect("creative", intensity="standard")\n  # [STATE bespoke: negative_suspicion]\n  $ apply_effects(vance_susp=-15)',

    '# [STATE] Charged path: Level 3/4 dominance play\n  $ apply_effects(vance_susp=15, insp=20, corr=10)':
    '$ apply_balanced_effect("transgressive", intensity="standard", witness="vance")',

    '# [STATE] Safe path: closes loop\n  $ apply_effects(vance_susp=-20, insp=5, corr=0)':
    '$ apply_balanced_effect("creative", intensity="standard")\n  # [STATE bespoke: negative_suspicion]\n  $ apply_effects(vance_susp=-20)',

    '# [STATE] Charged path: Level 4 tease, triggers Penance checkpoint\n  $ apply_effects(vance_susp=20, insp=20, corr=20)':
    '$ apply_balanced_effect("transgressive", intensity="standard", witness="vance")',

    '# [STATE] State/progression update\n  $ apply_effects(stern_susp=-35, insp=0, corr=5)':
    '# [STATE bespoke: legacy_exception]\n  $ apply_effects(stern_susp=-35, corr=5)',

    '# [STATE] State/progression update\n  $ apply_effects(vance_susp=-35, insp=0, corr=5)':
    '# [STATE bespoke: legacy_exception]\n  $ apply_effects(vance_susp=-35, corr=5)',

    '# [STATE] State/progression update\n  $ apply_effects(missy_susp=-35, insp=5)':
    '# [STATE bespoke: legacy_exception]\n  $ apply_effects(missy_susp=-35, insp=5)'
}

def migrate_file(file_path, replacements):
    content = file_path.read_text(encoding="utf-8")
    for old, new in replacements.items():
        content = content.replace(old, new)
    file_path.write_text(content, encoding="utf-8")
    print(f"Migrated {file_path.name}")

def main():
    migrate_file(ROOT / "main-game" / "non-prod-game" / "game" / "days" / "day100_non_canon.rpy", replacements_100)
    migrate_file(ROOT / "main-game" / "non-prod-game" / "game" / "days" / "day101_non_canon.rpy", replacements_101)
    migrate_file(ROOT / "main-game" / "non-prod-game" / "game" / "days" / "day102_non_canon.rpy", replacements_102)
    migrate_file(ROOT / "main-game" / "non-prod-game" / "game" / "days" / "day103_non_canon.rpy", replacements_103)
    migrate_file(ROOT / "main-game" / "non-prod-game" / "game" / "days" / "day104_non_canon.rpy", replacements_104)
    migrate_file(ROOT / "main-game" / "non-prod-game" / "game" / "days" / "day105_non_canon.rpy", replacements_105)
    migrate_file(ROOT / "main-game" / "non-prod-game" / "game" / "shared" / "story_chains_non_canon.rpy", replacements_chains)

if __name__ == "__main__":
    main()
