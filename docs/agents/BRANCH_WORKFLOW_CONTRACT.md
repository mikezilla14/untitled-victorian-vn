# Branch workflow contract

This contract keeps multi-tool agent work from scattering across tool-named branches or hidden worktrees. It is source-control policy for humans and agents; it does not replace Git.

## Core rule

Use one branch per goal, not one branch per tool.

Good branch names:

- `feature/day106-ledger-discrepancy`
- `feature/sidebar-ui-polish`
- `fix/renpy-lint-day103`
- `docs/agent-branch-workflow`

Avoid tool-owned branch names for durable work, such as `claude/foo`, `codex/bar`, or `gemini/baz`, unless the branch is a short-lived experiment that will be merged or deleted before handoff.

## Before editing

Every agent that may write files must run:

```powershell
py scripts/agent_git_preflight.py --require-feature-branch --fail-if-dirty
```

The agent must report:

- Current branch
- Whether the working tree is clean
- Whether extra worktrees are registered
- Whether the branch name matches the task goal

If the preflight fails, stop before editing and ask the human whether to switch branches, commit existing work, or continue intentionally.

## Handoff rule

Commits are handoff points.

Before changing tools, the current tool must either:

- Commit the completed checkpoint, or
- Report the exact unstaged/staged files and why they are intentionally left dirty

The next tool must begin by rerunning the preflight and reviewing the previous commit or dirty-file report.

## Worktree rule

Worktrees are for deliberate parallel isolation, not routine tool switching.

Allowed:

- One temporary worktree for a clearly named feature branch
- A read-only review worktree
- A short-lived experiment that will be removed after merge or rejection

Avoid:

- Long-lived worktrees under tool cache folders
- Multiple worktrees editing the same feature files
- Worktrees on branches that have already been merged to `main`

After merging a feature, remove its worktree and delete its local branch.

## Main branch rule

`main` is the integration branch. Do not do normal agent edits directly on `main`.

Allowed exceptions:

- Tiny documentation or metadata fixes with human approval
- Emergency repair after a broken merge
- Final integration, merge conflict resolution, or release preparation

When editing on `main`, the agent must say why it is safe.

## Multi-tool coordination

Only one writing tool should own overlapping files between commits.

Safe:

- Tool A edits `screens.rpy`, commits, then Tool B continues from that commit.
- Tool A writes code while Tool B reviews the diff without editing.
- Tool A edits narrative while Tool B checks history read-only.

Risky:

- Two tools editing `screens.rpy` at the same time.
- One tool editing a worktree while another edits the same branch elsewhere.
- A tool starting from stale `main` while another has unpushed feature commits.

## Completion checklist

Before merging back to `main`:

1. Working tree is clean or intentionally documented.
2. Relevant validation has passed.
3. The feature branch contains the handoff commits from all tools.
4. Extra worktrees for the feature are removed.
5. The branch name still describes the work that landed.

After merging:

1. Delete the local feature branch.
2. Prune stale worktree registrations if needed.
3. Confirm `git branch` shows only the branches that should remain active.
