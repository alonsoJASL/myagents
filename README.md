# myagents

Personal Claude Code configuration and workflow tooling.

## Install

### macOS / Linux
Clone the repo and run `install.sh`. It symlinks `CLAUDE.md`, `settings.json`,
`statusline.sh`, every file in `commands/`, and every skill directory (e.g.
`scaffold-docs/`) into your `~/.claude` directory. Existing non-symlink files are
skipped rather than overwritten.

```bash
git clone https://github.com/alonsoJASL/myagents
cd myagents

./install.sh
```

Prefer to do it by hand? Symlink the same files yourself:

```bash
mkdir -p ~/.claude/commands

ln -sf $PWD/CLAUDE.md      ~/.claude/CLAUDE.md
ln -sf $PWD/settings.json  ~/.claude/settings.json
ln -sf $PWD/statusline.sh  ~/.claude/statusline.sh
ln -sf $PWD/commands/*.md  ~/.claude/commands/

mkdir -p ~/.claude/skills
ln -sfn $PWD/scaffold-docs   ~/.claude/skills/scaffold-docs
```

Because everything is a live symlink back to this repo, edits take effect in the
next Claude Code session — no reinstall needed.

### Windows
Clone the repo and run `install.ps1`. Windows can't symlink reliably without
elevation, so it **copies** `CLAUDE.md`, `settings.json`, every file in
`commands/`, and every skill directory (e.g. `scaffold-docs/`) into
`%USERPROFILE%\.claude`. Existing files are skipped unless you pass `-Force`.

```powershell
git clone https://github.com/alonsoJASL/myagents
cd myagents

powershell -ExecutionPolicy Bypass -File install.ps1
```

Two Windows-specific notes:

- **Edits don't auto-apply.** Because the files are copied rather than symlinked,
  re-run `install.ps1` (with `-Force`) after editing anything in the repo.
- **No custom status line.** `statusline.sh` is bash/jq based and isn't installed
  on Windows; the installer strips the `statusLine` setting from the copied
  `settings.json`, so Claude Code uses its default status line. Everything else
  in `settings.json` (model, spinner verbs, theme, effort) is preserved.

## What's here

| File/Dir | Purpose |
|---|---|
| `CLAUDE.md` | Developer manifest — architectural principles and directives applied globally to all Claude Code sessions |
| `settings.json` | Claude Code configuration: model, status line, spinner verbs, effort level, theme, enabled plugins |
| `statusline.sh` | Bash script that renders the status bar: working directory, model, context window usage, and 5-hour / 7-day rate-limit usage |
| `commands/myinit.md` | Prompt for the `/myinit` skill — generates a project-level `CLAUDE.md` |
| `commands/context_migration.md` | Prompt for the `/context_migration` skill — produces a Transition Manifest for resuming across sessions |
| `commands/resume-skills.md` | Prompt for the `/resume-skills` skill — generates a resume-oriented skills summary of the current project |
| `commands/export-api.md` | Prompt for the `/export-api` skill — produces a structured API reference file for the current project |
| `commands/import-api.md` | Prompt for the `/import-api` skill — loads an external project's API reference to inform an implementation task |
| `commands/create-worktree-context.md` | Prompt for the `/create-worktree-context` skill — scans every worktree and writes a shared `WORKTREE_CONTEXT.md` at the git common directory |
| `commands/compare-branches.md` | Prompt for the `/compare-branches` skill — uses `WORKTREE_CONTEXT.md` to decide where new work should land across branches |
| `scaffold-docs/` | Skill (directory + bundled `assets/`) — scaffolds or refreshes an MkDocs + Material docs site for any project (markdown, C/C++, Python) via language profiles |

## Key concepts

**Developer manifest (`CLAUDE.md`)** — Encodes Jose's non-negotiables: separate orchestration from logic, explicit data contracts, stateless components, no singletons, no globals, dependency injection everywhere, Rule of Three before abstracting.

**Custom status line** — `statusline.sh` receives JSON from Claude Code and outputs a compact line showing the working directory, model, context window usage, and 5-hour / 7-day rate-limit usage.

**Slash commands** — `commands/*.md` files define skills invoked within Claude Code sessions. Each command is described below.

**Skills with assets** — a skill that needs bundled files (templates, configs) lives as its own directory containing a `SKILL.md` orchestrator plus an `assets/` tree, rather than a single `commands/*.md` file. The installer links/copies these whole directories into `~/.claude/skills/`. `scaffold-docs` is the first of these.

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

## Skills

| Skill | What it does |
|---|---|
| `/scaffold-docs` | Scaffolds or refreshes an MkDocs + Material documentation site for any project. Run it from the target repo root. It resolves a **profile** — `markdown`, `cpp`, or `python` (auto-detected, or pass one explicitly: `/scaffold-docs cpp`) — then copies the generic docs kit, fills site/repo fields from the git remote, wires the matching API backend (none / Doxygen via `mkdoxy` / `mkdocstrings`), and verifies with `mkdocs build --strict`. |

### scaffold-docs vs pycemrg-docs

`scaffold-docs` is the language-agnostic generalisation of the suite-specific `pycemrg-docs` skill (which lives in the `pycemrg-context` repo). They share the same 8-step spine, but `scaffold-docs` reads everything language-specific from a profile descriptor instead of hardcoding it, and drops the CEMRG branding and suite palette registry. Use `pycemrg-docs` for a pycemrg-suite library; use `scaffold-docs` for anything else. Adding a new language is a matter of dropping a descriptor in `scaffold-docs/assets/profiles/`.

## Requirements

- Claude Code CLI
- macOS / Linux: `bash` and `jq` (for the status line script)
- Windows: PowerShell 5+ (the status line is not installed on Windows)
