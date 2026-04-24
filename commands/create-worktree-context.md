Scan every worktree and produce a shared WORKTREE_CONTEXT.md at the git common directory, visible to all branches.

## Step 1: Identify the worktree layout

Run:
```bash
git worktree list
```

This gives you the path and branch for every active worktree. Note the
git common directory — for a bare repo this is the bare repo folder
itself, for a regular repo it is the `.git/` directory of the main
worktree. All linked worktrees share it, so a file placed there is
readable from every branch checkout.

## Step 2: Identify the output path

Resolve the output path:
```bash
echo "$(git rev-parse --git-common-dir)/WORKTREE_CONTEXT.md"
```

Confirm this path with the user before writing.

## Step 3: Decide create vs refresh

If the file already exists at that path:
- Read it first.
- Preserve the "Open Items Across Branches" section verbatim — it is
  hand-maintained and must not be rewritten from a scan.
- Refresh all other sections from the current state.

If it does not exist, generate from scratch using the template in Step 5.

## Step 4: Scan each worktree

For each worktree found in Step 1, read:
- README.md (if present)
- Any CLAUDE.md (if present)
- The top-level directory structure (2 levels deep)
- CMakeLists.txt or equivalent build entry point (if present)
- Any docs/ directory contents

Do not read build artifacts, object files, or generated output directories.

If there are more than ~6 worktrees, do a full scan only on the active
ones (master, development, and any feature branches the user is working
on). For archived or legacy branches, a one-line summary per branch is
enough.

## Step 5: Produce WORKTREE_CONTEXT.md

Use today's actual date (not the literal string) on the `Last updated`
line. Write the file using this structure:

```markdown
# [Project Name] — Worktree Context
Last updated: [today's date, YYYY-MM-DD]
Generated from: [current branch name]

## Project Architecture

[2-3 paragraphs: what this project is, what it builds, what the key
subsystems are. Ground this in what is actually present across branches,
not in aspirational descriptions.]

### Key Modules / Subsystems
| Module | Location | Purpose    |
| ------ | -------- | ---------- |
| [name] | [path]   | [one line] |

### Build Entry Points
[How to build, what the main CMakeLists.txt or equivalent drives,
any non-obvious build requirements.]

---

## Branch Map

| Branch      | Worktree path  | Status      | What it contains / is doing |
| ----------- | -------------- | ----------- | --------------------------- |
| master      | ../master      | stable      | [summary]                   |
| development | ../development | active      | [summary]                   |
| legacy      | ../legacy      | archived    | [summary]                   |
| [feature]   | ../feature/... | in progress | [summary]                   |

### Branch Divergence Notes
[Any known significant differences between branches that would affect
where new work should go. For example: "development has refactored
the meshing pipeline -- master still uses the old interface."]

---

## Open Items Across Branches
[Anything unresolved, in-flight, or deferred that spans branches.
Update this section manually as work progresses.]
```

## Step 6: Confirm

Report the path the file was written to and summarise what was found
across branches. Flag any branch where content was sparse or ambiguous.
