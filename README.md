# myagents

Personal Claude Code configuration and workflow tooling.

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

## Requirements

- Claude Code CLI
- `bash` and `jq` (for the status line script)
