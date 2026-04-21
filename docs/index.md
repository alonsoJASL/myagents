---
layout: home
title: myagents
---

**myagents** is a personal configuration set for [Claude Code](https://claude.ai/code), the AI coding assistant that runs in your terminal. It wires up a custom developer manifest, a compact status line, and a handful of slash commands that make sessions faster and more structured.

---

## Quick install

You need [Claude Code](https://claude.ai/code) and `git`. That's it.

> Works on macs and linux. Windows install coming sometime later.

```bash
git clone https://github.com/alonsoJASL/myagents
cd myagents

./install.sh # This is optional, if you know how to symlink you can just do that
```

The script handles all the plumbing. Once it finishes, open a new Claude Code session and everything is active.

---

## What you get

### José's Developer manifest

`CLAUDE.md` is a set of José's standing instructions that Claude reads at the start of every session. It encodes architectural principles, for example things like "separate orchestration from logic", "no singletons or globals", "wait for the Rule of Three before abstracting". That way you never have to re-explain these coding standards to the model.

### Status line

`statusline.sh` adds a live info bar to every Claude Code session showing:

- which model is running
- how much of the context window is used (with a visual bar)
- token counts and estimated cost
- elapsed session time

> This one sometimes does not work.

### Slash commands

These are skills you can invoke mid-session by typing `/command-name`:

| Command | What it does |
|---|---|
| `/myinit` | Reads the current project and writes a `CLAUDE.md` encoding its architecture, conventions, and entry points |
| `/context_migration` | Produces a structured handoff document so you can resume seamlessly when the context window fills up |
| `/export-api` | Writes a structured API reference file for the current project, suitable for use by another project or agent |
| `/import-api` | Loads an external project's API reference and uses it to inform an implementation task in the current project |
| `/resume-skills` | Scans the codebase and outputs a resume-oriented skills summary of the technologies and competencies in the code |

---

## Customise it

Two files are worth knowing about:

- **`CLAUDE.md`** — edit this to change the standing instructions Claude receives. Add your own principles, remove ones that don't fit your workflow.
- **`settings.json`** — controls the status line, spinner messages, effort level, and enabled plugins. 

Because everything is installed as a live link back to this repo, any edits you make here take effect immediately in the next Claude Code session, so no reinstall needed.

---

## Requirements

- [Claude Code CLI](https://claude.ai/code)
- `bash` and `jq` (for the status line)
