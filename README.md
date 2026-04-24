# myagents

Personal Claude Code configuration and workflow tooling.

## Install
The best way is to symlink the contents of this folder into your own `~/.claude`
directory.

```bash
git clone https://github.com/alonsoJASL/myagents 
cd /path/to/myagents 

mkdir -p ~/.claude/commands # just in case it's not there 

# do one by one 
ln -s $PWD/CLAUDE.md ~/.claude/ 

ln -s $PWD/commands/myinit.md ~/.claude/commands/ 
ln -s $PWD/commands/context_migration.md ~/.claude/commands/ 
ln -s $PWD/commands/export-api.md ~/.claude/commands/ 
ln -s $PWD/commands/import-api.md ~/.claude/commands/ 
```

## What's here

| File/Dir | Purpose |
|---|---|
| `CLAUDE.md` | Developer manifest — architectural principles and directives applied globally to all Claude Code sessions |
| `settings.json` | Claude Code configuration: status line, spinner verbs, effort level |
| `statusline.sh` | Bash script that renders session metrics (context %, token counts, cost, elapsed time) in the status bar |
| `commands/myinit.md` | Prompt for the `/myinit` skill — generates a project-level `CLAUDE.md` |
| `commands/context_migration.md` | Prompt for the `/context_migration` skill — produces a Transition Manifest for resuming across sessions |
| `commands/resume-skills.md` | Prompt for the `/resume-skills` skill — generates a resume-oriented skills summary of the current project |
| `commands/export-api.md` | Prompt for the `/export-api` skill — produces a structured API reference file for the current project |
| `commands/import-api.md` | Prompt for the `/import-api` skill — loads an external project's API reference to inform an implementation task |
| `commands/create-worktree-context.md` | Prompt for the `/create-worktree-context` skill — scans every worktree and writes a shared `WORKTREE_CONTEXT.md` at the git common directory |
| `commands/compare-branches.md` | Prompt for the `/compare-branches` skill — uses `WORKTREE_CONTEXT.md` to decide where new work should land across branches |

## Key concepts

**Developer manifest (`CLAUDE.md`)** — Encodes Jose's non-negotiables: separate orchestration from logic, explicit data contracts, stateless components, no singletons, no globals, dependency injection everywhere, Rule of Three before abstracting.

**Custom status line** — `statusline.sh` receives JSON from Claude Code and outputs a compact line showing model, context window usage (with a visual bar), token counts, cost, and session time.

**Slash commands** — `commands/*.md` files define skills invoked within Claude Code sessions. Each command is described below.

## Commands

| Command | What it does |
|---|---|
| `/myinit` | Analyzes the current project and generates a `CLAUDE.md` encoding its architecture, conventions, and key entry points |
| `/context_migration` | Produces a Transition Manifest — a structured handoff document for resuming work across context windows or sessions |
| `/resume-skills` | Scans the codebase and outputs a resume-oriented skills summary: concrete technologies and engineering competencies evidenced in the code |
| `/export-api` | Produces a structured API reference file for the current project, suitable for consumption by another project or orchestrator |
| `/import-api` | Loads an external project's API reference file and uses it to inform an implementation task in the current project |
| `/create-worktree-context` | Scans every worktree of the current repo and writes a shared `WORKTREE_CONTEXT.md` — project architecture, branch map, divergence notes — at the git common directory |
| `/compare-branches` | Reads `WORKTREE_CONTEXT.md` and compares branches for a specific task, then recommends where new work should land or flags that it already exists |

### Worktree workflow

`/create-worktree-context` and `/compare-branches` are a pair. When a project uses multiple long-lived worktrees (e.g. `master`, `development`, archived branches, feature branches), run `/create-worktree-context` once to produce a shared snapshot at the git common directory. After that, `/compare-branches` can answer "where should this new feature go?" or "does this already exist somewhere?" without re-scanning the entire repo each time. The snapshot is regenerated on demand; the "Open Items Across Branches" section is preserved across refreshes.

## Requirements

- Claude Code CLI
- `bash` and `jq` (for the status line script)
