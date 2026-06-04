# Branch Handoff

Use this skill before any agent edits files in a multi-tool workflow, and whenever work is handed from one tool to another.

## When to use

- Before starting feature or fix work.
- Before switching from one tool to another.
- Before creating or using a worktree.
- After merging a feature back to `main`.
- When the repo has unexpected branches, dirty files, or stale worktrees.

## What to do

1. Read the branch workflow contract:
   ```powershell
   Get-Content docs/agents/BRANCH_WORKFLOW_CONTRACT.md
   ```
2. Run the preflight before editing:
   ```powershell
   py scripts/agent_git_preflight.py --require-feature-branch --fail-if-dirty
   ```
3. If the script fails, stop before editing and report the reason.
4. Confirm the branch name matches the task goal.
5. Keep one writing tool active for overlapping files until the next commit.
6. Commit before handing the work to another tool, or report the exact dirty files and why they are intentionally uncommitted.

## Optional checks

Use these when preparing to merge or clean up:

```powershell
py scripts/agent_git_preflight.py --fail-if-dirty --fail-if-extra-worktrees
git branch --merged main
git worktree list
```

## Handoff report

End each tool handoff with:

- Branch name
- Commit hash, if committed
- Dirty files, if any
- Validation run and result
- Recommended next tool or next action
