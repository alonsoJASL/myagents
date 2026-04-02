Analyze this codebase and generate a resume-oriented skills summary aimed at
an LLM reviewer. The output should make clear what technical skills, domains,
and competencies a developer would demonstrate by having built this project.

## What to produce

A concise, structured summary with two sections:

### Technical Skills
List concrete technologies, languages, frameworks, libraries, and tools that
are directly evidenced in the code. Only include what is actually present --
no inferences or wishful additions.

### Engineering Competencies
Describe the non-trivial design decisions, architectural patterns, or problem
domains that the project demonstrates. For example: "designs event-driven
pipelines", "integrates third-party APIs with explicit auth flows",
"applies dependency injection across service boundaries". Keep each point
specific to what the code actually shows.

## Constraints

- Ground every claim in something observable in the repo (file, module, pattern)
- Do not pad with generic buzzwords (e.g. "strong communication skills")
- Do not include skills implied only by the language itself (e.g. "knows how
  to write functions" is not a skill)
- Prefer short, noun-phrase bullets over full sentences
- Keep the total output under 60 lines
- Output plain text, no emojis
