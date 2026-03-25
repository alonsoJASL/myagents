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

## Key concepts

**Developer manifest (`CLAUDE.md`)** — Encodes Jose's non-negotiables: separate orchestration from logic, explicit data contracts, stateless components, no singletons, no globals, dependency injection everywhere, Rule of Three before abstracting.

**Custom status line** — `statusline.sh` receives JSON from Claude Code and outputs a compact line showing model, context window usage (with a visual bar), token counts, cost, and session time.

**Slash commands** — `commands/*.md` files define skills invoked as `/myinit` and `/context_migration` within Claude Code sessions.

## Requirements

- Claude Code CLI
- `bash` and `jq` (for the status line script)
