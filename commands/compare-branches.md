Compare what exists across branches to decide where new functionality should live or whether it already exists.

## Step 1: Load shared context

Check if WORKTREE_CONTEXT.md exists at the shared git common directory:
```bash
cat "$(git rev-parse --git-common-dir)/WORKTREE_CONTEXT.md"
```

If it does not exist, tell the user to run /create-worktree-context first
and stop here.

## Step 2: Get the task description

If the user already provided a task alongside the command, use that and
skip the questions. Otherwise ask:
1. What do you want to implement or find?
2. Which branches are candidates? (or: should I check all of them?)

If only one branch is named, treat this as "does X already exist in
branch Y, and is Y the right place for it" rather than a multi-branch
comparison.

## Step 3: Inspect the relevant branches

For each candidate branch, look at the specific area relevant to the task.
Use the branch map from WORKTREE_CONTEXT.md to find the right worktree paths.

Run targeted searches rather than reading entire trees. Prefer `rg`
(ripgrep) when available:
```bash
# Find relevant files by pattern
rg -l "[relevant term]" ../[branch] 2>/dev/null \
  || grep -rl "[relevant term]" ../[branch] 2>/dev/null

# Check if a module or file exists
ls ../[branch]/[relevant path] 2>/dev/null

# Diff a specific file between branches
diff ../[branch_a]/[file] ../[branch_b]/[file]
```

Read only the files directly relevant to the task. Do not do a full
re-scan of branches already covered by WORKTREE_CONTEXT.md.

## Step 4: Produce a comparison and recommendation

Present:

### What exists across branches
| Branch   | Relevant file / module | Status                         | Notes  |
| -------- | ---------------------- | ------------------------------ | ------ |
| [branch] | [file or "absent"]     | [current / stale / refactored] | [note] |

### Recommendation
State clearly:
- Whether the functionality already exists in any branch
- If it exists: which branch has the most current version and whether
  it can be used as-is or needs porting
- If it does not exist: which branch is the right place to implement it
  and why (based on the branch map and divergence notes)
- Any risk: e.g. "development has diverged from master here -- implementing
  in development means this won't be in master without a merge"

### Proposed next step
One sentence: what should happen next and in which branch.

This command is read-only: do not run `git checkout`, do not edit files,
do not stage anything. Stop after the recommendation and wait for the
user to decide.
