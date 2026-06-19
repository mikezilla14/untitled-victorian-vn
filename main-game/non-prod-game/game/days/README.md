# Day drafts

This folder contains non-canon day scripts used as the source for future promotion.

## Naming contract

- Day drafts use `dayNNN_non_canon.rpy`, for example `day105_non_canon.rpy`.
- Book/manuscript support files may use domain-specific names, for example `book1_non_canon.rpy`.
- Test harnesses must make their purpose obvious in the filename and must not be reachable from the normal player `start` path.

## Source-of-truth rule

For prose and day flow, these draft files are the source of truth for future promotion. If a production file receives a hotfix, mirror the relevant prose/routing change back here or record the exception in the promotion handoff.

## Agent boundary

- Writers' room / Writer's Desk: owns prose intent and generated draft prose.
- Scene direction: may touch `[asset auto]` show/hide lines only.
- Non-prod code agent: may wrap approved prose and implement sandbox mechanics.
- Prod code agent: promotes from here to `main-game/prod-game/` after gates and checks.
