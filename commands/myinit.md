Analyze this codebase and generate a project-level CLAUDE.md file.

Before generating the CLAUDE.md, check if `.claude/last_migration.md` 
exists. If it does, read it and incorporate the Project State and Open 
Threads sections into the generated CLAUDE.md under a ## Session Context 
section. Then delete or archive the file to avoid stale context on 
subsequent inits.

## What to include

- Build, test, lint, and run commands, especially any non-obvious flags or 
  arguments specific to this project
- High-level architecture: key directories, what each does, and how they relate
- Domain-specific terminology or entity names that are not self-evident from 
  the code
- Non-obvious gotchas: known workarounds, fragile areas, or constraints future 
  contributors would not discover quickly
- Any project-specific tooling or scripts that should be used instead of 
  standard alternatives

## What to exclude

- Anything already covered in ~/.claude/CLAUDE.md (personal coding practices, 
  architecture principles, environment injection rules, abstraction discipline)
- Generic development advice Claude already knows
- File structure that is obvious from inspection
- Code style rules that can be enforced by a linter

## Constraints

- Keep it under 100 lines
- No emojis
- If a CLAUDE.md already exists, review and improve it rather than replacing it