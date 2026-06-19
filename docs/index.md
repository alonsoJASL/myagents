---
layout: home
title: myagents
---

**myagents** is a personal configuration set for [Claude Code](https://claude.ai/code), the AI coding assistant that runs in your terminal. It wires up a custom developer manifest, a compact status line, and a handful of slash commands that make sessions faster and more structured.

---

## Quick install

You need [Claude Code](https://claude.ai/code) and `git`. That's it.

### macOS / Linux

```bash
git clone https://github.com/alonsoJASL/myagents
cd myagents

./install.sh   # optional — if you know how to symlink, you can do that yourself
```

`install.sh` symlinks `CLAUDE.md`, `settings.json`, `statusline.sh`, and every
file in `commands/` into `~/.claude`. Because they're live symlinks, later edits
to the repo take effect in your next session — no reinstall needed.

### Windows

```powershell
git clone https://github.com/alonsoJASL/myagents
cd myagents

powershell -ExecutionPolicy Bypass -File install.ps1
```

Windows can't symlink reliably without elevation, so `install.ps1` **copies** the
files into `%USERPROFILE%\.claude` instead. Two consequences:

- Because they're copies, re-run `install.ps1 -Force` after editing the repo for
  your changes to take effect.
- The status line is bash/jq based and isn't installed on Windows; the installer
  strips the `statusLine` setting from the copied `settings.json`, so Claude Code
  uses its default status line. Everything else (model, spinner verbs, theme,
  effort) is preserved.

Once the installer finishes, open a new Claude Code session and everything is active.

---

## What you get

### José's Developer manifest

`CLAUDE.md` is a set of José's standing instructions that Claude reads at the start of every session. It encodes architectural principles, for example things like "separate orchestration from logic", "no singletons or globals", "wait for the Rule of Three before abstracting". That way you never have to re-explain these coding standards to the model.

### Status line

`statusline.sh` adds a live info bar to every Claude Code session showing:

- the working directory
- which model is running
- how much of the context window is used
- your 5-hour and 7-day rate-limit usage

> macOS / Linux only — it relies on `bash` and `jq`. Windows sessions use Claude Code's default status line.

### Slash commands

These are skills you can invoke mid-session by typing `/command-name`:

| Command | What it does |
|---|---|
| `/myinit` | Reads the current project and writes a `CLAUDE.md` encoding its architecture, conventions, and entry points |
| `/context_migration` | Produces a structured handoff document so you can resume seamlessly when the context window fills up |
| `/export-api` | Writes a structured API reference file for the current project, suitable for use by another project or agent |
| `/import-api` | Loads an external project's API reference and uses it to inform an implementation task in the current project |
| `/resume-skills` | Scans the codebase and outputs a resume-oriented skills summary of the technologies and competencies in the code |
| `/create-worktree-context` | Scans every worktree of the current repo and writes a shared `WORKTREE_CONTEXT.md` — project architecture, branch map, divergence notes — at the git common directory |
| `/compare-branches` | Reads `WORKTREE_CONTEXT.md` and compares branches for a specific task, then recommends where new work should land or flags that it already exists |

#### Worktree workflow

`/create-worktree-context` and `/compare-branches` work as a pair. If you keep several long-lived worktrees (e.g. `master`, `development`, a few feature branches), run `/create-worktree-context` once to produce a shared snapshot at the git common directory. After that, `/compare-branches` can answer "where should this new feature go?" or "does this already exist somewhere?" without re-scanning the repo each time. The snapshot can be refreshed on demand — the "Open Items Across Branches" section is preserved across refreshes so your running notes are not overwritten.

---

## Customise it

Two files are worth knowing about:

- **`CLAUDE.md`** — edit this to change the standing instructions Claude receives. Add your own principles, remove ones that don't fit your workflow.
- **`settings.json`** — controls the model, status line, spinner messages, effort level, theme, and enabled plugins.

On macOS / Linux everything is installed as a live symlink back to this repo, so edits take effect in your next Claude Code session — no reinstall needed. On Windows the files are copied, so re-run `install.ps1 -Force` after editing.

---

## Requirements

- [Claude Code CLI](https://claude.ai/code)
- macOS / Linux: `bash` and `jq` (for the status line)
- Windows: PowerShell 5+ (the status line is not installed on Windows)
